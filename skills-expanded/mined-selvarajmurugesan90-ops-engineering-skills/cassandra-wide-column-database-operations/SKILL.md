---
name: cassandra-wide-column-database-operations
description: >
  Covers Apache Cassandra ring topology and token/partition design,
  tunable consistency levels (ONE, QUORUM, ALL, LOCAL_QUORUM),
  compaction strategy selection (SizeTiered, Leveled, TimeWindow), and
  tombstone/GC-grace management. Use when the user asks to "design a
  Cassandra partition key," "choose a Cassandra consistency level,"
  "why is this Cassandra query slow," "pick a compaction strategy,"
  "Cassandra tombstone warnings in logs," or "add/remove a node from a
  Cassandra ring."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: database-operations
  maturity: stable
---

# Cassandra Wide-Column Database Operations

## Purpose

Cassandra's defining architectural choice — a masterless ring where
every node is structurally equal, data is distributed by consistent
hashing of the partition key, and consistency is tunable per query
rather than fixed by the engine — trades the strong consistency
guarantees of a single-primary database for horizontal write
scalability and no single point of failure. That trade only pays off
operationally if the partition key is chosen well (a bad choice creates
a hot partition the ring can't help with), the consistency level
matches the actual durability/availability requirement per query, and
compaction strategy matches the write pattern. This skill covers ring
topology and token design, consistency-level selection, and compaction/
tombstone management — the recurring operational decisions that
determine whether a Cassandra cluster stays healthy as it scales.

## When to use

- Designing a new table's partition key and clustering columns, or
  diagnosing an existing "hot partition" causing uneven node load.
- Choosing a consistency level for a specific read/write path (balancing
  latency/availability against consistency guarantees).
- Selecting or changing a table's compaction strategy
  (SizeTieredCompactionStrategy, LeveledCompactionStrategy,
  TimeWindowCompactionStrategy) to match its write/delete pattern.
- Tombstone-related warnings in logs (`ReadTimeoutException` mentioning
  tombstones, or a "tombstone_warn_threshold" log message) or overall
  read performance degrading over time on a table with regular deletes/
  TTLs.
- Adding, removing, or replacing a node in the ring, or diagnosing an
  uneven token/data distribution across nodes.
- Deciding on and validating a replication factor and rack/datacenter
  topology for a new keyspace.

## Prerequisites & environment

- Apache Cassandra 4.x assumed for the syntax below (the `nodetool`
  command surface and virtual tables referenced here are stable across
  most of the 3.x/4.x line, but note that vnodes — virtual nodes,
  multiple token ranges per physical node — have been the default since
  Cassandra 2.x, and choosing `num_tokens` deliberately still matters
  for cluster balance at small node counts).
- `nodetool` access on each node (local or via JMX) for ring, repair,
  and compaction administration — this typically requires host access
  or JMX credentials, not just CQL client access.
- A replication factor and `NetworkTopologyStrategy` keyspace
  configuration appropriate to the deployment's rack/datacenter
  layout — `SimpleStrategy` (rack/DC-unaware) is only appropriate for a
  single-datacenter test/dev cluster, never production.
- Familiarity with the actual query patterns a table will serve
  **before** creating it — unlike a relational schema, a Cassandra table
  design is driven by "what queries will read this data," since
  Cassandra has no general-purpose secondary-index-driven ad hoc query
  capability comparable to a relational engine's optimizer.

## Step-by-step guidance

### 1. Design the partition key around the actual query pattern, not the entity model

```sql
CREATE TABLE sensor_readings (
  device_id   UUID,
  reading_day DATE,
  reading_ts  TIMESTAMP,
  value       DOUBLE,
  PRIMARY KEY ((device_id, reading_day), reading_ts)
) WITH CLUSTERING ORDER BY (reading_ts DESC);
```
The **partition key** (`(device_id, reading_day)` here — a composite
key) determines which physical node(s) hold a given row via consistent
hashing of the key's hash into the ring's token range; the
**clustering columns** (`reading_ts`) determine sort order *within* a
partition, not distribution across the ring. A partition key that's
too broad (e.g. `device_id` alone for a high-volume sensor generating
years of readings) creates an ever-growing partition that eventually
becomes a genuine hotspot — one node handles disproportionate
read/write/compaction load for that key, and Cassandra's ring can't
help since that key hashes to one place regardless of cluster size.
Including `reading_day` bounds each partition to one day's readings for
one device, keeping partition size manageable indefinitely as time
passes, at the cost of queries spanning multiple days needing multiple
partition reads (an explicit, deliberate trade — not a defect).

### 2. Choose a consistency level per query, matching the actual requirement — not one global default

```sql
CONSISTENCY LOCAL_QUORUM;
SELECT * FROM sensor_readings WHERE device_id = <ID> AND reading_day = '2026-07-28';
```
Consistency level determines how many replicas must respond before a
read/write is acknowledged, out of the keyspace's configured
replication factor (RF):
- `ONE` — fastest, lowest availability requirement (any single replica
  answers), weakest consistency (can read stale data if the responding
  replica hasn't yet received the latest write).
- `QUORUM` — a strict majority of **all** replicas across **all**
  datacenters must respond; `LOCAL_QUORUM` requires a majority only
  within the local datacenter, avoiding cross-DC latency for
  multi-region deployments while still giving strong-enough consistency
  for most application needs.
- `ALL` — every replica must respond; strongest consistency, but
  availability drops to zero the moment even one replica holding that
  partition is unreachable — appropriate only for narrow cases where
  that trade is genuinely acceptable, essentially never as a default.
`R + W > RF` (read consistency level's replica count plus write
consistency level's replica count exceeding the replication factor)
is the classic condition for **strong** consistency on a given
read-after-write path — e.g. `QUORUM` writes plus `QUORUM` reads at
RF=3 (`2 + 2 > 3`) guarantees a read sees the latest acknowledged
write, at the cost of both operations needing a majority of replicas
available. `LOCAL_ONE` writes plus `LOCAL_ONE` reads does not give
that guarantee and should only be chosen for data where eventual
consistency is genuinely acceptable (e.g. non-critical telemetry,
idempotent counters with independent reconciliation).

### 3. Choose a compaction strategy matching the table's write/delete pattern

Cassandra is an LSM-tree-based engine: writes go to an in-memory
memtable, flushed periodically to immutable on-disk SSTables, which
**compaction** periodically merges to reclaim space from overwrites/
deletes and reduce the number of SSTables a read must check.
```sql
-- Default, general-purpose: good for write-heavy workloads with
-- moderate read amplification tolerance
ALTER TABLE sensor_readings WITH compaction =
  {'class': 'SizeTieredCompactionStrategy'};

-- Better read latency at the cost of more compaction I/O: good for
-- read-heavy workloads that can't tolerate SizeTiered's read amplification
ALTER TABLE user_profiles WITH compaction =
  {'class': 'LeveledCompactionStrategy'};

-- Purpose-built for time-series data with a natural TTL/expiry pattern
ALTER TABLE sensor_readings WITH compaction =
  {'class': 'TimeWindowCompactionStrategy', 'compaction_window_unit': 'DAYS', 'compaction_window_size': 1};
```
`TimeWindowCompactionStrategy` (TWCS) groups SSTables by time window and
compacts within a window only, never across windows — this makes
dropping expired data (via TTL) extremely cheap, since an entire
SSTable whose data has all aged past its TTL can simply be dropped
rather than compacted/rewritten. Choose TWCS for genuinely time-series,
mostly-append, TTL-expiring data (matching the window size to the TTL
and write rate); choose it incorrectly for a table with out-of-window
updates/deletes and it performs worse than SizeTiered, since data
correction across windows defeats TWCS's core assumption.

### 4. Manage tombstones and GC grace period deliberately

A `DELETE` (or a TTL expiry) in Cassandra doesn't immediately remove
data — it writes a **tombstone** marker that must persist until
`gc_grace_seconds` (default 10 days) has passed *and* a repair has run,
so that a tombstone isn't garbage-collected on one replica before
other, possibly-behind replicas have received it (which would cause a
deleted row to "resurrect" on those replicas). A read that must skip
over many tombstones to find live data is slow and can trigger
`tombstone_failure_threshold`:
```sql
SELECT * FROM events WHERE partition_key = <KEY>;
-- WARN: Read 1500 live and 8500 tombstoned cells in events
```
This is a strong signal of a query pattern that deletes/overwrites
heavily within a partition that's also read frequently (a common
anti-pattern: using Cassandra as a queue, where consumed rows are
deleted but the partition is still scanned). Redesign the data model
(e.g. bucket by time window so consumed/old buckets are simply not
queried rather than deleted row-by-row) rather than only tuning
`gc_grace_seconds` down, since lowering it without ensuring repairs run
frequently enough within the new, shorter window risks the exact
resurrection problem it exists to prevent.

### 5. Add, remove, or replace a node in the ring

```bash
# Check current ring token ownership and load balance
nodetool status
nodetool ring
```
Adding a node with `auto_bootstrap: true` (default) streams a share of
existing data to it from current owners of the token ranges it takes
over — this is I/O- and network-intensive and should be done one node
at a time, monitoring `nodetool netstats` for streaming progress, never
multiple nodes joining concurrently in a way that could leave overlapping
token ranges under-replicated during the transition.
```bash
nodetool decommission   # run on the node being removed — streams its data OUT to remaining owners first
```
> **Warning — destructive if done out of order.** Never simply stop and
> remove a node's process/host without running `nodetool decommission`
> first (or, if the node is already dead,
> `nodetool removenode` from a surviving node) — skipping this step
> means the data that node owned is not streamed anywhere first, and if
> the replication factor doesn't cover the loss adequately at that
> moment, that data is gone. Always run `nodetool repair` on the
> affected token ranges afterward to confirm replica consistency.

## Best practices

- Design partition keys to bound growth (a natural bucketing dimension
  like a time window, matching this repo's guidance for MongoDB shard
  keys in
  [mongodb-operations-and-scaling](../mongodb-operations-and-scaling/SKILL.md))
  rather than an unbounded, ever-growing key — this is the single
  hardest decision to fix after data has accumulated.
- Use `NetworkTopologyStrategy` with an explicit per-datacenter
  replication factor for every production keyspace — never
  `SimpleStrategy` outside of local development.
- Choose consistency level per query based on the actual
  consistency/availability trade the specific read or write path needs,
  not one blanket setting for the whole application — a write path that
  needs durability guarantees and a read path that's fine with eventual
  consistency are not the same decision.
- Match compaction strategy to write/delete pattern deliberately:
  SizeTiered as a reasonable general default, Leveled for read-heavy
  low-write-amplification-tolerance tables, TimeWindow for genuinely
  time-series TTL-expiring data.
- Run scheduled, regular repairs (`nodetool repair`, or an automated
  repair scheduler) within the `gc_grace_seconds` window on every
  table with deletes/TTLs — a missed repair window is what turns a
  routine tombstone GC into a data-resurrection bug.
- Always `nodetool decommission` a node being removed (never just stop
  the process), and add/remove nodes to a live cluster strictly one at
  a time, monitoring streaming progress before proceeding to the next.

## Common pitfalls

- **Symptom:** One node in the ring consistently shows much higher
  CPU/disk I/O and larger data size than others, and it worsens over
  time.
  **Fix:** The partition key is unbounded (e.g. a single `device_id`
  with years of accumulating data, no time-bucketing dimension),
  concentrating an ever-growing amount of data and read/write/compaction
  load onto whichever node(s) own that key's token range — the ring
  can't rebalance a hot single key regardless of node count. Redesign
  the partition key to include a bounding dimension (a time bucket, a
  shard suffix) so no single partition grows unbounded.

- **Symptom:** Reads against a table with regular deletes/TTL expiry
  slow down progressively, and logs show tombstone warning/failure
  threshold messages.
  **Fix:** The query pattern reads across many tombstoned cells to find
  live data — usually from deleting/expiring rows within a partition
  that's still scanned as a whole. Redesign the data model to bucket by
  time so expired data ages out of the query's scope entirely (never
  queried, not deleted-then-skipped), and confirm regular repairs run
  within `gc_grace_seconds` rather than only lowering the threshold.

- **Symptom:** A `DELETE`d row reappears ("resurrects") after some time,
  with no application code writing it back.
  **Fix:** A replica missed the tombstone (was down or partitioned
  during the delete) and its stale, pre-delete data was never
  reconciled by a repair before `gc_grace_seconds` elapsed and the
  tombstone was garbage-collected on other replicas — that stale
  replica's old data can then "win" on a subsequent read. Run
  `nodetool repair` regularly and comfortably within the
  `gc_grace_seconds` window (not just when convenient), and treat a
  missed repair window on a table with active deletes as an urgent gap
  to close, not routine maintenance debt.

- **Symptom:** After adding new nodes to the cluster, data distribution
  across nodes remains uneven despite `nodetool status` showing roughly
  equal `Owns` percentages.
  **Fix:** Even token ownership doesn't guarantee even data size if the
  partition key distribution itself is skewed (some partitions are much
  larger than others) — token-range ownership balance and actual data
  volume balance are related but distinct. Investigate partition size
  distribution (`nodetool tablehistograms`) rather than assuming ring
  rebalancing alone will fix a skewed-key-driven imbalance.

- **Symptom:** Someone runs `TRUNCATE` on a table, or `DROP KEYSPACE`,
  directly against production to "reset" data during an incident.
  **Fix:** Both are immediately destructive, cluster-wide operations —
  `TRUNCATE` in particular also forces a table-wide snapshot on all
  nodes by default (which is itself an I/O-heavy operation across the
  whole cluster) and cannot be undone via CQL.
  > **Warning — destructive action.** Never run `TRUNCATE`/`DROP
  > KEYSPACE` against a shared or production cluster without an
  > independently confirmed target and a verified, tested backup/snapshot
  > restore path (see
  > [database-backup-and-restore-strategies](../database-backup-and-restore-strategies/SKILL.md)),
  > and restrict these operations via role-based access control to a
  > narrow admin role rather than general application credentials.

## Worked example

**Scenario:** An IoT platform's `sensor_readings` table
(`PRIMARY KEY (device_id, reading_ts)`, unbounded partition key) has
been running for two years; one specific high-frequency industrial
sensor's node consistently shows 3x the disk I/O and query latency of
its peers, and read latency for that sensor's dashboard has degraded
noticeably.

1. Confirm the hot-partition hypothesis:
   ```bash
   nodetool tablehistograms keyspace.sensor_readings
   ```
   Shows a partition size distribution with a long tail — the
   affected sensor's partition (two years of readings, no bucketing) is
   orders of magnitude larger than the median partition.
2. Redesign the table with a bounded partition key (daily buckets, as
   in step 1 of the guidance above):
   ```sql
   CREATE TABLE sensor_readings_v2 (
     device_id UUID, reading_day DATE, reading_ts TIMESTAMP, value DOUBLE,
     PRIMARY KEY ((device_id, reading_day), reading_ts)
   ) WITH CLUSTERING ORDER BY (reading_ts DESC)
   AND compaction = {'class': 'TimeWindowCompactionStrategy', 'compaction_window_unit': 'DAYS', 'compaction_window_size': 1};
   ```
3. Dual-write to both tables from the ingestion pipeline during a
   migration window, backfill historical data into `sensor_readings_v2`
   bucketed by day, then cut reads over once backfill is verified
   complete for all devices.
4. Set a TTL matching the platform's actual required retention (say, 13
   months) on new writes to `sensor_readings_v2`, letting
   TimeWindowCompactionStrategy drop entire expired daily SSTables
   cheaply instead of accumulating tombstones from manual deletes.
5. Schedule regular `nodetool repair` runs comfortably within
   `gc_grace_seconds`, and monitor `nodetool tablehistograms` monthly
   for partition-size skew as a standing health check going forward,
   catching the next hot-partition trend before it's user-visible.

## Cross-references

- [mongodb-operations-and-scaling](../mongodb-operations-and-scaling/SKILL.md) — comparable partition/shard-key design trade-offs (monotonic/unbounded keys creating hotspots) in a document-oriented distributed database, useful as a direct conceptual parallel.
- [database-backup-and-restore-strategies](../database-backup-and-restore-strategies/SKILL.md) — snapshot/restore tooling and testing discipline that should back up any destructive operation (`TRUNCATE`, `DROP KEYSPACE`, a failed node removal) against a Cassandra cluster.
- [elasticsearch-opensearch-cluster-operations](../elasticsearch-opensearch-cluster-operations/SKILL.md) — comparable distributed-cluster shard placement and rebalancing operational concerns for a different (search-oriented) data model.
