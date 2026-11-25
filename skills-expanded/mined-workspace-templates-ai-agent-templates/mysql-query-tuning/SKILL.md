---
name: mysql-query-tuning
description: Finds slow MySQL queries in the slow log, reads EXPLAIN, and fixes them with correctly ordered composite indexes and query rewrites.
---

# MySQL query tuning

Rank first, then fix the top offenders only.

## Steps

1. Enable the slow log (`slow_query_log=1`, `long_query_time=0.2`) or read `performance_schema.events_statements_summary_by_digest`. Sort by total time, not by single worst run.
2. For each top query, run `EXPLAIN FORMAT=TREE` (or `EXPLAIN ANALYZE` on 8.0). Note the access type, rows examined versus rows returned, and any `Using filesort` or `Using temporary`.
3. Design the composite index with this order: equality columns first, then the one range column, then sort columns. A column after a range condition cannot be used for seeking.
4. Prefer covering indexes for hot read paths so InnoDB never touches the clustered row. Remember secondary indexes carry the primary key.
5. Rewrite where the index cannot help:
   - Remove functions on indexed columns (`WHERE DATE(created_at) = ...` becomes a range).
   - Fix implicit casts: compare strings to strings, and match collations.
   - Replace deep `OFFSET` pagination with keyset pagination (`WHERE id < ?` ORDER BY id DESC LIMIT n).
   - Turn `SELECT *` into named columns.
6. Add the index online (`ALGORITHM=INPLACE, LOCK=NONE`) and re-run EXPLAIN plus the real query timing.
7. Drop redundant prefixes: an index on (a) is covered by (a, b).

## Rules

- Change one thing at a time and keep the timings.
- Do not raise buffer sizes as a first move.
- Never alter a large table on production without a tested plan.

## Report

Each query with rows examined before and after, the index added and the timing.
