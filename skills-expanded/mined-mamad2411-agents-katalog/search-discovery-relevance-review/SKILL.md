---
name: search-discovery-relevance-review
description: Design and audit product search, marketplace discovery, recommendation surfaces, filters, facets, relevance signals, zero-results, query understanding, ranking drift, result quality evals, fairness, sponsored placement boundaries, and feedback loops. Use when users need to find content, products, creators, docs, apps, skills, or inventory quickly and trust the results.
---

# Search Discovery Relevance Review

Use this skill to convert a search, discovery, relevance quality, filters, ranking drift, zero-results, and user trust question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify searchable corpus, user intents, query types, ranking surfaces, business incentives, cold-start items, and harm from bad relevance.
2. Read `references/search-discovery-relevance-patterns.md`.
3. Separate retrieval, filtering, ranking, personalization, editorial curation, sponsored placement, and moderation eligibility.
4. Define quality evals, query logs, zero-result recovery, feedback signals, fairness checks, ranking-change rollout, and support/debug tools.
5. Produce relevance audit, state machine, decision table, event schema, eval set, and launch checklist.

## Guardrails

- Do not mix paid placement, editorial quality, eligibility, and organic ranking without labels and governance.
- Do not optimize clicks alone when long-term satisfaction, retained value, or abuse matters.
- Do not hide zero-result or low-confidence states behind random filler results.
- Do not personalize sensitive categories without privacy, fairness, and user control review.

## Output format

```text
Discovery context:
Corpus / intent / ranking surface / trust risk:

Relevance improvement plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Signals and evals:
- <item> -> <policy, metric, edge case, support note>

Ranking rollout and recovery:
- <trigger> -> <action, communication, owner>
```
