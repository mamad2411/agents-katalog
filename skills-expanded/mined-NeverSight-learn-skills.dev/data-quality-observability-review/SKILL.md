---
name: data-quality-observability-review
description: Design and audit data quality observability for analytics events, product metrics, warehouses, imports, pipelines, dashboards, AI datasets, billing data, and operational reports. Use when teams need freshness, completeness, accuracy, schema drift detection, lineage, backfill safety, alerting, incident ownership, and metric trust.
---

# Data Quality Observability Review

Use this skill to convert a data quality, freshness, completeness, schema drift, lineage, alerting, and metric trust question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify critical datasets, decisions they drive, owners, data producers, consumers, SLAs, freshness needs, and blast radius of wrong data.
2. Read `references/data-quality-observability-patterns.md`.
3. Classify quality checks: schema, freshness, volume, uniqueness, referential integrity, distribution, reconciliation, privacy, and semantic metric checks.
4. Define monitors, alert thresholds, owner routing, backfill policy, dashboard trust states, incident comms, and data contract changes.
5. Produce quality map, state machine, decision table, event schema, alert policy, and backfill checklist.

## Guardrails

- Do not treat a dashboard as trusted if upstream freshness, schema, and reconciliation are unowned.
- Do not alert every anomaly without severity, owner, and user-facing decision impact.
- Do not backfill customer, billing, or AI training data without idempotency and before/after reconciliation.
- Do not expose private data in quality logs, sample rows, or incident screenshots.

## Output format

```text
Data context:
Dataset / decision / SLA / blast radius:

Quality observability plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Checks and owners:
- <item> -> <policy, metric, edge case, support note>

Backfill and incident response:
- <trigger> -> <action, communication, owner>
```
