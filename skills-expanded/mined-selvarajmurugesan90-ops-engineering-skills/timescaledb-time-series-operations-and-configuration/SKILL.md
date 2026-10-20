---
name: timescaledb-time-series-operations-and-configuration
description: >
  Covers TimescaleDB as a PostgreSQL extension for time-series workloads:
  hypertable creation and chunk-interval sizing, continuous aggregates
  for pre-computed rollups, and retention/compression policies. Use when
  the user asks to "set up a TimescaleDB hypertable," "size chunk
  intervals," "create a continuous aggregate," "compress old
  time-series data," "set a data retention policy in TimescaleDB," or
  "why is my hypertable query slow."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: database-operations
  maturity: stable
---

# TimescaleDB Time-Series Operations and Configuration

## Purpose

TimescaleDB is a PostgreSQL extension, not a separate database engine —
it adds **hypertables** (transparently partitioned by time, and
optionally by an additional "space" dimension) on top of ordinary
PostgreSQL tables, along with continuous aggregates, compression, and
retention policies purpose-built for time-series workloads (metrics,
events, IoT telemetry, financial ticks). Because it's a normal
PostgreSQL table underneath, everything in
[postgresql-operations-and-performance-tuning](../postgresql-operations-and-performance-tuning/SKILL.md)
(vacuum, replication, connection pooling, `EXPLAIN`-driven index tuning)
still applies unchanged — this skill covers only what's genuinely
different: chunk sizing, continuous aggregates, and compression/
retention policies that a plain PostgreSQL table doesn't have.

## When to use

- Converting a plain table (or designing a new one) for time-series data
  into a hypertable, and choosing a chunk interval.
- Query performance degrades as a hypertable grows, especially queries
  scanning a wide time range or aggregating across many chunks.
- Setting up continuous aggregates to pre-compute rollups (hourly/daily
  averages, downsampled dashboards) instead of aggregating raw data on
  every query.
- Configuring compression for older chunks to reduce storage footprint
  and improve scan performance on cold data.
- Setting a retention policy to automatically drop data past a required
  window (regulatory retention limits, cost control).
- Diagnosing why chunk count has grown unexpectedly large, or why
  compression/retention jobs aren't running as scheduled.

## Prerequisites & environment

- TimescaleDB 2.x on PostgreSQL 13+ assumed for the syntax below —
  continuous aggregates' materialization model changed significantly
  between TimescaleDB 1.x and 2.x (2.x's `CREATE MATERIALIZED VIEW ...
  WITH (timescaledb.continuous)` replaced the older `cagg` API), so
  syntax here is not backward-compatible with 1.x deployments.
- The `timescaledb` extension created in the target database
  (`CREATE EXTENSION IF NOT EXISTS timescaledb;`) — this requires
  superuser or a role with `CREATE` on the database, and
  `shared_preload_libraries` must include `timescaledb` (a restart-
  required `postgresql.conf` change), which should be validated via
  [postgresql-configuration-validation](../postgresql-configuration-validation/SKILL.md)
  before applying to production.
- TimescaleDB's background worker scheduler enabled (default when the
  extension is loaded via `shared_preload_libraries`) for compression
  and retention policies to run automatically — a policy created without
  the scheduler running silently never executes.
- Familiarity with the underlying table's expected write rate and
  retention requirements before choosing a chunk interval — this is the
  single decision hardest to change after data has accumulated across
  many chunks at the wrong size.

## Step-by-step guidance

### 1. Create a hypertable and choose the chunk interval deliberately

```sql
CREATE TABLE metrics (
  time        TIMESTAMPTZ NOT NULL,
  device_id   TEXT NOT NULL,
  cpu_pct     DOUBLE PRECISION,
  mem_bytes   BIGINT
);

SELECT create_hypertable('metrics', by_range('time', INTERVAL '1 day'));
```
The chunk interval controls how much data each underlying physical
partition holds. Too small (e.g. 5 minutes on a low-volume table) creates
excessive per-chunk overhead (each chunk has its own indexes, and
constraint exclusion/chunk-exclusion planning cost grows with chunk
count) — too large (e.g. 30 days on a high-volume table) means each
chunk's indexes and any in-progress compression job operate on data too
large to fit comfortably in `shared_buffers`/`work_mem`, hurting both
query and maintenance performance. A commonly cited operational target
is sizing the interval so that **recent, actively-written chunks fit
within roughly 25% of available RAM** — for a high-ingest metrics table
this often lands in the hours-to-a-day range, while a lower-volume table
might use a week; treat this as a starting heuristic to validate against
your actual per-chunk row count and index size, not a fixed rule.

### 2. Add a space dimension only when a single time dimension isn't enough

For very high cardinality on a secondary key (e.g. millions of distinct
`device_id` values with skewed write volume per device), a second
partitioning dimension can help distribute chunk I/O:
```sql
SELECT add_dimension('metrics', by_hash('device_id', 4));
```
Space partitioning adds real complexity (more chunks per time interval,
more planning overhead for queries that don't filter on the space
dimension) — validate that time-only partitioning with a well-chosen
interval genuinely isn't sufficient before adding a space dimension,
since it's the exception, not the default, for most time-series
workloads.

### 3. Monitor chunk count and per-chunk size, and adjust interval going forward

```sql
SELECT chunk_name, range_start, range_end, is_compressed,
       pg_size_pretty(before_compression_total_bytes) AS raw_size
FROM chunk_compression_stats('metrics');

SELECT hypertable_name, num_chunks FROM timescaledb_information.hypertables;
```
Changing `create_hypertable`'s original chunk interval only affects
**newly created** chunks going forward — existing chunks keep their
original size:
```sql
SELECT set_chunk_time_interval('metrics', INTERVAL '12 hours');
```
There is no built-in way to retroactively re-chunk already-created
chunks other than manually rewriting the data (e.g. exporting and
re-inserting into a hypertable with the corrected interval) — validate
the interval choice against realistic ingest volume *before* the table
accumulates a large number of wrongly-sized chunks, since correcting it
after the fact is a genuinely disruptive data migration, not a
configuration tweak.

### 4. Create continuous aggregates for pre-computed rollups

```sql
CREATE MATERIALIZED VIEW metrics_hourly
WITH (timescaledb.continuous) AS
SELECT device_id,
       time_bucket('1 hour', time) AS bucket,
       avg(cpu_pct) AS avg_cpu,
       max(cpu_pct) AS max_cpu,
       count(*) AS sample_count
FROM metrics
GROUP BY device_id, bucket;
```
A continuous aggregate incrementally materializes rollups as new raw
data arrives, rather than recomputing an aggregate over the full raw
table on every dashboard query. Set a refresh policy so it stays current
without manual intervention:
```sql
SELECT add_continuous_aggregate_policy('metrics_hourly',
  start_offset => INTERVAL '3 days',
  end_offset   => INTERVAL '1 hour',
  schedule_interval => INTERVAL '1 hour');
```
`end_offset` leaves a deliberate gap (here, 1 hour) between "now" and
the most recent bucket the policy will materialize — this accounts for
late-arriving data (a common reality in IoT/metrics ingestion where
devices buffer and batch-send) that would otherwise be missed by a
policy that materializes right up to the current instant. Query the
aggregate directly for dashboards instead of re-aggregating raw data:
```sql
SELECT bucket, avg_cpu FROM metrics_hourly
WHERE device_id = 'device-42' AND bucket > now() - INTERVAL '7 days';
```

### 5. Enable compression for older, no-longer-actively-written chunks

```sql
ALTER TABLE metrics SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'device_id',
  timescaledb.compress_orderby = 'time DESC'
);

SELECT add_compression_policy('metrics', INTERVAL '7 days');
```
Compression converts a chunk's row-oriented storage into a columnar,
compressed representation — typically a large storage reduction for
time-series data with repeating values across columns, at the cost of
compressed chunks being append-only-hostile (an `UPDATE`/`DELETE`
against a compressed chunk triggers automatic, more expensive
decompress-then-modify behavior in current versions). Choose
`compress_segmentby` to match the column(s) most commonly used as an
equality filter (here, `device_id`) so a query filtering on that column
can skip decompressing unrelated segments, and `compress_orderby` to
match the column most commonly range-scanned (typically `time`).
`add_compression_policy` schedules compression automatically once a
chunk's data is older than the given interval — validate that interval
against how long data in this table is still expected to receive
updates/backfills, since compressing chunks that still receive routine
writes creates ongoing decompression overhead rather than a one-time
storage win.

### 6. Set a retention policy to drop data past its required window

```sql
SELECT add_retention_policy('metrics', INTERVAL '90 days');
```
> **Warning — destructive action.** A retention policy **permanently
> drops entire chunks** (not row-by-row deletes) once their data is
> older than the configured interval — this is irreversible without a
> separate backup/archive. Before enabling a retention policy on a
> table with any regulatory or business retention requirement, confirm
> the interval matches the actual required retention window (not just
> "however far back we currently look at"), and confirm any required
> long-term archive (e.g. exporting older chunks to object storage
> before they're dropped) is in place and tested first — see
> [database-backup-and-restore-strategies](../database-backup-and-restore-strategies/SKILL.md)
> for archive/restore-testing discipline. Retention drops whole chunks
> at a time, which is efficient (equivalent to `DROP TABLE` on the
> underlying chunk, not a scanning `DELETE`) but also means the
> granularity of what gets dropped is bounded by chunk interval, not by
> individual rows.

## Best practices

- Choose the initial chunk interval based on a realistic ingest-rate
  estimate and the "recent chunks fit in ~25% of RAM" heuristic before
  the table accumulates data at the wrong size — treat this as the
  single hardest-to-fix decision in this skill, on par with MongoDB
  shard key selection in
  [mongodb-operations-and-scaling](../mongodb-operations-and-scaling/SKILL.md).
- Set `compress_segmentby`/`compress_orderby` to match real query
  filter/sort patterns, not defaults — a mismatched segment-by column
  forces decompression of far more data than a query actually needs.
- Always leave a deliberate `end_offset` gap in continuous aggregate
  refresh policies for workloads with late-arriving data, rather than
  materializing right up to "now" and silently missing late writes.
- Treat retention policies as irreversible, destructive operations
  requiring the same sign-off and archive-before-drop discipline as any
  other data-deletion operation — never enable one on a production
  table without confirming the retention window against actual
  compliance/business requirements first.
- Keep ordinary PostgreSQL operational practice (autovacuum tuning,
  `pg_stat_statements`-driven query analysis, connection pooling)
  applied to the underlying database — a hypertable doesn't exempt the
  instance from anything in
  [postgresql-operations-and-performance-tuning](../postgresql-operations-and-performance-tuning/SKILL.md).
- Monitor background job execution (`timescaledb_information.jobs` and
  `job_stats`) for compression/retention/continuous-aggregate policies —
  a policy that silently stops running (e.g. due to a crashed background
  worker) leaves chunks uncompressed or undropped with no obvious
  application-level symptom until storage costs or query latency
  eventually surface it.

## Common pitfalls

- **Symptom:** Query latency against a hypertable degrades steadily as
  more historical data accumulates, even though queries filter on a
  narrow recent time range.
  **Fix:** The chunk interval is too small, so the query planner must
  perform chunk exclusion across a very large number of chunks even
  though most are irrelevant to the query's actual time range. Check
  `num_chunks` in `timescaledb_information.hypertables`; if it's in the
  thousands for a table only months old, increase
  `set_chunk_time_interval` for future chunks and consider whether
  existing chunks are numerous enough to warrant a one-time data
  migration to a hypertable with a corrected interval.

- **Symptom:** A continuous aggregate's dashboard occasionally shows
  slightly stale or incomplete numbers for the most recent time buckets
  compared to querying raw data directly.
  **Fix:** This is very likely late-arriving raw data landing after the
  continuous aggregate's `end_offset` window already materialized that
  bucket, or a refresh policy schedule interval too coarse for the
  freshness the dashboard needs. Widen `end_offset` to match the
  realistic worst-case data-arrival delay and/or invoke
  `CALL refresh_continuous_aggregate('metrics_hourly', NULL, NULL)`
  manually for a full backfill after confirming late data has settled.

- **Symptom:** Write latency against recent chunks in a table with
  compression enabled spikes unexpectedly.
  **Fix:** The compression policy's interval is compressing chunks that
  are still receiving routine `UPDATE`/backfill writes, triggering
  automatic decompress-then-modify on every touched compressed chunk.
  Push the compression policy's interval further back (only compress
  data confirmed to be past its active-write window) rather than
  compressing aggressively for storage savings alone.

- **Symptom:** Storage usage keeps growing even though a retention
  policy is configured and appears in
  `timescaledb_information.jobs`.
  **Fix:** The job is scheduled but check `job_stats` for its last
  successful run — a crashed background worker, an exception inside the
  job (e.g. a lock conflict with a long-running query on the same
  table), or the scheduler itself not running
  (`timescaledb.max_background_workers` exhausted by other policies)
  can leave a policy silently non-functional. Investigate
  `job_stats.last_run_status` before assuming the interval itself is
  misconfigured.

- **Symptom:** Someone runs `add_retention_policy` with an interval
  shorter than intended (a typo, or a misunderstanding of the required
  compliance window), and older data required for an audit is
  permanently dropped before anyone notices.
  **Fix:** This is an irreversible data-loss event once the policy's
  background job has run — chunks are dropped, not soft-deleted.
  Always review a proposed retention interval against the actual
  documented compliance/business requirement as an explicit sign-off
  step before enabling the policy, and confirm an independent archive
  (exported to object storage, or a separate long-term-retention
  hypertable/database) exists for any data with a real long-term
  retention obligation, tested via a real restore before relying on it.

## Worked example

**Scenario:** An IoT platform ingests ~50M rows/day of per-device
telemetry into a single hypertable created with the extension's default
7-day chunk interval, and dashboard queries aggregating the last 24
hours across 200K devices have become slow as the table has grown to
several billion rows over the past year.

1. Check current chunking: `num_chunks` is only ~52 (7-day chunks over a
   year), but each chunk is enormous (roughly 1B rows) — far above the
   size that comfortably fits recent-chunk indexes in memory.
2. Set a much smaller interval for new chunks matching the actual
   dashboard query pattern (24-hour windows):
   ```sql
   SELECT set_chunk_time_interval('telemetry', INTERVAL '6 hours');
   ```
   Existing oversized chunks are left as-is (no retroactive re-chunking
   available); new chunks going forward are appropriately sized.
3. Add a continuous aggregate for the dashboard's actual query shape
   (hourly per-device rollups) instead of aggregating raw rows on every
   dashboard load:
   ```sql
   CREATE MATERIALIZED VIEW telemetry_hourly
   WITH (timescaledb.continuous) AS
   SELECT device_id, time_bucket('1 hour', time) AS bucket,
          avg(cpu_pct) AS avg_cpu
   FROM telemetry GROUP BY device_id, bucket;

   SELECT add_continuous_aggregate_policy('telemetry_hourly',
     start_offset => INTERVAL '2 days', end_offset => INTERVAL '30 minutes',
     schedule_interval => INTERVAL '30 minutes');
   ```
   Dashboard queries switch to reading `telemetry_hourly` instead of raw
   `telemetry`, dropping typical dashboard query time from several
   seconds to tens of milliseconds.
4. Enable compression for chunks older than 3 days (well past this
   workload's backfill window) segmented by `device_id`:
   ```sql
   ALTER TABLE telemetry SET (timescaledb.compress,
     timescaledb.compress_segmentby = 'device_id',
     timescaledb.compress_orderby = 'time DESC');
   SELECT add_compression_policy('telemetry', INTERVAL '3 days');
   ```
   Storage for the compressed portion of the table drops significantly
   (typical for repetitive telemetry-style columns), and cold-data scan
   performance improves since fewer bytes must be read from disk.
5. Confirm with the compliance team that raw per-reading data is only
   required for 180 days, then add a retention policy after archiving
   older data to object storage and validating a test restore of that
   archive:
   ```sql
   SELECT add_retention_policy('telemetry', INTERVAL '180 days');
   ```

## Cross-references

- [postgresql-operations-and-performance-tuning](../postgresql-operations-and-performance-tuning/SKILL.md) — the underlying PostgreSQL vacuum, replication, and query-tuning practice that still applies unchanged to a hypertable's constituent chunk tables.
- [postgresql-configuration-validation](../postgresql-configuration-validation/SKILL.md) — validates the `shared_preload_libraries`/memory settings change required to enable the TimescaleDB extension before it reaches production.
- [clickhouse-analytical-database-operations](../clickhouse-analytical-database-operations/SKILL.md) — a purpose-built OLAP alternative for time-series/analytical workloads when a PostgreSQL-based extension no longer scales for the required ingest rate or query concurrency.
- [database-backup-and-restore-strategies](../database-backup-and-restore-strategies/SKILL.md) — archive-before-drop discipline for data that a TimescaleDB retention policy would otherwise permanently delete.
