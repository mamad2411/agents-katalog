---
name: data-lineage-impact-review
description: Design and audit data lineage impact reviews covering source systems, transformations, events, warehouse models, metrics, dashboards, ML/AI datasets, exports, privacy, retention, owners, schema changes, backfills, downstream consumers, incident blast radius, and change approvals. Use when a data, event, schema, or pipeline change could break decisions or compliance evidence.
---

# Data Lineage Impact Review

Use this skill to convert data lineage, schema change, downstream impact, metric, dashboard, AI dataset, privacy, and backfill questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify source change, affected tables/events/models, owners, downstream metrics, dashboards, AI/ML datasets, exports, privacy classes, SLAs, and consumers.
2. Read `references/data-lineage-impact-patterns.md`.
3. Classify impact as additive schema, breaking schema, semantic change, backfill, deletion, source migration, transformation change, metric change, privacy classification, or consumer deprecation.
4. Define lineage map, impact radius, owner approvals, tests, communication, migration/backfill plan, rollback, and monitoring.
5. Produce lineage impact review, state machine, decision table, event schema, impact checklist, and change rollout plan.

## Guardrails

- Do not change events, schemas, or model semantics without identifying downstream metrics, dashboards, exports, and AI datasets.
- Do not treat additive columns as risk-free when privacy, cardinality, cost, or semantic meaning changes.
- Do not backfill or delete data without consumer notice, reproducibility, and historical-metric impact analysis.
- Do not rely on tribal knowledge for lineage; produce durable owner and dependency records.

## Output format

```text
Lineage context:
Audience / source of truth / risk boundary:

Data impact plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Consumers, migrations, tests, and rollback:
- <trigger> -> <policy, metric, edge case, support note>
```
