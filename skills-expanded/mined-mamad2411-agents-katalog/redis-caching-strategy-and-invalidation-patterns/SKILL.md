---
name: redis-caching-strategy-and-invalidation-patterns
description: >
  Covers application-facing caching design on top of Redis: cache-aside
  vs. write-through vs. write-behind, TTL strategy (fixed, sliding,
  jittered), cache invalidation patterns (explicit delete, versioned
  keys, pub/sub fan-out) and their specific failure modes (stale reads,
  thundering herd, cache stampede). Distinct from cluster/persistence
  operations. Use when the user asks to "design a caching strategy for
  this service," "should I use cache-aside or write-through," "how do I
  invalidate a Redis cache on update," "why are we seeing stale data
  from Redis," or "prevent a thundering herd on cache expiry."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: database-operations
  maturity: stable
---

# Redis Caching Strategy and Invalidation Patterns

## Purpose

A cache is only as good as its invalidation strategy — the moment
between a source-of-truth write and the cache reflecting it (or not
reflecting it, deliberately) is where nearly every caching bug lives:
stale reads served long after data changed, a thundering herd of
duplicate rebuilds when a hot key expires, or a cache that's
"consistent" only because nobody has tested the race condition yet.
This skill covers the application-level design decisions that sit above
Redis's own mechanics: which caching pattern to use (cache-aside,
write-through, write-behind), how to set TTLs deliberately rather than
by habit, and how to invalidate correctly under concurrent writes. It
assumes Redis itself is already operating correctly — for the
cluster/persistence/memory-management layer underneath, see
[redis-operations-and-cluster-management](../redis-operations-and-cluster-management/SKILL.md);
for validating `maxmemory-policy` and persistence settings against the
TTL strategy chosen here, see
[redis-configuration-validation](../redis-configuration-validation/SKILL.md).

## When to use

- Designing a new caching layer for a service backed by a database
  (PostgreSQL, MongoDB, etc.) and choosing between cache-aside,
  write-through, or write-behind.
- Deciding TTL strategy for a cache — fixed vs. sliding expiration, and
  whether to jitter TTLs to avoid synchronized mass expiry.
- Investigating stale reads: a client sees old data from Redis after
  the underlying source of truth has already changed.
- Diagnosing a "thundering herd" / "cache stampede": a spike in backend
  load correlated with a popular cache key expiring.
- Designing cache invalidation for a multi-instance/multi-region
  deployment where a write on one node must invalidate a cached copy
  held by others.
- Reviewing whether a cache is masking a deeper problem (e.g. the
  database can't handle real load without the cache, meaning the cache
  is now a single point of failure disguised as an optimization).

## Prerequisites & environment

- A working Redis deployment (cluster or standalone) already handling
  the infrastructure concerns in
  [redis-operations-and-cluster-management](../redis-operations-and-cluster-management/SKILL.md)
  — this skill assumes Redis itself is reachable and correctly
  configured, and focuses on the application-side pattern built on top.
- A clear identification of the actual source of truth (the database or
  service Redis is caching in front of) and its own consistency
  guarantees, since a cache cannot be more consistent than the source it
  reads from at write time.
- Application-level ability to generate/manage cache keys with a
  consistent, collision-free naming scheme (typically including a
  version or entity-ID component) — this is a design decision made in
  application code, not a Redis setting.
- For pub/sub-based invalidation fan-out: all cache-reading instances
  subscribed to a shared invalidation channel, and a plan for what
  happens to an instance that's disconnected from pub/sub when an
  invalidation message is published (pub/sub messages are fire-and-
  forget — a disconnected subscriber never receives a missed message).

## Step-by-step guidance

### 1. Choose the caching pattern based on read/write ratio and staleness tolerance

**Cache-aside (lazy loading)** — the application checks the cache first,
and on a miss reads from the database and populates the cache:
```python
def get_user(user_id):
    cached = redis.get(f"user:{user_id}")
    if cached is not None:
        return deserialize(cached)
    user = db.query("SELECT * FROM users WHERE id = %s", user_id)
    redis.set(f"user:{user_id}", serialize(user), ex=300)
    return user
```
This is the most common pattern: simple, resilient to cache
unavailability (fall back to the database), and only caches data that's
actually read. Its weakness is a **write** to the database doesn't
automatically update or invalidate the cache — that must be handled
explicitly (step 3).

**Write-through** — every write goes through the cache, which writes to
the database synchronously before acknowledging:
```python
def update_user(user_id, data):
    db.execute("UPDATE users SET ... WHERE id = %s", user_id, data)
    redis.set(f"user:{user_id}", serialize(data), ex=300)
```
Keeps the cache consistent with every write at the cost of write
latency (every write pays both the database and cache round-trip) and
still caches data on write whether or not it's ever read again —
appropriate for read-heavy data with a low tolerance for staleness.

**Write-behind (write-back)** — writes go to the cache immediately and
are asynchronously flushed to the database later. Lowest write latency,
but introduces a durability gap (data in cache but not yet in the
database is lost if the cache node fails before flushing) and
significant complexity in guaranteeing eventual consistency and
ordering — reserve for genuinely write-heavy, staleness-tolerant
workloads (e.g. view counters, non-critical activity logs), never for
data where losing an unflushed write is unacceptable.

### 2. Set TTLs deliberately, and jitter them to avoid synchronized expiry

A fixed TTL applied identically to many keys populated at the same time
(e.g. a cache warm-up that sets thousands of keys with `ex=300` in a
tight loop) causes them all to expire simultaneously, producing a
correlated spike in cache misses and backend load exactly 300 seconds
later. Add jitter:
```python
import random
base_ttl = 300
jittered_ttl = base_ttl + random.randint(-30, 30)
redis.set(key, value, ex=jittered_ttl)
```
Choose TTL length based on actual staleness tolerance, not a
copy-pasted default: a product-catalog price shown to users tolerates
minutes of staleness; an inventory-availability count read at checkout
tolerates far less; a permissions/entitlement check may tolerate
almost none. Sliding expiration (refreshing the TTL on every read, via
`GETEX key EX <ttl>`) keeps frequently-accessed data cached longer at
the cost of never naturally expiring genuinely stale-but-still-read
data — use it deliberately for "hot and valid" data, not as a default
that silently extends staleness windows for data that should have
refreshed.

### 3. Invalidate on write — don't rely on TTL alone for correctness-sensitive data

For any data where staleness beyond the write itself is unacceptable
(not just "eventually consistent within a TTL window is fine"),
actively invalidate on write rather than waiting for natural expiry:
```python
def update_user(user_id, data):
    db.execute("UPDATE users SET ... WHERE id = %s", user_id, data)
    redis.delete(f"user:{user_id}")   # next read repopulates from DB (cache-aside)
```
Prefer **delete-then-let-cache-aside-repopulate** over
**update-the-cache-directly-on-write** for cache-aside systems — writing
the new value directly into the cache on update reintroduces a race:
if two concurrent writes interleave with two concurrent cache
repopulations, a slower, now-stale read can overwrite the cache with
old data *after* a newer write's cache update already landed. Deleting
the key and letting the next reader recompute from the (already
consistent) database avoids this race at the cost of one extra cache
miss per invalidation.

### 4. Fan out invalidation across instances/regions when a single Redis endpoint isn't shared

If multiple application regions each read from their own local Redis
(not a shared cluster), a write in one region must invalidate the
cached copy in every other region. Use Redis pub/sub for fan-out, but
design for its at-most-once, fire-and-forget delivery:
```python
# Publisher (on write)
redis.publish("cache-invalidate", json.dumps({"key": f"user:{user_id}"}))

# Subscriber (each app instance)
pubsub = redis.pubsub()
pubsub.subscribe("cache-invalidate")
for message in pubsub.listen():
    if message["type"] == "message":
        payload = json.loads(message["data"])
        local_cache.delete(payload["key"])
```
A subscriber disconnected at publish time never receives that message
and will keep serving stale data until its own TTL naturally expires —
this is why invalidation-on-write should be treated as an optimization
that *shortens* the staleness window, not the sole correctness
mechanism; TTL is still the backstop that bounds worst-case staleness
even if a pub/sub message is missed.

### 5. Prevent thundering herd / cache stampede on expiry of a hot key

When a frequently-requested key expires, many concurrent requests can
all miss simultaneously and all attempt to recompute and repopulate it
at once, multiplying backend load exactly when it was already handling
the read traffic via cache. Use a lock (or "recompute lease") so only
one request rebuilds the value while others either wait briefly or
serve a stale copy:
```python
def get_with_stampede_protection(key, rebuild_fn, ttl=300, lock_ttl=10):
    value = redis.get(key)
    if value is not None:
        return deserialize(value)
    lock_key = f"lock:{key}"
    got_lock = redis.set(lock_key, "1", nx=True, ex=lock_ttl)
    if got_lock:
        try:
            fresh = rebuild_fn()
            redis.set(key, serialize(fresh), ex=ttl)
            return fresh
        finally:
            redis.delete(lock_key)
    else:
        time.sleep(0.05)
        return get_with_stampede_protection(key, rebuild_fn, ttl, lock_ttl)
```
An alternative (or complement) is **early/probabilistic refresh**: read
the value along with its remaining TTL, and have a small, randomized
fraction of requests proactively recompute it slightly before actual
expiry, spreading rebuild load over time instead of concentrating it
at the exact expiry instant.

## Best practices

- Default to cache-aside for most read-heavy services — it degrades
  gracefully (a Redis outage means falling back to the database, not an
  application error) and only caches data that's actually requested.
- Jitter TTLs on any batch of keys populated together, and choose TTL
  length per data type based on its actual staleness tolerance, not one
  fleet-wide constant.
- Invalidate (delete) on write for correctness-sensitive data rather
  than writing the new value directly into the cache, to avoid the
  stale-overwrite race under concurrent writes.
- Treat TTL as the correctness backstop and invalidation-on-write as the
  staleness-window optimization — never design a system where a missed
  invalidation message (pub/sub, cross-region) has no bound on how long
  stale data can be served.
- Add stampede protection (a lock/lease or probabilistic early refresh)
  for any key popular enough that its concurrent-miss rebuild load would
  meaningfully spike backend load — don't wait for an incident to
  discover a hot key needs this.
- Make cache keys carry a version or schema-revision component
  (`user:v2:{id}`) when the cached value's shape can change across a
  deploy, so a rolling deploy with two code versions running
  simultaneously can't have one version read a cache entry shaped by the
  other.

## Common pitfalls

- **Symptom:** A user's profile update doesn't appear reflected when
  they immediately reload the page, even though the database write
  succeeded.
  **Fix:** The cache wasn't invalidated on write (relying on TTL alone),
  or was updated directly with a stale value due to a race between two
  concurrent writes. Invalidate (delete) the cache key as part of the
  same write transaction/operation, and prefer delete-then-repopulate
  over direct cache-value overwrite to avoid the concurrent-write race.

- **Symptom:** A popular cache key's expiry produces a visible latency/
  error spike on the backend database every time it expires, at a
  predictable interval.
  **Fix:** This is a classic thundering herd/cache stampede — many
  concurrent requests all miss and all recompute simultaneously. Add a
  rebuild lock (only one request repopulates, others wait briefly or
  serve stale) or probabilistic early refresh, and jitter the TTL so
  this key doesn't expire in lockstep with other related keys.

- **Symptom:** A cache warm-up script populates thousands of keys at
  startup, and exactly `TTL` seconds later the backend sees a large,
  correlated spike in load as they all expire together.
  **Fix:** All keys were set with an identical fixed TTL and no jitter.
  Add randomized jitter (e.g. ±10% of the base TTL) to spread expiry
  over time instead of a single synchronized wave.

- **Symptom:** In a multi-region deployment, a write in region A is
  correctly invalidated locally, but region B keeps serving stale data
  for much longer than expected — sometimes indefinitely until a
  process restart.
  **Fix:** Region B's pub/sub subscriber was disconnected (deploy,
  network blip, crash-restart) at the moment the invalidation message
  was published, and Redis pub/sub is fire-and-forget with no message
  replay for a reconnecting subscriber. Treat pub/sub invalidation as a
  latency optimization only, and ensure every cached key still carries a
  bounded TTL as the correctness backstop so a missed invalidation
  self-heals within a known worst-case window rather than indefinitely.

- **Symptom:** During a rolling deploy, some requests receive data
  shaped by the new code version and others receive data shaped by the
  old version, intermittently, for several minutes.
  **Fix:** Both code versions were reading/writing the same cache keys
  with different assumed value shapes (a field added/renamed in the new
  version). Version the cache key itself (`entity:v3:{id}`) whenever a
  deploy changes the cached value's shape, so old and new code paths
  never collide on the same key during a rolling deploy.

## Worked example

**Scenario:** A product page shows price and inventory-availability,
each currently cached with a single shared 60-second TTL and no
invalidation-on-write. Support has flagged two complaints: users
occasionally see a price that was already changed by a promotion, and
every hour on the hour (when a batch price-sync job runs and repopulates
thousands of keys at once) the database sees a load spike.

1. Split the caching strategy by staleness tolerance: price tolerates
   brief staleness (customers rarely notice a few seconds' lag) but
   should invalidate promptly on an explicit price change; inventory
   availability at add-to-cart time should have a much shorter TTL since
   overselling is more costly than a cache miss.
   ```python
   redis.set(f"price:{sku}", price, ex=90)              # base TTL, jittered below
   redis.set(f"inventory:{sku}", qty, ex=15)             # short TTL, staleness-sensitive
   ```
2. Add invalidation-on-write to the price-change code path (cache-aside,
   delete-then-repopulate):
   ```python
   def apply_price_change(sku, new_price):
       db.execute("UPDATE products SET price = %s WHERE sku = %s", new_price, sku)
       redis.delete(f"price:{sku}")
   ```
   This closes the "stale price after an explicit change" complaint
   immediately, independent of the 90-second TTL.
3. Fix the batch-sync thundering herd by jittering TTLs on the sync job
   and adding stampede protection for the highest-traffic SKUs:
   ```python
   jittered_ttl = 90 + random.randint(-15, 15)
   redis.set(f"price:{sku}", price, ex=jittered_ttl)
   ```
4. Verify: price-change complaints stop (confirmed via support ticket
   follow-up over the next release cycle), and the hourly database load
   spike from synchronized batch-sync expiry flattens into a smoother,
   spread-out pattern (confirmed via database CPU/query-rate graphs
   before/after the jitter change).

## Cross-references

- [redis-operations-and-cluster-management](../redis-operations-and-cluster-management/SKILL.md) — the persistence/cluster/memory infrastructure this caching strategy runs on top of, including how `maxmemory-policy` interacts with the TTLs set here.
- [redis-configuration-validation](../redis-configuration-validation/SKILL.md) — validates that the eviction policy and persistence settings actually match the TTL/data-classification assumptions this caching strategy depends on.
- [postgresql-operations-and-performance-tuning](../postgresql-operations-and-performance-tuning/SKILL.md) — the source-of-truth database performance work that a cache-aside layer here is meant to offload; a cache masking an unaddressed slow-query problem is a common anti-pattern worth checking against.
