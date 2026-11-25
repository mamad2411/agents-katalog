---
name: sql-query-devforge-sql-queries
description: Routes complex SQL query writing tasks to the SQL query specialist agent for DevForge AI.
company: devforge-ai
---

# SQL Query Specialist

## Overview
This skill routes complex SQL query writing tasks to the dedicated SQL query specialist for DevForge AI.

## Routing Criteria

Route to this skill when:
- Writing complex SELECT queries with multiple JOINs
- Creating subqueries or CTEs (Common Table Expressions)
- Building aggregate queries with GROUP BY/HAVING
- Writing UPDATE/INSERT/DELETE with complex WHERE clauses
- Creating dynamic SQL or stored procedures
- Query optimization and performance tuning

## Capabilities

### Core Query Writing
- Complex SELECT statements with multiple table joins
- Subqueries and nested queries
- Common Table Expressions (CTEs)
- Window functions and analytics
- Recursive queries

### Data Manipulation
- INSERT with SELECT
- UPDATE with JOINs
- DELETE with complex conditions
- MERGE operations

### Query Optimization
- Query execution plan analysis
- Index recommendations
- Query restructuring for performance
- Statistics and cardinality analysis

## Related Skills

- `schema-devforge-data-schema-management` - Schema design context
- `database-naming-standards` - Naming conventions
- `sql-optimization-devforge-performance` - Performance optimization

## Examples

```sql
-- Complex CTE with window functions
WITH ranked_transactions AS (
  SELECT 
    customer_id,
    transaction_date,
    amount,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY transaction_date DESC) as rank
  FROM transactions
)
SELECT * FROM ranked_transactions WHERE rank <= 5;
```

---

*This skill routes to the SQL query specialist agent for complex query writing tasks.*