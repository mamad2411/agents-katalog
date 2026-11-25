---
name: user-research-repository-review
description: Design and audit user research repositories that turn interviews, surveys, usability tests, support tickets, sales calls, churn reasons, app reviews, and product analytics into tagged, consent-safe, decision-linked evidence. Use when product teams need reusable insight instead of anecdote piles.
---

# User Research Repository Review

Use this skill to convert user research repository, insight taxonomy, evidence tagging, consent, synthesis, and decision-linkage questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify research sources, participant consent, data sensitivity, user segments, product decisions, taxonomy needs, repository owners, and current evidence failure modes.
2. Read `references/user-research-repository-patterns.md`.
3. Classify inputs as primary research, usability evidence, survey signal, support cluster, sales/CS note, churn reason, app review, analytics anomaly, or synthesized insight.
4. Define capture workflow, redaction, tagging, confidence scoring, insight lifecycle, decision linkage, search/browse views, and stale-evidence review.
5. Produce repository operating model, state machine, decision table, event schema, taxonomy checklist, and governance plan.

## Guardrails

- Do not store raw PII, recordings, or sensitive customer quotes without consent, access controls, and retention rules.
- Do not let loud anecdotes override sample quality, segment fit, recency, or contradictory evidence.
- Do not publish insights without separating observation, interpretation, confidence, and decision implication.
- Do not let research repositories become dead archives with no owner, decision link, or stale-evidence review.

## Output format

```text
Research repository context:
Audience / source of truth / risk boundary:

Repository operating model:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Taxonomy, confidence, and decision linkage:
- <trigger> -> <policy, metric, edge case, support note>
```
