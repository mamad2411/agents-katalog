---
name: redis-caching
description: "Apply when implementing caching, session storage, rate limiting, or pub/sub with Redis. Covers: key design, TTL strategy, cache invalidation, Redis Streams, connection pooling. Trigger for: Redis, cache, session, rate limit, pub/sub, queue."
---

# REDIS CACHING — Production Patterns

## Key Design (namespace:entity:id)
```python
# Always namespace to avoid collisions
f"session:{user_id}"           # user session
f"cache:user:{user_id}"        # cached user data
f"rate:{endpoint}:{ip}"        # rate limit counter
f"lock:job:{job_id}"           # distributed lock
f"worker:{worker_id}:alive"    # heartbeat

# Key limits: < 512 bytes, avoid spaces
```

## TTL Strategy
```python
import redis.asyncio as redis

r = redis.from_url("redis://localhost:6379/0")

# Always set TTL — never store without expiry
await r.setex("cache:user:123", 300, json.dumps(user_data))  # 5 min

# Check before compute (cache-aside pattern)
async def get_user(user_id: str) -> dict:
    cached = await r.get(f"cache:user:{user_id}")
    if cached:
        return json.loads(cached)
    user = await db.fetch_user(user_id)
    await r.setex(f"cache:user:{user_id}", 300, json.dumps(user))
    return user
```

## Distributed Lock (prevent race conditions)
```python
async def with_lock(key: str, ttl: int = 30):
    """Distributed lock using SET NX EX."""
    lock_key = f"lock:{key}"
    acquired = await r.set(lock_key, "1", nx=True, ex=ttl)
    if not acquired:
        raise LockError(f"Could not acquire lock: {key}")
    try:
        yield
    finally:
        await r.delete(lock_key)
```

## Rate Limiting
```python
async def is_rate_limited(identifier: str, limit: int, window: int) -> bool:
    key = f"rate:{identifier}"
    pipe = r.pipeline()
    pipe.incr(key)
    pipe.expire(key, window)
    results = await pipe.execute()
    return results[0] > limit
```

## Connection Pool (production)
```python
pool = redis.ConnectionPool.from_url(
    "redis://localhost:6379/0",
    max_connections=50,
    decode_responses=True,
)
r = redis.Redis(connection_pool=pool)
```

## Forbidden
❌ Keys without TTL (Redis will fill memory)
❌ `KEYS *` in production (blocks Redis, use SCAN)
❌ Storing large objects (> 1MB) — use S3/filesystem
❌ Using Redis as primary database (it's ephemeral)
❌ No connection pooling
❌ Storing sensitive data without encryption
