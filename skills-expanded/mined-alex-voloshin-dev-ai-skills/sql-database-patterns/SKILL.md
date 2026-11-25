---
name: sql-database-patterns
description: Use this skill when the agent is designing schemas, reviewing migrations, tuning queries, modeling NoSQL access patterns, configuring replication, planning partitioning, auditing indexes, or onboarding to database conventions — the database patterns knowledge base for PostgreSQL, MySQL, SQL Server, MongoDB, Redis, Cassandra, DynamoDB engines, schema design, SQL optimization, indexing strategies (B-tree, hash, GIN, GiST, BRIN, partial, covering), partitioning (range, list, hash), replication topologies, NoSQL data modeling, time-series, graph, monitoring, capacity planning, backup and recovery.
disable-model-invocation: true
---

# Database Patterns

Reference knowledge for relational and NoSQL database engineering — schema design, query optimization, indexing, partitioning, replication, NoSQL modeling, monitoring, and backup.

## When to Use

- Designing or evolving a schema; reviewing a migration PR
- Tuning a slow query (EXPLAIN, indexing)
- Modeling access patterns in MongoDB, DynamoDB, Cassandra, Redis
- Planning partitioning, sharding, or replication topology
- Configuring monitoring, slow-query logging, vacuum/bloat checks
- Designing backup, restore, RTO/RPO strategy

## When NOT to Use

- ORM-layer modeling in app code → `python-engineer` / `java-engineer` (reference this skill)
- Data pipelines / warehousing → `data-engineer`
- Database infra provisioning → `devops-engineer`

## SQL Database Engines

### PostgreSQL

- `timestamptz` not `timestamp`; `text` not `varchar`; `numeric(p,s)` for money
- `pg_stat_statements`, `pg_stat_user_tables`, `pg_stat_activity` for diagnostics
- `pgaudit` for audit trail; `pgcrypto` for column-level encryption
- `pg_repack` for online bloat reorganization; `REINDEX CONCURRENTLY` for index bloat
- Streaming replication: async for read replicas, sync for zero data loss
- PITR via `pg_basebackup` + WAL archiving
- Failover: Patroni, `pg_auto_failover`, or cloud-managed

### MySQL

- InnoDB default; check `innodb_buffer_pool_size` sizing (60-80% RAM)
- Use `EXPLAIN FORMAT=JSON` for execution plan; `performance_schema` for diagnostics
- Slow query log: `long_query_time`, `log_queries_not_using_indexes`
- Replication: row-based (RBR) default; GTID for failover; semi-sync for durability
- ProxySQL for read/write split and connection pooling
- Avoid `utf8` (3-byte) — use `utf8mb4` (4-byte) for full Unicode

### SQL Server

- Clustered index = physical row order; pick narrow, increasing, unique key
- Statistics auto-updated; use `UPDATE STATISTICS` after bulk loads
- `sys.dm_exec_query_stats`, `sys.dm_db_missing_index_details` for tuning
- Always On Availability Groups for HA; log shipping for DR
- Use `OPTION (RECOMPILE)` sparingly — parameter sniffing is usually preferable
- TDE for encryption at rest; Always Encrypted for column-level

## Schema Design

- **Normalization**: 3NF by default. Denormalize only with measured read-performance justification
- **Primary keys**: Surrogate (`BIGSERIAL`, UUID) for most tables. Natural keys only when immutable and unique
- **Foreign keys**: Always explicit ON DELETE/ON UPDATE. CASCADE for child lifecycle, RESTRICT for references, SET NULL for optional
- **Naming**: `snake_case`, plural tables (`users`, `orders`). FK: `{table_singular}_id`
- **Constraints**: NOT NULL by default. CHECK for value ranges. UNIQUE for business keys
- **Data types**: Most specific type for storage + correctness
- **Audit columns**: `created_at timestamptz DEFAULT now()`, `updated_at timestamptz` on every table

## SQL Optimization

- **EXPLAIN ANALYZE**: Always use actual execution. Compare estimated vs actual rows — gaps = stale statistics
- **Seq scan elimination**: Add indexes. Check `work_mem` for hash joins and sorts
- **Join order**: Optimizer handles most cases. 10+ joins → use `join_collapse_limit` or explicit order
- **CTEs**: PG 12+ inlines by default. Use `MATERIALIZED` only for optimization fences
- **Subquery vs JOIN**: Prefer JOIN for correlated subqueries. EXISTS over IN for large subsets
- **Batch ops**: `INSERT ... ON CONFLICT` (upsert). `COPY` for bulk. Avoid row-by-row loops
- **Locking**: `FOR UPDATE SKIP LOCKED` for queues. `NOWAIT` for fast fail. Advisory locks for app coordination
- **Statistics**: `ANALYZE` after bulk loads. Increase `default_statistics_target` for skewed distributions
- **No `SELECT *`** in production code — specify columns explicitly

## Indexing Strategies

- **B-tree** (default): Equality + range. Composite: equality columns first, then range
- **Hash**: Equality-only, faster than B-tree for `=` but no range
- **GIN**: Full-text search, JSONB `@>`, arrays. `gin_trgm_ops` for `LIKE '%term%'`
- **GiST**: Spatial (PostGIS), range types, nearest-neighbor
- **BRIN**: Large append-only tables with natural ordering (time-series). Tiny index size
- **Partial indexes**: `WHERE active = true` — index only filtered rows
- **Covering indexes**: `INCLUDE (col)` for index-only scans
- **Expression indexes**: `CREATE INDEX ON t (lower(email))` for case-insensitive lookups
- **Composite order**: Most selective first for equality; leftmost prefix rule applies
- **Maintenance**: `REINDEX CONCURRENTLY` for bloat. Monitor `pg_stat_user_indexes` for unused indexes
- **Justify cost**: Every index must have a documented query pattern. Indexes slow writes and waste storage

## Partitioning + Replication

### Partitioning

- **Range**: Time-series (month/year), numeric ranges — most common
- **List**: Categorical (region, status, tenant_id) — good for multi-tenant
- **Hash**: Even distribution when no natural range/list. High-throughput writes
- **Pruning**: Queries must include partition key in WHERE for pruning
- **Maintenance**: Pre-create future partitions. Detach and archive old ones
- **Constraints**: PK and UNIQUE must include partition key

### Replication

- **Streaming replication** (PostgreSQL): Async for read replicas, sync for zero data loss. Monitor replication lag
- **Connection routing**: Read queries to replicas, writes to primary. Use PgBouncer or application-level routing
- **Failover**: Automated via Patroni, `pg_auto_failover`, or cloud-managed. Test failover regularly
- **Logical replication**: For selective table replication, version upgrades, multi-master
- **RTO/RPO**: Define Recovery Time Objective and Recovery Point Objective. Design backup frequency and failover speed accordingly

## NoSQL

### MongoDB

- Schema design follows access patterns, not normalization. Embed for 1:1 and 1:few. Reference for 1:many and many:many
- Indexes: compound indexes follow ESR rule (Equality → Sort → Range). Use `explain()` with `executionStats`
- Aggregation pipeline for complex queries. Avoid `$lookup` on large collections — denormalize instead
- Sharding: choose shard key based on cardinality + write distribution + query isolation. Avoid monotonic keys (ObjectId) as shard key
- Write concern: `{w: "majority"}` for durability; `j: true` for journaled
- Replica sets: minimum 3 voting members; use hidden/delayed secondaries for analytics

### Redis

- Data structures: Strings (cache), Hashes (objects), Lists (queues), Sets (tags), Sorted Sets (leaderboards), Streams (event log)
- Key naming: `{service}:{entity}:{id}:{field}` — consistent, scannable, eviction-friendly
- TTL on every key — never store data without expiration unless explicitly persistent
- Memory management: `maxmemory-policy` (`allkeys-lru` for cache, `noeviction` for queues). Monitor `used_memory` vs `maxmemory`
- Persistence: RDB snapshots + AOF for durability; AOF-only for stricter RPO
- Cluster mode for horizontal scaling; sentinel for HA with single primary

### Cassandra / ScyllaDB

- Model by query, not entity. Each query pattern = one table. Denormalization expected
- Partition key = distribution, clustering key = sort within partition
- Avoid partitions >100MB. Time bucketing for growing partitions
- `LOCAL_QUORUM` for strong consistency, `ONE` for eventual
- Avoid secondary indexes on high-cardinality columns; use materialized views or denormalized tables
- Tombstones: `gc_grace_seconds` tuning critical for deletion-heavy workloads

### DynamoDB

- Single-table design: PK + SK overloading. GSIs for alternative access patterns
- Avoid hot partitions — random suffix on PK for high-throughput items
- `ProjectionExpression` to minimize read cost. Batch for bulk ops. TTL for auto-expiration
- On-demand vs provisioned capacity — choose based on traffic predictability
- DAX for sub-millisecond read cache
- Streams for change data capture into Lambda / Kinesis

## Time-Series + Graph

### Time-Series

- TimescaleDB (PG extension): hypertables = automatic time-range partitioning + compression
- InfluxDB: tag/field separation, downsampling via continuous queries
- Use BRIN indexes on append-only time columns in PostgreSQL
- Retention policies: drop or compress partitions older than N days
- Pre-aggregate (continuous aggregates) for dashboard queries

### Graph

- Neo4j: model relationships as first-class. Cypher queries for path/traversal
- Property graphs vs RDF/SPARQL — choose based on schema rigidity
- Index on node label + property for entry points
- Avoid unbounded variable-length paths in production queries

## Monitoring + Capacity Planning

- **Key metrics**: QPS, latency (p50/p95/p99), active connections, replication lag, cache hit ratio, disk I/O, bloat
- **PostgreSQL**: `pg_stat_statements` (query analysis), `pg_stat_user_tables` (seq scans, dead tuples), `pg_stat_activity` (locks)
- **Slow query log**: Enable with threshold (100ms). Review top offenders weekly
- **Connection pooling**: PgBouncer or pgpool-II. Monitor saturation and wait time
- **Vacuum**: Tune `autovacuum` per table. Monitor `n_dead_tup`. VACUUM FULL only in maintenance windows
- **Bloat**: Monitor table/index bloat. `pg_repack` for online reorganization
- **Capacity**: Project growth from current rate + business plan. Plan disk + memory + connection headroom 6–12 months ahead

## Backup + Recovery

- **PostgreSQL**: `pg_basebackup` + WAL archiving for PITR. `pg_dump` for logical backups
- **MySQL**: `mysqldump` (logical), `xtrabackup` (physical, hot), binlog for PITR
- **Verify restores on schedule** — untested backups are not backups
- **Off-site copy**: Backups must survive primary site failure
- **Encryption at rest** for backup files
- **RTO/RPO documented and tested** per database tier

## Database Security

- **Least privilege**: App accounts get only required permissions on specific tables. Never use superuser for applications
- **Row-Level Security (RLS)**: PostgreSQL RLS for multi-tenant isolation. Enable `FORCE ROW LEVEL SECURITY` on the table owner
- **Encryption**: TLS for connections (`sslmode=verify-full`). Encryption at rest via disk/tablespace. Column-level (pgcrypto) for PII
- **Audit logging**: `pgaudit` for DDL/DML audit trail. Log all privileged operations
- **SQL injection**: Parameterized queries only. Never concatenate user input. Review stored procedures for dynamic SQL
- **No secrets in SQL files**: Connection strings, passwords, keys → env vars or secret managers

## When this applies

| Workflow | Apply this knowledge |
|---|---|
| `Agent(db-engineer)` | Auto-loaded |
| `/develop` (DB work package) | Spawned db-engineer loads this |
| `/code-review` (migration PRs) | Indexing + schema sections |
| `/architecture-design` (data model) | NoSQL + partitioning sections |
| `/migrate` (schema migrations) | Replication + backup sections |
| `/bugfix` (query/perf) | EXPLAIN + indexing sections |

## Integration

- **Consumed by**: `db-engineer` (primary), `data-engineer`, `python-engineer` / `java-engineer` (ORM review), `solution-architect`
- **External references**: PostgreSQL, MySQL, SQL Server, MongoDB, Redis, Cassandra, DynamoDB official docs
