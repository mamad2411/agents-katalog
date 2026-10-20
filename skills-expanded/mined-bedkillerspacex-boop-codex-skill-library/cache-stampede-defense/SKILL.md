---
name: cache-stampede-defense
description: >
  Prevent cache stampede (thundering herd) on owned systems: single-flight/request
  coalescing, probabilistic early expiration, locking, soft TTL, and negative caching.
  Use when hot key misses overload origin/DB, cache stampede, dogpile effect, or
  synchronized TTL expiry storms — pair with `caching-strategies` for general cache design.
---

# Cache Stampede Defense

## Scope And Authorization

- **In scope:** Caches and origins you operate (Redis, Memcached, CDN, app memory).
- **Out of scope:** Stressing third-party APIs without agreement.
- Reproduce stampede in staging with production-like TTLs and concurrency.
- Redact cache key patterns that embed PII.
- Pair with `caching-strategies`, bulkheads, and `code-quality-standards`.

## When To Use

- Traffic spikes on expiry of popular keys cause DB/origin meltdown.
- Many pods recompute the same miss simultaneously.
- CDN origin shield insufficient alone for app-level hot keys.
- Negative lookups (missing rows) hammer the DB.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General cache TTLs, layers, invalidation | `caching-strategies` |
| CDN cache key design | `cdn-cache-key-design` |
| HTTP caching headers only | CDN/HTTP cache skills |
| DB query optimization root cause | database skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Technique | Idea |
| --- | --- |
| Single-flight / coalescing | One in-flight compute per key; others wait |
| Mutex / lock | Distributed lock around recompute |
| Probabilistic early expire | Refresh before TTL with randomness |
| Soft/hard TTL | Serve stale while refresh (stale-while-revalidate) |
| Negative cache | Cache misses briefly |
| Origin shield / request collapsing | Edge coalescing (CDN) |

## Workflow

### 1. Confirm scope and success criteria

1. Identify hot keys, origin cost per miss, SLOs.
2. Success: under synchronized expiry, origin QPS for key remains ~1 (or small constant), not = concurrent clients.
3. Decide staleness tolerance for each data class.

### 2. Prove stampede

```bash
# Staging: set short TTL on hot key; parallel fetch
# Observe origin/DB QPS spike at expiry
redis-cli TTL "product:42"
# app metrics: cache_miss_total{key_class=product}, db_query_total
```

1. Correlate dashboards: miss rate ↑ and DB CPU ↑ together.
2. Confirm no dogpile control in client library.

### 3. Choose defenses by constraint

| Constraint | Prefer |
| --- | --- |
| Stale OK for hundreds of ms–seconds | Soft TTL + background refresh |
| Must be fresh; can wait | Single-flight wait on lock |
| Multi-region independent caches | Probabilistic early expire + single-flight per region |
| Missing keys hot | Negative cache with short TTL |
| CDN layer | Origin shield + SWR headers where applicable |

### 4. Implement patterns

**Single-flight (process-local sketch):**

```python
# One compute per key in this process; still need distributed lock multi-pod
_futures = {}
async def get(key):
    if (v := await cache.get(key)) is not None:
        return v
    fut = _futures.get(key)
    if fut is None:
        fut = asyncio.create_task(compute_and_set(key))
        _futures[key] = fut
        try:
            return await fut
        finally:
            _futures.pop(key, None)
    return await fut
```

**Distributed lock recompute (Redis):**

```text
1. GET key → hit return
2. SET lock:key NX PX 5000
3. if got lock: compute; SET key; DEL lock; return
4. else: brief sleep/backoff; retry GET (optionally wait)
```

**Probabilistic early expiration (XFetch-style):**

```python
def should_recompute(ttl_remaining, beta=1.0, expiry=None):
    # if random() * delta * beta < expiry - now → recompute early
    ...
```

**Stale-while-revalidate:**

```text
value = { data, soft_exp, hard_exp }
if now < soft_exp: return data
if now < hard_exp: return data + async refresh
else: blocking refresh with single-flight
```

**Negative cache:**

```text
cache SET key=__NULL__ TTL=30s on miss
```

### 5. Wire limits and fallbacks

1. Lock TTL must exceed compute p99 or use fencing tokens / extend.
2. On compute failure: do not leave permanent lock; serve stale if available.
3. Bulkhead origin compute (`bulkhead-isolation`).
4. Metrics: `stampede_lock_wait`, `stale_served`, `recompute_total`, origin QPS per key class.

### 6. Verify

```bash
# Load test: concurrent clients after flush of one hot key
k6 run stampede_hotkey.js
# Expect: origin computations ≈ 1 per expiry window (plus early refresh rate)
```

1. Multi-pod test (not only single process single-flight).
2. Failure test: origin errors during recompute — users get stale or controlled error.
3. Watch lock contention metrics for hot key fair behavior.

### 7. Hand off

1. Document per key class: TTL, soft TTL, lock strategy, staleness SLO.
2. Alert on origin QPS spike correlated with miss storms.
3. Apply `code-quality-standards`; avoid per-key unbounded wait queues.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Miss storm | Single-flight + SWR | Everyone hits DB on miss |
| Expiry | Jittered / probabilistic | Identical TTL all keys same second |
| Locks | Short TTL + extend | Lock forever on crash |
| Negatives | Short NULL cache | Cache nothing → repeat miss |
| Stale | Explicit soft TTL | Silent forever stale |
| Proof | Multi-pod load evidence | Unit test only |

## Output Checklist

- [ ] Hot keys and origin cost documented
- [ ] Stampede reproduced in staging
- [ ] Defense technique chosen per class
- [ ] Multi-instance safe (not only local)
- [ ] Metrics for recompute/stale/lock
- [ ] Load verification shows collapsed origin load
- [ ] Failure modes defined
- [ ] Runbook/alerts updated
- [ ] `code-quality-standards` applied

## Rules

- Process-local single-flight is not enough for multi-replica systems.
- Prefer serving brief stale over melting the database when policy allows.
- Always jitter or probabilistic-refresh synchronized expirations.
- Authorized load tests only.
- General caching design → `caching-strategies`.
