---
name: follow-lib-drizzle-optimize queries
description: optimize Drizzle queries — indexes, relations, select/where performance
argument-hint: "[table-or-query]"
related:
  - follow-lib-drizzle
  - run-bench
  - scan-codebase
  - report-before-after
---

## Goal

Improve the performance of Drizzle queries — indexes, relations, select/where patterns — measuring before and after, without changing output

## Scope

- Use when queries are slow, N+1, missing indexes, or selects exceed what's needed
- Covers: index design, relational query tuning, select/where optimization, batching
- Always measure a baseline first — optimizing without numbers is guessing

## Execute

### 1. Baseline And Profile

> Goal: identify the real bottleneck with numbers, not guesses

1. Do `/run-bench` or time the slow query — record the baseline (latency, row count, query count)
2. Use `EXPLAIN ANALYZE` on the generated SQL (get the real SQL with `.toSQL()`)
3. Do `/scan-codebase` to find call sites running the query in a loop (N+1 candidates)
4. Do `/deep-optimize` if a wider-scope analysis is needed

### 2. Add Indexes

> Goal: indexes covering the real query patterns

1. Add `index()`/`uniqueIndex()` in the schema on columns frequently used in filter (`where`), join, order by
2. Composite index: order columns by selectivity and query pattern (equality before range)
3. Partial index (`index().where(...)`) when the query filters on repeated constant values
4. Generate the migration via `workflows/migrate-schema/SKILL.md` — a new index must always go through a migration

### 3. Optimize Select And Where

> Goal: select only what's used, where clauses an index can serve

1. Specify columns explicitly in `db.select({...})` instead of `select()` on the whole table — fewer bytes + enables covering index
2. Write SARGable `where` — avoid wrapping columns in functions (`lower(col)` etc.) unless there's an expression index
3. Use `inArray`/`between`/`and`/`or` from `drizzle-orm` to match the existing indexes
4. Use `limit`+`offset` or keyset pagination — big offsets = wasted scans

### 4. Fix Relations And N+1

> Goal: cut N+1 with relational queries or suitable joins

1. Use `db.query.<table>.findMany({ with: {...} })` instead of looping per-row queries
2. Beware deeply nested `with` — each level is a separate query; if large, split into a single join query
3. Use `columns: {...}` in the relational query to limit fields of parent and child
4. Batch reads with `inArray` when fetching many ids — see [../../references/api/queries.md](../../references/api/queries.md)

### 5. Measure Again

> Goal: compare against the baseline and decide

1. Re-measure the same point with the same workload — report before/after numbers with `/report-before-after`
2. Re-run `EXPLAIN ANALYZE` — confirm the index is used (Index Scan instead of Seq Scan)
3. If no improvement or a regression → revert that point then report; passing → `/suggest-next-action`

## Rules

- Baseline always first — never optimize without comparison numbers
- Fix one point at a time ordered by impact high → low (index/query shape before micro-tuning)
- Preserve behavior — optimizing must never change query output
- Every index has a write cost — don't add an index no query uses
- If unsure about index syntax → check the official docs

## Expected Outcome

- Slow queries identified with a baseline and `EXPLAIN ANALYZE`
- Indexes covering the real query patterns, via migration
- N+1 fixed with relational query/batching
- Post-fix numbers better than the baseline — report with evidence
