---
name: database-patterns
description: Database design patterns — schema design, indexing, migrations, query optimization.
---

# Database Patterns

## Schema Design

### Naming
- Tables: plural, snake_case (`users`, `order_items`)
- Columns: snake_case (`created_at`, `user_id`)
- Primary keys: `id` (auto-increment or UUID)
- Foreign keys: `<table>_id` (`user_id`, `order_id`)
- Timestamps: `created_at`, `updated_at`, `deleted_at`

### Data Types
- Strings: `VARCHAR(n)` for known max, `TEXT` for unlimited
- Numbers: `INTEGER` for whole numbers, `DECIMAL(p,s)` for money
- Booleans: `BOOLEAN` or `TINYINT(1)`
- Dates: `TIMESTAMP` for date+time, `DATE` for date only
- JSON: `JSONB` (PostgreSQL) for flexible structure

### Relationships
- One-to-many: foreign key on the many side
- Many-to-many: junction table
- One-to-one: foreign key with unique constraint

## Indexing

### When to Index
- Columns used in WHERE clauses
- Columns used in JOIN conditions
- Columns used in ORDER BY
- Columns with high cardinality (many unique values)

### When NOT to Index
- Small tables (< 1000 rows)
- Columns with low cardinality (boolean, status)
- Columns that are frequently updated
- Tables with heavy write loads

### Index Types
- B-tree: default, good for most queries
- Hash: exact match only, very fast
- GIN: full-text search, JSON queries
- Partial: index with WHERE clause

## Migrations

### Rules
- Every migration must be reversible
- Never modify a deployed migration
- Add columns as nullable first, then backfill
- Create index CONCURRENTLY in production
- Test migrations on a copy of production data

### Safe Migration Pattern
```sql
-- Step 1: Add nullable column
ALTER TABLE users ADD COLUMN bio TEXT;

-- Step 2: Backfill
UPDATE users SET bio = '' WHERE bio IS NULL;

-- Step 3: Add NOT NULL constraint
ALTER TABLE users ALTER COLUMN bio SET NOT NULL;
```

## Query Optimization

- Use EXPLAIN ANALYZE to check query plans
- Avoid SELECT * — select only needed columns
- Use LIMIT for large result sets
- Batch inserts instead of single inserts
- Use connection pooling
- Avoid N+1 queries — use JOINs or eager loading
