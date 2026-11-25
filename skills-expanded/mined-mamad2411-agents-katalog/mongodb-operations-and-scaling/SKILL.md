---
name: mongodb-operations-and-scaling
description: >
  Covers MongoDB replica set operations, sharding design (shard key
  selection, chunk balancing), index tuning, and routine operational
  maintenance (compaction, oplog sizing, election tuning). Use when the
  user asks to "set up MongoDB sharding," "pick a shard key," "why is
  this MongoDB query slow," "resize the oplog," "add a replica set
  member," or "MongoDB is rebalancing chunks unevenly."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: database-operations
  maturity: stable
---

# MongoDB Operations and Scaling

## Purpose

MongoDB's replica-set and sharding architecture makes horizontal scaling
and automatic failover a built-in capability rather than a bolted-on
add-on, but that capability only holds up operationally if the shard key
is chosen well, indexes match real query patterns, and the replica set's
election and oplog settings match the workload's write volume and
network reality. A bad shard key choice in particular is expensive to
fix after the fact (it requires resharding or a full data migration in
older versions), which makes it the single highest-leverage decision in
this skill. This skill covers replica sets, sharding, index tuning, and
day-2 maintenance; for validating a proposed replica-set or sharding
config change before it reaches production, see
[mongodb-configuration-validation](../mongodb-configuration-validation/SKILL.md).

## When to use

- Standing up or scaling a sharded cluster, and specifically choosing a
  shard key for a new or existing collection.
- A replica set needs a member added/removed, or elections are firing
  more often than expected (flapping primary).
- Diagnosing a slow query with `explain()` and deciding what index (or
  index change) fixes it.
- The oplog window is too short (replicas fall behind and can't resume
  without a full resync) or chunk migrations are creating uneven load
  ("jumbo chunks," a hot shard).
- Routine maintenance: compaction after heavy delete volume, reviewing
  `mongostat`/`mongotop` output, or planning a `mongodump`/`mongorestore`
  operation.

## Prerequisites & environment

- MongoDB 5.0+ assumed for the guidance and syntax below (the
  aggregation-based `explain()` output shape and `$merge`/sharding
  behavior referenced here matches 5.0+; call out explicitly where
  older-version behavior differs, e.g. pre-4.4 resharding required a
  full manual migration rather than the `reshardCollection` command).
- A replica set (minimum 3 voting members for real fault tolerance — a
  2-member set plus arbiter is a common budget compromise but has weaker
  guarantees, covered in the config-validation skill) already
  initialized, or a sharded cluster with config servers and `mongos`
  routers already deployed.
- `clusterAdmin` or `dbAdmin` role for index and sharding operations;
  `clusterMonitor` is sufficient for read-only diagnostics
  (`rs.status()`, `sh.status()`, `db.collection.stats()`).
- For sharding: config server replica set (3 members minimum) already
  running, and at least one `mongos` router reachable by applications.

## Step-by-step guidance

### 1. Choose a shard key deliberately — this is the decision hardest to undo

A shard key determines how documents distribute across shards, and a
poor choice produces one of two failure patterns: a **monotonically
increasing key** (e.g. `_id` default ObjectId, or a timestamp) sends all
new writes to whichever shard currently owns the highest chunk range,
making that shard a permanent write hotspot; a **low-cardinality key**
(e.g. a `status` field with 3 possible values) can't split into more
chunks than it has distinct values, capping how far the collection can
scale out regardless of shard count. Prefer a compound shard key with
good cardinality and write distribution, often a hashed key for pure
write-distribution or a compound `{ tenant_id: 1, created_at: 1 }` style
key when queries commonly filter by the leading field (so `mongos` can
target specific shards instead of broadcasting every query to all of
them):
```js
// Hashed sharding — best write distribution, but ranged queries broadcast to all shards
sh.shardCollection("app.events", { deviceId: "hashed" });

// Ranged/compound — preserves query targeting if queries commonly filter by tenantId
sh.shardCollection("app.orders", { tenantId: 1, orderId: 1 });
```
For MongoDB 4.4+, `reshardCollection` allows changing a shard key after
the fact without a fully manual migration, but it still reshuffles the
entire collection's data and should be planned as a significant,
maintenance-window operation, not a quick fix — validate the shard key
choice thoroughly before initial rollout rather than counting on easy
resharding later.

### 2. Monitor chunk distribution and catch "jumbo chunks" early

```js
sh.status()
```
Look for chunk count imbalance across shards and any chunk flagged
`jumbo: true` — a jumbo chunk exceeds the configured chunk size
(default 128MB) but can't be split further, usually because its shard
key range maps to too few distinct key values (a low-cardinality shard
key symptom) or too many documents share the exact same shard key value.
A jumbo chunk can't be migrated by the balancer, which means it (and the
data it holds) is permanently stuck on its current shard, defeating the
purpose of sharding for that data. Investigate the shard key's real-world
cardinality distribution before it produces jumbo chunks at scale.

### 3. Configure and monitor replica set elections

```js
rs.status()
```
Check each member's `stateStr` (`PRIMARY`, `SECONDARY`, `ARBITER`) and
`health`. Frequent unexpected elections ("flapping primary") are usually
caused by network latency/instability between members exceeding the
election timeout, or a member under heavy load failing to send
heartbeats in time — check:
```js
rs.config().settings.electionTimeoutMillis   // default 10000
```
Raising `electionTimeoutMillis` trades slower failover (longer time to
notice a genuinely dead primary) for more tolerance of transient network
blips — tune it based on measured real inter-member latency and jitter,
not a guess. For geographically distributed replica sets, set member
`priority` explicitly so elections prefer a same-region member over one
across a high-latency link:
```js
cfg = rs.conf()
cfg.members[2].priority = 0.5   // deprioritize a cross-region member
rs.reconfig(cfg)
```

### 4. Size the oplog for the real write volume and expected maintenance windows

```js
db.oplog.rs.stats()   // check maxSize and current window via first/last timestamp
```
The oplog is a capped collection — once full, the oldest entries are
overwritten, and a secondary offline longer than the oplog's time window
cannot resume replication; it needs a full resync (`rs.syncFrom()` after
wiping its data, or restoring from a recent backup). Size the oplog for
the longest realistic planned-maintenance window (not just steady-state
write volume) on the highest-write-volume period, with margin:
```js
db.adminCommand({ replSetResizeOplog: 1, size: 20480 })   // MB
```

### 5. Diagnose a slow query with `explain()` before guessing at an index

```js
db.orders.find({ customerId: 42, status: "pending" }).explain("executionStats")
```
Check `executionStats.executionStages.stage` — `COLLSCAN` means a full
collection scan; compare `totalDocsExamined` against `nReturned` — a
large ratio between them means an index would help even if a `COLLSCAN`
isn't shown (e.g. an index exists but doesn't match the query's actual
filter/sort combination, forcing an `IXSCAN` followed by heavy
in-memory filtering). Create a compound index matching the filter and
any sort:
```js
db.orders.createIndex({ customerId: 1, status: 1 }, { background: true })
```
`background: true` (or, in modern MongoDB, the default online index
build behavior) avoids blocking reads/writes for the whole build — always
prefer it on a live collection, equivalent in intent to PostgreSQL's
`CREATE INDEX CONCURRENTLY`.

### 6. Routine maintenance: compaction and storage reclamation

After heavy delete volume, WiredTiger doesn't automatically return
freed disk space to the OS — check actual vs. allocated size:
```js
db.orders.stats().storageSize   // allocated
db.orders.stats().size          // actual data
```
```js
db.runCommand({ compact: "orders" })
```
`compact` blocks other operations on that collection for its duration on
most storage engine versions (check current behavior for your specific
MongoDB version, since this has improved but is still not fully
lock-free) — schedule it in a low-traffic window, and on a replica set
run it against secondaries one at a time (stepping each out of the read
path first) rather than the primary, to avoid a foreground availability
impact.

## Best practices

- Choose the shard key based on actual query patterns and write
  distribution requirements measured against real or realistically
  synthetic data, not convenience — treat shard key selection as a
  one-time, high-stakes design decision, not something to iterate on
  casually in production.
- Keep the oplog sized for your worst realistic maintenance window, not
  average write volume — recovering a secondary via full resync under
  time pressure is far more disruptive than the extra disk space an
  appropriately sized oplog costs.
- Always build indexes online/in the background on live collections, and
  build them on a rolling basis (secondaries first, stepped out of the
  read path, then primary) for large collections rather than
  foreground-blocking the primary.
- Set replica set member `priority` and `votes` deliberately for
  cross-region topologies — don't leave every member at the default
  priority when some are meant to be failover-only, and keep total
  voting members odd to avoid election ties.
- Monitor `sh.status()` chunk distribution and jumbo chunk count as a
  standing health check, not just when a hotspot is already
  user-visible — a shard key trending toward imbalance is much cheaper
  to address before jumbo chunks accumulate.

## Common pitfalls

- **Symptom:** One shard consistently shows much higher CPU/disk I/O
  than the others, and it keeps getting worse as the collection grows.
  **Fix:** The shard key is monotonically increasing (default `_id`
  ObjectId or a timestamp-based key), sending all new writes to
  whichever shard owns the current top of the range. Consider a hashed
  shard key for write-heavy, low-query-targeting-benefit collections, or
  `reshardCollection` (4.4+) to a better key — planned as a real
  maintenance operation, not a quick config flip.

- **Symptom:** `sh.status()` shows a chunk flagged `jumbo: true` that
  never gets migrated or split, and that shard's data keeps growing
  disproportionately.
  **Fix:** The shard key's cardinality is too low for that key range to
  split further (too many documents share the same or a narrow set of
  shard key values). This requires addressing the shard key design
  itself (a compound key with a higher-cardinality trailing field, or
  reconsidering the leading field) — a jumbo chunk cannot be fixed by
  balancer settings alone.

- **Symptom:** The primary steps down and a new election happens
  every few minutes, with no actual hardware/network failure that ops
  can see.
  **Fix:** `electionTimeoutMillis` (default 10s) is too aggressive for
  the real inter-member network latency/jitter, or the primary is
  periodically too loaded (e.g. a long-running query or backup holding
  a lock) to send heartbeats in time. Measure real inter-member latency,
  raise the timeout if warranted, and check for foreground operations
  that starve the primary's heartbeat thread.

- **Symptom:** A secondary that was offline for a maintenance window
  comes back and immediately drops into `RECOVERING` state, needing a
  full resync instead of catching up.
  **Fix:** The offline window exceeded the oplog's retention window (the
  oldest entry the secondary needs to resume from has already been
  overwritten). Resize the oplog for realistic maintenance windows
  (`replSetResizeOplog`) going forward, and for this instance either
  restore from a recent backup and let it catch up from there, or accept
  the full initial sync — do not repeatedly retry `rs.syncFrom()` hoping
  it resolves itself, since a gap past the oplog window cannot self-heal.

- **Symptom:** Someone runs `db.dropDatabase()` or a broad
  `deleteMany({})` directly against production to "clean up test data,"
  with no prior backup and no `--dry-run` equivalent step.
  **Fix:** This is a destructive, irreversible action against
  production. Always take a verified backup (or confirm point-in-time
  recovery via oplog is available) before any bulk delete/drop, run the
  equivalent read-only query first (`countDocuments` with the same
  filter) to confirm scope matches intent, and restrict
  `dropDatabase`/collection-drop privileges to a narrow admin role
  rather than general application credentials.

## Worked example

**Scenario:** An `events` collection (500M+ documents, IoT device
telemetry) needs to be sharded ahead of an expected 5x traffic increase;
current writes use MongoDB's default `_id` ObjectId as the effective
insertion order.

1. Analyze query patterns: the dominant query is
   `db.events.find({ deviceId: X, timestamp: { $gte: ..., $lte: ... } })`
   — filtering by a specific device's recent events, not cross-device
   scans.
2. Reject a monotonic key (timestamp alone) — it would concentrate all
   new writes on one shard. Reject pure `deviceId` hashed sharding alone
   too quickly — check cardinality first: with 200K distinct devices,
   cardinality is high enough for good distribution.
3. Choose a compound key preserving query targeting:
   ```js
   sh.shardCollection("app.events", { deviceId: 1, timestamp: 1 });
   ```
   This distributes writes across shards by `deviceId` (good
   cardinality, not monotonic) while keeping each device's events
   colocated and sorted, so the common per-device time-range query
   targets a single shard instead of broadcasting to all of them.
4. Pre-split chunks ahead of the traffic increase rather than waiting for
   the balancer to react under load:
   ```js
   sh.splitAt("app.events", { deviceId: MinKey, timestamp: MinKey })
   ```
   repeated at calculated boundaries based on expected device ID
   distribution.
5. Monitor `sh.status()` weekly during the ramp-up for chunk balance and
   jumbo chunks; none observed since `deviceId` cardinality is high.
6. Size the oplog on each shard's replica set for the new, higher write
   volume's worst-case maintenance window (`replSetResizeOplog`), since
   the 5x traffic increase would otherwise shrink the effective oplog
   time window by roughly the same factor.

## Cross-references

- [mongodb-configuration-validation](../mongodb-configuration-validation/SKILL.md) — validates a proposed shard key, replica set member config, or index change against production impact before rollout, complementing the operational guidance here.
- [redis-operations-and-cluster-management](../redis-operations-and-cluster-management/SKILL.md) — comparable cluster-topology and resharding concerns (hash slots vs. shard keys) if MongoDB and Redis Cluster are both in the same platform.
- [database-schema-migration-with-liquibase-and-flyway](../database-schema-migration-with-liquibase-and-flyway/SKILL.md) — for schema-adjacent changes in a hybrid stack; MongoDB itself is schemaless but index/shard-key changes should still go through a tracked, reviewed change process similar to migrations there.
