---
name: data-warehouse-metrics-layer-review
description: Design and audit data warehouse metrics layers, semantic models, KPI definitions, source lineage, grain, dimensions, ownership, freshness, quality tests, backfills, access, dashboards, finance/product reconciliation, and metric change control. Use when teams need trusted metrics instead of duplicated BI formulas.
---

# Data Warehouse Metrics Layer Review

Use this skill to convert warehouse metrics layer, semantic model, KPI definition, lineage, freshness, and dashboard trust questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify decision questions, source systems, metric consumers, current dashboard conflicts, event tables, warehouse models, BI tools, owners, freshness needs, and compliance constraints.
2. Read `references/data-warehouse-metrics-layer-patterns.md`.
3. Classify metric as financial, product usage, growth funnel, support, reliability, marketplace, experiment, AI cost, or operational health.
4. Define canonical metric contract, grain, dimensions, filters, owner, lineage, freshness SLA, quality tests, access rules, dashboard publishing, and change log.
5. Produce metrics-layer design, state machine, decision table, event schema, quality checklist, and migration/deprecation plan.

## Guardrails

- Do not let every dashboard redefine core metrics such as active user, conversion, churn, ARR, support SLA, or usage cost.
- Do not publish metrics without grain, timezone, identity resolution, exclusions, source lineage, and owner.
- Do not backfill or redefine a KPI without change log, consumer notification, and historical impact estimate.
- Do not expose sensitive row-level data through convenience metrics or broad BI access.

## Output format

```text
Metrics-layer context:
Audience / source of truth / risk boundary:

Metric contract plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Lineage, freshness, and change control:
- <trigger> -> <policy, metric, edge case, support note>
```
