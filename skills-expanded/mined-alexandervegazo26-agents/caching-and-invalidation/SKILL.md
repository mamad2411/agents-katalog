---
name: caching-and-invalidation
version: 1.0.0
description: Cache invalidation strategies and staleness failure modes — what to actually check for stale reads, read-your-own-writes violations, cache stampedes, and multi-layer inconsistency. Use whenever software-engineer or database-engineer introduces a cache layer, and whenever qa-engineer or site-reliability investigates a staleness or consistency issue involving one. Do NOT use for cross-service consistency models or replication lag as a distributed-design question — that is `distributed-systems`.
---

# Caching and Invalidation

## Why this is hard
A cache is a second copy of the truth, maintained for speed, that must be kept consistent with the first copy without being told about every change automatically. Every caching bug is some version of: the second copy stopped agreeing with the first, and nothing noticed.

## Invalidation strategies
- **TTL (time-to-live)** — simplest, but creates a window where staleness is guaranteed by design, not a bug; the question is only whether that window is short enough to be acceptable for this data.
- **Write-through** — write to cache and source simultaneously; strong consistency, but every write pays the cache-write cost and a failure mid-write can leave them disagreeing unless handled explicitly.
- **Write-behind** — write to cache immediately, propagate to source asynchronously; fast, but a crash before propagation loses the write, and readers of the source-of-truth (not the cache) see stale data in the interim.
- **Explicit invalidation on write** — the write path actively evicts or updates the affected cache entries. Correct in principle, wrong in practice whenever there's a write path that doesn't go through the code responsible for invalidation (a direct DB write, a batch job, an admin tool) — audit every way the underlying data can change, not just the primary application path.
- **Event-driven invalidation** — a change event (e.g., a database change-data-capture stream) triggers invalidation, decoupling the writer from needing to know about the cache. More robust to the "forgot one write path" problem, at the cost of eventual (not immediate) consistency and a new failure mode if the event pipeline itself lags or drops events.

## Staleness failure classes to specifically test for
- **Read-your-own-writes violation** — a user updates something and then immediately reads a stale cached version of their own change. Especially likely with any layer of caching between the write path and the read path (CDN, application cache, read replica lag).
- **Stale-after-update** — the general case above, for any reader, not just the writer.
- **Thundering herd / cache stampede** — a hot key expires and many concurrent requests simultaneously miss the cache and hit the source at once, which can look like a load spike or outage unrelated to the actual cause. Mitigate with jittered TTLs, request coalescing, or a lock/single-flight pattern around cache population.
- **Cached error / negative caching gone wrong** — caching a failure or empty result and serving it long after the underlying condition that caused it has resolved.
- **Partial invalidation** — a change affects multiple cache keys or layers, and only some are invalidated, leaving the cache internally inconsistent even though each individual entry is "valid" against some past state.

## Multi-layer caching
Real systems often stack a browser cache, a CDN, an application-level cache, and a database query cache — and invalidation must actually propagate through every layer that's in front of the change, or the layers disagree with each other, not just with the source of truth. When diagnosing a "stale data" report, identify which layer is actually serving the stale response before assuming it's the application cache — it's frequently not.

## Testing cache behavior explicitly
- Test the cache-hit path and the cache-miss path as two separate cases, not as one path that "usually hits." A bug that only manifests on miss (e.g., a race during population) won't show up if tests only ever exercise a warm cache.
- Test that invalidation actually propagates end-to-end after a write — not just that the invalidation call was made, but that a subsequent read reflects the change.
- Test concurrent writes during cache population (the thundering-herd scenario) explicitly if the traffic pattern makes it plausible, rather than assuming single-request testing generalizes. That population race is a concurrency bug specifically — see `concurrency-and-thread-safety`.
- The metamorphic relation "cached and uncached reads agree" (per `qa-engineer`'s technique set) is the right invariant to check directly — force one path through the cache and one around it for the same underlying data, and diff the results.
