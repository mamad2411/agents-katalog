---
name: database-patterns
description: >
  Database design and operations patterns. Schema design, migration best practices, indexing strategy,
  query optimization, and PostgreSQL patterns. Use when designing schemas, writing migrations,
  or optimizing queries.
---

# database-patterns

Database design and operations patterns.

## how to use

- `/database-patterns`
  Apply these database standards to all data work in this conversation.

- `/database-patterns <query or schema>`
  Review against rules below and suggest improvements.

## when to apply

Reference these guidelines when:
- designing database schemas or data models
- writing or reviewing migrations
- creating indexes or optimizing queries
- managing connection pools
- implementing data integrity constraints
- choosing between SQL and NoSQL

## rule categories by priority

| priority | category | impact |
|----------|----------|--------|
| 1 | schema design | critical |
| 2 | migrations | critical |
| 3 | indexing | high |
| 4 | query optimization | high |
| 5 | connection management | medium |
| 6 | data integrity | critical |

## quick reference

### 1. schema design (critical)

- use descriptive table names (plural, snake_case): `user_profiles`, `order_items`
- use descriptive column names (snake_case): `created_at`, `is_active`
- every table must have a primary key
- prefer UUIDs for public-facing IDs; auto-increment for internal use
- use appropriate data types; don't store numbers as strings
- add `created_at` and `updated_at` timestamps to all tables
- normalize to 3NF by default; denormalize intentionally with documentation
- use foreign keys to enforce relationships
- add NOT NULL constraints by default; allow NULL only when semantically meaningful
- avoid reserved words as column names

**Naming conventions**:
| Element | Convention | Example |
|---------|-----------|---------|
| Table | plural snake_case | `user_accounts` |
| Column | singular snake_case | `first_name` |
| Primary key | `id` | `id` |
| Foreign key | `<singular_table>_id` | `user_id` |
| Boolean | `is_` or `has_` prefix | `is_active` |
| Timestamp | `_at` suffix | `deleted_at` |
| Index | `idx_<table>_<columns>` | `idx_users_email` |
| Unique constraint | `uq_<table>_<columns>` | `uq_users_email` |

### 2. migrations (critical)

- one logical change per migration
- migrations must be reversible (include up AND down)
- never modify a migration that has been applied to shared environments
- test migrations against a copy of production data
- use transactional migrations where supported
- add indexes concurrently in PostgreSQL: `CREATE INDEX CONCURRENTLY`
- backfill data in batches, not single statements
- separate schema changes from data migrations
- keep migrations idempotent where possible

**Dangerous operations** (require special care):
| Operation | Risk | Mitigation |
|-----------|------|------------|
| DROP TABLE | data loss | verify no references, backup first |
| DROP COLUMN | data loss | deprecate first, backup, then drop |
| RENAME COLUMN | breaks queries | use dual-write pattern during transition |
| ALTER TYPE | locks table | create new column, backfill, swap |
| ADD NOT NULL | fails if nulls exist | backfill data first, then add constraint |

### 3. indexing (high)

**Decision tree**:
- column in WHERE clause frequently? -> consider index
- column in JOIN condition? -> index
- column in ORDER BY? -> consider index
- high cardinality (many unique values)? -> B-tree index
- text search? -> GIN index with tsvector
- JSONB queries? -> GIN index
- geometric/range data? -> GiST index
- exact equality only? -> hash index (rare)

**Rules**:
- index foreign keys (not auto-indexed in PostgreSQL)
- use composite indexes for multi-column queries; put most selective column first
- don't over-index; each index slows writes
- use partial indexes for filtered queries: `WHERE is_active = true`
- use covering indexes to avoid table lookups: `INCLUDE (column)`
- monitor unused indexes and remove them
- analyze index usage: `pg_stat_user_indexes`

### 4. query optimization (high)

- use `EXPLAIN ANALYZE` to understand query plans
- avoid `SELECT *`; select only needed columns
- avoid N+1 queries; use JOINs or batch loading
- use EXISTS instead of COUNT for existence checks
- use LIMIT for pagination; never fetch unbounded results
- avoid functions on indexed columns in WHERE: `WHERE LOWER(email)` defeats index
- use CTEs for readability, but know they may be optimization fences
- prefer bulk operations over row-by-row
- use connection pooling (PgBouncer, application-level)

**Query plan red flags**:
| Plan Element | Problem | Fix |
|-------------|---------|-----|
| Seq Scan on large table | missing index | add appropriate index |
| Nested Loop with large sets | inefficient join | use Hash or Merge Join |
| Sort with high cost | missing index for ORDER BY | add sorted index |
| Rows estimate wildly wrong | stale statistics | run ANALYZE |

### 5. connection management (medium)

- use connection pooling; never open connections per request
- set appropriate pool size: `(2 * CPU cores) + effective_spindle_count`
- set connection timeout and idle timeout
- handle connection failures gracefully with retry logic
- use read replicas for read-heavy workloads
- monitor connection count and pool utilization

### 6. data integrity (critical)

- use transactions for multi-statement operations
- choose appropriate isolation level (READ COMMITTED is default and usually correct)
- use constraints (NOT NULL, UNIQUE, CHECK, FK) over application-level validation
- implement soft deletes for audit trail: `deleted_at` timestamp
- use optimistic locking for concurrent updates: version column
- never trust client-provided IDs for authorization
- backup regularly; test restore procedures

## common fixes

| problem | fix |
|---------|-----|
| slow query | run EXPLAIN ANALYZE; add missing index |
| N+1 queries | use JOIN or batch loader (dataloader pattern) |
| table lock during migration | use CONCURRENTLY for index creation |
| connection exhaustion | implement connection pooling |
| data inconsistency | add database constraints, use transactions |
| missing timestamps | add created_at/updated_at with defaults |
