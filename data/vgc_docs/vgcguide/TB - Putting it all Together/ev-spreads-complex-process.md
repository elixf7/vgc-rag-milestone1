> Source era: 2016 Worlds (restricted/Primal-era format). Strategic reference only — defer to the current-format source for legality and live meta.

## Complex EV Spreads — Process Overview

Building a complex EV spread is an iterative process, not a one-pass calculation. Begin with a simple or recycled spread, identify what the Pokémon needs through practice, and refine toward specific benchmarks over time. A complex spread is only as good as its context — the scenarios it targets must actually occur in the games you play, and the spread must fit the team it's built for.

The three-step process below applies to any Pokémon in any format:
1. Lock in non-negotiables (what the Pokémon must always accomplish).
2. Decide on a Speed target.
3. Distribute remaining EVs toward secondary goals.

## Complex EV Spreads — Step 1: Non-Negotiables

Before touching a damage calculator, identify what the Pokémon must always be able to do. These are the benchmarks you will not compromise on.

- **For offensive Pokémon**: the attacks that must land at a guaranteed threshold (e.g. always securing a 2HKO on a key target, or always landing a knockout after a specific condition), and/or the Speed floor below which the Pokémon stops functioning.
- **For defensive Pokémon**: the hits that must always be survived, regardless of other concessions.

The difficulty of this step is not mechanical — it is identifying *which* benchmarks are actually worth building around. This judgment improves with metagame experience. Focus on the Pokémon your team will realistically face, and ask which knockouts and survivals actually decide games. Avoid building benchmarks around scenarios that are unlikely to occur or that the Pokémon wouldn't be brought into.

## Complex EV Spreads — Step 2: Choosing a Speed Target

After non-negotiables, set the Speed stat. Speed is not a dial — it is a discrete decision that determines the order of play.

Questions to work through:
- Are there Pokémon this Pokémon needs to outpace to function, even partially?
- Is there a relevant speed mirror (same species or same speed tier) where moving first decides the outcome?
- How many EVs does reaching the target cost, and does that cost leave enough room for the other benchmarks?

If no clear target emerges, start with a tentative value and adjust after practice. Outrunning a Pokémon only matters if there is something meaningful to do against it — if the usual line is to switch out or use a non-speed-dependent move, the investment may not be worth it.

Practical note: in **Trick Room**, the Speed target becomes a ceiling rather than a floor. Minimize Speed to maximize how often the Pokémon moves first under reversed priority.

## Complex EV Spreads — Step 3: Rounding Out the Spread

With a Speed target and non-negotiable benchmarks set, distribute remaining EVs toward secondary goals. This step is usually driven by practice — unexpected knockouts or failures to secure a KO in games reveal what the spread is missing.

When evaluating a secondary benchmark:
- Open a damage calculator and find how many EVs the threshold requires.
- Weigh that cost against what those EVs could do elsewhere (opportunity cost).
- A benchmark that requires heavy investment for a scenario that rarely occurs may not be worth pursuing.

The spread should eventually be stable enough to remember during a live game. Benchmarks you cannot recall under pressure provide no value.

## Complex EV Spreads — Efficiency and Redistribution

When a benchmark can be met in multiple ways (e.g. by splitting EVs between HP and Defense rather than stacking one stat), explore the alternatives — a different distribution may achieve the same threshold while freeing EVs for other use.

Key mechanics to exploit:
- **Stat points are discrete**: not every EV change shifts the damage roll. Step down investment one point at a time and verify each change in the calculator before locking in a value.
- **HP and defense trade off**: adding HP while reducing a defensive stat can preserve a survival threshold at a lower total EV cost, leaving more EVs available for other stats.
- **HP-dependent effects**: **Life Orb** recoil, **Grassy Terrain** recovery, **Sandstorm** chip, and similar effects scale off HP. If these are relevant to the team, adjust the HP stat so the last digit minimizes damage or maximizes recovery as needed (Life Orb prefers a higher final digit; passive damage like Sandstorm prefers a lower one).

## Complex EV Spreads — Natures and Stat Prioritization

A nature provides the most value when it raises the highest stat after EV investment — the multiplier acts on a larger number. If no specific benchmark requires a particular stat boosted, default to raising the highest stat.

**Diminishing marginal returns** are real but often misapplied. Adding EVs to a low stat produces a larger *proportional* change and a more visible impact in the damage formula — the same number of EVs changes a weak stat by a larger fraction than a strong one. This does not mean always investing in the lowest stat; it means being aware that a small investment in a weak stat can sometimes cover a benchmark that a large investment in a strong stat cannot.

## Complex EV Spreads — Spreading Remaining EVs

After all benchmarks are met, leftover EVs (often 4–16) can be used to:
- **Increase Speed** to win relevant speed ties or creep another Pokémon that invested similarly.
- **Push toward a stretch-goal benchmark** that was just out of reach.
- **Add general HP bulk** for resilience across varied matchups.
- **Add to the attacking stat** for specific offensive thresholds (e.g. breaking a **Substitute** or securing a knockout on a target with specific defensive investment).

The correct choice depends on the team's needs and what threats the leftover EVs can realistically address.

## Complex EV Spreads — EV Mechanics Reference

Technical rules that apply to all spread construction:

- Always invest in an **odd number of stats** (3 or 5). Investing in 2, 4, or 6 stats wastes EVs at level 50.
- All EV values should follow the sequence 4, 12, 20, 28 … 244, 252 (multiples of 8, offset by 4). Values outside this sequence waste stat points at level 50.
- The first 4 EVs in a stat grant one stat point; after that, 8 EVs are required per point. For this reason, a 252 / 244 / 4 / 4 / 4 distribution yields one more stat point than 252 / 252 / 4. Avoid pulling those 8 EVs from Speed.
- A **neutral nature** (no stat raised or lowered) is never mathematically optimal — always choose a nature that raises something meaningful.
- Not every EV change alters the relevant damage roll. Always confirm that a stat point actually shifts the calc before locking in a value.

## Complex EV Spreads — Raichu Case Study (2016 Worlds, Restricted Format)

This example illustrates the full process using a supportive **Raichu** built for a restricted doubles format. The Pokémon-specific context is era-specific, but the decision-making structure applies universally.

**Role**: Supportive attacker using **Fake Out**, **Nuzzle**, **Volt Switch**, and **Endeavor**. The team relied on Raichu to chip key restricted threats to low HP via **Endeavor** after surviving a big hit — lower HP on Raichu made **Endeavor** more threatening, creating an incentive to keep HP investment as low as viable.

**Step 1 — Non-negotiables:**
- Survive a strong physical Normal-type hit from a top threat after **Intimidate** drop (defense benchmark).
- Survive a strong special Water-type spread move from a dominant rain attacker (special defense benchmark).
- Keep HP low beyond the survival floor to maximize **Endeavor** damage.

**Step 2 — Speed:**
- Determined the minimum Speed to outpace the most relevant threat (a Pokémon with 100 base Speed). Settled on the smallest Speed investment that cleared that threshold, reserving EVs for bulk.

**Step 3 — Rounding out:**
- After setting Speed, the remaining EVs were allocated to Defense first (to survive the physical benchmark), then redistributed between HP and Defense to find the most EV-efficient combination that still met the threshold.
- Special Defense was added in the smallest amount needed to survive the special benchmark reliably.
- Leftover EVs went to Attack to reach a specific offensive threshold (breaking a common **Substitute** user that threatened the team).

**Key takeaway from this case study**: the final spread was not the only acceptable solution — alternative spreads with slightly higher Speed, Defense, or Special Defense were equally valid depending on which secondary goal was prioritized. The spread reflects the team's specific matchup priorities, not a universal optimum for the Pokémon.
