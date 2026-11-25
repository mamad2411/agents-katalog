---
name: optimize-olap-database
description: Design high-throughput OLAP schemas for Iceberg v3, tune ClickHouse/DuckDB columnar engines, configure 8192-row sparse index granules, govern partition key cardinality, enable MinMax data skipping, implement streaming micro-batch buffering, profile query execution plans, enforce native table encryption (KMS), and prepare for Spark 4.2+/Flink 2.3. Use when designing, tuning, or troubleshooting high-throughput columnar databases and analytical storage engines.
version: 2.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_build, run_tests]
---

# Optimize OLAP Database

Use this skill when designing, tuning, or troubleshooting high-throughput columnar databases (ClickHouse, DuckDB, Apache Iceberg v3). For ad-hoc exploratory querying and cross-source joins, use `query-analytical-engine` instead.

## When to Use

- designing columnar database schemas and primary sorting keys for ClickHouse, DuckDB, or Apache Iceberg v3
- configuring sparse primary index granules (8192-row alignment) to minimize index RAM footprint
- governing partition key cardinality (`PARTITION BY toYYYYMM`) to prevent the "Too many parts" error
- adding secondary data skipping indexes (minmax, set, bloom filter, tokenbf_v1) for non-prefix filter columns
- accelerating dimension lookups via LowCardinality dictionary encoding and in-memory external dictionaries
- designing streaming micro-batch ingestion pipelines (Buffer engine, Kafka MV, 256MB Parquet blocks)
- profiling query performance bottlenecks using `EXPLAIN PIPELINE`, `EXPLAIN ESTIMATE`, and `EXPLAIN PLAN`
- configuring automated TTL lifecycle policies for data expiration and tiered storage migration to S3
- deploying specialized MergeTree engines (ReplacingMergeTree, SummingMergeTree, AggregatingMergeTree)
- **implementing native table encryption (KMS) for Iceberg and Delta Lake tables**
- **preparing for Spark 4.2+ and Flink 2.3 compatibility**

## Core Rules

- **Sparse Index Granularity**: align ClickHouse primary keys with 8192-row granules (`index_granularity = 8192`); order primary key columns strictly from lowest to highest cardinality.
- **Partition Key Governance**: govern partition key cardinality to maintain <= 1000 active parts per table (e.g. `toYYYYMM(event_date)`); never partition by high-cardinality columns (UUID, timestamp by second).
- **Secondary Data Skipping**: configure `minmax`, `set(max_rows)`, or `bloom_filter` indexes on non-primary-key filter columns to eliminate unnecessary granule scans.
- **Dictionary Acceleration**: encode low-cardinality string columns as `LowCardinality(String)` and cache dimension tables in memory via `CREATE DICTIONARY` to replace distributed hash joins with O(1) lookups.
- **Micro-Batch Buffering**: prohibit single-row streaming inserts; enforce client or engine buffering (Buffer table engine or Kafka MV) with batches >= 10,000 rows or 5–30s flush intervals.
- **Engine Specialization**: leverage `ReplacingMergeTree` for deduplication, `SummingMergeTree` for metric accumulation, and `AggregatingMergeTree` with `-State`/`-Merge` combinators for pre-computed rollups.
- **Plan Profiling**: inspect execution plans via `EXPLAIN ESTIMATE` and `EXPLAIN PIPELINE header=1` before promoting queries to production dashboards.
- **TTL Lifecycle & Tiering**: declare table TTLs to purge stale data and tier cold partitions to S3 object storage (`TTL event_date + INTERVAL 30 DAY TO VOLUME 's3_cold'`).
- **Native Table Encryption (KMS)**: mandate AES-256 encryption at rest via cloud KMS (AWS KMS, GCP CMEK, Azure Key Vault) for all Iceberg and Delta Lake tables.
- **Spark 4.2+ & Flink 2.3 Readiness**: prepare OLAP schemas for compatibility with Spark 4.2+ compute engines and Flink 2.3 streaming sinks; validate schema evolution paths and partition evolution strategies.
- Detailed architecture, DDL templates, and profiling runbooks are maintained in [`references/olap-database-guide.md`](references/olap-database-guide.md).

## Suggested Process

### 1. Workload Profiling & Access Pattern Identification
Analyze query filter predicates, aggregation grains, and data arrival rates. Identify primary sort keys and dimension lookup requirements.

### 2. Schema Design & Primary Key Ordering
Define columnar DDL with `ORDER BY (tenant_id, event_date, event_type, id)`. Apply `LowCardinality(String)` to categorical columns.

### 3. Partition Strategy & Skipping Index Configuration
Configure coarse partition key (`PARTITION BY toYYYYMM(event_date)`). Attach secondary `minmax` and `bloom_filter` skipping indexes for selective non-key filters.

### 4. Ingestion Buffering & Engine Selection
Select MergeTree family engine (`ReplacingMergeTree`, `AggregatingMergeTree`). Configure client micro-batching or Buffer engine to guarantee batch flushes >= 10,000 rows.

### 5. Query Plan Profiling & Optimization Verification
Run `EXPLAIN ESTIMATE` and `EXPLAIN PIPELINE header=1`. Verify that index pruning eliminates >= 80% of unneeded granules without full table scans.

### 6. Native Encryption & Compatibility
Implement AES-256 encryption via KMS for all Iceberg tables. Validate Spark 4.2+ and Flink 2.3 compatibility for schema evolution and partition strategies.

### 7. Emit Data Pipeline Specification
Validate specifications against `contracts/schemas/data-pipeline-spec.json` and document schema properties.

## Checklist

- [ ] primary key columns ordered from lowest to highest cardinality with 8192-row granule alignment
- [ ] partition key expression evaluated to guarantee <= 1000 active parts across table lifecycle
- [ ] secondary skipping indexes (`minmax`, `set`, or `bloom_filter`) configured for non-primary filter columns
- [ ] low-cardinality categorical dimensions encoded via `LowCardinality(String)` or memory dictionaries
- [ ] streaming ingestion configured with micro-batch buffering (>= 10,000 rows or 5–30s intervals)
- [ ] query execution plan profiled via `EXPLAIN ESTIMATE` and `EXPLAIN PIPELINE header=1`
- [ ] automated TTL policies configured for data retention and S3 tiered storage migration
- [ ] schema specifications emitted and validated against `contracts/schemas/data-pipeline-spec.json`
- [ ] **Native table encryption (KMS) implemented** for Iceberg and Delta Lake tables
- [ ] **Spark 4.2+ and Flink 2.3 compatibility validated** for schema evolution and partition strategies

## Related Skills

- **build-data-pipeline**: Design transactional lakehouse pipelines and WAP branches for Iceberg tables
- **database-maintenance**: Execute 256MB bin-pack compaction and snapshot expiration
- **query-analytical-engine**: Execute in-process embedded SQL via chDB/DuckDB and cross-source joins
- **create-migration**: Author version-controlled DDL migration scripts for relational stores
- **security-audit**: Audit access control, TLS encryption, and PII masking across analytical stores

## Output Contracts

When emitting OLAP database specifications and performance audit results, emit:

- `contracts/schemas/data-pipeline-spec.json` — complete table definition, engine parameters, partition key, index granules, buffering rules, TTL policies, **native encryption (KMS) config, Spark 4.2+/Flink 2.3 compatibility notes**.
- `contracts/schemas/data-analysis-report.json` — query profiling benchmarks, scanned parts/marks metrics, and storage reduction figures.

## Failure Modes

- **Part fragmentation storm**: high-frequency single-row inserts create thousands of tiny parts, causing "Too many parts" merge errors. Mitigation: enforce micro-batch buffering >= 10,000 rows.
- **Over-partitioning catastrophe**: partitioning by high-cardinality columns exhausts filesystem inodes and crashes merges. Mitigation: restrict partition keys to coarse date ranges (`toYYYYMM`).
- **Primary key prefix misordering**: high-cardinality column placed first in `ORDER BY` disables pruning for subsequent columns. Mitigation: sort primary keys by cardinality ascending.
- **Unindexed cartesian joins**: joining large tables without dictionaries or subquery projections exhausts memory. Mitigation: pre-cache dimension tables in dictionaries and use `dictGet()`.
- **Missing native table encryption (KMS)**: Iceberg tables lack AES-256 encryption at rest. Mitigation: mandate KMS-managed encryption for all production lakehouse tables.
- **Incompatible with Spark 4.2+/Flink 2.3**: OLAP schemas break with newer compute engines. Mitigation: validate compatibility, test schema evolution paths, prepare for VARIANT type support.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: enforce role-based access control and read-only connection scoping for analytical query clients.
- **ASI04 Agentic Supply Chain**: validate database connectors, dictionary source drivers, and extension packages against verified package repositories.
- **ASI05 Unexpected Code Execution**: prohibit unvalidated raw SQL execution; parameterize dynamic filters and sanitize table identifiers.
- **ASI06 Memory & Context Poisoning**: sanitize document table extracts (Kreuzberg patterns) and validate schema contracts before lakehouse persistence.
- **ASI07 Insecure Inter-Agent Communication**: emit machine-readable `data-pipeline-spec.json` contracts for downstream agents.
- **ASI09 Human-Agent Trust Exploitation**: report true scanned row counts, query latencies, and storage overhead transparently.
- **NATIVE-ENCRYPTION-LOCK**: all Iceberg and Delta Lake tables must enforce AES-256 encryption at rest via cloud KMS; encryption keys managed through catalog-integrated key management.
- **SPARK-FLINK-COMPATIBILITY-LOCK**: OLAP schemas must maintain compatibility with Spark 4.2+ compute engines and Flink 2.3 streaming sinks; validate schema evolution paths and partition strategies.
