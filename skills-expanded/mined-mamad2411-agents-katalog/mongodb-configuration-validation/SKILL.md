---
name: mongodb-configuration-validation
description: >
  Validates proposed MongoDB replica set configuration, sharding setup,
  and index changes before production rollout — checking voting-member
  quorum math, shard key cardinality against real data, and index build
  impact. Use when the user asks to "review this MongoDB replica set
  config," "validate a shard key before we commit to it," "check this
  index change is safe to run in production," or "will this MongoDB
  config change cause an election issue."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: database-operations
  maturity: stable
---

# MongoDB Configuration Validation

## Purpose

MongoDB's flexibility — reconfiguring a replica set, resharding a
collection, adding an index — makes it easy to apply a change that looks
fine in the shell but has a consequence that only surfaces under
production load: a replica set reconfiguration that breaks voting quorum
math, a shard key that seemed reasonable in a sample but has terrible
real-world cardinality, or a foreground index build that stalls writes
on a busy primary. This skill is the pre-production validation gate for
those changes, complementing the operational depth in
[mongodb-operations-and-scaling](../mongodb-operations-and-scaling/SKILL.md).

## When to use

- Before running `rs.reconfig()` to add/remove a replica set member,
  change priorities/votes, or adjust `electionTimeoutMillis`.
- Before committing to a shard key for a new sharded collection, or
  before running `reshardCollection` on an existing one.
- Before creating a new index on a large or high-traffic production
  collection.
- Before changing `writeConcern`/`readConcern` defaults, or introducing a
  `readPreference` change to an application that reads from secondaries.
- As a review gate for infrastructure-as-code that manages MongoDB
  replica set/sharding topology.

## Prerequisites & environment

- `clusterMonitor` role (or higher) for read-only validation queries
  (`rs.conf()`, `rs.status()`, `sh.status()`, `db.collection.stats()`);
  `clusterAdmin`/`dbAdmin` only needed to actually apply validated
  changes.
- MongoDB 5.0+ assumed for command syntax below; note explicitly where
  behavior differs on older supported versions (e.g. `reshardCollection`
  requires 4.4+, `replSetResizeOplog` requires 3.6+).
- Access to representative production data (or a realistic sample) for
  shard-key cardinality analysis — validating a shard key against a tiny
  or synthetic dataset with artificially even distribution gives false
  confidence.
- Knowledge of the collection's real read/write traffic pattern (peak
  QPS, whether reads target primary or secondaries) to validate index
  build timing and write-concern changes against actual load, not just
  configuration correctness in isolation.

## Step-by-step guidance

### 1. Validate replica set voting/quorum math before any `rs.reconfig()`

```js
cfg = rs.conf()
cfg.members.forEach(m => print(m.host, m.votes, m.priority, m.arbiterOnly))
```
A replica set needs a **majority of voting members** reachable to elect
a primary and to accept majority-acknowledged writes. Validate:
- Total voting members should be odd (max 7 voting members is a MongoDB
  hard limit) — an even number of voters risks an election tie with no
  majority achievable, stalling failover indefinitely until the tie is
  broken by a member coming back.
- Adding a single new member with `votes: 1` to an existing set with an
  even total is a common mistake made "to add capacity" that actually
  degrades quorum math — validate the resulting total, not just that the
  new member itself looks reasonable.
- An arbiter counts as a voting member but never holds data or can
  become primary — useful to break a tie cheaply, but adding multiple
  arbiters, or an arbiter to a set that already has an odd number of
  data-bearing voters, adds complexity without benefit and should be
  flagged.
- Any member with `priority: 0` cannot become primary but still votes
  (unless also configured `votes: 0`) — confirm this is intentional
  (e.g. a reporting-only or cross-region DR replica) and not an
  unintended side effect of a copy-pasted config.

### 2. Validate a proposed shard key against real cardinality and distribution, not assumption

```js
db.orders.aggregate([
  { $group: { _id: "$tenantId", count: { $sum: 1 } } },
  { $sort: { count: -1 } },
  { $limit: 10 }
])
```
Run this against the *actual* candidate shard key fields (or the leading
field of a compound key) on production or a representative snapshot,
not a synthetic test dataset. Flag as unsafe:
- A leading field with very low cardinality relative to the number of
  target shards (e.g. 3 distinct values across 10 shards — cannot
  usefully distribute).
- A heavily skewed distribution even with adequate raw cardinality (e.g.
  one tenant holding 80% of documents) — this produces a hot shard even
  though the key has "enough" distinct values in aggregate.
- A monotonically increasing leading field (default `_id`, or any
  timestamp/auto-increment field) for a write-heavy collection, since
  this concentrates new writes on one shard's current chunk range
  regardless of overall cardinality.
Cross-check the query patterns that will run against the sharded
collection: a shard key that distributes writes well but doesn't appear
as a filter in the majority of queries forces `mongos` to broadcast
(scatter-gather) those queries to every shard — validate this trade-off
explicitly rather than optimizing purely for write distribution.

### 3. Validate an index change's build impact before running it on a live collection

```js
db.orders.stats().count          // collection size
db.currentOp({ "command.createIndexes": { $exists: true } })  // check for an in-progress build
```
Confirm the index build will run in the background/online mode
appropriate to the MongoDB version in use (default online builds since
4.2), and — critically — confirm it will be run as a **rolling build**
(secondaries first, each stepped out of the effective read path via
`readPreference` before its build starts, then the primary) for a large
collection on a busy replica set, rather than a single foreground build
against the primary. Validate the collection's current size and expected
build duration against a maintenance window if the workload cannot
tolerate any degraded secondary read capacity during the build.

### 4. Validate `writeConcern`/`readConcern` changes against the actual durability requirement

```js
db.orders.insertOne({...}, { writeConcern: { w: "majority", wtimeout: 5000 } })
```
- `w: 1` (default in some driver configs) acknowledges a write once the
  primary applies it, with no guarantee it's replicated anywhere —
  survivable data loss on primary failure. Validate that any collection
  storing data where loss is unacceptable (financial, audit) uses
  `w: "majority"` explicitly, not an inherited driver default.
- Validate `wtimeout` is set to a sane, non-zero value — an unbounded
  wait for majority acknowledgment during a replica set election or
  network partition can hang application writes indefinitely otherwise.
- For `readPreference: secondary` or `secondaryPreferred` changes,
  validate the read traffic being redirected can tolerate replication
  lag (i.e. it's not read-your-own-write-sensitive application logic) —
  this is a common source of "the record I just wrote isn't there yet"
  bugs when validation is skipped.

### 5. Validate against a staging replica set/cluster with representative shape before production

Apply the reconfiguration/index build/shard key choice against a
staging environment seeded with production-shaped data (real
cardinality distributions matter far more than raw row count for shard
key validation specifically) before scheduling the production change.

## Best practices

- Always compute the resulting voting-member count and majority
  threshold explicitly after any proposed `rs.reconfig()`, rather than
  reviewing each member change in isolation — quorum math is a property
  of the whole set, not any single member.
- Validate shard key cardinality and skew against real or realistically
  representative data before committing — a shard key decision is far
  more expensive to reverse (a full `reshardCollection` or manual
  migration) than the validation effort up front.
- Require rolling index builds (secondaries first) as the default
  expectation for any collection above a size/traffic threshold your
  team defines, and require an explicit justification to skip that and
  build directly on the primary.
- Treat `w: 1` writeConcern on any collection storing data with real
  durability requirements as a finding to flag, not a silent default to
  accept.
- Bake shard-key and index-build validation into the review process for
  infrastructure-as-code-managed MongoDB schemas/topology, not just as
  manual shell-command review.

## Common pitfalls

- **Symptom:** After adding a new replica set member "for read capacity,"
  the set fails to elect a primary during a later single-node outage that
  previously would have been survivable.
  **Fix:** The new member's vote pushed the total voting member count to
  an even number, so a single-node loss can produce a tie with no
  majority achievable. Recompute total voters after every membership
  change and keep the total odd — consider `votes: 0` for a member
  that's meant to be read-capacity-only, not a failover participant.

- **Symptom:** A shard key validated against a small staging dataset
  looked evenly distributed, but in production one shard receives a
  wildly disproportionate share of both storage and query load.
  **Fix:** The staging dataset's cardinality/skew didn't represent
  production reality (e.g. synthetic data with uniform random tenant
  IDs, vs. production's actual heavy-tailed tenant size distribution).
  Re-validate shard key candidates against a production data snapshot or
  a statistically representative sample, specifically checking for skew,
  not just raw cardinality count.

- **Symptom:** A `createIndex()` run directly against the primary of a
  busy replica set causes a multi-minute write stall and elevated
  application error rates during the build.
  **Fix:** The build wasn' t run as a rolling, secondary-first operation,
  or the collection was large enough that even a background/online build
  contended heavily for I/O and CPU on the primary. Validate collection
  size and current load before deciding foreground vs. rolling build
  approach, and prefer rolling builds by default on any
  production-traffic-bearing replica set.

- **Symptom:** An application intermittently fails to read a document it
  just wrote, only under moderate load.
  **Fix:** A `readPreference: secondaryPreferred` change was applied to
  a code path with read-your-own-write requirements, and replication lag
  under load exceeds the assumption. Validate read-preference changes
  against each call site's actual consistency requirement, and use
  causal consistency sessions or `readPreference: primary` for
  read-your-own-write-sensitive paths.

- **Symptom:** A reviewer approves a `reshardCollection` run against a
  large production collection with no verification that the new shard
  key was validated, and it triggers a multi-hour, cluster-wide
  resource-intensive resharding operation during business hours.
  **Fix:** This is a high-blast-radius, hard-to-reverse operation once
  started — always validate the target shard key against real
  cardinality/skew data first (step 2 above), and schedule
  `reshardCollection` for a low-traffic maintenance window with
  monitoring on cluster resource usage throughout, since it competes
  for I/O and CPU with live traffic for its full duration.

## Worked example

**Scenario:** A team proposes two changes together: adding a 4th replica
set member (a new cross-region DR replica with `priority: 0`) and
creating a new compound index on a 200M-document `orders` collection to
support a new reporting query.

1. Validate the replica set change: current set has 3 voting
   data-bearing members (odd, healthy majority math). The proposed 4th
   member is drafted with default `votes: 1`, which would bring the
   total to 4 (even) — flagged as a quorum regression. Corrected
   proposal: set the new member's `votes: 0` in addition to
   `priority: 0`, since it's explicitly DR-only and shouldn't
   participate in elections or count toward write majority overhead
   across a high-latency cross-region link.
   ```js
   cfg = rs.conf()
   cfg.members.push({ _id: 3, host: "<DR_HOST>:27017", priority: 0, votes: 0 })
   rs.reconfig(cfg)
   ```
2. Validate the index change: `db.orders.stats().count` shows ~200M
   documents, and current traffic shows continuous write load with no
   natural low-traffic window (24/7 global user base). Recommend a
   rolling build: build on each secondary first (temporarily removing it
   from `readPreference: secondaryPreferred` rotation via
   `hidden: true` during the build), verify build completion via
   `db.currentOp()` clearing, restore it to rotation, then repeat for the
   primary last using a brief step-down if a fully non-blocking build
   isn't available in the deployed version.
3. Confirm the new index's field order matches the actual reporting
   query's filter/sort to avoid needing a second, redundant index later:
   ```js
   db.orders.createIndex({ region: 1, createdAt: -1 }, { background: true })
   ```
4. Recommendation delivered with both changes approved as revised: DR
   member added with `votes: 0`/`priority: 0`, index built as a rolling,
   secondary-first operation scheduled outside the collection's daily
   peak window despite no true 24/7 lull, to minimize contention.

## Cross-references

- [mongodb-operations-and-scaling](../mongodb-operations-and-scaling/SKILL.md) — the operational depth (shard key mechanics, replica set election tuning, index build behavior) this skill's validation checks are grounded in.
- [postgresql-configuration-validation](../postgresql-configuration-validation/SKILL.md) — comparable pre-production configuration validation discipline applied to PostgreSQL, useful as a pattern reference in a polyglot database environment.
- [redis-configuration-validation](../redis-configuration-validation/SKILL.md) — comparable validation approach for Redis maxmemory/eviction/cluster settings, if the same platform runs both.
