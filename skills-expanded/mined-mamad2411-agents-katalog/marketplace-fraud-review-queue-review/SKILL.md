---
name: marketplace-fraud-review-queue-review
description: Design and audit marketplace fraud review queues across risk signals, seller/buyer behavior, payout holds, refund abuse, fake reviews, account takeover, collusion, chargebacks, listing scams, reviewer workflows, evidence packages, SLAs, queue prioritization, decision QA, appeals, fairness monitoring, and policy feedback. Use when marketplace trust decisions need consistent human review and measurable outcomes.
---

# Marketplace Fraud Review Queue Review

Use this skill to convert marketplace fraud review queue, trust queue, payout hold review, refund abuse, fake review, account takeover, collusion, and reviewer QA questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify fraud surface, signal source, queue priority, entity type, financial exposure, customer harm, evidence, reviewer role, SLA, appeal path, and fairness segment.
2. Read `references/marketplace-fraud-review-queue-patterns.md`.
3. Classify the situation as payout-risk review, refund-abuse review, fake-review review, account-takeover review, seller scam review, buyer abuse review, collusion review, chargeback review, or manual escalation.
4. Define risk tiers, queue routing, evidence requirements, reviewer decisions, temporary actions, QA sampling, appeal path, metrics, and policy/model feedback loop.
5. Produce fraud queue governance plan, state machine, decision table, event schema, reviewer checklist, QA plan, and appeal/fairness monitoring.

## Guardrails

- Do not expose fraud model features, abuse thresholds, or reviewer private notes in user-facing messages.
- Do not let high-revenue sellers or buyers bypass the evidence standard.
- Do not use automated risk scores as final decisions without human review where stakes are high.
- Do not optimize loss rate while ignoring false positives, appeal overturns, seller churn, or buyer harm.

## Output format

```text
Marketplace fraud queue context:
Audience / source of truth / risk boundary:

Fraud review queue plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Signals, priority, evidence, reviewer action, QA, appeal, fairness, and policy feedback:
- <trigger> -> <policy, metric, edge case, support note>
```
