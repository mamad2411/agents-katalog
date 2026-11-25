---
name: caching-strategy
description: Design a multi-layer caching strategy for performance optimization. Outputs cache types, TTLs, invalidation, and cache-aside patterns.
argument-hint: [application type, read/write ratio, data freshness requirements]
allowed-tools: Read, Write, Bash
---

# Caching Strategy

Design a comprehensive caching system that speeds up reads, reduces database load, and keeps data reasonably fresh. Not "add Redis everywhere" — specific cache layers, TTL strategies, invalidation patterns, and cost-benefit analysis.

## Process

1. **Identify cacheable data.** Read-heavy, infrequent writes, tolerable staleness.
2. **Choose cache layers.** Browser, CDN, application (Redis/Memcached), database query cache.
3. **Set TTLs.** Based on data freshness requirements (seconds to days).
4. **Design invalidation.** Time-based, event-based, manual purge.
5. **Handle cache misses.** Cache-aside, read-through, write-through patterns.
6. **Plan warming.** Pre-populate cache on deploy.
7. **Estimate savings.** Cache hit rate, reduced DB queries, latency improvement.
8. **Monitor.** Hit rate, eviction rate, memory usage.

## Output Format

### Caching Strategy: [Application Name]

**Read/Write Ratio:** 90% reads, 10% writes  
**Data Freshness:** Can tolerate 5-60 seconds staleness  
**Cache Layers:** 4 (Browser, CDN, Application, Database)  
**Expected Hit Rate:** 85%  
**Estimated Savings:** 70% reduction in database queries  

---

## Cache Layers

### Layer 1: Browser Cache
**Purpose:** Cache static assets (JS, CSS, images) on user's device  
**Storage:** User's browser  
**TTL:** 30 days for versioned assets, 5 minutes for HTML  
**Size Limit:** ~50 MB per domain  
**Control:** HTTP headers (`Cache-Control`, `ETag`)

### Layer 2: CDN (Content Delivery Network)
**Purpose:** Cache static and dynamic content close to users  
**Storage:** CloudFlare, Fastly, AWS CloudFront  
**TTL:** 1 hour for API responses, 1 day for assets  
**Size Limit:** Unlimited (CDN-dependent)  
**Control:** HTTP headers + CDN purge API

### Layer 3: Application Cache (Redis/Memcached)
**Purpose:** Cache database query results, computed data, session data  
**Storage:** Redis Cluster  
**TTL:** 30 seconds to 1 hour (data-dependent)  
**Size Limit:** 16 GB per instance (scale horizontally)  
**Control:** Application code

### Layer 4: Database Query Cache
**Purpose:** Cache repeated queries at database level  
**Storage:** PostgreSQL query cache, MySQL query cache  
**TTL:** Automatic (invalidated on table write)  
**Size Limit:** 1-4 GB  
**Control:** Database configuration

---

## What to Cache

### High-Value Candidates

#### User Profile (Read-heavy, infrequent writes)
- **Current:** Query database on every request
- **Cached:** Store in Redis for 5 minutes
- **Impact:** 1000 req/s → 5 DB queries/s (99.5% reduction)
- **TTL:** 5 minutes (acceptable staleness)
- **Invalidation:** Purge on profile update

#### Product Catalog (Read-heavy, daily updates)
- **Current:** Query database for product list
- **Cached:** Store in Redis for 1 hour
- **Impact:** 500 req/s → 0.14 DB queries/s
- **TTL:** 1 hour
- **Invalidation:** Purge on product update

#### Homepage (Read-only, hourly updates)
- **Current:** Render HTML on every request
- **Cached:** Store rendered HTML in CDN for 5 minutes
- **Impact:** 10,000 req/s → 33 origin requests/s
- **TTL:** 5 minutes
- **Invalidation:** Auto-expire + manual purge on content publish

#### Session Data (Read-heavy per user)
- **Current:** Query database for session token validation
- **Cached:** Store in Redis with JWT
- **Impact:** Every authenticated request → 0 DB queries
- **TTL:** 24 hours
- **Invalidation:** Logout or token refresh

---

### Low-Value Candidates (Don't Cache)

#### User Orders (Fresh data critical)
- **Why:** Order status must be real-time
- **Alternative:** Cache individual order if unchanged for 1 minute

#### Inventory Count (High write frequency)
- **Why:** Changes on every purchase, cache would be stale
- **Alternative:** Cache at 10-second granularity if acceptable

#### Financial Transactions (Zero staleness tolerance)
- **Why:** Must be accurate to the cent
- **Alternative:** No caching

---

## TTL Strategy

### By Data Type

| Data Type | TTL | Reason |
|-----------|-----|--------|
| User profile | 5 minutes | Updates rare, some staleness OK |
| Product catalog | 1 hour | Daily updates, not time-sensitive |
| Search results | 30 seconds | Recency important |
| Static assets (versioned) | 365 days | Never change (URL includes hash) |
| Static assets (not versioned) | 5 minutes | Might change on deploy |
| API responses (public data) | 1 hour | Low change frequency |
| Session tokens | 24 hours | Expiry matches token lifetime |
| Configuration | 10 minutes | Changes very rare |

### Dynamic TTL Based on Access Frequency
```python
def get_ttl(key_access_frequency):
    """High-frequency keys get longer TTL"""
    if key_access_frequency > 100:  # 100 accesses/hour
        return 3600  # 1 hour
    elif key_access_frequency > 10:
        return 600   # 10 minutes
    else:
        return 60    # 1 minute
```

---

## Cache Patterns

### 1. Cache-Aside (Lazy Loading)

**Flow:**
```
1. App checks cache
2. If hit: Return cached data
3. If miss: Query database → Store in cache → Return data
```

**Implementation (Python + Redis):**
```python
import redis
import json

cache = redis.Redis()

def get_user(user_id):
    cache_key = f"user:{user_id}"
    
    # Check cache
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Cache miss: Query database
    user = db.query(User).filter(User.id == user_id).one()
    
    # Store in cache with 5-minute TTL
    cache.setex(cache_key, 300, json.dumps(user.to_dict()))
    
    return user.to_dict()
```

**Pros:** Only caches requested data (efficient)  
**Cons:** First request is slow (cold start)

---

### 2. Read-Through Cache

**Flow:**
```
1. App requests data from cache
2. Cache checks itself
3. If miss: Cache queries database, stores result, returns data
```

**When:** Cache library handles database fallback

**Pros:** Application code simpler  
**Cons:** Requires cache library with DB integration

---

### 3. Write-Through Cache

**Flow:**
```
1. App writes to cache
2. Cache writes to database synchronously
3. Return success
```

**When:** Data must be in cache immediately after write

**Pros:** Cache always up-to-date  
**Cons:** Write latency increased, database still hit on every write

---

### 4. Write-Behind (Write-Back) Cache

**Flow:**
```
1. App writes to cache
2. Return success immediately
3. Cache asynchronously writes to database (batched)
```

**When:** Write performance critical, eventual consistency OK

**Pros:** Fast writes  
**Cons:** Data loss risk if cache crashes before DB write

---

## Cache Invalidation Strategies

### 1. Time-Based (TTL)
**How:** Set expiration time, cache auto-deletes  
**When:** Acceptable staleness window  
**Example:** Product catalog with 1-hour TTL

```python
cache.setex("product:123", 3600, json.dumps(product))
```

---

### 2. Event-Based (Explicit Invalidation)
**How:** Purge cache on data change event  
**When:** Must be fresh immediately  
**Example:** User updates profile → purge user cache

```python
def update_user(user_id, data):
    db.update(User, user_id, data)
    cache.delete(f"user:{user_id}")  # Invalidate cache
```

---

### 3. Cache Stampede Protection
**Problem:** Cache expires → 1000 concurrent requests hit database → database overload

**Solution: Lock during cache rebuild**
```python
import time

def get_product_with_lock(product_id):
    cache_key = f"product:{product_id}"
    lock_key = f"lock:{cache_key}"
    
    # Check cache
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Try to acquire lock
    lock = cache.set(lock_key, "1", nx=True, ex=10)
    
    if lock:
        # This request rebuilds cache
        product = db.query(Product).filter(Product.id == product_id).one()
        cache.setex(cache_key, 3600, json.dumps(product.to_dict()))
        cache.delete(lock_key)
        return product.to_dict()
    else:
        # Another request is rebuilding, wait and retry
        time.sleep(0.1)
        return get_product_with_lock(product_id)  # Retry
```

---

### 4. Tag-Based Invalidation
**How:** Tag cache entries, purge by tag  
**When:** Need to invalidate related items  
**Example:** Invalidate all caches for user's orders

```python
# Store with tag
cache.set("order:123", order_data, tags=["user:xyz", "orders"])

# Invalidate by tag
cache.invalidate_tag("user:xyz")  # Clears all user's data
```

---

## Cache Warming

### On Application Start
```python
def warm_cache():
    """Pre-populate cache with hot data"""
    # Top 100 products by sales
    top_products = db.query(Product).order_by(Product.sales.desc()).limit(100)
    for product in top_products:
        cache.setex(f"product:{product.id}", 3600, json.dumps(product.to_dict()))
    
    # Active users (logged in last 24h)
    active_users = db.query(User).filter(User.last_login > datetime.now() - timedelta(days=1))
    for user in active_users:
        cache.setex(f"user:{user.id}", 300, json.dumps(user.to_dict()))
```

---

## HTTP Caching Headers

### Cache-Control
```
Cache-Control: public, max-age=3600
```
- `public` — Can be cached by CDN and browser
- `private` — Browser only (not CDN)
- `max-age=3600` — Cache for 1 hour
- `no-cache` — Must revalidate with server
- `no-store` — Never cache (sensitive data)

### ETag (Entity Tag)
```
Response:
  ETag: "abc123"

Next request:
  If-None-Match: "abc123"

Response:
  304 Not Modified (if ETag matches)
```

**Use:** Validate if content changed without re-downloading

### Example (Express.js)
```javascript
app.get('/api/products', (req, res) => {
  const products = getProducts();
  res.set('Cache-Control', 'public, max-age=3600');
  res.set('ETag', generateETag(products));
  
  if (req.headers['if-none-match'] === res.get('ETag')) {
    return res.sendStatus(304);  // Not Modified
  }
  
  res.json(products);
});
```

---

## Monitoring Cache Performance

### Key Metrics

#### Hit Rate
```
hit_rate = (cache_hits / (cache_hits + cache_misses)) * 100
```
**Target:** > 80% for frequently accessed data

#### Eviction Rate
```
eviction_rate = evictions_per_second
```
**Alert if:** > 100/sec (cache too small)

#### Memory Usage
```
memory_used / memory_available
```
**Alert if:** > 80% (add capacity)

#### Latency
```
p50, p95, p99 cache read latency
```
**Target:** < 1ms for Redis

---

### Metrics Dashboard (Prometheus Queries)
```promql
# Hit rate
rate(cache_hits_total[5m]) / (rate(cache_hits_total[5m]) + rate(cache_misses_total[5m]))

# Evictions
rate(cache_evictions_total[5m])

# Memory usage
redis_memory_used_bytes / redis_memory_max_bytes
```

---

## Cache Sizing

### Estimate Memory Requirement

**Example: User profile caching**
- Users: 1 million active
- Profile size: 2 KB
- Cache all active users: 1M × 2 KB = 2 GB
- Add 30% overhead: 2.6 GB
- **Recommendation:** 4 GB Redis instance (with headroom)

**Cost:** AWS ElastiCache t3.medium (3.09 GB RAM) = $0.068/hour = $50/month

**Savings:** Reduced database load from 1000 QPS to 10 QPS → can use smaller RDS instance, saves $200/month

**ROI:** Spend $50, save $200 = net $150/month

---

## Common Pitfalls

### 1. Caching Entire Database
**Problem:** Cache becomes larger than memory  
**Solution:** Cache only hot data (20% of data = 80% of requests)

### 2. Infinite TTL
**Problem:** Stale data never refreshed  
**Solution:** Max TTL = 24 hours, even for "static" data

### 3. Not Handling Cache Failures
**Problem:** Redis down → entire app down  
**Solution:** Graceful degradation (query DB on cache failure)

```python
try:
    cached = cache.get(key)
    if cached:
        return cached
except redis.ConnectionError:
    logger.warning("Cache unavailable, querying DB")

return db.query(...)
```

### 4. Caching User-Specific Data Globally
**Problem:** User A sees User B's data  
**Solution:** Include user ID in cache key: `user:{user_id}:orders`

---

## Testing Cache Strategy

### Unit Tests
```python
def test_cache_hit():
    cache.set("user:123", user_data)
    result = get_user("123")
    assert result == user_data
    assert db_mock.call_count == 0  # DB not queried

def test_cache_miss():
    cache.delete("user:123")
    result = get_user("123")
    assert db_mock.call_count == 1  # DB queried
```

### Load Tests
```
Simulate 10,000 requests with cache enabled
Compare latency vs without cache
Verify 80%+ hit rate
```

## Rules

- Cache key must be unique and predictable: `{resource}:{id}` format (e.g., `user:123`, `product:abc`).
- TTL must be set for every cache entry — infinite TTL = eventual stale data.
- Cache invalidation must happen synchronously with writes — update DB then invalidate cache, not the reverse.
- Always handle cache failures gracefully — app must work if Redis is down (degraded, not broken).
- Hit rate below 70% means caching wrong data or TTL too short.
- Include user_id in cache key for user-specific data to prevent data leakage.
- Never cache sensitive data (passwords, credit cards) even with short TTL.
- Eviction rate > 100/sec means cache is undersized — increase memory or reduce TTL.
- For high-write workloads (> 50% writes), caching may hurt more than help — benchmark first.
- Cache warming is optional for small datasets, mandatory for large datasets to prevent cold-start stampede.
