---
name: creator-ranking-quality-review
description: Design and audit creator, listing, plugin, skill, app, marketplace, content, or community ranking quality across relevance, quality signals, freshness, fairness, fraud resistance, diversity, monetization, review abuse, creator trust, and user outcomes. Use when marketplaces need discovery/ranking systems that reward quality without becoming pay-to-win or spam-prone.
---

# Creator Ranking Quality Review

Use this skill to convert a risky product, operations, trust, or marketplace question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify marketplace surface, user intent, creator incentives, ranking inventory, quality signals, abuse vectors, and business constraints.
2. Read `references/creator-ranking-quality-patterns.md`.
3. Separate retrieval, eligibility, ranking, merchandising, paid placement, review quality, and moderation actions.
4. Define quality metrics, fairness checks, creator feedback, abuse controls, and experiment/rollback plan.
5. Produce ranking scorecard, signal matrix, decision table, event schema, and governance cadence.

## Guardrails

- Do not let revenue or paid promotion silently masquerade as organic quality.
- Do not rank only by installs/downloads when this creates rich-get-richer loops or spam incentives.
- Do not expose enough ranking mechanics to enable easy gaming, but give creators actionable quality feedback.
- Ranking changes need trust, moderation, support, and creator-communication readiness.

## Output format

```text
Ranking context:
Marketplace / user intent / creator incentives:

Signal matrix:
| Signal | Purpose | Abuse risk | Weight direction | Guardrail |
| --- | --- | --- | --- | --- |

Ranking decision table:
- <scenario> -> <eligibility/ranking/merchandising/action>

Governance:
- <metric, review cadence, creator/support comms>
```
