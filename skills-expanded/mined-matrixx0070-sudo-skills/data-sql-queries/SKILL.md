---
name: data-sql-queries
version: 1.0.0
description: Write correct, performant SQL across warehouse dialects and diagnose queries that are slow, wrong, or expensive.
author: matrixx0070
tags: [sql, warehouse, optimization, bigquery, snowflake, query-tuning]
capabilities: []
---

# data-sql-queries

## When to use

Use this for production-grade SQL — a new query, a refactor, or a fix for one that is slow, wrong, or expensive — on a warehouse (BigQuery, Snowflake, Redshift, Postgres, DuckDB). Correctness first, then performance.

**Not for:** translating a plain-English ask from scratch (use data-write-query), judging whether numbers are statistically real (use data-statistical-analysis), or documenting metric definitions (use data-context-extractor).

## Method

1. **Confirm the contract:** dialect, source tables, grain, expected output columns, and how the result is used. Ambiguity here yields confidently wrong SQL.
2. **Get the grain right.** Know each table's grain before joining. Decision point: if a join key is non-unique, expect fan-out — verify row counts before and after each join.
3. **Structure for readability:** CTEs, one logical step each. Filter early, aggregate late; explicit column lists over `SELECT *`.
4. **Match the dialect.** Date functions, `QUALIFY` (BigQuery/Snowflake), array/struct handling, and window syntax differ — do not port blindly.
5. **Optimize:** prune partitions and clustering keys, push filters down, replace correlated subqueries with joins/windows, pre-aggregate before joining. On BigQuery watch bytes scanned; on Snowflake watch spillage and warehouse size.
6. **Read the plan.** Use `EXPLAIN`/query profile to confirm the fix. Decision point: if you cannot show before/after cost or runtime, do not claim it is faster.

## Example

A `SUM(amount)` doubled after adding an `orders → shipments` join because an order has many shipments (fan-out). Fix: pre-aggregate shipments to order grain first.

```sql
WITH ship AS (            -- collapse to one row per order
  SELECT order_id, COUNT(*) AS n_ship
  FROM shipments GROUP BY order_id
)
SELECT o.order_id, o.amount, s.n_ship   -- amount no longer multiplied
FROM orders o
LEFT JOIN ship s USING (order_id);
```

## Pitfalls

- Trusting a SUM without checking row counts across joins — fan-out is silent.
- `SELECT *` on wide/columnar tables, scanning and paying for unused columns.
- Correlated subqueries where a window function is cheaper and clearer.
- Asserting a speedup with no plan or timing to back it.

## Output format

```
SQL:               <final, dialect labeled, commented per CTE>
Assumptions:       <grain, keys, filters, dialect>
Correctness notes: <fan-out checks; nulls, ties, timezone edge cases>
Performance:       <what changed + measured/plan-based evidence>
```

If the grain is unclear, state your assumption explicitly.
