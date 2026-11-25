---
name: marketplace-quality-scoring-review
description: Design and audit marketplace quality scoring for creators, sellers, listings, skills, apps, plugins, services, content, search ranking, recommendations, certification, trust badges, appeals, moderation, fraud, fairness, freshness, feedback loops, and score explainability. Use when a marketplace needs quality signals that improve discovery without unfairly burying good supply.
---

# Marketplace Quality Scoring Review

Use this skill to convert marketplace quality scoring, ranking signal, certification, fairness, appeal, and quality-feedback questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify marketplace supply type, buyer promise, quality dimensions, ranking surfaces, moderation signals, feedback sources, abuse risks, creator incentives, and fairness concerns.
2. Read `references/marketplace-quality-scoring-patterns.md`.
3. Classify score as eligibility gate, ranking signal, trust badge, certification, warning, demotion, recommendation feature, freshness signal, or manual review trigger.
4. Define scoring inputs, weights, thresholds, evidence quality, anti-gaming controls, explanations, appeal path, monitoring, and retraining/review cadence.
5. Produce quality-scoring plan, state machine, decision table, event schema, scoring checklist, and experiment guardrails.

## Guardrails

- Do not use opaque quality scores to silently punish creators/sellers without explanation or appeal.
- Do not reward engagement, volume, or revenue if it correlates with low quality, fraud, or buyer harm.
- Do not let early incumbents permanently dominate discovery without freshness and new-supply paths.
- Do not collect sensitive or biased signals without fairness, privacy, and policy review.

## Output format

```text
Marketplace scoring context:
Audience / source of truth / risk boundary:

Quality scoring plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Signals, thresholds, ranking impact, and appeals:
- <trigger> -> <policy, metric, edge case, support note>
```
