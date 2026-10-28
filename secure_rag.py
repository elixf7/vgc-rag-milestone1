"""Security-hardened Self-RAG for DATA 790 Milestone 2.

Wraps the Milestone 1 pipeline (rag_system.py) with the Lab 9 defense layers (security.py).
rag_system.py is left unchanged so Milestone 1 still runs on its own.
"""

# imports
import time
from pathlib import Path

from langchain_community.callbacks import get_openai_callback
from langchain_core.documents import Document
from openai import BadRequestError

import rag_system as rag
import security as sec


# ---------------------------------------------------------------------------
# Index: the Milestone 1 guides plus the planted (poisoned) documents
# ---------------------------------------------------------------------------

PLANTED_DIR = Path(__file__).parent / "data" / "planted"


def load_planted_documents():
    """Load the planted attack documents, used to test indirect prompt injection."""
    documents = []
    for path in sorted(PLANTED_DIR.glob("*.md")):
        # source starts with "planted/" so it is easy to tell when one gets retrieved
        documents.append(Document(page_content=path.read_text(encoding="utf-8"),
                                  metadata={"source": f"planted/{path.name}"}))
    return documents


def build_index(name="milestone2"):
    """Build the vector store: Milestone 1 guides chunked the same way, plus the planted docs."""
    # Same "small" chunking strategy that won in Milestone 1
    chunks = rag.chunk_documents(rag.load_documents(), chunk_size=300, chunk_overlap=30)
    vectorstore = rag.build_vectorstore(chunks, name)
    # Planted docs go in whole (not chunked) so each hidden instruction stays in one piece
    vectorstore.add_documents(load_planted_documents())
    return vectorstore


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

# Both versions carry the canary so a system prompt leak can be detected in either run
UNDEFENDED_PROMPT = rag.SYSTEM_PROMPT + "\n" + sec.CANARY_LINE
# Prompt hardening: tell the model retrieved text is data, not instructions
DEFENDED_PROMPT = UNDEFENDED_PROMPT + "\n" + sec.HARDENING_NOTE

BLOCK_MESSAGE = "I can only help with Pokemon VGC strategy questions."

# Output token caps stop one request from running up the bill (OWASP LLM10 unbounded consumption)
MAX_ANSWER_TOKENS = 300  # the prompt asks for under 150 words, so 300 tokens is plenty
answer_llm = rag.llm.bind(max_tokens=MAX_ANSWER_TOKENS)
classifier_llm = rag.llm.bind(max_tokens=5)  # the classifier only needs one word


def generate_answer(question, docs, defended):
    """Same as rag.generate_answer, but the defended version is hardened and capped."""
    # Chunks go inside <context> tags, a clear delimiter between data and the question
    context = "\n\n".join(doc.page_content for doc in docs)
    system_prompt = DEFENDED_PROMPT if defended else UNDEFENDED_PROMPT
    messages = [
        ("system", system_prompt),
        ("human", f"<context>\n{context}\n</context>\n\nQuestion: {question}"),
    ]
    llm = answer_llm if defended else rag.llm
    return llm.invoke(messages).content


# ---------------------------------------------------------------------------
# Self-RAG with the defense layers
# ---------------------------------------------------------------------------

def secure_self_rag(question, vectorstore, defended=True):
    """Milestone 1 Self-RAG with the 4 Lab 9 layers, input cleaning, and input PII redaction around it.

    defended=False runs the same pipeline with no layers, which is the "before" for attacks.
    Returns the answer, the chunks used, and caught_by (every layer that acted).
    """
    caught = []

    if defended:
        # Input sanitization: undo disguises like zero-width spaces and look-alike letters
        question = sec.clean_input(question)

        # Layer 1: input pattern check and length cap (free, runs before any API call)
        is_safe, reason = sec.check_input(question)
        if not is_safe:
            caught.append("input pattern")
            return {"answer": BLOCK_MESSAGE, "docs": [], "caught_by": ", ".join(caught)}

        # Input PII redaction: the user's personal info never reaches the model or the gateway
        question, pii_count = sec.redact_pii(question)
        if pii_count:
            caught.append("input PII redacted")

        # Layer 2: LLM classifier (one extra call, catches reworded attacks)
        if not sec.classify_input(question, classifier_llm):
            caught.append("LLM classifier")
            return {"answer": BLOCK_MESSAGE, "docs": [], "caught_by": ", ".join(caught)}

    docs = vectorstore.similarity_search(question, k=rag.TOP_K)

    if defended:
        # Layer 3: sanitize retrieved chunks, since layers 1 and 2 only read the question
        clean_docs = [Document(page_content=sec.sanitize_chunk(doc.page_content), metadata=doc.metadata)
                      for doc in docs]
        if [d.page_content for d in clean_docs] != [d.page_content for d in docs]:
            caught.append("sanitizer")
        docs = clean_docs

    # Self-RAG step 1 (from Milestone 1): keep only the chunks that help answer the question
    relevant = []
    for doc in docs:
        if rag.ask_yes_no(f"Question: {question}\n\nPassage:\n{doc.page_content}\n\n"
                          "Does this passage help answer the question? Reply with only yes or no."):
            relevant.append(doc)
    if not relevant:
        caught.append("self-rag refusal")
        return {"answer": rag.REFUSAL, "docs": [], "caught_by": ", ".join(caught)}

    answer = generate_answer(question, relevant, defended)

    # Self-RAG step 2 (from Milestone 1): refuse if the answer is not supported by the chunks
    if answer != rag.REFUSAL:
        context = "\n\n".join(doc.page_content for doc in relevant)
        if not rag.ask_yes_no(f"Passages:\n{context}\n\nAnswer:\n{answer}\n\n"
                              "Is every claim in the answer supported by the passages? "
                              "Reply with only yes or no."):
            answer = rag.REFUSAL
            caught.append("self-rag refusal")

    if defended:
        # Layer 4: output filter (canary, override phrases) and PII redaction
        answer, action = sec.filter_output(answer)
        if action != "pass":
            caught.append(f"output filter ({action})")

    return {"answer": answer, "docs": relevant, "caught_by": ", ".join(caught) or "none"}


# ---------------------------------------------------------------------------
# Run one question and record time, cost, and gateway blocks
# ---------------------------------------------------------------------------

def run_question(question, vectorstore, defended=True):
    """Run one question and add seconds and cost to the result.

    The UNC gateway has its own content filter. A block raises a 400 BadRequestError,
    which is recorded as a result (caught_by "gateway") instead of crashing.
    """
    price = rag.PRICE_PER_1K[rag.CHAT_MODEL]
    start = time.perf_counter()
    try:
        with get_openai_callback() as cb:  # counts the tokens of every chat call inside
            result = secure_self_rag(question, vectorstore, defended)
        # Input and output tokens are priced differently
        result["cost"] = (cb.prompt_tokens / 1000 * price["input"]
                          + cb.completion_tokens / 1000 * price["output"])
    except BadRequestError as e:
        if not sec.is_gateway_block(e):
            raise  # a real error, not the content filter
        result = {"answer": "[blocked by the gateway content filter]", "docs": [],
                  "caught_by": "gateway", "cost": 0.0}
    result["seconds"] = time.perf_counter() - start
    return result
