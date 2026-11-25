---
name: postgres-index-tuning
description: Reads EXPLAIN ANALYZE output for a slow Postgres query, then adds or drops indexes only when the measured timing proves a gain.
---

# Postgres index tuning

One change, one measurement. Never add an index you have not justified from a plan.

## Steps

1. Get the exact query with real parameter values. Run `EXPLAIN (ANALYZE, BUFFERS)` on a copy or inside a rolled-back transaction when it writes. Record total time.
2. Read the plan from the innermost node out. Find the node with the largest actual time. Compare estimated rows to actual rows: a gap of 10x or more points to stale statistics, so run `ANALYZE` on the table and re-measure first.
3. Match the problem to a fix:
   - Seq Scan with a selective filter: b-tree on the filtered columns, equality columns first, then range or sort column.
   - Sort on a large set: index that matches `ORDER BY` so the sort disappears.
   - Many rows fetched for few kept: partial index (`WHERE status = 'open'`) or a covering index with `INCLUDE`.
   - `LIKE '%x%'` or fuzzy text: `pg_trgm` GIN index. JSONB containment: GIN.
4. Create it with `CREATE INDEX CONCURRENTLY` so writes are not blocked.
5. Re-run the same `EXPLAIN`, confirm the plan uses it and the time dropped. If not, drop it.
6. Check unused indexes: `pg_stat_user_indexes` where `idx_scan = 0` for weeks. Report them, do not drop without approval.

## Rules

- Never run `CREATE INDEX` without `CONCURRENTLY` on a live table.
- Do not index low-cardinality booleans alone.
- Mention index size from `pg_relation_size`.

## Report

Query, plan before and after with timings, the index definition, its size and the write cost.
