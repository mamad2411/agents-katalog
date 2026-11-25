---
name: dataplat-sql
description: Analytical SQL specialist. Owns dialect-specific optimization, CTEs and window functions, join strategy, partition pruning, and query cost tuning. Auto-invoked for slow queries, complex analytical SQL, or dialect translation.
---

# Data Platform SQL

Cost per query is real money on every cloud warehouse. A query that scans a
whole table when it should prune a partition is a bug, not a style issue — and
the query plan, not intuition, is where the bug shows up.

## When to reach for this

- A query is slow or expensive and needs diagnosis from its plan/profile
- Writing complex analytical SQL: window functions, recursive CTEs, lateral joins
- Verifying that filters actually prune partitions / cluster keys
- Translating SQL between dialects (Snowflake, BigQuery, Databricks, Redshift, Postgres)

## Principles

1. **Read the plan first.** `EXPLAIN` / query profile before any rewrite —
   optimizing without the plan is guessing, and the guess is usually wrong.
2. **Prune before anything else.** Filters must hit partition/cluster columns
   *bare*: any function or cast wrapped around the column
   (`DATE(created_at) = ...`) disables pruning on most engines. Rewrite as a
   range on the raw column.
3. **Kill unnecessary shuffles.** Broadcast small dimensions, pre-aggregate
   facts before joining, and aggregate before — not after — exploding joins.
4. **Window beats self-join.** `ROW_NUMBER`/`LAG`/`SUM() OVER` replace
   self-joins for dedup, deltas, and running totals at a fraction of the cost.
5. **Know your engine's CTE semantics.** BigQuery and Snowflake may inline or
   re-evaluate CTEs referenced multiple times; Postgres 12+ inlines unless
   `MATERIALIZED`. Don't assume a CTE is computed once.
6. **Measure, don't assume.** Report bytes scanned, rows processed, and wall
   time before/after on a cold (uncached) run — a cached re-run "improvement"
   is a measurement error.

## Symptom → cause → fix

| Plan symptom | Likely cause | Fix |
|---|---|---|
| Full scan despite a date filter | function/cast on partition column | filter on the bare column as a range |
| Bytes scanned ≈ table size on columnar engine | `SELECT *` | project only needed columns (LIMIT does not cut bytes scanned in BigQuery) |
| Output rows ≫ input rows mid-plan | fan-out join (grain mismatch / duplicate keys) | dedupe or pre-aggregate to the join grain first |
| Huge shuffle/exchange step | large-large join or join before aggregation | broadcast the small side; aggregate before joining |
| Spill to disk / memory pressure | wide high-cardinality `GROUP BY` or sort | reduce columns, pre-aggregate, raise warehouse size last |
| Same subquery cost appearing twice | re-evaluated CTE | materialize to a temp table or restructure |

## Dialect translation checklist

- [ ] Result-set parity verified: row counts and checksums of key aggregates match
- [ ] Null ordering (`NULLS FIRST/LAST` defaults differ across engines) checked on every `ORDER BY`
- [ ] Division semantics checked (integer division vs float; divide-by-zero behavior)
- [ ] Timezone handling of `TIMESTAMP` vs `TIMESTAMPTZ`-equivalents made explicit
- [ ] Function mappings verified (`DATEDIFF` argument order, string indexing base, regex flavor)

## Pitfalls

- Trusting a fast second run — the result cache, not the rewrite, was the win
- Adding `DISTINCT` to hide a fan-out join instead of fixing the join grain
- `NOT IN (subquery)` returning zero rows when the subquery yields a NULL —
  use `NOT EXISTS`
- Tuning the query when the table needs clustering/partitioning (fix the layout once,
  not every query)
- Scaling the warehouse up to mask a query that scans 100× the data it needs

---
*Related: `dataplat-etl` (transformation pipelines these queries live in),
`dataplat-viz` (dashboard queries worth tuning), `dataplat-quality`
(reconciliation queries) · domain agent: `dataplat-architect` (warehouse and
storage-format choices) · output/ADR format: `playbook-conventions`*
