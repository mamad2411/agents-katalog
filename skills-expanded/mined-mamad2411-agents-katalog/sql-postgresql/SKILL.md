---
name: sql-postgresql
description: "Applies when writing or reviewing PostgreSQL queries and schemas. Covers JSONB, UPSERT, GIN/GiST/BRIN indexes, RETURNING, CTEs, advisory locks, and autovacuum."
---

# PostgreSQL

## Data types

1. **`BIGINT GENERATED ALWAYS AS IDENTITY`** for internal PKs. `gen_random_uuid()` (PG 13+) or UUIDv7 for external IDs.
2. **`JSONB` over `JSON`.** Binary decomposed, indexable (GIN), supports `@>`, `<@` operators. `JSON` only preserves formatting.
3. **`TEXT` over `VARCHAR(n)`** unless you need a length constraint. Identical performance; `VARCHAR(n)` adds overhead.
4. **`TIMESTAMPTZ`** for all temporal data. Never bare `TIMESTAMP` for wall-clock events.
5. **Range types (`TSTZRANGE`, `INT4RANGE`)** for intervals. Pair with `EXCLUDE USING gist` for overlap prevention.
6. **Arrays (`INTEGER[]`, `TEXT[]`)** for small multi-value columns that don't need joins.

## Upsert and RETURNING

7. **`ON CONFLICT DO UPDATE` for upserts:**
   ```sql
   INSERT INTO inventory (product_id, qty) VALUES (101, 5)
   ON CONFLICT (product_id) DO UPDATE SET qty = inventory.qty + EXCLUDED.qty;
   ```
8. **`RETURNING` after mutations** to avoid a separate SELECT:
   ```sql
   INSERT INTO orders (customer_id, total) VALUES (42, 99.99)
   RETURNING id, created_at;
   ```
9. **Chain `RETURNING` with CTEs** for multi-step mutations (DELETE → INSERT archive).

## Indexes

10. **GIN** for JSONB, arrays, full-text, trigram similarity. `CREATE INDEX ... USING gin (data jsonb_path_ops)`.
11. **GiST** for geometric, range, full-text types. Required for exclusion constraints.
12. **BRIN** for naturally ordered large tables (time-series, append-only logs). Tiny size, fast scans.
13. **Partial indexes:** `CREATE INDEX ix_orders_pending ON orders (created_at) WHERE status = 'pending'`.
14. **Expression indexes:** `CREATE INDEX ix_lower_email ON users (LOWER(email))`.
15. **Always `CREATE INDEX CONCURRENTLY`** in production. Cannot run inside a transaction but avoids write locks.

## Extensions

16. **`pg_trgm`** for fuzzy text search and `LIKE '%partial%'` with GIN indexes.
17. **`pg_stat_statements`** for identifying slow and frequent queries. Query it regularly.
18. **`pgcrypto`** for `gen_random_uuid()` (pre-PG13) and `crypt()` for password hashing.

## Maintenance

19. **Understand autovacuum.** High-write tables may need tuned thresholds. Dead tuples are not reclaimed until VACUUM.
20. **`ANALYZE` after large data loads** to update planner statistics.
21. **Set `idle_in_transaction_session_timeout`** to kill idle-in-transaction connections that block vacuum.

## PostgreSQL pitfalls

22. **Connection pooling is mandatory.** PG forks a process per connection (~5-10 MB). Use PgBouncer (transaction mode). Aim for `max_connections` 100-300.
23. **Long transactions prevent dead-tuple cleanup** across the entire database.
24. **`FOR UPDATE SKIP LOCKED`** for job-queue patterns. Without `SKIP LOCKED`, workers deadlock.
25. **`TRUNCATE` acquires `ACCESS EXCLUSIVE` lock.** For production deletes, batch `DELETE ... LIMIT` or drop partitions.
26. **CTEs are optimization fences before PG 12.** Use `NOT MATERIALIZED` hint (PG 12+) or inline subqueries for performance.

## Sources

- https://www.postgresql.org/docs/current/indexes.html
- https://www.postgresql.org/docs/current/routine-vacuuming.html
