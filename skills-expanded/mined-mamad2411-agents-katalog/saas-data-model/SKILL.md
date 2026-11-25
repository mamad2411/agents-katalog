---
name: saas-data-model
description: Schema design and data access specialist for SaaS workloads. Auto-invoked when schemas are being created or changed, migrations are written, indexes are added/removed, ORMs are being configured, or slow queries need investigation.
---

# SaaS Data Model

Schema decisions are the ones a SaaS lives with longest. The goal is a model
that still works at the largest tenant's scale — and migrations that never take
the product down to get there.

## When to reach for this

- Designing tables, keys, and constraints for a new feature
- Writing or reviewing a migration, especially on a large/hot table
- Adding or dropping indexes, or investigating a slow query / plan regression
- Configuring ORM loading patterns or hunting N+1s

## Principles

1. **Model for the query path.** Design around the reads that will dominate
   production, not abstract normalization purity.
2. **Tenant identifier everywhere.** In pooled multi-tenant schemas the tenant ID
   belongs in every row and usually leads every composite index — it is also what
   RLS policies key on.
3. **Assume the largest tenant.** Index and partition for the 99th-percentile
   tenant, not the median; the median query will be fine either way.
4. **Online-safe migrations by default.** No DDL that takes a long strong lock on
   a large table. `CREATE INDEX CONCURRENTLY`, batched backfills, `NOT VALID`
   constraints validated separately.
5. **Measure before and after.** Every index decision ships with an
   `EXPLAIN (ANALYZE, BUFFERS)` before and after. No "this should help" without a plan diff.
6. **Resist premature denormalization.** Materialized views and caches only after
   a measured read problem exists — they all add a consistency liability.
7. **Every migration has a rollback.** State how to reverse it before applying it;
   "roll forward" is a decision, not a default.

## Online-migration playbook (Postgres)

The sequence for adding a required column to a large, hot table:

- [ ] `SET lock_timeout = '2s';` before any DDL — fail fast and retry rather than
      queueing behind it and blocking all traffic
- [ ] `ALTER TABLE t ADD COLUMN c type;` nullable — metadata-only. (Postgres 11+
      also makes `ADD COLUMN ... DEFAULT <constant>` non-rewriting.)
- [ ] Backfill in batches (1k–10k rows per statement, keyed by PK range, brief
      pause between batches); never one giant `UPDATE`
- [ ] `ALTER TABLE t ADD CONSTRAINT c_not_null CHECK (c IS NOT NULL) NOT VALID;`
      then `VALIDATE CONSTRAINT` (takes only a weak lock)
- [ ] `ALTER TABLE t ALTER COLUMN c SET NOT NULL;` — Postgres 12+ skips the full
      scan when a validated check constraint already proves it; drop the check after
- [ ] Indexes: `CREATE INDEX CONCURRENTLY` only (cannot run inside a transaction;
      on failure it leaves an `INVALID` index — drop and retry)
- [ ] Column drops and renames: deploy code that stops reading the old name first,
      migrate after — never in the same release

For ORM work: default to lazy loading plus explicit batch/eager declarations per
query path, and run an N+1 detector (query-count assertions in tests) on list endpoints.

## Pitfalls

- Composite indexes that don't lead with `tenant_id` in pooled schemas — every
  tenant-scoped query scans across tenants
- `ALTER TABLE ... SET NOT NULL` / `ADD COLUMN` with volatile default executed
  directly on a big table — full rewrite under an exclusive lock
- Backfills as a single transaction: bloat, replication lag, lock pileups
- Index added for one slow query without checking write amplification on a
  hot-insert table
- `EXPLAIN` run only on dev-sized data — plans flip with row counts; test against
  production-scale (or the largest tenant's) statistics
- Soft-delete flags without partial indexes (`WHERE deleted_at IS NULL`), so every
  index carries dead rows forever

---
*Related: `saas-multitenancy` (RLS on these tables), `saas-billing` (metering
schema) · domain agent: `saas-architect` (pooled/bridge/silo tenancy choice) ·
output/ADR format: `playbook-conventions`*
