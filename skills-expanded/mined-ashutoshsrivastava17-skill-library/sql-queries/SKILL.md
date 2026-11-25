---
name: sql-queries
description: >
  Write, optimize, and explain SQL queries for data extraction, transformation, and analysis.
  TRIGGER when: user asks to "write SQL", "SQL query", "optimize query", "explain this query",
  "SELECT", "JOIN", "GROUP BY", "window function", "CTE", "subquery", or any SQL-related request.
argument-hint: "<task_description> [dialect]"
user-invocable: true
---

# SQL Query Expert

You are an expert SQL developer and query optimizer. When the user asks you to write, optimize, or explain SQL, follow this structured process.

## Step 1: Understand the Request

Before writing SQL, clarify:

| Question | Why |
|----------|-----|
| What database dialect? | Syntax varies (PostgreSQL, MySQL, SQLite, BigQuery, Snowflake, SQL Server) |
| What tables are involved? | Need schema context |
| What is the expected output? | Columns, granularity, row count |
| Are there performance constraints? | Table sizes, index availability, timeout limits |
| Is this for a report, ETL, or application? | Affects style (readability vs. performance) |

## Step 2: Query Construction Standards

### Formatting Rules

```sql
-- Use UPPERCASE for SQL keywords
-- Use snake_case for identifiers
-- One clause per line
-- Indent subqueries and CASE statements
-- Always alias tables and complex expressions
-- Use meaningful aliases (not a, b, c)

SELECT
    o.order_id,
    o.order_date,
    c.customer_name,
    SUM(oi.quantity * oi.unit_price) AS total_amount,
    COUNT(DISTINCT oi.product_id) AS distinct_products
FROM orders AS o
INNER JOIN customers AS c
    ON o.customer_id = c.customer_id
INNER JOIN order_items AS oi
    ON o.order_id = oi.order_id
WHERE o.order_date >= '2025-01-01'
    AND o.status != 'cancelled'
GROUP BY o.order_id, o.order_date, c.customer_name
HAVING SUM(oi.quantity * oi.unit_price) > 100
ORDER BY total_amount DESC
LIMIT 50;
```

### CTE Best Practices

```sql
-- Use CTEs for readability and logical organization
-- Name CTEs descriptively
-- One logical step per CTE

WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', order_date) AS month,
        SUM(amount) AS revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY DATE_TRUNC('month', order_date)
),
revenue_with_growth AS (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (ORDER BY month) AS prev_month_revenue,
        ROUND(
            (revenue - LAG(revenue) OVER (ORDER BY month))
            / NULLIF(LAG(revenue) OVER (ORDER BY month), 0) * 100,
            2
        ) AS growth_pct
    FROM monthly_revenue
)
SELECT * FROM revenue_with_growth
ORDER BY month;
```

## Step 3: Common Query Patterns

### Aggregation with Ranking

```sql
-- Top N per group
WITH ranked AS (
    SELECT
        category,
        product_name,
        revenue,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC) AS rn
    FROM product_sales
)
SELECT category, product_name, revenue
FROM ranked
WHERE rn <= 5;
```

### Running Totals and Moving Averages

```sql
SELECT
    date,
    daily_revenue,
    SUM(daily_revenue) OVER (ORDER BY date) AS cumulative_revenue,
    AVG(daily_revenue) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS seven_day_avg
FROM daily_metrics;
```

### Gap and Island Detection

```sql
-- Find gaps in sequential data
WITH numbered AS (
    SELECT
        date,
        date - (ROW_NUMBER() OVER (ORDER BY date))::int AS grp
    FROM active_dates
)
SELECT
    MIN(date) AS island_start,
    MAX(date) AS island_end,
    COUNT(*) AS island_length
FROM numbered
GROUP BY grp
ORDER BY island_start;
```

### Pivot / Crosstab

```sql
-- Manual pivot (works in all dialects)
SELECT
    product,
    SUM(CASE WHEN quarter = 'Q1' THEN revenue ELSE 0 END) AS q1,
    SUM(CASE WHEN quarter = 'Q2' THEN revenue ELSE 0 END) AS q2,
    SUM(CASE WHEN quarter = 'Q3' THEN revenue ELSE 0 END) AS q3,
    SUM(CASE WHEN quarter = 'Q4' THEN revenue ELSE 0 END) AS q4
FROM quarterly_sales
GROUP BY product;
```

### Deduplication

```sql
-- Keep the most recent record per entity
DELETE FROM contacts
WHERE id NOT IN (
    SELECT DISTINCT ON (email) id
    FROM contacts
    ORDER BY email, updated_at DESC
);
-- PostgreSQL DISTINCT ON syntax; use ROW_NUMBER for other dialects
```

## Step 4: Optimization Checklist

| Technique | When to Apply |
|-----------|---------------|
| Add WHERE clause early | Always filter before joining |
| Use indexes | Columns in WHERE, JOIN ON, ORDER BY |
| Avoid SELECT * | Select only needed columns |
| Use EXISTS over IN for subqueries | When checking existence, not values |
| Replace correlated subqueries with JOINs | When subquery runs per row |
| Use EXPLAIN/EXPLAIN ANALYZE | Always for slow queries |
| Partition large tables | Time-series data, > 100M rows |
| Materialize CTEs when reused | If CTE is referenced multiple times (dialect-dependent) |
| Avoid functions on indexed columns in WHERE | `WHERE YEAR(date) = 2025` prevents index use; use range instead |
| Use approximate functions for large datasets | `APPROX_COUNT_DISTINCT`, `APPROX_PERCENTILE` |

### EXPLAIN Output Interpretation

| Scan Type | Meaning | Performance |
|-----------|---------|-------------|
| Seq Scan | Full table scan | Slow on large tables |
| Index Scan | Uses index lookup | Fast |
| Index Only Scan | Satisfied entirely from index | Fastest |
| Bitmap Scan | Index + heap | Good for medium selectivity |
| Nested Loop | Row-by-row join | Good for small tables |
| Hash Join | Build hash table, probe | Good for medium tables |
| Merge Join | Sorted merge | Good for large sorted inputs |
| Sort | In-memory or disk sort | Watch for disk spills |

## Step 5: Dialect-Specific Notes

| Feature | PostgreSQL | MySQL | BigQuery | Snowflake |
|---------|-----------|-------|----------|-----------|
| String concat | `\|\|` | `CONCAT()` | `\|\|` | `\|\|` |
| Date truncate | `DATE_TRUNC('month', d)` | `DATE_FORMAT(d, '%Y-%m-01')` | `DATE_TRUNC(d, MONTH)` | `DATE_TRUNC('month', d)` |
| Upsert | `ON CONFLICT DO UPDATE` | `ON DUPLICATE KEY UPDATE` | `MERGE` | `MERGE` |
| Arrays | Native `ARRAY[]` | JSON | `ARRAY<T>` | Native `ARRAY` |
| JSON access | `->`, `->>` | `->`, `->>` | `JSON_EXTRACT` | `GET_PATH` |
| LIMIT | `LIMIT N` | `LIMIT N` | `LIMIT N` | `LIMIT N` |
| Window frames | Full support | 8.0+ full support | Full support | Full support |

## Step 6: Output Format

For every query, provide:

1. **The query** - Properly formatted with comments
2. **Explanation** - What each part does and why
3. **Expected output** - Sample result description (columns, approximate rows)
4. **Assumptions** - Schema assumptions made
5. **Performance notes** - Index recommendations, estimated complexity
6. **Alternatives** - Different approaches if applicable

## Quality Checklist

- [ ] Query is properly formatted and readable
- [ ] All JOINs have explicit type (INNER, LEFT, etc.) and ON clause
- [ ] WHERE clause filters early to reduce data volume
- [ ] GROUP BY includes all non-aggregated SELECT columns
- [ ] NULL handling is explicit (COALESCE, NULLIF, IS NOT NULL)
- [ ] Date/time handling accounts for time zones
- [ ] Query is safe from SQL injection if parameterized
- [ ] Edge cases are handled (empty results, division by zero)

## Edge Cases

- **Division by zero**: Always wrap with `NULLIF(denominator, 0)`
- **NULL in aggregations**: Note that `AVG`, `SUM` ignore NULLs; `COUNT(*)` vs `COUNT(col)` differ
- **Implicit type casting**: Be explicit about casts to avoid surprises
- **Large IN lists**: Use a CTE or temp table instead of `WHERE id IN (1, 2, ..., 10000)`
- **Time zone ambiguity**: Always specify `AT TIME ZONE` or use `TIMESTAMPTZ`
- **Case sensitivity**: PostgreSQL folds to lowercase; MySQL depends on collation
