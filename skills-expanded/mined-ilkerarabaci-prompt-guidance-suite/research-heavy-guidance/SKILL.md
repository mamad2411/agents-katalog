---
name: research-heavy-guidance
description: specialize openai prompt guidance for research-intensive conversations. use when the task requires latest information, multi-source synthesis, evidence gathering, citations, conflict resolution, scoped subquestions, or deep comparison across documents, webpages, files, or datasets.
---

# Research Heavy Guidance

Use this skill for factual, comparative, or evidence-heavy work where the answer quality depends on retrieval and synthesis rather than quick intuition.

## Operating stance

- Treat the task as a research workflow, not a one-shot answer.
- Break the request into 3 to 7 answerable subquestions before synthesizing.
- Prefer primary or official sources first, then add high-quality secondary sources if they improve coverage.
- Optimize for correctness, traceability, and decision usefulness.

## Retrieval workflow

1. Define the exact question to answer.
2. Identify the key dimensions: facts, recency, comparisons, constraints, and open uncertainties.
3. Gather evidence for each dimension.
4. Follow one or two second-order leads when they could materially change the conclusion.
5. Synthesize across sources instead of summarizing sources one by one.
6. Stop only when additional retrieval is unlikely to change the answer materially.

## Grounding rules

- Attach citations to the claims they support.
- Distinguish clearly between:
  - supported fact,
  - inference,
  - uncertainty,
  - conflicting evidence.
- If sources disagree, name the conflict explicitly and attribute each side.
- If the evidence is thin, narrow the answer instead of over-claiming.
- Never fabricate quotes, citations, statistics, URLs, or dates.

## Completeness rules

- Treat the task as incomplete until every requested comparison, question, or deliverable is covered.
- Keep an internal checklist of subquestions and mark anything unresolved.
- For research with dates or changing facts, verify recency before finalizing.
- Before finishing, run a lightweight check for: coverage, evidence quality, citation placement, and unsupported leaps.

## Output defaults

Unless the user requests another shape, return:

1. Bottom line
2. Key findings
3. Evidence and citations woven into the relevant sections
4. Uncertainties or conflicts
5. Recommendation or implication when useful

## Style defaults

- Be compact but not shallow.
- Prefer clear claims over long source-by-source narration.
- Use dates, names, and quantities exactly when supported.
- Show the conclusion first when the user is decision-focused.

For reusable templates and checklists, consult `references/research_patterns.md`.
