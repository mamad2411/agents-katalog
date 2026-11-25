---
name: database-maintenance
description: Plan and execute operational data store and modern lakehouse maintenance, including Apache Iceberg/Delta 256MB bin-pack compaction merging Deletion Vectors, manifest rewriting, snapshot expiration, 72h orphan vacuuming, and FinOps cost attribution. Use when performing cleanup, compaction, repair, index reindexing, or operational performance tuning.
version: 1.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, query_db, read_database, run_tests]
---

# Database Maintenance

Use this skill when planning or performing operational maintenance on relational databases, pgvector stores, or modern lakehouses to preserve health, query performance, and financial efficiency.

## When to Use

- compacting small files in Apache Iceberg or Delta Lake tables via bin-pack rewriting and merging Deletion Vectors to target 256MB Parquet blocks
- consolidating fragmented Avro manifests via `rewrite_manifests` for rapid query planning
- expiring stale lakehouse snapshots with 7-day TTL while preserving a 50-snapshot safety floor
- vacuuming orphaned data files with a mandatory 72-hour grace window to safeguard concurrent writers
- tuning multi-dimensional Z-Order clustering on high-cardinality columns and partition pruning strategies
- calculating Data FinOps metrics (file reduction ratio, storage reclaimed GB, monthly S3 GET savings) and tagging runs with CostCenter, Environment, and TableOwner
- monitoring analytical query costs, setting 50 GB scan limits, and enforcing warehouse auto-suspend (≤ 60s)
- rebuilding fragmented B-tree, HNSW, or IVFFlat pgvector indexes concurrently

## Core Rules

- assess store state and small file distribution before initiating maintenance
- **bin-pack file compaction**: run `rewrite_data_files` merging Deletion Vectors (Puffin RoaringBitmaps) to target 256 MB Parquet blocks (min 64 MB, max 512 MB)
- **manifest consolidation**: execute `rewrite_manifests` to coalesce micro-batch manifests into sorted manifest lists
- **snapshot lifecycle**: enforce 7-day TTL with an immutable minimum 50-snapshot safety floor (`retain_last = 50`)
- **orphan vacuuming**: execute `remove_orphan_files` strictly enforcing a 72-hour safety grace window to protect in-flight transactions
- **Data FinOps tracking**: calculate file reduction ratio, storage reclaimed (GB), and projected monthly S3 GET savings; tag every job with `CostCenter`, `Environment`, and `TableOwner`
- **query scan ceilings**: auto-abort queries projecting > 50 GB scans without partition filters; enforce warehouse auto-suspend (≤ 60s)
- **relational safety**: always use `REINDEX CONCURRENTLY` and enforce mandatory lock timeout `SET lock_timeout = '2s';`
- **object storage prefix hashing**: verify `write.object-storage.enabled = true` on Iceberg tables to eliminate AWS S3 503 Slow Down throttling
- require an approved rollback and backup plan before initiating any destructive or compaction operation
- detailed SQL runbooks, procedures, and FinOps policies are maintained in [`references/lakehouse-ops-and-finops.md`](references/lakehouse-ops-and-finops.md) and [`references/relational-and-vector-maintenance.md`](references/relational-and-vector-maintenance.md)

## Suggested Process

### 1. Assess Store State & Bloat Metrics
Inspect table bloat, dead tuple ratios, fragmented vector index graphs, or lakehouse small file counts and snapshot ages.

### 2. Formulate Maintenance Window & Rollback Plan
Determine online concurrency feasibility. Establish maintenance windows, lock timeout thresholds, and rollback criteria.

### 3. Execute Bin-Pack Compaction & Manifest Rewriting
Execute `rewrite_data_files` to merge files and resolve Deletion Vectors into target 256MB Parquet blocks. Run `rewrite_manifests` to consolidate Avro manifests.

### 4. Execute Snapshot Expiration & Orphan Vacuuming
Expire snapshots older than 7 days while retaining a minimum 50-snapshot floor. Vacuum unreferenced files older than 72 hours.

### 5. Enforce FinOps Cost Attribution & Tagging
Compute file reduction ratio, storage reclaimed (GB), and projected monthly S3 GET request savings. Tag execution with `CostCenter`, `Environment`, and `TableOwner`.

### 6. Verify Health & Post-Maintenance SLA
Validate query latency improvements, verify optimizer statistics, and confirm table integrity before closing the window.

## Checklist

- [ ] table bloat, small file distribution, and snapshot tree inspected before execution
- [ ] `write.object-storage.enabled = true` verified to distribute objects and prevent S3 503 throttling
- [ ] bin-pack compaction executed via `rewrite_data_files` merging Deletion Vectors to target 256MB Parquet blocks
- [ ] manifest files rewritten via `rewrite_manifests` to coalesce small Avro manifests
- [ ] snapshots older than 7 days expired via `expire_snapshots` preserving the 50-snapshot safety floor
- [ ] orphan files vacuumed via `remove_orphan_files` with a mandatory 72-hour grace period
- [ ] FinOps cost attribution calculated (file reduction ratio, reclaimed GB, projected monthly S3 GET savings)
- [ ] maintenance runs tagged with `CostCenter`, `Environment`, and `TableOwner` metadata
- [ ] relational maintenance executed with `CONCURRENTLY` and `SET lock_timeout = '2s';`
- [ ] query scan ceilings (≤ 50 GB) and warehouse auto-suspend (≤ 60s) enforced
- [ ] post-maintenance query benchmarks and plan emitted against `contracts/schemas/deployment-plan.json`

## Related Skills

- **build-data-pipeline**: Producer contract enforcement, WAP branches, and lakehouse ingestion architecture
- **analyze-data**: Semantic metric querying, statistical drift testing, and query cost profiling
- **create-migration**: Relational DDL schema changes and non-destructive migrations
- **performance-profiling**: Measure query latencies, execution plans, and compaction impact
- **troubleshoot-service**: Diagnose operational bottlenecks, metadata bloat, or lock contention
- **review-service**: Review release and operational risks following data store maintenance
- **commit-code**: Safely commit updated maintenance runbooks and configuration scripts

## Output Contracts

When maintenance operations are coordinated with SRE, release managers, or audit agents, emit:

- `contracts/schemas/deployment-plan.json` — detailing maintenance window, target tables, execution steps, rollback procedure, and validation benchmarks.
- `contracts/schemas/data-pipeline-spec.json` — verifying storage format properties, compaction schedule, and FinOps budget thresholds.
- Markdown runbook / FinOps report summarizing file reduction ratio, storage reclaimed (GB), projected monthly S3 GET savings, and resource tags (`CostCenter`, `Environment`, `TableOwner`).

## Failure Modes

- **Lakehouse metadata explosion**: unmanaged snapshot commits create gigabytes of metadata JSON and S3 503 storms. Mitigation: enforce automated 7-day TTL snapshot expiration with `rewrite_manifests` and S3 prefix hashing.
- **Corrupted snapshot cleanup**: aggressive vacuuming removes active time-travel references. Mitigation: maintain a strict 50-snapshot retention safety floor.
- **In-flight transaction deletion**: vacuuming removes files written by concurrent active commits. Mitigation: mandate a 72-hour grace window on orphan removal.
- **Exclusive lock starvation**: relational DDL blocks application queries. Mitigation: enforce `SET lock_timeout = '2s';` on every maintenance command.
- **Uncontrolled scan costs**: full table scans inflate warehouse bills. Mitigation: enforce 50 GB scan limits and warehouse auto-suspend timers (≤ 60s).

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: restrict maintenance roles to least-privilege operations; avoid superuser connections for routine index or compaction work.
- **ASI04 Supply Chain**: validate maintenance CLI tools, database extensions, and catalog drivers against approved manifests.
- **ASI05 RCE Guard**: parameterize all maintenance commands; never build dynamic SQL from untrusted inputs.
- **ASI07 Inter-Agent Communication**: emit structured `deployment-plan.json` so coordinating agents share identical execution parameters.
- **ASI09 Human-Agent Trust Exploitation**: surface rollback risks, expected lock impacts, and storage reclaimed honestly without omitting failure probabilities.
