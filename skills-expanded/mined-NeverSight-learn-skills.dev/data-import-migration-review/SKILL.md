---
name: data-import-migration-review
description: Design and audit data imports, customer migrations, bulk uploads, CSV/schema mapping, backfills, migration wizards, dry runs, validation, idempotency, reconciliation, rollback, progress visibility, and support handoffs. Use when moving product data between systems, onboarding customers from competitors, importing files, or migrating accounts without data loss.
---

# Data Import Migration Review

Use this skill to convert a data import, migration, mapping, backfill, dry run, rollback, reconciliation, and customer trust question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify source system, target model, data classes, owner, scale, time window, loss tolerance, and customer-facing promise.
2. Read `references/data-import-migration-patterns.md`.
3. Classify the job as self-serve import, assisted migration, admin bulk upload, background backfill, restore, or continuous sync cutover.
4. Define schema mapping, validation, dedupe, idempotency, retry, progress, rollback, audit, and acceptance checks.
5. Produce migration plan, state machine, decision table, event schema, support script, and reconciliation checklist.

## Guardrails

- Do not mutate customer data at scale without dry-run results, backup/restore path, idempotency key, and rollback owner.
- Do not trust file headers, row counts, timestamps, identifiers, currencies, or encodings without validation.
- Do not hide partial success; expose skipped, failed, duplicated, transformed, and pending records clearly.
- Do not log raw sensitive fields, uploaded files, secrets, or private customer data in migration diagnostics.

## Output format

```text
Import context:
Source / target / scale / loss tolerance:

Migration plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Mapping and validation:
- <item> -> <policy, metric, edge case, support note>

Rollback and reconciliation:
- <trigger> -> <action, communication, owner>
```
