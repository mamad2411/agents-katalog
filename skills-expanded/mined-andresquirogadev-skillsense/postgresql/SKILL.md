# PostgreSQL Skill

You are working with a PostgreSQL database. Apply these best practices.

## Schema Design

- Always define a primary key — prefer `BIGSERIAL` or `UUID` with `gen_random_uuid()` as default.
- Use `NOT NULL` constraints by default; allow NULL only when the absence of a value is meaningful.
- Use `TEXT` instead of `VARCHAR(n)` unless you have a proven reason to constrain length.
- Use `TIMESTAMPTZ` (timestamp with time zone) — never `TIMESTAMP` without time zone.
- Define foreign keys with `ON DELETE CASCADE` or `ON DELETE SET NULL` (never leave it implicit).
- Normalize data to at least 3NF; denormalize with JSON/JSONB columns only when truly needed.

## Indexes

- Index every foreign key column — Postgres does NOT create these automatically.
- Add `CREATE INDEX CONCURRENTLY` to add indexes without blocking production writes.
- Use partial indexes for common filtered queries: `CREATE INDEX ON orders (status) WHERE status = 'pending'`.
- Use `EXPLAIN ANALYZE` to verify index usage; look for Seq Scan on large tables as a red flag.
- Composite indexes: column order matters — most selective or most frequently filtered column first.

## Queries

- Use `$1`, `$2` parameterized queries — never interpolate user input into SQL strings.
- Use `RETURNING *` on INSERT/UPDATE/DELETE to avoid a second SELECT round-trip.
- Use CTEs (`WITH … AS (…)`) for readability; use `WITH … AS MATERIALIZED` when you need to prevent inlining.
- Use window functions (`ROW_NUMBER()`, `RANK()`, `LAG()`, `LEAD()`) for ranking and running totals.
- Use `UPSERT`: `INSERT … ON CONFLICT (col) DO UPDATE SET …`.

## Transactions & Locking

- Use `BEGIN` / `COMMIT` / `ROLLBACK` for multi-statement atomic operations.
- Use `SELECT … FOR UPDATE SKIP LOCKED` for queue-like workloads to avoid lock contention.
- Keep transactions short — long-running transactions block autovacuum and cause bloat.

## Performance

- Run `VACUUM ANALYZE` regularly; configure autovacuum aggressively for write-heavy tables.
- Use `pg_stat_user_tables` and `pg_stat_statements` to identify slow queries.
- Use connection pooling (PgBouncer, Supabase Pooler) for serverless/edge environments.

## JSON / JSONB

- Prefer `JSONB` over `JSON` — JSONB is stored in binary and supports indexing.
- Use GIN indexes for JSONB column searches: `CREATE INDEX on items USING GIN (metadata)`.
