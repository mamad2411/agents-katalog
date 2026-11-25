---
name: migration-rehearsal
description: Run a pending migration against a restored prod-sized copy. Measure duration, the lock profile, the algorithm the engine actually chose, and rollback behaviour. Postgres and MySQL lanes. Do this BEFORE prod.
kind: skill
pack: database
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# migration-rehearsal

A migration that takes 80ms on a dev DB can lock prod for 20 minutes. Rehearse on real data first.

## Premise

Deterministic procedure. Every duration, lock window, and rollback claim must come from a real timed run against a real restored copy. Inputs (dump/snapshot, target DB URL, migration ref) and outputs (timing, lock log, chosen algorithm, schema diff) are cited verbatim. The recommendation block is grounded in the captured numbers, not in folklore about how `ALTER TABLE` "usually" behaves. If the rehearsal DB is empty or undersized, abort and restore a full copy first — synthesized timings are worse than none.

## Halt conditions

- Refuse to report a "duration" without `time` output captured from the actual run.
- Refuse to claim "no locks held" without the lock-observer log for the engine's lane.
- Refuse to certify rollback without a post-rollback schema diff = 0.
- Refuse to report an operation as metadata-only without the engine's own confirmation (the algorithm probe in step 4) — a fast rehearsal is not proof the fast path was taken.
- Halt and ask if the copy is a sample / partial — don't extrapolate from a 10k-row table to a 50M-row prod table.

## When to use

- Before any migration on a populated table where the op is class-2 or class-3 (see `migrations.md`), or where the class is unknown.
- Before any `ALTER COLUMN` type change, `SET NOT NULL` on an existing column, `ADD FOREIGN KEY`, or an index build without the engine's online clause.
- Before a release window, so the duration estimate is in the runbook.
- After a migration was rejected in review for "looks slow" — prove it.

## Prerequisites

- A restored copy of the latest prod backup in an isolated rehearsal DB (PII anonymized for regulated data), **on the same engine and major version as prod**.
- Network isolation — the rehearsal DB cannot reach prod.
- The engine's client + `time` for duration measurement.
- Application code at the post-migration commit (so smoke tests can run).

## Procedure — Postgres lane

1. Restore:
   ```bash
   pg_restore --clean --if-exists --no-owner -d "$REHEARSAL_DB" /backups/prod-latest.dump
   ```
2. Baseline:
   ```bash
   psql "$REHEARSAL_DB" -c "SELECT pg_size_pretty(pg_total_relation_size('orders')), (SELECT count(*) FROM orders);"
   psql "$REHEARSAL_DB" -c "SELECT indexname FROM pg_indexes WHERE tablename='orders';"
   ```
3. Lock observer, second session:
   ```bash
   watch -n 0.5 "psql \"$REHEARSAL_DB\" -c \"SELECT mode, granted, relation::regclass, pid, now()-query_start AS held FROM pg_locks JOIN pg_stat_activity USING(pid) WHERE relation::regclass::text='orders' ORDER BY held DESC;\""
   ```
4. Algorithm probe: read the plan of record from [PG `ALTER TABLE` § Notes](https://www.postgresql.org/docs/17/sql-altertable.html) and confirm against the run — a rewrite shows as a sustained `ACCESS EXCLUSIVE` and a changed `pg_relation_filenode`; capture it before and after:
   ```bash
   psql "$REHEARSAL_DB" -c "SELECT pg_relation_filenode('orders');"   # before and after; a change means the table was rewritten
   ```
5. Apply with timing: `time <migration-tool> <up-command>`.
6. Smoke tests against the migrated DB (read paths, write paths, the feature this migration enables).
7. Rollback with timing: `time <migration-tool> <down-command>`.
8. Confirm schema restored — re-run step 2 and diff.

## Procedure — MySQL / MariaDB lane

1. Restore. **Prefer a physical snapshot** (storage/volume snapshot, `xtrabackup`) over a logical `mysqldump` restore, and record which you used:
   ```bash
   mysql --defaults-file=... "$REHEARSAL_DB" < /backups/prod-latest.sql    # logical — see the caveat below
   ```
   > A logical restore rebuilds every table fresh. That resets `INNODB_TABLES.TOTAL_ROW_VERSIONS` to 0 and removes prod's fragmentation, so the rehearsal will show the `ALGORITHM=INSTANT` fast path **even when prod is at the row-version ceiling and would be refused**. If you rehearse on a logical restore, capture `TOTAL_ROW_VERSIONS` from **prod** separately and report both.
2. Baseline:
   ```sql
   SELECT TABLE_ROWS, DATA_LENGTH, INDEX_LENGTH, DATA_FREE, ROW_FORMAT
     FROM information_schema.TABLES WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='orders';
   SELECT NAME, TOTAL_ROW_VERSIONS FROM information_schema.INNODB_TABLES WHERE NAME='<schema>/orders';
   SHOW INDEX FROM orders;
   SHOW CREATE TABLE orders\G   -- ROW_FORMAT, FULLTEXT keys, ON DELETE CASCADE/SET NULL
   ```
3. Lock observer, second session — metadata locks are the ones that matter here:
   ```bash
   watch -n 0.5 "mysql -N -e \"
     SELECT OBJECT_NAME, LOCK_TYPE, LOCK_STATUS, OWNER_THREAD_ID
       FROM performance_schema.metadata_locks WHERE OBJECT_NAME='orders';
     SELECT * FROM sys.innodb_lock_waits\G
     SELECT trx_id, trx_started, trx_state, trx_query
       FROM information_schema.INNODB_TRX ORDER BY trx_started;\""
   ```
   The `wait/lock/metadata/sql/mdl` instrument is enabled by default. If it was disabled at startup, `metadata_locks` stays empty whether or not a lock is held — confirm the instrument first, and otherwise report the lock profile as `UNVERIFIED (mdl instrument disabled)` rather than as "no locks".
4. Algorithm probe — **state the algorithm in the DDL**. MySQL errors instead of silently downgrading, which converts a guess into a fact:
   ```sql
   SET SESSION lock_wait_timeout = 60;
   ALTER TABLE orders ADD COLUMN status VARCHAR(32) NULL, ALGORITHM=INSTANT;
   -- refused → the exclusion applies (ROW_FORMAT=COMPRESSED, FULLTEXT index, row-version
   --           ceiling ERROR 4092, row-size/column-count limit ERROR 4158); retry INPLACE, then COPY
   ```
   After an INSTANT add or drop, re-read `TOTAL_ROW_VERSIONS` — an increment confirms the instant path was taken. Also run `SHOW ENGINE INNODB STATUS\G` during a long build to see what phase it is in.
5. Apply with timing: `time <migration-tool> <up-command>`.
6. Smoke tests.
7. Rollback with timing: `time <migration-tool> <down-command>`. Note that a `DROP COLUMN` rollback of an instant add burns **another** row version.
8. Confirm schema restored:
   ```bash
   mysqldump --no-data --skip-comments --skip-dump-date "$DB" orders > after.sql && diff before.sql after.sql
   ```

### Dry-run alternative when no restore is possible

`pt-online-schema-change --dry-run --alter "<the ALTER>" D=<db>,t=<table>` creates and drops the shadow table without swapping. It bounds the *approach*, not the duration. Report it as `PARTIAL — dry-run only, no timing`, never as a rehearsal.

## Output

```
Migration: <migration-ref>
Engine:    <engine> <version>       Restore: <physical snapshot | logical dump>
Target:    <table> (<rows> rows, <data+index bytes>), idx_count=<n>
           ROW_FORMAT=<x>, FULLTEXT=<y/n>, cascade FKs=<y/n>, TOTAL_ROW_VERSIONS=<n> (prod: <n>)

Forward:
  Algorithm: <requested> → <accepted | refused: reason>
  Duration:  <measured>
  Locks:     <max mode> on <table> held <measured>
  MDL wait:  <measured wait for the definition lock, or "none — no open transactions">
  Impact:    <which statements blocked, from the observer log>

Rollback:
  Duration:  <measured>
  Locks:     <max mode> held <measured>
  Schema:    restored ✓ (baseline diff = 0) | NOT restored — <diff>

Recommendation:
  <held> against the deploy SLO of <n>s → <ship as-is | split per expand-contract | book a window>
```

Every angle-bracketed field is a captured value. A report with any of them still bracketed is `INCOMPLETE`, not a rehearsal.

## False positives / gotchas

- A small copy ≠ realistic — rehearse against full-size copies; row count matters more than table count.
- A **logical** MySQL restore hides the row-version ceiling and prod fragmentation (see step 1). A **fresh Postgres restore** likewise has no bloat and perfectly ordered heaps — a rewrite there is faster than on prod.
- Rehearsal disks faster or slower than prod skew duration in the obvious direction — record the disk class next to the number.
- MySQL: `ADD FOREIGN KEY` is `ALGORITHM=COPY` unless `foreign_key_checks` is disabled, and `LOCK=NONE` is refused entirely on a table with `ON…CASCADE`/`ON…SET NULL` constraints. Both change the class; check `SHOW CREATE TABLE` before trusting a "safe" verdict.
- MySQL: an in-place build that applies its online log can raise `ERROR 1062 (23000): Duplicate entry` from a *temporary* duplicate that later traffic would have resolved. A rehearsal with no concurrent write load will never reproduce it — say so rather than reporting the risk as absent.
- Postgres: `CREATE INDEX` without `CONCURRENTLY` takes a write lock; a rehearsal on an idle copy shows the duration but not the blocking, which is the part that hurts.
- The rehearsal cannot reproduce the **definition-lock queue**, because there is no long-running production transaction on the copy. That risk is assessed against prod's `INNODB_TRX` / `pg_stat_activity`, not here. Report it as a separate line, never as "no locks observed".
- Never rehearse ON prod, even "read-only" — heavy queries cascade into replication lag.
