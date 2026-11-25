---
name: "caching-patterns"
description: "Caching patterns with code: cache-aside, write-through, write-behind for counters, probabilistic early recomputation against stampedes, Redis sorted-set rate limiting, cache warming, and the anti-patterns that leak data or serve stale results. Use when adding or reviewing a cache."
---

# Caching Patterns

> Named patterns with code examples for cache-aside, write-through, write-behind, cache stampede prevention (PER), Redis data structure selection, CDN cache headers, and cache warming strategies.

## Patterns

### Pattern: Cache-Aside (Lazy Loading)

The most common caching pattern. Application checks cache first; on miss, loads from database and populates cache. Cache holds only data that has been requested at least once.

```typescript
// TypeScript — cache-aside with Redis
import { createClient } from 'redis';

const redis = createClient({ url: 'redis://redis.internal:6379' });

interface UserProfile {
  id: string;
  name: string;
  email: string;
  tier: string;
}

async function getUserProfile(userId: string): Promise<UserProfile> {
  const cacheKey = `user:profile:${userId}`;
  const TTL_SECONDS = 300;  // 5 minutes tolerable staleness

  // 1. Check cache
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached) as UserProfile;
  }

  // 2. Cache miss — load from database
  const user = await db.query(
    'SELECT id, name, email, tier FROM users WHERE id = $1',
    [userId]
  );
  if (!user) throw new NotFoundError(`User ${userId} not found`);

  // 3. Populate cache (do NOT await — fire and forget to reduce latency)
  redis.setEx(cacheKey, TTL_SECONDS, JSON.stringify(user))
    .catch(err => logger.warn('Cache write failed', { userId, err }));

  return user;
}
```

Cache invalidation — delete on write:
```typescript
async function updateUserTier(userId: string, tier: string): Promise<void> {
  await db.query('UPDATE users SET tier = $1 WHERE id = $2', [tier, userId]);
  await redis.del(`user:profile:${userId}`);  // Invalidate — next read repopulates
}
```

### Pattern: Write-Through

Application writes to cache and database atomically. Cache never contains stale data. Use when reads are much more frequent than writes and the cost of a cache miss is high.

```java
// Java — write-through with Redis and PostgreSQL
@Service
public class ProductCatalogService {

    private final RedisTemplate<String, Product> redis;
    private final ProductRepository repo;
    private static final Duration TTL = Duration.ofMinutes(30);

    public Product updateProduct(String productId, ProductUpdate update) {
        // Write to database first
        Product saved = repo.save(productId, update);

        // Write to cache immediately — keeps cache current
        String cacheKey = "product:" + productId;
        redis.opsForValue().set(cacheKey, saved, TTL);

        return saved;
    }

    public Optional<Product> getProduct(String productId) {
        String cacheKey = "product:" + productId;

        // Cache should always have it (if write-through is consistently applied)
        Product cached = redis.opsForValue().get(cacheKey);
        if (cached != null) return Optional.of(cached);

        // Cold start or eviction — load from DB, repopulate
        return repo.findById(productId)
            .map(product -> {
                redis.opsForValue().set(cacheKey, product, TTL);
                return product;
            });
    }
}
```

### Pattern: Write-Behind (Write-Back) for Counters

Write to cache immediately, flush to database asynchronously. High write throughput with eventual persistence. Only for data where loss of recent writes is acceptable (view counts, likes, non-financial counters).

```python
# Python — write-behind for page view counters
import redis
import threading

r = redis.Redis(host='redis.internal', decode_responses=True)

def increment_page_view(page_id: str):
    """Immediate in-memory increment; DB flush is async."""
    key = f"views:{page_id}"
    r.incr(key)
    r.expire(key, 3600)  # Keep key alive for 1 hour

def flush_to_database():
    """Run periodically (e.g., every 60s) to flush counters to DB."""
    pattern = "views:*"
    cursor = 0
    while True:
        cursor, keys = r.scan(cursor, match=pattern, count=100)
        for key in keys:
            page_id = key.split(':')[1]
            count = r.getdel(key)  # Atomic get + delete
            if count:
                db.execute(
                    "INSERT INTO page_views (page_id, count, recorded_at) VALUES (%s, %s, NOW()) "
                    "ON CONFLICT (page_id) DO UPDATE SET count = page_views.count + EXCLUDED.count",
                    [page_id, int(count)]
                )
        if cursor == 0:
            break

# Run flush on schedule
scheduler = threading.Timer(60, flush_to_database)
scheduler.daemon = True
scheduler.start()
```

### Pattern: PER (Probabilistic Early Recomputation) — Stampede Prevention

The mathematically optimal algorithm for preventing cache stampede (Vattani et al., VLDB 2015). A request proactively refreshes the cache entry before expiry with probability proportional to how close to expiry the entry is. No coordination or locks needed.

```python
import math, random, time, json
from typing import Callable, TypeVar

T = TypeVar('T')

def get_with_per(
    redis_client,
    key: str,
    compute_fn: Callable[[], T],
    ttl: int,
    beta: float = 1.0,
) -> T:
    """
    Probabilistic Early Recomputation.
    beta: tuning parameter. 1.0 is optimal for most cases.
    Higher beta = more aggressive early refresh (more background computation, less stampede risk).
    """
    raw = redis_client.get(key)
    if raw is not None:
        entry = json.loads(raw)
        remaining = redis_client.ttl(key)  # seconds remaining
        delta = entry.get('delta', 1.0)    # last compute time in seconds

        # Probabilistic early refresh decision
        if -delta * beta * math.log(random.random()) >= remaining:
            # This caller refreshes early; others continue serving cached value
            t0 = time.monotonic()
            value = compute_fn()
            delta = time.monotonic() - t0
            redis_client.setex(key, ttl, json.dumps({'v': value, 'delta': delta}))
            return value
        return entry['v']

    # Cache miss — compute and populate
    t0 = time.monotonic()
    value = compute_fn()
    delta = time.monotonic() - t0
    redis_client.setex(key, ttl, json.dumps({'v': value, 'delta': delta}))
    return value
```

### Pattern: Redis Sorted Set for Sliding Window Rate Limit

Use ZADD with timestamp as score. ZREMRANGEBYSCORE removes old entries. ZCARD counts current window.

```python
def is_rate_limited(redis_client, user_id: str, limit: int, window_seconds: int) -> bool:
    """
    Sliding window rate limit using Redis Sorted Set.
    Complexity: O(log N) per request. Precise — no boundary burst.
    """
    now = time.time()
    window_start = now - window_seconds
    key = f"rl:user:{user_id}"

    pipe = redis_client.pipeline()
    pipe.zremrangebyscore(key, 0, window_start)           # Remove expired entries
    pipe.zadd(key, {str(now): now})                        # Add current request
    pipe.zcard(key)                                         # Count requests in window
    pipe.expire(key, window_seconds + 1)
    results = pipe.execute()

    request_count = results[2]
    return request_count > limit
```

### Pattern: Cache Warming Before Deploy

Prevents cold-cache database spike after deployment:

```bash
#!/bin/bash
# cache-warm.sh — run before deploying new instance to production

echo "Warming cache for top-100 products..."
psql $DATABASE_URL -t -c "SELECT id FROM products ORDER BY view_count DESC LIMIT 100" | \
  while read product_id; do
    curl -s -H "X-Internal: cache-warm" "http://localhost:8080/api/products/$product_id" > /dev/null
    echo "Warmed product:$product_id"
  done

echo "Warming cache for active user sessions..."
# Sessions are already in Redis from previous instance — no action needed

echo "Cache warm complete. Proceed with traffic cutover."
```

## Anti-Patterns

### Anti-Pattern: Caching Without Namespace (Shared Cache Cross-Tenant Leak)

**Incident type**: Multi-tenant SaaS, customer A's data served to customer B because cache key was `user:42` instead of `tenant:acme:user:42`. Tenant ID not included in cache key.

**Rule**: Cache key must include every dimension that makes data unique. For multi-tenant systems: `{tenant}:{resource_type}:{id}`. For user-specific data: `user:{user_id}:{resource_type}`.

Bad:
```python
cache_key = f"user:{user_id}"  # shared across tenants!
```

Good:
```python
cache_key = f"tenant:{tenant_id}:user:{user_id}"
```

### Anti-Pattern: Caching at All Costs (No Cache Budget)

Caching every database query without considering hit rate, compute cost, or invalidation complexity. A cache with a 10% hit rate adds latency (Redis round-trip on miss) while providing little benefit.

Measure before caching:
- Hit rate: (cache_hits / total_requests). Target > 80% for the cache to be beneficial.
- Miss penalty: how much does a cache miss cost vs. Redis round-trip?
- Invalidation cost: how often does this data change? High churn + short TTL = low effective hit rate.

### Anti-Pattern: Setting TTL Equal to Business SLA

Business says "data must be fresh within 5 minutes." Developer sets TTL = 300 seconds. When data changes at second 1 and the user reads at second 299, they get 299-second-old data — within SLA but at the very edge. If the business means "no more than 5 minutes stale," TTL = 300 is correct. But if there are other factors (cache stampede adds time), effective staleness can exceed TTL.

TTL should be: `max_acceptable_staleness - max_refresh_time`. If refresh takes 5s and SLA is 5 minutes, TTL = 295s.

### Anti-Pattern: Write-Behind for Financial Data

An e-commerce site uses write-behind for order totals. During the 30-second flush window, Redis crashes. 30 seconds of order total updates are lost. Financial reconciliation fails.

Rule: Write-behind is never appropriate for data where loss is unacceptable: orders, payments, inventory adjustments, user account balances. Use write-through or skip caching entirely.

### Anti-Pattern: In-Process Cache in Horizontally-Scaled Service

Service has 20 instances. Each instance has its own in-process LRU cache. User data is updated. One instance invalidates its local cache. The other 19 instances continue serving stale data from their local caches for up to TTL.

Rule: In-process caches are only safe for immutable or rarely-changing reference data (country codes, feature flags refreshed on deploy). Mutable per-user data requires a shared cache (Redis).

## References

- Fowler, Martin. _Patterns of Enterprise Application Architecture_. Addison-Wesley, 2002.
- Vattani, Andrea, et al. "Optimal Probabilistic Cache Stampede Prevention." VLDB 2015.
- Nishtala, Rajesh, et al. "Scaling Memcache at Facebook." NSDI 2013.
- Redis documentation: redis.io/docs.
- Caffeine (Java): github.com/ben-manes/caffeine.
- RFC 7234: HTTP/1.1 Caching.
