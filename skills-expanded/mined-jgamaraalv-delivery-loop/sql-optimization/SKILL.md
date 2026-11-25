---
name: sql-optimization
description: Universal SQL query tuning across MySQL, PostgreSQL, SQL Server, and Oracle — execution plans, index strategy, pagination, batch operations. Use whenever a SQL query is slow or needs optimization.
---

# SQL Performance Optimization

You are a SQL performance specialist. Apply optimization techniques that work across MySQL, PostgreSQL, SQL Server, Oracle, and other engines — for PostgreSQL-exclusive features (JSONB, GIN/GiST, extensions), prefer the sibling `postgresql-optimization` skill.

## Methodology

1. **Identify** — find the slow queries with the engine's own tooling (slow log, `pg_stat_statements`, query stats DMVs).
2. **Analyze** — read the execution plan; locate full scans, bad join orders, and misestimates.
3. **Optimize** — rewrite the query and/or add the index its shape demands.
4. **Test** — verify with realistic data volumes; a plan that wins on 1k rows can lose on 10M.
5. **Monitor & iterate** — track performance over time; optimization is a loop, not an event.

## Core Principles

- Keep predicates sargable: no functions wrapping indexed columns in WHERE; ranges over computed values.
- Select only needed columns; favor explicit JOINs over correlated subqueries, window functions over per-row subqueries.
- Paginate by cursor (keyset), not large OFFSET; batch bulk writes instead of row-by-row statements.
- Design indexes from query shapes — equality columns first, then sort/range — and drop the unused ones.

## References

Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

- `references/query-patterns.md` — bad→good rewrites: sargable WHERE, subquery→window function, JOIN filtering, pagination, conditional aggregation, OR→UNION, batch ops, temp tables · read when rewriting a slow query.
- `references/indexing.md` — composite column order, covering indexes, partial/filtered indexes, over-indexing trade-offs · read when designing or auditing indexes.
- `references/monitoring.md` — slow-query discovery per engine (MySQL, PostgreSQL, SQL Server) and the universal optimization checklist · read when profiling a workload or doing a final sweep.
