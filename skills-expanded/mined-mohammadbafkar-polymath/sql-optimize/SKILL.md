---
name: sql-optimize
description: Read EXPLAIN ANALYZE output and propose targeted optimizations — index, predicate, join order, or query shape changes.
---

# sql-optimize

> A SQL query is slow. Read the plan, identify the dominant cost, propose one concrete change.

## When to use

- A query is slow in production or in development.
- A scheduled report has crept up over time and you want to know why.

## Inputs

- The query.
- The plan: `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)` on Postgres (or the dialect equivalent). Run with a warmed cache when comparing.
- Schema and indexes for the involved tables.

## Reading the plan, by dialect

The plan format differs, but the questions are the same: which node
dominates, what does it scan, why was that picked, what could change
it. Cheat sheet:

| Dialect | Command | Key fields to read |
| --- | --- | --- |
| Postgres | `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) <query>` | `cost`, `actual time`, `rows`, `loops`, `Buffers: shared hit / read`, `Sort Method: external merge` |
| MySQL ≥ 8 | `EXPLAIN ANALYZE <query>` or `EXPLAIN FORMAT=JSON <query>` | `actual_time_first`, `actual_time_last`, `rows_examined_per_scan`, `using_temporary_table`, `using_filesort` |
| SQLite | `EXPLAIN QUERY PLAN <query>` | `SCAN` vs `SEARCH`, `USING INDEX` / `USING COVERING INDEX` |
| BigQuery | `EXECUTION DETAILS` tab or `INFORMATION_SCHEMA.JOBS_BY_*.query_info` | `slot_ms`, `shuffle output bytes`, `repartitioned input rows`, stage `compute ratio max/avg` (skew) |
| Snowflake | `EXPLAIN <query>` and the Query Profile UI | `bytes scanned`, `partitions scanned/total`, `spilling to local/remote storage`, `cardinality estimate vs actual` |
| Redshift | `EXPLAIN <query>` + `SVL_QUERY_REPORT` | step type, `rows_pre_filter` vs `rows`, `is_diskbased`, distribution / sort key alignment |
| DuckDB | `EXPLAIN ANALYZE <query>` | `actual time`, `cardinality`, `function` (operator) names |

Read Postgres bottom-up; read MySQL / BigQuery / Snowflake top-down
(the root node is the final operator and children are inputs). The
*dominant cost* rule is dialect-independent: pick the single node
accounting for > 50 % of runtime; if no node dominates, pick the
deepest one.

## Procedure

1. **Read the plan bottom-up**. The expensive nodes are usually the leaves (sequential scans, large hash builds).
2. **Look for**:
   - **Seq Scan on a large table** with a selective predicate → missing or unused index.
   - **Index Scan** on the wrong index (high "buffers read" relative to rows returned) → composite index column order is wrong.
   - **Nested Loop** with high outer rows → join order / hash join would be cheaper.
   - **Sort** spilling to disk (high "external merge" or "Sort Method: external") → memory or pre-sorted index.
   - **Hash Aggregate** with very high `Rows Removed by Filter` → predicate could move earlier.
   - **Function call in WHERE** (`WHERE lower(email) = ...`) blocking index use → use a functional index or normalize on write.
   - **CTE materialization** on Postgres < 12 (CTEs are an optimization fence in old versions) → inline or use a subquery.
3. **Compute the dominant cost**. Pick the single node accounting for > 50% of total runtime; if no single node dominates, pick the deepest one.
4. **Propose ONE change**. State the expected effect with a rationale, then verify with a fresh `EXPLAIN ANALYZE` of the patched query.

## Output

```text
Slow query: top countries by active users.

Plan summary:
  - Total: 4,200 ms.
  - Dominant: Seq Scan on events (3,800 ms, 12M rows, returns 480k).
  - Predicate: created_at >= now() - interval '7 days' AND country_code IS NOT NULL.

Diagnosis:
  events.created_at is indexed but the planner picked Seq Scan because
  the optimizer's row estimate for the predicate is off by 10x.

First fix:
  ANALYZE events;
  Re-run EXPLAIN. If the planner still picks Seq Scan, force-test with
    SET enable_seqscan = off;
  to confirm the index would be cheaper.

Likely permanent fix:
  Composite index events(created_at, country_code).
  Drop the standalone events(country_code) index if unused.
```

## Anti-patterns to avoid

- "Add an index" without checking pg_stat_user_indexes (or the
  dialect equivalent like MySQL `sys.schema_unused_indexes`,
  BigQuery's "this query did not use the partition / cluster column"
  warning) for unused ones first.
- Rewriting the query before reading the plan.
- Comparing runtimes on a cold vs warm cache.
- Changing multiple things at once and not knowing which helped.
- On BigQuery / Snowflake / Redshift: optimizing a query whose actual
  cost is data movement (shuffle / spill / cross-region scan) by
  rewriting the SQL. Fix the storage layout (partition / cluster /
  sort key) first.

## Related skills

- [`polymath-backend:migration-plan`](../../../polymath-backend/skills/migration-plan/SKILL.md)
  — when the proposed fix is a schema change (new index, new
  composite key, change of partition / sort column), plan it as an
  online migration first.
- [`polymath-backend:review-migration`](../../../polymath-backend/skills/review-migration/SKILL.md)
  — Postgres-specific lock review before shipping the index change.
- [`polymath-data:sql-write`](../sql-write/SKILL.md)
  — when the right fix is rewriting the query rather than the schema.
