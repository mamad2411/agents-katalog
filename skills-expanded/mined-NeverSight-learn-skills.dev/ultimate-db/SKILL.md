---
name: ultimate-db
description: Database engineering guidance covering schema design, indexing, query optimization, replication, and production operations across relational, document, and columnar stores. Primary focus is PostgreSQL; covers MySQL, MongoDB, ClickHouse, Redis, SQLite, and DuckDB. Use when designing schemas, optimizing slow queries, choosing index types, reviewing migrations, setting up replication, modeling documents, handling VACUUM/MVCC, or when the user mentions SQL, NoSQL, OLAP, EXPLAIN, index bloat, sharding, partitioning, or any named database system.
---

# Ultimate Database Engineering

Engine-agnostic principles first. For engine-specific patterns, indexes, and operational details see the `reference/` files.

## Reference files

| Engine | File | When to read |
| :--- | :--- | :--- |
| PostgreSQL | [reference/postgresql.md](reference/postgresql.md) | SQL, MVCC, JSONB, FTS, RLS, replication, pooling, extensions |
| MySQL | [reference/mysql.md](reference/mysql.md) | InnoDB, charset, fulltext, replication |
| MongoDB | [reference/mongodb.md](reference/mongodb.md) | Document modeling, aggregation, Atlas |
| ClickHouse | [reference/clickhouse.md](reference/clickhouse.md) | OLAP, MergeTree engines, insert strategy |
| Redis | [reference/redis.md](reference/redis.md) | Caching, pub/sub, streams, data structures |
| SQLite | [reference/sqlite.md](reference/sqlite.md) | Embedded, WAL, local-first applications |
| DuckDB | [reference/duckdb.md](reference/duckdb.md) | In-process OLAP, Parquet, analytics |

Read the relevant reference file before making engine-specific decisions. Always check docs for the exact version in use.

## Universal principles

These apply regardless of engine, paradigm, or scale:

1. **Design for access patterns.** Model data around the queries you run, not idealized normal form.
2. **Indexes are the primary performance lever.** A missing index on a large table turns milliseconds into seconds.
3. **Measure before changing.** Use `EXPLAIN ANALYZE` (SQL), `.explain("executionStats")` (MongoDB), or the engine equivalent before adding indexes or rewriting queries.
4. **Smallest correct type.** Over-provisioned types waste cache, IO, and index space.
5. **Short transactions.** Long-running transactions block vacuuming, lock acquisition, and replication everywhere.
6. **Parameterized queries always.** No string interpolation into SQL or query builders.
7. **Mutations are expensive in append-optimized engines.** In ClickHouse and similar, model to avoid UPDATE/DELETE; prefer reinsert or versioned rows.
8. **Enforce invariants at the database layer.** Constraints, domains, and check constraints catch bugs that application code misses.

## Index decision guide

Follow **ESR** order for compound indexes (applies to SQL and MongoDB alike):

1. **E**quality predicates -- most selective first.
2. **S**ort columns -- eliminates in-memory sort.
3. **R**ange predicates -- last.

```sql
-- Query: WHERE status = 'active' AND created_at > $1 ORDER BY priority DESC
CREATE INDEX idx_tasks ON tasks (status, priority DESC, created_at);
```

| Scenario | Go-to index type |
| :--- | :--- |
| Equality / range / sort (general) | B-tree (all SQL engines) |
| JSONB containment / array overlap | GIN (PostgreSQL) |
| Full-text search | GIN on `tsvector` (PG) / FULLTEXT (MySQL) / Atlas Search (Mongo) |
| Geospatial | GiST / PostGIS (PG) -- `2dsphere` (Mongo) |
| Filtered subset of rows | Partial index (`WHERE` clause) |
| Avoid heap fetch | Covering index (`INCLUDE`) |
| Large append-only time-series | BRIN (PG) / ORDER BY date column (ClickHouse) |
| Auto-expiry | TTL index (Mongo) / partition drop (PG, ClickHouse) |

## Query anti-patterns (universal)

| Pattern | Fix |
| :--- | :--- |
| Function on indexed column in `WHERE` | Use expression index or rewrite the predicate |
| `OFFSET n` pagination on large tables | Keyset / cursor pagination |
| `SELECT *` | Name only the columns needed |
| `LIKE '%term%'` on plain column | Full-text index or trigram index |
| N+1 queries | `JOIN`, `$lookup`, or batch `IN (...)` |
| Implicit type coercion in predicates | Match query type to column type exactly |
| Single-row inserts in batch workloads | Batch 10K+ rows per statement (critical for ClickHouse) |

## Schema design checklist

- [ ] Timestamps store timezone (`TIMESTAMPTZ`, `DateTime64('UTC')`, ISO 8601).
- [ ] Monetary values use exact decimal type (`NUMERIC`, `DECIMAL`, `Decimal128`).
- [ ] Enumerations use a native enum type or a `CHECK` constraint, not bare strings.
- [ ] Foreign keys declared and indexed.
- [ ] Partitioning chosen for lifecycle (DROP PARTITION), not as index substitute.
- [ ] Zero-downtime migration path planned: additive first, backfill, then constrain.

## Replication and HA summary

| Engine | Streaming / physical | Logical | Recommended HA tool |
| :--- | :--- | :--- | :--- |
| PostgreSQL | WAL streaming | Publications / subscriptions | Patroni |
| MySQL | Binary log (row-based) | CDC via Debezium | Orchestrator |
| MongoDB | Replica sets (oplog) | Change streams | built-in replica set |
| ClickHouse | ReplicatedMergeTree | -- | ClickHouse Keeper |
| Redis | AOF + RDB snapshots | -- | Redis Sentinel / Cluster |

For configuration details, failover procedures, and monitoring queries see the relevant reference file.
