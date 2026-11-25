---
name: databases-data-core
description: "Shared reference for the databases-data cluster: the store-selection model (OLTP vs OLAP vs in-memory vs ORM-managed), and the conventions every spoke shares — index choice, ID strategy, connection pooling, expand/contract migrations, and idempotent bulk writes. USE WHEN choosing a database, designing a schema/index, planning a migration, or moving data — the interlocking rules every data spoke depends on."
cluster: databases-data
version: 1.0.0
---

# Databases & Data Core

Shared model for the `databases-data` cluster. The engine spokes, the migration spoke,
and the throughput spoke all depend on these decisions — keep them consistent here so no
spoke contradicts another.

## 1. The store-selection model (the decision this cluster turns on)

Match the **store to the access pattern** before writing any schema. Picking the wrong
store is the single most expensive mistake to undo.

```
Workload ──is──> { OLTP rows · OLAP scans · in-memory · ORM-managed } ──picks──> Store
```

| Access pattern | Pick | Why | Spoke |
|---|---|---|---|
| Transactional reads/writes, single rows, strong consistency | **PostgreSQL** | RLS, rich types, GIN/BRIN, mature ecosystem | `postgres-patterns` |
| Transactional, MySQL/MariaDB shop or existing fleet | **MySQL / MariaDB** | replication, wide hosting; mind engine divergence | `mysql-patterns` |
| TypeScript app wanting typed models over PG/MySQL | **Prisma ORM** | typed client + migrations — atop a relational store, not instead of one | `prisma-patterns` |
| Aggregations/scans over huge append-only datasets | **ClickHouse** | column store, partition pruning, materialized views | `clickhouse-io` |
| Cache, locks, counters, queues, ephemeral state | **Redis** | in-memory, atomic ops, TTLs — not a system of record | `redis-patterns` |

**Rules:** never run analytics off your primary OLTP store (replicate/ETL to ClickHouse);
Redis is a cache/coordination layer, never the source of truth; an ORM is a convenience
*over* a relational engine — you still own the index and pool decisions below.

## 2. Index & schema conventions (relational)

- **Index by query shape:** equality → B-tree; `WHERE a = x AND b > y` → composite (equality cols first); `jsonb @>`/full-text → GIN; time-series ranges → BRIN. → `postgres-patterns`, `mysql-patterns`
- **Types:** `bigint` IDs, `text` over `varchar(n)`, `timestamptz`/UTC, `numeric` for money (never `float`).
- **ID strategy:** sequential `bigint`/auto-increment for internal joins; `cuid`/`uuid` for public/interop IDs — but random UUIDs as a PK fragment B-tree indexes on high-write tables. → `prisma-patterns`
- **Index the FK side** of every relation; an unindexed foreign key is the most common hidden table scan.

## 3. Connection & pooling

The pool, not the query, is what falls over first under load.

- One pool per process; size it to the DB's `max_connections`, not to request volume.
- **Serverless** (Lambda/Vercel/Workers): low per-instance limit (e.g. `connection_limit=1`) **plus** an external pooler (PgBouncer / RDS Proxy / Prisma Accelerate) — function fan-out otherwise exhausts connections. → `prisma-patterns`, `postgres-patterns`, `mysql-patterns`
- Set `statement_timeout` and `idle_in_transaction_session_timeout`; use `SKIP LOCKED` only for queue work, never for integrity-sensitive reads.

## 4. Migration model (expand / contract)

Every production schema change is a migration, applied through tooling, **forward-only**:

```
EXPAND (add nullable col / new table, concurrent index)
  → BACKFILL (separate data migration)
    → switch app reads/writes
      → CONTRACT (drop old column/table a later deploy)
```

- Never `NOT NULL` without a default; never an inline index on a large existing table — `CREATE INDEX CONCURRENTLY`.
- Schema (DDL) and data (DML) live in **separate** migrations; deployed migrations are immutable (fix forward). → `database-migrations`

## 5. Moving data correctly

- Move compute to where the data is; prefer warehouse-native scans/appends for large landed files.
- Make bulk writes **idempotent** (unique keys, manifests, replaceable staging) and batch small writes.
- Keep raw / derived / serving tables separately accountable; prove a job done with manifest + row-count + max-timestamp gates, not wall-clock. → `data-throughput-accelerator`

## 6. Version / tooling matrix

| Store | Target | Watch for | Spoke |
|---|---|---|---|
| PostgreSQL | 14+ | RLS policy perf (wrap `auth.uid()` in `SELECT`), `pg_stat_statements` | `postgres-patterns` |
| MySQL / MariaDB | MySQL 8 / MariaDB 10.6+ | `VALUES()` vs row-alias divergence in `ON DUPLICATE KEY UPDATE` | `mysql-patterns` |
| Prisma | 5.x / 6.x | `relationJoins` row explosion; `updateMany` returns count; `migrate dev` resets DB | `prisma-patterns` |
| ClickHouse | recent LTS | MergeTree engine + ORDER BY/partition choice; avoid `FINAL` and small inserts | `clickhouse-io` |
| Redis | 6+ | atomicity needs Lua/MULTI; eviction policy + persistence (RDB/AOF) | `redis-patterns` |
| Migration tooling | Prisma · Drizzle · Kysely · Django · TypeORM · golang-migrate | forward-only in prod | `database-migrations` |

## 7. Shared guardrails

- **Match the store to the access pattern** (§1); don't run OLAP on your OLTP primary; Redis is never the system of record.
- Index by query shape; index every FK; pick types deliberately (no `float` money, no `varchar(255)` reflex).
- Size pools to the DB, not the traffic; serverless = external pooler + low per-instance limit; always set timeouts.
- Every prod schema change is a forward-only migration via expand/contract; no `NOT NULL` without default; build indexes concurrently; DDL and DML separate; deployed migrations immutable.
- Validate inputs at the app boundary; never interpolate untrusted SQL.
- Bulk/ETL writes are idempotent and proven correct (manifests + counts) before completion.
