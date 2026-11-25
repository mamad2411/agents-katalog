---
name: database-queries
description: "Writing queries that are correct and fast: joins, aggregates, window functions and CTEs, the N+1 problem, keyset pagination, selecting only what is needed, parameters always, reading EXPLAIN, and the ORM habits that cause slow queries. Read before writing or reviewing a query or an ORM data access path."
---

# Queries that are right and fast

The generated query: `SELECT *` over two joins, summed in code, `DISTINCT`
added when the totals came out doubled, a day filtered with
`date(created_at) = ?` in the server's time zone, `NOT IN` against a column
with NULLs, and an ORM loop that loads each order's customer one at a time.
It returns plausible numbers on seed data and wrong ones, slowly, on real
data. This skill is correctness first, then speed. Indexes are in
`database-indexes`, locking and races in `database-transactions`. Examples
are PostgreSQL unless marked.

## 1. Correct before fast

- **Joins that multiply rows.** Joining orders and payments to customers
  repeats each order once per payment, and the sums double. Aggregate each
  child before joining (or use LATERAL or a subquery):

```sql
SELECT c.id, c.name, coalesce(o.order_count, 0) AS order_count, o.revenue_cents
FROM customers c
LEFT JOIN (
  SELECT customer_id, count(*) AS order_count, sum(total_cents) AS revenue_cents
  FROM orders WHERE status = 'paid'
  GROUP BY customer_id
) o ON o.customer_id = c.id;
```

  `DISTINCT` added to fix a count hides the fan-out while the sums stay
  wrong. For "has any", use `EXISTS`, not a join.
- **NULL.** `x = NULL` is never true: `IS NULL`, `IS DISTINCT FROM`.
  `NOT IN (subquery)` returns nothing at all if the subquery yields one NULL:
  use `NOT EXISTS`. `count(col)` skips NULLs, `count(*)` does not; `sum` over
  no rows is NULL (`coalesce(sum(x), 0)`); `avg` ignores NULLs.
- **Outer joins.** A condition on the right-hand table in `WHERE` turns a
  LEFT JOIN into an inner join; put it in `ON`.
- **GROUP BY.** Every selected column is grouped or aggregated. Keep MySQL's
  `ONLY_FULL_GROUP_BY` on; without it MySQL returns an arbitrary row's value.
- **Time ranges**: half-open, in the user's zone, on the raw column:

```sql
-- orders placed on 1 September 2026, Jakarta time
WHERE created_at >= '2026-09-01 00:00:00+07' AND created_at < '2026-09-02 00:00:00+07'
```

  Not `created_at::date = '2026-09-01'` (server zone, no index), not
  `BETWEEN` (includes the end, misses 23:59:59.5).
- **Order.** Without `ORDER BY` rows come in whatever order the plan made.
  With `LIMIT`, end the sort on a unique column (`created_at DESC, id DESC`).
- **Arithmetic**: `7 / 2` is `3` on integers; cast for ratios
  (`7::numeric / 2`), and round money once, at the end.

## 2. SQL worth knowing

- Top N per group: `row_number()`, `DISTINCT ON` for the top one
  (Postgres), or `LATERAL` with `LIMIT`, which walks an index on
  `(customer_id, created_at)` instead of ranking every row:

```sql
SELECT c.id, last.*
FROM customers c
CROSS JOIN LATERAL (
  SELECT id, total_cents, created_at FROM orders
  WHERE customer_id = c.id
  ORDER BY created_at DESC, id DESC
  LIMIT 3
) last;
```

- Running totals: `sum(amount_cents) OVER (PARTITION BY account_id ORDER BY
  created_at, id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`. Say
  `ROWS`: the default `RANGE` frame lumps rows with equal sort keys.
- Conditional aggregates: `count(*) FILTER (WHERE status = 'paid')`
  (Postgres, SQLite 3.30+); in MySQL `SUM(status = 'paid')`.
- CTEs for readability. Since Postgres 12 a CTE used once is inlined;
  `AS MATERIALIZED` computes it once as a fence, `NOT MATERIALIZED` inlines.
- Upsert: `INSERT ... ON CONFLICT (shop_id, sku) DO UPDATE SET stock =
  excluded.stock` (Postgres, SQLite 3.24+); MySQL 8.0.19+
  `INSERT ... AS new ON DUPLICATE KEY UPDATE stock = new.stock` (`VALUES()`
  there is deprecated). `ON CONFLICT DO NOTHING RETURNING id` returns no row
  when it already existed: select it afterwards.
- `RETURNING` on insert, update and delete saves a round trip (Postgres,
  SQLite 3.35+, MariaDB 10.5+ on insert and delete; not MySQL).
- `MERGE` (Postgres 15+, `RETURNING` from 17) for multi-branch syncs; for
  one table and a unique key, `ON CONFLICT` is simpler and safe under races.

## 3. Bulk work

- Inserts as multi-row `VALUES` in batches of 500 to 1,000 rows. Postgres
  takes at most 65,535 bind parameters per statement, SQLite 32,766 by
  default. Or send arrays: `INSERT INTO tags (name) SELECT unnest($1::text[])`,
  and `WHERE id = ANY($1)` for a list in one parameter.
- Large loads: `COPY ... FROM STDIN` through the driver (Postgres),
  `LOAD DATA` (MySQL), one transaction around the inserts (SQLite: thousands
  per second instead of dozens).
- Reading a big table: keyset batches (`WHERE id > $last ORDER BY id LIMIT
  1000`) or a server-side cursor (psycopg named cursors, SQLAlchemy
  `yield_per`, Django `.iterator(chunk_size=2000)`, Rails `find_each`,
  Laravel `chunkById` or `lazyById`). OFFSET chunking skips or repeats rows
  while the table changes.
- Bulk updates as one statement:
  `UPDATE products p SET price_cents = v.price FROM (VALUES (1, 1500), (2, 990)) AS v(id, price) WHERE p.id = v.id;`

## 4. N+1

- One query for a list, then one per row for a relation: 50 rows are 51
  round trips, 100ms of waiting at 2ms each before any work is done.
- Find it: the query log in development (Prisma `log: ['query']`,
  `django-debug-toolbar`, Rails `bullet` or `strict_loading`, Laravel
  `Model::preventLazyLoading()`), or a test that counts queries per request
  (Django `assertNumQueries`).
- Fix it with one more query or a join:

| Layer | Eager load |
|---|---|
| Prisma | `include: { customer: true }`, or `select` with the relation |
| Drizzle | relational queries, `with: { customer: true }` |
| SQLAlchemy | `selectinload(Order.items)`, `joinedload(Order.customer)` |
| Django | `select_related("customer")`, `prefetch_related("items")` |
| Rails | `includes(:customer)`, `preload`, `eager_load` |
| Laravel | `with('customer')`, `load()` |
| GraphQL | a DataLoader per request |

- For to-many relations prefer the separate `IN` query (`selectinload`,
  `prefetch_related`, `preload`): a join repeats the parent's columns for
  each child.

## 5. Pagination and counts

- Keyset for long or changing lists, with an index on the sort key and id:

```sql
SELECT id, created_at, total_cents FROM orders
WHERE customer_id = $1
  AND (created_at, id) < ($2, $3)   -- the last row of the previous page
ORDER BY created_at DESC, id DESC
LIMIT 50;
```

  Row comparison works in Postgres and SQLite; in MySQL write
  `created_at < ? OR (created_at = ? AND id < ?)`, which it plans reliably.
- OFFSET only for short lists and page-numbered admin screens: every skipped
  row is read and thrown away, and rows shift between pages as data changes.
- Exact counts scan in Postgres and InnoDB. For a whole table, an estimate:
  `SELECT reltuples::bigint FROM pg_class WHERE oid = 'orders'::regclass;`.
  For a filter, a capped count shown as "10,000+":
  `SELECT count(*) FROM (SELECT 1 FROM orders WHERE ... LIMIT 10001) t;`.
  Or no total at all, only "next".

## 6. Fast by default

- Select the columns you use. `SELECT *` drags big `text` and `jsonb`
  columns over the network, prevents index-only scans, and changes shape
  when a column is added.
- Keep predicates usable by an index: nothing computed on the indexed column
  (`created_at > now() - interval '1 day'`, not
  `created_at + interval '1 day' > now()`; `lower(email) = $1` only with an
  index on `lower(email)`), and no implicit casts (MySQL comparing a
  `VARCHAR` column to a number scans the table).
- `LIKE 'abc%'` can use a B-tree (Postgres needs `text_pattern_ops` unless
  the collation is `C`); `LIKE '%abc%'` and `ILIKE` need trigrams
  (`database-indexes`) or full-text search.
- `OR` across different columns often scans; rewrite as `UNION ALL` of two
  indexed queries when the plan says so.
- `EXISTS` for "is there any", not `count(*) > 0`.
- A ceiling on every query: `statement_timeout` for the web role (5 to 15s)
  and `SET LOCAL statement_timeout = '2s'` inside the transaction of a risky
  one, so a bad plan fails instead of piling up connections.

## 7. Parameters, always

- Values through placeholders (`$1`, `?`, `:name`) or a safe template
  (postgres.js and Drizzle `sql` tagged templates, Prisma `$queryRaw` with a
  template literal, SQLAlchemy `text()` with bound parameters). Never
  `$queryRawUnsafe`, `sql.raw`, f-strings or `+` with anything a user sent.
- Identifiers (sort column, direction) cannot be parameters: map them from
  an allow-list (`{ newest: 'created_at DESC', total: 'total_cents DESC' }`),
  or quote with `format('%I', name)` inside Postgres functions.
- A list as one array parameter (`= ANY($1)`) or the builder's expansion,
  never a joined string.

## 8. Reading EXPLAIN

`EXPLAIN (ANALYZE, BUFFERS)` runs the query and reports what happened
(Postgres 18 adds buffers by default). For a write:
`BEGIN; EXPLAIN (ANALYZE, BUFFERS) UPDATE ...; ROLLBACK;`.

| You see | It means | Try |
|---|---|---|
| `Seq Scan` on a big table, `Rows Removed by Filter` in the millions | No usable index for the filter | An index on the filter; a sargable rewrite |
| Estimated `rows=10`, actual `rows=100000` | Stale statistics or correlated columns | `ANALYZE orders`; `CREATE STATISTICS` on the columns |
| `Nested Loop` with a large `loops=` | A plan made for few rows ran for many | Fix the estimate; index the inner join key |
| `Sort Method: external merge  Disk: ...` | The sort spilled to disk | An index in `ORDER BY` order, or more `work_mem` for it |
| `Index Only Scan` with many `Heap Fetches` | The visibility map is behind | Vacuum the table |
| `Buffers: shared read=` large | Pages came from disk, not cache | Fewer rows or columns; check the cache hit ratio |

- Per-node times are per loop: multiply by `loops`. Paste a plan into
  explain.dalibo.com or explain.depesz.com to read it as a tree.
- MySQL: `EXPLAIN ANALYZE` (8.0.18+) or `EXPLAIN FORMAT=TREE`; `type: ALL` is
  a full scan, `Using filesort` and `Using temporary` are sorts and temp
  tables. SQLite: `EXPLAIN QUERY PLAN` (`SCAN` is a full scan, `SEARCH ...
  USING INDEX` is not). MongoDB: `explain("executionStats")`.
- Judge plans on realistic volumes: on a 100-row table a sequential scan is
  the right plan.

## 9. ORM habits that make queries slow

- Lazy loading inside a loop or a template (section 4).
- Whole records loaded to use two fields: `select`, `only()`, `values()`,
  `pluck`, `defer` for big columns.
- Counting or checking in memory (`len(queryset)`, `->get()->count()`,
  `.length` of a fetched array); use `count()` and `exists()`.
- Read, change, save for counters and totals; an `UPDATE` with an expression
  (`F("stock") - 1`, `decrement('stock')`, `{ stock: { decrement: 1 } }`) is
  one query and race-free (`database-transactions`).
- A save per row in a loop; use `bulk_create`, `insert_all`, `createMany`.
- Filtering after fetching; filter in the query.
- `findMany()` or `all()` behind an endpoint with no limit.

## Check it

- Run the query with the edge rows present: NULLs, a customer with no
  orders, an order with several payments, a row at 23:59 on the boundary
  day.
- Compute an aggregate a second, simpler way (a count through `EXISTS`
  against the join version) and compare.
- `EXPLAIN (ANALYZE, BUFFERS)` on production-like volumes: the intended
  index is used and estimates are within about ten times of actual rows.
- Count queries per request in development: a list page issues the same
  number of queries for 5 rows as for 500.
- After release, `pg_stat_statements` or the slow log: the new query is not
  among the top by total time.

## Avoid

`SELECT *`; `DISTINCT` to hide duplicated rows; sums over joins that fan
out; `NOT IN` with a nullable subquery; `date(created_at) = ?`; `BETWEEN` on
timestamps; `LIMIT` without a unique `ORDER BY`; deep OFFSET pages; exact
counts of millions of rows on every page view; a query per row; values or
sort columns concatenated into SQL; functions on indexed columns in `WHERE`;
a plan judged on a 100-row table; a table read into memory to filter or
count it.
