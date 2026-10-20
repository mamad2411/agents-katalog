---
name: sql-write
description: Write a SQL query that answers a specific question; parameterized, dialect-aware, readable, with the assumed schema documented inline.
---

# sql-write

> Translate a question into a SQL query. Output the query, the schema assumptions, and how to verify the result.

## When to use

- A specific analytical or operational question needs SQL.
- A query is being copied around and needs to be canonical.

## Inputs

- The question in English.
- Database dialect (Postgres, MySQL, SQLite, DuckDB, BigQuery, Snowflake, Redshift). Different dialects have different functions (`DATE_TRUNC` vs `DATE_FORMAT`, `INTERVAL '7 days'` vs `INTERVAL 7 DAY`).
- Schema: table and column names. If unknown, ask before guessing.

## Procedure

1. **Restate the question**. "How many active users in the last 7 days, by country" → exact rows, exact columns, exact grain.
2. **Identify the dialect**. Different `DATE_TRUNC` / window-function syntax.
3. **Sketch tables and joins** before writing the query. Document the join keys.
4. **Use CTEs** for readability over deeply-nested subqueries. Each CTE has one purpose; name it after the purpose.
5. **Parameterize**. Use placeholders (`$1`, `?`, `:name`) — never string-concatenate user input.
6. **Indexed predicates first**. If you know the indexed column, put the equality predicate on it in the join / where.
7. **Aggregations** — explicit `GROUP BY <columns>`; don't rely on MySQL's loose grouping. Use `HAVING` for filtering aggregates, `WHERE` for filtering rows.
8. **Window functions** when the question is "top-N per group" or "running sum / rank".

## Output

```sql
-- Active users in the last 7 days by country.
-- Dialect: Postgres 15. Grain: country code.
-- Tables: events(user_id, created_at, country_code).
-- Assumes country_code is indexed; (user_id, created_at) is indexed.

WITH recent_active AS (
  SELECT DISTINCT user_id, country_code
  FROM   events
  WHERE  created_at >= now() - INTERVAL '7 days'
)
SELECT
  country_code,
  COUNT(*) AS active_users
FROM   recent_active
GROUP BY country_code
ORDER BY active_users DESC;
```

Verification:

- Spot-check one country with a smaller window (`'1 day'`); the count for the 7-day query should be ≥ the 1-day count for the same country.
- Schema match: confirm `events.country_code` is non-null for the rows you care about; otherwise add an `IS NOT NULL` predicate and discuss the bias.

## Anti-patterns to avoid

- `SELECT *` in production queries.
- String-concatenated user input.
- `BETWEEN` with timestamps when one side is exclusive in the intent.
- Implicit type coercion in joins (`varchar = int`).
