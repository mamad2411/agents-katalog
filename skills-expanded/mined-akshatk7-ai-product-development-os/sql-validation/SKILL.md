---
name: sql-validation
description: >
  Validate SQL queries for correctness, performance, and common pitfalls before
  execution. Use this skill whenever the user writes, edits, debugs, or reviews
  a SQL query — including Snowflake, Trino, or general ANSI SQL. Also trigger
  when the user asks to "check my query", "review this SQL", "find bugs in my
  query", "validate SQL", or mentions SQL correctness, query optimization, or
  data quality checks.
owners:
  - analytics
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Validating SQL

Static analysis of SQL queries to catch correctness issues, performance anti-patterns, and safety risks — before a single row is scanned.

## When to Validate

Run validation whenever you see a SQL query that is about to be executed, or when the user explicitly asks for a review. If errors are found, recommend fixing them before execution. If only warnings or info items are found, note them but allow execution to proceed.

## How to Validate

Read the query carefully and check it against each category below. You do not need to execute the query or connect to any database — this is purely static analysis of the query text.

Present findings as a numbered list grouped by severity. Each finding should include:
- The **line number** (or relevant clause) where the issue occurs
- A **clear explanation** of what is wrong and why it matters
- A **concrete fix** — not just "consider changing this", but actual rewritten SQL

## Validation Checks

### 1. Fanout Join Detection (ERROR)

Joining two tables where the join key is not unique on at least one side causes row multiplication — one of the most common and hardest-to-debug data quality issues.

Look for:
- JOIN on columns that are unlikely to be unique (e.g., `user_id` in a fact table) without prior deduplication or aggregation
- Multiple JOINs that compound the fanout (A -> B -> C where B has multiple rows per A key)
- Missing DISTINCT or GROUP BY that would mask the fanout

Suggest: `QUALIFY ROW_NUMBER() OVER (PARTITION BY <key> ORDER BY <tiebreaker>) = 1`, or a CTE that deduplicates first.

### 2. NULL Handling (WARNING)

NULL behaves counter-intuitively in SQL and is a frequent source of silent data loss.

Look for:
- `WHERE col = NULL` or `WHERE col != NULL` — should be `IS NULL` / `IS NOT NULL`
- `NOT IN (subquery)` where the subquery column could contain NULLs — this silently returns zero rows. Use `NOT EXISTS` instead, or add `WHERE col IS NOT NULL` inside the subquery.
- `COUNT(col)` silently excludes NULLs; `COUNT(*)` does not. Flag when the distinction matters.
- JOIN conditions on nullable columns without COALESCE
- NULLs in GROUP BY — each NULL forms its own group in some engines

### 3. Date and Time Boundary Errors (ERROR)

Date logic is deceptively tricky, especially when mixing DATE and TIMESTAMP types.

Look for:
- `BETWEEN '2024-01-01' AND '2024-01-31'` on TIMESTAMP columns — this misses times after midnight on the 31st. Use `>= ... AND < next_day` instead.
- Mixing DATE and TIMESTAMP types without explicit CAST
- Comparing TIMESTAMP_NTZ with TIMESTAMP_LTZ (timezone mismatch)
- Hardcoded dates that should use `CURRENT_DATE` / `DATEADD` for dynamic ranges
- Off-by-one in `DATEADD` / `DATEDIFF` (especially around week boundaries)

### 4. Aggregation Errors (ERROR)

Look for:
- SELECT columns not in GROUP BY and not wrapped in an aggregate function
- `COUNT(DISTINCT col)` on very high-cardinality columns in large datasets (expensive — flag as performance concern)
- `SUM` / `AVG` on columns that could contain non-numeric values or mixed types
- `GROUP BY 1, 2, 3` using ordinal positions — fragile if the SELECT list changes. Prefer explicit column names.

### 5. Performance Anti-Patterns (WARNING)

These won't produce wrong results, but they can be extremely expensive.

Look for:
- `SELECT *` in production or analytical queries — pulls unnecessary columns across the network
- `LIKE '%pattern%'` with a leading wildcard — cannot use indexes, triggers full scan
- `ORDER BY` without `LIMIT` on large result sets
- Correlated subqueries that could be rewritten as JOINs or window functions
- `UNION` instead of `UNION ALL` when duplicates are not a concern (UNION forces a sort + dedup)
- Subqueries nested more than 3 levels deep — consider refactoring into CTEs for readability and optimizer clarity

### 6. Data Type Mismatches (WARNING)

Implicit type coercion can produce unexpected results and hurt performance.

Look for:
- JOIN conditions comparing VARCHAR to NUMBER — some engines will coerce, but it disables pruning
- String-to-date comparisons without `TO_DATE` or `CAST`
- Integer division truncation: `COUNT(*) / total` should cast one operand to `FLOAT` or use `::FLOAT`

### 7. Window Function Issues (WARNING)

Look for:
- `ROW_NUMBER()` without `ORDER BY` — non-deterministic, results change between runs
- Window functions without `PARTITION BY` — operates over the entire dataset, which is usually unintended
- `ORDER BY` on a non-deterministic column (e.g., `created_at` with ties) — use a tiebreaker
- `RANGE` vs `ROWS` frame confusion — `RANGE` is the default and groups ties differently than `ROWS`

### 8. Snowflake-Specific Pitfalls (INFO)

These are valid Snowflake patterns that frequently catch people out.

- `FLATTEN` without `LATERAL` — Snowflake requires `LATERAL` for table functions in FROM
- `PARSE_JSON` on columns that may contain invalid JSON — use `TRY_PARSE_JSON` instead
- VARIANT column comparisons without explicit `::STRING` or `::NUMBER` cast
- `MERGE` with non-deterministic match (multiple source rows match one target row)
- `COPY INTO` without `ON_ERROR` handling
- `GET_PATH` / dot notation on VARIANT returning NULL silently when the path does not exist

### 9. Safety Checks (ERROR)

These are dangerous operations that warrant immediate attention.

- `UPDATE` or `DELETE` without a `WHERE` clause — will modify/delete every row in the table
- `TRUNCATE` or `DROP` appearing outside an explicit DDL context
- `INSERT` without an explicit column list — fragile to schema changes
- `GRANT` / `REVOKE` statements — flag for review

## Output Format

Present results using this structure:

```
## SQL Validation Results

### Errors (must fix)
1. **Fanout join on line 12**: `orders` JOIN `order_items` on `order_id` — `order_items` has multiple rows per `order_id`. This will multiply your row count.
   **Fix:** Aggregate `order_items` in a CTE first, or add `QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY created_at DESC) = 1`.

### Warnings (should review)
2. **NULL-unsafe NOT IN on line 8**: `WHERE id NOT IN (SELECT id FROM excluded)` — if `excluded.id` contains any NULLs, this returns zero rows.
   **Fix:** Use `NOT EXISTS` or add `WHERE id IS NOT NULL` in the subquery.

### Info
3. **Hardcoded date on line 5**: Consider using `DATEADD(DAY, -7, CURRENT_DATE)` instead of `'2024-01-15'` for maintainability.

**Summary**: 1 error, 1 warning, 1 info item. Fix the fanout join before executing.
```

If the query passes all checks, say so:

```
## SQL Validation Results

No issues found. The query looks correct and ready to execute.
```

## What This Skill Does NOT Do

- It does not execute queries or connect to databases.
- It does not review DDL or schema design — that is data-modelling territory.
- It does not run `EXPLAIN` plans or analyse runtime performance — that requires execution.
