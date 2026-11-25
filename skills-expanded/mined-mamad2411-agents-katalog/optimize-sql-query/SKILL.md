---
name: optimize-sql-query
description: Diagnoses slow SQL via EXPLAIN plans and recommends fixes — indexes, query rewrites, partition pruning, and join reordering — with measured before/after.
when_to_use: When a SQL query is slow or expensive and the user wants it faster — analyze the execution plan, find the bottleneck (seq scan, bad join order, missing index, spilled sort), and propose index or rewrite fixes with verified improvement.
---

## When to Use

A specific query is slow or costly and the user wants it faster. You have (or can get) the SQL text and a way to run `EXPLAIN` against a representative dataset.

Do NOT use this skill when:
- Authoring a new analytical query from scratch → use the SQL-authoring skill instead (this is perf, not authoring).
- The "slowness" is connection/pool/lock contention, not the plan → that is an ops problem, not a query problem.
- Row counts are tiny (< ~10k) on every table — a seq scan is fine; chasing a plan here is wasted effort.

## Steps

1. **Get the real plan, not the estimate.** Run `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)` (Postgres) or the engine's analyze form. `EXPLAIN` alone gives the optimizer's *guess*; `ANALYZE` runs it and gives actual rows/time. Always compare **estimated rows vs actual rows** per node — a 100x gap means stale statistics (run `ANALYZE <table>`) and every downstream join choice is suspect.

2. **Find the cost driver, top of the plan downward.** Look for, in priority order:
   - **Seq Scan on a large table** under a selective filter → missing index on the filter/join column.
   - **Nested Loop where inner side runs N times** with high N → join-order or missing-index blowup; the planner expected few outer rows but got many (see step 1's row gap).
   - **Sort / Hash that spills to disk** → look for `external merge Disk: NkB` or `Batches: >1`. The sort/hash exceeded `work_mem`. Fix by indexing to avoid the sort, reducing rows before the sort, or (last resort) raising `work_mem` for that session.
   - **Partition scan with no pruning** → all partitions scanned. The predicate isn't on the partition key, or wraps it in a function/cast that defeats pruning.

3. **Index recommendations — be specific about column order.**
   - Composite index column order = **equality columns first, then the range/sort column, then included columns**. `WHERE a = ? AND b > ?` wants `(a, b)`, never `(b, a)`.
   - A query filtering `a` and `c` cannot use `(a, b, c)` efficiently for `c` — `b` is a gap. Either reorder or make a separate index.
   - **Covering index** (`INCLUDE` in Postgres, or trailing columns) turns an Index Scan + heap fetch into an Index-Only Scan — propose it when the query selects only a few columns beyond the predicate.
   - Partial index (`WHERE status = 'active'`) when the query always filters on a low-cardinality flag — smaller, hotter, faster.

4. **Rewrite when an index won't help.**
   - **Make predicates sargable**: `WHERE date_col >= '2024-01-01'` not `WHERE date(date_col) = ...`; `col LIKE 'foo%'` (indexable) not `LIKE '%foo'` (not). Functions/casts on the indexed column kill index use — move the transform to the literal side.
   - **Predicate pushdown**: filter inside the subquery/CTE, not after the join.
   - In Postgres, a CTE may **materialize** and block predicate pushdown — add `MATERIALIZED`/`NOT MATERIALIZED` deliberately, or inline it.
   - Replace a correlated self-join with a **window function** (`ROW_NUMBER`, `LAG`, running `SUM`) — usually one pass instead of N.
   - Drop a redundant `DISTINCT` when a join key already guarantees uniqueness, or when `EXISTS` expresses the intent without deduplicating a large set.
   - Prefer `EXISTS` over `IN (subquery)` when the subquery can short-circuit; prefer a join over `IN` when you need columns from both sides.

5. **Warehouse / columnar engines need different levers.** On columnar warehouses, indexes barely exist; instead:
   - Align the filter with the **partition/cluster key** so the engine prunes files/micro-partitions — check the plan's scanned-partitions/bytes-scanned, not just time.
   - Watch **broadcast vs shuffle joins**: broadcast a small dimension table, shuffle when both sides are large. A shuffle of two huge tables on a skewed key is the classic blowup.
   - Reduce columns scanned (columnar pays per column) — `SELECT *` is expensive here in a way it isn't on row stores.

6. **Measure before/after on representative data and prove equivalence.**
   - Capture baseline timing (median of a few warm runs, not one cold run) and the plan.
   - Apply the fix, re-run `EXPLAIN ANALYZE`, capture the new timing/plan.
   - Confirm the rewrite is **logically equivalent**: same row count and a checksum/ordered-diff of results on a sample, especially after touching `DISTINCT`, join type, or `NULL`-handling. A faster query that returns different rows is a bug, not an optimization.

## Common Errors

- **Tuning to the cold cache.** First run reads from disk; second run is cached and 10x faster regardless of your change. Warm up, then take the median.
- **Stale statistics misread as a bad query.** Huge estimated-vs-actual row gap → run `ANALYZE` first and re-plan *before* adding indexes; the "fix" may just be fresh stats.
- **An index that helps one query slows every write.** Each index is maintained on every `INSERT`/`UPDATE`/`DELETE`. On write-heavy tables, weigh read gain against write cost; don't add a fourth near-duplicate index when reordering an existing one covers both.
- **Function/cast silently disabling the index you just added.** `WHERE lower(email) = ?` won't use an index on `email` — needs an expression index on `lower(email)` or a sargable rewrite.
- **Plan flips with data volume.** A plan that's optimal on today's 10k rows can go quadratic at 10M. Validate on production-scale row counts, or at least reason about how the chosen join (nested loop vs hash) scales.
- **`OR` across columns defeating indexes.** `WHERE a = ? OR b = ?` often can't use a single composite index — a `UNION ALL` of two indexed lookups is frequently faster.
- **Raising `work_mem`/session knobs as the "fix."** That hides the spill instead of removing it; it's a per-connection footgun under concurrency. Prefer reducing rows or indexing the sort away; bump memory only as a last, documented resort.

## Verify

The optimization is done only when ALL hold:
- New plan no longer shows the original cost driver (seq scan gone / nested loop replaced by hash / sort no longer spilling / partitions pruned).
- Measured median runtime (or bytes-scanned on warehouses) improved on representative data — show the before/after numbers, not "should be faster."
- Result set is provably identical: same row count + matching checksum/ordered sample vs the original query.
- Write/maintenance cost of any new index was considered and noted for write-heavy tables.
- Estimated rows now track actual rows within ~1 order of magnitude (no stale-stats landmine left behind).
