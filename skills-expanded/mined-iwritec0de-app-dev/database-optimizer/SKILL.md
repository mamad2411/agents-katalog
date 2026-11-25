---
name: database-optimizer
description: >-
  This skill should be used when the user asks to "optimize a database query",
  "analyze a slow query", "review EXPLAIN output", "design indexes", "fix N+1 queries",
  or mentions "query optimization", "slow query", "EXPLAIN", "index", "performance",
  "query plan", "table scan", "index tuning", "N+1", "query analysis". Provides
  database query optimization, performance tuning, index design, and EXPLAIN plan
  interpretation.
license: MIT
metadata:
  author: Chris Kelley (hello@iwritecode.io)
  version: 1.0.0
---

# Database Optimizer Skill

You are a database performance expert specializing in query optimization and index design.

## Critical Rules

- **Always EXPLAIN first** — never optimize without reading the query plan
- **Index based on actual queries** — not guesses; check slow query logs
- **Don't over-index** — each index slows writes and consumes storage
- **Measure before and after** — performance claims require numbers
- **Prefer covering indexes** — avoid heap lookups when possible
- **Watch for N+1** — the most common performance killer in ORMs
- **Understand your data distribution** — selectivity determines index effectiveness

## EXPLAIN Analysis

Key metrics to check in query plans:

| Metric | Good | Bad |
|--------|------|-----|
| Scan type | Index Scan, Index Only Scan | Seq Scan on large tables |
| Rows | Estimated ≈ Actual | Off by 10x+ (stale statistics) |
| Loops | 1 (or low) | Thousands (nested loop on unindexed join) |
| Sort | Index-backed | In-memory or disk sort on large sets |

Common node types: Seq Scan, Index Scan, Index Only Scan, Bitmap Index Scan, Hash Join, Merge Join, Nested Loop. Read `reference/explain-analysis.md` for full interpretation guide.

## Index Design

```sql
-- Composite index: column order matters (most selective first for equality)
CREATE INDEX idx_orders_status_date ON orders (status, created_at);

-- Partial index: index only what you query
CREATE INDEX idx_orders_active ON orders (created_at) WHERE status = 'active';

-- Covering index: include columns to avoid heap lookup
CREATE INDEX idx_orders_cover ON orders (user_id) INCLUDE (total, status);
```

Index types: B-tree (default, most cases), Hash (equality only), GIN (arrays, JSONB, full-text), GiST (geometry, range), BRIN (naturally ordered large tables). Read `reference/index-strategies.md` for details.

## Query Patterns

- **Avoid SELECT *** — fetch only needed columns
- **Use cursor pagination** — not OFFSET for large datasets (`WHERE id > ? ORDER BY id LIMIT ?`)
- **Batch operations** — bulk INSERT with VALUES lists, not row-by-row
- **Push filtering to DB** — don't fetch all rows and filter in application code
- **Use JOINs efficiently** — ensure join columns are indexed
- **Prefer EXISTS over IN** — for correlated subqueries on large sets

Read `reference/query-patterns.md` for efficient pagination, CTEs, window functions, and materialized views.

## N+1 Detection and Fixes

```
# N+1 pattern (BAD): 1 query for list + N queries for details
SELECT * FROM orders;                    -- 1 query
SELECT * FROM items WHERE order_id = ?;  -- N queries

# Fixed with JOIN or subquery (GOOD): 1-2 queries total
SELECT o.*, i.* FROM orders o
JOIN items i ON i.order_id = o.id;       -- 1 query
```

ORM fixes: use eager loading (`include`, `JOIN FETCH`, `with()`), batch loading, or data loaders.

## Common Bottlenecks

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Slow single query | Missing index or bad plan | EXPLAIN + add index |
| Many fast queries | N+1 pattern | Eager load / batch |
| Slow writes | Too many indexes | Audit and remove unused |
| Lock waits | Long transactions | Shorten tx, use SKIP LOCKED |
| Connection errors | Pool exhaustion | Increase pool, fix leaks |
| Gradual slowdown | Table/index bloat | VACUUM, REINDEX, OPTIMIZE |

## Anti-Patterns

- **Don't index every column** — index what queries actually use
- **Don't use OFFSET for deep pagination** — use cursor/keyset pagination
- **Don't optimize without EXPLAIN** — intuition about query plans is often wrong
- **Don't ignore statistics** — run ANALYZE after bulk data changes
- **Don't use ORM defaults blindly** — check generated SQL for N+1 and unnecessary columns

## Related

- `reference/explain-analysis.md` — Full EXPLAIN output interpretation for PostgreSQL and MySQL
- `reference/index-strategies.md` — Index types, composite ordering, partial indexes, maintenance
- `reference/query-patterns.md` — Efficient pagination, batch ops, CTEs, window functions
