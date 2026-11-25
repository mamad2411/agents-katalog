---
name: redis-operations-and-cluster-management
description: >
  Covers Redis persistence (RDB snapshots, AOF with rewrite), Redis
  Cluster topology (hash slots, resharding, replica failover), Sentinel-
  based HA for non-clustered deployments, and memory management
  (maxmemory, eviction policy interaction with persistence and
  replication). Use when the user asks to "set up Redis Cluster," "why
  did my Redis replica fail over," "configure RDB vs AOF persistence,"
  "reshard Redis hash slots," "Redis is evicting keys unexpectedly," or
  "size Redis memory for production."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: database-operations
  maturity: stable
---

# Redis Operations and Cluster Management

## Purpose

Redis is an in-memory data store first — every operational decision
(persistence mode, cluster topology, memory limits) is really a decision
about what happens when a process restarts, a node dies, or memory fills
up, since none of those are free consequences of "just using Redis" the
way they might be with a disk-native database. This skill covers the
operational core: persistence (RDB snapshots vs. AOF append-only
logging, and running both together), Redis Cluster's hash-slot sharding
and failover mechanics, Sentinel as the alternative HA mechanism for
non-clustered deployments, and memory management under `maxmemory` and
eviction policies. It is deliberately scoped to infrastructure/topology
operations — for validating a proposed `maxmemory`/eviction/cluster
config before it's relied on in production, see
[redis-configuration-validation](../redis-configuration-validation/SKILL.md);
for the application-facing question of *how* to use Redis as a cache
(cache-aside vs. write-through, TTL strategy, invalidation), see
[redis-caching-strategy-and-invalidation-patterns](../redis-caching-strategy-and-invalidation-patterns/SKILL.md),
which is a distinct concern from the cluster/persistence mechanics here.

## When to use

- Standing up or troubleshooting Redis Cluster: hash slot assignment,
  adding/removing shards, resharding, or a cluster stuck in a `fail`
  state.
- Choosing or troubleshooting persistence: deciding between RDB-only,
  AOF-only, or both, or diagnosing data loss after a restart/crash that
  shouldn't have happened given the configured persistence.
- A replica failed to take over automatically after a primary died (in
  Cluster mode or with Sentinel), or failover took much longer than
  expected.
- Redis is evicting keys or returning `OOM command not allowed` errors,
  and the cause isn't obvious from `maxmemory` alone.
- Planning capacity: sizing `maxmemory` per node, deciding shard count
  for a cluster, or estimating memory overhead of a specific data
  structure choice at scale.
- Rebalancing an unevenly-loaded cluster (a hot shard, uneven hash slot
  distribution) or migrating slots off a node being decommissioned.

## Prerequisites & environment

- Redis 6.2+ assumed for the guidance and command syntax below;
  Redis Cluster's core hash-slot mechanics have been stable since
  Cluster's introduction in Redis 3.0, but ACL-related cluster commands
  and some `CLUSTER` subcommand output shapes assume 6+. Call out
  explicitly where a feature needs a specific newer version (e.g.
  `CLUSTER SHARDS` replacing the older `CLUSTER SLOTS` output shape is
  7.0+).
- For Cluster mode: a minimum of 3 primary nodes (Redis Cluster requires
  at least 3 primaries to form a cluster and reach quorum on slot
  ownership), each ideally with at least one replica for automatic
  failover — a 3-primary, 0-replica cluster survives no primary failure
  without manual intervention.
- For Sentinel-based HA (non-clustered, single-primary-with-replicas
  topology): a minimum of 3 Sentinel processes across independent
  failure domains, since Sentinel's own failover decision requires a
  quorum vote among Sentinels, not just one Sentinel's opinion.
- `redis-cli` and (for cluster operations) `redis-cli --cluster` support
  compiled in, or the standalone `redis-trib.rb` on older (pre-5.0)
  versions where the cluster helper wasn't yet folded into `redis-cli`.
- Enough disk space on each node for RDB snapshots and/or the AOF file
  (plus headroom during `BGREWRITEAOF`, which briefly holds both old and
  new AOF content) — sized independently from the `maxmemory` RAM
  budget.

## Step-by-step guidance

### 1. Choose a persistence strategy deliberately, not by default

Redis offers two independent, combinable mechanisms:
- **RDB** — point-in-time binary snapshots, taken on a schedule
  (`save 900 1` etc.) or on demand (`BGSAVE`). Fast to load on restart,
  compact on disk, but loses everything since the last snapshot on a
  crash.
- **AOF** — an append-only log of write commands, replayed on restart.
  Configurable durability via `appendfsync`:
  ```
  appendonly yes
  appendfsync everysec   # fsync once per second — default, small (~1s) loss window
  # appendfsync always   # fsync every write — near-zero loss, materially slower
  # appendfsync no       # let the OS decide — fastest, largest loss window
  ```
  `everysec` is the right default for most workloads: `always` adds
  meaningful per-write latency for a durability gain most workloads
  don't need, and `no` reintroduces most of RDB's loss-window risk while
  giving up RDB's compactness.

Running both (`appendonly yes` plus scheduled RDB) is the common
production choice: AOF for a small loss window on restart, RDB for fast
full-cluster bootstrap and for portable backups (RDB files are a single
compact file, easy to ship off-box; AOF files can be large and slower to
replay on cold start). Redis prefers the AOF for recovery when both are
present and `appendonly yes`, since it's more current.

### 2. Manage AOF growth with rewrite, and understand what triggers it

The AOF file grows forever without rewriting — periodically Redis
compacts it into the minimal set of commands that reproduce the current
dataset:
```
auto-aof-rewrite-percentage 100   # rewrite when AOF is 2x the size after last rewrite
auto-aof-rewrite-min-size 64mb    # don't rewrite tiny files at startup
```
```bash
redis-cli BGREWRITEAOF
```
A rewrite forks the process (same COW mechanics as `BGSAVE`) — on a
host with little free memory margin, a fork on a large dataset can fail
or cause a latency spike as the kernel sets up copy-on-write page
tables. Size hosts with real headroom above `maxmemory` (a common
starting rule of thumb is roughly 1.5x `maxmemory` free, though the
actual requirement scales with write rate during the fork, not a fixed
ratio) rather than running right up to the memory ceiling.

### 3. Understand Redis Cluster's hash slot model before resharding anything

Redis Cluster splits the keyspace into 16384 hash slots, each owned by
exactly one primary at a time:
```bash
redis-cli -c CLUSTER SHARDS
redis-cli -c CLUSTER SLOTS       # older/wider-compatible form
```
A key's slot is `CRC16(key) mod 16384`, or the slot of the substring
inside `{}` if the key contains a hash tag (e.g. `user:{1000}:profile`
and `user:{1000}:orders` hash to the same slot, enabling multi-key
operations across them) — a design decision that must be made when
choosing key naming conventions, not retrofitted later, since existing
keys don't get hash tags added automatically.

### 4. Reshard deliberately, with monitoring, never as a blind migration

```bash
redis-cli --cluster reshard <any-node>:6379 \
  --cluster-from <source-node-id> \
  --cluster-to <dest-node-id> \
  --cluster-slots 1000 \
  --cluster-yes
```
Resharding moves slots (and the keys in them) live, slot-range by
slot-range, migrating keys one at a time via `MIGRATE` under the hood —
clients see a brief `ASK`/`MOVED` redirect for keys mid-transfer rather
than an outage, provided client libraries handle cluster redirects
correctly (most modern cluster-aware clients do this transparently).
Reshard in a maintenance window for large slot ranges regardless, since
`MIGRATE` for very large keys (a huge hash or sorted set) can add
latency during that specific key's move, and monitor
`redis-cli --cluster check <any-node>:6379` afterward to confirm no
slot is left in a transitional/inconsistent state.

### 5. Configure replica-based failover and verify it actually completes

In Cluster mode, each primary should have at least one replica; Redis
Cluster's own failure detection (gossip-based, via `CLUSTER NODES`
health state) promotes a replica automatically once enough other
primaries mark the failed primary `PFAIL`/`FAIL`:
```bash
redis-cli -c CLUSTER NODES | grep master
```
For non-clustered HA, Sentinel monitors a primary/replica set and
performs the promotion:
```
# sentinel.conf
sentinel monitor mymaster <PRIMARY_HOST> 6379 2   # quorum = 2 of N sentinels must agree
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
```
The quorum value (`2` above) is the number of Sentinels that must agree
the primary is down before a failover is *initiated* — it is not the
number needed to *elect the Sentinel leader* that carries it out, which
requires a majority of all configured Sentinels regardless of the
monitor quorum setting. Run an odd number of Sentinels (3 or 5) across
independent failure domains for the same reason a consensus store needs
odd-numbered quorum in any leader-election design.

### 6. Size `maxmemory` and choose an eviction policy that matches data classification

```
maxmemory 8gb
maxmemory-policy allkeys-lru
```
- `noeviction` (the default if unset): writes fail with `OOM command
  not allowed` once memory is full — correct for data that must never be
  silently dropped (e.g. Redis used as a primary datastore, a queue), but
  it will surface as application write errors, not graceful degradation.
- `allkeys-lru` / `allkeys-lfu`: evict any key regardless of whether it
  has a TTL, approximating least-recently/frequently-used — appropriate
  for a pure cache where every key is disposable.
- `volatile-lru` / `volatile-lfu` / `volatile-ttl`: only evict keys that
  have a TTL set, leaving keys with no TTL untouched even under memory
  pressure — useful when Redis holds a mix of cache data (with TTLs) and
  data that must persist (no TTL), but dangerous if application code
  assumes *all* data is safe from eviction just because some of it is.
Mismatching policy to actual data classification is one of the most
common production incidents with Redis — see the pitfalls below.

### 7. Monitor real memory fragmentation, not just used memory against maxmemory

```bash
redis-cli INFO memory | grep -E "used_memory:|used_memory_rss:|mem_fragmentation_ratio"
```
`mem_fragmentation_ratio` well above 1.0 (rule of thumb: above ~1.5)
indicates the OS-level RSS is significantly larger than Redis's own
accounting of `used_memory`, usually from allocator fragmentation after
heavy key churn with varying value sizes. This headroom is *not*
visible in `maxmemory` accounting (which tracks `used_memory`, not RSS)
and can still trigger an OS-level OOM kill even though Redis believes
it's under its configured limit. `MEMORY PURGE` (where supported by the
allocator, e.g. jemalloc) or a planned restart/failover to a fresh
replica can reclaim fragmented memory; investigate before assuming a
`maxmemory` increase alone fixes a fragmentation problem, since it
often doesn't.

## Best practices

- Run both RDB and AOF in production for anything beyond a pure,
  fully-disposable cache — RDB for fast full recovery and portable
  backups, AOF (`appendfsync everysec`) for a small restart-loss window.
- Give hosts genuine free-memory headroom above `maxmemory` for
  `BGSAVE`/`BGREWRITEAOF` fork operations — don't size to the RAM ceiling
  with no margin for copy-on-write growth during a fork.
- Always run at least one replica per primary shard in Cluster mode (or
  a 3+ Sentinel quorum for non-clustered HA) — a cluster with zero
  replicas has no automatic failover path at all, only manual
  intervention after data loss on that shard.
- Choose `maxmemory-policy` based on actual data classification per
  logical use, not a single fleet-wide default — a shared Redis instance
  mixing cache and non-disposable data needs `volatile-*` with disposable
  data explicitly TTL'd, verified, not assumed.
- Bake hash-tag conventions (`{}`) into key naming from day one for any
  application that will eventually need multi-key transactions or
  Lua scripts spanning related keys in a clustered deployment — adding
  hash tags retroactively means re-keying existing data.
- Monitor `mem_fragmentation_ratio` and replication lag
  (`master_repl_offset` vs. replica's `slave_repl_offset`) as standing
  health metrics, not just `used_memory` against `maxmemory`.

## Common pitfalls

- **Symptom:** Application writes intermittently fail with
  `OOM command not allowed when used memory > 'maxmemory'`, even though
  the workload is a cache and eviction was assumed to be handling this.
  **Fix:** `maxmemory-policy` is set to (or defaulted to) `noeviction`.
  Confirm the intended policy with `CONFIG GET maxmemory-policy` and set
  an eviction policy that matches the data (`allkeys-lru` for a pure
  cache) rather than assuming eviction is on by default — `noeviction`
  is Redis's actual default.

- **Symptom:** Keys that the application assumed were safe from eviction
  (no TTL set) are missing after a period of memory pressure.
  **Fix:** `maxmemory-policy` is set to `allkeys-lru`/`allkeys-lfu`,
  which evicts *any* key regardless of TTL. If some keys must survive
  eviction, switch to a `volatile-*` policy and confirm every key that
  must persist genuinely has no TTL set (a bug that sets an accidental
  TTL on non-cache data under `volatile-*` is just as dangerous as the
  wrong policy).

- **Symptom:** A primary node crashes in Cluster mode and the cluster
  stays in a `FAIL`/degraded state instead of promoting a replica.
  **Fix:** That shard has zero replicas configured, or its replica is
  also unreachable (e.g. colocated with the primary on the same failed
  host/AZ). Verify replica placement is genuinely spread across failure
  domains (`CLUSTER NODES` showing replica host != primary host, ideally
  different AZ/rack) and that every shard has at least one healthy
  replica before treating the cluster as production-ready.

- **Symptom:** Redis's process RSS memory (as seen by the OS / `top`)
  is much higher than `used_memory` reported by `INFO memory`, and the
  host eventually hits an OS-level OOM kill despite `maxmemory` never
  being exceeded from Redis's own perspective.
  **Fix:** This is allocator fragmentation (`mem_fragmentation_ratio`
  significantly above 1), not a `maxmemory` misconfiguration — `maxmemory`
  only bounds `used_memory`, not RSS. Investigate key churn patterns
  causing fragmentation, try `MEMORY PURGE` on a jemalloc-backed build,
  or plan a rolling restart/failover to defragment, and size host RAM
  with fragmentation headroom beyond `maxmemory`, not exactly at it.

- **Symptom:** Someone runs `FLUSHALL` against what turns out to be the
  production cluster (intending a staging/test instance), wiping every
  key with no confirmation prompt and no way to undo it.
  **Fix:** `FLUSHALL`/`FLUSHDB` are immediate, irreversible, cluster-wide
  (in `FLUSHALL`'s case) destructive operations with no built-in
  confirmation step.
  > **Warning — destructive action.** Never run `FLUSHALL`/`FLUSHDB`
  > against a shared or production endpoint without independently
  > confirming the target host/cluster via `CLUSTER INFO` or a
  > connection-string review, and restrict the command via Redis ACLs
  > (`-@dangerous` category, or explicitly denying `flushall`/`flushdb`)
  > for any role/credential that doesn't specifically need it, so a
  > mistaken connection to production can't execute it at all.

## Worked example

**Scenario:** A session-store Redis deployment (currently a single
primary + 1 replica with Sentinel) needs to move to a 3-shard Redis
Cluster ahead of an expected 4x traffic increase, and persistence needs
review since a prior incident lost 30 minutes of session data on an
unplanned restart.

1. Review current persistence: RDB-only, `save 3600 1` (hourly
   snapshot) — this is why 30 minutes of writes were lost on restart, a
   30-minute window is far larger than the incident's actual tolerance.
   Enable AOF alongside the existing RDB schedule:
   ```
   appendonly yes
   appendfsync everysec
   ```
2. Provision 3 primaries + 3 replicas (one replica per primary, each
   replica placed in a different AZ than its primary) and initialize
   the cluster:
   ```bash
   redis-cli --cluster create \
     <node1>:6379 <node2>:6379 <node3>:6379 \
     <node4>:6379 <node5>:6379 <node6>:6379 \
     --cluster-replicas 1
   ```
3. Adopt a hash-tag key convention ahead of migration so multi-key
   session operations (e.g. a session plus its associated rate-limit
   counter) land on the same slot:
   `session:{<session_id>}:data`, `session:{<session_id>}:ratelimit`.
4. Migrate existing single-primary data into the cluster via
   application-level dual-write during a cutover window, then verify
   via `redis-cli --cluster check` that all 16384 slots are covered with
   no gaps before cutting reads over.
5. Set `maxmemory-policy volatile-lru` (sessions carry a TTL; nothing
   else is stored on this instance) and size `maxmemory` per node with
   ~40% headroom over steady-state `used_memory` for `BGREWRITEAOF` fork
   safety during the 4x traffic ramp.
6. Post-migration, monitor `CLUSTER NODES` for replica health and
   `mem_fragmentation_ratio` weekly; the old Sentinel-based pair is
   decommissioned only after a full week of clean cluster operation
   under real production traffic.

## Cross-references

- [redis-configuration-validation](../redis-configuration-validation/SKILL.md) — validates `maxmemory`/eviction policy and cluster topology changes like the ones made here before they're relied on in production.
- [redis-caching-strategy-and-invalidation-patterns](../redis-caching-strategy-and-invalidation-patterns/SKILL.md) — the application-facing caching patterns (cache-aside, TTL strategy, invalidation) that run on top of the cluster/persistence infrastructure covered here.
- [mongodb-operations-and-scaling](../mongodb-operations-and-scaling/SKILL.md) — comparable sharding/resharding and replica-election concerns (chunk migration vs. hash slot migration) if MongoDB and Redis Cluster coexist in the same platform.
