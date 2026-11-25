---
name: sql-performance
description: "Make a slow SQL query fast, or prove it cannot be: start from the statement with the most total time in pg_stat_statements or MySQL's performance_schema, not the one someone complained about, read EXPLAIN (ANALYZE, BUFFERS) from the deepest node out to the first place estimated and actual rows diverge tenfold, and fix what that divergence names — stale statistics, a correlated predicate, a generic plan. Covers index choice and column order, ORM N+1 in the query log, and pool exhaustion that only looks like a slow query. Use this skill whenever someone says \"this endpoint takes 4 seconds\", \"why is postgres not using my index\", \"explain analyze output attached\", or asks whether a column needs an index. Not for a wrong answer rather than a slow one, which is debugging; not for shipping a schema change, which is db-migration; not for sizing for an expected peak, which is capacity-planning; not for time outside the query itself, which is profiling."
allowed-tools: "Read, Grep, Glob, Edit, Bash(psql:*), Bash(mysql:*), Bash(pt-query-digest:*), Bash(mysqldumpslow:*)"
---

# SQL Performance

This is finished when you can name the plan node that produced the cost, say in one sentence why the planner chose it, and show a before and after measurement of the same statement against data that resembles production — or when you can say which of the four non-index answers applies and why.

Four things go wrong, and each of them feels like work. The first is tuning the wrong query: the one a person noticed is the one that is visible, not the one that is expensive, and a statement running 40,000 times a minute at 0.8ms outranks the 900ms report nobody waits for. The second is reading `EXPLAIN` instead of `EXPLAIN ANALYZE` and reporting the planner's guess as a measurement — the guess is precisely what is wrong when a query is slow for a reason the planner did not see. The third is chasing the node with the biggest time, which is usually an innocent index scan being asked to run 48,000 times because a node below it was estimated at 12 rows and returned 48,213; the fix goes in at the estimate, not at the node doing the work. The fourth is answering every complaint with an index, which is free to write and permanent to carry: each one slows every write to the table, and in PostgreSQL an index on a frequently-updated column disables heap-only-tuple updates and turns the table into a bloat generator.

Be specific about the engine at every step. PostgreSQL and MySQL disagree about partial indexes, about what "using index" means, about clustered storage and about how a prepared statement is planned, and advice that does not name the engine is wrong about one of them.

## Scope

Use for: a slow statement, endpoint or job where the time is in the database; reading an `EXPLAIN ANALYZE` plan someone has pasted; deciding whether to add, extend or drop an index; a query that degraded as a table grew; a query fast for most parameters and slow for one; an ORM producing hundreds of small queries; deciding that a query cannot usefully be made faster and what to do instead.

Do not use for: a query returning the wrong rows rather than slow ones, which is `debugging`; getting the schema change or the index itself onto a live database without taking a lock, which is `db-migration` — decide the index here, ship it there; designing the schema and its indexes before a single table exists, which is `schema-design`; deciding whether the system survives an expected peak, or sizing instances and replicas, which is `capacity-planning`; choosing offset against cursor pagination as an interface commitment, which is `api-design`, though the keyset rewrite below is the query half of the same decision; judging a diff nobody has run, which is `code-review`; adding spans and metrics so the next one is diagnosable, which is `instrumentation`; a live outage, which is `incident-response`, or `k8s-triage` for a Kubernetes workload.

## Gates

1. A measurement from the database before any change. Not a profiler's opinion of where time goes and not a recollection of which query is slow.
2. `EXPLAIN (ANALYZE, BUFFERS)` on PostgreSQL, `EXPLAIN ANALYZE` on MySQL 8.0.18 or later. Both execute the statement, so wrap anything that writes in a transaction you roll back.
3. One change at a time, re-measured. An index and a rewrite applied together leave you unable to drop the index that did nothing.
4. No index added without naming the write cost, checking whether an existing index can be extended instead, and confirming the new one is actually used afterwards.
5. Measure against production-like row counts and distribution, or state plainly that the number is not trustworthy. A plan chosen over 5,000 rows tells you nothing about 50 million.

## Workflow

### 1. Find the statement that actually costs the most

Order by total time, never by mean. Mean time hides the N+1 that is the whole problem, and the top of a list sorted by mean is usually a nightly report.

PostgreSQL, with `pg_stat_statements` loaded via `shared_preload_libraries` and `CREATE EXTENSION pg_stat_statements`:

```sql
SELECT calls,
       round(total_exec_time::numeric, 0)  AS total_ms,
       round(mean_exec_time::numeric, 2)   AS mean_ms,
       rows,
       shared_blks_hit, shared_blks_read,
       left(query, 120) AS query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 15;
```

The column is `total_exec_time` from PostgreSQL 13 onward and `total_time` before that. `SELECT pg_stat_statements_reset();` first when you want a window rather than everything since the last restart — an all-time ranking is dominated by whatever ran during the last backfill.

MySQL, from `performance_schema`, where the timers are picoseconds:

```sql
SELECT count_star,
       round(sum_timer_wait / 1e12, 1) AS total_s,
       round(avg_timer_wait / 1e9,  2) AS avg_ms,
       left(digest_text, 120)          AS query
FROM performance_schema.events_statements_summary_by_digest
ORDER BY sum_timer_wait DESC
LIMIT 15;
```

`sys.statement_analysis` presents the same data with the units already applied. For the slow query log, `long_query_time` is read at connect time, so `SET GLOBAL long_query_time = 0.2` affects new connections only — existing pool connections keep the old value until they are recycled, which is why "I turned it on and nothing appeared". Aggregate the log with `pt-query-digest /var/log/mysql/slow.log` rather than reading it; `mysqldumpslow -s t` is the smaller alternative when Percona Toolkit is not installed.

When the slow statement will not reproduce outside production, capture the plan where it happens: PostgreSQL's `auto_explain` with `auto_explain.log_min_duration = '500ms'` and `auto_explain.log_analyze = on` logs the real plan for the real parameters. `log_analyze` adds per-node instrumentation overhead to every statement it captures, so turn it on for a window rather than leaving it on.

Write down the ranking before touching anything. It is the evidence that the query you are about to spend an afternoon on is worth the afternoon.

### 2. Confirm the time is in the database at all

A pool that has run out of connections presents exactly as a slow query: the endpoint takes two seconds, and every statement the database reports is fast. Check this before reading a plan, because the plan will look fine and you will keep reading it.

The test is one subtraction. Sum the database-side time for the statements a request issues and compare it to the request's own latency. If the database accounts for 20ms of a 2,000ms request, the time is spent waiting for a connection or elsewhere in the application, and no index will move it.

- HikariCP and similar pools expose a pending-acquisition count and an acquire timer. Pending above zero under normal load is the finding.
- PgBouncer: `SHOW POOLS;` — `cl_waiting` above zero with a non-trivial `maxwait` is clients queueing for a server connection.
- PostgreSQL: `SELECT state, count(*) FROM pg_stat_activity GROUP BY state;` A pile of `idle in transaction` means connections are held open across work that is not database work.

In order of how often each is the cause: a transaction left open across an HTTP call or a slow external service; a connection leaked on an error path; a pool sized below the request concurrency; and one genuinely slow query occupying every connection at once, which is the case where this step hands back to the rest of the skill. Size the pool small rather than large — roughly twice the core count plus the effective spindle count is the standard guidance, and a larger pool usually lowers throughput because the database is the contended resource. In PostgreSQL every connection is an operating-system process, so the answer to needing 500 of them is PgBouncer in transaction mode, not a higher `max_connections`.

### 3. Get the plan, with actual rows in it

PostgreSQL:

```sql
EXPLAIN (ANALYZE, BUFFERS, VERBOSE) SELECT ...;
```

`BUFFERS` is what tells you whether the time was I/O or work: `shared hit=` is cache, `shared read=` is a fetch, `temp read=/written=` is a spill to disk. `SETTINGS` (PostgreSQL 12 and later) appends any non-default planner settings, which is how you find the `work_mem` or `random_page_cost` someone set in this session and forgot. `SET track_io_timing = on` adds real I/O timings. On a plan with hundreds of thousands of loops the per-node timing instrumentation itself distorts the result — use `EXPLAIN (ANALYZE, BUFFERS, TIMING OFF)` and read row counts instead.

For a statement that writes, `ANALYZE` executes it:

```sql
BEGIN;
EXPLAIN (ANALYZE, BUFFERS) UPDATE orders SET status = 'shipped' WHERE id = 42;
ROLLBACK;
```

MySQL: `EXPLAIN ANALYZE` (8.0.18 and later) gives actual time, rows and loops per iterator; `EXPLAIN FORMAT=TREE` (8.0.16 and later) gives the same shape with estimates only; plain `EXPLAIN` gives the classic table, which is still the fastest way to see `type`, `key` and `Extra`. `EXPLAIN ANALYZE` also executes the statement, so wrap a write in `START TRANSACTION; ... ROLLBACK;` — and note that DDL cannot be rolled back in MySQL at all.

Run it twice and compare. The first run reads from disk and the second from cache, and a "10x improvement" that is really a warm cache is the most common false result in this work.

### 4. Read the plan outward from the deepest node

The reading order is fixed, and it is not top to bottom.

1. Read `Planning Time` and `Execution Time` first. Planning time that is a meaningful fraction of the total points at a partitioned table with too many partitions or a plan cache doing no work, which is a different problem from the one in the plan.
2. Go to the deepest, most-indented node — the leaf with no children. That is where rows enter.
3. At each node compare the estimate, `rows=` in the first parenthesis, against the measurement, `rows=` in the `actual` parenthesis. Both are per execution of that node. `loops=N` says the node ran N times, so total work is rows × loops, but the comparison you want is the two `rows=` values as printed.
4. Walk outward, one node at a time, and stop at the first node where the two differ by roughly an order of magnitude. That node is the cause.
5. Only now look at time. A node's `actual time` includes its children, so its own cost is `(total time × loops)` minus the same for each child.

Step 4 is the whole technique. Every node above the first bad estimate inherits it: a nested loop told to expect 12 outer rows makes a perfectly sensible choice, then runs its inner side 48,213 times. The inner node will have the largest time in the plan and there will be nothing wrong with it. Chasing it is the wasted hour this skill exists to prevent.

`references/reading-a-plan.md` has the worked example end to end for both engines — a real plan, the divergence located, the fix, and what changed — plus what each node type means and the specific strings worth searching a plan for. Read it when you have a plan in front of you.

### 5. Name what the divergence means

| What you see | Usual cause | Fix |
| --- | --- | --- |
| Estimate far below actual, single table, one predicate | Statistics are stale; the table grew or was bulk-loaded since the last sample | `ANALYZE t;` (PostgreSQL) or `ANALYZE TABLE t;` (MySQL). If it recurs, autovacuum is not keeping up: `ALTER TABLE t SET (autovacuum_analyze_scale_factor = 0.02)` beats the 0.1 default on a large table |
| Estimate far below actual, two or more predicates on the same table | The planner multiplies selectivities as if independent, and the columns are correlated — pending orders are recent orders | PostgreSQL, and only when the correlated predicates are equalities: `CREATE STATISTICS s (dependencies, mcv) ON status, tier FROM orders;` then `ANALYZE orders;`. A correlated range gets nothing from this — give it a partial or composite index instead. MySQL has no multi-column statistics: a composite index or a restructured predicate |
| Estimate is a suspiciously round number | The planner has no statistics for that expression — a function call, a set-returning function, an opaque subquery | PostgreSQL: index the expression (`CREATE INDEX ON users (lower(email))`), or declare `ROWS` and `COST` on the function, or from 14 onward `CREATE STATISTICS ON lower(email) FROM users`. MySQL 8.0.13 and later: a functional index, which is a hidden generated column underneath |
| Estimate wrong only for certain parameter values | PostgreSQL built a generic plan: from the sixth execution of a prepared statement it may plan without the values | The condition shows `$1` rather than a literal. `SET plan_cache_mode = force_custom_plan` (PostgreSQL 12 and later), per session or per role. MySQL re-optimises a prepared statement on each execution, so this is rarely a MySQL finding |
| Estimate far above actual | A skewed column the histogram resolution cannot represent | PostgreSQL: `ALTER TABLE t ALTER COLUMN c SET STATISTICS 1000;` (up to 10000) then `ANALYZE`. MySQL: `ANALYZE TABLE t UPDATE HISTOGRAM ON c WITH 64 BUCKETS;` |
| `Rows Removed by Filter` large under an index scan | The index reaches a range and then most of it is thrown away | Put the filtered column in the index, as a later column or as a partial-index predicate |
| `Sort Method: external merge  Disk: 24MB`, or MySQL `Using filesort` over many rows | The sort spilled | Raise `work_mem` for that statement only (`SET LOCAL work_mem = '64MB'`), or provide the order with an index. MySQL: `sort_buffer_size`, or an index |
| Hash join with `Batches: 8` | The hash table did not fit in `work_mem` | Same as above, and check the build side is the smaller relation |
| `Heap Fetches:` large on an index-only scan | The visibility map is stale, so the "index-only" scan is visiting the heap anyway | `VACUUM t;` and check autovacuum is reaching this table |
| `loops=` very large on an inner node | A nested loop driven by a bad outer estimate | Fix the estimate on the node below; the inner node is not the problem |

### 6. Decide whether an index is the answer

**A sequential scan is not a defect.** It is correct when the table is small enough that the index adds a round trip for nothing, when the predicate matches a large fraction of rows, when the query aggregates most of the table anyway, and when the pages are already in cache (`Buffers: shared hit=` with `read=0`). What is a defect is a sequential scan over 40 million rows that returns twelve.

The rough selectivity where an index stops paying, with PostgreSQL's defaults of `seq_page_cost = 1` and `random_page_cost = 4`: an index path costs up to four page fetches per matched row when matched rows land on distinct pages, so break-even sits near a quarter of the table's pages. In practice, under about 1% of rows an index is almost always right; between 1% and 10% it depends on physical correlation (`pg_stats.correlation` for that column) and on whether an index-only scan is available; above roughly 20% the sequential scan is usually correct and forcing the index makes the query slower. On SSD, `random_page_cost = 1.1` is the usual setting and it moves that boundary up. MySQL's optimiser makes the same trade with different constants, and `eq_range_index_dive_limit` is where a large `IN` list's estimate goes wrong: past that many values it stops diving into the index and falls back to coarser statistics.

To find out what the planner thinks the index would have cost, make it choose the index and read the estimate:

```sql
SET enable_seqscan = off;   -- a diagnostic, in a session, never a fix in production
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;
RESET enable_seqscan;
```

If the index path is genuinely more expensive, the planner was right and the answer is in step 7.

The index decisions that carry real gates:

- **Column order is not negotiable.** A b-tree is sorted by the whole tuple, so `(a, b)` serves `WHERE a = ?`, `WHERE a = ? AND b = ?` and `WHERE a = ? ORDER BY b` — and does not serve `WHERE b = ?`. Equality columns first, then the single range column, then the columns you order by. Once a range predicate is used on a column, the columns after it are no longer in usable order for anything.
- **Covering indexes and index-only scans.** PostgreSQL: `CREATE INDEX ON orders (customer_id) INCLUDE (total)` (11 and later) lets the scan answer from the index — verify with `Heap Fetches: 0`, because a stale visibility map silently takes the win away. MySQL: `Extra: Using index` means covering, and an InnoDB secondary index already contains the primary key, so primary-key columns are free in every secondary index.
- **Partial indexes are PostgreSQL only.** `CREATE INDEX ON jobs (created_at) WHERE state = 'pending'` on a table that is 0.3% pending is a tiny index that stays in cache. MySQL has no equivalent; the nearest thing is a generated column with an index on it.
- **A low-cardinality column earns nothing on its own.** An index on a three-value status matches a third of the table, the planner will decline it, and the planner will be right. It is worth something only as the leading column of a composite index whose later columns are selective, or as the predicate of a PostgreSQL partial index on the rare value.
- **Every index is paid for on every write.** Each one is another structure to maintain on `INSERT`, `DELETE` and any `UPDATE` touching its columns. In PostgreSQL the sharper cost is heap-only-tuple updates: an `UPDATE` that touches no indexed column and finds room on its page updates no index at all, so indexing a hot, frequently-updated column takes that optimisation away and converts the table into a bloat source.

`references/index-selection.md` has the full decision, the queries that find unused and redundant indexes in both engines, prefix and expression indexes, `LIKE` and text search, and what to check before dropping one. Read it before adding or removing an index.

### 7. The N+1, which the log shows and the code hides

It appears in step 1 as one statement with tens of thousands of `calls`, a mean under a millisecond, and a place near the top of the list by total time. It never appears in a MySQL slow log at a default `long_query_time`, which is the reason step 1 sorts by total.

Detect it from the query log, not by reading code. The code that produces it is a loop over a collection touching a relation, and it looks entirely reasonable. On PostgreSQL, `SET log_min_duration_statement = 0` on one session for a minute, or read `calls` in `pg_stat_statements`. On MySQL, `SET GLOBAL long_query_time = 0` for a window and run `pt-query-digest` over the result. The number to look at is queries per request, not milliseconds per query.

Three fixes, and the trade-off is the whole choice:

1. **One statement with a join** — Django `select_related`, SQLAlchemy `joinedload`, ActiveRecord `includes` when it resolves to a join. Cheapest for a to-one relation. For a to-many relation it multiplies parent rows by child rows and re-sends every parent column once per child, and with two collections it is a cartesian product that is slower than the N+1 it replaced.
2. **A second statement with `WHERE parent_id IN (...)`** — Django `prefetch_related`, SQLAlchemy `selectinload`, ActiveRecord `preload`. The right default for collections: two round trips, no row multiplication. The cost is that the `IN` list varies in length, which churns plan caches and can hit parameter limits, so it should be chunked rather than unbounded.
3. **Denormalise or cache the one value you needed** — a counter column on the parent, maintained in the same transaction, or a cache. Correct when the value is read far more often than written; the cost is invalidation, which is now yours.

The fourth answer is to leave it. Twelve queries rendering an admin page that loads once a day is not a problem. What stops a real one from returning is an assertion on the query count in a test — Django's `assertNumQueries`, an ActiveRecord counter subscriber, a SQLAlchemy event listener — added in the same change as the fix.

### 8. When the answer is not an index

Each of these has a test. Apply the test before the work, not after.

- **Rewrite the query.** Test: the plan shows work the answer did not need — an `OFFSET` discarding 50,000 rows to return 20, a `DISTINCT` compensating for a join fan-out, a correlated subquery executed once per row, an `OR` across two columns that stops either index being usable. Keyset pagination replaces the offset: `WHERE (created_at, id) < (?, ?) ORDER BY created_at DESC, id DESC LIMIT 20`, which needs an index on `(created_at DESC, id DESC)` and a total order to be correct. A `UNION ALL` of two index-using branches replaces the `OR`. A lateral or derived-table aggregate replaces the correlated subquery.
- **Denormalise.** Test: the value is read far more often than it is written, and the write path can maintain it in the same transaction. A materialised view with `REFRESH MATERIALIZED VIEW CONCURRENTLY` (PostgreSQL, and it requires a unique index on the view) fits when minutes of staleness are acceptable; a trigger-maintained counter fits when they are not. The schema change itself is `db-migration`.
- **Cache.** Test: state the staleness the product will accept as a number, and estimate the hit rate, both before building anything. A cache in front of a query with a 5% hit rate is a second system to operate in exchange for nothing, and it converts a latency problem into a correctness problem.
- **Accept it.** Test: the statement's share of total database time — which step 1 already ranked — is small, or it is a nightly job that finishes inside its window. Write the number down, say it is accepted, and move to the query above it in the ranking.

### 9. Prove the improvement

Same statement, same parameters, same warmed cache state, before and after, on data that resembles production. Report total time and rows examined, not just wall clock: a 40x improvement that came from a cache warmed by the previous run will not survive deployment. Then confirm the new index is used — `pg_stat_user_indexes.idx_scan` for it should be climbing — and re-check the ranking from step 1, because fixing the top statement promotes a new one and the second is sometimes the same bug.

## Anti-patterns

**An index per slow query.** Each complaint adds one, none is ever removed, and a year later the table carries fourteen indexes, writes cost four times what they did, and the planner is choosing between near-duplicates. The gate is to check first whether an existing index can be extended by one column instead, and to look at what the existing ones are actually used for.

**`SELECT *` in a hot path.** It rules out the index-only scan that would have made the query fast, drags large out-of-line values over the wire in PostgreSQL and BLOBs in MySQL, and silently gets more expensive the next time someone adds a column.

**Tuning against a dataset that does not resemble production.** Over 5,000 rows the planner sequentially scans everything and every index looks useless; the plan shape changes with volume, not just the timing. Check the numbers before believing a local result: `SELECT reltuples FROM pg_class WHERE relname = 't'` and `SELECT n_distinct, most_common_freqs FROM pg_stats WHERE tablename = 't' AND attname = 'c'` on PostgreSQL; `SHOW TABLE STATUS LIKE 't'` on MySQL, where `Rows` is an InnoDB estimate that can be off by half.

**Optimising a query nobody runs.** The report that takes nine seconds and runs twice a month costs less per year than the 0.8ms statement running 40,000 times a minute. The ranking in step 1 is the defence, which is why it comes first.

**Reporting `EXPLAIN` without `ANALYZE`.** Those numbers are the planner's estimate, and a query is usually slow precisely because the estimate is wrong. Costs are also in arbitrary units, so comparing the cost of one query against a different query is meaningless — only the same query before and after can be compared.

**Fixing the plan with a hint.** `FORCE INDEX`, `pg_hint_plan` or `enable_seqscan = off` left on in production freezes a decision against data that will keep changing, and the freeze outlives the person who knew why. Use them to learn what the planner believed; if one must ship, record it with a date and the condition that would let it be removed.

**Believing the mean.** 2ms at the median and 900ms at p99 is two plans, or one plan meeting two data distributions, and the mean describes neither. Find which parameter values are in the slow group before touching anything.

## Output format

```markdown
## Statement
[The normalised SQL, and its rank: calls, total time, share of database time.]

## Where the time goes
[Database or not — the subtraction from step 2. Then the plan's Execution Time and the node that owns it.]

## Plan finding
[The first node where estimate and actual diverge, both numbers, and what the divergence names.]

## Cause
[One sentence naming the mechanism. Not "missing index" unless the index is genuinely missing.]

## Change
[The index, rewrite, statistics object or setting. For an index: exact DDL, and the write cost accepted.]

## Measurement
[Before and after on the same statement and parameters, cache state stated, against N rows.]

## Not done
[What was rejected and why — including "accepted as is", with the share of total time that justifies it.]
```

## Reference files

- `references/reading-a-plan.md` — read when you have a plan to interpret: the worked PostgreSQL example node by node with the arithmetic, the MySQL equivalent in both classic and `EXPLAIN ANALYZE` form, what every common node type and `Extra` value means, and the strings worth searching a plan for first.
- `references/index-selection.md` — read before adding, extending or dropping an index: column order with worked cases, covering and partial indexes, expression and prefix indexes, `LIKE` and text search, the write cost in each engine, and the queries that find unused and redundant indexes.
