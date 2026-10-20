---
name: redis-configuration-validation
description: >
  Validates proposed Redis maxmemory/eviction-policy settings, persistence
  configuration (RDB/AOF), and Redis Cluster topology before they are
  relied on in production — checking eviction policy against actual data
  classification, replica placement against failure domains, and
  quorum/majority math for Sentinel and Cluster failover. Use when the
  user asks to "review this Redis config before we deploy it," "validate
  maxmemory-policy before we go live," "is this Redis Cluster topology
  actually safe," "check this Sentinel quorum setting," or "will this
  Redis config change cause eviction we don't expect."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: database-operations
  maturity: stable
---

# Redis Configuration Validation

## Purpose

A Redis configuration can look internally consistent and still fail
badly in production: an eviction policy that matches "a cache" in
principle but not the specific mix of TTL'd and non-TTL'd keys actually
stored, a Cluster topology where every replica happens to sit in the
same availability zone as its primary, or a Sentinel quorum number
copied from an example that doesn't match the actual number of deployed
Sentinels. This skill is the pre-production validation gate for those
settings, complementing the operational depth in
[redis-operations-and-cluster-management](../redis-operations-and-cluster-management/SKILL.md)
— that skill covers how persistence, cluster, and memory management
work; this one covers how to check a specific proposed configuration
against them before it's trusted with production traffic.

## When to use

- Before deploying a new Redis instance/cluster to production, to
  validate `maxmemory`, `maxmemory-policy`, and persistence settings
  match the actual data being stored (pure cache vs. mixed cache and
  durable data).
- Before or after standing up Redis Cluster, to validate replica
  placement genuinely spans failure domains and every shard has
  adequate replica coverage.
- Before relying on a Sentinel deployment for HA, to validate the
  configured quorum and the actual number of running Sentinel processes
  are consistent with the failure tolerance the team believes it has.
- Before applying a `CONFIG SET` change (or an infra-as-code-managed
  `redis.conf` change) to a production instance, especially anything
  touching `maxmemory`, `appendfsync`, or `save`.
- As a review gate for infrastructure-as-code that provisions Redis
  Cluster/Sentinel topology.

## Prerequisites & environment

- Read access to `CONFIG GET *` (or the specific parameters in
  question) and `INFO` on the target instance/cluster — a role with
  Redis ACL category `@read` and `@admin`-config-read is sufficient for
  validation; no write access needed unless applying the validated
  change.
- Redis 6.2+ assumed for ACL-aware validation guidance below; note
  explicitly where an older deployment lacks a feature being validated
  against (e.g. ACLs themselves require 6.0+; `CLUSTER SHARDS` requires
  7.0+, use `CLUSTER SLOTS`/`CLUSTER NODES` on older clusters).
- Knowledge of the actual data being stored — specifically, whether
  every key is disposable cache data or whether some subset must survive
  memory pressure — since this is not discoverable from configuration
  alone and must come from the application team.
- For Cluster/Sentinel validation: the real physical/logical placement
  of each node (which AZ/rack/host each primary and replica actually
  runs on), not just the logical replica-count from `CLUSTER NODES`.
- Knowledge of measured production write volume and average key/value
  size, to validate `maxmemory` and fork-headroom sizing against
  reality rather than a guess.

## Step-by-step guidance

### 1. Validate `maxmemory-policy` against actual data classification, not assumption

```bash
redis-cli CONFIG GET maxmemory-policy
redis-cli CONFIG GET maxmemory
```
- If the instance stores **only** disposable cache data, `allkeys-lru`
  or `allkeys-lfu` is appropriate — validate every keyspace prefix in
  use is genuinely safe to evict at any time, not assumed to be.
- If the instance stores a **mix** of disposable and non-disposable
  data, only a `volatile-*` policy is safe, and it must be paired with a
  concrete audit that every non-disposable key genuinely has no TTL and
  every disposable key genuinely does:
  ```bash
  redis-cli --scan --pattern 'session:*' | head -20 | xargs -I{} redis-cli TTL {}
  ```
  A `volatile-*` policy does not protect against an application bug that
  fails to set a TTL on cache data (it accumulates forever, never
  evicted) or that accidentally sets a TTL on durable data (it silently
  becomes evictable). Validate both directions, not just the policy name.
- `noeviction` should be the validated choice for any instance acting as
  a primary datastore (queues, non-cache session truth, rate-limit
  counters that must not silently disappear) — confirm the application
  has a real plan for handling `OOM command not allowed` errors (backoff,
  alerting) rather than this being an unplanned failure mode discovered
  in production.

### 2. Validate persistence settings match the actual recovery-time/data-loss tolerance

```bash
redis-cli CONFIG GET save
redis-cli CONFIG GET appendonly
redis-cli CONFIG GET appendfsync
```
- If `save ""` (RDB disabled) and `appendonly no` (AOF disabled) both
  hold, the instance has **zero persistence** — any restart, planned or
  not, loses all data. Validate this is genuinely intended (e.g. a
  pure, rebuildable cache where cold-start-empty is acceptable) and not
  an oversight for a payments/session-critical instance.
- For any instance where restart data loss matters, validate `appendonly
  yes` is set (not relying on RDB's coarser snapshot interval alone) and
  `appendfsync` matches the durability requirement — flag `appendfsync
  always` as a latency cost worth confirming is actually needed versus
  `everysec`'s ~1-second loss window, and flag `appendfsync no` as
  effectively equivalent to RDB-only durability despite AOF being
  enabled.

### 3. Validate Cluster replica placement actually spans failure domains

```bash
redis-cli -c CLUSTER NODES
```
Cross-check each primary/replica pair's *actual* host/AZ placement
(from cloud provider tags or infra-as-code inventory, not inferable from
`CLUSTER NODES` alone) against the assumption that a replica survives
its primary's failure:
- Flag any shard whose replica is colocated with its primary in the
  same AZ/rack/physical host — this shard has no real fault tolerance
  even though `CLUSTER NODES` shows a replica configured, since a single
  zone failure takes out both.
- Flag any shard with zero replicas — confirm this is an accepted,
  deliberate risk (e.g. a non-critical cache shard) and not an
  unnoticed gap in an otherwise-replicated cluster.
- Validate slot coverage is complete and non-overlapping:
  ```bash
  redis-cli --cluster check <any-node>:6379
  ```
  Any gap or overlap reported here means some keys are currently
  unreachable or ambiguously owned — this must be resolved (via
  `--cluster fix`, cautiously and in a maintenance window) before the
  cluster is considered production-ready, not left as a known issue.

### 4. Validate Sentinel quorum against the actual deployed Sentinel count

```
sentinel monitor mymaster <PRIMARY_HOST> 6379 2
```
The `quorum` value (2 in this example) must be validated against:
- The actual number of running Sentinel processes — a quorum of 2
  configured against only 2 total Sentinels means losing a single
  Sentinel makes failover-initiation agreement impossible (no majority
  of the surviving process(es) can reach the configured quorum).
- The Sentinel **leader election** requirement, which is separate from
  the monitor quorum: carrying out a failover requires a majority of
  *all configured* Sentinels to elect a leader, regardless of the
  quorum value used to *decide the primary is down*. Validate total
  Sentinel count is odd (3 or 5) and quorum is set to a real majority
  fraction of that total, not an arbitrary small number.
- Validate Sentinels are placed across independent failure domains —
  3 Sentinels all in the same AZ recreates the same single-zone-failure
  risk as un-replicated Cluster shards.

### 5. Validate a proposed `CONFIG SET`/`redis.conf` change against restart requirements and blast radius

Most Redis parameters take effect immediately via `CONFIG SET` and
persist to `redis.conf` only if followed by `CONFIG REWRITE` — validate
which behavior is intended:
```bash
redis-cli CONFIG SET maxmemory 8gb
redis-cli CONFIG REWRITE   # persist to redis.conf, or it reverts on restart
```
A `CONFIG SET` without a subsequent `CONFIG REWRITE` reverts silently on
the next restart, which is a common source of "the setting we applied
last month is gone" surprises — validate that infra-as-code-managed
`redis.conf` and any live `CONFIG SET` changes are kept in sync, rather
than allowing drift between the file and the running instance.

### 6. Validate against a staging cluster with representative shape before production

Apply the proposed `maxmemory-policy`, persistence, or topology change
against a staging Redis Cluster/Sentinel deployment seeded with
production-representative key size and TTL distribution (not just row
count) before scheduling the production change, since eviction behavior
and fork/rewrite timing are both sensitive to real value-size
distribution, not just total dataset size.

## Best practices

- Require an explicit data-classification statement (pure cache vs.
  mixed vs. durable) as part of any Redis provisioning request, and
  validate the proposed `maxmemory-policy` against that statement
  directly rather than defaulting to whatever the last deployment used.
- Treat "zero persistence" (`save ""` and `appendonly no`) as a finding
  requiring explicit sign-off, not a silent default — confirm in writing
  that cold-start-empty is acceptable for that specific instance.
- Validate Cluster replica-to-primary failure-domain placement using
  real infrastructure inventory, not `CLUSTER NODES` output alone, since
  Redis itself has no concept of AZ/rack and cannot tell you if a
  replica placement is actually fault-tolerant.
- Recompute Sentinel quorum and leader-majority math after every change
  to Sentinel count, the same way replica-set voting math must be
  recomputed after any MongoDB membership change.
- Bake `CONFIG REWRITE` (or the infra-as-code equivalent of updating the
  source-of-truth `redis.conf`) into the same change as any `CONFIG SET`
  applied live, so the file and the running instance never silently
  diverge.

## Common pitfalls

- **Symptom:** A Redis instance is provisioned as "just a cache," but
  months later an incident reveals it also stores rate-limit counters
  that must not silently disappear, and a memory-pressure event evicted
  them under `allkeys-lru`.
  **Fix:** The `maxmemory-policy` was validated against an assumption
  ("it's a cache") rather than the actual keyspace contents. Audit real
  key prefixes in use (`--scan --pattern`) before approving an
  `allkeys-*` policy, and require any non-disposable use case to either
  move to its own instance or use a validated `volatile-*` policy with a
  confirmed TTL audit.

- **Symptom:** A Redis Cluster passes every health check
  (`CLUSTER NODES` shows every shard with a replica) but an AZ outage
  takes out multiple shards simultaneously with no automatic recovery.
  **Fix:** Replica placement wasn't validated against real
  infrastructure topology — replicas were colocated with their primaries
  in the same AZ. Validate placement against actual cloud
  provider/rack metadata, not just replica *count*, before treating the
  cluster as AZ-fault-tolerant.

- **Symptom:** A Sentinel-monitored primary fails, and failover never
  completes even though the configured quorum (2) was reached.
  **Fix:** Reaching the monitor quorum is not sufficient — carrying out
  the failover requires a majority of *all configured* Sentinels to
  elect a leader, and if one of only 3 Sentinels was already down when
  the primary failed, the 2 remaining can still fail to reach a
  majority in some topologies, or a total that's even to begin with
  makes this worse. Validate total Sentinel count is odd and the
  election-majority math (not just the monitor quorum number) is sound
  for the actual deployed count.

- **Symptom:** A `CONFIG SET maxmemory-policy volatile-lru` change
  applied via `redis-cli` during an incident works immediately, but
  reverts to the old (wrong) policy after the next routine restart/
  failover.
  **Fix:** `CONFIG REWRITE` was never run (or the infra-as-code
  `redis.conf` template was never updated to match), so the live change
  and the persisted config file diverged. Always follow a live
  `CONFIG SET` with either `CONFIG REWRITE` or an equivalent update to
  the managed config source, and validate the two are in sync as part
  of the change.

- **Symptom:** A reviewer approves disabling persistence
  (`save ""`, `appendonly no`) on an instance "to improve write
  throughput," without confirming what data the instance actually
  holds, and a routine node replacement wipes production session data.
  **Fix:** This is a high-blast-radius change if the instance isn't
  genuinely a rebuildable cache — always validate the actual data
  classification and get explicit sign-off before approving zero
  persistence, and prefer AOF with `everysec` as a low-cost default
  that preserves most of the throughput benefit while keeping a small
  loss window, rather than jumping straight to no persistence at all.

## Worked example

**Scenario:** A team requests review of a new Redis Cluster
provisioning PR before go-live: 3 primaries, 3 replicas, `maxmemory-policy
allkeys-lru`, `save ""`, `appendonly no`, Sentinel not used (Cluster mode
handles failover). The instance will store both a product-catalog cache
(fully disposable) and a shopping-cart service's cart contents (must
survive a restart without silently vanishing, per the product team).

1. Validate `maxmemory-policy`: `allkeys-lru` is unsafe given the cart
   data is not disposable — carts have no TTL requirement stated and
   would be evicted under memory pressure exactly like catalog cache
   entries. Flag as blocking; recommend either splitting cart data to a
   separate instance/policy, or moving to `volatile-lru` with a
   confirmed TTL audit showing catalog-cache keys have TTLs and cart
   keys do not (making carts eviction-exempt) — team confirms carts
   should also expire, just on a longer, explicit TTL (24h), resolving
   the conflict cleanly under `volatile-lru`.
2. Validate persistence: `save ""` and `appendonly no` together mean
   zero persistence — a routine node restart during a rolling upgrade
   would silently drop all in-progress carts. Flag as blocking; require
   `appendonly yes` with `appendfsync everysec` given cart loss has real
   business cost but sub-second precision durability (`always`) isn't
   needed.
3. Validate Cluster replica placement: infra-as-code shows replicas
   assigned round-robin without an explicit anti-affinity rule — cross-
   check actual AZ assignment and find replica-3 colocated with
   primary-3 in the same AZ. Flag as blocking; require an explicit
   anti-affinity constraint in the provisioning IaC before merge.
4. Revised config approved: `maxmemory-policy volatile-lru` with all
   cart and catalog keys carrying explicit TTLs, `appendonly yes` /
   `appendfsync everysec`, and replica placement corrected to guarantee
   every primary/replica pair spans separate AZs — validated against a
   staging cluster seeded with representative cart/catalog key
   proportions before the production change is scheduled.

## Cross-references

- [redis-operations-and-cluster-management](../redis-operations-and-cluster-management/SKILL.md) — the operational mechanics (persistence, cluster topology, memory management) this skill's validation checks are grounded in.
- [redis-caching-strategy-and-invalidation-patterns](../redis-caching-strategy-and-invalidation-patterns/SKILL.md) — validates the *policy* layer here against the actual caching pattern in use (e.g. whether TTL strategy assumed by `volatile-*` matches the application's cache-aside/write-through design).
- [mongodb-configuration-validation](../mongodb-configuration-validation/SKILL.md) — comparable pre-production configuration validation discipline (quorum math, replica placement, staged rollout) applied to MongoDB, useful as a pattern reference in a polyglot environment.
