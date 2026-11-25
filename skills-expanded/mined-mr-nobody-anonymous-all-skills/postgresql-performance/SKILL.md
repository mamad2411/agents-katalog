---
name: postgresql-performance
description: "Tune PostgreSQL with evidence: `EXPLAIN (ANALYZE, BUFFERS)`, index strategy, VACUUM and bloat, connection pooling, and configuration that matches the workload."
type: procedural
category: databases
domain: databases
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - postgres slow query
  - explain analyze buffers
  - postgres index strategy
  - postgres vacuum bloat
  - postgres connection pooling
aliases:
  - postgres-perf
  - pg
keywords:
  - postgresql
  - explain
  - index
  - vacuum
  - bloat
  - pgbouncer
  - autovacuum
mcp_servers:
  - postgres
  - filesystem
source: custom
enabled: true
---

# PostgreSQL Performance

## Purpose

Tune PostgreSQL with evidence: `EXPLAIN (ANALYZE, BUFFERS)`, index strategy, VACUUM and bloat, connection pooling, and configuration that matches the workload.

## When to Use

- A query is slow and you need to know why, from the plan and the buffers.
- Tables or indexes are bloated and autovacuum is losing the race.
- Connection count or pooling is limiting throughput.

## When NOT to Use

- The bottleneck is the application's N+1 pattern; fix that first.
- The engine is not PostgreSQL.
- A schema change is needed for correctness, not speed.

## Capabilities

- Read actual plans and separate planning cost from I/O and row-estimate error.
- Design indexes that match predicates, join keys and sort order.
- Diagnose bloat, wraparound risk and autovacuum settings.
- Size a pool and pick a pooling strategy for the deployment.
- Tune the handful of settings that matter for the workload.

## Inputs

- The slow query, its parameters and the real data distribution.
- `pg_stat_statements` output ranked by total time.
- Server resources: RAM, cores, storage type, and the pool in front.

## Workflow

1. Rank queries by total time with `pg_stat_statements`, not by anecdotes.
2. Run `EXPLAIN (ANALYZE, BUFFERS)` on the worst offender and read the estimate vs actual rows.
3. Fix the biggest error source: stale statistics, missing index, or a bad join order.
4. Add the narrowest index that serves the predicate and ordering; verify it is used.
5. Check bloat and autovacuum behaviour on the affected tables.
6. Re-run the same workload and compare buffers read, not just wall time.

## Tools

- psql
- pg_stat_statements
- pgbadger
- pgbouncer
- explain.depesz

## Examples

- `A 400× row-estimate error usually means stale statistics, not a missing index — `ANALYZE` first.`
- ``BUFFERS` showing 2M shared hits with 0 reads means the query is CPU-bound, so indexes will not help.`

## Safety

- Never run `EXPLAIN ANALYZE` on a write statement in production without a transaction rollback.
- `VACUUM FULL` takes an exclusive lock; use `pg_repack` on live systems.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `postgres` | stdio | standard | medium | `POSTGRES_URL` |
| `filesystem` | stdio | core | low | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/databases/postgresql-performance`). First-party skill, maintained in this repository.

## Notes

- An index that is never used still costs writes; audit and drop.
- Pool size is bounded by cores, not by the number of app instances.
- Pairs with: `database-query-optimization`, `fastapi-expert`.
