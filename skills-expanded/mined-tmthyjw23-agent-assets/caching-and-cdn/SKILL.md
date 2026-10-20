---
name: caching-and-cdn
description: >
  Speed up reads with caches and content delivery. Use when adding a cache,
  choosing cache strategy (read-through/write-through/write-behind), eviction
  policy, cache invalidation, Redis vs Memcached, CDN, edge caching, or
  diagnosing cache stampede/penetration/consistency problems. Triggers:
  "caching strategy", "Redis", "CDN", "cache invalidation", "TTL", "eviction".
---

# Caching and CDN

The fastest request is the one you never make. Cache close to the reader.

## When to use
- Read-heavy paths with repeated data.
- Reducing DB load or latency.
- Global content delivery (static + dynamic).
- Cache correctness problems (stale, stampede, penetration).

## Caching layers
1. Client / browser cache (Cache-Control, ETag).
2. CDN / edge cache.
3. Application/service cache (in-memory, e.g. local LRU).
4. Distributed cache (Redis/Memcached).
5. Database cache / buffer pool, materialized views.

## Strategies
| Strategy | Behavior | Use when |
|---|---|---|
| Cache-aside (lazy) | App reads cache, on miss loads DB and fills | General default |
| Read-through | Cache loads from DB on miss | Cache lib abstracts load |
| Write-through | Write cache + DB together | Strong freshness needed |
| Write-behind | Write cache, async flush to DB | Write-heavy, can lose latency |
| Refresh-ahead | Pre-refresh hot keys before TTL | Predictable hot keys |

## Eviction & expiry
- Policies: LRU, LFU, FIFO, TTL, random; `most-popular-cache-eviction.md`,
  `top-8-cache-eviction-strategies.md`.
- TTL + jitter to avoid synchronized expiry.
- Size for working set, not whole dataset.

## Correctness & failure modes
- **Cache penetration:** lookups for missing keys → guard with null caching /
  bloom filter (`cache-miss-attack.md`).
- **Cache stampede/thundering herd:** many misses at once → lock/mutex or
  refresh-ahead + jitter.
- **Cache invalidation:** the hard part. Prefer short TTL + versioned keys /
  event-driven invalidation over trying to invalidate in place.
- **Consistency:** accept staleness explicitly; define max staleness.

## CDN
- Cache static assets aggressively (immutable, hashed filenames).
- Dynamic acceleration: edge compute, origin shielding, tiered cache.
- Purge/invalidation strategy; cache key design (vary by device/locale).
- TTLs: long for static, short for API, no-store for private.

## Checklist
- [ ] Cache strategy chosen and documented.
- [ ] Key design + versioning + TTL/jitter defined.
- [ ] Invalidation strategy stated; max staleness agreed.
- [ ] Penetration/stampede protection.
- [ ] Eviction policy matches access pattern.
- [ ] What to never cache (auth, per-user secrets) identified.
- [ ] Hit ratio + latency + errors monitored.

## Common pitfalls
- Caching without an invalidation plan.
- Caching personalized/private data at shared layers → data leaks.
- Thundering herd on expiry.
- Stale data causing correctness bugs (prices, permissions).
- Unbounded cache memory growth.

## References
- `...\learn-cache.md`, `...\top-5-caching-strategies.md`, `...\what-are-the-top-caching-strategies.md`
- `...\things-to-consider-when-using-cache.md`, `...\how-can-cache-systems-go-wrong.md`
- `...\most-popular-cache-eviction.md`, `...\top-8-cache-eviction-strategies.md`
- `...\cache-miss-attack.md`
- `...\the-ultimate-redis-101.md`, `...\why-is-redis-so-fast.md`, `...\how-can-redis-be-used.md`, `...\how-does-redis-persist-data.md`, `...\memcached-vs-redis.md`
- `...\what-is-cdn-content-delivery-network.md`, `...\how-does-cnd-work.md`, `...\a-beginner's-guide-to-cdn-content-delivery-network.md`
- `...\how-to-load-your-websites-at-lightning-speed.md`, `...\top-9-website-performance-metrics-you-cannot-ignore.md`
Base: `D:\Agent-Assets\system-design-101\data\guides\`

## Related skills
`scalability-and-performance`, `database-design`, `system-design-method`.
