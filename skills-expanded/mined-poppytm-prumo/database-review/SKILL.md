# Database & Schema Review

## Purpose
Review and harden relational schemas, migrations, indexes, constraints, transactions, and query plans using EXPLAIN ANALYZE evidence, pg_stat_statements data, and reversible migration discipline with zero-downtime guarantees.

## Use when
- Reviewing migrations, schema changes, index additions, or constraint alterations before merge.
- Diagnosing slow queries, sequential scans, N+1 access, lock contention, or connection exhaustion.
- Defining transaction boundaries, isolation levels, foreign keys, uniqueness, and check constraints.
- Auditing backup, restore, retention, and data-migration safety for production databases.

## Do not use when
- Implementing HTTP endpoints or API contracts without schema changes (use `backend-api`).
- Tuning in-process or distributed caches without touching the database (use `caching`).
- Verifying API serialization schemas without persistence changes (use `api-contract-testing`).

## Required context
- Schema dump or migration files under review with target tables, row counts, and growth rates.
- EXPLAIN ANALYZE plans for affected queries plus pg_stat_statements top-20 by total time.
- Transaction inventory: boundaries, isolation levels, retry behavior, and lock timeouts.
- Operational constraints: maintenance windows, backup RPO/RTO, allowed downtime in seconds.

## Procedure
1. **Inspect the migration for reversibility**: confirm every migration has a tested down path (or documented forward-only fix), uses explicit transaction blocks, avoids locking rewrites like bare ADD COLUMN with defaults on tables over 1 M rows, and expands in small batches of 1,000–5,000 rows.
2. **Analyze query plans with EXPLAIN ANALYZE**: run EXPLAIN ANALYZE BUFFERS on affected queries against a production-sized snapshot, require index-only or index scans on hot paths, flag sequential scans over 100 k rows, and verify join order and row estimates within one order of magnitude.
3. **Right-size indexes and constraints**: add B-tree indexes for equality/range predicates, composite indexes ordered by selectivity, partial indexes for hot subsets, and trigram (pg_trgm) indexes for LIKE searches; enforce foreign keys, NOT NULL, uniqueness, and check constraints at the database layer, never only in application code.
4. **Harden transactions and concurrency**: keep transactions under 500 ms, set lock_timeout to 3 s and statement_timeout to 10 s on OLTP workloads, use READ COMMITTED by default with explicit row locking (SELECT FOR UPDATE) for account-balance style mutations, and retry serialization failures with capped exponential backoff.
5. **Verify safety gates**: run migrations on a staging clone with production volume, measure lock wait events in pg_locks, confirm rollback completes in under 60 s, and capture pg_stat_statements deltas proving no regression beyond 10 percent on p95 query time.
6. **Record evidence and run scripts/verify.sh** from the repo root with plans, migration logs, and rollback timings attached.

## Decision rules
- **Every migration is reversible**: untested or irreversible DDL never merges to main.
- **No sequential scans on hot paths**: queries above 100 queries per minute must use index access verified by EXPLAIN ANALYZE.
- **Constraints live in the database**: foreign keys, uniqueness, and checks are DDL, not application hopes.
- **Small transactions only**: transactions exceeding 500 ms or holding locks across network calls are rejected in review.
- **Production-sized proof required**: plan evidence from empty dev databases is inadmissible; use snapshots with real volume.

## Evidence required
- EXPLAIN ANALYZE BUFFERS plans before and after for every affected query.
- pg_stat_statements deltas showing p95 query time within 10 percent of baseline.
- Migration up/down logs on staging clone with rollback timing under 60 s.
- Passing execution log from scripts/verify.sh.

## Output contract
- Review verdict per migration: approve, approve with conditions, or block with concrete remediation.
- Index and constraint DDL with plan evidence and rollback procedure.
- Transaction and timeout configuration changes with monitoring hooks.

## Stop conditions
- All migrations reviewed with reversible paths, indexed hot paths, and staging rollback under 60 s.
- Blocking defect found (data-loss risk, irreversible DDL, unindexed hot query) requiring author rework.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to DBA if lock contention, replication lag above 5 s, or autovacuum backlog threatens the migration window.
- Escalate to Lead Architect if a schema change forces a breaking API contract change or cross-service data ownership dispute.
