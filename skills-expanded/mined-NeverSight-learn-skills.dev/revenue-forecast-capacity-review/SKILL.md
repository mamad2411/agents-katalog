---
name: revenue-forecast-capacity-review
description: Design and audit revenue forecasts, capacity planning, funnel assumptions, pipeline, conversion, expansion, churn, retention cohorts, gross margin, infrastructure capacity, support capacity, sales capacity, inventory/supply, scenario planning, leading indicators, and forecast governance. Use when growth plans, pricing, launches, or operations need financially credible capacity-aware planning.
---

# Revenue Forecast Capacity Review

Use this skill to convert a revenue forecasts, capacity planning, funnel assumptions, retention, gross margin, support/infra constraints, and scenarios question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify revenue model, forecast horizon, segments, funnel stages, capacity constraints, cost drivers, owner, and decisions the forecast will change.
2. Read `references/revenue-forecast-capacity-patterns.md`.
3. Classify forecast: bookings, revenue, usage, marketplace GMV, ad revenue, game monetization, support demand, infra load, or supply capacity.
4. Define assumptions, source data, leading indicators, cohort retention, conversion, churn, expansion, margin, capacity limits, scenarios, and review cadence.
5. Produce forecast model review, state machine, decision table, event schema, scenario checklist, and governance loop.

## Guardrails

- Do not present a single optimistic forecast without base/downside scenarios and capacity constraints.
- Do not forecast revenue without churn, expansion, refunds, discounts, payment/platform fees, and gross margin.
- Do not ignore support, infrastructure, inventory, creator supply, or sales capacity when launch demand grows.
- Do not let stale pipeline or vanity signups drive hiring, infra spend, or investor narrative.

## Output format

```text
Forecast context:
Model / horizon / segment / capacity constraint:

Forecast and capacity plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Assumptions and indicators:
- <item> -> <policy, metric, edge case, support note>

Scenario and governance loop:
- <trigger> -> <action, communication, owner>
```
