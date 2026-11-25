# SQL Review Skill

Systematic checklist for reviewing SQL queries and dbt models for correctness, performance,
and maintainability.

## Review Checklist

### Correctness

- [ ] **JOIN semantics are intentional.** Is this INNER, LEFT, or FULL OUTER? Does NULL handling match the intent?
- [ ] **Aggregation is at the right grain.** Does GROUP BY match the intended unit of analysis?
- [ ] **DISTINCT is not hiding a fan-out.** If DISTINCT is used, understand why duplicates appeared.
- [ ] **NULL handling is explicit.** `COALESCE`, `NULLIF`, `IS NULL` — are NULLs treated as meaningful or as data quality failures?
- [ ] **Date/time arithmetic is timezone-aware.** Timestamps converted to local time before truncation? UTC vs. local?
- [ ] **Division handles zero denominators.** `NULLIF(denominator, 0)` prevents division-by-zero.
- [ ] **CASE exhaustiveness.** Does the CASE cover all possible values? Is an ELSE clause present?

### Performance

- [ ] **No SELECT *.** Enumerate columns explicitly. SELECT * breaks downstream when the schema changes.
- [ ] **Partition pruning is possible.** The WHERE clause filters on a partition column.
- [ ] **EXPLAIN plan reviewed.** Look for: full table scans, Cartesian joins, nested loops on large tables, high estimated row counts.
- [ ] **Joins on correct types.** Joining VARCHAR to INT causes implicit casts and defeats indexes.
- [ ] **Window functions over full scans.** PARTITION BY on a high-cardinality column forces full shuffles in Spark.
- [ ] **Subquery vs CTE.** CTEs are more readable. In some engines (Snowflake, BigQuery), CTEs are materialized — use subqueries when the optimizer needs to inline.
- [ ] **LIMIT on exploratory queries.** Never run `SELECT * FROM billion_row_table` without LIMIT in development.

### Readability & Maintainability

- [ ] **CTEs are named after what they produce, not how.** `customer_orders` not `cte1` or `step1`.
- [ ] **One logical transformation per CTE.** Each CTE does one thing.
- [ ] **Column aliases are descriptive.** `revenue_usd`, not `rev` or `r`.
- [ ] **No magic numbers.** `WHERE status_code = 4` → what is status 4? Use a named constant or join to a lookup table.
- [ ] **Consistent capitalization.** Keywords UPPER or lower — pick one. Column names snake_case.

### dbt-Specific

- [ ] **Primary key tested.** `not_null` + `unique` tests on the model's grain column.
- [ ] **Foreign key relationships documented.** `relationships` test or description references the upstream model.
- [ ] **`ref()` and `source()` used, not hardcoded table names.** Never `FROM prod.orders.order_events` — use `{{ ref('order_events') }}`.
- [ ] **Incremental models have a filter.** `{% if is_incremental() %} WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }}) {% endif %}`.
- [ ] **No business logic in staging models.** Staging = rename + cast + deduplicate. Business logic belongs in mart/reporting models.

## Common SQL Anti-Patterns

### The N+1 equivalent in SQL: correlated subquery in SELECT

```sql
-- BAD: executes once per row in the outer query
SELECT
    o.order_id,
    (SELECT COUNT(*) FROM order_items oi WHERE oi.order_id = o.order_id) AS item_count
FROM orders o;

-- GOOD: single pass with window function or JOIN
SELECT
    o.order_id,
    COUNT(oi.item_id) AS item_count
FROM orders o
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id;
```

### Fan-out from unintended many-to-many join

```sql
-- BAD: if orders has multiple payments, revenue is double-counted
SELECT
    SUM(p.amount) AS total_revenue
FROM orders o
JOIN payments p ON o.order_id = p.order_id;

-- GOOD: aggregate payments before joining
WITH payment_totals AS (
    SELECT order_id, SUM(amount) AS total_amount
    FROM payments
    GROUP BY order_id
)
SELECT SUM(pt.total_amount) AS total_revenue
FROM orders o
JOIN payment_totals pt ON o.order_id = pt.order_id;
```

### Filtering after aggregation when filtering before is possible

```sql
-- BAD: aggregates all rows, then filters
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING customer_id IN (SELECT customer_id FROM vip_customers);

-- GOOD: filter before aggregating reduces scan size
SELECT o.customer_id, COUNT(*) AS order_count
FROM orders o
INNER JOIN vip_customers v ON o.customer_id = v.customer_id
GROUP BY o.customer_id;
```

### Implicit type coercion in JOIN

```sql
-- BAD: customer_id is VARCHAR, user_id is INT — full scan on both
SELECT * FROM orders o JOIN users u ON o.customer_id = u.user_id;

-- GOOD: cast explicitly and document why the types differ
SELECT * FROM orders o
JOIN users u ON o.customer_id = CAST(u.user_id AS VARCHAR);
-- Note: customer_id stores legacy string IDs; user_id is the new integer PK.
-- Tracked in ADR-0008.
```

## EXPLAIN Output Reading Guide

| Pattern | Risk | Action |
|---|---|---|
| `Seq Scan` on large table | High | Add index, verify partition pruning |
| `Hash Join` on very large tables | Medium | Check join cardinality, consider bucketing |
| `Nested Loop` on large tables | Very High | Rewrite as hash join or add index |
| `Sort` with large estimated rows | Medium | Index if query runs frequently |
| Estimated rows << Actual rows | High | Run `ANALYZE` to update statistics |
| `Broadcast` in Spark on large DF | High | Use sort-merge join instead |
