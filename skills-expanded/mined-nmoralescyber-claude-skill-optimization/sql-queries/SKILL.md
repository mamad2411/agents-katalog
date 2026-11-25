---
name: sql-queries
description: Writes correct, performant, readable SQL across all major data warehouse dialects (Snowflake, BigQuery, Databricks, PostgreSQL, MySQL, Redshift, MS SQL Server). Make sure to use this skill whenever the user says write a query, write SQL, query the warehouse, pull this from [table], join these tables, build a CTE, optimize this query, fix this slow query, translate this from [dialect A] to [dialect B], or describes a data need in natural language that requires database access. Detects warehouse dialect from connected tools or asks if ambiguous. Includes window functions, CTEs, partitioning awareness, query plan reading, and dialect-specific syntax differences. Do NOT use for: NoSQL queries (MongoDB, DynamoDB, Cassandra), regex/text parsing of log files (use raw scripting), in-memory dataframe operations on already-loaded data (use Python/pandas directly), or building dashboards/visualizations (use data:build-dashboard or data:create-viz). Absorbs the deprecated data:write-query skill as of 2026-04-25.
---

# SQL Queries

Writes correct, performant, readable SQL across all major data warehouse dialects.

## When to use vs. adjacent skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Writing or editing any SQL query | Querying NoSQL stores (MongoDB, DynamoDB) — use direct API calls |
| Optimizing a slow query | Working with already-loaded pandas DataFrames — use Python directly |
| Translating between dialects | Profiling raw data shape & quality before querying — use `data:explore-data` |
| Building CTEs, window functions, partitioned scans | Building the visualization or dashboard from query results — use `data:build-dashboard` |
| Reading or explaining a query plan | Validating an analysis end-to-end — use `data:validate-data` |

## Dialect detection

Before writing any non-trivial query, identify the warehouse:
1. Check connected MCPs (BigQuery, Snowflake, Databricks, Postgres connectors).
2. Check workspace memory (CLAUDE.md, data warehouse docs).
3. If still ambiguous, ASK before assuming. `LIMIT` vs. `TOP`, `DATEADD` vs. `DATE_ADD`, `STRING_AGG` vs. `LISTAGG` matter.

## Writing principles

**Readability over cleverness.** A subquery that needs a comment is better as a CTE.

**CTEs over nested subqueries.** Always. The 1990s called and they want their `SELECT FROM (SELECT FROM (SELECT` back.

**Explicit JOIN syntax.** Never use comma-joins (`FROM a, b WHERE a.id = b.id`). Always `FROM a INNER JOIN b ON a.id = b.id`.

**Filter early, aggregate late.** Push WHERE predicates to the deepest CTE that can hold them. Helps the optimizer prune.

**Column lists, not SELECT *.** Except in ad-hoc exploration where you're sampling.

**One CTE = one purpose.** If a CTE does two things, split it.

**Comment the WHY, not the WHAT.** `-- exclude test accounts` is good. `-- where account_type != 'test'` is noise.

## Performance defaults

**Partitioned tables (BigQuery, Snowflake, Databricks):**
- Always include partition column in WHERE
- Use date literals, not functions on the partition column (`WHERE date = '2026-04-01'` not `WHERE EXTRACT(YEAR FROM date) = 2026`)

**Clustered/sorted tables:**
- Order WHERE conditions to use cluster keys first

**Window functions:**
- Be explicit about PARTITION BY and ORDER BY
- Use `ROWS BETWEEN` or `RANGE BETWEEN` to bound the frame
- `QUALIFY` is your friend in BigQuery/Snowflake/Databricks for filtering window results

**Aggregations:**
- `COUNT(DISTINCT x)` is expensive — consider `APPROX_COUNT_DISTINCT` for billions of rows when ±2% accuracy is OK
- `GROUP BY` columns must be in `SELECT` (or use `GROUP BY ALL` if dialect supports it)

**Joins:**
- Smaller table on the right of the join (most optimizers prefer)
- Join on indexed/clustered columns
- Avoid joining on functions (`ON LOWER(a.email) = LOWER(b.email)`) — pre-compute in a CTE

## Dialect quick-reference (most common gotchas)

| Concept | Snowflake | BigQuery | Postgres | Databricks |
|---|---|---|---|---|
| Limit results | `LIMIT n` | `LIMIT n` | `LIMIT n` | `LIMIT n` |
| Date difference | `DATEDIFF(day, a, b)` | `DATE_DIFF(b, a, DAY)` | `b - a` (int days) | `DATEDIFF(b, a)` |
| String concat | `||` or `CONCAT()` | `CONCAT()` or `||` | `||` or `CONCAT()` | `||` or `CONCAT()` |
| Null-safe equal | `EQUAL_NULL(a, b)` | `a IS NOT DISTINCT FROM b` | `IS NOT DISTINCT FROM` | `<=>` |
| Pivoting | `PIVOT(...)` | `PIVOT(...)` | manual `CASE WHEN` | `PIVOT(...)` |
| Regex match | `REGEXP_LIKE` | `REGEXP_CONTAINS` | `~` or `SIMILAR TO` | `RLIKE` |
| Quote identifier | `"col"` | `` `col` `` | `"col"` | `` `col` `` |
| Current timestamp | `CURRENT_TIMESTAMP()` | `CURRENT_TIMESTAMP()` | `NOW()` | `CURRENT_TIMESTAMP()` |
| Array agg | `ARRAY_AGG()` | `ARRAY_AGG()` | `ARRAY_AGG()` | `COLLECT_LIST()` |
| Median | `MEDIAN()` | `APPROX_QUANTILES(x, 2)[OFFSET(1)]` | `PERCENTILE_CONT(0.5)` | `PERCENTILE(x, 0.5)` |

## Query plan reading (when optimizing)

Get the plan, look for:
1. **Full table scans** on large tables → missing partition filter or index
2. **Spilling to disk** (`Spill` operator) → reduce memory pressure with smaller batches or pre-aggregation
3. **Skewed joins** → one partition has 100x rows of others → salt the join key
4. **Cartesian product** → missing or wrong JOIN condition

## Output format

For every query:
1. The query itself, formatted
2. Dialect assumed (and why)
3. Rough row-count expectation
4. Performance notes (which partition/index it leverages, expected runtime ballpark)
5. Test query: a small `LIMIT 10` version the user can run first to validate
