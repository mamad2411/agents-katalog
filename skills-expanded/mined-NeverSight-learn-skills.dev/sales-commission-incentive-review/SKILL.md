---
name: sales-commission-incentive-review
description: Design and audit sales commission and incentive plans covering quota, attainment, accelerators, clawbacks, renewals, expansion credit, multi-year deals, discounting, channel conflict, services, usage commitments, churn risk, sales behavior, margin, customer quality, and RevOps/finance controls. Use when compensation could shape pipeline quality, pricing discipline, or customer trust.
---

# Sales Commission Incentive Review

Use this skill to convert sales commission, incentive, quota, accelerator, clawback, discount, expansion-credit, and behavior-risk questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify sales roles, quota model, bookings/revenue metric, deal types, payout timing, discount policy, renewal/expansion ownership, channel rules, and behavior risks.
2. Read `references/sales-commission-incentive-patterns.md`.
3. Classify incentive as new logo, expansion, renewal, usage commit, multi-year, services, channel, team quota, SPIFF, accelerator, or clawback.
4. Define payout basis, eligibility, quality gates, margin guardrails, crediting rules, exception approval, dispute path, and reporting controls.
5. Produce incentive review, state machine, decision table, event schema, compensation checklist, and risk controls.

## Guardrails

- Do not reward behavior that creates bad-fit customers, discount abuse, inflated commitments, unsupported terms, churn, or channel conflict.
- Do not base payout on data that CRM, billing, finance, and contracts cannot reconcile.
- Do not launch incentives without dispute rules, clawback policy, exception owner, and scenario testing.
- Do not let short-term accelerators undermine customer quality, margin, or retention.

## Output format

```text
Incentive context:
Audience / source of truth / risk boundary:

Commission plan review:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Crediting, guardrails, disputes, and controls:
- <trigger> -> <policy, metric, edge case, support note>
```
