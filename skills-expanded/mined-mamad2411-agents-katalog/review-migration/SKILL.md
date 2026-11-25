---
name: review-migration
description: Review a Postgres migration for lock surface, online/offline safety, backfill strategy — flags ACCESS EXCLUSIVE locks and unsafe defaults on large tables.
---

# review-migration

> Review a `.sql` migration the way an on-call reviewer would: which lock does each statement need, how long it holds, and whether it's safe to apply against a live, replicating, big-table prod.

## When to use

- A schema migration is in a PR.
- A long-lived table needs a structural change and someone has drafted SQL.
- A previous migration timed out and you're trying to figure out why.

## Related skills

- [`polymath-backend:migration-plan`](../../../polymath-backend/skills/migration-plan/SKILL.md)
  — vendor-agnostic expand-migrate-contract phasing for online
  migrations. Plan the phases there; review each Postgres-specific
  statement here.
- [`polymath-backend:audit-pg-config`](../audit-pg-config/SKILL.md)
  — review the Postgres server configuration the migration will run
  against.

## Procedure

1. **Parse statements.** For each statement, identify the locks acquired and held:
   - `CREATE INDEX` — `SHARE` lock (writes blocked).
   - `CREATE INDEX CONCURRENTLY` — `SHARE UPDATE EXCLUSIVE` lock (writes ok); cannot run inside a transaction.
   - `ALTER TABLE … ADD COLUMN` (without default) — `ACCESS EXCLUSIVE`, fast (PG 11+ tracks default separately).
   - `ALTER TABLE … ADD COLUMN … DEFAULT <volatile>` — `ACCESS EXCLUSIVE`, rewrites the table (slow + outage on large tables).
   - `ALTER TABLE … ADD COLUMN … DEFAULT <constant>` (PG 11+) — fast; uses fast-default optimization.
   - `ALTER TABLE … SET NOT NULL` — `ACCESS EXCLUSIVE`, full scan unless a `CHECK CONSTRAINT NOT VALID` was added + validated first.
   - `ALTER TABLE … DROP COLUMN` — `ACCESS EXCLUSIVE`, metadata-only (fast).
   - `RENAME` — `ACCESS EXCLUSIVE`, but instant. Watch out for app code still using the old name.
2. **Backfill plan.** If the migration rewrites data:
   - Batch in chunks (`UPDATE … LIMIT 10000`) with explicit commits.
   - Run outside the schema-migration tool (which usually wraps in a single tx).
   - Pace by `pg_sleep` or external orchestration so the WAL backlog stays manageable.
3. **`NOT NULL` rollout (multi-step).** The safe pattern:
   ```sql
   ALTER TABLE refunds ADD COLUMN currency text;            -- step 1
   ALTER TABLE refunds ADD CONSTRAINT refunds_currency_not_null
     CHECK (currency IS NOT NULL) NOT VALID;               -- step 2
   -- backfill: UPDATE refunds SET currency='USD' WHERE currency IS NULL; (batched, separate deploys)
   ALTER TABLE refunds VALIDATE CONSTRAINT refunds_currency_not_null;  -- step 3
   ALTER TABLE refunds ALTER COLUMN currency SET NOT NULL; -- step 4 (fast because constraint is valid)
   ALTER TABLE refunds DROP CONSTRAINT refunds_currency_not_null;
   ```
4. **Index migrations.** Always `CONCURRENTLY` for production. Note: `CONCURRENTLY` can fail and leave an `INVALID` index — the review should check there's a cleanup statement (`DROP INDEX IF EXISTS … ; CREATE INDEX CONCURRENTLY …`).
5. **Foreign keys.** `ADD CONSTRAINT … FOREIGN KEY … NOT VALID` then `VALIDATE CONSTRAINT` later — same pattern as NOT NULL.
6. **Lock timeout.** Recommend `SET lock_timeout = '5s'` at the top of risky migrations so they fail fast under contention instead of holding the queue.
7. **Statement timeout.** Likewise `SET statement_timeout = '30s'` for individual statements; backfills set their own batch-scoped timeouts.

## Output

```text
review-migration

File:    db/migrations/20260523_add_currency.sql
Target:  refunds (≈ 50M rows)

Statements
  1. ALTER TABLE refunds ADD COLUMN currency text;
     Lock: ACCESS EXCLUSIVE (fast, metadata-only).                ✓

  2. ALTER TABLE refunds ALTER COLUMN currency SET DEFAULT 'USD';
     Lock: ACCESS EXCLUSIVE (fast on PG 11+).                     ✓

  3. ALTER TABLE refunds ALTER COLUMN currency SET NOT NULL;
     Lock: ACCESS EXCLUSIVE; full scan on 50M rows.               ✗ unsafe

Issues
  - Statement 3 will block writes for the duration of the scan on a 50M-row table.
    Fix: split into the 4-step NOT VALID → backfill → VALIDATE → SET NOT NULL pattern.

  - No lock_timeout set. Risk: migration holds the queue if contention spikes.
    Fix: prepend `SET lock_timeout = '5s';`.

Recommendation: split into 3 deploys (constraint+backfill+set-not-null). Block PR until restructured.
```

## Quality bar

- Every statement classified by lock + cost.
- Multi-step pattern named when a single statement is unsafe.
- `CONCURRENTLY` flagged where it should be present (and not inside a transaction).
- `lock_timeout` / `statement_timeout` recommendations stated.

## Anti-patterns to avoid

- "Just add NOT NULL, the table isn't that big" without measuring. Big tables are big at 3 AM, not at code-review time.
- `CREATE INDEX` (not CONCURRENTLY) on a live table. Writes blocked for the duration.
- Wrapping CONCURRENTLY in a transaction. Postgres rejects; the migration tool may obscure the error.
- Running backfill in a single statement on a 50M-row table. WAL bloat, replica lag, undo time after rollback.
