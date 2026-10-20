---
name: sql-query-assistant
description: Use when writing, optimizing, or debugging SQL queries for enterprise databases. Includes best practices for performance, debugging, complex query patterns, and database-agnostic approaches. Based on SQL certification standards and database performance tuning best practices.
license: MIT
---

# SQL Query Assistant

## Overview

This skill provides guidance for writing, optimizing, and debugging SQL queries in enterprise environments. It covers best practices for performance, query patterns, and database-specific considerations. Based on SQL certification standards and database performance tuning best practices.

## When to Use

**Use this skill when:**

- Writing complex SQL queries for reporting and analytics
- Optimizing slow database queries (performance tuning)
- Debugging query performance issues with EXPLAIN plans
- Designing database schemas and indexes
- Working with PostgreSQL, MySQL, SQL Server, or SQLite
- Need to understand query execution plans and optimization
- Implementing window functions for complex calculations
- Creating CTEs for readable multi-step queries
- Building efficient JOIN strategies
- Implementing pagination for large datasets
- Writing subqueries and correlated subqueries
- Optimizing aggregate functions and GROUP BY clauses
- Implementing database-specific optimizations
- Setting up database indexes for query optimization
- Creating materialized views for performance
- Implementing query caching strategies
- Debugging deadlocks and locking issues
- Writing efficient batch processing queries
- Implementing data warehouse star schemas
- Building ETL pipelines with SQL
- Creating database views for complex joins
- Implementing recursive queries for hierarchical data
- Optimizing full-text search queries
- Setting up database partitioning strategies

**Do NOT use this skill when:**

- Simple CRUD operations that can use an ORM
- Using an ORM for basic queries (use ORM-specific skill)
- Database administration tasks (backup, restore, user management)
- Database migration scripting (use database migration skill)
- NoSQL database queries (use NoSQL-specific skill)

## Core Patterns

### Query Optimization Checklist

```sql
-- 1. Use EXPLAIN to analyze query plan
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 1;

-- 2. Add indexes for frequently queried columns
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- 3. Avoid SELECT *
SELECT id, name, email FROM users WHERE active = true;

-- 4. Use JOINs instead of subqueries when possible
SELECT o.id, u.name
FROM orders o
JOIN users u ON o.user_id = u.id;

-- 5. Limit result sets
SELECT * FROM orders WHERE created_at > '2024-01-01' LIMIT 100;
```

### Common Query Patterns

```sql
-- Pagination with offset
SELECT * FROM products
ORDER BY created_at DESC
LIMIT 50 OFFSET 0;

-- Window functions
SELECT
  name,
  salary,
  RANK() OVER (ORDER BY salary DESC) as rank
FROM employees;

-- CTE for complex queries
WITH sales_by_region AS (
  SELECT region, SUM(amount) as total_sales
  FROM sales
  GROUP BY region
)
SELECT region, total_sales
FROM sales_by_region
WHERE total_sales > 10000;
```

## Database-Specific Considerations

### PostgreSQL

- Use `EXPLAIN (ANALYZE, BUFFERS)` for detailed analysis
- Consider partial indexes for filtered queries
- Use `COPY` for bulk imports
- Enable `pg_stat_statements` for query monitoring

### MySQL

- Use `EXPLAIN FORMAT=JSON` for detailed analysis
- Consider index merge optimization
- Use `INSERT DELAYED` for non-critical inserts
- Enable slow query log

### SQL Server

- Use `SET SHOWPLAN_ALL ON` for execution plan
- Consider filtered indexes
- Use `BULK INSERT` for bulk operations
- Monitor with DMVs

## Common Mistakes

### ❌ Bad: N+1 Query Problem

```sql
-- Get users and their orders
SELECT * FROM users;  -- Query 1
-- Then for each user:
SELECT * FROM orders WHERE user_id = ?;  -- Query N
```

### ✅ Good: JOIN or IN clause

```sql
-- Single query with JOIN
SELECT u.*, o.*
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- Or use IN with subquery
SELECT * FROM orders
WHERE user_id IN (SELECT id FROM users);
```

### ❌ Bad: Using Functions in WHERE Clause

```sql
-- Prevents index usage
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';
```

### ✅ Good: Pre-process value

```sql
-- Allows index usage
SELECT * FROM users WHERE email = 'test@example.com';
-- Application converts to lowercase before query
```

## Real-World Impact

**Before this skill:**

- Queries taking 10+ seconds
- No understanding of execution plans
- N+1 query patterns
- Missing indexes

**After this skill:**

- Queries under 100ms
- Understanding of query plans
- Proper JOIN usage
- Strategic indexing

## SQL Formatting Standards

All SQL queries MUST follow this format:

```sql
-- ✅ CORRECT: Uppercase keywords, one column per line, indented JOINs
SELECT
    p.id,
    p.name,
    p.email,
    r.name AS role_name
FROM
    users p
    INNER JOIN roles r ON p.role_id = r.id
WHERE
    p.status = 'active'
    AND p.deleted_at IS NULL
ORDER BY
    p.created_at DESC
LIMIT 20 OFFSET 0;
```

```sql
-- ❌ WRONG: Lowercase, everything on one line, inline JOINs
select p.id, p.name, p.email, r.name as role_name from users p inner join roles r on p.role_id = r.id where p.status = 'active' and p.deleted_at is null order by p.created_at desc limit 20 offset 0;
```

**Rules:**

- Keywords: UPPERCASE (SELECT, FROM, WHERE, JOIN, AND, OR, ORDER BY, etc.)
- Columns: One per line with trailing comma
- JOINs: Indented under FROM clause
- WHERE conditions: One per line, AND/OR at start of line
- Always use parameterized queries (never string concatenation)

## Cross-References

- **`designing-architecture`** - For database architecture decisions
- **`analyzing-projects`** - For database schema analysis
- **`tdd-workflow`** - For database testing strategies

## References

- [PostgreSQL Performance Tips](https://www.postgresql.org/docs/current/performance-tips.html)
- [SQL Performance Explained](https://sql-performance-explained.com/)
- [Use The Index, Luke](https://use-the-index-luke.com/)
