---
name: data-residency-region-review
description: Design and audit data residency and regional operating models covering customer region commitments, data classification, storage, processing, backups, logs, analytics, search, AI providers, subprocessors, support/admin access, replication, failover, deletion, migrations, contracts, and proof. Use when customers or regulators require clarity about where data lives and moves.
---

# Data Residency Region Review

Use this skill to convert data residency, regional architecture, replication, subprocessor, support access, and compliance-proof questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify customer commitments, regions, data classes, systems, subprocessors, backups, logs, analytics, AI processing, support access, failover needs, and contractual/regulatory constraints.
2. Read `references/data-residency-region-patterns.md`.
3. Classify data as customer content, metadata, billing, telemetry, support data, logs, backups, derived analytics, AI input/output, or admin audit record.
4. Define residency boundary, allowed transfers, regional services, access controls, replication, backup/restore, deletion, migration, monitoring, and evidence.
5. Produce residency design, state machine, decision table, event schema, control checklist, and customer proof plan.

## Guardrails

- Do not promise residency unless storage, processing, backups, logs, analytics, support access, and subprocessors match the claim.
- Do not ignore metadata, telemetry, derived data, search indexes, AI inputs, or admin audit logs when defining region scope.
- Do not make failover or support access silently move restricted data outside the committed region.
- Do not answer customer residency questions without approved architecture and legal/compliance review.

## Output format

```text
Residency context:
Audience / source of truth / risk boundary:

Regional data plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Transfers, access, and evidence controls:
- <trigger> -> <policy, metric, edge case, support note>
```
