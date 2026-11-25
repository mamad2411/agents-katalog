---
name: node-pg-8-performance-diagnostics
description: Investigates Node pg 8.x SQL performance, query plans, pool pressure, lock waits, streaming bottlenecks, and slow database behavior.
license: MIT
compatibility: Node applications using Node pg 8.x with PostgreSQL.
---

# Node pg 8 Performance Diagnostics

This skill guides practical performance investigation for handwritten SQL through Node `pg` 8.x.

## When to Use

Use this skill when the task involves:

- slow SQL
- high query latency
- pool checkout timeouts
- increasing `pool.waitingCount`
- lock waits or long-running transactions
- missing indexes
- expensive joins or scans
- slow streams or exports
- reviewing `EXPLAIN` or `EXPLAIN (ANALYZE, BUFFERS)` output

## Diagnostic Principles

- Separate application pool pressure from database query slowness.
- Do not increase pool size before checking query latency, indexes, client leaks, and total instance count.
- Use `EXPLAIN` first; use `EXPLAIN ANALYZE` only when it is safe to execute the query.
- Never run `EXPLAIN ANALYZE` on data-changing statements unless inside a deliberate rollback-only test transaction and approved.
- Check predicates, join order, row estimates, index usage, sort/hash memory pressure, and lock waits.
- Keep transactions short and avoid external I/O inside transaction windows.
- For streams, inspect backpressure and downstream output before blaming PostgreSQL.

## Workflows

Use `workflows/query-performance-investigation-workflow.md` for slow query, streaming, or pool pressure investigations.

## Resources

Use `resources/performance-diagnostics-checklist.md` during investigation.

## Examples

Use `examples/explain-review-example.md` for an example plan review template.
