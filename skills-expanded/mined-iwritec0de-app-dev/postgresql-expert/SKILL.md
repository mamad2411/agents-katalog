---
name: postgresql-expert
description: >-
  This skill should be used when the user asks to 'write a PostgreSQL query',
  'configure postgresql.conf', 'use JSONB', 'set up a PG extension', 'tune
  Postgres performance', 'optimize a Postgres query', or mentions 'postgresql',
  'postgres', 'pg_', 'jsonb', 'array type', 'CTE', 'window function',
  'extension', 'postgresql.conf', 'pg_stat', 'vacuum', 'WAL'. Provides
  PostgreSQL-specific expertise for advanced SQL, types, extensions, and tuning.
license: MIT
metadata:
  author: Chris Kelley (hello@iwritecode.io)
  version: 1.0.0
---

# PostgreSQL Expert Skill

You are a PostgreSQL expert specializing in PG-specific features, types, and tuning.

## Critical Rules

- **Use JSONB not JSON** — JSONB is binary, indexable, and queryable; JSON is just text storage
- **Use arrays for simple lists** — prefer `TEXT[]` over junction tables for tags-like data
- **VACUUM ANALYZE after bulk ops** — keep statistics and dead tuple counts current
- **Use pg_stat_statements** — the single most important extension for query analysis
- **Prefer `gen_random_uuid()`** — built-in since PG 13, no extension needed
- **CTEs are optimization fences in PG < 12** — use `WITH ... AS MATERIALIZED/NOT MATERIALIZED` in 12+
- **Use RETURNING** — avoid separate SELECT after INSERT/UPDATE/DELETE

## PG-Specific Types

| Type | Use Case | Example |
|------|----------|---------|
| `UUID` | Distributed-safe primary keys | `gen_random_uuid()` |
| `JSONB` | Flexible/schemaless data | `data->'key'`, `data @> '{"a":1}'` |
| `TEXT[]` | Simple lists, tags | `ARRAY['a','b']`, `ANY(tags)` |
| `ENUM` | Fixed small sets | `CREATE TYPE status AS ENUM (...)` |
| `TSTZRANGE` | Time ranges | `[2024-01-01, 2024-12-31)` |
| `TSVECTOR` | Full-text search | `to_tsvector('english', body)` |
| `INET/CIDR` | IP addresses | `'192.168.1.0/24'::cidr` |

## Advanced SQL

```sql
-- Recursive CTE: tree traversal
WITH RECURSIVE tree AS (
  SELECT id, name, parent_id, 0 AS depth FROM categories WHERE parent_id IS NULL
  UNION ALL
  SELECT c.id, c.name, c.parent_id, t.depth + 1 FROM categories c JOIN tree t ON c.parent_id = t.id
) SELECT * FROM tree;

-- Window function: running total
SELECT id, amount, SUM(amount) OVER (ORDER BY created_at) AS running_total FROM payments;

-- UPSERT with conflict handling
INSERT INTO settings (key, value) VALUES ('theme', 'dark')
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = NOW();

-- LATERAL join: top-N per group
SELECT u.*, recent.* FROM users u
CROSS JOIN LATERAL (
  SELECT * FROM orders WHERE user_id = u.id ORDER BY created_at DESC LIMIT 3
) recent;
```

Read `reference/advanced-sql.md` for recursive CTEs, window functions, JSONB queries, and array operations.

## Extensions

| Extension | Purpose | Setup |
|-----------|---------|-------|
| `pg_stat_statements` | Query performance analysis | `CREATE EXTENSION pg_stat_statements;` |
| `pg_trgm` | Fuzzy text search, similarity | `CREATE INDEX ... USING gin (name gin_trgm_ops);` |
| `pgvector` | AI embedding similarity search | `CREATE INDEX ... USING ivfflat (embedding vector_cosine_ops);` |
| `pg_cron` | Scheduled jobs inside PG | `SELECT cron.schedule('0 3 * * *', $$VACUUM$$);` |
| `PostGIS` | Geospatial queries | `ST_DWithin(geom, point, 1000)` |
| `citext` | Case-insensitive text | `email CITEXT UNIQUE` |

Read `reference/extensions.md` for setup guides and usage patterns.

## Configuration Tuning

Key `postgresql.conf` settings (adjust for your RAM):

| Setting | Default | Recommendation |
|---------|---------|---------------|
| `shared_buffers` | 128MB | 25% of RAM |
| `work_mem` | 4MB | 64-256MB (per operation) |
| `effective_cache_size` | 4GB | 75% of RAM |
| `maintenance_work_mem` | 64MB | 512MB-1GB |
| `random_page_cost` | 4.0 | 1.1 for SSDs |

Read `reference/tuning.md` for WAL config, connection pooling, VACUUM strategies, and replication.

## Monitoring

```sql
-- Slow queries (requires pg_stat_statements)
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 20;

-- Table bloat / dead tuples
SELECT relname, n_dead_tup, last_autovacuum FROM pg_stat_user_tables
WHERE n_dead_tup > 1000 ORDER BY n_dead_tup DESC;

-- Active queries and locks
SELECT pid, state, query, wait_event_type FROM pg_stat_activity WHERE state != 'idle';
```

## Related

- `reference/advanced-sql.md` — Recursive CTEs, window functions, LATERAL, JSONB, arrays
- `reference/extensions.md` — pg_trgm, pg_stat_statements, PostGIS, pgvector, pg_cron
- `reference/tuning.md` — postgresql.conf tuning, PgBouncer, VACUUM, WAL, replication
