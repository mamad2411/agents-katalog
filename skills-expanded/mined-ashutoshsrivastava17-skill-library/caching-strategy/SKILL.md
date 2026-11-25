---
name: caching-strategy
description: >
  Design caching layers — cache placement (CDN/app/DB), invalidation
  strategies, TTL policies, cache warming, and consistency tradeoffs.
  TRIGGER when: user says /caching-strategy, needs to design caching,
  or asks about cache invalidation, TTL, or performance optimization via caching.
argument-hint: "[system or endpoint to cache]"
user-invocable: true
---

# Caching Strategy

You are a performance engineering specialist. Design caching strategies that balance speed, consistency, and complexity.

## Process

### Step 1: Identify What to Cache

| Signal | Indicates Good Cache Candidate |
|--------|-------------------------------|
| High read frequency | Same data requested often |
| Low write frequency | Data doesn't change often |
| Expensive to compute | Heavy queries, aggregations |
| Latency-sensitive | User-facing, real-time requirements |
| Predictable access | Known hot keys, popular items |

**Anti-patterns — do NOT cache:**
- Highly personalized data that's unique per request
- Data that changes every second and requires real-time accuracy
- Security-sensitive data that could leak across users

### Step 2: Choose Cache Placement

| Layer | Technology | Latency | Use Case |
|-------|-----------|---------|----------|
| CDN | CloudFront, Fastly, Cloudflare | ~10ms | Static assets, public API responses |
| Application (in-process) | Local hashmap, Caffeine | <1ms | Hot config, session data, small datasets |
| Distributed cache | Redis, Memcached | 1-5ms | Shared state, sessions, query results |
| Database cache | Query cache, materialized views | 5-20ms | Complex aggregations, read replicas |
| Client-side | Browser cache, service worker | 0ms | Static resources, offline support |

### Step 3: Select Invalidation Strategy

| Strategy | How It Works | Consistency | Complexity |
|----------|-------------|-------------|-----------|
| TTL-based | Expire after fixed time | Eventual (bounded) | Low |
| Event-driven | Invalidate on write/update event | Near-real-time | Medium |
| Write-through | Write to cache + DB simultaneously | Strong | Medium |
| Write-behind | Write to cache, async flush to DB | Eventual | High |
| Cache-aside | App manages read/write (most common) | Eventual | Low |
| Versioned keys | Append version to cache key | Strong | Low |

### Step 4: Design TTL Policy

| Data Type | TTL | Rationale |
|-----------|-----|-----------|
| Static config | 1-24 hours | Rarely changes, low risk |
| User profiles | 5-15 minutes | Changes occasionally, moderate staleness OK |
| Search results | 1-5 minutes | Freshness matters, moderate read volume |
| Real-time data | 10-30 seconds | High freshness need |
| Auth tokens | Match token lifetime | Security requirement |

### Step 5: Handle Cache Failures

| Failure Mode | Mitigation |
|-------------|-----------|
| Cache miss storm | Cache warming, request coalescing (singleflight) |
| Hot key | Replicate across shards, local cache in front |
| Cache stampede | Mutex/lock on cache population, stale-while-revalidate |
| Cache unavailable | Graceful degradation to database (with circuit breaker) |
| Stale data served | Version-based invalidation, manual purge API |
| Memory pressure | LRU eviction, TTL limits, max memory config |

### Step 6: Monitor and Tune

| Metric | Target | Action if Off |
|--------|--------|--------------|
| Hit rate | > 90% | Review what's being cached, adjust TTLs |
| Latency (p95) | < 5ms | Check network, connection pooling |
| Eviction rate | Low and steady | Increase memory or reduce TTLs |
| Memory usage | < 80% capacity | Right-size or evict more aggressively |
| Stale serve rate | < 1% | Tighten TTLs or add event invalidation |

## Output Format

```markdown
## Caching Strategy: [System/Endpoint]

### What's Cached: [Data types with TTLs]
### Placement: [Layer and technology]
### Invalidation: [Strategy per data type]
### Failure Handling: [Degradation plan]
### Monitoring: [Key metrics and targets]
```

## Quality Checklist

- [ ] Only cache data that benefits from caching (high read, low write)
- [ ] Invalidation strategy matches consistency requirements
- [ ] TTLs are appropriate for data freshness needs
- [ ] Cache failures degrade gracefully
- [ ] No user data leaks across cache entries (cache key includes user context)
- [ ] Monitoring covers hit rate, latency, and evictions

## Edge Cases

- For multi-region, decide between local caches (fast but inconsistent) vs global cache (consistent but slower)
- For authenticated data, include user/tenant ID in cache keys
- If cache size is limited, use LRU + TTL together
- For write-heavy workloads, caching may not help — profile first
- For GraphQL, cache at the resolver level, not the query level
