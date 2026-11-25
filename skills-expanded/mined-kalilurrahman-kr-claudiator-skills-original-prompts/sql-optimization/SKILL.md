---
name: sql-optimization
description: Optimize slow SQL queries with indexing, query rewriting, and execution plan analysis. Outputs before/after metrics and index strategies.
argument-hint: [slow query, database type, table sizes]
allowed-tools: Read, Write, Bash
---

# SQL Query Optimization

Transform slow queries into fast ones through indexing, rewriting, and execution plan tuning. Not guesswork — systematic analysis using EXPLAIN, index strategies, and measurable improvements.

## Process

1. **Identify slow queries.** Logs, APM tools, pg_stat_statements.
2. **Analyze execution plan.** EXPLAIN ANALYZE shows actual cost.
3. **Add indexes.** Covering indexes, composite indexes, partial indexes.
4. **Rewrite query.** Avoid anti-patterns (N+1, SELECT *, OR conditions).
5. **Update statistics.** ANALYZE table for query planner accuracy.
6. **Consider denormalization.** Materialized views, summary tables.
7. **Measure improvement.** Before/after execution time.

## Output Format

### Query Optimization: [Query Description]

**Database:** PostgreSQL 15  
**Table Size:** 5M rows  
**Before:** 8.5 seconds  
**After:** 45 milliseconds  
**Improvement:** 189x faster  
**Method:** Composite index + query rewrite

---

## Common Anti-Patterns

### 1. Missing Index (Table Scan)

**Slow:**
```sql
SELECT * FROM orders WHERE user_id = 123;
-- Execution time: 2500ms (scans all 5M rows)
```

**EXPLAIN Output:**
```
Seq Scan on orders  (cost=0.00..125000.00 rows=100 width=200)
  Filter: (user_id = 123)
```

**Fix: Add Index**
```sql
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

**Fast:**
```sql
SELECT * FROM orders WHERE user_id = 123;
-- Execution time: 15ms
```

**EXPLAIN Output:**
```
Index Scan using idx_orders_user_id on orders  (cost=0.42..12.50 rows=100)
  Index Cond: (user_id = 123)
```

**Improvement:** 167x faster

---

### 2. SELECT * (Transfer Unnecessary Data)

**Slow:**
```sql
SELECT * FROM orders WHERE status = 'pending';
-- Returns 50 columns, 100KB per row
```

**Fast:**
```sql
SELECT id, user_id, total, created_at 
FROM orders 
WHERE status = 'pending';
-- Returns 4 columns, 200 bytes per row
```

**Improvement:** 500x less data transferred

---

### 3. N+1 Query Problem

**Slow:**
```python
# Django ORM
orders = Order.objects.all()  # 1 query
for order in orders:
    print(order.user.name)    # N queries (1 per order)
# Total: 1 + 1000 = 1001 queries
```

**Fast:**
```python
orders = Order.objects.select_related('user').all()  # 1 query with JOIN
for order in orders:
    print(order.user.name)  # No additional queries
# Total: 1 query
```

**SQL Generated:**
```sql
SELECT orders.*, users.* 
FROM orders 
INNER JOIN users ON orders.user_id = users.id;
```

**Improvement:** 1001 queries → 1 query

---

### 4. OR Conditions (Index Not Used)

**Slow:**
```sql
SELECT * FROM orders 
WHERE status = 'pending' OR status = 'processing';
-- Index on status not used efficiently
```

**Fast:**
```sql
SELECT * FROM orders 
WHERE status IN ('pending', 'processing');
-- Index scan
```

**Even Better:**
```sql
SELECT * FROM orders WHERE status = 'pending'
UNION ALL
SELECT * FROM orders WHERE status = 'processing';
-- Uses index twice
```

---

### 5. Function on Indexed Column

**Slow:**
```sql
SELECT * FROM users 
WHERE LOWER(email) = 'user@example.com';
-- Index on email not used (function applied)
```

**Fix: Functional Index**
```sql
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
```

**Or: Rewrite Query**
```sql
SELECT * FROM users 
WHERE email = 'user@example.com'  -- Assume already lowercase
   OR email = 'USER@EXAMPLE.COM';
```

---

### 6. LIKE with Leading Wildcard

**Slow:**
```sql
SELECT * FROM products 
WHERE name LIKE '%phone%';
-- Cannot use index (leading wildcard)
```

**Fix: Full-Text Search**
```sql
-- PostgreSQL
CREATE INDEX idx_products_name_fts ON products 
USING GIN (to_tsvector('english', name));

SELECT * FROM products 
WHERE to_tsvector('english', name) @@ to_tsquery('phone');
```

**Or: Trigram Index**
```sql
CREATE EXTENSION pg_trgm;
CREATE INDEX idx_products_name_trgm ON products 
USING GIN (name gin_trgm_ops);

SELECT * FROM products 
WHERE name ILIKE '%phone%';
-- Now uses GIN index
```

---

## Index Strategies

### Composite Index (Multiple Columns)

**Query:**
```sql
SELECT * FROM orders 
WHERE user_id = 123 
  AND status = 'pending' 
ORDER BY created_at DESC;
```

**Optimal Index:**
```sql
CREATE INDEX idx_orders_user_status_created 
ON orders(user_id, status, created_at DESC);
```

**Order Matters:**
- Most selective column first (user_id)
- Equality conditions before range
- ORDER BY column last

**Wrong Index:**
```sql
CREATE INDEX idx_orders_bad 
ON orders(created_at, user_id, status);
-- Less efficient: created_at first is not selective
```

---

### Covering Index (Include Columns)

**Query:**
```sql
SELECT id, total, created_at 
FROM orders 
WHERE user_id = 123;
```

**Index-Only Scan:**
```sql
CREATE INDEX idx_orders_user_covering 
ON orders(user_id) 
INCLUDE (id, total, created_at);
```

**Benefit:** No need to access table (index contains all data)

---

### Partial Index (Filtered)

**Query:**
```sql
SELECT * FROM orders WHERE status = 'pending';
```

**Smaller Index:**
```sql
CREATE INDEX idx_orders_pending 
ON orders(created_at) 
WHERE status = 'pending';
-- Index only pending orders (10% of table)
```

**Benefit:** Smaller index, faster updates

---

### Expression Index

**Query:**
```sql
SELECT * FROM orders 
WHERE DATE(created_at) = '2024-01-15';
```

**Index:**
```sql
CREATE INDEX idx_orders_date 
ON orders(DATE(created_at));
```

---

## Query Rewriting Patterns

### Join Elimination

**Slow:**
```sql
SELECT users.name, COUNT(orders.id)
FROM users
LEFT JOIN orders ON users.id = orders.user_id
GROUP BY users.id;
```

**Fast:**
```sql
SELECT users.name,
       (SELECT COUNT(*) FROM orders WHERE user_id = users.id) as order_count
FROM users;
```

---

### Subquery to JOIN

**Slow:**
```sql
SELECT * FROM orders
WHERE user_id IN (
    SELECT id FROM users WHERE country = 'US'
);
-- Subquery executed for each row
```

**Fast:**
```sql
SELECT orders.* 
FROM orders
INNER JOIN users ON orders.user_id = users.id
WHERE users.country = 'US';
```

---

### Limit Before Join

**Slow:**
```sql
SELECT users.*, orders.*
FROM users
LEFT JOIN orders ON users.id = orders.user_id
ORDER BY users.created_at DESC
LIMIT 10;
-- Joins all users then limits
```

**Fast:**
```sql
SELECT users.*, orders.*
FROM (
    SELECT * FROM users 
    ORDER BY created_at DESC 
    LIMIT 10
) users
LEFT JOIN orders ON users.id = orders.user_id;
-- Limits first, then joins
```

---

## Execution Plan Analysis

### Reading EXPLAIN ANALYZE

```sql
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 123;
```

**Output:**
```
Index Scan using idx_orders_user_id on orders  
  (cost=0.42..12.50 rows=100 width=200) 
  (actual time=0.025..0.138 rows=95 loops=1)
  Index Cond: (user_id = 123)
Planning Time: 0.123 ms
Execution Time: 0.165 ms
```

**Key Metrics:**
- `cost=0.42..12.50` — Estimated cost (startup..total)
- `rows=100` — Estimated rows
- `actual time=0.025..0.138` — Actual time (ms)
- `rows=95` — Actual rows returned
- `Execution Time: 0.165 ms` — Total query time

**Red Flags:**
- `Seq Scan` — Table scan (add index)
- `rows=100` vs `rows=10000` — Bad cardinality estimate (run ANALYZE)
- `loops=1000` — Nested loop executed many times

---

### Common Scan Types

| Scan Type | Speed | When Used |
|-----------|-------|-----------|
| Index Scan | Fast | Small result set with index |
| Index Only Scan | Fastest | Covering index |
| Bitmap Index Scan | Medium | Multiple index conditions |
| Seq Scan | Slow | No index or full table needed |
| Nested Loop | Varies | Small join, good for small tables |
| Hash Join | Medium | Large join |
| Merge Join | Fast | Sorted inputs |

---

## Statistics & Vacuuming

### Update Table Statistics

```sql
-- Manual analyze
ANALYZE orders;

-- Verbose output
ANALYZE VERBOSE orders;

-- Auto-vacuum settings (postgresql.conf)
autovacuum = on
autovacuum_analyze_threshold = 50
autovacuum_analyze_scale_factor = 0.1
```

**When:** After bulk inserts, deletes, or updates

---

### Find Bloated Tables

```sql
SELECT 
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) AS external_size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 20;
```

---

## Materialized Views

**Slow:**
```sql
SELECT 
  DATE(created_at) as date,
  COUNT(*) as orders,
  SUM(total) as revenue
FROM orders
GROUP BY DATE(created_at);
-- Scans 5M rows every query
```

**Fast: Materialized View**
```sql
CREATE MATERIALIZED VIEW daily_revenue AS
SELECT 
  DATE(created_at) as date,
  COUNT(*) as orders,
  SUM(total) as revenue
FROM orders
GROUP BY DATE(created_at);

CREATE INDEX idx_daily_revenue_date ON daily_revenue(date);

-- Refresh daily
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_revenue;
```

**Query:**
```sql
SELECT * FROM daily_revenue WHERE date = '2024-01-15';
-- 5ms instead of 2500ms
```

---

## Partitioning (Very Large Tables)

```sql
-- Range partition by date
CREATE TABLE orders (
    id BIGSERIAL,
    created_at TIMESTAMPTZ NOT NULL,
    ...
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2024_01 PARTITION OF orders
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE orders_2024_02 PARTITION OF orders
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Indexes on each partition
CREATE INDEX idx_orders_2024_01_user ON orders_2024_01(user_id);
CREATE INDEX idx_orders_2024_02_user ON orders_2024_02(user_id);
```

**Benefit:** Queries on recent data only scan recent partition

---

## Monitoring Slow Queries

### PostgreSQL: pg_stat_statements

```sql
-- Enable extension
CREATE EXTENSION pg_stat_statements;

-- Find slowest queries
SELECT 
  query,
  calls,
  total_exec_time / 1000 AS total_seconds,
  mean_exec_time / 1000 AS avg_seconds,
  max_exec_time / 1000 AS max_seconds
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

### MySQL: Slow Query Log

```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;  -- Log queries > 1s

-- Analyze with pt-query-digest
pt-query-digest /var/log/mysql/slow.log
```

---

## Testing

```sql
-- Before optimization
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;
-- Note execution time: 2500ms

-- Add index
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- After optimization
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;
-- Note execution time: 15ms

-- Improvement: 167x faster
```

## Rules

- Run EXPLAIN ANALYZE before and after optimization — measure actual improvement, not guesswork.
- Index WHERE clause columns — most important optimization for reads.
- Composite index column order: equality → range → sort — maximizes index usage.
- Avoid SELECT * — retrieve only needed columns, reduces I/O.
- Update statistics with ANALYZE after bulk changes — query planner needs accurate cardinality.
- Covering indexes for read-heavy queries — include all SELECT columns in index.
- Partial indexes for filtered queries — smaller index, faster updates.
- N+1 queries must use JOINs or prefetch — 100x fewer roundtrips.
- Materialized views for expensive aggregations — refresh periodically, query is instant.
- Partition tables > 100M rows — query only relevant partitions, not entire table.
