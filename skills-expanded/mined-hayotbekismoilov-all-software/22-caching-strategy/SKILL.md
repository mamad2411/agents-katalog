---
name: caching-strategy
description: |
  Caching patterns for backend and frontend. Apply when optimizing slow endpoints, reducing
  DB load, or planning cache architecture. Covers Redis cache-aside, write-through,
  cache invalidation, HTTP caching headers, and TanStack Query stale-time configuration.
---

# Caching Strategy

## Cache Levels (Choose the right level)
```
Level 1: HTTP Cache Headers     — CDN, browser (static assets, public pages)
Level 2: Application Cache      — Redis (computed data, expensive queries, sessions)
Level 3: DB Query Cache         — PostgreSQL buffer pool, pg_bouncer
Level 4: Client Cache           — TanStack Query (server state), Zustand (UI state)
```

## Redis Cache Patterns

### Cache-Aside (Most common)
```python
from functools import wraps
import json

def cache(key_template: str, ttl: int = 300):
    """Decorator for cache-aside pattern"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = key_template.format(*args, **kwargs)
            cached = await redis.get(key)
            if cached:
                return json.loads(cached)
            result = await func(*args, **kwargs)
            await redis.setex(key, ttl, json.dumps(result, default=str))
            return result
        return wrapper
    return decorator

@cache("product:{0}:detail", ttl=3600)
async def get_product(product_id: str) -> dict:
    product = await Product.objects.aget(id=product_id)
    return ProductDetailSerializer(product).data
```

### Write-Through (Keeps cache fresh)
```python
async def update_product(product_id: str, data: dict) -> Product:
    # 1. Update DB
    product = await Product.objects.filter(id=product_id).aupdate(**data)
    # 2. Update cache immediately (write-through)
    serialized = ProductDetailSerializer(product).data
    await redis.setex(f"product:{product_id}:detail", 3600, json.dumps(serialized, default=str))
    # 3. Invalidate list caches (they're harder to update precisely)
    await redis.delete_pattern("product_list:*")
    return product
```

### Cache Stampede Prevention
```python
import asyncio

_locks: dict[str, asyncio.Lock] = {}

async def get_or_set_cached(key: str, fetch_fn, ttl: int = 300):
    """Prevent multiple simultaneous cache misses rebuilding the same key"""
    cached = await redis.get(key)
    if cached:
        return json.loads(cached)
    
    if key not in _locks:
        _locks[key] = asyncio.Lock()
    
    async with _locks[key]:
        # Double-check after acquiring lock
        cached = await redis.get(key)
        if cached:
            return json.loads(cached)
        result = await fetch_fn()
        await redis.setex(key, ttl, json.dumps(result, default=str))
        return result
```

## HTTP Cache Headers
```python
# Nginx / Django response headers

# Static assets: immutable (1 year)
Cache-Control: public, max-age=31536000, immutable
# → For: /assets/main.abc123.js, /images/logo.webp

# API list endpoints: short cache with revalidation
Cache-Control: public, max-age=60, stale-while-revalidate=300
# → For: GET /api/v1/products (public catalog)

# User-specific: no public cache
Cache-Control: private, max-age=0, no-store
# → For: GET /api/v1/orders (user orders)

# HTML pages: always revalidate
Cache-Control: no-cache
ETag: "abc123"
# → Browser uses conditional request: If-None-Match: "abc123"
```

## TanStack Query staleTime Strategy
```typescript
const STALE_TIMES = {
  // Changes rarely — user can tolerate stale data
  STATIC: 60 * 60 * 1000,       // 1 hour: categories, config, static lists

  // Changes occasionally
  SLOW: 5 * 60 * 1000,          // 5 min: product catalog, blog posts

  // Changes frequently but not real-time
  MODERATE: 60 * 1000,          // 1 min: inventory levels, prices

  // Must be fresh
  FAST: 10 * 1000,              // 10s: order status, notifications

  // Always fresh
  REALTIME: 0,                   // 0: live data, use with WebSocket instead
};
```
