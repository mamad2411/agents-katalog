---
name: SQL
description: Write efficient queries avoiding common performance traps and subtle bugs.
metadata: {"clawdbot":{"emoji":"🗄️","os":["linux","darwin","win32"]}}
---

# SQL Gotchas

## NULL Traps
- `NOT IN (subquery)` returns empty if subquery contains any NULL — use `NOT EXISTS` instead
- `NULL = NULL` evaluates to NULL, not true — use `IS NULL`, never `= NULL`
- `COUNT(column)` excludes NULLs, `COUNT(*)` counts all rows — behavior differs silently
- Arithmetic with NULL produces NULL — `5 + NULL` is NULL, not 5
- `COALESCE(col, 0)` in WHERE prevents index usage on `col` — filter NULLs separately

## Index Killers
- Functions on indexed columns disable index — `WHERE YEAR(date_col) = 2024` scans full table
- Implicit type conversion prevents index — `WHERE varchar_col = 123` won't use index
- `LIKE '%term'` can't use index — only `LIKE 'term%'` uses index
- `OR` conditions often skip index — rewrite as `UNION` when performance matters
- Composite index `(a, b)` won't help queries filtering only on `b` — leftmost column must be in query

## Performance Traps
- `SELECT *` in subqueries forces unnecessary data retrieval — select only needed columns
- `ORDER BY` on large result sets is expensive — add `LIMIT` or ensure index covers order
- `DISTINCT` is often a sign of bad join — fix the join instead of deduping
- Correlated subqueries run once per outer row — rewrite as JOIN when possible
- `EXISTS` stops at first match, `IN` evaluates all — EXISTS faster for large subqueries

## Join Gotchas
- LEFT JOIN with WHERE condition on right table becomes INNER JOIN — put condition in ON clause instead
- Self-join without proper aliases causes ambiguous column errors — always alias both instances
- Cartesian product from missing JOIN condition multiplies rows — usually a bug, rarely intentional
- Multiple LEFT JOINs can multiply rows unexpectedly — aggregate before joining or use subqueries

## Aggregation Bugs
- Selecting non-grouped columns silently picks random values in MySQL — explicit error in other databases
- HAVING without GROUP BY is valid but confusing — filters on whole result set aggregate
- Window functions execute after WHERE — can't filter on window function result directly
- `AVG(integer_column)` truncates in some databases — cast to decimal first

## Data Modification Dangers
- `UPDATE` or `DELETE` without `WHERE` affects all rows — no confirmation, instant disaster
- `UPDATE ... SET col = (SELECT ...)` sets NULL if subquery returns empty — use COALESCE or validate
- Cascading deletes via foreign keys can delete more than expected — check constraints before bulk delete
- `TRUNCATE` is not transactional in most databases — can't rollback

## Portability
- `LIMIT` syntax differs: MySQL/Postgres use `LIMIT`, SQL Server uses `TOP`, Oracle uses `FETCH FIRST`
- `ILIKE` (case-insensitive) is Postgres-only — use `LOWER()` for portability
- Boolean handling varies — MySQL uses 1/0, Postgres has true/false, SQL Server has no boolean
- `UPSERT` syntax: Postgres `ON CONFLICT`, MySQL `ON DUPLICATE KEY`, SQL Server `MERGE`
- String concatenation: `||` in Postgres/Oracle, `+` in SQL Server, `CONCAT()` everywhere
