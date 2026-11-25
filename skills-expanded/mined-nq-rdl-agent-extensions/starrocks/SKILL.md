---
name: starrocks
license: CC-BY-4.0
description: >-
  StarRocks analytical data warehouse skill. Use when writing or reviewing
  StarRocks SQL, designing tables, choosing partition/bucket strategies,
  loading or unloading data, creating materialized views, tuning queries,
  or working with external catalogs (Hive, Iceberg, Hudi, Delta Lake).
  Covers DBA and data architect concerns — not cluster deployment or
  platform engineering. Trigger on mentions of 'starrocks', 'StarRocks',
  table types (Duplicate Key, Primary Key, Aggregate, Unique Key),
  Routine Load, Stream Load, or StarRocks-specific SQL.
compatibility: >-
  Requires a StarRocks cluster and a MySQL-compatible client. Examples as
  written need StarRocks v3.3.5+ (cpu_weight); Arrow Flight SQL needs
  v3.5.1+. Per-feature minimums are listed in the body. Checked against
  docs.starrocks.io on 2026-09-29, when the latest release was 4.1.3.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# StarRocks — Analytical Data Warehouse Guide

StarRocks is an MPP analytical database with columnar storage, a fully vectorized
execution engine, a cost-based optimizer (CBO), and MySQL protocol compatibility.
It supports real-time ingestion, sub-second queries, and zero-migration data lake
analytics via external catalogs.

Verify against the canonical docs (https://docs.starrocks.io/docs/introduction/StarRocks_intro/; versioned
docs exist from 3.3, e.g. `/docs/3.3/...`) when being wrong would mislead, and
check the cluster version with `SELECT current_version();` before using a
version-gated feature.

| Minimum version | Features used in this skill |
|-----------------|-----------------------------|
| v3.0 | Expression partitioning with `date_trunc`; separate sort key (`ORDER BY`) for Primary Key tables |
| v3.1 | Random bucketing; sync MVs with expressions; Skew Join V1 |
| v3.2 | Pipe; `INSERT INTO FILES` (Parquet); `information_schema.routine_load_jobs` |
| v3.3 | ORC/CSV unload; Flat JSON (v3.3.3 in shared-data) |
| v3.3.5 | Resource group `cpu_weight` (earlier: `cpu_core_limit`) |
| v3.5.1 | Arrow Flight SQL |

Before writing DDL or loading data, read the relevant reference files:
- `references/table-design.rst` — Table types, partitioning, bucketing, indexing quick-ref
- `references/data-loading.rst` — Loading methods comparison and patterns
- `references/query-acceleration.rst` — Materialized views, CBO, join strategies, caching

---

## Table Design

### Choose the Right Table Type

| Type | Use When | Key Behaviour |
|------|----------|---------------|
| **Duplicate Key** | Raw logs, append-only data | Rows stored as-is; sort key for scan efficiency |
| **Aggregate** | Pre-aggregated metrics | Rows with same key auto-aggregate (SUM, MAX, MIN, etc.) |
| **Unique Key** | Dimension tables, dedup | Latest row per key wins (merge-on-read) |
| **Primary Key** | Real-time upserts, CDC | Latest row per key wins (delete+insert, better read perf) |

**Default choice**: Primary Key for mutable data, Duplicate Key for append-only.

### Partitioning

Partition by time or a low-cardinality dimension that aligns with query predicates.
Use expression-based partitioning for automatic partition creation. A Primary Key
table's primary key must include its partition and bucket columns:

```sql
CREATE TABLE events (
    event_time  DATETIME NOT NULL,
    user_id     BIGINT NOT NULL,
    event_type  VARCHAR(64),
    payload     JSON
)
PRIMARY KEY (event_time, user_id)
PARTITION BY date_trunc('day', event_time)
DISTRIBUTED BY HASH(user_id) BUCKETS 16
ORDER BY (user_id, event_time)
PROPERTIES ("replication_num" = "3");
```

### Bucketing

- **Hash bucketing** — use when queries filter on specific columns (e.g., `user_id`)
- **Random bucketing** — use for append-only tables without clear filter columns
  (Duplicate Key tables only)
- Bucket count: omit `BUCKETS` to let StarRocks set it; if set manually, the docs
  recommend about 10 GB of raw data per tablet

### Sort Key (Table Clustering)

The sort key is the highest-leverage physical design knob. Place the most frequently
filtered columns first. For Primary Key tables, set it with `ORDER BY`; without
`ORDER BY`, the primary key is used.

### Indexing

| Index Type | Best For |
|------------|----------|
| Prefix index | Range scans on leading sort key columns (automatic) |
| Bitmap index | Low-cardinality columns in WHERE clauses |
| Bloom filter | High-cardinality equality lookups |
| Ngram bloom filter | LIKE '%substring%' queries on text columns |

---

## Data Loading

### Method Selection

| Method | Source | Best For |
|--------|--------|----------|
| **Stream Load** | HTTP push | Small batches, real-time micro-batch |
| **Broker Load** | S3, HDFS, GCS | Large-scale batch import from object storage |
| **INSERT INTO** | SQL | Small inserts, ETL within StarRocks |
| **Routine Load** | Kafka | Continuous streaming ingestion |
| **Spark connector** | Spark | ETL pipelines via Spark jobs |
| **Flink connector** | Flink | Streaming ETL via Flink |
| **Pipe** | S3 (continuous) | Auto-discovery of new files in a bucket |
| **INSERT INTO FILES** | StarRocks → S3/HDFS | Data export to remote storage |

### Loading Best Practices

- Use Primary Key tables for CDC/upsert workloads
- Transform data during load with column expressions to avoid post-load ETL
- Enable strict mode to reject rows that fail type conversion
- For Kafka: one Routine Load job per topic partition group; monitor via
  `information_schema.routine_load_jobs`

See `references/data-loading.rst` for detailed patterns per method.

---

## Data Unloading

- **EXPORT** — CSV to HDFS/S3; simple but limited formats
- **INSERT INTO FILES** — Parquet/ORC/CSV to S3/HDFS with partitioned output
- **Arrow Flight SQL** — High-throughput programmatic access (v3.5.1+; enable
  `arrow_flight_port` on FE and BE)
- **Spark/Flink connectors** — Read StarRocks tables as DataFrames

Prefer `INSERT INTO FILES` for bulk export with format control. `compression` is
required, and S3 needs `aws.s3.region`:

```sql
INSERT INTO FILES (
    "path" = "s3://bucket/export/",
    "format" = "parquet",
    "compression" = "zstd",
    "aws.s3.region" = "us-west-2",
    "aws.s3.access_key" = "...",
    "aws.s3.secret_key" = "..."
)
SELECT * FROM my_table WHERE dt = '2024-01-01';
```

Partitioned output, EXPORT and Arrow Flight setup: `references/data-loading.rst` → "Data Unloading".

---

## Query Acceleration

### Cost-Based Optimizer (CBO)

Collect statistics so the CBO can choose optimal plans (`ANALYZE [FULL|SAMPLE] TABLE`)
and check freshness with `SHOW STATS META` — there is no `SHOW COLUMN STATS`.
See `references/query-acceleration.rst` → "Cost-Based Optimizer (CBO) Statistics".

### Materialized Views

- **Synchronous MVs** — single-table, auto-refreshed on load, transparent rewrite
- **Asynchronous MVs** — multi-table, `REFRESH ASYNC EVERY (INTERVAL ...)` or manual
  refresh, query rewrite

Examples and limits: `references/query-acceleration.rst` → "Materialized Views".

### Join Optimizations

- **Colocate join** — eliminates shuffle when joined tables share the same
  distribution (same bucket columns and count). Set `"colocate_with"` property.
- **Skew join** — V1 query rewrite (v3.1+, default) or V2 hint-based broadcast of
  named skew values (v3.5+)
- **Lateral join** — use with `unnest()` for array/JSON expansion

### Caching

- **Query cache** — caches per-tablet intermediate aggregation results; useful for
  repeated dashboard aggregations
- **Data cache** — caches remote storage data on local disks (shared-data and
  external tables)

See `references/query-acceleration.rst` for the full acceleration toolkit.

---

## Catalog & Schema Management

### Internal vs External Catalogs

- **Internal catalog** (`default_catalog`) — StarRocks-managed tables
- **External catalogs** — query Hive, Iceberg, Hudi, Delta Lake, JDBC without data movement

```sql
-- Create a Hive external catalog
CREATE EXTERNAL CATALOG hive_catalog
PROPERTIES (
    "type" = "hive",
    "hive.metastore.uris" = "thrift://metastore:9083"
);

-- Query across catalogs
SELECT s.user_id, h.page_views
FROM default_catalog.analytics.sessions s
JOIN hive_catalog.web.pageviews h ON s.user_id = h.user_id;
```

### Information Schema

Use `information_schema` views for metadata queries:

- `tables` / `columns` — table and column metadata
- `materialized_views` — MV definitions and refresh status
- `loads` (v3.1+) / `load_tracking_logs` (v3.0+) — load job status and errors
- `routine_load_jobs` (v3.2+) — Kafka ingestion job monitoring
- `be_tablets` — tablet distribution across BE nodes
- `partitions_meta` (v3.1+) — partition details

---

## Resource Groups

Isolate workloads for multi-tenant environments. `WITH` properties must be quoted
strings. `cpu_weight` needs v3.3.5+; earlier versions call it `cpu_core_limit`:

```sql
-- Create a resource group for ETL workloads
CREATE RESOURCE GROUP etl_group
TO (user = 'etl_user')
WITH ('cpu_weight' = '4', 'mem_limit' = '40%', 'concurrency_limit' = '20');

-- Create a resource group for dashboard queries
CREATE RESOURCE GROUP dashboard_group
TO (user = 'dashboard_user')
WITH ('cpu_weight' = '8', 'mem_limit' = '30%', 'concurrency_limit' = '50');
```

---

## Best Practices Summary

1. **Partition by time** — align with query predicates and retention policies
2. **Hash-bucket on the most filtered column** — reduces scan width
3. **Sort key = most selective filter columns first** — maximises prefix index hit rate
4. **Collect CBO stats after bulk loads** — stale stats produce bad plans
5. **Use async MVs for cross-table aggregates** — offload repeated joins to refresh time
6. **Primary Key tables for CDC** — better read performance than Unique Key
7. **Colocate tables that join frequently** — eliminates network shuffle
8. **Monitor via information_schema** — `loads`, `routine_load_jobs`, `be_tablets`

---

## References

Documentation URLs here and in the local references were verified against the
official StarRocks site on 2026-09-16.

- [StarRocks Introduction](https://docs.starrocks.io/docs/introduction/StarRocks_intro/)
- [Best Practices](https://docs.starrocks.io/docs/best_practices/)
- [Table Design](https://docs.starrocks.io/docs/table_design/)
- [Data Loading](https://docs.starrocks.io/docs/loading/)
- [Data Unloading](https://docs.starrocks.io/docs/unloading/)
- [Information Schema](https://docs.starrocks.io/docs/sql-reference/information_schema/)
- [Query Acceleration](https://docs.starrocks.io/docs/using_starrocks/)
- `references/table-design.rst` — Table types, partitioning, bucketing, indexing quick-ref
- `references/data-loading.rst` — Loading methods comparison and patterns
- `references/query-acceleration.rst` — Materialized views, CBO, join strategies, caching
