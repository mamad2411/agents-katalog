---
name: database-migration-safety
description: "Plans schema changes that run without downtime: expand and contract steps, safe backfills, lock checks and a tested rollback for each migration."
---

# Database migration safety

Assume the old and the new application code run at the same time during the deploy.

## Steps

1. Read the migration and find the table size and traffic. Name the lock each statement takes (`ACCESS EXCLUSIVE` blocks all reads and writes).
2. Split risky changes using expand and contract:
   - Expand: add the new column as nullable with no default, or add the new table. Deploy code that writes both old and new.
   - Backfill in batches.
   - Switch reads to the new column, deploy, observe.
   - Contract: drop the old column in a later release, never the same one.
3. Safe forms (PostgreSQL): `CREATE INDEX CONCURRENTLY` outside a transaction; add a constraint as `NOT VALID` then `VALIDATE CONSTRAINT`; add a foreign key the same way; set `NOT NULL` only after a validated check constraint exists. Set `lock_timeout` (for example 3s) and retry, so a waiting migration cannot block traffic.
4. Backfills: update by primary key ranges of 1,000 to 10,000 rows, commit each batch, sleep briefly between batches, make it resumable and idempotent. Never one giant UPDATE.
5. Renames and type changes are breaking: add a new column and copy, do not rename in place.
6. Write the down migration or a documented reverse plan, and say what data cannot be recovered (dropped columns).
7. Run it on a restored copy of production-size data, record the duration and locks, then run the down path.

## Rules

- Never run a migration against production yourself.

## Report

Verdict (safe, safe with changes, unsafe), each risky statement with its lock and fix, the staged plan, the rollback.
