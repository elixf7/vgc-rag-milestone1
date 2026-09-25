"""VGC strategy RAG system for DATA 790 Milestone 1.
"""

# imports
import json
import logging
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.callbacks import get_openai_callback
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

# Read the API key from the .env
load_dotenv()

# Change logging to critical
logging.getLogger("chromadb.telemetry.product.posthog").setLevel(logging.CRITICAL)

# UNC gateway setup
UNC_AI_BASE_URL = "https://azureaiapi.cloud.unc.edu/openai/v1"
UNC_AI_API_KEY = os.getenv("UNC_AI_API_KEY")
assert UNC_AI_API_KEY, "Missing UNC_AI_API_KEY in .env"

CHAT_MODEL = "gpt-4.1-mini"
EMBED_MODEL = "text-embedding-3-small"
TOP_K = 5  # chunks retrieved per question

# Prices per 1K tokens
PRICE_PER_1K = {
    "gpt-4.1-mini": {"input": 0.0004, "output": 0.0016},
    "text-embedding-3-small": {"input": 0.00002},
}

DATA_DIR = Path(__file__).parent / "data" / "vgc_docs"

# The embedding model turns a piece of text into a list of 1536 numbers
# Text with similar meaning ends up with similar vectors, which is what makes search work.
embeddings = OpenAIEmbeddings(model=EMBED_MODEL, base_url=UNC_AI_BASE_URL, api_key=UNC_AI_API_KEY)

# temperature=0 so the answers are as repeatable as possible
llm = ChatOpenAI(model=CHAT_MODEL, base_url=UNC_AI_BASE_URL, api_key=UNC_AI_API_KEY, temperature=0)


# ---------------------------------------------------------------------------
# Ingestion, chunking, and embedding
# ---------------------------------------------------------------------------

def load_documents():
    """Load every markdown guide as a Document, with its file path saved."""
    documents = []
    # rglob looks through every subfolder, so guides in nested folders get picked up too
    for path in sorted(DATA_DIR.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        # Keep track of which guide the text came from
        source = str(path.relative_to(DATA_DIR))
        documents.append(Document(page_content=text, metadata={"source": source}))
    return documents


def chunk_documents(documents, chunk_size, chunk_overlap):
    """Split the documents into chunks."""
    # The splitter tries these separators in order: paragraphs first, then lines, then
    # sentences, then words. 
    # That way a chunk only gets cut mid-sentence as a last resort
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(documents)


def build_vectorstore(chunks, name):
    """Embed the chunks into a Chroma collection that uses cosine distance.
    """
    Chroma(collection_name=name, embedding_function=embeddings).delete_collection()
    # from_documents embeds every chunk and stores the vectors. 
    # Cosine distance compares the direction of two vectors, which shows similarity
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=name,
        collection_metadata={"hnsw:space": "cosine"},
    )


# ---------------------------------------------------------------------------
# Security: input validation
# ---------------------------------------------------------------------------

MAX_QUESTION_LENGTH = 500

# Phrases used in common injection attempts
BLOCKED_PHRASES = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "ignore the above",
    "system prompt",
    "you are now",
    "jailbreak",
]


def validate_input(question):
    """Check a question before it is sent to the model. Returns (is_safe, message)."""
    # These checks run before any API call so they cost nothing
    if not question.strip():
        return False, "Blocked: empty question"
    # A length cap stops someone from pasting in a huge block of text
    if len(question) > MAX_QUESTION_LENGTH:
        return False, f"Blocked: question longer than {MAX_QUESTION_LENGTH} characters"
    # Prompt injection: the user tries to talk the model out of its instructions.
    # lower() so "IGNORE PREVIOUS INSTRUCTIONS" gets caught too.
    for phrase in BLOCKED_PHRASES:
        if phrase in question.lower():
            return False, "Blocked: possible prompt injection"
    return True, "OK"


# ---------------------------------------------------------------------------
# Self-RAG
# ---------------------------------------------------------------------------

# The model is told to answer only from the retrieved text and to say it doesn't know otherwise
SYSTEM_PROMPT = """You are a VGC (Pokemon doubles) strategy assistant.
Answer the question using ONLY the reference passages inside the <context> tags.
If the passages do not contain the answer, reply exactly: I don't know based on the provided documents.
Keep the answer under 150 words."""

REFUSAL = "I don't know based on the provided documents."


def generate_answer(question, docs):
    """Answer the question from the given chunks."""
    # paste all the chunks into one prompt.
    context = "\n\n".join(doc.page_content for doc in docs)
    messages = [
        ("system", SYSTEM_PROMPT),
        ("human", f"<context>\n{context}\n</context>\n\nQuestion: {question}"),
    ]
    return llm.invoke(messages).content


def ask_yes_no(prompt):
    """Ask the model a yes or no question and return True for yes."""
    reply = llm.invoke(prompt).content
    return reply.strip().lower().startswith("yes")


def self_rag(question, vectorstore):
    """Self-RAG: retrieve, keep only the relevant chunks, answer, then check the answer.

    If no chunk is relevant, or the answer is not supported by the chunks, refuse to answer.
    """
    is_safe, message = validate_input(question)
    if not is_safe:
        return {"answer": message, "docs": []}

    # Eembed the question and grab the 5 chunks whose vectors are closest to it
    docs = vectorstore.similarity_search(question, k=TOP_K)

    # Grade each retrieved chunk and keep the ones that help answer the question.
    relevant = []
    for doc in docs:
        if ask_yes_no(f"Question: {question}\n\nPassage:\n{doc.page_content}\n\n"
                      "Does this passage help answer the question? Reply with only yes or no."):
            relevant.append(doc)
    if not relevant:
        return {"answer": REFUSAL, "docs": []}

    # Answer from the relevant chunks only
    answer = generate_answer(question, relevant)

    # Check that the answer is supported by those chunks.
    if answer != REFUSAL:
        context = "\n\n".join(doc.page_content for doc in relevant)
        if not ask_yes_no(f"Passages:\n{context}\n\nAnswer:\n{answer}\n\n"
                          "Is every claim in the answer supported by the passages? "
                          "Reply with only yes or no."):
            answer = REFUSAL

    return {"answer": answer, "docs": relevant}


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

def load_golden_set():
    """20 in-scope questions with the guides that answer them, and 5 out-of-scope questions."""
    # The golden set is the answer key: questions I wrote where I already know
    # which guide should come back.
    data = json.loads((Path(__file__).parent / "golden_set.json").read_text())
    return data["in_scope"], data["out_of_scope"]


def retrieval_metrics(vectorstore, in_scope):
    """Hit rate and average characters retrieved.

    A question is a hit if any of the top k chunks came from one of its expected guides.
    """
    hits = 0
    total_chars = 0
    for item in in_scope:
        docs = vectorstore.similarity_search(item["question"], k=TOP_K)
        # More characters means more text in the prompt, which means more cost.
        total_chars += sum(len(doc.page_content) for doc in docs)
        # Hit rate only looks at retrieval
        if any(doc.metadata["source"] in item["sources"] for doc in docs):
            hits += 1
    return {"hit_rate": hits / len(in_scope), "avg_chars": total_chars / len(in_scope)}


def evaluate_self_rag(vectorstore, in_scope, out_of_scope):
    """Run Self-RAG on every question and measure accuracy, time, and cost.

    answered rate: in-scope questions that got a real answer
    refusal rate:  out-of-scope questions that were correctly refused
    """
    price = PRICE_PER_1K[CHAT_MODEL]
    answered = 0
    refused = 0
    total_seconds = 0
    total_cost = 0

    all_questions = [item["question"] for item in in_scope] + out_of_scope
    for question in all_questions:
        start = time.perf_counter()
        with get_openai_callback() as cb:  # counts tokens
            result = self_rag(question, vectorstore)
        total_seconds += time.perf_counter() - start
        # Input and output tokens are priced differently
        total_cost += (cb.prompt_tokens / 1000 * price["input"]
                       + cb.completion_tokens / 1000 * price["output"])

        # In-scope questions should get a real answer. 
        # Out-of-scope ones should get the refusal
        if question in out_of_scope:
            refused += result["answer"] == REFUSAL
        else:
            answered += result["answer"] != REFUSAL

    return {
        "answered rate": answered / len(in_scope),
        "refusal rate": refused / len(out_of_scope),
        "avg seconds": total_seconds / len(all_questions),
        "avg cost": total_cost / len(all_questions),
    }
