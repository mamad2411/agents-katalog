---
name: sql-query-development
description: Write correct and efficient SQL. Use when authoring queries, views,
  or stored procedures.
metadata:
  tags: sql, query, development
---

# SQL Query Development

## Use this skill when
- Writing SELECT/JOIN/AGG queries
- Using window functions and CTEs
- Reviewing correctness of business queries

## Do not use this skill when
- Optimizing existing slow queries (use query-optimization)
- Schema work (use its own skill)

## Instructions
1. Prefer explicit JOINs to implicit; qualify all columns.
2. Use CTEs for readability; watch for repeated materialization.
3. Handle NULLs deliberately (IS NULL, COALESCE, DISTINCT).
4. Aggregate correctly before joining to avoid fanout.
5. Use window functions for rankings/running totals.
6. Keep transactions and locking in mind for UPDATE/DELETE.
7. Limit early and shape results to the task.
8. Test on realistic data volumes.

## Output Format
- Query | intent | edge-case handling | volume testing notes

## Common Mistakes
- Lossy group-by returns arbitrary rows
- Cardinality explosions from bad joins
- NULL semantics surprises
