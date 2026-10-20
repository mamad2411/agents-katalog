---
name: designing-data-models
description: Designs database schemas and data models — choosing relational vs document vs key-value vs time-series stores, normalization, indexing, partitioning, and zero-downtime schema migrations. Use when creating tables or collections, adding columns or indexes, writing migrations, choosing a database, or fixing data integrity problems.
metadata:
  role: system-architect
  version: "1.0"
---

# Designing data models

Data outlives code. Design for integrity first, then for the access patterns you actually have.

## Workflow

1. **List access patterns** before entities: every query/write with its frequency, latency target, and expected row counts. ("Get a customer's last 20 orders, 500/s, p99 < 20 ms.")
2. **Choose the store** by access pattern, not fashion:

| Store type | Fits | Examples |
|-----------|------|----------|
| Relational | Transactions, joins, constraints, ad-hoc queries — the default | PostgreSQL, MySQL |
| Document | Self-contained aggregates read/written as a unit, flexible shape | MongoDB, DynamoDB (single-table) |
| Key-value | Lookup by key at extreme scale, caching, sessions | Redis, DynamoDB |
| Wide-column | Massive write throughput, known query patterns | Cassandra, Bigtable |
| Time-series | Metrics, events by time, downsampling | TimescaleDB, InfluxDB |
| Search | Full-text, faceting, relevance | OpenSearch, Elasticsearch |
| Graph | Deep relationship traversal | Neo4j |
| Analytical (OLAP) | Aggregations over large history | BigQuery, Snowflake, ClickHouse |

3. **Model entities** (relational default):
   - Normalize to 3NF; denormalize only for a measured read pattern, and document how the copy stays in sync.
   - Every table has a primary key; prefer surrogate keys (UUIDv7 / bigint identity) plus unique constraints on natural keys.
   - Enforce integrity in the database: `NOT NULL`, `UNIQUE`, `CHECK`, foreign keys. Application validation is not enough.
   - Money: integer minor units or `NUMERIC`, never float. Time: `timestamptz` in UTC.
   - Add `created_at`, `updated_at`; consider soft-delete only if there is a real need (it complicates every query and unique constraint).
4. **Index for the access patterns** from step 1: composite index column order = equality columns, then range/sort columns. Verify with `EXPLAIN ANALYZE`. Every index slows writes — remove unused ones.
5. **Plan growth:** retention/archival, partitioning (by time or tenant) when tables reach hundreds of millions of rows, read replicas, and multi-tenancy model (shared table with `tenant_id` + row-level security, schema per tenant, or DB per tenant).
6. **Privacy:** classify PII columns, minimize collection, encrypt sensitive fields, support deletion/export (GDPR).

## Zero-downtime migrations (expand → migrate → contract)

1. **Expand:** add new column/table, nullable or with a default; deploy code that writes to both old and new.
2. **Migrate:** backfill in small batches (e.g. 1–10k rows per transaction) with throttling; verify counts/checksums.
3. **Switch reads** to the new structure.
4. **Contract:** stop writing the old one; drop it in a later release.

Dangerous operations to avoid on large live tables: adding `NOT NULL` without default on old engines, rewriting column types, non-concurrent index builds (use `CREATE INDEX CONCURRENTLY` in PostgreSQL), long-held locks. Set `lock_timeout` / `statement_timeout` in migrations. Every migration must be reversible or have a documented rollback.

## Review checklist

- [ ] Access patterns listed and each has a supporting index
- [ ] Constraints enforce invariants in the DB
- [ ] Types correct for money, time, IDs
- [ ] Migration is backward compatible with the currently deployed code
- [ ] Backfill is batched and resumable
- [ ] PII identified; retention defined
