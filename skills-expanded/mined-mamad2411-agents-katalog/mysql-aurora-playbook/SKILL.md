---
name: mysql-aurora-playbook
description: >
  Use when writing or reviewing MySQL 8.0 or Aurora MySQL 3 SQL, indexes,
  UUID storage, cursor pagination, EXPLAIN, HLL, deadlocks, MDL, gh-ost, pt-osc,
  RDS Proxy, JDBC Wrapper, slow query logs, schema migrations, connection pools,
  or Aurora failover.
---

# MySQL 8.0 & Aurora MySQL 3 Playbook

Use this as a router. Load only the reference file or files needed for the current database task.

Aurora MySQL 3.x is MySQL 8.0-compatible, but exact feature behavior depends on the Aurora minor version. Check `select aurora_version();` or `select @@aurora_version;` before relying on version-gated features.

## When to Use

- Writing or reviewing SQL queries (SELECT, INSERT, UPDATE, DELETE)
- Designing tables, indexes, or choosing data types
- Diagnosing slow queries, deadlocks, or HLL growth
- Planning DDL / schema migrations (instant DDL, gh-ost, pt-osc)
- Configuring Aurora endpoints, serverless v2, connection pools
- Setting up monitoring, alerts, or slow query logging

**Not for:** PostgreSQL, MariaDB-specific features, DynamoDB, or pure application-layer ORM patterns.

For Caruso Ent schema or migration implementation, use `caruso-ent-orm-mysql` first. Use this skill for SQL, MySQL, Aurora, index, migration safety, and operational tradeoffs below the ORM layer.

## DDL Safety Rule

Before any production DDL:

```sql
SET SESSION lock_wait_timeout = 10;
```

Then check blockers, choose the lowest-impact algorithm, and prove the migration path. DDL can queue behind metadata locks and then block all later reads/writes on the same table.

## Quick Reference

| Task | Default Pattern | Load |
|------|-----------------|------|
| Indexes, leftmost prefix, covering index, JSON index, cardinality | Prefer workload-shaped composite indexes; verify with EXPLAIN | `references/indexes.md` |
| Types, UUID, DATETIME, charset, utf8mb4 index length | Size to domain and index byte limits | `references/data-types.md` |
| Aurora endpoints, Serverless v2, I/O-Optimized, Backtrack, Blue/Green, failover | Version-gate Aurora-specific behavior | `references/aurora-features.md` |
| EXPLAIN, slow query, optimizer hints, hash join, histogram, upsert | Inspect actual plan before forcing hints | `references/query-optimization.md` |
| Cursor pagination, deep OFFSET, row constructors | Cursor with unique tiebreaker | `references/pagination.md` |
| SELECT *, coercion, long transaction, HLL, deadlock detect | Fix query shape and transaction scope first | `references/anti-patterns.md` |
| DDL, MDL, instant DDL, gh-ost, pt-osc, OPTIMIZE TABLE | Set lock wait timeout, check blockers, choose algorithm | `references/ddl-migration.md` |
| Bulk insert, chunked update/delete, sparse IDs | PK-window or keyset batches with throttling | `references/batch-ops.md` |
| Pooling, RDS Proxy, JDBC Wrapper, failover reconnect | Budget total connections across app instances | `references/connection-mgmt.md` |
| CloudWatch, Performance Insights, slow log, pt-query-digest, lock waits | Use live metrics plus slow-query evidence | `references/monitoring.md` |
| Skill validation scenarios | Check whether agents avoid known traps | `references/pressure-tests.md` |
