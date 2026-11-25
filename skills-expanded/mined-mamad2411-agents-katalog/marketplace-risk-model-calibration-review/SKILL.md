---
name: marketplace-risk-model-calibration-review
description: Design and audit marketplace risk model calibration for fraud, trust, abuse, quality, payout, listing, buyer, and seller risk covering labels, ground truth, thresholds, reviewer queues, false positives, false negatives, fairness, drift, appeals, policy feedback, model monitoring, and business guardrails. Use when risk scores influence marketplace actions or review priority.
---

# Marketplace Risk Model Calibration Review

Use this skill to convert marketplace risk model, fraud score, trust score, abuse classifier, quality risk, payout risk, listing risk, queue threshold, calibration, drift, appeal, and policy feedback questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify risk actions, model outputs, label sources, ground truth windows, reviewer queues, threshold decisions, protected/segment fairness, appeals, drift signals, loss functions, and business constraints.
2. Read `references/marketplace-risk-model-calibration-patterns.md`.
3. Classify the situation as new model launch, threshold retune, drift investigation, false-positive spike, false-negative loss spike, new abuse pattern, policy change, or appeals quality review.
4. Define calibration dataset, threshold policy, queue routing, human review, appeal loop, fairness checks, drift monitoring, policy feedback, and safe rollout plan.
5. Produce risk model calibration review, state machine, decision table, event schema, threshold matrix, monitoring checklist, and policy-feedback plan.

## Guardrails

- Do not make automated model scores the final decision for high-impact marketplace actions without review and appeal.
- Do not optimize only for loss reduction while ignoring false positives, creator trust, buyer harm, fairness, and market liquidity.
- Do not leak exact risk signals, thresholds, or adversarial tactics in public-facing explanations.
- Do not recalibrate thresholds without measuring downstream queue capacity and reviewer quality.

## Output format

```text
Marketplace risk model context:
Audience / source of truth / risk boundary:

Calibration and governance plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Labels, thresholds, review queues, appeals, fairness, drift, policy feedback, and monitoring:
- <trigger> -> <policy, metric, edge case, support note>
```
