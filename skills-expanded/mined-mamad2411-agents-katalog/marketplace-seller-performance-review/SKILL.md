---
name: marketplace-seller-performance-review
description: Design and audit marketplace seller performance systems covering fulfillment, quality, response time, refunds, disputes, cancellations, policy violations, customer satisfaction, support burden, fraud signals, ranking impact, badges, warnings, coaching, suspension, appeals, fairness, and seller lifecycle. Use when marketplaces need reliable supply incentives without unfair punishment.
---

# Marketplace Seller Performance Review

Use this skill to convert marketplace seller performance, creator quality, seller health, ranking impact, warnings, coaching, suspension, appeal, and marketplace incentive questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify seller type, category, lifecycle stage, buyer promise, performance signals, evidence quality, policy thresholds, ranking surfaces, intervention ladder, and appeal path.
2. Read `references/marketplace-seller-performance-patterns.md`.
3. Classify the situation as new seller onboarding, quality coaching, warning, ranking demotion, payout hold, badge eligibility, suspension, appeal, fraud review, or high-performing seller expansion.
4. Define performance dimensions, thresholds, confidence, explanations, interventions, appeal evidence, fairness monitoring, ranking impact, and improvement loop.
5. Produce seller performance plan, state machine, decision table, event schema, scoring checklist, intervention ladder, and fairness review.

## Guardrails

- Do not use opaque performance scores to punish sellers without explanations, evidence, and appeal.
- Do not reward volume or revenue when disputes, refunds, policy violations, or support burden show buyer harm.
- Do not let new sellers be permanently buried by cold-start data gaps.
- Do not leak fraud or abuse signals while explaining performance actions.

## Output format

```text
Seller performance context:
Audience / source of truth / risk boundary:

Seller performance plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Signals, thresholds, interventions, ranking, appeal, fairness, and improvement loop:
- <trigger> -> <policy, metric, edge case, support note>
```
