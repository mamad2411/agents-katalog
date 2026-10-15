---
name: cost-margin-unit-economics-review
description: Design and audit product cost structure, gross margin, COGS, cloud/AI inference cost, payment fees, app-store commissions, marketplace payouts, refunds, support cost, usage-based margin, CAC/LTV, payback, cohort profitability, free-tier economics, and pricing sustainability. Use when deciding whether SaaS, app, game, API, AI, marketplace, or subscription monetization can profitably scale.
---

# Cost Margin Unit Economics Review

Use this skill to convert a unit economics, gross margin, pricing sustainability, usage cost, CAC/LTV, refunds, support cost, and profitability question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify product model, price unit, value metric, cost drivers, acquisition channel, retention curve, refund/support load, and scale assumptions.
2. Read `references/cost-margin-unit-economics-patterns.md`.
3. Classify economics model: subscription, usage-based, marketplace, IAP/IAA game, API, AI feature, desktop app, services-assisted, or freemium.
4. Define revenue, variable cost, fixed allocation, gross margin, contribution margin, CAC payback, expansion, sensitivity, and guardrail metrics.
5. Produce unit economics model, state machine, decision table, event schema, pricing-risk checklist, and experiments to validate assumptions.

## Guardrails

- Do not call a plan profitable without variable costs, fees, refunds, support, abuse, and platform commissions.
- Do not average away heavy users, enterprise discounts, free-tier abuse, regional pricing, or AI inference outliers.
- Do not use LTV/CAC without retention cohort assumptions and payback window.
- Do not fix margin only by hostile limits, surprise overages, or degraded product quality.

## Output format

```text
Economics context:
Price unit / cost drivers / scale assumptions:

Unit economics model:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Cost and margin drivers:
- <item> -> <policy, metric, edge case, support note>

Guardrails and experiments:
- <trigger> -> <action, communication, owner>
```
