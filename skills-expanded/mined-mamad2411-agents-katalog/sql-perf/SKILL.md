---
name: sql-perf
description: SQL performance patterns - indexing and query optimization
---

# /sql-perf — SQL Performance

Channel Markus Winand: author of "SQL Performance Explained" and use-the-index-luke.com.

## Core Philosophy

"Indexes are the key to SQL performance. Understand how they work, not just how to create them."

**The Indexing Mantra:** The database doesn't know what you want. Help it by designing proper indexes.

## How Indexes Work

### B-Tree Structure

```
         [50]
        /    \
    [25]      [75]
   /    \    /    \
[10,20] [30,40] [60,70] [80,90]
         ↓
    Leaf nodes contain row pointers
```

- **Logarithmic access**: O(log n) to find any value
- **Range scans**: Efficient once you find the start
- **Ordering**: Index is pre-sorted

### Index Lookup Process

1. **INDEX RANGE SCAN**: Traverse B-tree to find matching entries
2. **TABLE ACCESS BY ROWID**: Fetch actual rows from table
3. **Problem**: Step 2 is random I/O (expensive)

## The Golden Rules

### 1. Index Columns in WHERE Clause

```sql
-- Index on (status)
SELECT * FROM orders WHERE status = 'shipped';  -- Uses index

-- But NOT for functions on columns
SELECT * FROM orders WHERE UPPER(status) = 'SHIPPED';  -- Full scan!

-- Solution: Function-based index or fix the query
CREATE INDEX idx_orders_status_upper ON orders (UPPER(status));
```

### 2. Leftmost Prefix Rule (Composite Indexes)

```sql
-- Index on (a, b, c)
WHERE a = 1                    -- Uses index
WHERE a = 1 AND b = 2          -- Uses index
WHERE a = 1 AND b = 2 AND c = 3 -- Uses index (fully)
WHERE b = 2                    -- Does NOT use index
WHERE a = 1 AND c = 3          -- Uses index for 'a' only
```

### 3. Range Conditions Stop Index Usage

```sql
-- Index on (date, status)
WHERE date = '2024-01-01' AND status = 'shipped'  -- Full index use
WHERE date > '2024-01-01' AND status = 'shipped'  -- Only date part used!

-- Solution: Reorder index
-- Index on (status, date)
WHERE status = 'shipped' AND date > '2024-01-01'  -- Full index use
```

## Index Types for Common Queries

### Equality + Range

```sql
-- Query: WHERE tenant_id = ? AND created_at > ?
-- Best index: (tenant_id, created_at)
-- Equality columns first, then range column
```

### Sorting

```sql
-- Query: WHERE status = 'active' ORDER BY created_at DESC
-- Best index: (status, created_at DESC)
-- Avoids filesort

-- LIMIT optimization
-- Query: WHERE status = 'active' ORDER BY created_at DESC LIMIT 10
-- Same index, but DB can stop after 10 rows
```

### Covering Indexes

```sql
-- Query: SELECT id, name FROM users WHERE email = ?
-- Covering index: (email, id, name)
-- All data from index, no table access needed
CREATE INDEX idx_users_email_covering ON users (email) INCLUDE (id, name);
```

## EXPLAIN Analysis

### Key Metrics

```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 1;
```

| Metric | Good | Bad |
|--------|------|-----|
| Type | eq_ref, ref, range | ALL (full scan) |
| Rows | Small number | Large number |
| Extra | Using index | Using filesort, Using temporary |

### Common Issues

| Problem | Symptom | Fix |
|---------|---------|-----|
| Full table scan | type: ALL | Add appropriate index |
| Filesort | Extra: Using filesort | Index for ORDER BY |
| Temporary table | Extra: Using temporary | Optimize GROUP BY |
| Index not used | Key: NULL | Check index, query |

## Anti-Patterns

### 1. Too Many Indexes

```sql
-- BAD: Separate index for each column
CREATE INDEX idx_a ON t(a);
CREATE INDEX idx_b ON t(b);
CREATE INDEX idx_c ON t(c);

-- Query: WHERE a = 1 AND b = 2 AND c = 3
-- Only ONE index used! Others wasted.

-- GOOD: Composite index for common query patterns
CREATE INDEX idx_abc ON t(a, b, c);
```

### 2. Low Selectivity Indexes

```sql
-- BAD: Index on boolean (only 2 values)
CREATE INDEX idx_active ON users(is_active);
-- Usually not used - full scan might be faster

-- GOOD: Partial index (if supported)
CREATE INDEX idx_active_users ON users(id) WHERE is_active = true;
```

### 3. LIKE with Leading Wildcard

```sql
-- BAD: Cannot use index
WHERE name LIKE '%smith%'

-- BETTER: Use full-text search
WHERE MATCH(name) AGAINST('smith')

-- OR: Only trailing wildcard (uses index)
WHERE name LIKE 'smith%'
```

## Pagination Done Right

### Offset Pagination (AVOID for large offsets)

```sql
-- SLOW: Must scan and discard 10000 rows
SELECT * FROM posts ORDER BY created_at DESC LIMIT 10 OFFSET 10000;
```

### Keyset Pagination (USE THIS)

```sql
-- FAST: Seeks directly to the right position
SELECT * FROM posts
WHERE created_at < '2024-01-15 10:30:00'
ORDER BY created_at DESC
LIMIT 10;

-- Client passes the last seen value for next page
```

## Partial Indexes

```sql
-- Only index the subset you actually query
CREATE INDEX idx_active_orders ON orders(customer_id)
WHERE status = 'active';

-- Smaller index, faster maintenance
-- Only useful for queries that include WHERE status = 'active'
```

## References

- "SQL Performance Explained" - Markus Winand
- use-the-index-luke.com - Free online resource
- modern-sql.com - Modern SQL features
