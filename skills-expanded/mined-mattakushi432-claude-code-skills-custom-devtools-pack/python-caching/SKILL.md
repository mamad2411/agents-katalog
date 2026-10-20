---
name: python-caching
description: "When to activate: Redis, caching strategies, cache-aside, TTL, cache invalidation, aiocache, cache decorators"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Python Caching Patterns

## Redis with aioredis / redis-py
```python
from redis.asyncio import Redis, ConnectionPool
import json
from typing import TypeVar, Callable, Awaitable
from functools import wraps

T = TypeVar("T")

pool = ConnectionPool.from_url("redis://redis:6379", max_connections=20)

async def get_redis() -> Redis:
    return Redis(connection_pool=pool)

# Basic operations
async def cache_set(redis: Redis, key: str, value: dict, ttl: int = 300) -> None:
    await redis.setex(key, ttl, json.dumps(value))

async def cache_get(redis: Redis, key: str) -> dict | None:
    raw = await redis.get(key)
    return json.loads(raw) if raw else None
```

## Cache-Aside Pattern (Read-Through)
```python
async def get_user_cached(user_id: int, redis: Redis, db: AsyncSession) -> User | None:
    cache_key = f"user:{user_id}"
    
    # Try cache first
    cached = await cache_get(redis, cache_key)
    if cached:
        return User(**cached)
    
    # Cache miss: fetch from DB
    user = await db.get(User, user_id)
    if user:
        await cache_set(redis, cache_key, user.__dict__, ttl=600)
    
    return user

# Invalidate on update
async def update_user(user_id: int, data: dict, redis: Redis, db: AsyncSession) -> User:
    user = await db.get(User, user_id)
    for k, v in data.items():
        setattr(user, k, v)
    await db.commit()
    await redis.delete(f"user:{user_id}")  # invalidate
    return user
```

## Decorator Pattern
```python
import hashlib
import functools

def cached(ttl: int = 300, key_prefix: str = ""):
    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @functools.wraps(func)
        async def wrapper(*args, redis: Redis, **kwargs) -> T:
            # Build cache key from function name + args
            raw_key = f"{key_prefix or func.__name__}:{args}:{kwargs}"
            cache_key = hashlib.sha256(raw_key.encode()).hexdigest()[:16]
            
            cached_val = await redis.get(cache_key)
            if cached_val:
                return json.loads(cached_val)
            
            result = await func(*args, **kwargs)
            await redis.setex(cache_key, ttl, json.dumps(result, default=str))
            return result
        return wrapper
    return decorator

@cached(ttl=60, key_prefix="products")
async def get_products(category: str, *, redis: Redis) -> list[dict]:
    return await db.query_products(category)
```

## Cache Stampede Prevention (Lock)
```python
async def get_with_lock(redis: Redis, cache_key: str, compute: Callable) -> dict:
    lock_key = f"lock:{cache_key}"
    
    value = await redis.get(cache_key)
    if value:
        return json.loads(value)
    
    # Use Redis lock to prevent multiple concurrent DB fetches
    async with redis.lock(lock_key, timeout=10, blocking_timeout=5):
        # Check again after acquiring lock
        value = await redis.get(cache_key)
        if value:
            return json.loads(value)
        
        result = await compute()
        await redis.setex(cache_key, 300, json.dumps(result))
        return result
```

## Common Cache Key Patterns
```python
USER_KEY = "user:{user_id}"                          # single entity
USER_LIST_KEY = "users:page:{page}:limit:{limit}"   # paginated list
USER_PERMS_KEY = "user:{user_id}:permissions"       # derived data
SESSION_KEY = "session:{session_token}"             # sessions (use TTL = session expiry)
RATE_LIMIT_KEY = "ratelimit:{ip}:{minute}"         # rolling window rate limit
```
