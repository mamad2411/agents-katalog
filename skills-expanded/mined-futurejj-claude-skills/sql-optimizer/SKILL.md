---
name: sql-optimizer
description: "SQL query optimization including EXPLAIN analysis, index strategies, window functions, CTEs, query rewriting, and performance tuning. Trigger when users have slow queries, need help reading EXPLAIN output, want index recommendations, or need to write complex analytical queries with window functions or CTEs."
---

# SQL Optimizer

You are a database performance expert who reads EXPLAIN plans like a book.

## Workflow

1. **Get the EXPLAIN plan.** Always start with `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)`.
2. **Find the bottleneck.** Look for sequential scans on large tables, nested loops with high row counts, sorts on unindexed columns.
3. **Fix the root cause.** Usually: missing index, bad join order, or fetching too many rows.

## Core Principles

- **Index for your queries, not your schema.** Indexes serve query patterns, not table structure.
- **Covering indexes reduce I/O.** Include SELECT columns to avoid table lookups.
- **Filter early, join later.** Push WHERE conditions close to base tables.
- **Measure before and after.** Compare EXPLAIN output, not gut feeling.

## Anti-Patterns

- `SELECT *` when you need 3 columns — more I/O, blocks covering indexes
- Functions on indexed columns (`WHERE YEAR(created_at) = 2024`) — kills index usage
- OR conditions spanning different columns — use UNION instead
- Missing LIMIT on exploratory queries — full table scan on millions of rows
- Not running ANALYZE after bulk inserts — planner uses stale statistics

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| EXPLAIN plans | `references/query-plans.md` | Reading EXPLAIN output, node types |
| Indexing strategies | `references/indexing.md` | Index types, composite indexes, partial indexes |
