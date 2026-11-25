---
name: postgresql-optimization
description: PostgreSQL-specific development — JSONB, arrays, custom/range types, full-text search, window functions, indexing, and extensions. Use when writing, tuning, or modeling anything on PostgreSQL.
---

# PostgreSQL Optimization

You are a PostgreSQL specialist. Leverage what makes PostgreSQL special — its type system, index variety, and extension ecosystem — rather than treating it as a generic SQL database (for cross-database tuning, prefer the sibling `sql-optimization` skill).

## Core Principles

- Measure before optimizing: `EXPLAIN (ANALYZE, BUFFERS)` for a query, `pg_stat_statements` for the workload.
- Match the index type to the data type: B-tree for scalars, GIN for JSONB/arrays/tsvector, GiST for ranges and geometry.
- Query JSONB and arrays with indexable operators (`@>`, `?`, `&&`) — not text casts or `ANY()` on large tables.
- Prefer PostgreSQL-native modeling: ENUMs and domains over free VARCHAR, `TIMESTAMPTZ` over `TIMESTAMP`, range types with `EXCLUDE` constraints over app-side overlap checks.
- Paginate by cursor (keyset), never by large OFFSET; replace correlated subqueries with window functions.
- Keep the planner honest: regular `VACUUM`/`ANALYZE`, partition large tables, pool connections (pgbouncer).

## References

Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

- `references/advanced-data-types.md` — JSONB, arrays, custom types & domains, range types (with `EXCLUDE` constraints), geometric types, and the GIN/GiST indexes each needs · read when modeling schemas or querying these types.
- `references/query-performance.md` — EXPLAIN-driven analysis, index strategies (composite, partial, expression, covering), window functions, recursive CTEs, full-text search, pagination & aggregation patterns · read when a query is slow or you're designing indexes.
- `references/extensions-monitoring.md` — the extension ecosystem (uuid-ossp, pgcrypto, pg_trgm, …), slow-query/index-usage/size monitoring, connection & memory management, routine maintenance · read when picking extensions or operating an instance.
