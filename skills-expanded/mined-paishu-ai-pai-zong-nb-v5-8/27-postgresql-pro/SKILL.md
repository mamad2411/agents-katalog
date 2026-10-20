---
name: postgresql-pro
description: PostgreSQL-specific professional development and optimization. Use for Postgres schema design, migrations, indexes, EXPLAIN, JSONB, full-text search, constraints, transactions, locks, isolation, RLS, partitioning, generated columns, extensions, and query tuning.
---

# PostgreSQL Pro

## Workflow

1. Inspect schema, migrations, Postgres version, ORM behavior, and target query.
2. Use constraints and types to encode invariants: `uuid`, `bigint`, `numeric`, `timestamptz`, enums/domains only when appropriate.
3. Use `EXPLAIN (ANALYZE, BUFFERS)` when safe and available for performance work.
4. Choose indexes based on query shape: B-tree, partial, composite, expression, GIN, GiST, BRIN.
5. Review locks, transaction isolation, long-running migrations, and concurrent index builds.
6. Consider RLS, tenant isolation, and audit requirements for sensitive data.

## Index Guidance

- Put equality filters before range/sort columns in composite indexes when appropriate.
- Use partial indexes for common filtered subsets.
- Use GIN for JSONB containment or full-text search when query patterns justify it.
- Use `CREATE INDEX CONCURRENTLY` for large production tables when available and safe.
- Avoid duplicate and low-selectivity indexes without evidence.

## Migration Guidance

- Avoid table rewrites and long exclusive locks on large tables.
- Add nullable columns, backfill in batches, then enforce not-null where needed.
- Add constraints as `NOT VALID` then `VALIDATE CONSTRAINT` for large existing data when appropriate.
- Be careful with enum changes and irreversible DDL.

## Query Guidance

- Watch for N+1 queries, sequential scans on large tables, bad estimates, and sort spill.
- Prefer keyset pagination for large changing datasets.
- Use `timestamptz` for absolute times.
- Keep JSONB for flexible attributes, not as a replacement for relational modeling.

## Output

State Postgres-specific choice, query plan concern, migration lock risk, and exact verification command when available.
