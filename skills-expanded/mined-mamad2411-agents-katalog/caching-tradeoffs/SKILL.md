---
name: caching-tradeoffs
description: Design a cache — what's cached, where (local / regional / shared), invalidation strategy, staleness tolerance, named failure modes (stampede, poisoning, drift). Strategy, not Redis key/TTL design.
---

# caching-tradeoffs

> "There are only two hard things …" The trade-offs are real. Output is the cache shape + an explicit decision on each of the five hard questions.

## When to use

- Adding caching to a new code path.
- An existing cache misbehaves (high miss rate, stampedes, stale UI).
- A perf budget needs cache help and you want to scope it correctly.

## Related skills

- [`polymath-performance:design-cache-layer`](../design-cache-layer/SKILL.md)
  — Redis-specific implementation: key schema, eviction policy,
  persistence, replication. Use `caching-tradeoffs` first to decide
  the cache *shape*; then `design-cache-layer` to ship the Redis
  layer.
- [`polymath-performance:audit-redis-config`](../audit-redis-config/SKILL.md)
  — review an existing Redis configuration once a cache layer is
  running.

## The five hard questions

A cache design that doesn't have an answer to each of these is a bug nursery.

1. **What's cached?** Exact request signature → exact response. Be specific: `(method, path, sorted query params, auth-tier, region)` not "the API response".
2. **Where does it live?**
   - **In-process LRU**: fastest; per-process, lost on restart.
   - **Sidecar / local Redis**: per-host; shared within a host.
   - **Shared regional cache (Redis/Memcached cluster)**: shared across hosts; ~1ms.
   - **CDN edge cache**: shared across regions; ~10ms first byte; only for cacheable HTTP responses.
   Layering is OK; each layer adds an explicit hit-rate goal.
3. **Invalidation**: how does a cached entry stop being correct?
   - **TTL** — simplest. Pick from the staleness tolerance.
   - **Write-through invalidation** — write to source + cache atomically (or near-atomically).
   - **Pub/sub bust** — writers publish "key X invalid"; readers subscribe.
   - **Versioned keys** — cache keys include a content version, so new versions don't collide.
   Avoid "manual flush" as the primary mechanism; it's an outage waiting.
4. **Staleness tolerance**: how stale can the cached entry be before users notice / lose money / get hurt? This is a product decision, not a technical one. Surface and pin.
5. **Failure modes** — name and design around each:
   - **Cache stampede**: cache miss + many concurrent requests → many duplicate computes. Mitigate with single-flight (locking-on-miss) or request-coalescing.
   - **Cache poisoning**: a bad write contaminates many reads. Mitigate with versioned keys + write validation.
   - **Cache drift**: cache + source diverge silently. Mitigate with periodic full-scan reconciliation + alerts on divergence rate.
   - **Hot key**: one key absorbs disproportionate traffic. Mitigate with local LRU layer in front of the shared cache.

## Procedure

1. Answer the 5 questions explicitly. If you can't answer one, you don't have a cache design yet.
2. Estimate the hit rate. Below 80% hit rate, the cache is often net cost (extra latency on miss + extra system to operate). Re-design or skip.
3. Decide the layer(s). Most services need only one cache layer; resist stacking until measured.
4. Decide the warming path (cold cache after deploy / instance start). Pre-warm? Accept the slow first wave? Document.
5. Decide the observability — hit rate, miss rate, eviction rate, P99 latency for hit vs miss; alert when hit rate drops > 20% from baseline.

## Output

```text
Cache design: <name>

What's cached:
  Key:     (GET, /v1/refunds, order_id, user_tier)
  Value:   serialized Refund proto, ~2KB.
  TTL:     5 minutes (staleness tolerance below).

Where:
  Layer 1: in-process LRU, 50k entries, ~200ns hit.
  Layer 2: regional Redis cluster, ~1ms hit.
  (No CDN; response is per-user.)

Invalidation:
  TTL 5 min + versioned keys (version bumps on Refund schema change).
  No active bust on write — staleness window accepted.

Staleness tolerance:
  Up to 5 minutes. Confirmed with product: refund-status pages are
  acceptable to show "processing" for 5 min after backend transitions
  to "succeeded".

Failure modes (explicit):
  - Stampede: single-flight via Redis SETNX lock on miss; max 1s lock.
  - Poisoning: keys versioned; validation on write rejects malformed.
  - Hot key: in-process LRU layer absorbs hot keys before they hit Redis.
  - Drift: nightly cron reconciles 100k random keys; alert on > 0.1%
    divergence.

Expected hit rate: 85% (modeled from current request distribution).
Below 80% triggers a re-design review.

Observability:
  - cache_hit_total, cache_miss_total, cache_eviction_total counters.
  - Hit-vs-miss latency histograms (p99 each).
  - Alert: hit_rate < 65% for 15 min → page sev3.
```

## Quality bar

- All 5 questions explicitly answered.
- Failure modes named and mitigated.
- Hit-rate estimate present (and ≥ 80% target).
- Observability defined (not "we'll add metrics later").

## Anti-patterns to avoid

- "Add a cache" without the 5 questions answered.
- Stacking 3 cache layers without measuring hit rate per layer.
- TTL alone for entries that must invalidate on write.
- No staleness tolerance pinned — engineering picks one, product is surprised.
