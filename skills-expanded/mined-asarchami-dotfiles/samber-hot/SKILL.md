---
name: samber-hot
description: "cache — in-memory caching in Go with samber/hot: choose an eviction algorithm (W-TinyLFU, LRU, LFU, S3FIFO, ARC, TwoQueue, SIEVE, FIFO), build a cache with TTL and janitor, size capacity from a memory budget, and monitor hit rate. Use when adopting samber/hot, the codebase imports github.com/samber/hot, or the project repeatedly loads the same resources at high frequency."
license: MIT
---

# samber/hot

**Leading word: cache.** Caching is a system design decision, not a convenience wrapper: choose an eviction algorithm from measured access patterns, size capacity from a memory budget, and plan expiration, loader failures, and monitoring before the cache ever serves a hit.

## Steps — build the cache

1. **Start with `hot.WTinyLFU`.** It is the general-purpose default. Switch algorithms only when the measured miss rate misses the SLO; consult the algorithm table before choosing anything else.
   *Done when: the algorithm is WTinyLFU, or a different choice is justified by a profiled access pattern.*
2. **Chain the builder.** `hot.NewHotCache[K, V](algorithm, capacity)` → `.WithTTL(d)` → `.WithJanitor()` → `Build()`, with `defer cache.StopJanitor()` on the build line. Without the janitor, expired entries stay in memory until eviction.
   *Done when: every cache has a janitor and a deferred StopJanitor.*
3. **Always set a TTL, and add jitter.** Unbounded caches serve stale data indefinitely; `WithJitter(lambda, upperBound)` spreads expirations so items created together don't expire together (thundering herd on the loader).
   *Done when: every cache has a TTL and same-age items are jittered.*
4. **Read through with a loader.** `WithLoaders(func(ids []K) (map[K]V, error))` batch-fetches misses; singleflight dedup means concurrent `Get()`s for the same missing key share one loader invocation. Check `err` as well as `found`.
   *Done when: misses flow through a loader and every `Get` checks err.*
5. **Protect mutable values.** `WithCopyOnRead(fn)` / `WithCopyOnWrite(fn)` for values callers can mutate — otherwise one caller corrupts shared cached state.
   *Done when: any mutable cached value goes through a copy option.*
6. **Configure the missing cache before `SetMissing`.** `WithMissingCache(algorithm, capacity)` or `WithMissingSharedCache()` must be in the builder first — otherwise `SetMissing` panics at runtime.
   *Done when: missing-cache config is present exactly when `SetMissing` is used.*

## Steps — size the capacity

1. **Estimate the per-entry cost.** Size of the struct plus its heap-allocated fields (slices, maps, strings), the key, and ~100 bytes of bookkeeping overhead (pointers, expiry timestamps, algorithm metadata).
2. **Ask for the memory budget.** Get the developer's number for what this cache may use in production (e.g., 256 MB, 1 GB) — it depends on the service's total memory and what else shares the process.
3. **Compute `capacity = budget / itemSize`, rounded down** for headroom. If the item size is unknown, measure it with a unit test that allocates N items and reads `runtime.ReadMemStats`.
   *Done when: capacity is derived from a stated budget and a measured (not guessed) item size.*

## Steps — monitor or diagnose

1. **Wire `WithPrometheusMetrics(cacheName)`.** Hit rate below 80% signals an undersized cache or the wrong algorithm for the workload.
2. **Watch the panic pairs.** `WithoutLocking()` + `WithJanitor()` are mutually exclusive — keep locking whenever background cleanup runs.
   *Done when: hit rate is visible on a dashboard and drives algorithm and capacity changes.*

## Reference

### Algorithm selection

Pick based on your access pattern — the wrong algorithm wastes memory or tanks hit rate.

| Algorithm | Constant | Best for | Avoid when |
| --- | --- | --- | --- |
| **W-TinyLFU** | `hot.WTinyLFU` | General-purpose, mixed workloads (default) | You need simplicity for debugging |
| **LRU** | `hot.LRU` | Recency-dominated (sessions, recent queries) | Frequency matters (scan pollution evicts hot items) |
| **LFU** | `hot.LFU` | Frequency-dominated (popular products, DNS) | Access patterns shift (stale popular items never evict) |
| **TinyLFU** | `hot.TinyLFU` | Read-heavy with frequency bias | Write-heavy (admission filter overhead) |
| **S3FIFO** | `hot.S3FIFO` | High throughput, scan-resistant | Small caches (<1000 items) |
| **ARC** | `hot.ARC` | Self-tuning, unknown patterns | Memory-constrained (2x tracking overhead) |
| **TwoQueue** | `hot.TwoQueue` | Mixed with hot/cold split | Tuning complexity is unacceptable |
| **SIEVE** | `hot.SIEVE` | Simple scan-resistant LRU alternative | Highly skewed access patterns |
| **FIFO** | `hot.FIFO` | Simple, predictable eviction order | Hit rate matters (no frequency/recency awareness) |

### Basic cache with TTL

```go
cache := hot.NewHotCache[string, *User](hot.WTinyLFU, 10_000).
    WithTTL(5 * time.Minute).
    WithJanitor().
    Build()
defer cache.StopJanitor()

cache.Set("user:123", user)
cache.SetWithTTL("session:abc", session, 30*time.Minute)
value, found, err := cache.Get("user:123")
```

### Loader pattern (read-through)

```go
cache := hot.NewHotCache[int, *User](hot.WTinyLFU, 10_000).
    WithTTL(5 * time.Minute).
    WithLoaders(func(ids []int) (map[int]*User, error) {
        return db.GetUsersByIDs(ctx, ids) // batch query
    }).
    WithJanitor().
    Build()
defer cache.StopJanitor()

user, found, err := cache.Get(123) // triggers loader on miss
```

### Capacity example

```
*User struct ~500 bytes + string key ~50 bytes + overhead ~100 bytes = ~650 bytes/entry
256 MB budget → 256_000_000 / 650 ≈ 393,000 items
```

- **[Algorithm Guide](./references/algorithm-guide.md)** — detailed comparison, benchmarks, decision tree
- **[Production Patterns](./references/production-patterns.md)** — revalidation, sharding, missing cache, monitoring
- **[API Reference](./references/api-reference.md)** — complete API surface

## Watch for

| Mistake | Fix |
| --- | --- |
| Forgetting `WithJanitor()` | Chain `WithJanitor()` and `defer cache.StopJanitor()` |
| `SetMissing` without missing cache config | Configure `WithMissingCache` / `WithMissingSharedCache` first |
| `WithoutLocking()` + `WithJanitor()` | Keep locking while background cleanup runs |
| Oversized cache | Size to the working set (10–20% of data), monitor hit rate |
| Ignoring loader errors | Check `err` from `Get`, not only `found` |
| No TTL | Always set TTL so stale data gets refreshed |

## Cross-references

- → See `go-performance` for caching strategy and in-memory vs Redis vs CDN
- → See `go-observability` for Prometheus metrics and monitoring
- → See `go-database` for query patterns that pair with cache loaders
