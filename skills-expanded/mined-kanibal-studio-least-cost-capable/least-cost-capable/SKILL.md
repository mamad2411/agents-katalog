---
name: least-cost-capable
description: Compare declared relative cost ranks among catalogued agent models after checking task capability, availability, authorization, workload, and cost evidence.
---

# Least-cost capable model selection

Compare candidates in the user's supplied catalogue. This is a decision aid based only on supplied facts; it does not establish the completeness or truth of the catalogue, promise actual savings, call providers, spend credits, change settings, or launch agents.

1. Define the task's required capabilities from the requested work and risk. Treat capability claims as supplied evidence, not as assumptions based on model names.
2. Treat only explicit `true`/`false` availability and authorization as known. Unknown or omitted values stay unresolved. A candidate marked unavailable or unauthorized is excluded with that reason.
3. Treat a capability list as complete only when the catalogue explicitly says so. Missing or incomplete lists remain unresolved; a missing capability excludes a candidate only when its list is confirmed complete. Never infer capability from a model name.
4. Compare relative rank only when each capable candidate supplies the same metric, unit, workload, and observation window, plus a source and `as_of` date. API input-token cost and output-token cost are different metrics; currency cost, provider credits, and quota units are not interchangeable. Missing, stale per the user's own freshness requirement, or conflicting evidence remains unknown. Do not browse or invent prices to fill gaps.
5. If evidence is comparable, report the candidate with the lowest supplied rank for that declared comparison. Say that this is the catalogue's ranking, not a guarantee of real-world savings, universal cheapest status, or dispatch. If evidence is unresolved, explain what is missing. If no candidate qualifies, say only that none is established in this catalogue; do not imply no capable model exists elsewhere.
6. A higher-cost model may be selected only when the user specifies a task need or preference that the lower-ranked candidate cannot meet; state that reason. Do not turn this into a universal premium-model rule.

For a repeatable comparison, use `scripts/select_model.py` with the schema shown in `examples/catalogue.json`. Duplicate IDs are invalid. The script returns a decision only from supplied facts and preserves exclusions and unknowns in its output.

Keep the action within the user's authorization. A model choice does not authorize delegation, provider calls, spending, or changes to an account. Ask for any missing facts needed to make the comparison; otherwise report the uncertainty and continue with work that does not depend on it.
