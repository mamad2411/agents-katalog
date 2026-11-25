---
name: clickhouse-analytical-database-operations
description: >
  Covers operating ClickHouse, the leading open-source OLAP columnar
  database: MergeTree engine family selection (MergeTree,
  ReplacingMergeTree, AggregatingMergeTree, SummingMergeTree), sharding
  and replication topology via ReplicatedMergeTree and Distributed
  tables, and materialized views for streaming aggregation. Use when the
  user asks to "set up a ClickHouse cluster," "pick a MergeTree engine,"
  "why are my ClickHouse queries slow," "shard and replicate ClickHouse
  tables," "deduplicate rows in ClickHouse," or "build a ClickHouse
  materialized view for rollups."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: database-operations
  maturity: stable
---

# ClickHouse Analytical Database Operations

## Purpose

ClickHouse is a column-oriented OLAP database built for aggregating
billions of rows in sub-second time, at the cost of assumptions that
are the opposite of a typical OLTP engine: it favors large batched
inserts over row-by-row writes, has no transactional multi-row `UPDATE`/
`DELETE` in the traditional sense (mutations are async, heavyweight
background rewrites), and gets its performance almost entirely from
choosing the right member of the **MergeTree engine family** and a
sensible sharding/replication topology up front. This skill covers
those foundational decisions — engine selection, `ReplicatedMergeTree`
plus `Distributed` tables for a sharded/replicated cluster, and
materialized views for streaming aggregation — the operational core
that determines whether a ClickHouse deployment stays fast as data
volume grows.

## When to use

- Designing a new ClickHouse table and choosing among `MergeTree`,
  `ReplacingMergeTree`, `SummingMergeTree`, `AggregatingMergeTree`, or
  `CollapsingMergeTree`/`VersionedCollapsingMergeTree` for the table's
  actual update/deduplication pattern.
- Setting up a sharded and/or replicated ClickHouse cluster
  (`ReplicatedMergeTree` plus `Distributed` table engine) for scale-out
  or fault tolerance.
- Query performance is poor despite the right engine choice — usually a
  partition/order-by key mismatch with actual query filters.
- Building a materialized view to maintain a pre-aggregated rollup
  incrementally as data is inserted, instead of aggregating raw
  high-cardinality data on every query.
- Diagnosing excessive background merge activity, "too many parts"
  errors, or a mutation (`ALTER TABLE ... UPDATE/DELETE`) that's taking
  much longer than expected.

## Prerequisites & environment

- ClickHouse 23.x/24.x assumed for the syntax below; note that
  `ReplicatedMergeTree` historically required ZooKeeper for replica
  coordination, while ClickHouse Keeper (`clickhouse-keeper`, a
  ClickHouse-native reimplementation of the ZooKeeper protocol) is now
  the recommended coordination layer for new deployments — check which
  your cluster uses before assuming ZooKeeper-specific tooling applies.
- A coordination service (ClickHouse Keeper or ZooKeeper, an odd number
  of nodes — 3 minimum) reachable by every node, required for any
  `Replicated*` table engine to coordinate replica state and part
  assignment.
- Cluster topology defined in `config.xml`/`cluster.xml`
  (`<remote_servers>`) so `Distributed` tables know the shard/replica
  layout — this is infrastructure configuration, not something set
  per-query.
- Enough disk headroom for background merges: ClickHouse periodically
  merges smaller data parts into larger ones, and a merge briefly
  requires space for both the source parts and the resulting merged
  part simultaneously.
- Client access via the native protocol (port 9000) or HTTP interface
  (port 8123); `clickhouse-client` for interactive administration.

## Step-by-step guidance

### 1. Choose the MergeTree engine variant to match the table's actual update pattern

Plain `MergeTree` is the default: an immutable, append-only, sorted
data structure per partition — there is no way to "update a row in
place," only insert new rows and periodically merge parts in the
background. The variants exist specifically to express common
update/aggregation patterns on top of that immutable model:

```sql
-- ReplacingMergeTree: keeps only the latest row per sorting-key value,
-- but only during background merges (not immediately on insert)
CREATE TABLE user_profiles (
  user_id UInt64,
  updated_at DateTime,
  email String
) ENGINE = ReplacingMergeTree(updated_at)
ORDER BY user_id;
```
Duplicate `user_id` rows are collapsed to the one with the latest
`updated_at` **only when ClickHouse happens to merge the parts
containing them** — a `SELECT` immediately after insert can still
return duplicates, so a query needing guaranteed deduplication must use
`FINAL`:
```sql
SELECT * FROM user_profiles FINAL WHERE user_id = 42;
```
`FINAL` forces merge-time deduplication logic at query time, which is
materially slower than a plain scan — use it only where correctness
requires it, not as a default on every query against a
`ReplacingMergeTree` table.

```sql
-- SummingMergeTree: sums numeric columns for rows sharing the same sort key, on merge
CREATE TABLE daily_revenue (
  day Date,
  region String,
  revenue Decimal64(2)
) ENGINE = SummingMergeTree(revenue)
ORDER BY (day, region);
```
```sql
-- AggregatingMergeTree: stores partial aggregate states, combined on merge/query
CREATE TABLE daily_stats (
  day Date,
  region String,
  revenue_state AggregateFunction(sum, Decimal64(2)),
  visits_state  AggregateFunction(uniq, UInt64)
) ENGINE = AggregatingMergeTree
ORDER BY (day, region);
```
`AggregatingMergeTree` is the engine typically paired with a
materialized view (step 4) to maintain incrementally-updated
aggregates (sums, distinct counts, quantiles) that are far cheaper to
query than recomputing from raw fact rows every time.

### 2. Choose the partition key and ORDER BY key based on real query filters

```sql
CREATE TABLE events (
  event_time DateTime,
  tenant_id  UInt32,
  event_type String,
  payload    String
) ENGINE = MergeTree
PARTITION BY toYYYYMM(event_time)
ORDER BY (tenant_id, event_time);
```
`PARTITION BY` determines which physical directories exist on disk —
partitioning by month (`toYYYYMM`) is a common default for time-series
data, letting old-partition drops (`ALTER TABLE ... DROP PARTITION`) be
an efficient metadata operation rather than a scanning delete. Avoid
over-partitioning (e.g. partitioning by day for a low-volume table, or
including a high-cardinality column in the partition key) — too many
partitions means too many small parts, which increases merge overhead
and can trigger "too many parts" insert errors.

`ORDER BY` (the table's sorting/primary key) determines how efficiently
ClickHouse can skip irrelevant granules during a query — put the column
most commonly used in equality filters first (here, `tenant_id`, since
most queries scope to one tenant), and range-filtered columns
(`event_time`) after it. A query filtering only on a column *not* in
the `ORDER BY` prefix forces a full partition scan regardless of index
presence, since ClickHouse's primary index is a sparse index over the
sort order, not a general-purpose B-tree.

### 3. Set up sharding and replication with ReplicatedMergeTree and Distributed tables

```sql
-- On each replica of a given shard, the local table uses ReplicatedMergeTree
CREATE TABLE events_local ON CLUSTER my_cluster (
  event_time DateTime,
  tenant_id  UInt32,
  event_type String
) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/events', '{replica}')
PARTITION BY toYYYYMM(event_time)
ORDER BY (tenant_id, event_time);

-- A Distributed table on top routes queries/inserts across all shards
CREATE TABLE events ON CLUSTER my_cluster AS events_local
ENGINE = Distributed(my_cluster, default, events_local, rand());
```
`ReplicatedMergeTree` handles replication *within* a shard (every
replica of the same shard stays in sync via the Keeper/ZooKeeper
coordination path); the `Distributed` table engine handles *sharding*
(routing rows across different shards, typically via a hash of some
column, or `rand()` for even distribution with no query-targeting
benefit). Applications generally query and insert against the
`Distributed` table, not the underlying `_local` tables directly —
querying `_local` directly only returns that one node's data, a common
mistake when first setting up a cluster.

### 4. Build materialized views for streaming, incremental aggregation

```sql
CREATE MATERIALIZED VIEW daily_stats_mv
TO daily_stats
AS SELECT
  toDate(event_time) AS day,
  tenant_id,
  sumState(1) AS visits_state
FROM events_local
GROUP BY day, tenant_id;
```
A ClickHouse materialized view is fundamentally a **trigger on
insert**, not a periodically refreshed snapshot: it runs its `SELECT`
against each newly inserted *block* of rows (not the whole table) and
writes the result into the target table. This means a materialized
view only ever sees data inserted after it was created — backfilling
historical data into it requires a separate, explicit `INSERT INTO ...
SELECT` against the target table for the historical range. Query the
resulting aggregate table with the matching `-Merge` combinator to
finalize partial aggregate states:
```sql
SELECT day, tenant_id, sumMerge(visits_state) AS visits
FROM daily_stats GROUP BY day, tenant_id;
```

### 5. Diagnose slow queries and excessive parts

```sql
SELECT query, query_duration_ms, read_rows, read_bytes
FROM system.query_log
WHERE type = 'QueryFinish'
ORDER BY query_duration_ms DESC LIMIT 20;
```
Check `system.parts` for part count and size distribution per table —
a rapidly growing part count with small average part size indicates
inserts are too small/frequent (ClickHouse creates one part per insert
before background merges combine them), which increases both query
overhead (more parts to scan/merge per query) and can eventually hit
the `max_parts_in_total`/"too many parts" insert-rejection safeguard:
```sql
SELECT table, count() AS part_count, sum(rows) AS total_rows
FROM system.parts WHERE active GROUP BY table ORDER BY part_count DESC;
```
The standard fix is batching inserts application-side (hundreds to
thousands of rows per insert statement, not one row per `INSERT`) or
routing through a buffering layer, rather than tuning merge settings to
compensate for a fundamentally too-granular insert pattern.

## Best practices

- Choose the MergeTree variant based on the table's genuine
  update/aggregation semantics, not "MergeTree because it's the
  default" — a table that logically needs deduplication or aggregation
  and uses plain `MergeTree` instead just pushes that complexity into
  every downstream query.
- Batch inserts aggressively (hundreds to thousands of rows per insert)
  — ClickHouse is optimized for large sequential writes, and small,
  frequent inserts are the most common self-inflicted performance and
  stability problem in production ClickHouse deployments.
- Design the `ORDER BY` key around real, dominant query filter patterns
  before the table accumulates significant data — like a MergeTree
  engine choice, this is far more disruptive to change after the fact
  (requiring a full table rewrite) than to get right up front.
- Query `Distributed` tables from applications, never the underlying
  `_local`/`ReplicatedMergeTree` tables directly, unless deliberately
  performing node-local diagnostics.
- Backfill materialized views explicitly for historical data
  immediately after creation — never assume a newly created view
  retroactively covers data already in the source table.
- Monitor `system.parts` part count and `system.mutations` for
  in-progress/stuck mutations as standing health metrics, since both
  degrade gradually and non-obviously until they cause an insert
  rejection or a very slow query.

## Common pitfalls

- **Symptom:** A query against a `ReplacingMergeTree` table returns
  duplicate rows for what should be a unique key.
  **Fix:** Deduplication in `ReplacingMergeTree` happens only during
  background merges, not immediately on insert or on every `SELECT`.
  Use `FINAL` in the query if immediate correctness is required
  (accepting the performance cost), or rely on eventual merge-time
  deduplication only for use cases that can tolerate transient
  duplicates (e.g. a dashboard that's acceptable to be briefly
  approximate).

- **Symptom:** Inserts start failing with "Too many parts" errors
  during a traffic spike.
  **Fix:** The application is issuing many small, frequent `INSERT`
  statements (e.g. one row per HTTP request), creating one part per
  insert faster than background merges can consolidate them. Batch
  inserts application-side or route through a buffering layer
  (application-level batching, or a message queue with a batched
  consumer) so ClickHouse receives large, infrequent inserts instead of
  a high rate of tiny ones.

- **Symptom:** A query filtering on a column that's part of the table's
  schema, and that "should" be fast, still scans the entire partition.
  **Fix:** The filtered column isn't a prefix of the table's `ORDER BY`
  key — ClickHouse's sparse primary index only helps skip granules for
  filters aligned with the sort order, not an arbitrary column.
  Redesign the `ORDER BY` to put the actually-dominant filter column
  first (this requires recreating the table and reinserting data —
  there's no in-place `ORDER BY` change), or add a
  projection/secondary index if changing the primary sort order isn't
  feasible.

- **Symptom:** A materialized view created to capture new aggregated
  data shows no rows, or is missing all data older than its creation
  time.
  **Fix:** This is the intended, if often surprising, semantics of a
  ClickHouse materialized view — it triggers only on newly inserted
  blocks going forward. Explicitly backfill it with a one-time `INSERT
  INTO target_table SELECT ... FROM source_table WHERE <historical
  range>` immediately after creating the view.

- **Symptom:** Someone runs `ALTER TABLE events DELETE WHERE tenant_id =
  X` (a mutation) directly against a large production table expecting
  it to behave like a fast, synchronous `DELETE`.
  **Fix:** ClickHouse mutations are asynchronous background rewrites of
  entire affected parts, not row-level deletes — a mutation against a
  large table can take a long time, consumes significant I/O
  competing with normal merge activity, and cannot be easily rolled
  back once running.
  > **Warning — heavyweight, hard-to-reverse action.** Before running a
  > mutation against a large production table, check `system.mutations`
  > for expected duration/progress on a comparable prior mutation if
  > available, prefer partition-level operations
  > (`ALTER TABLE ... DROP PARTITION`) when the deletion criteria align
  > with partition boundaries (a metadata-only, fast operation instead
  > of a rewriting mutation), and schedule large non-partition-aligned
  > mutations for low-traffic windows.

## Worked example

**Scenario:** An analytics platform ingests ~200M click events/day into
a single-node ClickHouse instance using a plain `MergeTree` table with
one-row-per-request inserts from the application; dashboard queries
filtering by `tenant_id` and a date range have become slow, and inserts
occasionally fail with "too many parts."

1. Diagnose the insert pattern:
   ```sql
   SELECT table, count() FROM system.parts WHERE active GROUP BY table;
   -- events: 48,000 active parts
   ```
   Confirmed the application inserts one row per event synchronously —
   far too granular.
2. Introduce an application-side batching buffer (accumulate 5,000 rows
   or 2 seconds, whichever comes first, then issue one `INSERT`), which
   drops active part count to a few hundred within a day as background
   merges catch up.
3. Redesign the table with `ORDER BY` matching the dashboard's actual
   filter pattern and add sharding/replication ahead of continued growth:
   ```sql
   CREATE TABLE events_local ON CLUSTER my_cluster (
     event_time DateTime, tenant_id UInt32, event_type String
   ) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/events', '{replica}')
   PARTITION BY toYYYYMM(event_time)
   ORDER BY (tenant_id, event_time);

   CREATE TABLE events ON CLUSTER my_cluster AS events_local
   ENGINE = Distributed(my_cluster, default, events_local, rand());
   ```
   Historical data is backfilled shard-by-shard via `INSERT INTO
   events_local SELECT ...` against each shard's data subset.
4. Add an `AggregatingMergeTree`-backed materialized view for the
   dashboard's actual hourly-rollup query shape, backfilled explicitly
   for the existing historical range immediately after creation.
5. Dashboard query latency drops from several seconds (scanning raw
   events) to tens of milliseconds (querying the pre-aggregated rollup
   table), and the "too many parts" insert failures stop recurring
   entirely once batching is in place.

## Cross-references

- [timescaledb-time-series-operations-and-configuration](../timescaledb-time-series-operations-and-configuration/SKILL.md) — a PostgreSQL-extension alternative for time-series workloads, useful as a contrast when deciding between a dedicated OLAP engine and a PostgreSQL-based approach.
- [cloud-data-warehouse-operations-snowflake-bigquery-redshift](../cloud-data-warehouse-operations-snowflake-bigquery-redshift/SKILL.md) — comparable managed-warehouse alternatives when self-hosting/operating a ClickHouse cluster isn't the desired operational trade-off.
- [elasticsearch-opensearch-cluster-operations](../elasticsearch-opensearch-cluster-operations/SKILL.md) — comparable sharded/replicated distributed-cluster operational concerns (shard allocation, replica placement) for a different query workload (search vs. columnar analytics).
