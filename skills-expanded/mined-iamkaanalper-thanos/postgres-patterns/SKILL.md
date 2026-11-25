---
name: postgres-patterns
description: PostgreSQL database patterns for query optimization, schema design, indexing, and security. Based on Supabase best practices. Grok-native with Production Contract, hooks, compound, palace.
when-to-use: When writing SQL, migrations, schema design, slow query troubleshooting, RLS, or connection pooling. Pair with database-reviewer, backend-dev, vault.
---

# PostgreSQL Patterns (Grok Port)

Quick reference + production guardrails for PostgreSQL (Supabase-inspired + general). Focus on index strategy, data types, RLS, anti-pattern detection, and Grok system integration (ledger for migrations, preflight checks, compound for recurring pain).

## When to Activate
- Writing or reviewing SQL / migrations
- Schema design or normalization decisions
- Troubleshooting slow queries or bloat
- Implementing RLS or security policies
- Setting up pooling (PgBouncer) or read replicas

## Index Cheat Sheet
| Query Pattern                  | Index Type | Example |
|--------------------------------|------------|---------|
| `WHERE col = value`            | B-tree     | `CREATE INDEX idx ON t (col)` |
| `WHERE col > value`            | B-tree     | `CREATE INDEX idx ON t (col)` |
| `WHERE a = x AND b > y`        | Composite  | `CREATE INDEX idx ON t (a, b)` |
| `WHERE jsonb @> '{}'`          | GIN        | `CREATE INDEX idx ON t USING gin (col)` |
| `WHERE tsv @@ query`           | GIN        | `CREATE INDEX idx ON t USING gin (col)` |
| Time-series ranges             | BRIN       | `CREATE INDEX idx ON t USING brin (col)` |

**Composite order rule:** equality columns first, then range columns.
```sql
CREATE INDEX idx ON orders (status, created_at);
-- Good for: WHERE status = 'pending' AND created_at > '2024-01-01'
```

**Covering index (INCLUDE):**
```sql
CREATE INDEX idx ON users (email) INCLUDE (name, created_at);
-- Avoids heap lookup for SELECT email, name, created_at
```

**Partial index (for soft-delete / active-only):**
```sql
CREATE INDEX idx ON users (email) WHERE deleted_at IS NULL;
```

## Data Type Quick Reference
- IDs: `bigint` (or `uuid` with care); avoid random UUID as PK for insert perf.
- Strings: `text` (no artificial 255 limit).
- Timestamps: `timestamptz` always.
- Money: `numeric(10,2)` never `float`/`double`.
- Flags: `boolean`.

## Common Safe Patterns
**UPSERT (idempotent insert):**
```sql
INSERT INTO settings (user_id, key, value)
VALUES (123, 'theme', 'dark')
ON CONFLICT (user_id, key)
DO UPDATE SET value = EXCLUDED.value, updated_at = now();
```

**Cursor pagination (O(1) vs OFFSET O(n)):**
```sql
SELECT * FROM products WHERE id > $last_id ORDER BY id LIMIT 20;
```

**Queue / SKIP LOCKED (claim next job safely):**
```sql
UPDATE jobs SET status = 'processing'
WHERE id = (
  SELECT id FROM jobs WHERE status = 'pending'
  ORDER BY created_at LIMIT 1
  FOR UPDATE SKIP LOCKED
) RETURNING *;
```

**RLS policy (wrap subselect for perf):**
```sql
CREATE POLICY orders_user ON orders
  USING ((SELECT auth.uid()) = user_id);
```

## Anti-Pattern Detection Queries
```sql
-- Unindexed foreign keys
SELECT conrelid::regclass, a.attname
FROM pg_constraint c
JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
WHERE c.contype = 'f'
  AND NOT EXISTS (SELECT 1 FROM pg_index i WHERE i.indrelid = c.conrelid AND a.attnum = ANY(i.indkey));

-- Slow queries (requires pg_stat_statements)
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
WHERE mean_exec_time > 100
ORDER BY mean_exec_time DESC;

-- Table bloat
SELECT relname, n_dead_tup, last_vacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

## Configuration Guardrails
```sql
ALTER SYSTEM SET max_connections = 100;
ALTER SYSTEM SET work_mem = '8MB';
ALTER SYSTEM SET idle_in_transaction_session_timeout = '30s';
ALTER SYSTEM SET statement_timeout = '30s';
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
REVOKE ALL ON SCHEMA public FROM public;
SELECT pg_reload_conf();
```

## Grok Integration (Production Contract)
- Primary agents: database-reviewer, backend-dev, vault (DBA).
- Fire on_db_change hook for any migration, new index, RLS policy, or connection string change.
- Pre-Flight (mandatory for schema/migration work): "Have we chosen the right partition/index strategy? N+1 risk modeled? RLS or row-level security needed? Rollback plan for this migration? Connection pool sizing for expected load?"
- Ledger: every migration (up/down), index addition, or policy change recorded with task_id + SQL diff + estimated impact (rows affected, downtime).
- Handoff: include migration SQL, explain analyze output, before/after query plans, rollback script, affected endpoints/tests, RLS policy review.
- Friction + compound: every "slow query because missing composite index" or "RLS policy caused 100x slowdown because subselect not wrapped" → compound to preflight checklists, linter rules, or skill defaults.
- Palace: store "chose composite (status, created_at) for orders because 90% queries filter status + recent window; rejected single-column because range scan was killing perf".
- Claim-verification: Two-pass strict. Grep for "CREATE INDEX" → read_file actual migration file + run `EXPLAIN ANALYZE` on representative data → "Composite index on orders(status, created_at) exists at migrations/2026_xx_add_status_idx.sql:12 and reduces query from 1200ms to 3ms ✓VERIFIED". Never claim "indexed" or "optimized" without reading the actual object and evidence.
- Use with: backend-patterns, api-patterns, mutation-testing (test the queries), test-enforcement, memory-palace + layered-recall (store schema decisions), sast-patterns (SQLi guard), gdpr-compliance (erasure cascades + audit).

## When to Activate
- Any SQL migration, new table, index, view, function, or RLS policy.
- Swarm Phase 2 (backend/DB tracks) and Phase 3 (review).
- Before deploys that touch DB schema or queries.
- PRs with .sql, knex/typeorm/prisma changes, or raw queries.
- Performance or compliance reviews (shipper + verifier + compliance-expert).

See .grok/skills/backend-patterns/SKILL.md, api-patterns, kubernetes-patterns (for Postgres operators), preflight, compound-learnings, memory-palace. Always run `EXPLAIN` + verify on real data volume. Production Contract: ledger entry + handoff + preflight + friction record for every schema change.

Prefer partial/composite/covering indexes over "add index later". Soft deletes + audit columns are default for compliance. Never trust coverage numbers alone — measure with real EXPLAIN + pg_stat_statements.
