---
name: sql-optimization
description: Diagnoses and fixes slow SQL using real query plans, index design, sargable rewrites, keyset pagination and ORM fixes such as N+1 queries. Use when a query, endpoint, report or job is slow, database CPU or IO is high, an EXPLAIN plan needs reading, an index needs designing, or an ORM issues too many queries. Covers PostgreSQL and MySQL.
license: MIT
---

# SQL Optimization

Measure, don't guess. Find the query that actually costs the most, read its real plan with real parameters, change one thing, and measure again on realistic data. An index added on a hunch is a permanent write cost that may not help.

## When to use

- A page, API endpoint, report or background job is slow and the time is in the database.
- High database CPU, IO, or lock waits.
- Reading or explaining an `EXPLAIN` plan.
- Designing indexes for a new query or table.
- An ORM generates many small queries (N+1) or huge ones.

Not for: changing schemas safely on a live database (use database-migrations; it covers building indexes without blocking writes).

## Workflow

1. **Find the expensive queries.** Rank by total time (calls × mean), not just the slowest single run.
   - PostgreSQL: `pg_stat_statements` (needs `shared_preload_libraries = 'pg_stat_statements'` and `CREATE EXTENSION pg_stat_statements;`).
   - MySQL 8: `performance_schema.events_statements_summary_by_digest`, or the slow query log summarised with `pt-query-digest`.
   - APM traces and ORM query logs show which code path issues each query.
2. **Get the exact SQL and real parameter values** from logs or traces. A plan for `WHERE status = 'active'` can differ completely from one for `WHERE status = 'archived'`.
3. **Get the real plan.**
   - PostgreSQL: `EXPLAIN (ANALYZE, BUFFERS) <query>;`
   - MySQL 8.0.18+: `EXPLAIN ANALYZE <query>;` (older: `EXPLAIN FORMAT=TREE` or plain `EXPLAIN`, estimates only)
   - **`EXPLAIN ANALYZE` executes the statement.** For `INSERT`/`UPDATE`/`DELETE`, wrap it in `BEGIN; ... ROLLBACK;`. Prefer a replica or a production-sized copy. **Ask the user before running it against production.**
4. **Read the plan.** Find where the time goes, and compare estimated vs actual rows. Read [references/reading-query-plans.md](references/reading-query-plans.md) for node types and red flags.
5. **Pick the fix** from the diagnosis table below.
6. **Apply one change and re-measure** with the same parameters and similar cache state (run each version a few times). Keep the before/after plans and timings.
7. **Count the cost.** For a new index: check for existing overlapping indexes and weigh the extra write and storage cost. For a rewrite: confirm the results are identical.
8. **Ship it safely.** Build indexes without blocking writes (`CREATE INDEX CONCURRENTLY` or MySQL online DDL), and add a regression test where possible (a query-count assertion, or a plan check in CI for critical queries).

### Top queries

```sql
-- PostgreSQL 13+ (older versions: total_time / mean_time)
SELECT queryid, calls,
       round(total_exec_time::numeric)    AS total_ms,
       round(mean_exec_time::numeric, 2)  AS mean_ms,
       rows,
       left(query, 120)                   AS query
FROM   pg_stat_statements
ORDER  BY total_exec_time DESC
LIMIT  20;
```

```sql
-- MySQL 8 (timer columns are in picoseconds)
SELECT DIGEST_TEXT,
       COUNT_STAR                          AS calls,
       ROUND(SUM_TIMER_WAIT / 1e12, 1)     AS total_s,
       ROUND(AVG_TIMER_WAIT / 1e9, 2)      AS avg_ms,
       SUM_ROWS_EXAMINED, SUM_ROWS_SENT
FROM   performance_schema.events_statements_summary_by_digest
ORDER  BY SUM_TIMER_WAIT DESC
LIMIT  20;
```

Turning on the slow query log or changing `long_query_time` changes server configuration. Ask before doing it on a shared server.

## Diagnosis → fix

| Symptom in the plan | Likely cause | Fix |
|---|---|---|
| Seq Scan / `type: ALL` on a large table, few rows returned | No usable index | Add an index matching the predicate (rules below) |
| Index exists but is not used | Non-sargable predicate, type mismatch, low selectivity, stale stats | Rewrite the predicate; fix types; `ANALYZE`; check the estimates |
| Estimated rows far off actual (10× or more) | Stale or insufficient statistics, correlated columns | `ANALYZE`; raise the statistics target; extended statistics |
| Large `Rows Removed by Filter` | Index covers only part of the predicate | Composite or partial index |
| Sort spilling to disk / `Using filesort` on a big set | No index providing the order | Index on (filter columns, sort columns) |
| Nested Loop with a large outer side and loops in the thousands | Bad estimate or missing index on the inner side | Fix stats; index the join key |
| Fast in the plan, slow in the app | N+1, network round trips, over-fetching, lock waits | Count queries per request; check locks |
| Slow deep pages | `OFFSET` scanning and discarding rows | Keyset pagination |

## Index design rules

- **Equality columns first, then range or sort columns.** For `WHERE tenant_id = ? AND created_at > ? ORDER BY created_at`, use `(tenant_id, created_at)`.
- **Leftmost prefix:** an index on `(a, b, c)` serves `a`, `a, b` and `a, b, c`. It does not serve `b` alone.
- **Match WHERE + ORDER BY + LIMIT** so the database reads the first N rows in order and stops: `WHERE user_id = ? ORDER BY created_at DESC LIMIT 20` → `(user_id, created_at)`.
- **Covering indexes** avoid table lookups: PostgreSQL 11+ `CREATE INDEX ... (customer_id) INCLUDE (status, total);`. Index-only scans in PostgreSQL also depend on the visibility map (a well-vacuumed table). InnoDB secondary indexes already contain the primary key.
- **Partial indexes** (PostgreSQL only) for hot subsets: `CREATE INDEX ... ON jobs (run_at) WHERE status = 'pending';`. The query's predicate must imply the index's `WHERE`.
- **Expression indexes** for computed predicates: PostgreSQL `CREATE INDEX ... ON users (lower(email));`; MySQL 8.0.13+ functional key parts `INDEX ((LOWER(email)))`.
- **Low-cardinality columns** (booleans, small status sets) rarely help as a leading column on their own. Combine them, or use a partial index.
- **Foreign key columns** used in joins or cascaded deletes usually need an index. PostgreSQL does not create one automatically.

### Every index has a cost

- Each index slows `INSERT`, `UPDATE` and `DELETE` and uses memory and disk. In PostgreSQL, indexing a frequently updated column also prevents HOT updates.
- Remove redundant indexes: `(a)` is redundant when `(a, b)` exists, unless it is needed for a unique constraint.
- Find unused indexes before adding more: PostgreSQL `SELECT * FROM pg_stat_user_indexes WHERE idx_scan = 0;` (counts since the last stats reset; check replicas too, since they have their own counters). MySQL `SELECT * FROM sys.schema_unused_indexes;`.
- Dropping an index is a schema change. Confirm with the user and follow database-migrations.

## Sargable predicates

Write predicates the index can use directly:

| Instead of | Write |
|---|---|
| `WHERE date(created_at) = '2026-01-15'` | `WHERE created_at >= '2026-01-15' AND created_at < '2026-01-16'` |
| `WHERE lower(email) = ?` (no expression index) | Add an expression index, or store a normalised column (PostgreSQL: `citext`) |
| `WHERE name LIKE '%smith'` | Full-text search, or PostgreSQL `pg_trgm` with a GIN/GiST index |
| `WHERE varchar_col = 123` (MySQL implicit cast) | Compare with the same type: `WHERE varchar_col = '123'` |
| Joining columns of different types or collations | Make the types and collations match |
| `WHERE a = ? OR b = ?` | `UNION ALL` of two indexed queries (PostgreSQL can also combine indexes with BitmapOr) |
| `WHERE id NOT IN (SELECT ...)` with NULLs possible | `WHERE NOT EXISTS (SELECT 1 ...)`, which is correct with NULLs and usually faster |
| `SELECT *` on a hot path | Only the columns you need, which may let a covering index serve it |

## ORM N+1 queries

The pattern: one query for a list, then one query per row for a relation. Each is fast; together they are slow.

**Detect:** log queries per request and look for the same statement repeated with different ids. Tools include Bullet (Rails), django-debug-toolbar and `assertNumQueries` (Django), Hibernate statistics, EF Core logging, and Laravel's `preventLazyLoading`.

**Fix by eager loading or batching:**

| ORM | Fix |
|---|---|
| Django | `select_related()` for FK/one-to-one (JOIN); `prefetch_related()` for many-valued relations |
| Rails | `includes`, `preload` or `eager_load` |
| SQLAlchemy | `selectinload()` (usually best for collections) or `joinedload()` |
| Hibernate / JPA | `JOIN FETCH`, `@EntityGraph`, or batch fetching (`@BatchSize`) |
| EF Core | `.Include()` / `.ThenInclude()`; consider `.AsSplitQuery()` for multiple collections |
| Prisma | `include` / `select` with relations |
| GORM | `Preload()` |
| GraphQL resolvers | A DataLoader that batches ids into one `WHERE id IN (...)` |

Lock it in with a test that asserts the query count for the endpoint.

## Pagination

`OFFSET 100000` still reads and throws away 100,000 rows. Use keyset (seek) pagination for deep or infinite lists:

```sql
-- First page
SELECT id, created_at, title FROM events
ORDER  BY created_at DESC, id DESC
LIMIT  50;

-- Next page: pass the last row's (created_at, id) from the previous page
SELECT id, created_at, title FROM events
WHERE  (created_at, id) < (:last_created_at, :last_id)
ORDER  BY created_at DESC, id DESC
LIMIT  50;
```

- Index `(created_at, id)`; B-tree indexes can be scanned backwards.
- Include a unique tiebreaker (`id`) so rows with equal timestamps are not skipped or repeated.
- On MySQL, check with `EXPLAIN` that the row-value comparison uses a range scan on the index. If it does not, use the expanded form: `WHERE created_at < :c OR (created_at = :c AND id < :id)`.
- Keyset pagination cannot jump to page N. If the product needs page numbers, cap the maximum offset.

## Statistics

- PostgreSQL: `ANALYZE table_name;` after bulk loads or large deletes (autovacuum does it eventually). For skewed columns: `ALTER TABLE t ALTER COLUMN c SET STATISTICS 1000;` then `ANALYZE`. For correlated columns (`city`, `zip`): `CREATE STATISTICS ... (dependencies) ON city, zip FROM t;` then `ANALYZE`.
- MySQL: `ANALYZE TABLE t;`. MySQL 8.0 histograms for non-indexed columns: `ANALYZE TABLE t UPDATE HISTOGRAM ON c WITH 64 BUCKETS;`.

## Locks and long transactions

A query can be slow because it waits, not because it works.

- PostgreSQL: query `pg_stat_activity` with `pg_blocking_pids(pid)` and look at `wait_event_type = 'Lock'`. Look for `idle in transaction` sessions.
- MySQL: `SELECT * FROM sys.innodb_lock_waits;` and `information_schema.innodb_trx`.
- Fix at the source: shorter transactions, no network calls or user think-time inside a transaction, consistent lock ordering, batched bulk updates.
- Killing or cancelling another session affects real users. Ask first.

## Prepared statements and plan caching

A query that is fast in a SQL console but slow from the app may be getting a different plan:

- PostgreSQL may switch a prepared statement to a generic plan after several executions. Compare with `EXPLAIN (ANALYZE) EXECUTE stmt(...)` and look at `plan_cache_mode`.
- Drivers may send parameters as a different type than the column (for example text vs integer, or `varchar` vs `nvarchar` on SQL Server), which blocks index use.

## Anti-patterns

- **Adding indexes without a plan** — measure first; most "missing index" guesses are wrong.
- **Testing on a tiny dev database** — the planner picks different plans for 1,000 rows than for 100 million.
- **Caching to hide a slow query** you have not understood. It comes back on a cache miss or a cold start.
- **Optimizer hints as the first fix** — they freeze a plan that goes stale as the data changes. Fix statistics and indexes first.
- **Indexing every column separately** instead of designing composite indexes for the actual queries.
- **Running `EXPLAIN ANALYZE` on a production `DELETE`** without a transaction you roll back.

## Done when

- The target query was measured before and after with the same parameters on realistic data, and the improvement is recorded.
- The new plan uses the intended access path, and estimated and actual rows are close.
- Any new index is justified, overlapping indexes were checked, and it is built without blocking writes.
- Results are unchanged (same rows, same order where order matters).
- N+1 fixes have a query-count test.

## References

- [references/reading-query-plans.md](references/reading-query-plans.md) — read when interpreting PostgreSQL `EXPLAIN (ANALYZE, BUFFERS)` or MySQL `EXPLAIN` / `EXPLAIN ANALYZE` output.
