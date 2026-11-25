---
name: database-query-optimization
description: "Optimise query patterns across engines: N+1 elimination, set-based rewrites, pagination that scales, join strategy, and measurement before and after."
type: procedural
category: databases
domain: databases
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - n+1 query problem
  - keyset pagination
  - slow join query
  - orm query optimization
  - offset pagination slow
aliases:
  - query-tuning
keywords:
  - query-optimization
  - n+1
  - pagination
  - joins
  - orm
  - set-based
mcp_servers:
  - postgres
  - github
source: custom
enabled: true
---

# Database Query Optimization

## Purpose

Optimise query patterns across engines: N+1 elimination, set-based rewrites, pagination that scales, join strategy, and measurement before and after.

## When to Use

- An endpoint issues hundreds of queries per request.
- Pagination degrades as the offset grows.
- An ORM generates a plan no human would write.

## When NOT to Use

- The plan is fine and the problem is network or serialisation.
- The data model itself is wrong; fix the schema first.
- The engine-specific tuning is the real issue.

## Capabilities

- Detect N+1 patterns in ORMs and replace them with eager or batched loading.
- Rewrite row-by-row logic as set-based SQL.
- Implement keyset pagination that stays flat at any depth.
- Choose join strategies with knowledge of cardinality.
- Prove the improvement with query counts and timings.

## Inputs

- The endpoint or job, and its query log or ORM debug output.
- Table sizes and index coverage for the joined columns.
- Acceptable latency and the pagination contract the clients depend on.

## Workflow

1. Count the queries for one request; the number, not the duration, is the first signal.
2. Replace per-row lookups with a join or a batched `IN` query.
3. For pagination, switch OFFSET to keyset on an indexed, unique ordering.
4. Check that every join and filter column is covered by an index.
5. Measure again with the same data volume and record query count and p95.
6. Add a regression test that asserts the query count for the hot endpoint.

## Tools

- psql
- sqlalchemy
- prisma
- django-orm
- pg_stat_statements

## Examples

- `OFFSET 100000 reads 100,000 rows to discard them; keyset pagination reads only the page.`
- `Lazy loading 200 orders with 3 items each becomes 3 queries instead of 201.`

## Safety

- Never disable prepared statements to make a query planner behave; fix the plan.
- Batch operations need size limits so a single request cannot exhaust memory.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `postgres` | stdio | standard | medium | `POSTGRES_URL` |
| `github` | http | standard | medium | `GITHUB_PERSONAL_ACCESS_TOKEN` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/databases/database-query-optimization`). First-party skill, maintained in this repository.

## Notes

- A query-count assertion in tests catches N+1 regressions earlier than a benchmark.
- Sorting must be deterministic or keyset pagination will skip rows.
- Pairs with: `postgresql-performance`, `nestjs-expert`.
