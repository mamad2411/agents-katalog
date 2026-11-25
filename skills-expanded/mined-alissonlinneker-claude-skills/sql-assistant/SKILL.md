---
name: sql-assistant
description: >
  Write, explain, optimize, and debug SQL queries of any complexity. Use this skill whenever
  the user says "write a SQL query", "help me with SQL", "optimize this query", "explain this
  query", "why is this slow", "convert to PostgreSQL/MySQL/BigQuery/SQLite/SQL Server/Snowflake/DuckDB",
  "create a migration", "design the schema", "how do I join these tables", "what index should I add",
  or pastes SQL code for any reason. Also trigger for dbt models, dbt macros, dbt snapshots,
  window functions, CTEs, recursive queries, stored procedures, transactions, JSON queries,
  and any database-related question. Covers PostgreSQL, MySQL, SQLite, BigQuery, Snowflake,
  SQL Server, DuckDB, and dbt. Works equally well for beginners asking basic questions and
  senior engineers optimizing complex analytical queries. Includes schema design patterns
  (star schema, SCD Type 2, event sourcing), transaction isolation, security (SQL injection,
  row-level security), migration safety classification, and performance report cards.
---

# SQL Assistant

The definitive SQL pair-programmer. Writes correct, readable, production-grade SQL from natural
language, explains complex queries in plain terms, diagnoses slow queries without needing
EXPLAIN output (though uses it when provided), designs schemas, writes safe migrations, and
covers every major SQL dialect in production use today.

---

## Input Modes

### 1. Natural Language to SQL

"Give me the top 10 customers by revenue in the last 90 days, grouped by country"

**Action:** Write the complete query with comments, explain choices, note assumptions about schema. Always state assumed table and column names explicitly so the user can correct them.

### 2. SQL to Explanation

User pastes a complex query and asks "what does this do?" or "walk me through this."

**Action:** Explain in plain English, section by section (CTE by CTE, clause by clause), then summarize the business question the query answers. For long queries, produce a numbered list mapping each CTE/subquery to its purpose.

### 3. Optimization

User pastes a slow query or describes a performance problem.

**Action:** Diagnose the bottleneck, explain why it is slow, produce the optimized version, suggest indexes, and generate a **Performance Report Card** (see section below).

### 4. Dialect Conversion

"Convert this from MySQL to PostgreSQL" / "rewrite for BigQuery" / "make this work in SQL Server."

**Action:** Translate syntax, flag semantic differences (NULL handling, date functions, LIMIT vs TOP, string concatenation, type differences), and warn about features that have no direct equivalent.

### 5. Schema Design

"I need to model a subscription billing system" / "how do I structure this many-to-many?"

**Action:** Design tables, relationships, constraints, indexes. Output as runnable CREATE TABLE statements. Apply the appropriate data modeling pattern (star schema, normalized, SCD, etc.) based on the use case.

### 6. Migration Writing

"Add a `deleted_at` column with soft delete logic" / "rename this column without downtime."

**Action:** Write the migration script with rollback. Classify the migration by safety level. Note if the operation requires a lock or causes downtime.

### 7. Debugging

"This query returns wrong results" / "why am I getting duplicate rows?"

**Action:** Diagnose from the query structure. Ask for sample data if needed. Fix the query and explain the root cause.

### 8. Transaction and Concurrency Design

"How do I prevent double-spending?" / "What isolation level should I use?"

**Action:** Design the transaction strategy with the correct isolation level, locking pattern, and retry logic.

### 9. Security Review

"Is this query safe?" / "How do I prevent SQL injection here?"

**Action:** Audit the query or code for injection vectors, recommend parameterization, and suggest GRANT/REVOKE and row-level security where appropriate.

---

## Query Complexity Meter

Every query produced includes a complexity indicator in a comment at the top:

```sql
-- Complexity: Simple | Moderate | Complex | Expert
```

| Level | Criteria |
|-------|----------|
| **Simple** | Single table, basic WHERE/ORDER BY, no joins or aggregations |
| **Moderate** | 1-2 joins, GROUP BY with simple aggregations, basic subqueries |
| **Complex** | 3+ joins, window functions, CTEs, correlated subqueries, HAVING |
| **Expert** | Recursive CTEs, advanced window frames, LATERAL joins, PIVOT/UNPIVOT, multi-step transformations, cross-dialect edge cases |

---

## Query Writing Standards

Every query must follow these rules:

### Correctness First

Never guess at column names. State assumptions clearly:

> "I am assuming your table is named `orders` with columns `customer_id`, `total_amount`, and `created_at`. Adjust if your schema differs."

If the user has provided their schema (DDL, description, or ERD), use exact names from it.

### CTEs for Complexity

When a query has more than 2 joins or 3 aggregation steps, break it into named CTEs. Inline subqueries are hard to read and hard to debug.

```sql
-- Complexity: Complex
-- Top 10 customers by revenue per country in the last 90 days

-- Step 1: Aggregate revenue per customer from recent orders
WITH recent_orders AS (
    SELECT
        customer_id
        , SUM(total_amount) AS revenue
    FROM orders
    WHERE created_at >= NOW() - INTERVAL '90 days'
    GROUP BY customer_id
),
-- Step 2: Rank customers within each country
ranked_customers AS (
    SELECT
        c.name
        , c.country
        , ro.revenue
        , RANK() OVER (PARTITION BY c.country ORDER BY ro.revenue DESC) AS country_rank
    FROM customers c
    JOIN recent_orders ro ON c.id = ro.customer_id
)
SELECT
    name
    , country
    , revenue
FROM ranked_customers
WHERE country_rank <= 10
ORDER BY country, revenue DESC;
```

### No SELECT *

Always name columns explicitly. When teaching, explain why: SELECT * breaks when columns are added/removed, transfers unnecessary data, and prevents covering indexes.

### Inline Comments

One comment above each CTE explaining its purpose. One comment for any non-obvious predicate, calculation, or business rule.

### Consistent Formatting

- Keywords in UPPERCASE: `SELECT`, `FROM`, `WHERE`, `JOIN`, `GROUP BY`, `ORDER BY`, `HAVING`, `WITH`, `ON`, `AND`, `OR`, `CASE`, `WHEN`, `THEN`, `ELSE`, `END`, `AS`, `IN`, `NOT`, `NULL`, `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `ALTER`, `DROP`, `INDEX`, `TABLE`
- 4-space indentation
- One clause per line
- Leading commas for multi-column SELECT lists (prevents trailing comma bugs and makes diffs cleaner)
- JOIN conditions on the same line as JOIN or indented on the next line
- Each CTE separated by a blank comment line for readability

### Aliases

- Table aliases: short but meaningful (`o` for `orders`, `c` for `customers`, `li` for `line_items`)
- Column aliases: descriptive snake_case (`total_revenue`, `order_count`, `first_purchase_date`)
- Always use `AS` for column aliases (some dialects require it; always including it is safer)

---

## Optimization Workflow

When asked to optimize a query, follow this structured process:

### Step 1 — Identify the Bottleneck Pattern

| Pattern | Symptom | Fix |
|---------|---------|-----|
| Full table scan | No WHERE clause on indexed columns | Add index, rewrite predicate |
| N+1 queries | Loop of queries instead of one JOIN | Rewrite as single query with JOIN |
| Non-sargable predicate | `WHERE YEAR(created_at) = 2024` | `WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'` |
| Cartesian product | Missing or incorrect JOIN condition | Add explicit JOIN ON condition |
| Correlated subquery | Subquery re-executes for each outer row | Rewrite as JOIN or window function |
| Missing covering index | Index lookup followed by table access | Add INCLUDE columns or widen index |
| Implicit type cast | `WHERE user_id = '123'` (string vs int) | Match types; cast in the application layer |
| SELECT * | Fetches all columns including BLOBs | Name only needed columns |
| DISTINCT as band-aid | Masking a duplicate-producing JOIN | Fix the JOIN logic instead |
| OR on different columns | `WHERE a = 1 OR b = 2` prevents index use | Rewrite as UNION ALL of two indexed queries |
| LIKE with leading wildcard | `WHERE name LIKE '%smith'` | Full-text search or trigram index |
| Large IN list | `WHERE id IN (1, 2, ..., 10000)` | JOIN against a VALUES list or temp table |
| Sorting without index | `ORDER BY` on non-indexed column with LIMIT | Add index matching the ORDER BY |
| Window function over full table | No PARTITION BY on large dataset | Add PARTITION BY or pre-filter with CTE |

### Step 2 — Produce the Optimized Query

Show **before** and **after** side by side. Explain each change and quantify the expected improvement where possible (e.g., "eliminates full table scan on 10M rows", "reduces from O(n^2) to O(n log n)").

### Step 3 — Index Recommendations

```sql
-- Recommended index for this query pattern:
CREATE INDEX CONCURRENTLY idx_orders_customer_created
ON orders (customer_id, created_at DESC)
INCLUDE (total_amount);

-- CONCURRENTLY avoids table lock (PostgreSQL-specific; omit in MySQL)
-- INCLUDE adds total_amount to leaf pages = covering index = no heap access
-- Column order matters: equality predicates first, then range/sort columns
```

**Index design rules to follow:**

1. Equality columns first, then range/sort columns
2. Most selective column first among equality columns
3. Include columns for covering only if the query is critical and frequently run
4. Partial indexes when the WHERE clause filters a small subset (`WHERE status = 'active'`)
5. Always name indexes descriptively: `idx_{table}_{columns}`

### Step 4 — Interpret EXPLAIN / EXPLAIN ANALYZE Output

When the user provides EXPLAIN output:

- **Identify the most expensive nodes:** Highest `actual time`, largest gap between estimated and actual rows
- **Flag Seq Scans** on tables with more than ~10K rows
- **Flag Nested Loop** on large datasets (usually means a missing index)
- **Flag Hash Join spills to disk** (`Batches > 1` means `work_mem` is too low)
- **Flag large estimation errors** (estimated 1 row, actual 50,000 = stale statistics; recommend `ANALYZE`)
- **Flag Sort operations** that spill to disk (`Sort Method: external merge`)
- **Calculate the actual bottleneck** as a percentage of total execution time
- Present findings as a bulleted list ordered by impact

### Step 5 — Performance Report Card

After optimization, produce a summary block:

```
PERFORMANCE REPORT CARD
-----------------------
Query:        [brief description]
Dialect:      PostgreSQL 16

BEFORE                          AFTER
------                          -----
Full table scan on orders       Index scan via idx_orders_customer_created
Estimated rows: 1,000,000       Estimated rows: 5,200
Seq Scan + Sort                 Index Only Scan (no sort needed)
No covering index               Covering index eliminates heap access

Indexes added:
  - idx_orders_customer_created ON orders (customer_id, created_at DESC) INCLUDE (total_amount)

Risk: LOW — index creation with CONCURRENTLY, no table lock
Estimated improvement: ~100x for this query pattern
```

---

## Window Functions — Dedicated Teaching Mode

Window functions are one of the most powerful and most misunderstood SQL features. When the user asks about them, always explain the anatomy of the OVER() clause before writing the query:

```
FUNCTION() OVER (
    PARTITION BY [column]   -- "reset the calculation for each group"
    ORDER BY [column]       -- "define the row order within each partition"
    ROWS/RANGE BETWEEN ...  -- "define the window frame" (optional, defaults vary)
)
```

### Window Frame Defaults (a common source of bugs)

- With no ORDER BY: the frame is the entire partition (RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
- With ORDER BY: the default frame is RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW — which means SUM() gives a running total, not a partition total. This surprises people.
- ROWS vs RANGE: ROWS counts physical rows. RANGE groups rows with equal ORDER BY values. For most use cases, ROWS is what you want.

### Common Window Function Recipes

```sql
-- Running total
SUM(amount) OVER (
    PARTITION BY customer_id
    ORDER BY created_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
) AS running_total

-- Row number per group (useful for deduplication: keep latest per group)
ROW_NUMBER() OVER (
    PARTITION BY customer_id
    ORDER BY created_at DESC
) AS rn
-- Then: WHERE rn = 1

-- Compare to previous row
LAG(revenue, 1) OVER (
    PARTITION BY region
    ORDER BY month
) AS prev_month_revenue

-- Percentage of group total
100.0 * amount / SUM(amount) OVER (PARTITION BY department) AS pct_of_department

-- Percentile rank
PERCENT_RANK() OVER (ORDER BY score DESC) AS percentile

-- 7-day moving average
AVG(daily_sales) OVER (
    ORDER BY sale_date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
) AS moving_avg_7d

-- Cumulative distinct count (advanced — use COUNT DISTINCT workaround)
-- Note: COUNT(DISTINCT x) OVER (...) is not supported in most dialects.
-- Use DENSE_RANK() as a workaround:
DENSE_RANK() OVER (PARTITION BY group_col ORDER BY value_col)
+ DENSE_RANK() OVER (PARTITION BY group_col ORDER BY value_col DESC)
- 1 AS distinct_count_in_partition

-- First/last value in partition
FIRST_VALUE(product_name) OVER (
    PARTITION BY category
    ORDER BY sales DESC
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
) AS top_product_in_category

-- Gap detection (find missing sequence numbers)
id - ROW_NUMBER() OVER (ORDER BY id) AS gap_group
```

---

## Recursive CTE Patterns

Recursive CTEs solve hierarchical and graph traversal problems. Always include a depth limiter to prevent infinite loops.

### Org Chart / Management Hierarchy

```sql
-- Complexity: Expert
-- Find all reports (direct and indirect) under a given manager

WITH RECURSIVE org_tree AS (
    -- Anchor: the starting manager
    SELECT
        id
        , name
        , manager_id
        , 0 AS depth
        , ARRAY[id] AS path  -- PostgreSQL; use VARCHAR concat in MySQL/SQL Server
    FROM employees
    WHERE id = :manager_id

    UNION ALL

    -- Recursive: find direct reports of current level
    SELECT
        e.id
        , e.name
        , e.manager_id
        , ot.depth + 1
        , ot.path || e.id
    FROM employees e
    JOIN org_tree ot ON e.manager_id = ot.id
    WHERE ot.depth < 20  -- safety: prevent infinite recursion
      AND e.id <> ALL(ot.path)  -- cycle detection
)
SELECT id, name, depth
FROM org_tree
ORDER BY depth, name;
```

### Bill of Materials / Part Explosion

```sql
-- Complexity: Expert
-- Calculate total cost of an assembly including all sub-components

WITH RECURSIVE bom AS (
    SELECT
        component_id
        , component_name
        , quantity
        , unit_cost
        , quantity * unit_cost AS line_cost
        , 1 AS level
    FROM components
    WHERE parent_id = :assembly_id

    UNION ALL

    SELECT
        c.component_id
        , c.component_name
        , c.quantity * b.quantity AS quantity  -- multiply by parent quantity
        , c.unit_cost
        , c.quantity * b.quantity * c.unit_cost AS line_cost
        , b.level + 1
    FROM components c
    JOIN bom b ON c.parent_id = b.component_id
    WHERE b.level < 50
)
SELECT
    component_name
    , SUM(quantity) AS total_quantity
    , SUM(line_cost) AS total_cost
FROM bom
GROUP BY component_name
ORDER BY total_cost DESC;
```

### Category Tree / Breadcrumb Path

```sql
-- Complexity: Complex
-- Build full breadcrumb paths for all categories

WITH RECURSIVE category_tree AS (
    SELECT
        id
        , name
        , parent_id
        , name AS breadcrumb
        , 0 AS depth
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT
        c.id
        , c.name
        , c.parent_id
        , ct.breadcrumb || ' > ' || c.name
        , ct.depth + 1
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.id
    WHERE ct.depth < 20
)
SELECT id, name, breadcrumb, depth
FROM category_tree
ORDER BY breadcrumb;
```

### Date/Number Series Generation

```sql
-- Generate a date series (useful for filling gaps in time series data)
-- PostgreSQL: use generate_series() instead. This is the portable version.

WITH RECURSIVE date_series AS (
    SELECT DATE '2024-01-01' AS dt
    UNION ALL
    SELECT dt + INTERVAL '1 day'
    FROM date_series
    WHERE dt < DATE '2024-12-31'
)
SELECT dt FROM date_series;
```

---

## JSON / JSONB Operations — Cross-Dialect Deep Dive

JSON support varies dramatically across dialects. When the user works with JSON columns, use the correct syntax for their dialect and warn about performance implications.

### PostgreSQL (JSONB)

PostgreSQL has the most mature JSON support. Prefer `jsonb` over `json` (binary storage, indexable, faster operators).

```sql
-- Extract a text value
SELECT data->>'name' AS name FROM users;

-- Extract nested value
SELECT data->'address'->>'city' AS city FROM users;

-- Filter on JSON field
SELECT * FROM users WHERE data->>'role' = 'admin';

-- Check if key exists
SELECT * FROM users WHERE data ? 'email';

-- Check if JSON contains a sub-object
SELECT * FROM users WHERE data @> '{"role": "admin"}'::jsonb;

-- Expand JSON array into rows
SELECT u.id, elem->>'tag' AS tag
FROM users u, jsonb_array_elements(u.data->'tags') AS elem;

-- Aggregate into JSON array
SELECT jsonb_agg(jsonb_build_object('id', id, 'name', name)) FROM users;

-- Update a nested field (immutable — returns new JSONB)
UPDATE users
SET data = jsonb_set(data, '{address,city}', '"New York"'::jsonb)
WHERE id = 1;

-- GIN index for fast @>, ?, ?| , ?& operators
CREATE INDEX idx_users_data ON users USING GIN (data);

-- GIN index on a specific path (smaller, faster for single-key lookups)
CREATE INDEX idx_users_data_role ON users USING GIN ((data->>'role'));
```

### MySQL (JSON)

```sql
-- Extract value (returns JSON-typed value)
SELECT JSON_EXTRACT(data, '$.name') FROM users;
-- Or use shorthand:
SELECT data->'$.name' FROM users;

-- Extract as text (unquoted)
SELECT JSON_UNQUOTE(JSON_EXTRACT(data, '$.name')) FROM users;
-- Or shorthand:
SELECT data->>'$.name' FROM users;  -- MySQL 8.0.21+

-- Filter on JSON field
SELECT * FROM users WHERE JSON_EXTRACT(data, '$.role') = '"admin"';

-- Check if key exists
SELECT * FROM users WHERE JSON_CONTAINS_PATH(data, 'one', '$.email');

-- Expand JSON array into rows
SELECT u.id, jt.tag
FROM users u,
JSON_TABLE(u.data, '$.tags[*]' COLUMNS (tag VARCHAR(255) PATH '$')) AS jt;

-- Multi-valued index (MySQL 8.0.17+)
CREATE INDEX idx_users_tags ON users ((CAST(data->'$.tags' AS CHAR(255) ARRAY)));

-- Generated column + index (general pattern for JSON indexing in MySQL)
ALTER TABLE users ADD COLUMN role VARCHAR(50) GENERATED ALWAYS AS (data->>'$.role') STORED;
CREATE INDEX idx_users_role ON users (role);
```

### BigQuery

```sql
-- Extract scalar value
SELECT JSON_EXTRACT_SCALAR(data, '$.name') AS name FROM users;

-- Extract JSON value (returns JSON type)
SELECT JSON_EXTRACT(data, '$.address') AS address FROM users;

-- Extract from array
SELECT JSON_EXTRACT_SCALAR(tag, '$') AS tag
FROM users, UNNEST(JSON_EXTRACT_ARRAY(data, '$.tags')) AS tag;

-- Query JSON with JSON_QUERY
SELECT JSON_QUERY(data, '$.address') FROM users;

-- BigQuery also supports the dot notation on JSON columns:
SELECT data.name FROM users;  -- if column type is JSON (not STRING)
```

### SQL Server

```sql
-- Extract scalar value
SELECT JSON_VALUE(data, '$.name') AS name FROM users;

-- Extract JSON object/array
SELECT JSON_QUERY(data, '$.address') AS address FROM users;

-- Filter on JSON field
SELECT * FROM users WHERE JSON_VALUE(data, '$.role') = 'admin';

-- Check if valid JSON
SELECT * FROM users WHERE ISJSON(data) = 1;

-- Expand JSON array into rows
SELECT u.id, j.[value] AS tag
FROM users u
CROSS APPLY OPENJSON(u.data, '$.tags') AS j;

-- Shred JSON into relational columns
SELECT *
FROM OPENJSON(@json)
WITH (
    name    NVARCHAR(100)   '$.name',
    age     INT             '$.age',
    city    NVARCHAR(100)   '$.address.city'
);

-- Computed column + index (for JSON indexing in SQL Server)
ALTER TABLE users ADD role AS JSON_VALUE(data, '$.role');
CREATE INDEX idx_users_role ON users (role);
```

### SQLite

```sql
-- Extract value
SELECT json_extract(data, '$.name') FROM users;

-- Shorthand (SQLite 3.38+)
SELECT data->>'$.name' FROM users;

-- Expand JSON array
SELECT u.id, je.value AS tag
FROM users u, json_each(json_extract(u.data, '$.tags')) AS je;
```

### DuckDB

```sql
-- DuckDB has struct/list types AND JSON support
-- Extract from JSON string
SELECT json_extract_string(data, '$.name') FROM users;

-- If stored as native STRUCT, use dot notation
SELECT data.name FROM users;

-- Expand list column
SELECT u.id, UNNEST(u.tags) AS tag FROM users u;
```

### JSON Performance Warning

Always include this warning when users store data in JSON columns:

> **Performance note:** JSON columns bypass the relational model. Queries filtering on JSON fields are slower than queries on native columns unless you create specialized indexes (GIN in PostgreSQL, generated columns in MySQL/SQL Server). If you find yourself filtering, joining, or aggregating on a JSON field frequently, consider extracting it into a proper column.

---

## Dialect Differences — Comprehensive Reference

### Core Syntax

| Feature | PostgreSQL | MySQL | SQL Server | BigQuery | Snowflake | SQLite | DuckDB |
|---------|-----------|-------|------------|---------|-----------|--------|--------|
| String concat | `\|\|` | `CONCAT()` | `+` or `CONCAT()` | `\|\|` or `CONCAT()` | `\|\|` or `CONCAT()` | `\|\|` | `\|\|` or `CONCAT()` |
| Current timestamp | `NOW()` / `CURRENT_TIMESTAMP` | `NOW()` | `GETDATE()` / `SYSDATETIME()` | `CURRENT_TIMESTAMP()` | `CURRENT_TIMESTAMP()` / `SYSDATE()` | `datetime('now')` | `NOW()` / `CURRENT_TIMESTAMP` |
| Limit rows | `LIMIT n OFFSET m` | `LIMIT n OFFSET m` | `TOP n` / `OFFSET m ROWS FETCH NEXT n ROWS ONLY` | `LIMIT n OFFSET m` | `LIMIT n OFFSET m` | `LIMIT n OFFSET m` | `LIMIT n OFFSET m` |
| Regex | `~`, `~*` | `REGEXP` | `LIKE` / `PATINDEX` (no native regex) | `REGEXP_CONTAINS()` | `REGEXP_LIKE()` / `RLIKE` | none | `regexp_matches()` |
| True / false | `TRUE` / `FALSE` | `1` / `0` (or `TRUE`/`FALSE`) | `1` / `0` | `TRUE` / `FALSE` | `TRUE` / `FALSE` | `1` / `0` | `TRUE` / `FALSE` |
| Auto increment | `SERIAL` / `GENERATED ALWAYS AS IDENTITY` | `AUTO_INCREMENT` | `IDENTITY(1,1)` | n/a | `AUTOINCREMENT` / `IDENTITY` | `AUTOINCREMENT` | `GENERATED ALWAYS AS IDENTITY` |
| Upsert | `INSERT ... ON CONFLICT` | `INSERT ... ON DUPLICATE KEY UPDATE` | `MERGE` | `MERGE` | `MERGE` | `INSERT OR REPLACE` / `ON CONFLICT` | `INSERT OR REPLACE` / `ON CONFLICT` |
| Temp tables | `CREATE TEMP TABLE ...` | `CREATE TEMPORARY TABLE ...` | `#table_name` / `CREATE TABLE #t` | session-scoped temp tables | `CREATE TEMPORARY TABLE ...` | `CREATE TEMP TABLE ...` | `CREATE TEMP TABLE ...` |
| CTE syntax | `WITH ... AS` | `WITH ... AS` (8.0+) | `WITH ... AS` | `WITH ... AS` | `WITH ... AS` | `WITH ... AS` | `WITH ... AS` |
| Recursive CTE | `WITH RECURSIVE` | `WITH RECURSIVE` (8.0+) | `WITH ... AS` (no RECURSIVE keyword needed) | `WITH RECURSIVE` | `WITH RECURSIVE` | `WITH RECURSIVE` | `WITH RECURSIVE` |

### Date Functions

| Operation | PostgreSQL | MySQL | SQL Server | BigQuery | Snowflake | SQLite | DuckDB |
|-----------|-----------|-------|------------|---------|-----------|--------|--------|
| Add days | `+ INTERVAL '7 days'` | `+ INTERVAL 7 DAY` | `DATEADD(day, 7, col)` | `DATE_ADD(col, INTERVAL 7 DAY)` | `DATEADD('day', 7, col)` | `datetime(col, '+7 days')` | `+ INTERVAL 7 DAY` |
| Difference | `AGE(a, b)` / `a - b` | `DATEDIFF(a, b)` | `DATEDIFF(day, a, b)` | `DATE_DIFF(a, b, DAY)` | `DATEDIFF('day', a, b)` | `julianday(a) - julianday(b)` | `DATEDIFF('day', a, b)` |
| Truncate | `DATE_TRUNC('month', col)` | `DATE_FORMAT(col, '%Y-%m-01')` | `DATEFROMPARTS(YEAR(col), MONTH(col), 1)` | `DATE_TRUNC(col, MONTH)` | `DATE_TRUNC('month', col)` | `strftime('%Y-%m-01', col)` | `DATE_TRUNC('month', col)` |
| Extract part | `EXTRACT(YEAR FROM col)` | `YEAR(col)` / `EXTRACT(YEAR FROM col)` | `YEAR(col)` / `DATEPART(year, col)` | `EXTRACT(YEAR FROM col)` | `EXTRACT(YEAR FROM col)` / `YEAR(col)` | `strftime('%Y', col)` | `EXTRACT(YEAR FROM col)` |
| Format | `TO_CHAR(col, 'YYYY-MM-DD')` | `DATE_FORMAT(col, '%Y-%m-%d')` | `FORMAT(col, 'yyyy-MM-dd')` / `CONVERT(VARCHAR, col, 23)` | `FORMAT_DATE('%Y-%m-%d', col)` | `TO_CHAR(col, 'YYYY-MM-DD')` | `strftime('%Y-%m-%d', col)` | `strftime(col, '%Y-%m-%d')` |

### Type Casting

| From/To | PostgreSQL | MySQL | SQL Server | BigQuery | Snowflake | SQLite | DuckDB |
|---------|-----------|-------|------------|---------|-----------|--------|--------|
| Cast syntax | `col::TYPE` or `CAST(col AS TYPE)` | `CAST(col AS TYPE)` | `CAST(col AS TYPE)` or `CONVERT(TYPE, col)` | `CAST(col AS TYPE)` / `SAFE_CAST()` | `CAST(col AS TYPE)` / `TRY_CAST()` | `CAST(col AS TYPE)` | `col::TYPE` or `CAST(col AS TYPE)` |
| Safe cast | `(none, use TRY in a function)` | `(none)` | `TRY_CAST(col AS TYPE)` | `SAFE_CAST(col AS TYPE)` | `TRY_CAST(col AS TYPE)` | `(none)` | `TRY_CAST(col AS TYPE)` |

---

## SQL Server / T-SQL Specific Features

SQL Server has unique syntax patterns. When the user's dialect is SQL Server or T-SQL:

### TOP Instead of LIMIT

```sql
-- SQL Server: TOP instead of LIMIT
SELECT TOP 10 name, revenue
FROM customers
ORDER BY revenue DESC;

-- With ties (include rows that tie with the last row)
SELECT TOP 10 WITH TIES name, revenue
FROM customers
ORDER BY revenue DESC;

-- OFFSET/FETCH (SQL Server 2012+, required for pagination)
SELECT name, revenue
FROM customers
ORDER BY revenue DESC
OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;
```

### CROSS APPLY and OUTER APPLY

```sql
-- CROSS APPLY = LATERAL JOIN in PostgreSQL
-- Returns rows from the outer table only when the subquery produces rows
SELECT c.name, latest.order_date, latest.total
FROM customers c
CROSS APPLY (
    SELECT TOP 1 order_date, total
    FROM orders o
    WHERE o.customer_id = c.id
    ORDER BY order_date DESC
) AS latest;

-- OUTER APPLY = LEFT LATERAL JOIN (includes outer rows even if subquery is empty)
SELECT c.name, latest.order_date, latest.total
FROM customers c
OUTER APPLY (
    SELECT TOP 1 order_date, total
    FROM orders o
    WHERE o.customer_id = c.id
    ORDER BY order_date DESC
) AS latest;
```

### PIVOT and UNPIVOT

```sql
-- PIVOT: rows to columns
SELECT customer_id, [2023], [2024], [2025]
FROM (
    SELECT customer_id, YEAR(order_date) AS yr, total
    FROM orders
) AS src
PIVOT (
    SUM(total) FOR yr IN ([2023], [2024], [2025])
) AS pvt;

-- UNPIVOT: columns to rows
SELECT customer_id, year_label, revenue
FROM yearly_revenue
UNPIVOT (
    revenue FOR year_label IN ([y2023], [y2024], [y2025])
) AS unpvt;
```

### Temp Tables and Table Variables

```sql
-- Local temp table (session-scoped, dropped on disconnect)
CREATE TABLE #recent_orders (
    order_id INT,
    customer_id INT,
    total DECIMAL(10,2)
);

-- Global temp table (visible to all sessions, dropped when last session disconnects)
CREATE TABLE ##shared_lookup (
    code VARCHAR(10),
    description VARCHAR(255)
);

-- Table variable (transaction-scoped, no statistics, best for small datasets)
DECLARE @ids TABLE (id INT);
INSERT INTO @ids VALUES (1), (2), (3);

SELECT o.* FROM orders o
JOIN @ids i ON o.id = i.id;
```

### STRING_AGG (SQL Server 2017+)

```sql
-- Concatenate values into a comma-separated list (like GROUP_CONCAT in MySQL)
SELECT
    department
    , STRING_AGG(employee_name, ', ') WITHIN GROUP (ORDER BY employee_name) AS members
FROM employees
GROUP BY department;
```

### TRY_CAST and TRY_CONVERT

```sql
-- Safe type conversion: returns NULL instead of error
SELECT TRY_CAST('not-a-number' AS INT);  -- returns NULL
SELECT TRY_CONVERT(DATE, 'invalid-date');  -- returns NULL
```

### MERGE Statement (SQL Server flavor)

```sql
MERGE INTO target_table AS t
USING source_table AS s
ON t.id = s.id
WHEN MATCHED THEN
    UPDATE SET t.name = s.name, t.updated_at = GETDATE()
WHEN NOT MATCHED BY TARGET THEN
    INSERT (id, name, created_at) VALUES (s.id, s.name, GETDATE())
WHEN NOT MATCHED BY SOURCE THEN
    DELETE;
```

---

## Snowflake-Specific Features

### VARIANT, OBJECT, and ARRAY Types

Snowflake stores semi-structured data (JSON, Avro, Parquet) natively in VARIANT columns.

```sql
-- Create table with VARIANT column
CREATE TABLE events (
    id INTEGER AUTOINCREMENT,
    event_time TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    payload VARIANT
);

-- Insert JSON data
INSERT INTO events (payload)
SELECT PARSE_JSON('{
    "user_id": 42,
    "action": "click",
    "metadata": {"page": "/home", "button": "signup"}
}');

-- Query VARIANT fields (use : and . notation)
SELECT
    payload:user_id::INTEGER AS user_id
    , payload:action::STRING AS action
    , payload:metadata.page::STRING AS page
FROM events;

-- Check type of a VARIANT field
SELECT TYPEOF(payload:user_id) FROM events;
```

### FLATTEN (Expand Nested Arrays/Objects)

```sql
-- FLATTEN replaces UNNEST / json_array_elements
-- Expand a JSON array
SELECT
    e.id
    , f.value::STRING AS tag
FROM events e,
LATERAL FLATTEN(input => e.payload:tags) f;

-- FLATTEN with path into nested arrays
SELECT
    e.id
    , f.value:name::STRING AS item_name
    , f.value:quantity::INTEGER AS quantity
FROM events e,
LATERAL FLATTEN(input => e.payload:order_items) f;

-- Recursive FLATTEN for deeply nested structures
SELECT
    f.path
    , f.key
    , f.value
FROM events e,
LATERAL FLATTEN(input => e.payload, recursive => true) f;
```

### QUALIFY (Filter Window Function Results)

```sql
-- QUALIFY eliminates the need for a subquery/CTE to filter window functions
-- Equivalent of WHERE on a window function result

-- Keep only the latest order per customer
SELECT
    customer_id
    , order_id
    , order_date
    , total
FROM orders
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) = 1;

-- Without QUALIFY (what you have to do in other dialects):
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn
    FROM orders
)
SELECT customer_id, order_id, order_date, total
FROM ranked WHERE rn = 1;
```

### TIME_SLICE (Time-Bucketed Aggregation)

```sql
-- Group timestamps into fixed-width buckets
SELECT
    TIME_SLICE(event_time, 15, 'MINUTE') AS bucket
    , COUNT(*) AS event_count
FROM events
GROUP BY bucket
ORDER BY bucket;
```

### Warehouse Sizing Advice

When the user asks about Snowflake performance, include warehouse sizing guidance:

| Warehouse Size | Credits/Hour | Use Case |
|---------------|-------------|----------|
| X-Small | 1 | Simple queries, small datasets, development |
| Small | 2 | Moderate queries, dashboards |
| Medium | 4 | Complex joins on medium datasets |
| Large | 8 | Heavy ETL, large aggregations |
| X-Large+ | 16+ | Massive data processing, ML training queries |

**Key advice:**
- Scale **up** (bigger warehouse) for complex single queries
- Scale **out** (multi-cluster warehouse) for many concurrent simple queries
- Use `WAREHOUSE_SIZE` and `AUTO_SUSPEND` / `AUTO_RESUME` settings
- Check `QUERY_HISTORY` view for queries that spill to remote storage (sign of too-small warehouse)

```sql
-- Check for queries spilling to disk
SELECT query_id, query_text, bytes_spilled_to_local_storage, bytes_spilled_to_remote_storage
FROM TABLE(information_schema.query_history())
WHERE bytes_spilled_to_remote_storage > 0
ORDER BY bytes_spilled_to_remote_storage DESC
LIMIT 20;
```

---

## DuckDB-Specific Features

DuckDB is an in-process analytical database designed for OLAP. It excels at querying local files directly.

### Direct File Querying

```sql
-- Query Parquet files directly (no COPY/import needed)
SELECT * FROM read_parquet('data/sales_2024.parquet');

-- Query multiple Parquet files with glob
SELECT * FROM read_parquet('data/sales_*.parquet', filename = true);

-- Query CSV files
SELECT * FROM read_csv_auto('data/customers.csv');

-- Query CSV with explicit schema
SELECT * FROM read_csv('data/customers.csv',
    columns = {'id': 'INTEGER', 'name': 'VARCHAR', 'revenue': 'DECIMAL(10,2)'},
    header = true,
    delim = ','
);

-- Query JSON files
SELECT * FROM read_json_auto('data/events.json');

-- Query remote files (S3, HTTP)
SELECT * FROM read_parquet('s3://bucket/path/data.parquet');
SELECT * FROM read_csv_auto('https://example.com/data.csv');

-- Write query results to Parquet
COPY (SELECT * FROM sales WHERE year = 2024) TO 'output.parquet' (FORMAT PARQUET);
```

### ASOF Joins

```sql
-- ASOF JOIN: match the closest row by timestamp (no exact match required)
-- Perfect for joining time series data with different granularities

-- Join stock trades with the most recent quote at or before each trade time
SELECT
    t.trade_time
    , t.symbol
    , t.price AS trade_price
    , q.bid
    , q.ask
FROM trades t
ASOF JOIN quotes q
    ON t.symbol = q.symbol
    AND t.trade_time >= q.quote_time;
```

### LIST, STRUCT, and MAP Types

```sql
-- DuckDB supports nested/complex types natively

-- LIST (array)
SELECT [1, 2, 3] AS my_list;
SELECT list_aggregate([1, 2, 3, 4, 5], 'sum') AS total;  -- 15
SELECT UNNEST([1, 2, 3]) AS val;  -- expands to 3 rows

-- STRUCT (named tuple / object)
SELECT {'name': 'Alice', 'age': 30} AS person;
SELECT person.name FROM (SELECT {'name': 'Alice', 'age': 30} AS person);

-- MAP
SELECT MAP {'key1': 'value1', 'key2': 'value2'} AS my_map;

-- Create table with complex types
CREATE TABLE events (
    id INTEGER,
    tags VARCHAR[],  -- list of strings
    metadata STRUCT(source VARCHAR, version INTEGER)
);

-- Aggregate into lists
SELECT
    customer_id
    , LIST(product_name ORDER BY purchase_date) AS purchase_history
FROM purchases
GROUP BY customer_id;
```

### Friendly SQL Extensions

```sql
-- GROUP BY ALL: automatically groups by all non-aggregate columns
SELECT customer_id, product_category, SUM(amount)
FROM orders
GROUP BY ALL;

-- ORDER BY ALL: order by all selected columns
SELECT DISTINCT country, city FROM addresses ORDER BY ALL;

-- SELECT * EXCLUDE: select all columns except specified
SELECT * EXCLUDE (internal_id, debug_flag) FROM orders;

-- SELECT * REPLACE: select all but replace specific columns
SELECT * REPLACE (ROUND(revenue, 2) AS revenue) FROM sales;

-- FROM-first syntax (experimental)
FROM orders SELECT customer_id, SUM(total) GROUP BY ALL;

-- PIVOT / UNPIVOT (DuckDB-native syntax)
PIVOT orders ON YEAR(order_date) USING SUM(total) GROUP BY customer_id;
```

### Columnar Performance Tips

- DuckDB is columnar: SELECT only the columns you need (SELECT * on wide tables is slow)
- Parquet is the ideal input format (already columnar, pushes filters down)
- Use `EXPLAIN ANALYZE` to check for filter pushdown on Parquet files
- For large datasets, consider partitioned Parquet (Hive-style: `year=2024/month=01/data.parquet`)

---

## dbt — Comprehensive Guide

### Model Materialization Strategies

| Materialization | When to Use | Trade-offs |
|----------------|-------------|------------|
| `view` | Light transformations, always-fresh data | Slow for downstream queries on large data |
| `table` | Moderate data, acceptable staleness | Rebuilds entirely on each run |
| `incremental` | Large fact tables, append-mostly data | Complex to implement correctly; requires unique_key |
| `ephemeral` | Reusable logic, no need to query directly | Cannot be queried outside dbt; compiled inline as CTE |

### Incremental Model Patterns

```sql
-- models/marts/finance/fct_orders.sql
{{
    config(
        materialized='incremental',
        unique_key='order_id',
        incremental_strategy='merge',  -- or 'delete+insert', 'append'
        on_schema_change='sync_all_columns',
        cluster_by=['order_date']  -- Snowflake/BigQuery
    )
}}

WITH source AS (
    SELECT *
    FROM {{ ref('stg_orders') }}
    {% if is_incremental() %}
    -- Only process rows newer than the latest in the existing table
    WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
    {% endif %}
),

enriched AS (
    SELECT
        s.order_id
        , s.customer_id
        , s.order_date
        , s.total_amount
        , c.customer_segment
        , s.updated_at
    FROM source s
    LEFT JOIN {{ ref('dim_customers') }} c ON s.customer_id = c.customer_id
)

SELECT * FROM enriched
```

### Snapshots (SCD Type 2)

```sql
-- snapshots/orders_snapshot.sql
{% snapshot orders_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='order_id',
        strategy='timestamp',
        updated_at='updated_at',
        invalidate_hard_deletes=True
    )
}}

SELECT *
FROM {{ source('raw', 'orders') }}

{% endsnapshot %}
```

This creates `dbt_valid_from`, `dbt_valid_to`, and `dbt_scd_id` columns automatically. Use it when you need to track historical changes (e.g., order status changes, price history).

### Macros

```sql
-- macros/cents_to_dollars.sql
{% macro cents_to_dollars(column_name) %}
    ROUND({{ column_name }} / 100.0, 2)
{% endmacro %}

-- Usage in a model:
SELECT
    order_id
    , {{ cents_to_dollars('total_cents') }} AS total_dollars
FROM {{ ref('stg_orders') }}
```

```sql
-- macros/generate_surrogate_key.sql
{% macro generate_surrogate_key(field_list) %}
    {{ dbt_utils.generate_surrogate_key(field_list) }}
{% endmacro %}
```

```sql
-- macros/grant_select.sql (post-hook macro)
{% macro grant_select(schema, role) %}
    GRANT SELECT ON ALL TABLES IN SCHEMA {{ schema }} TO ROLE {{ role }};
{% endmacro %}
```

### Custom Tests

```sql
-- tests/generic/test_accepted_range.sql
{% test accepted_range(model, column_name, min_value, max_value) %}

SELECT {{ column_name }}
FROM {{ model }}
WHERE {{ column_name }} < {{ min_value }}
   OR {{ column_name }} > {{ max_value }}

{% endtest %}
```

```yaml
# schema.yml usage
models:
  - name: fct_orders
    columns:
      - name: total_cents
        tests:
          - accepted_range:
              min_value: 0
              max_value: 100000000  # $1M max order
```

### Singular Tests (One-off Data Quality Checks)

```sql
-- tests/assert_total_revenue_positive.sql
-- This test fails if any day has negative total revenue

SELECT
    order_date
    , SUM(total_amount) AS daily_revenue
FROM {{ ref('fct_orders') }}
GROUP BY order_date
HAVING SUM(total_amount) < 0
```

### Exposures

```yaml
# models/exposures.yml
exposures:
  - name: weekly_revenue_dashboard
    type: dashboard
    maturity: high
    url: https://looker.company.com/dashboards/42
    description: "Executive weekly revenue dashboard. Refreshed daily at 6am UTC."
    depends_on:
      - ref('fct_orders')
      - ref('dim_customers')
    owner:
      name: Data Team
      email: data-team@company.com
```

### dbt Project Structure (Recommended)

```
models/
  staging/           # 1:1 with source tables. Clean, rename, cast.
    stg_orders.sql
    stg_customers.sql
    _stg_sources.yml
  intermediate/      # Business logic building blocks. Not queried directly.
    int_order_items_aggregated.sql
  marts/             # Business-facing. One folder per domain.
    finance/
      fct_orders.sql
      dim_customers.sql
      _finance_models.yml
    marketing/
      fct_campaigns.sql
snapshots/
  orders_snapshot.sql
macros/
  cents_to_dollars.sql
tests/
  assert_total_revenue_positive.sql
```

### schema.yml Best Practices

```yaml
version: 2

models:
  - name: fct_orders
    description: "One row per order. Source of truth for revenue reporting."
    meta:
      owner: "data-team"
      contains_pii: false
    columns:
      - name: order_id
        description: "Surrogate key. SHA256 of source system order_id."
        tests:
          - unique
          - not_null
      - name: customer_id
        description: "FK to dim_customers"
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id
      - name: order_date
        description: "Date the order was placed (UTC)"
        tests:
          - not_null
      - name: total_amount
        description: "Order total in USD (decimal, not cents)"
        tests:
          - not_null
          - accepted_range:
              min_value: 0
              max_value: 1000000

sources:
  - name: raw
    schema: raw_production
    freshness:
      warn_after: {count: 12, period: hour}
      error_after: {count: 24, period: hour}
    loaded_at_field: _loaded_at
    tables:
      - name: orders
        identifier: raw_orders
```

---

## Data Modeling Patterns

### Star Schema

The workhorse of analytics. One central **fact table** (events/transactions) surrounded by **dimension tables** (descriptive attributes).

```sql
-- Complexity: Complex
-- Star schema for e-commerce analytics

-- Fact table: one row per order line item
CREATE TABLE fct_order_items (
    order_item_id   BIGSERIAL PRIMARY KEY,
    order_id        BIGINT NOT NULL,
    customer_key    BIGINT NOT NULL REFERENCES dim_customers(customer_key),
    product_key     BIGINT NOT NULL REFERENCES dim_products(product_key),
    date_key        INT NOT NULL REFERENCES dim_date(date_key),
    quantity        INT NOT NULL,
    unit_price      DECIMAL(12,2) NOT NULL,
    discount_amount DECIMAL(12,2) NOT NULL DEFAULT 0,
    net_amount      DECIMAL(12,2) NOT NULL
);

-- Dimension: customers
CREATE TABLE dim_customers (
    customer_key    BIGSERIAL PRIMARY KEY,
    customer_id     BIGINT NOT NULL,  -- natural key from source
    name            TEXT NOT NULL,
    email           TEXT,
    segment         TEXT NOT NULL,
    country         TEXT NOT NULL,
    is_current      BOOLEAN NOT NULL DEFAULT TRUE,
    valid_from      TIMESTAMPTZ NOT NULL,
    valid_to        TIMESTAMPTZ  -- NULL = current record
);

-- Dimension: date (pre-populated calendar table)
CREATE TABLE dim_date (
    date_key        INT PRIMARY KEY,  -- YYYYMMDD format
    full_date       DATE NOT NULL,
    year            INT NOT NULL,
    quarter         INT NOT NULL,
    month           INT NOT NULL,
    month_name      TEXT NOT NULL,
    day_of_week     INT NOT NULL,
    day_name        TEXT NOT NULL,
    is_weekend      BOOLEAN NOT NULL,
    is_holiday      BOOLEAN NOT NULL DEFAULT FALSE,
    fiscal_year     INT,
    fiscal_quarter  INT
);

-- Dimension: products
CREATE TABLE dim_products (
    product_key     BIGSERIAL PRIMARY KEY,
    product_id      BIGINT NOT NULL,
    name            TEXT NOT NULL,
    category        TEXT NOT NULL,
    subcategory     TEXT,
    brand           TEXT,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE
);

-- Key indexes for the fact table
CREATE INDEX idx_fct_order_items_customer ON fct_order_items (customer_key);
CREATE INDEX idx_fct_order_items_product ON fct_order_items (product_key);
CREATE INDEX idx_fct_order_items_date ON fct_order_items (date_key);
```

**When to use:** Dashboards, BI tools, ad-hoc analytics. Optimized for aggregation queries.

### Snowflake Schema

Like star schema, but dimensions are normalized into sub-dimensions. Saves storage, adds joins.

```
fct_order_items → dim_products → dim_categories → dim_departments
                → dim_customers → dim_regions → dim_countries
```

**When to use:** When dimension tables are very large and have clear hierarchies. Trade-off: more joins, slower queries, but less redundant data.

### Slowly Changing Dimensions (SCD)

#### SCD Type 1 — Overwrite

Simply update the dimension row. No history preserved.

```sql
-- SCD Type 1: just UPDATE the row
UPDATE dim_customers
SET segment = 'Enterprise', updated_at = NOW()
WHERE customer_id = 42;
```

**When to use:** When historical values do not matter (e.g., fixing a typo in a name).

#### SCD Type 2 — Historical Rows

Create a new row for each change. Track validity with `valid_from` / `valid_to`.

```sql
-- SCD Type 2: expire the old row, insert a new one

-- Step 1: Expire current record
UPDATE dim_customers
SET
    valid_to = NOW()
    , is_current = FALSE
WHERE customer_id = 42
  AND is_current = TRUE;

-- Step 2: Insert new version
INSERT INTO dim_customers (customer_id, name, segment, country, is_current, valid_from, valid_to)
VALUES (42, 'Acme Corp', 'Enterprise', 'US', TRUE, NOW(), NULL);
```

**When to use:** When you need to answer "what was the customer's segment when this order was placed?" Use dbt snapshots to automate this.

#### SCD Type 3 — Previous Value Column

Add a `previous_` column. Only tracks one change.

```sql
ALTER TABLE dim_customers
ADD COLUMN previous_segment TEXT;

UPDATE dim_customers
SET previous_segment = segment, segment = 'Enterprise'
WHERE customer_id = 42;
```

**When to use:** Rarely. Only when you need exactly one level of history.

### Event Sourcing Pattern

Store every state change as an immutable event. Derive current state from the event log.

```sql
-- Events table: immutable append-only log
CREATE TABLE order_events (
    event_id    BIGSERIAL PRIMARY KEY,
    order_id    BIGINT NOT NULL,
    event_type  TEXT NOT NULL CHECK (event_type IN (
        'created', 'item_added', 'item_removed',
        'submitted', 'paid', 'shipped', 'delivered', 'cancelled', 'refunded'
    )),
    payload     JSONB NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by  BIGINT NOT NULL REFERENCES users(id)
);

-- Derive current state from events
WITH latest_events AS (
    SELECT
        order_id
        , event_type
        , payload
        , ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY created_at DESC) AS rn
    FROM order_events
)
SELECT
    order_id
    , event_type AS current_status
    , payload
FROM latest_events
WHERE rn = 1;

-- Rebuild order state at any point in time
SELECT *
FROM order_events
WHERE order_id = :order_id
  AND created_at <= :point_in_time
ORDER BY created_at;
```

**When to use:** Audit trails, financial systems, systems where "undo" is required, debugging production issues.

### CQRS Pattern (Command Query Responsibility Segregation)

Separate the write model (normalized, event-sourced) from the read model (denormalized, optimized for queries).

```sql
-- WRITE SIDE: normalized events table (as above)
-- Insert events via application code

-- READ SIDE: materialized view or separate table, updated by event handlers
CREATE TABLE orders_read_model (
    order_id        BIGINT PRIMARY KEY,
    customer_id     BIGINT NOT NULL,
    customer_name   TEXT NOT NULL,      -- denormalized from customers
    status          TEXT NOT NULL,
    item_count      INT NOT NULL,
    total_amount    DECIMAL(12,2) NOT NULL,
    last_updated_at TIMESTAMPTZ NOT NULL
);

-- In PostgreSQL, you can use a materialized view that refreshes:
CREATE MATERIALIZED VIEW mv_orders AS
SELECT
    o.order_id
    , c.name AS customer_name
    , o.status
    , COUNT(li.id) AS item_count
    , SUM(li.amount) AS total_amount
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN line_items li ON li.order_id = o.order_id
GROUP BY o.order_id, c.name, o.status;

-- Refresh periodically or on-demand:
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_orders;
```

**When to use:** High-read, low-write systems. Dashboard backends. Systems where read and write patterns are fundamentally different.

---

## Transaction Patterns

### Isolation Levels — When to Use Each

| Level | Dirty Reads | Non-Repeatable Reads | Phantom Reads | Use Case |
|-------|------------|---------------------|---------------|----------|
| **READ UNCOMMITTED** | Yes | Yes | Yes | Almost never. Only for rough estimates on data you do not care about consistency for. |
| **READ COMMITTED** | No | Yes | Yes | Default in PostgreSQL. Good for most OLTP workloads. |
| **REPEATABLE READ** | No | No | Yes (varies) | Reports that must see a consistent snapshot. PostgreSQL's implementation also prevents phantoms. |
| **SERIALIZABLE** | No | No | No | Financial transactions, inventory management, anything where correctness is non-negotiable. |

```sql
-- Set isolation level per transaction
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- ... your critical operations ...

COMMIT;
```

### Optimistic Locking (Application-Level)

```sql
-- Add a version column
ALTER TABLE orders ADD COLUMN version INT NOT NULL DEFAULT 1;

-- Read the current version
SELECT id, status, total, version FROM orders WHERE id = 42;
-- Application stores version = 3

-- Update only if version has not changed
UPDATE orders
SET status = 'shipped', version = version + 1, updated_at = NOW()
WHERE id = 42 AND version = 3;
-- If 0 rows affected: another process modified the row. Retry or error.

-- In the application:
-- if affected_rows == 0: raise ConcurrencyError("Order was modified by another process")
```

**When to use:** Low-contention scenarios. Web applications where conflicts are rare.

### Pessimistic Locking (SELECT FOR UPDATE)

```sql
-- Lock the row until this transaction commits or rolls back
BEGIN;

SELECT * FROM inventory
WHERE product_id = 42
FOR UPDATE;  -- blocks other transactions trying to lock this row

-- Safe to modify — no one else can change it
UPDATE inventory
SET quantity = quantity - 1
WHERE product_id = 42
  AND quantity > 0;

COMMIT;
```

```sql
-- SKIP LOCKED: process queues without blocking
-- (PostgreSQL 9.5+, MySQL 8.0+, SQL Server with READPAST hint)
BEGIN;

SELECT * FROM job_queue
WHERE status = 'pending'
ORDER BY created_at
LIMIT 1
FOR UPDATE SKIP LOCKED;

-- Process the job...

UPDATE job_queue SET status = 'processing' WHERE id = :id;
COMMIT;
```

**When to use:** High-contention scenarios. Inventory systems, seat reservations, financial transfers.

### Advisory Locks (PostgreSQL)

```sql
-- Application-level named locks (not tied to a row or table)
-- Useful for ensuring only one process runs a specific job

-- Try to acquire lock (non-blocking, returns true/false)
SELECT pg_try_advisory_lock(hashtext('daily_report_generation'));

-- If true: proceed with the job
-- If false: another process is running it

-- Release when done
SELECT pg_advisory_unlock(hashtext('daily_report_generation'));

-- Or use session-level lock (released on disconnect)
SELECT pg_advisory_lock(12345);  -- blocks until acquired
-- ... do work ...
SELECT pg_advisory_unlock(12345);
```

### Deadlock Prevention

Rules to prevent deadlocks:

1. **Always acquire locks in the same order.** If you lock tables A then B, every transaction must lock A then B (never B then A).
2. **Keep transactions short.** Do reads outside the transaction, lock and write inside.
3. **Use NOWAIT or SKIP LOCKED** to fail fast instead of waiting.
4. **Avoid user interaction inside transactions.** Never hold a lock waiting for user input.

```sql
-- NOWAIT: fail immediately if the row is locked
SELECT * FROM accounts WHERE id = 42 FOR UPDATE NOWAIT;
-- ERROR: could not obtain lock on row
```

---

## Security

### SQL Injection Prevention

**Rule: NEVER concatenate user input into SQL strings.**

```python
# DANGEROUS — SQL injection
cursor.execute(f"SELECT * FROM users WHERE name = '{user_input}'")

# SAFE — parameterized query
cursor.execute("SELECT * FROM users WHERE name = %s", (user_input,))
```

```javascript
// DANGEROUS
db.query(`SELECT * FROM users WHERE id = ${userId}`)

// SAFE — parameterized
db.query('SELECT * FROM users WHERE id = $1', [userId])
```

When reviewing user-provided SQL or code that builds SQL:
- Flag any string concatenation or interpolation in query construction
- Recommend parameterized queries / prepared statements for every dialect
- For dynamic column/table names (which cannot be parameterized), use allowlists:

```python
ALLOWED_SORT_COLUMNS = {'name', 'created_at', 'revenue'}
if sort_column not in ALLOWED_SORT_COLUMNS:
    raise ValueError(f"Invalid sort column: {sort_column}")
query = f"SELECT * FROM users ORDER BY {sort_column}"  # safe: validated against allowlist
```

### GRANT / REVOKE Patterns

```sql
-- Principle of least privilege

-- Create roles for different access levels
CREATE ROLE readonly;
CREATE ROLE readwrite;
CREATE ROLE admin;

-- Read-only: SELECT on all tables in a schema
GRANT USAGE ON SCHEMA public TO readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly;

-- Read-write: SELECT, INSERT, UPDATE, DELETE
GRANT USAGE ON SCHEMA public TO readwrite;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO readwrite;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO readwrite;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO readwrite;

-- Assign roles to users
GRANT readonly TO report_user;
GRANT readwrite TO app_user;
GRANT admin TO dba_user;

-- Revoke access
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM some_user;
```

### Row-Level Security (PostgreSQL)

```sql
-- Enable RLS on a table
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Policy: users can only see their own orders
CREATE POLICY user_orders_policy ON orders
    FOR ALL
    USING (user_id = current_setting('app.current_user_id')::BIGINT);

-- Set the user context in each connection (from your application)
SET app.current_user_id = '42';

-- Now: SELECT * FROM orders; only returns orders for user 42
-- Even admin queries are filtered unless BYPASSRLS is granted

-- Policy for multi-tenant SaaS
CREATE POLICY tenant_isolation ON all_data
    USING (tenant_id = current_setting('app.tenant_id')::INT);
```

### Column-Level Masking

```sql
-- Using views to mask sensitive columns
CREATE VIEW customers_safe AS
SELECT
    id
    , name
    , CONCAT(LEFT(email, 2), '***@', SPLIT_PART(email, '@', 2)) AS email_masked
    , CONCAT('***-**-', RIGHT(ssn, 4)) AS ssn_masked
    , created_at
FROM customers;

-- Grant access to the view, not the base table
GRANT SELECT ON customers_safe TO analyst_role;
REVOKE SELECT ON customers FROM analyst_role;
```

### Dynamic Data Masking (SQL Server)

```sql
-- SQL Server native column masking
ALTER TABLE customers
ALTER COLUMN email ADD MASKED WITH (FUNCTION = 'email()');

ALTER TABLE customers
ALTER COLUMN ssn ADD MASKED WITH (FUNCTION = 'partial(0,"XXX-XX-",4)');

ALTER TABLE customers
ALTER COLUMN salary ADD MASKED WITH (FUNCTION = 'random(1000, 9999)');

-- Users without UNMASK permission see masked values
GRANT UNMASK TO trusted_analyst;
```

---

## Migration Safety Levels

Every migration operation is classified by risk. Always include this classification when writing migrations.

### SAFE (Green) — No Downtime, No Lock Risk

These operations are safe to run during peak traffic:

| Operation | Notes |
|-----------|-------|
| Add nullable column | `ALTER TABLE ADD COLUMN ... DEFAULT NULL` (instant in modern Postgres/MySQL) |
| Add index CONCURRENTLY | PostgreSQL: `CREATE INDEX CONCURRENTLY` (does not lock writes) |
| Create new table | No impact on existing tables |
| Add CHECK constraint NOT VALID | PostgreSQL: adds constraint without validating existing rows |
| Add column with DEFAULT (Postgres 11+, MySQL 8.0.12+) | Stored as metadata, instant |

```sql
-- SAFE: Add a nullable column
-- Safety: GREEN — instant metadata change, no table rewrite, no lock
ALTER TABLE orders ADD COLUMN notes TEXT;

-- SAFE: Add index without locking writes
-- Safety: GREEN — CONCURRENTLY prevents write lock (PostgreSQL)
CREATE INDEX CONCURRENTLY idx_orders_status ON orders (status);

-- Rollback:
DROP INDEX CONCURRENTLY idx_orders_status;
```

### CAUTION (Yellow) — Brief Lock or Moderate Risk

These operations acquire brief locks or may cause issues under specific conditions:

| Operation | Notes |
|-----------|-------|
| Add NOT NULL constraint | Requires scanning all rows to validate. Use NOT VALID + VALIDATE separately in Postgres. |
| Add foreign key | Requires checking all existing rows. Use NOT VALID in Postgres. |
| Add index (non-concurrent) | Locks writes for the duration of index build |
| Backfill data in existing column | UPDATE on large table: do in batches |
| Rename column | Some ORMs/applications may break. Requires coordinated deploy. |

```sql
-- CAUTION: Add NOT NULL constraint safely in PostgreSQL
-- Safety: YELLOW — split into two steps to minimize lock time

-- Step 1: Add constraint without validating existing data (instant, brief lock)
ALTER TABLE orders ADD CONSTRAINT orders_status_not_null
    CHECK (status IS NOT NULL) NOT VALID;

-- Step 2: Validate existing data (scans table but does NOT lock writes)
ALTER TABLE orders VALIDATE CONSTRAINT orders_status_not_null;

-- Rollback:
ALTER TABLE orders DROP CONSTRAINT orders_status_not_null;
```

```sql
-- CAUTION: Backfill data in batches to avoid long locks and WAL bloat
-- Safety: YELLOW — batch updates to prevent long-running transactions

-- Do NOT do this:
-- UPDATE orders SET notes = 'none' WHERE notes IS NULL;  -- locks millions of rows

-- DO this instead (PostgreSQL example):
DO $$
DECLARE
    batch_size INT := 10000;
    rows_updated INT;
BEGIN
    LOOP
        UPDATE orders
        SET notes = 'none'
        WHERE id IN (
            SELECT id FROM orders
            WHERE notes IS NULL
            LIMIT batch_size
            FOR UPDATE SKIP LOCKED
        );
        GET DIAGNOSTICS rows_updated = ROW_COUNT;
        RAISE NOTICE 'Updated % rows', rows_updated;
        EXIT WHEN rows_updated = 0;
        COMMIT;
        PERFORM pg_sleep(0.1);  -- brief pause to let other transactions through
    END LOOP;
END $$;
```

### DANGER (Red) — Downtime Risk, Data Loss Risk, or Long Lock

These operations can cause downtime, data loss, or extended locks. Require maintenance windows and/or careful planning:

| Operation | Notes |
|-----------|-------|
| Drop column | Irreversible data loss. Some databases lock the table. |
| Drop table | Irreversible. Always backup first. |
| Alter column type | May rewrite the entire table (hours on large tables). |
| Rename table | Breaks all queries referencing the old name. |
| Add column with volatile DEFAULT (old Postgres/MySQL) | Rewrites entire table. |
| TRUNCATE | Irreversible unless inside a transaction (PostgreSQL supports transactional TRUNCATE). |

```sql
-- DANGER: Change column type
-- Safety: RED — table rewrite, exclusive lock for duration
-- Strategy: use a parallel column approach for zero-downtime

-- Step 1: Add new column
ALTER TABLE orders ADD COLUMN total_new DECIMAL(12,2);

-- Step 2: Backfill in batches (see CAUTION pattern above)

-- Step 3: Application reads from COALESCE(total_new, total_old)

-- Step 4: Once backfill is complete and app is deployed:
ALTER TABLE orders RENAME COLUMN total_old TO total_deprecated;
ALTER TABLE orders RENAME COLUMN total_new TO total;

-- Step 5: After verification period, drop the old column
ALTER TABLE orders DROP COLUMN total_deprecated;

-- Rollback (before Step 5):
ALTER TABLE orders RENAME COLUMN total TO total_new;
ALTER TABLE orders RENAME COLUMN total_deprecated TO total;
ALTER TABLE orders DROP COLUMN total_new;
```

### Migration Template

Every migration should follow this format:

```sql
-- Migration: [descriptive name]
-- Safety: GREEN | YELLOW | RED
-- Estimated duration: [instant | seconds | minutes | hours]
-- Locks: [none | brief ACCESS EXCLUSIVE | sustained ACCESS EXCLUSIVE]
-- Requires maintenance window: YES | NO
-- Reversible: YES | NO

-- === FORWARD MIGRATION ===
BEGIN;

-- [migration SQL here]

COMMIT;

-- === ROLLBACK ===
BEGIN;

-- [rollback SQL here]

COMMIT;
```

---

## Schema Design Principles

When designing schemas from scratch, follow these conventions:

### Naming

1. **Tables:** plural snake_case (`users`, `order_items`, `product_categories`)
2. **Columns:** singular snake_case (`user_id`, `total_amount`, `created_at`)
3. **Primary keys:** `id` (BIGSERIAL in Postgres, BIGINT AUTO_INCREMENT in MySQL, IDENTITY in SQL Server)
4. **Foreign keys:** `{referenced_table_singular}_id` (e.g., `user_id`, `product_id`)
5. **Boolean columns:** prefix with `is_` or `has_` (`is_active`, `has_subscription`)
6. **Timestamps:** `created_at`, `updated_at`, `deleted_at` (not `creation_date` or `date_created`)
7. **Indexes:** `idx_{table}_{columns}` (`idx_orders_customer_id`, `idx_orders_status_created_at`)
8. **Constraints:** `chk_{table}_{description}` (`chk_orders_total_positive`)

### Standard Columns

```sql
CREATE TABLE orders (
    id              BIGSERIAL PRIMARY KEY,
    -- business columns here --
    user_id         BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status          TEXT NOT NULL CHECK (status IN ('pending', 'paid', 'cancelled', 'refunded')),
    total_cents     INTEGER NOT NULL CHECK (total_cents >= 0),  -- money as integers, never FLOAT
    currency        TEXT NOT NULL DEFAULT 'USD' CHECK (LENGTH(currency) = 3),
    -- standard timestamps --
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at      TIMESTAMPTZ DEFAULT NULL  -- NULL = active (soft delete)
);

-- Foreign key index (PostgreSQL does NOT auto-create these)
CREATE INDEX idx_orders_user_id ON orders (user_id);

-- Common query pattern index
CREATE INDEX idx_orders_status_created ON orders (status, created_at DESC);

-- Partial index for active records only
CREATE INDEX idx_orders_active ON orders (created_at DESC) WHERE deleted_at IS NULL;
```

### Money

- **NEVER use FLOAT or DOUBLE for money.** Floating point arithmetic causes rounding errors.
- Store as integer cents/minor units (`total_cents INTEGER`) or `DECIMAL(12,2)` / `NUMERIC(12,2)`.
- Store the currency code alongside the amount.
- Format for display in the application layer, never in SQL.

### Enums vs Check Constraints vs Lookup Tables

| Approach | Pros | Cons |
|----------|------|------|
| `CHECK (status IN (...))` | Simple, no join needed | Changing values requires ALTER TABLE |
| `CREATE TYPE status_enum AS ENUM (...)` (Postgres) | Type safety | Adding values requires ALTER TYPE; removing is hard |
| Lookup/reference table | Most flexible, can add metadata | Requires JOIN; slightly more complex |

**Recommendation:** Use CHECK constraints for small, stable sets (< 10 values that rarely change). Use lookup tables for larger or frequently changing sets.

---

## Common Beginner Pitfalls — Proactive Warnings

When writing queries for users who appear to be learning SQL, proactively flag these issues:

| Pitfall | Problem | Fix |
|---------|---------|-----|
| `JOIN` without `ON` | Produces Cartesian product (every row x every row) | Always specify the JOIN condition |
| `WHERE` on aggregated column | `WHERE COUNT(*) > 5` does not work | Use `HAVING COUNT(*) > 5` |
| `COUNT(*)` vs `COUNT(column)` | `COUNT(column)` excludes NULLs; `COUNT(*)` counts all rows | Be explicit about which you want |
| Date `=` comparison | `WHERE date = '2024-01-15'` misses rows with time components | Use `>= AND <` range, or `DATE_TRUNC` |
| `NOT IN` with NULLs | If the subquery returns any NULL, the entire NOT IN returns zero rows | Use `NOT EXISTS` instead |
| `UNION` vs `UNION ALL` | `UNION` deduplicates (slow); `UNION ALL` keeps all rows | Use `UNION ALL` unless you specifically need dedup |
| Modifying and reading same table | `DELETE FROM t WHERE id IN (SELECT id FROM t WHERE ...)` can behave unpredictably | Use a CTE or temporary result |
| `GROUP BY` with non-aggregated columns | Selecting columns not in GROUP BY or an aggregate function | Add to GROUP BY or wrap in an aggregate |
| String comparison collation | `'A' = 'a'` varies by database and collation settings | Be explicit: use `LOWER()` or specify collation |
| NULL in equality | `WHERE column = NULL` never matches | Use `WHERE column IS NULL` |
| Implicit JOIN (comma syntax) | `FROM a, b WHERE a.id = b.a_id` — old syntax, easy to forget the WHERE | Use explicit `JOIN ... ON` syntax |

---

## Output Style Rules

1. **Always produce runnable SQL** — never pseudocode, never partial snippets (unless the user explicitly asks for a fragment).
2. **Include the Complexity Meter** comment at the top of every query.
3. For long queries, add **inline comments** explaining each CTE or non-obvious clause.
4. When teaching, use the pattern: **explain the concept in isolation, then apply it to their specific data.**
5. When optimizing, show **before and after** plus a **Performance Report Card**.
6. **Flag destructive operations** explicitly with a warning: `-- WARNING: This will permanently delete data. Are you sure?`
7. For migrations, always provide a **rollback script** and **safety classification**.
8. When multiple dialects could apply, ask which dialect the user is using. If they do not specify, default to PostgreSQL and note that in the output.
9. When the user provides a schema, use their exact table and column names.
10. When the user does not provide a schema, state assumptions clearly and use realistic example names.
