---
name: sql-query-performance
category: database
description: Use when writing or changing a query against PostgreSQL from Go — avoiding N+1 loops, reading EXPLAIN output, indexing, and keyset pagination
tech_stack: PostgreSQL
source: samber/cc-skills-golang golang-database (MIT), wshobson/agents sql-optimization-patterns (MIT), adapted
---
# SQL Query Performance (Go)

## Overview

Go has no ORM to blame for an N+1 — it's a loop you wrote yourself, calling the repository once per item instead of once for the batch. This skill is the Go-side half of query performance; java-persistence covers the JPA/Hibernate side.

**Core principle:** one round trip per request-shaped operation, not one per row.

## N+1 in Go

```go
// ❌ one query per item: N+1
for _, id := range ids {
    task, err := repo.Get(ctx, id)   // round trip per id
    ...
}

// ✅ one query for the batch
tasks, err := repo.GetMany(ctx, ids)   // SELECT ... WHERE id = ANY($1)
```

```sql
SELECT id, title, status FROM tasks WHERE id = ANY($1);
```
Bind `ids` as a `[]uuid.UUID` (pgx encodes a Go slice as a Postgres array directly — no manual `IN (...)` string building). For a write-side batch, use `pgx.Batch` to pipeline multiple statements over one round trip instead of looping with individual `Exec` calls.

## Database hygiene

- Every call takes a `context.Context` — `QueryContext`/`ExecContext` (`database/sql`) or pgx's `ctx` parameter — so a slow query is cancelable and traceable.
- `defer rows.Close()` immediately after a successful `Query`, and check `rows.Err()` after the loop — a `Query` that returns rows can still fail mid-stream, and an unclosed `Rows` leaks the connection.
- Use `Exec`, not `Query`, for statements that return no rows (`INSERT`/`UPDATE`/`DELETE` without `RETURNING`) — `Query` leaves a result set open that must still be drained.
- No `SELECT *` in application code — name the columns, so an added column doesn't silently change scan order or payload size.

## Reading EXPLAIN

```
psql "$DATABASE_URL" -c "EXPLAIN (ANALYZE, BUFFERS) <query with literal values, not placeholders>"
```
Run it against realistically seeded data, not an empty table — an empty-table plan hides the index Postgres would actually need. Read for:
- `Seq Scan` on a table bigger than a few thousand rows → missing index.
- Estimated vs actual row counts far apart → stale statistics (`ANALYZE <table>`) or a predicate the planner can't estimate well.
- A `Sort` that spills to disk (`Sort Method: external merge`) → needs `work_mem` tuning or an index that avoids the sort.

## Indexes

- Postgres does **not** auto-index foreign-key columns — add one explicitly for every FK you join or filter on.
- Composite index column order follows the leftmost-prefix rule: an index on `(a, b)` serves queries filtering on `a` alone or `a AND b`, not `b` alone.
- A partial index (`WHERE status = 'open'`) for a hot subset of a much larger table.
- A covering index (`INCLUDE (col)`) to let an index-only scan satisfy a query without a heap fetch.

See postgres-migrations for how to add an index on a live table without locking it.

## Query-count regression test

Wrap the pool/connection to count statements in a test, or use `pg_stat_statements` where the test DB has it enabled, and assert the count stays constant as the dataset grows — this is what catches an N+1 before it ships, the same way java-persistence's Hibernate-statistics assertion does on the Java side.

## Keyset pagination

See api-design-conventions for the full pagination guidance; the query shape is:
```sql
SELECT ... FROM tasks
WHERE (created_at, id) < ($1, $2)
ORDER BY created_at DESC, id DESC
LIMIT $3 + 1;   -- fetch one extra row to know has_more
```

## Common Mistakes

- A loop calling the repository once per id instead of a batched `= ANY($1)` query.
- `rows.Close()` missing or only deferred conditionally (e.g. after an early `if err != nil { return }` that skips the defer).
- `rows.Err()` never checked after the loop.
- Adding a filter/join column with no matching index.
- Reading `EXPLAIN` against an empty or tiny local table and concluding the query is fine.

## Red Flags

- Query count in a test or log scales linearly with row count.
- `Seq Scan` on a table expected to hold more than a few thousand rows.
- A new `WHERE`/`JOIN` column with no migration adding its index.
