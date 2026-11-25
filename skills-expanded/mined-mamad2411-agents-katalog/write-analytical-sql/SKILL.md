---
name: write-analytical-sql
description: Writes accurate, readable, dialect-correct analytical SQL — CTEs, window functions, aggregations, and joins — across Postgres, BigQuery, Snowflake, and Databricks.
when_to_use: When the user needs an analytical SQL query written or translated — build a report query with CTEs/window functions/aggregations, express business logic in SQL, or translate a query between warehouse dialects (Postgres/BigQuery/Snowflake/Databricks).
---

## When to Use

Use when the task is to **write or translate analytical SQL** — reports, metrics, cohort/funnel logic, dedup, running totals, rankings — in Postgres, BigQuery, Snowflake, or Databricks SQL.

- Use for: report queries with CTEs/window functions, expressing business logic in SQL, dialect translation preserving semantics.
- Do NOT use for: query performance tuning (use optimize-sql-query) or schema migrations (out of scope).
- Hard rule: **never invent column or table names.** If schema is unknown, inspect or ask before writing — a wrong column name is worse than a question.

## Steps

1. **Lock the dialect first.** If unstated, ask or infer from connection/context. Dialect changes date functions, dedup syntax (QUALIFY), array/struct access, and string concat — get it wrong and the query won't parse.
2. **Get the real schema.** Inspect via `information_schema.columns` / `\d table` / `DESCRIBE table`, or ask. Confirm for every joined table: the **grain** (one row per what?), the join keys, and which columns are nullable. Grain ambiguity is the #1 source of wrong numbers.
3. **Decompose into named CTEs**, one logical step per CTE (filter → join → aggregate → rank → final select). Name them for intent (`active_users`, `daily_revenue`), not `cte1`. Keep the final `SELECT` thin.
4. **Pick the right join type and verify grain.** Before any join, confirm the right side is unique on the join key. If it can have multiple rows, you have **fan-out** — pre-aggregate the right side in a CTE first, or the join multiplies your fact rows and inflates every `SUM`/`COUNT`.
5. **Use window functions instead of self-joins** for ranking, running totals, dedup, period-over-period:
   - Dedup / latest-per-group: `ROW_NUMBER() OVER (PARTITION BY id ORDER BY updated_at DESC)` then keep `= 1`.
   - Running total: `SUM(x) OVER (PARTITION BY ... ORDER BY dt ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`.
   - Period-over-period: `LAG(metric) OVER (ORDER BY period)`.
   - Be explicit about the frame — default frame is `RANGE UNBOUNDED PRECEDING AND CURRENT ROW`, which silently sums ties together; use `ROWS` when you mean row-by-row.
6. **Guard aggregates against NULL and the empty set.**
   - `COUNT(col)` skips NULLs; `COUNT(*)` doesn't — pick deliberately. Distinct users = `COUNT(DISTINCT user_id)`.
   - `SUM` over zero rows returns NULL, not 0 — wrap with `COALESCE(SUM(x), 0)` when a numeric default is expected.
   - `AVG` ignores NULLs in the denominator; if NULL means zero, `COALESCE` before averaging.
   - Filtered aggregates: `COUNT(*) FILTER (WHERE cond)` (Postgres/Databricks) or `COUNT(CASE WHEN cond THEN 1 END)` (portable, works everywhere).
7. **Apply dialect specifics** (see table below) for dates, dedup, arrays, and row limiting.
8. **For translation:** map semantics, not text. Re-express date math, dedup, array/struct access, and `QUALIFY`/`LIMIT`/`TOP` per the target dialect. Re-check that NULL and casting behavior still match the source intent.
9. **Format for review:** keywords uppercase, leading commas or trailing — pick one, one join per line, CTEs separated by blank lines. Add a one-line comment stating what the query answers and its output grain.
10. **Validate** on a sample if a DB is reachable (see Verify).

### Dialect cheat-sheet

| Need | Postgres | BigQuery | Snowflake | Databricks (Spark SQL) |
|---|---|---|---|---|
| Current date | `CURRENT_DATE` | `CURRENT_DATE()` | `CURRENT_DATE` | `current_date()` |
| Truncate to month | `DATE_TRUNC('month', d)` | `DATE_TRUNC(d, MONTH)` | `DATE_TRUNC('month', d)` | `date_trunc('month', d)` |
| Date diff (days) | `d2 - d1` | `DATE_DIFF(d2, d1, DAY)` | `DATEDIFF(day, d1, d2)` | `datediff(d2, d1)` |
| Add interval | `d + INTERVAL '7 day'` | `DATE_ADD(d, INTERVAL 7 DAY)` | `DATEADD(day, 7, d)` | `date_add(d, 7)` |
| Dedup top-1 per group | `ROW_NUMBER()` in CTE, filter outer | `QUALIFY ROW_NUMBER()...=1` | `QUALIFY ROW_NUMBER()...=1` | `QUALIFY ROW_NUMBER()...=1` |
| Row limit | `LIMIT n` | `LIMIT n` | `LIMIT n` (not `TOP`) | `LIMIT n` |
| String concat | `\|\|` or `CONCAT` | `CONCAT` (`\|\|` ok) | `\|\|` or `CONCAT` | `\|\|` or `concat` |
| Safe divide | `x / NULLIF(y,0)` | `SAFE_DIVIDE(x,y)` | `x / NULLIF(y,0)` | `x / NULLIF(y,0)` |
| Array element | `arr[1]` (1-based) | `arr[OFFSET(0)]` (0-based) | `arr[0]` (0-based) | `arr[0]` (0-based) |

## Common Errors

- **Postgres has no `QUALIFY`.** Wrap the window function in a CTE/subquery and filter `WHERE rn = 1` in the outer query. BigQuery/Snowflake/Databricks support `QUALIFY` directly.
- **`GROUP BY` ordinals.** Postgres/Snowflake/Databricks accept `GROUP BY 1, 2`; prefer explicit column names in CTEs so a column reorder doesn't silently regroup.
- **Fan-out from a one-to-many join silently inflates `SUM`/`COUNT`.** Always pre-aggregate the many-side to the fact's grain before joining. Symptom: totals are too high and don't reconcile.
- **`COUNT(DISTINCT)` is the fix when fan-out already happened**, but it's a band-aid — fixing the grain is correct. Don't reach for `DISTINCT` to hide a join bug.
- **`WHERE` on a `LEFT JOIN`ed table turns it into an `INNER JOIN`.** Filters on the right table belong in the `ON` clause, or the unmatched (NULL) rows get dropped.
- **`NULL` never equals `NULL`.** `x = NULL` is always false — use `IS NULL` / `IS DISTINCT FROM`. `NOT IN (subquery with a NULL)` returns zero rows; use `NOT EXISTS`.
- **BigQuery arrays are 0-based with `OFFSET`; Postgres is 1-based.** Off-by-one when translating array access is a silent wrong-row bug.
- **Integer division truncates** in Postgres/Snowflake/Databricks (`5/2 = 2`). Cast one side: `x::numeric / y` or `CAST(x AS FLOAT64)/y` (BigQuery).
- **Window frame defaults to `RANGE`, which lumps tied `ORDER BY` rows together** in running totals. Use `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` for true row-by-row cumulation.
- **`HAVING` filters after aggregation, `WHERE` before.** Putting an aggregate condition in `WHERE` errors; putting a row filter in `HAVING` works but scans more than needed.
- **Timezone drift:** BigQuery `TIMESTAMP` is UTC; casting to `DATE` without a timezone shifts day boundaries. Be explicit: `DATE(ts, 'Asia/Bangkok')`.

## Verify

- **Parse/compile:** if a DB is reachable, run the query (or `EXPLAIN` it) — confirm it executes and column names resolve.
- **Grain check:** run `SELECT key, COUNT(*) FROM result GROUP BY key HAVING COUNT(*) > 1` on the claimed unique key; expect zero rows. If not, you have fan-out or a dedup miss.
- **Reconcile a total:** compute one headline metric two independent ways (e.g. `SUM` of the detail vs. a separate aggregate) and confirm they match — catches join inflation.
- **NULL/empty edge:** confirm the query returns a sensible value (0 vs NULL) when a group has no rows, per the `COALESCE` decision in Step 6.
- **Translation parity:** if translating, run source and target against the same sample and diff the result sets — they must be identical, not just "look right."
- State the **output grain and what the query answers** in one line so the caller can sanity-check intent against numbers.
