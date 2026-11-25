---
name: zero-downtime-schema-change
description: Plans schema changes as expand, migrate and contract steps with batched backfills, so old and new code both work during every deploy.
---

# Zero downtime schema change

Every deploy must work with the schema before and after it. Split the change so that holds.

## Steps

1. Describe the target change and the table size and write rate. Find all code that reads or writes the affected columns, including jobs, reports and other services.
2. Expand: add the new column or table as nullable with no default that forces a rewrite, or add the index with the non-blocking form (`CONCURRENTLY` in Postgres, online DDL in MySQL). Set a short `lock_timeout` so the migration fails fast instead of queuing behind a long transaction.
3. Dual write: deploy code that writes both old and new. Reads still use the old one.
4. Backfill existing rows in batches of 1,000 to 10,000 by primary key range, committing each batch, sleeping between batches and watching replication lag. The job must be restartable and idempotent.
5. Verify: compare old and new for every row (count mismatches, expect zero).
6. Switch reads to the new column behind a flag, then watch errors and latency.
7. Add constraints last: create `NOT VALID` foreign keys or checks, then `VALIDATE` them separately.
8. Contract: stop writing the old one, wait a full release cycle, then drop it in its own migration.

## Rules

- Never rename or change a column type in place on a live table.
- Never mix schema and data changes in one migration.
- Each step ships in its own deploy and has a stated rollback.

## Report

An ordered runbook with the SQL, the code change per step, batch settings and rollback for each.
