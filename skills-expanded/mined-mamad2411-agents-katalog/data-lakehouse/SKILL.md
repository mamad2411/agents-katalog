---
name: data-lakehouse
version: 1.0.0
min_mindforge_version: 10.6.0
status: stable
triggers: data lakehouse architecture, medallion architecture, schema evolution lakehouse, time travel data, partition optimization, Delta Lake implementation, Iceberg table design, lakehouse query performance, data lakehouse governance, lakehouse ingestion, lakehouse serving layer, lakehouse cost optimization
---

# Skill — Data Lakehouse

## When this skill activates
This skill activates when implementing lakehouse architectures combining data lake flexibility with data warehouse performance. Use when building Delta Lake, Iceberg, or Hudi tables with ACID guarantees, schema evolution, and time travel capabilities.

## Mandatory actions when this skill is active

### Before writing any code
1. Design medallion architecture layers: bronze (raw ingestion), silver (cleansed/conformed), gold (business-level aggregates) with clear promotion criteria
2. Select table format (Delta, Iceberg, Hudi) based on requirements: write patterns, query patterns, ecosystem compatibility, and feature needs
3. Plan partitioning strategy based on query patterns: typically date/time for time-series, geography for location-based, or composite keys avoiding over-partitioning (<1000 partitions)
4. Define schema evolution policy: additive changes (safe), nullable to required (breaking), type changes (migration required) with versioning strategy

### During implementation
- Implement ACID transactions for atomic writes: use table format's transaction log (Delta Log, Iceberg metadata) to ensure consistency
- Configure file sizing for optimal query performance: target 128MB-1GB per file, run regular OPTIMIZE/COMPACT operations to prevent small files
- Enable time travel with retention policy: maintain snapshots for point-in-time queries and audit, configure vacuum/expire based on compliance needs
- Design incremental processing patterns: merge/upsert operations for CDC, append for event streams, overwrite partitions for batch updates
- Implement Z-ordering or clustering on frequently filtered columns (non-partition keys) to improve query performance via data skipping
- Build schema evolution handlers: automatic schema merging for new columns, validation for breaking changes, schema registry integration
- Create data quality checkpoints between medallion layers: row counts, null checks, referential integrity, business rule validation with quarantine tables

### After implementation
- Monitor table health metrics: file count, average file size, partition count, metadata size, and compaction needs
- Build cost optimization reports: storage by layer, compute for jobs, query costs, and opportunities for partition pruning or materialization
- Create governance controls: table-level access policies, column masking, row filtering, and audit logging for sensitive data access
- Generate performance analysis: query patterns, partition pruning effectiveness, file skipping statistics, and optimization recommendations

## Self-check before task completion
- [ ] Medallion layers clearly defined with data quality gates between bronze → silver → gold promotions
- [ ] Partitioning strategy optimized for query patterns with validation that queries prune partitions effectively
- [ ] ACID transactions tested with concurrent writes and failure scenarios to ensure consistency
- [ ] Schema evolution tested with backward and forward compatibility for common evolution scenarios
- [ ] File management strategy (OPTIMIZE/VACUUM) scheduled with monitoring for small file accumulation
