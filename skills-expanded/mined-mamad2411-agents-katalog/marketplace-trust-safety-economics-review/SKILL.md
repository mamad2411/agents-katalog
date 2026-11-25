---
name: marketplace-trust-safety-economics-review
description: Design and audit marketplace trust and safety economics covering buyer/seller incentives, fraud, abuse, moderation cost, dispute handling, refunds, chargebacks, ratings, ranking incentives, creator payouts, quality gates, take rate, liquidity, supply quality, false positives, appeals, enforcement ladders, and unit economics. Use when a marketplace must grow without rewarding harmful behavior.
---

# Marketplace Trust Safety Economics Review

Use this skill to convert marketplace trust-safety economics, incentives, abuse, disputes, refunds, ranking, payout, and unit-economics questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify marketplace sides, value exchange, monetization, ranking signals, payout rules, dispute/refund paths, quality gates, abuse patterns, moderation cost, and liquidity goals.
2. Read `references/marketplace-trust-safety-economics-patterns.md`.
3. Classify risk as fraud, spam, low-quality supply, review manipulation, refund abuse, payout abuse, unsafe content, counterfeit service, collusion, ranking gaming, or enforcement overreach.
4. Define incentive model, control ladder, review/appeal workflow, payout holds, quality metrics, ranking guardrails, cost model, and trust-health dashboard.
5. Produce marketplace trust-economics plan, state machine, decision table, event schema, risk checklist, and experiment guardrails.

## Guardrails

- Do not optimize GMV, take rate, or supply growth while ignoring fraud, refunds, disputes, support cost, or buyer trust.
- Do not create ranking, rewards, or payout incentives that make low-quality or abusive behavior profitable.
- Do not enforce safety rules without appeals, false-positive review, and creator/seller communication.
- Do not hide moderation or dispute costs from marketplace unit economics.

## Output format

```text
Marketplace context:
Audience / source of truth / risk boundary:

Trust-safety economics plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Incentives, controls, payouts, disputes, and metrics:
- <trigger> -> <policy, metric, edge case, support note>
```
