---
name: sql-queries
description: Write correct, performant SQL across all major data warehouse dialects (Snowflake, BigQuery, Databricks, PostgreSQL, etc.). Use when writing queries, optimizing slow SQL, translating between dialects, or building complex analytical queries with CTEs, window functions, or aggregations.
user-invocable: false
---

# SQL Queries Skill

Write correct, performant, readable SQL across all major data warehouse dialects.

## Dialect-Specific Reference

> **For full syntax reference across PostgreSQL, Snowflake, BigQuery, Redshift, and Databricks (date/time, strings, JSON, arrays, performance tips), see:**
> `references/dialect-reference.md`

### Quick Dialect Differences

| Feature | PostgreSQL | Snowflake | BigQuery | Redshift | Databricks |
|---------|-----------|-----------|----------|----------|------------|
| Case-insensitive LIKE | `ILIKE` | `ILIKE` | `LOWER()` + `LIKE` | `ILIKE` | `ILIKE` |
| Date add | `+ INTERVAL` | `DATEADD()` | `DATE_ADD()` | `DATEADD()` | `DATE_ADD()` |
| Date diff | `age()` / `-` | `DATEDIFF()` | `DATE_DIFF()` | `DATEDIFF()` | `DATEDIFF()` |
| JSON access | `->>` | `:key::TYPE` | Dot notation | N/A | `:` |
| Array flatten | `UNNEST()` | `LATERAL FLATTEN` | `UNNEST()` | N/A | `EXPLODE()` |
| String agg | `STRING_AGG()` | `LISTAGG()` | `STRING_AGG()` | `LISTAGG()` | `COLLECT_LIST()` |

---

## Common SQL Patterns

### Window Functions

```sql
-- Ranking
ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC)
RANK() OVER (PARTITION BY category ORDER BY revenue DESC)

-- Running totals / moving averages
SUM(revenue) OVER (ORDER BY date_col ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total
AVG(revenue) OVER (ORDER BY date_col ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7d

-- Lag / Lead
LAG(value, 1) OVER (PARTITION BY entity ORDER BY date_col) as prev_value

-- Percent of total
revenue / SUM(revenue) OVER () as pct_of_total
```

### CTEs for Readability

```sql
WITH
base_users AS (
    SELECT user_id, created_at, plan_type
    FROM users
    WHERE created_at >= DATE '2024-01-01' AND status = 'active'
),
user_metrics AS (
    SELECT u.user_id, u.plan_type,
        COUNT(DISTINCT e.session_id) as session_count,
        SUM(e.revenue) as total_revenue
    FROM base_users u
    LEFT JOIN events e ON u.user_id = e.user_id
    GROUP BY u.user_id, u.plan_type
),
summary AS (
    SELECT plan_type, COUNT(*) as user_count,
        AVG(session_count) as avg_sessions, SUM(total_revenue) as total_revenue
    FROM user_metrics GROUP BY plan_type
)
SELECT * FROM summary ORDER BY total_revenue DESC;
```

### Cohort Retention

```sql
WITH cohorts AS (
    SELECT user_id, DATE_TRUNC('month', first_activity_date) as cohort_month FROM users
),
activity AS (
    SELECT user_id, DATE_TRUNC('month', activity_date) as activity_month FROM user_activity
)
SELECT c.cohort_month, COUNT(DISTINCT c.user_id) as cohort_size,
    COUNT(DISTINCT CASE WHEN a.activity_month = c.cohort_month THEN a.user_id END) as month_0,
    COUNT(DISTINCT CASE WHEN a.activity_month = c.cohort_month + INTERVAL '1 month' THEN a.user_id END) as month_1
FROM cohorts c LEFT JOIN activity a ON c.user_id = a.user_id
GROUP BY c.cohort_month ORDER BY c.cohort_month;
```

### Funnel Analysis

```sql
WITH funnel AS (
    SELECT user_id,
        MAX(CASE WHEN event = 'page_view' THEN 1 ELSE 0 END) as step_1,
        MAX(CASE WHEN event = 'signup_complete' THEN 1 ELSE 0 END) as step_2,
        MAX(CASE WHEN event = 'first_purchase' THEN 1 ELSE 0 END) as step_3
    FROM events WHERE event_date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY user_id
)
SELECT COUNT(*) as total,
    SUM(step_1) as viewed, SUM(step_2) as signed_up, SUM(step_3) as purchased,
    ROUND(100.0 * SUM(step_2) / NULLIF(SUM(step_1), 0), 1) as conversion_pct
FROM funnel;
```

### Deduplication

```sql
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY entity_id ORDER BY updated_at DESC) as rn
    FROM source_table
)
SELECT * FROM ranked WHERE rn = 1;
```

---

## Error Handling and Debugging

| Error | Fix |
|-------|-----|
| Syntax errors | Check dialect-specific syntax (e.g., `ILIKE` not in BigQuery) |
| Column not found | Verify names, case sensitivity (PG quoted identifiers) |
| Type mismatches | Cast explicitly: `CAST(col AS DATE)` or `col::DATE` |
| Division by zero | Use `NULLIF(denominator, 0)` |
| Ambiguous columns | Always qualify with table alias in JOINs |
| Group by errors | All non-aggregated columns must be in GROUP BY |
