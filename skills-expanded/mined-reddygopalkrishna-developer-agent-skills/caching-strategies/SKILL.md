---
name: caching-strategies
description: Designs caches that stay correct, covering where to cache (browser, CDN, application, distributed), cache-aside vs write-through, key design, TTLs, invalidation, stampede protection and HTTP Cache-Control headers. Use when adding Redis, Memcached, a CDN or HTTP caching, when users see stale data or cache hit rates are low, or when someone proposes caching a slow endpoint or query. Not for finding why code is slow (see performance-profiling) or tuning queries (see sql-optimization).
license: MIT
---

# Caching Strategies

A cache is a second copy of data that is allowed to be wrong for a bounded time. Before adding one, write down three things: how stale the data may be, how it gets invalidated, and what happens when the cache is down or empty. If you cannot answer all three, do not add the cache yet.

## When to use

- Adding Redis, Memcached, an in-process cache, a CDN, or HTTP cache headers.
- Users see stale or wrong data, or one user sees another user's data.
- Hit ratio is low, evictions spike, or the database falls over when the cache restarts.
- Someone proposes "just cache it" for a slow endpoint or query.

Not for: finding the slow code path (performance-profiling) or fixing a slow query (sql-optimization). Fix those first when you can; a cache in front of a missing index hides the problem and adds a consistency problem.

## Workflow

1. **Measure first.** Confirm the slow path with numbers: p95 latency, request rate, source load (DB CPU, QPS). Check whether fixing the query or call is cheaper than caching it.
2. **Characterize the data.** Read/write ratio, value size, number of distinct keys, who may see it (public, per tenant, per user), and the staleness budget per field ("prices may be 60 s old; account balances never").
3. **Pick the layer** using the table below.
4. **Pick the pattern.** Default to cache-aside with a TTL and delete-on-write.
5. **Design keys and TTLs** (rules below).
6. **Design invalidation** and write the consistency contract in a comment or doc next to the code.
7. **Protect hot keys** against stampedes, and define behavior when the cache is down.
8. **Instrument** hit ratio, latency, evictions and errors. Load test a cold cache.
9. **Roll out behind a flag.** For critical data, compare cached and uncached results in shadow mode before trusting the cache.

## Where to cache

| Layer | Good for | Watch out for |
| --- | --- | --- |
| Browser HTTP cache | Static assets; per-user GET responses marked `private` | You cannot purge it. Control is only headers and URL versioning |
| CDN / shared proxy | Public pages, assets, public API responses | Must never store personalized responses. A wrong cache key or `Vary` leaks data |
| In-process memory | Small, hot, rarely changing data (config, reference tables) | Each instance has its own copy, so instances disagree. Bound the size. Lost on restart |
| Distributed cache (Redis, Memcached) | Data shared across instances, sessions, rate-limit counters | Extra network hop; becomes a critical dependency; evictions |
| Database side (materialized views, summary tables) | Expensive aggregates and reports | Refresh cost and staleness between refreshes |

A two-level cache (in-process with a short TTL in front of a distributed cache) works for very hot keys, but keep the local TTL short because there is no cross-instance invalidation unless you build a broadcast.

## Patterns

| Pattern | How it works | Use when | Risk |
| --- | --- | --- | --- |
| Cache-aside (lazy loading) | Read: get from cache; on miss load from source and set with TTL. Write: update the source, then delete the key | The default for application caches | A race can re-insert a stale value; first read after expiry is slow |
| Read-through | A cache library calls a loader on miss | You want loading logic in one place | Same as cache-aside |
| Write-through | Writes update source and cache synchronously | Reads right after writes must hit a fresh cache | Slower writes; caches data nobody reads |
| Write-behind (write-back) | Writes go to the cache and are flushed to the source later | Very high write volume where some loss is acceptable (view counters) | Data loss on crash, ordering bugs. Never use for business records |
| Refresh-ahead | Popular keys are refreshed before they expire | Predictable hot keys with expensive loads | Wasted work on keys nobody reads anymore |

## Keys

- **Include every input the value depends on**: entity ID, tenant ID, user ID when the value is per user, locale, currency, feature-flag variant, API or schema version. A missing input means serving the wrong data to someone.
- **Namespace and version**: `app:v3:product:{tenantId}:{productId}`. To invalidate everything after a format change, bump the version prefix instead of flushing the whole cache.
- **Normalize** inputs before building keys (sort query parameters, lowercase where case does not matter) so equal requests share one entry.
- **Bound key length**: hash long inputs with a stable hash (for example SHA-256 of the normalized query string).
- **Serialize with a schema-tolerant format**, or put the schema version in the key so a deploy with a new format does not read old entries.

## TTLs

- Give every entry a TTL, even when you also invalidate explicitly. The TTL is the safety net for invalidations you missed.
- Derive the TTL from the staleness budget, not from the hit ratio you want.
- Add jitter (for example ±10-20%) so entries written together do not expire together.
- Use a shorter TTL for negative results ("not found").

## Invalidation

| Strategy | How | Staleness |
| --- | --- | --- |
| TTL only | Entries expire | Up to the TTL |
| Delete on write | After the source write commits, delete the key | Small race window (below) |
| Versioned keys | Put the entity's version or `updated_at` in the key | None for readers who know the version; old entries age out |
| Event-driven | Publish change events (outbox or CDC); consumers delete keys | Event delivery lag; works across services |
| Tag / surrogate-key purge | Tag CDN or cache entries and purge by tag | Purge propagation time |

Rules:

- **Delete, do not update, on write.** Updating the cache from the writer can race with another writer and leave the older value in place.
- **Invalidate after the transaction commits**, not before. Deleting first lets a concurrent reader reload the old row and cache it again.
- **Know the cache-aside race:** reader misses and reads the old row; writer commits and deletes the key; reader then writes the old value. The TTL bounds it. When that is not acceptable, use versioned keys or a compare-and-set on a version field.
- In-process caches are not invalidated across instances. Keep their TTL short or add a pub/sub broadcast.

## Stampede protection

When a hot key expires, many requests miss at once and all hit the source.

- **Request coalescing (single-flight):** one load per key per process; other callers wait for that result. Go has `golang.org/x/sync/singleflight`; elsewhere, keep a map of in-flight futures/promises per key.
- **Distributed lock for expensive loads:** `SET lock:{key} {random-token} NX PX 10000` in Redis. Only the holder loads; others serve the stale value or wait briefly. Release only if the token still matches, and let the expiry handle crashed holders.
- **Soft and hard TTL (stale-while-revalidate):** after the soft TTL, one request refreshes in the background while others get the stale value; after the hard TTL, the entry is gone.
- **Probabilistic early refresh:** refresh with a probability that rises as expiry approaches, so refreshes spread out.
- **Warm critical keys** on deploy or failover when a cold cache would overload the source.

## Negative caching

Cache "not found" results with a short TTL so repeated lookups for missing IDs (bots, typos, enumeration) do not reach the database. Delete the negative entry when the item is created.

## Failure behavior

- A cache outage must not take the application down. Use short timeouts on cache calls (tens of milliseconds), then fall back to the source with load shedding or a circuit breaker (see resilience-patterns).
- Check whether the source survives a 100% miss rate. If it does not, record that as a capacity risk and plan warming or rate limiting.
- Set the eviction policy on purpose. Redis defaults to `maxmemory-policy noeviction` (writes fail when memory is full); a pure cache usually wants `allkeys-lru` or `allkeys-lfu`. Check with `CONFIG GET maxmemory-policy`.
- Never store data only in the cache unless it is deliberately configured as a durable store.
- Flushing a production cache, changing eviction policy, or purging a CDN is a production change: stop and get confirmation first, and say what load the source will take.

## HTTP caching quick defaults

| Response | `Cache-Control` |
| --- | --- |
| Fingerprinted static assets (`app.3f9a1c.js`) | `public, max-age=31536000, immutable` |
| HTML documents | `no-cache` plus an `ETag`, so browsers revalidate each time |
| Public API GET that may be briefly stale | `public, max-age=60, stale-while-revalidate=30` |
| Per-user responses | `private, no-cache` |
| Sensitive data (account pages, tokens, PII) | `no-store` |

- `no-cache` means "store, but revalidate before use". `no-store` means "do not store".
- `s-maxage` sets the lifetime for shared caches (CDNs) separately from browsers.
- Always send an explicit `Cache-Control`. Without one, caches may apply heuristic freshness to responses that have `Last-Modified`.
- `Vary` must list request headers that change the response (`Accept-Encoding`, `Accept-Language`). `Vary: Cookie` or `Vary: Authorization` usually defeats a CDN; do not share-cache those responses at all.
- Prefer versioned URLs over CDN purges.

Read [references/http-caching.md](references/http-caching.md) when setting headers, configuring a CDN cache key, or debugging why a response was or was not cached.

## Security

- Per-user or per-tenant data never goes into a shared cache under a key without the user or tenant ID.
- Make sure the CDN never caches responses that carry `Set-Cookie` or depend on `Authorization`, and that it honors `private` and `no-store`.
- Cache poisoning: request headers that change the response (for example `X-Forwarded-Host`) but are not part of the cache key let an attacker store a malicious response for everyone. Either add such headers to the key or stop them from affecting the response.
- Cache servers should not be reachable from the internet and should require authentication and TLS where the network is not trusted.

## Metrics

- Hit ratio per key prefix, hit vs miss latency, evictions, memory used, key count, cache errors and timeouts, and source load.
- Alert on a sudden hit-ratio drop and on eviction spikes.
- For HTTP, inspect `Age` and the CDN's cache status header when debugging.

## Anti-patterns

- **Caching to hide a missing index or N+1 query.** Fix the query first.
- **No TTL.** One missed invalidation keeps wrong data forever.
- **Updating the cache on write** instead of deleting the key.
- **Invalidating before the commit.**
- **Shared cache key without the user or tenant.** This is a data leak, not a performance bug.
- **Treating the cache as the source of truth.**
- **Caching errors** (5xx, timeouts) for long periods. Cache failures, if at all, only for seconds.
- **Unbounded in-process maps** used as caches. Use a size-bounded LRU.
- **Caching everything "just in case".** A low hit ratio adds latency, memory cost and bugs.

## Done when

- The staleness budget, invalidation method and cache-down behavior are written next to the code.
- Keys include every input; per-user and per-tenant data is never shared unkeyed.
- Every entry has a TTL with jitter; hot keys have stampede protection.
- Tests cover hit, miss, invalidation after a write, and cache unavailable.
- Hit ratio, evictions and latency are on a dashboard, and the source is known to survive a cold cache.

## References

- [references/http-caching.md](references/http-caching.md) — read when choosing `Cache-Control` directives, setting up a CDN, or checking headers with curl.
