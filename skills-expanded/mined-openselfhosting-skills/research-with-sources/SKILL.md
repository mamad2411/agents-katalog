---
name: research-with-sources
description: "Produces a source-backed answer to a research question by defining scope, finding authoritative and current evidence, checking corroboration, and separating facts from inference. Use when accuracy, traceability, or changing information matters."
license: MIT
metadata:
  author: OpenSelfHosting
  version: "1.0.0"
---

# Research With Sources

## Goal
Answer a defined question with verifiable evidence, transparent uncertainty, and sources appropriate to the claim.

## Workflow
1. Rewrite the question as a decision or set of subquestions. Identify geography, timeframe, audience, and what would make the answer useful.
2. Determine freshness requirements. For laws, product features, prices, public figures, schedules, software versions, or active events, prioritize current sources and record publication/update dates.
3. Search primary sources first when possible: official documentation, specifications, filings, research papers, datasets, release notes, or the directly responsible organization. Use independent secondary sources to contextualize or corroborate.
4. Evaluate each source for authority, date, methodology, conflicts of interest, scope, and direct support for the exact claim. Do not treat search snippets or summaries as proof when the underlying source is accessible.
5. Cross-check material claims with another independent source where practical. If reliable sources conflict, explain the disagreement and why one source may be more applicable.
6. Track claim → source relationships. Keep quotations short and distinguish direct quotations, paraphrases, calculations, and your own inference.
7. Avoid false precision. Label estimates, assumptions, missing data, and limits of comparability. Do not extrapolate beyond a source's population or timeframe without saying so.
8. Build the answer around the decision: findings first, then evidence, implications, uncertainty, and next steps. Cite claims close to the evidence that supports them.
9. Review whether any important conclusion rests on only one weak or stale source. Search again if the gap could materially change the answer.

## Output format
- Direct answer or main findings.
- Evidence with source names, dates, and links/citations.
- Important comparisons or assumptions.
- Conflicts, limitations, and confidence.
- What would change the conclusion, if relevant.

## Guardrails
Do not invent citations, page titles, authors, dates, studies, or data. Do not present sponsored content as independent evidence. Do not quote large copyrighted passages when a summary is sufficient. For high-stakes medical, legal, safety, or financial decisions, communicate limitations and direct the reader to qualified/official sources as appropriate.
