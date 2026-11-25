---
name: database-migration-planner
description: "Plans and executes safe schema changes on live databases using expand-contract. Use when altering tables, dropping columns, renaming, adding indexes, or any DDL on production."
---

# Database Migration Planner

## Overview

Schema changes on live databases kill services when done wrong: long locks starve connections, dropped columns crash old code still reading them, and un-rollbackable migrations turn a 5-minute deploy into an all-night incident. This skill enforces the expand-contract (parallel-change) pattern so every migration is additive first, fully reversible, and tested on prod-like data before it touches production.

**Core principle:** Every destructive or locking schema change MUST be split across at least two deploys — one that expands (adds) and a later one that contracts (removes) — with a tested rollback step at every stage.

## The Iron Law

```
NEVER DROP, RENAME, OR LOCK IN THE SAME DEPLOY THAT FIRST USES THE NEW SHAPE.
EXPAND FIRST. MIGRATE DATA. VERIFY. THEN CONTRACT — IN SEPARATE DEPLOYS.
```

If you have not completed Phase 1 (audit + rollback plan) before touching a schema, you are not doing migrations — you are gambling with production data.

## When to Use

**Use this when:**
- Adding, removing, or renaming a column or table on a live database
- Adding an index to a table that has live traffic
- Changing a column type, constraint, or default
- Splitting or merging tables (normalization / denormalization)
- Any DDL that could acquire a table-level lock for more than ~200 ms

**Use this ESPECIALLY when:**
- Someone says "it's a quick column rename" (renames break every ORM query and every old deploy in flight)
- The table has > 1 M rows (DDL lock duration scales with row count)
- You are mid-sprint and there is pressure to "just run the migration"
- The database is PostgreSQL and someone writes `ALTER TABLE … ADD COLUMN … NOT NULL DEFAULT …` — this rewrites the whole table in Postgres < 11
- A rollback plan is described as "we'll just revert the migration file" (migration files rarely reverse data backfills safely)

**Never skip when:**
- The change "only affects dev" but the migration file will be promoted to production
- Zero-downtime is not a stated requirement (latent locks still cause incidents under load)
- A NoSQL store is involved — schema-less does not mean migration-less; documents have implied shapes

## Phase 1: Audit & Rollback Design

**BEFORE writing any SQL:**

1. **Characterise the table** — row count, write QPS, longest-running queries touching it, foreign key dependents.

   ```sql
   -- PostgreSQL: row estimate and live activity
   SELECT relname, n_live_tup, n_dead_tup
   FROM pg_stat_user_tables
   WHERE relname = 'orders';

   SELECT pid, state, query_start, query
   FROM pg_stat_activity
   WHERE query ILIKE '%orders%' AND state != 'idle'
   ORDER BY query_start;
   ```

2. **Identify the lock tier** — classify every DDL statement against the locking danger table:

   | Operation | Lock acquired | Safe on live traffic? |
   |-----------|---------------|-----------------------|
   | `ADD COLUMN … DEFAULT NULL` (PG 11+) | ShareUpdateExclusiveLock | Yes |
   | `ADD COLUMN … NOT NULL DEFAULT …` (PG < 11) | AccessExclusiveLock | NO — rewrites table |
   | `DROP COLUMN` | AccessExclusiveLock | NO — breaks running code |
   | `RENAME COLUMN / TABLE` | AccessExclusiveLock | NO — breaks ORM/queries |
   | `ADD CONSTRAINT NOT NULL` (PG 12+ `NOT VALID`) | ShareUpdateExclusiveLock | Yes (validate separately) |
   | `CREATE INDEX` | ShareLock (blocks writes) | NO — use `CONCURRENTLY` |
   | `CREATE INDEX CONCURRENTLY` | No table lock | Yes (slower, cannot run in txn) |
   | `ALTER COLUMN TYPE` (compatible cast) | AccessExclusiveLock | NO — rewrite |
   | `TRUNCATE` | AccessExclusiveLock | NO |

3. **Write the rollback step first.** If you cannot write a safe rollback, you cannot write the migration.

   ```sql
   -- Example rollback for adding a column
   -- Forward:  ALTER TABLE orders ADD COLUMN fulfilled_at timestamptz;
   -- Rollback: ALTER TABLE orders DROP COLUMN fulfilled_at;
   -- ✓ Safe — column is nullable, old code ignores unknown columns
   ```

4. **Test on a prod-like snapshot.** Restore the latest anonymised dump to a staging database, run `EXPLAIN (ANALYZE, BUFFERS)` on the DDL, measure lock wait duration.

**Output:** written audit doc with row count, lock tier, rollback SQL, and staging test results.

## Phase 2: Expand (Additive Deploy)

Add the new shape without removing anything the existing code depends on. The application continues to run unchanged.

```sql
-- Scenario: rename column  user_name → display_name
-- Step 1 — add the new column (nullable, no default lock)
ALTER TABLE users ADD COLUMN display_name text;

-- Step 2 — copy existing data in batches (never a single UPDATE)
DO $$
DECLARE
  batch_size INT := 5000;
  offset_val INT := 0;
  rows_updated INT;
BEGIN
  LOOP
    UPDATE users
    SET display_name = user_name
    WHERE id IN (
      SELECT id FROM users
      WHERE display_name IS NULL
      LIMIT batch_size
    );
    GET DIAGNOSTICS rows_updated = ROW_COUNT;
    EXIT WHEN rows_updated = 0;
    PERFORM pg_sleep(0.1);   -- yield to live traffic between batches
  END LOOP;
END;
$$;

-- Step 3 — add NOT NULL + default AFTER backfill, using NOT VALID to skip full scan
ALTER TABLE users
  ADD CONSTRAINT users_display_name_not_null
  CHECK (display_name IS NOT NULL) NOT VALID;
```

Rules for this phase:
- No DROP, no RENAME, no type changes that break existing queries
- All new columns nullable or with a safe server-side default
- Indexes created with `CREATE INDEX CONCURRENTLY` — outside any transaction block
- New constraints added `NOT VALID`, validated separately

## Phase 3: Dual-Write / Dual-Read (Application Layer)

Deploy the application code that writes to BOTH the old and new columns and reads from the new one (with fallback to old). This is the bridge phase.

```python
# Example: reading display_name with fallback to user_name
def get_display_name(user: User) -> str:
    return user.display_name or user.user_name  # fallback during transition

# Example: writing both columns
def update_display_name(user_id: int, name: str, db: Session) -> None:
    db.execute(
        "UPDATE users SET display_name = :name, user_name = :name WHERE id = :id",
        {"name": name, "id": user_id},
    )
```

Validate constraints created with `NOT VALID` during this phase (off-peak):

```sql
-- Validates without full AccessExclusiveLock
ALTER TABLE users VALIDATE CONSTRAINT users_display_name_not_null;
```

## Phase 4: Verify Before Contract

Before removing the old column, confirm zero consumers remain:

1. **Search application code** for any direct reference to the old column name.
2. **Check views, functions, and triggers** in the database.

   ```sql
   -- PostgreSQL: find all objects referencing a column by name
   SELECT dependent_ns.nspname, dependent.relname, pg_get_definition(dependent.oid)
   FROM pg_depend dep
   JOIN pg_class dependent ON dependent.oid = dep.objid
   JOIN pg_namespace dependent_ns ON dependent_ns.oid = dependent.relnamespace
   WHERE dep.classid = 'pg_class'::regclass
     AND dep.deptype = 'n';

   -- Simpler: search pg_views and pg_proc source
   SELECT viewname, definition FROM pg_views WHERE definition ILIKE '%user_name%';
   SELECT proname, prosrc FROM pg_proc WHERE prosrc ILIKE '%user_name%';
   ```

3. **Verify old column write traffic is zero** — add a temporary metric or check slow-query logs for the old column name over 48 hours.
4. **Confirm all application replicas are on the new code** (no old deploy pods still running).

## Phase 5: Contract (Remove Old Shape)

Only now — in a separate deploy, days or weeks after expand — is it safe to drop the old column.

```sql
-- Remove the bridge fallback from application code first, then:
ALTER TABLE users DROP COLUMN user_name;

-- Drop the temporary constraint (if you promoted display_name to a real NOT NULL column):
ALTER TABLE users ALTER COLUMN display_name SET NOT NULL;
ALTER TABLE users DROP CONSTRAINT users_display_name_not_null;
```

For index removal:

```sql
-- DROP INDEX CONCURRENTLY avoids locking reads
DROP INDEX CONCURRENTLY idx_users_user_name;
```

## Phase 6: Post-Migration Verification

Run immediately after contract deploy:

```sql
-- Confirm column is gone
SELECT column_name FROM information_schema.columns
WHERE table_name = 'users' AND column_name = 'user_name';
-- Expected: 0 rows

-- Confirm index status
SELECT indexname, indisvalid, indisready
FROM pg_indexes
JOIN pg_class ON pg_class.relname = pg_indexes.indexname
JOIN pg_index ON pg_index.indexrelid = pg_class.oid
WHERE tablename = 'users';

-- Check for table bloat introduced by the migration
SELECT relname, n_dead_tup FROM pg_stat_user_tables WHERE relname = 'users';
-- If n_dead_tup is high: schedule VACUUM ANALYZE users;
```

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "It's just adding a column, no need for expand-contract"
- "The table is small, the lock will be milliseconds"
- "We'll handle rollback if we need it"
- "I'll run the backfill in a single UPDATE — it's only 2 million rows"
- "The ORM handles migrations automatically, it should be fine"
- "We can rename the column and do a find-replace in the code at the same time"
- "It's a one-person app, no concurrent traffic"
- No staging test performed before touching production

**ALL of these mean: STOP. Return to Phase 1.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "ADD COLUMN is instant in Postgres" | Only if nullable with no default in PG 11+. A NOT NULL default rewrites the table in older versions. Always check your engine version. |
| "Our database is small, locks won't matter" | A 200 ms lock at 500 req/s queues 100 connections. Connection pools exhaust in seconds. |
| "We'll test migration on staging" | Staging with 10k rows tells you nothing about a 50M-row prod table. Use anonymised prod snapshots. |
| "Rollback just means reverting the migration file" | The migration file does not undo a 2 M-row data backfill or re-create deleted data. |
| "The ORM migration tool handles this safely" | ORMs generate `ALTER TABLE … NOT NULL DEFAULT …` without lock awareness. Always inspect generated SQL. |
| "We have a maintenance window, locking is fine" | Maintenance windows are a crutch. Zero-downtime migrations are possible — learn them once, use forever. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Why is the site down?" — A lock was held too long; you skipped Phase 1 lock audit.
- "Old code is still crashing after the deploy" — You contracted before all replicas drained; you skipped Phase 4 consumer check.
- "The backfill is still running 6 hours later" — You ran a single-statement UPDATE; restart Phase 2 with batched updates.
- "We can't roll back, the column is already gone" — You contracted without a tested rollback; return to Phase 1.
- "Staging tests passed but prod locked" — Staging data volume was not prod-like; fix the staging snapshot process.

**When you see these:** STOP. Diagnose lock waits with `pg_stat_activity`, assess data loss risk, then return to the relevant phase.

## Related Skills

- **backend-senior-engineer** — use for application-layer dual-write/dual-read code during Phase 3
- **spec-first-development** — use BEFORE this skill if the schema change is driven by a new feature spec
- **backup-dr-planner** — verify a verified backup exists and restore is tested before any Phase 5 contract step
- **performance-engineer** — use after migration to validate query plans have not regressed on the new schema
- **edge-case-hunter** — use to stress-test the backfill and constraint validation under concurrent load scenarios

## Verification

Before marking any migration complete:

- [ ] Row count, write QPS, and foreign-key dependents documented for every affected table
- [ ] Every DDL statement classified against the locking danger table (Phase 1)
- [ ] Rollback SQL written and tested on staging before any production change
- [ ] Prod-like data volume used for staging test (not a trimmed dev fixture)
- [ ] All new indexes created with `CREATE INDEX CONCURRENTLY` outside a transaction
- [ ] NOT NULL constraints added as `NOT VALID` and validated separately in Phase 3
- [ ] Data backfill runs in batches with a sleep/yield between iterations
- [ ] Dual-write confirmed active and metrics show zero writes to old column before contract
- [ ] `pg_views` and `pg_proc` searched for references to dropped/renamed columns
- [ ] Contract deploy is a separate PR/deploy from the expand deploy
- [ ] Post-migration query plans verified — no sequential scans introduced unexpectedly
- [ ] `VACUUM ANALYZE` scheduled if `n_dead_tup` is elevated after backfill
- [ ] Incident runbook updated with this migration's rollback procedure
