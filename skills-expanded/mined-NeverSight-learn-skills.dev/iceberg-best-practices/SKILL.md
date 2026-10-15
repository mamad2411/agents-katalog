---
name: iceberg-best-practices
description: Apache Iceberg best practices for table design, partitioning, compaction, catalog configuration, and multi-engine lakehouse management
---

# Apache Iceberg Best Practices

## Core Principles

- Use hidden partitioning with transforms — never create explicit partition columns
- Run table maintenance regularly — expire snapshots, compact files, rewrite manifests
- Use Parquet with ZSTD compression for all data files
- Configure sort order on frequently filtered columns
- Use a production catalog (REST, Glue, or Hive Metastore) — never Hadoop catalog
- Set state TTL / snapshot retention to prevent unbounded metadata growth
- Design for schema evolution from day one — Iceberg tracks columns by ID, not name

## Table Design and Schema Evolution (CRITICAL)

### schema-evolution-safety

**Iceberg schema evolution is safe — use it instead of recreating tables.**

Every column gets a unique ID. Renaming, reordering, adding, or dropping columns are metadata-only operations that never rewrite data files.

Safe operations (metadata-only):
- Add optional column
- Drop column (data files untouched; column excluded from reads)
- Rename column (tracked by ID — historical data readable under new name)
- Reorder columns
- Widen type (`int` -> `long`, `float` -> `double`, `decimal(P,S)` -> `decimal(P',S)` where P' > P)
- Make required field optional

Not supported:
- Narrowing types (`long` -> `int`)
- Incompatible type changes (`string` -> `int`)
- Making optional field required

### schema-type-choices

**Choose types carefully — they are hard to change later.**

| Value | Recommended Type | Notes |
|-------|-----------------|-------|
| Event timestamps | `timestamptz` | Always use timezone; avoids ambiguity across engines |
| IDs | `long` | Prefer over `int` for growth headroom |
| Money | `decimal(P, S)` | Never `float`/`double` |
| UUIDs | `string` | Native `uuid` type has inconsistent engine support |
| Nested data | `struct` | Prefer over flattened column names with prefixes |

### schema-best-practices

**Design schemas for evolution from day one.**

- Add new columns as optional with documented defaults
- Use `COMMENT ON COLUMN` to track field semantics
- Coordinate with downstream consumers before dropping columns
- Test schema changes in a branch or test environment before production

---

## Partitioning (CRITICAL)

### partition-hidden

**Use hidden partitioning with transforms — never create explicit partition columns.**

Iceberg applies partition transforms automatically. Users query raw columns and the engine applies partition pruning transparently. No synthetic partition columns needed.

```sql
CREATE TABLE events (
    event_id STRING,
    event_time TIMESTAMP,
    user_id BIGINT,
    event_type STRING
) USING iceberg
PARTITIONED BY (day(event_time), bucket(16, user_id));
```

Available transforms: `year(ts)`, `month(ts)`, `day(ts)`, `hour(ts)`, `bucket(N, col)`, `truncate(L, col)`, `identity(col)`.

### partition-transform-selection

**Choose partition transforms based on data volume.**

| Data Volume | Time Transform | Notes |
|-------------|---------------|-------|
| < 10 GB/day | `month(ts)` | ~12 partitions/year |
| 10–100 GB/day | `day(ts)` | Most common choice |
| > 100 GB/day | `hour(ts)` | Only for very high volume |

For non-time columns, use `bucket(N, col)` where N produces partitions of 100 MB–1 GB each.

### partition-sizing

**Target partition sizes of 100 MB–1 GB per partition.**

- Avoid more than ~10,000 total partitions (metadata overhead)
- Avoid fewer than ~10 partitions (limits parallelism)
- If partitions produce files < 25 MB, use coarser partitioning or compaction
- If partitions produce files > 2 GB, use finer partitioning

### partition-evolution

**Iceberg supports changing partition schemes without rewriting data.**

Old data retains the old layout; new data uses the new layout. The query planner handles both transparently.

```sql
-- Evolve from monthly to daily as data volume grows
ALTER TABLE db.events SET PARTITION SPEC (day(event_time), bucket(16, user_id));
```

### partition-anti-patterns

**Avoid these partitioning mistakes.**

- `identity(high_cardinality_column)` — creates one partition per unique value
- `hour(ts)` on low-volume tables — thousands of tiny files
- Three-level partitioning — almost never needed; keep fanout manageable
- Explicit partition columns (Hive-style) — defeats Iceberg's hidden partitioning

---

## Sort Order (HIGH)

### sort-order-configuration

**Set sort order on frequently filtered columns to enable min/max metadata filtering.**

```sql
ALTER TABLE db.events WRITE ORDERED BY (tenant_id ASC NULLS LAST, event_time ASC);
```

- Sort by columns most commonly used in `WHERE` clauses (after partition columns)
- Put low-cardinality filter columns first
- Sort order applies only to newly written files; run `rewrite_data_files` with `sort` strategy to apply to existing data

### sort-order-zorder

**Use Z-order when queries filter on multiple columns with roughly equal selectivity.**

Z-order interleaves bits of multiple columns for balanced multi-dimensional clustering. Linear sort is better when one column dominates filter patterns.

```sql
CALL catalog.system.rewrite_data_files(
  table => 'db.events',
  strategy => 'zorder',
  sort_order => 'tenant_id,event_type'
)
```

---

## File Format (HIGH)

### format-parquet-zstd

**Use Parquet with ZSTD compression. There is rarely a reason to deviate.**

```sql
ALTER TABLE db.events SET TBLPROPERTIES (
  'write.format.default' = 'parquet',
  'write.parquet.compression-codec' = 'zstd'
);
```

Key tuning properties:
- `write.parquet.compression-codec`: `zstd` (recommended), `snappy`, `gzip`, `lz4`
- `write.parquet.compression-level`: 1–3 for ZSTD (good balance)
- `write.parquet.row-group-size-bytes`: 134217728 (128 MB default)
- `write.parquet.dict-size-bytes`: 2097152 (2 MB; increase for high-cardinality dictionary columns)

| Format | Use For |
|--------|---------|
| Parquet | All data files (default) |
| ORC | Migrating from Hive ORC tables |
| Avro | Delete files in merge-on-read mode only |

---

## Catalog Configuration (CRITICAL)

### catalog-selection

**Choose a production catalog. Never use Hadoop catalog in production.**

| Catalog | Best For | Notes |
|---------|----------|-------|
| REST (Polaris, Gravitino) | Multi-engine production | Vendor-neutral, spec-driven, credential vending |
| AWS Glue | AWS-native stacks | Zero infrastructure; watch for API rate limits |
| Hive Metastore | Existing Hive infrastructure | No multi-table atomic commits |
| JDBC | Development, small deployments | Simple, any JDBC database |
| Nessie | Git-like data branching | CI/CD for data, branch/merge semantics |
| Hadoop | Never in production | No atomic commits, no concurrency safety |

### catalog-rest

**Use REST catalog for multi-engine deployments.**

```
spark.sql.catalog.my_catalog=org.apache.iceberg.spark.SparkCatalog
spark.sql.catalog.my_catalog.type=rest
spark.sql.catalog.my_catalog.uri=http://catalog-host:port/api/v1
spark.sql.catalog.my_catalog.warehouse=s3://bucket/warehouse
```

REST catalog supports credential vending — engines get short-lived credentials for storage access.

### catalog-caching

**Enable catalog caching to reduce metadata lookups.**

```
spark.sql.catalog.my_catalog.cache-enabled=true
spark.sql.catalog.my_catalog.cache.expiration-interval-ms=300000
```

---

## Write Optimization (HIGH)

### write-target-file-size

**Target file sizes of 256 MB–1 GB.**

```sql
ALTER TABLE db.events SET TBLPROPERTIES (
  'write.target-file-size-bytes' = '536870912'  -- 512 MB
);
```

- High-query-frequency tables: 256–512 MB (more parallelism)
- Archival/cold tables: 512 MB–1 GB (fewer files, less metadata)
- Never below 32 MB (too many small files) or above 2 GB (too little parallelism)

### write-distribution-mode

**Choose write distribution mode based on table structure.**

| Mode | Behavior | Best For |
|------|----------|----------|
| `none` | No shuffle before writing | Append-only unpartitioned tables |
| `hash` | Hash-distribute by partition key | Partitioned tables (recommended) |
| `range` | Range-distribute by sort key | When sort order optimization is critical |

```sql
ALTER TABLE db.events SET TBLPROPERTIES (
  'write.distribution-mode' = 'hash'
);
```

### write-streaming-flink

**For Flink streaming, set checkpoint interval to 1–5 minutes and target 128 MB files.**

```sql
ALTER TABLE db.events SET TBLPROPERTIES (
  'write.target-file-size-bytes' = '134217728'  -- 128 MB for streaming
);
```

10-second checkpoint intervals create many tiny files. Use longer intervals and rely on compaction.

### write-commit-retry

**Increase commit retries for high-contention environments.**

```
commit.retry.num-retries=4
commit.retry.min-wait-ms=100
commit.manifest-merge.enabled=true
commit.manifest.target-size-bytes=8388608
```

---

## Read Optimization (HIGH)

### read-predicate-pushdown

**Always filter on partition columns first, then sorted columns.**

Iceberg pushes predicates down to three levels:
1. **Partition pruning** — skips entire partitions
2. **Manifest filtering** — min/max per file from manifest metadata
3. **Row-group filtering** — min/max within Parquet row groups

Use explicit equality and range predicates. Avoid UDFs or complex expressions that prevent pushdown.

### read-column-pruning

**Select only needed columns — never `SELECT *` on wide tables.**

Iceberg + Parquet skips entire column chunks for unselected columns. Wide tables (100+ columns) benefit enormously.

### read-metadata-metrics

**Configure column-level metrics for optimal metadata filtering.**

```sql
ALTER TABLE db.events SET TBLPROPERTIES (
  'write.metadata.metrics.default' = 'truncate(16)',
  'write.metadata.metrics.column.tenant_id' = 'full',
  'write.metadata.metrics.column.raw_payload' = 'none'
);
```

- `full`: complete min/max stats — for columns always filtered on
- `truncate(N)`: first N bytes of min/max — default, good for most strings
- `none`: no stats — for columns never filtered on (reduces metadata size)

### read-split-size

**Tune split size for read parallelism.**

```sql
ALTER TABLE db.events SET TBLPROPERTIES (
  'read.split.target-size' = '134217728'  -- 128 MB default
);
```

Decrease for more parallelism on large clusters; increase for small clusters.

### read-vectorized

**Enable vectorized reading in Spark.**

```
spark.sql.iceberg.vectorization.enabled=true
```

Processes data in columnar batches rather than row-by-row — significant speedup for scan-heavy queries.

---

## Table Maintenance (CRITICAL)

### maintenance-expire-snapshots

**Expire snapshots daily. This is the most important maintenance task.**

```sql
CALL catalog.system.expire_snapshots(
  table => 'db.events',
  older_than => TIMESTAMP '2024-01-01 00:00:00',
  retain_last => 10
);
```

Without expiration, metadata files grow unboundedly, slowing down all query planning. Keep enough snapshots for your time travel needs (default retention: 5 days).

### maintenance-compaction

**Run binpack compaction daily (hourly for streaming tables).**

```sql
CALL catalog.system.rewrite_data_files(
  table => 'db.events',
  strategy => 'binpack',
  options => map(
    'target-file-size-bytes', '536870912',
    'min-file-size-bytes', '67108864',
    'max-file-size-bytes', '1073741824',
    'min-input-files', '5',
    'partial-progress.enabled', 'true',
    'partial-progress.max-commits', '10'
  )
);
```

| Strategy | Cost | Effect |
|----------|------|--------|
| `binpack` | Low | Combines small files — routine compaction |
| `sort` | High | Re-sorts data by sort order — better read performance |
| `zorder` | High | Z-order clustering — better multi-column filtering |

Run `binpack` daily/hourly. Run `sort` weekly during off-peak hours.

### maintenance-rewrite-manifests

**Rewrite manifests weekly to improve query planning performance.**

```sql
CALL catalog.system.rewrite_manifests(table => 'db.events');
```

Consolidates many small manifest files into fewer, larger ones. Run after heavy write operations.

### maintenance-orphan-files

**Remove orphan files weekly or monthly.**

```sql
CALL catalog.system.remove_orphan_files(
  table => 'db.events',
  older_than => TIMESTAMP '2024-06-01 00:00:00',
  dry_run => true  -- preview first
);
```

Use `older_than` > max expected write duration to avoid deleting in-progress writes (default: 3 days).

### maintenance-schedule

**Recommended maintenance schedule.**

| Task | Frequency | Priority |
|------|-----------|----------|
| Expire snapshots | Daily | Critical |
| Binpack compaction | Daily / hourly (streaming) | Critical |
| Sort compaction | Weekly (off-peak) | High |
| Rewrite manifests | Weekly | Medium |
| Remove orphan files | Weekly / monthly | Medium |

---

## Time Travel and Snapshots (MEDIUM)

### timetravel-queries

**Query historical data by snapshot ID or timestamp.**

```sql
SELECT * FROM db.events VERSION AS OF 1234567890;
SELECT * FROM db.events TIMESTAMP AS OF '2024-06-15 10:00:00';
```

Time travel only works for snapshots that haven't been expired. Retain enough snapshots for your incident response SLA.

### timetravel-rollback

**Rollback is a metadata-only operation (instant).**

```sql
CALL catalog.system.rollback_to_snapshot('db.events', 1234567890);
CALL catalog.system.rollback_to_timestamp('db.events', TIMESTAMP '2024-06-15 10:00:00');
```

Does not delete data files — the rolled-back-to snapshot's files are still present.

### timetravel-tags

**Use tags to protect important snapshots from expiration.**

```sql
ALTER TABLE db.events CREATE TAG release_2024_q2 AS OF VERSION 1234567890 RETAIN 365 DAYS;
```

Tagged snapshots are immune from `expire_snapshots` for the retention period.

---

## Merge-on-Read vs Copy-on-Write (HIGH)

### mor-vs-cow

**Choose based on read/write ratio.**

| Mode | Write Speed | Read Speed | Best For |
|------|------------|------------|----------|
| Copy-on-Write | Slow (rewrites files) | Fast (no delete files) | Read-heavy, batch updates |
| Merge-on-Read | Fast (append delete markers) | Slower (merge at read time) | Write-heavy, streaming CDC |

```sql
-- Copy-on-Write (default, recommended for most tables)
ALTER TABLE db.events SET TBLPROPERTIES (
  'write.delete.mode' = 'copy-on-write',
  'write.update.mode' = 'copy-on-write',
  'write.merge.mode' = 'copy-on-write'
);

-- Merge-on-Read (for streaming/CDC tables)
ALTER TABLE db.events SET TBLPROPERTIES (
  'write.delete.mode' = 'merge-on-read',
  'write.update.mode' = 'merge-on-read',
  'write.merge.mode' = 'merge-on-read'
);
```

**Positional vs equality deletes:**
- Positional deletes reference file path + row position — efficient for engines to apply, used by Spark
- Equality deletes reference column values to match — more flexible but more expensive at read time
- Positional deletes are preferred; Iceberg v2 supports both

**Critical for MoR:** Run compaction regularly to merge delete files into base data files. If a data file has >10 associated delete files, compaction is overdue.

---

## Multi-Engine Integration (HIGH)

### integration-spark

**Spark has the most mature Iceberg integration.**

```
spark.sql.catalog.my_catalog=org.apache.iceberg.spark.SparkCatalog
spark.sql.catalog.my_catalog.type=rest
spark.sql.catalog.my_catalog.uri=http://catalog-host:port/api/v1
```

- Use Spark for all maintenance procedures (`rewrite_data_files`, `expire_snapshots`, etc.)
- Enable vectorized reads: `spark.sql.iceberg.vectorization.enabled=true`
- Use `DataFrame.writeTo("catalog.db.table").append()` or `.overwritePartitions()` for writes
- `spark.sql.shuffle.partitions` affects output file count

### integration-flink

**Flink is best for streaming ingestion into Iceberg.**

- Set checkpoint interval to control commit frequency (1–5 minutes)
- `write.upsert.enabled=true` for CDC upsert semantics
- Flink writes smaller files by nature (streaming) — rely on compaction to consolidate
- Target 128 MB file sizes for streaming

### integration-trino

**Trino is excellent for interactive analytics and ad-hoc queries.**

- Supports reads, writes, schema evolution, time travel, hidden partitioning
- Does not support all maintenance procedures — use Spark for full maintenance
- Set `iceberg.file-format=PARQUET` and `iceberg.compression-codec=ZSTD`

### integration-cross-engine

**Use a shared catalog for multi-engine access.**

- All engines read/write the same Iceberg format — true interoperability
- Ensure all engines use compatible Iceberg library versions
- Avoid engine-specific table properties when multi-engine access is needed

---

## Branching and Tagging (MEDIUM)

### branching-wap

**Use branches for Write-Audit-Publish (WAP) workflows.**

```sql
-- Create a branch
ALTER TABLE db.events CREATE BRANCH audit_branch;

-- Write to branch (Spark)
SET spark.wap.branch = audit_branch;
INSERT INTO db.events VALUES (...);

-- Read from branch
SELECT * FROM db.events VERSION AS OF 'audit_branch';

-- Fast-forward main after validation
CALL catalog.system.fast_forward('db.events', 'main', 'audit_branch');
```

### branching-nessie

**Use Nessie for catalog-level branching across multiple tables.**

Nessie provides Git-like branching across the entire catalog. Create a branch, modify multiple tables, merge atomically. Enables data CI/CD with merge conflict detection.

### branching-cleanup

**Set retention on branches and tags. Clean up stale branches.**

```sql
ALTER TABLE db.events DROP BRANCH old_branch;
```

Unmanaged branches and tags cause unbounded metadata growth.

---

## Common Anti-Patterns

| Anti-Pattern | Problem | Solution |
|---|---|---|
| `identity(high_cardinality_col)` | One partition per unique value | Use `bucket(N, col)` |
| `hour(ts)` on low-volume tables | Thousands of tiny files | Use `day(ts)` or `month(ts)` |
| Not expiring snapshots | Metadata grows unboundedly | Expire daily, retain what you need |
| Not compacting (streaming/MoR) | Small files degrade reads | Binpack hourly for streaming |
| Hadoop catalog in production | No atomic commits, unsafe | Use REST, Glue, or Hive catalog |
| `SELECT *` on wide tables | Reads all columns | Project only needed columns |
| No sort order | Min/max filtering ineffective | Sort by frequently filtered columns |
| Delete file accumulation (MoR) | Exponential read degradation | Compact to merge deletes into base |
| `TIMESTAMP` without timezone | Ambiguity across engines/regions | Use `timestamptz` |
| Tiny streaming commit intervals | Many tiny files | Use 1–5 minute intervals + compaction |
| Incompatible library versions | Metadata corruption | Align versions across engines |
| Explicit partition columns | Defeats hidden partitioning | Use partition transforms |
| Skipping `rewrite_manifests` | Slow query planning | Rewrite weekly |
| Large updates with copy-on-write | Wasteful file rewrites | Switch to merge-on-read |
