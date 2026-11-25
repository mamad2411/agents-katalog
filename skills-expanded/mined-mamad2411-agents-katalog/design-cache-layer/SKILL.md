---
name: design-cache-layer
description: Design a Redis cache layer — key schema, TTLs, eviction policy, stampede + thundering-herd protection, hot-key + big-key avoidance. Use after caching-tradeoffs picks where; not Redis server config.
---

# design-cache-layer

> Cache design that survives Black Friday, not just the demo. Output: key schema, TTL strategy, write/read path, failure modes considered.

## When to use

- A read-heavy endpoint needs caching.
- An existing cache is causing incidents (stampedes, hot keys, memory pressure).
- A PRD says "use Redis" with no further detail.

## Related skills

- [`polymath-performance:caching-tradeoffs`](../caching-tradeoffs/SKILL.md)
  — vendor-agnostic decision: *what* to cache, *where* to cache,
  staleness tolerance, failure modes. Run that first to decide the
  shape; use this skill to ship the Redis layer.
- [`polymath-performance:audit-redis-config`](../audit-redis-config/SKILL.md)
  — once the cache layer is running, review `maxmemory`, eviction,
  persistence, replication.

## Procedure

1. **Identify the value.** Caching is for *expensive-to-compute, frequently-read, eventually-consistent* values. If the data is cheap to compute or strongly consistent, do not cache.
2. **Key schema.** Structured + versioned:
   ```
   <domain>:<entity>:<id>:v<version>      e.g. refund:profile:42:v3
   <domain>:list:<filter-hash>:v<version> e.g. refund:list:sha8af2:v3
   ```
   The `v<n>` suffix lets a deploy invalidate everything by bumping it; the alternative (deleting keys) is slow on large keyspaces.
3. **TTL strategy.**
   - Per-entry TTL with jitter: `TTL = base ± random(0, base/10)`. Prevents synchronized expiry storms.
   - Sliding TTL only when reads are bursty around a record (re-set on hit).
   - Negative caching: also cache "not found" for a shorter TTL to absorb 404 floods.
4. **Eviction.** `maxmemory-policy = allkeys-lru` for pure caches; `volatile-lru` if you also store non-cache data with no TTL.
5. **Read path with stampede protection.**
   ```
   value = GET key
   if value:
       return value
   # cache miss
   if NOT SET nx:lock:key (NX, EX=5):
       sleep + retry GET key                 # someone else is computing
   else:
       value = expensive_compute()
       SET key value EX=TTL
       DEL nx:lock:key
       return value
   ```
   Single-flight by lock; concurrent misses don't all hammer the origin.
6. **Write path.** Update-then-invalidate (`SET origin = new; DEL key`) is simpler than write-through; tolerate the brief window when a stale read can occur.
7. **Hot keys.** A key with > 1% of total RPS is a hot key. Strategies:
   - Shard the value into multiple keys (`refund:profile:42:shard:{0..9}` round-robin).
   - Use a local in-process cache in front (Caffeine / lru-cache) for sub-second TTL.
8. **Big keys.** A single key > 100KB or a single LIST/HASH with > 10k items is a big key. Cluster mode bites on slot rebalances; split.
9. **Failure modes.**
   - Cache down → origin slammed. Add a circuit breaker that fails open (skip cache) for a short window.
   - Origin slow + cache miss → request hangs. Set a *cache-fill timeout* and serve stale.
10. **Observability.** Hit ratio, miss latency, eviction rate, slow-log entries. Without these, you don't know if the cache is helping or hurting.

## Output

```text
design-cache-layer

Endpoint:   GET /refund/profile/:id
Value:      RefundProfile (~5KB JSON, computed from 4 SQL queries)

Key schema
  refund:profile:<id>:v3                                   primary
  nx:lock:refund:profile:<id>:v3   EX=5s, NX               stampede guard

TTL:        300s ± 30s (jitter)
Negative:   10s for not-found

Eviction:   allkeys-lru, maxmemory ~ 8GB.

Read path:
  GET → on miss, NX-lock → compute → SET EX=jittered → DEL lock.

Write path:
  Update SQL → DEL refund:profile:<id>:v3.

Failure modes covered:
  ✓ stampede via NX lock
  ✓ thundering herd via TTL jitter
  ✓ origin slowness via cache-fill timeout + stale-serve
  ⚠ hot key: monitor; shard if a single id exceeds 1% RPS

Observability: hit ratio, miss latency p99, eviction rate, slow-log.
```

## Quality bar

- Key schema versioned for cheap global invalidation.
- TTL has jitter.
- Stampede protection in the read path.
- Failure modes named, not assumed.

## Anti-patterns to avoid

- TTL without jitter on a hot key. Synchronized expiry → origin stampede.
- Write-through caching for everything. Couples writes to cache latency.
- Forgetting negative caching. 404 floods are real.
- Using Redis as a primary store without persistence understanding. RDB + AOF have different durability stories.
