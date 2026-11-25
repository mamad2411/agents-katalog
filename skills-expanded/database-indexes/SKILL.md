---
name: database-indexes
description: "Indexes that pay for themselves: B-tree by default, the order of columns in composite indexes, covering, partial and expression indexes, GIN for JSON, arrays, full text and trigrams, BRIN for time series, what each costs on writes, finding missing and unused ones, and creating them without locking. Read before adding, changing or removing an index."
---

# Indexes

The generated version: an index on every column one by one, none on the pair
the hot query filters by, `(created_at, customer_id)` for a query that
filters by customer, a GIN index on a `jsonb` column nobody queries with
`@>`, a boolean indexed alone, a foreign key without an index so deleting a
customer scans the orders table, and every index built with a plain
`CREATE INDEX` that blocks writes while it runs. An index is a sorted copy of
some columns: it makes certain reads fast and every write slower. This skill
is choosing the few that pay. Query shape is in `database-queries`. Examples
are PostgreSQL unless marked.

## 1. Start from the queries

- List the queries that matter: those on every request, the slowest by total
  time (`pg_stat_statements`), those behind a timeout. For each, note the
  equality columns, range columns, join keys, `ORDER BY` and `LIMIT`.
- `EXPLAIN (ANALYZE, BUFFERS)` before, create the index, `EXPLAIN` after;
  keep it only when the plan uses it and time or buffers drop. Test on
  realistic volumes: under a few thousand rows a sequential scan is right,
  and the planner ignores your index.
- One composite index often serves several queries; extending an existing
  index beats adding another.

## 2. B-tree and column order

B-tree is the default and serves `=`, `<`, `>`, `BETWEEN`, `IN`, `IS NULL`,
prefix `LIKE`, and `ORDER BY` in either direction.

- Equality columns first, then one range or sort column:

```sql
-- WHERE tenant_id = $1 AND status = $2 ORDER BY created_at DESC LIMIT 50
CREATE INDEX CONCURRENTLY idx_orders_tenant_id_status_created_at
  ON orders (tenant_id, status, created_at);
```

  It is read backwards for `DESC`; declare directions only for mixed sorts
  (`ORDER BY priority DESC, created_at` wants `(priority DESC, created_at)`).
- After a range condition the next columns cannot narrow the scan: for
  `WHERE customer_id = $1 AND created_at > $2`, `(customer_id, created_at)`
  is right and `(created_at, customer_id)` walks the whole range.
- Leftmost prefix: `(a, b, c)` serves filters on `a`, `a, b` and `a, b, c`,
  not `b` alone. Skip scan (Postgres 18, MySQL 8.0.13+) can use it for `b`
  when `a` has few distinct values; do not design for it.
- Among equality columns, lead with the one most queries share (`tenant_id`,
  the parent id), so the index serves them all.
- End with `id` for keyset pagination: `(customer_id, created_at, id)`.

## 3. Covering, partial, expression, unique

- **Covering** (`INCLUDE`, Postgres 11+) for index-only scans, which read no
  table pages while the visibility map is current (vacuum keeps it so):

```sql
CREATE INDEX CONCURRENTLY idx_orders_customer_id_created_at
  ON orders (customer_id, created_at) INCLUDE (status, total_cents);
```

  MySQL secondary indexes carry the primary key already; add other columns
  to the key.
- **Partial**: only the rows you query, so smaller and cheaper to keep:

```sql
CREATE INDEX CONCURRENTLY idx_jobs_queued_run_at ON jobs (run_at) WHERE status = 'queued';
CREATE UNIQUE INDEX CONCURRENTLY users_email_live_key
  ON users (lower(email)) WHERE deleted_at IS NULL;
```

  The query must repeat the condition as written, with a constant rather
  than a parameter. MySQL has no partial indexes (index a generated column
  that is NULL for the rows to skip); SQLite has them.
- **Expression**: index what the query computes. `ON users (lower(email))`
  serves `WHERE lower(email) = $1`, that exact expression; MySQL 8.0.13+
  writes `INDEX ((lower(email)))`. The expression must be immutable, so
  `date(created_at)` on a `timestamptz` is refused: filter by a range.
- **Unique**: prefer a constraint (`UNIQUE (shop_id, sku)`), which shows in
  the schema and can be the target of a foreign key; a unique index for
  partial and expression rules.

## 4. The other index types (Postgres)

| Type | For | Example |
|---|---|---|
| GIN | `jsonb` containment and keys, arrays, full text, trigrams | `USING gin (tags)` |
| GiST | Ranges and overlaps, exclusion constraints, geometry, nearest neighbour | `USING gist (during)` |
| BRIN | Huge append-only tables whose column follows insert order | `USING brin (created_at)` |
| HNSW (pgvector) | Vector similarity (`database-postgres`) | `USING hnsw (embedding vector_cosine_ops)` |
| Hash | Equality only | Rarely better than B-tree |

- `jsonb`: `jsonb_path_ops` is smaller and faster but serves only `@>`,
  `@?` and `@@`; the default `jsonb_ops` also serves key existence (`?`).
  One key compared by equality is better served by a B-tree expression:

```sql
CREATE INDEX CONCURRENTLY idx_events_payload ON events USING gin (payload jsonb_path_ops);
-- WHERE payload @> '{"type": "refund"}'
CREATE INDEX CONCURRENTLY idx_events_customer_id ON events ((payload ->> 'customer_id'));
-- WHERE payload ->> 'customer_id' = $1
```

- Full text: a stored generated `tsvector` column with GIN, queried with
  `search @@ websearch_to_tsquery('english', $1)`. Adding a stored column
  rewrites the table, so on a big one it is a migration step of its own:

```sql
ALTER TABLE articles ADD COLUMN search tsvector GENERATED ALWAYS AS
  (to_tsvector('english', coalesce(title, '') || ' ' || coalesce(body, ''))) STORED;
CREATE INDEX CONCURRENTLY idx_articles_search ON articles USING gin (search);
```

- Substring and fuzzy search (`ILIKE '%term%'`, similarity with `%`):
  `CREATE EXTENSION pg_trgm;` then
  `CREATE INDEX CONCURRENTLY idx_products_name_trgm ON products USING gin (name gin_trgm_ops);`.
  It helps from three characters of search term up.
- BRIN is kilobytes for billions of rows and helps only while physical order
  follows the column (append-only events by `created_at`); on tables that
  are updated or reordered it does nothing.
- GIN writes are expensive; its pending list (`fastupdate`) defers them at
  some cost to reads. Measure before adding GIN to a write-heavy table.

## 5. What each index costs

- Every insert writes every index. In Postgres an update that changes a
  column in any B-tree index loses the HOT path (updating in place without
  touching indexes) and writes every index of the table: an index on a hot
  table's `updated_at` does that to every update.
- Indexes compete with table data for memory; a table whose indexes are
  bigger than its data is a smell. Vacuum, backups, restores and replication
  carry them all.
- Low selectivity alone is useless: `is_active` true for 95% of rows is
  never used for `true`. If the rare value is what you query, a partial
  index on it.
- Update-heavy tables leave room for HOT updates with
  `ALTER TABLE counters SET (fillfactor = 90);` (new pages; a rewrite
  applies it to all).

## 6. Foreign keys need indexes

Postgres indexes the referenced key (it is unique) but not the referencing
column. Without that index a join from the parent scans the child, and each
delete or key update on the parent scans the child while holding locks.
InnoDB creates one automatically. Single-column foreign keys without an
index whose first column matches:

```sql
SELECT c.conrelid::regclass AS table_name, c.conname, a.attname AS column_name
FROM pg_constraint c
JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = c.conkey[1]
WHERE c.contype = 'f' AND cardinality(c.conkey) = 1
  AND NOT EXISTS (
    SELECT 1 FROM pg_index i
    WHERE i.indrelid = c.conrelid AND i.indkey[0] = c.conkey[1]
  );
```

## 7. Missing, unused, duplicate

- Missing: the top of `pg_stat_statements` by `total_exec_time`, and big
  tables read by sequential scans:

```sql
SELECT relname, seq_scan, seq_tup_read, idx_scan, n_live_tup
FROM pg_stat_user_tables
WHERE n_live_tup > 100000
ORDER BY seq_tup_read DESC LIMIT 20;
```

  `auto_explain` with `auto_explain.log_min_duration = '500ms'` logs the
  plans of slow statements. MySQL: `sys.statements_with_full_table_scans`
  and the slow log.
- Unused: not scanned since statistics were reset, over a window that
  includes month-end jobs:

```sql
SELECT s.relname, s.indexrelname, s.idx_scan,
       pg_size_pretty(pg_relation_size(s.indexrelid)) AS size
FROM pg_stat_user_indexes s
JOIN pg_index i ON i.indexrelid = s.indexrelid
WHERE s.idx_scan = 0 AND NOT i.indisunique AND NOT i.indisprimary
ORDER BY pg_relation_size(s.indexrelid) DESC;
```

  Statistics are per server: check replicas before dropping, since reports
  may use an index only there. MySQL: `sys.schema_unused_indexes`; make it
  invisible first (`ALTER TABLE orders ALTER INDEX idx_x INVISIBLE`), drop it
  after a quiet week.
- Duplicates: two indexes on the same columns, or `(a)` beside `(a, b)`,
  where the second serves both unless `(a)` is unique. MySQL:
  `sys.schema_redundant_indexes`.
- Bloat after heavy updates or deletes: `pgstatindex()` from `pgstattuple`
  measures it; `REINDEX INDEX CONCURRENTLY` (Postgres 12+) rebuilds without
  blocking.

## 8. Creating and dropping on a live table

- Postgres: `CREATE INDEX CONCURRENTLY` and `DROP INDEX CONCURRENTLY`,
  outside a transaction, through the migration tool's no-transaction mode
  (`database-migrations`). Two table scans and a wait for older
  transactions make it slower, but writes continue. A failed build leaves an
  `INVALID` index to drop and rebuild. `SET maintenance_work_mem = '1GB'` in
  the session speeds up a big build.
- MySQL: `ALTER TABLE orders ADD INDEX idx_x (col), ALGORITHM=INPLACE,
  LOCK=NONE;` is online; on the largest tables gh-ost spares the replicas.
- SQLite: `CREATE INDEX` blocks writers while it runs; seconds for a few
  gigabytes, so run it at a quiet moment.
- MongoDB builds indexes without blocking since 4.2 (`database-mongodb`).

## 9. MySQL and SQLite notes

- InnoDB is clustered on the primary key: rows are stored in its order and
  every secondary index entry carries it. A wide key (a UUID string) bloats
  every index; a random one scatters inserts (`database-mysql`).
- MySQL prefix indexes (`INDEX (title(50))`) for long strings cannot cover a
  query or serve `ORDER BY`; keys are limited to 3,072 bytes (768
  `utf8mb4` characters).
- Histograms help filters on unindexed columns:
  `ANALYZE TABLE orders UPDATE HISTOGRAM ON status;`.
- SQLite: confirm with `EXPLAIN QUERY PLAN`, keep statistics with
  `PRAGMA optimize`; partial and expression indexes are supported.

## Check it

- `EXPLAIN (ANALYZE, BUFFERS)` of each target query before and after, on
  realistic volumes: the new index is in the plan and time or buffers
  dropped. If it is not in the plan, drop it.
- The build used `CONCURRENTLY` or the engine's online form, and
  `SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;` returns
  nothing.
- The foreign key query in section 6 lists nothing new.
- A week after release: the new index's `idx_scan` climbs and write latency
  on the table did not jump.

## Avoid

An index per column; the range column first in a composite; indexes no plan
uses; a boolean indexed alone; foreign keys without an index in Postgres;
`CREATE INDEX` without `CONCURRENTLY` on a live table; GIN on `jsonb` for
queries that never use `@>`; dropping an unused index without checking the
replicas and the monthly jobs; an index on a hot table's `updated_at` with
no query that needs it; an index judged on a table of 100 rows.
