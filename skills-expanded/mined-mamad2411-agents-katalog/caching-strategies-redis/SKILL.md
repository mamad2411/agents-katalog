---
name: caching-strategies-redis
description: Production caching patterns with Redis — cache-aside, write-through, TTL, invalidation
triggers: [caching, Redis, cache strategy, cache invalidation, cache-aside, write-through, performance]
---

# SKILL: Caching Strategies with Redis

## Cache Patterns

### Pattern 1: Cache-Aside (Lazy Loading)
```python
import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_user(user_id: str):
    # 1. Try cache first
    cached = r.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    
    # 2. Cache miss - fetch from DB
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)
    
    # 3. Store in cache
    r.setex(
        f"user:{user_id}",
        3600,  # TTL: 1 hour
        json.dumps(user)
    )
    
    return user
```

### Pattern 2: Write-Through
```python
def update_user(user_id: str, data: dict):
    # 1. Update database
    db.execute("UPDATE users SET name = ? WHERE id = ?", data["name"], user_id)
    
    # 2. Update cache immediately
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)
    r.setex(f"user:{user_id}", 3600, json.dumps(user))
```

### Pattern 3: Write-Behind (Write-Back)
```python
from queue import Queue

write_queue = Queue()

def update_user_async(user_id: str, data: dict):
    # 1. Update cache immediately
    r.hset(f"user:{user_id}", mapping=data)
    
    # 2. Queue DB write
    write_queue.put(("user", user_id, data))

# Background worker
def process_writes():
    while True:
        table, id, data = write_queue.get()
        db.execute(f"UPDATE {table} SET ... WHERE id = ?", id)
```

### Pattern 4: Cache Invalidation
```python
def invalidate_user_cache(user_id: str):
    """Delete from cache on update"""
    r.delete(f"user:{user_id}")

def invalidate_pattern(pattern: str):
    """Delete all keys matching pattern"""
    for key in r.scan_iter(match=pattern):
        r.delete(key)

# Usage
invalidate_pattern("user:*")  # Clear all user caches
```

### Pattern 5: TTL Strategy
```python
# Different TTL for different data types
CACHE_TTL = {
    "user_profile": 3600,      # 1 hour (changes infrequently)
    "product_price": 300,      # 5 min (changes frequently)
    "session": 1800,           # 30 min
    "analytics": 86400,        # 24 hours
}

def cache_with_ttl(key: str, data: dict, data_type: str):
    ttl = CACHE_TTL.get(data_type, 3600)
    r.setex(key, ttl, json.dumps(data))
```

### Pattern 6: Cache Warming
```python
def warm_cache():
    """Pre-populate cache with hot data"""
    # Get most accessed users
    popular_users = db.query("SELECT * FROM users ORDER BY views DESC LIMIT 100")
    
    for user in popular_users:
        r.setex(f"user:{user['id']}", 3600, json.dumps(user))
```

### Pattern 7: Distributed Cache with Redis Cluster
```python
from redis.cluster import RedisCluster

# Connect to cluster
cluster = RedisCluster(
    host='redis-cluster.example.com',
    port=6379
)

# Automatic sharding across nodes
cluster.set("key1", "value1")
cluster.get("key1")
```

### Pattern 8: Cache Stampede Prevention
```python
import time
from threading import Lock

locks = {}

def get_with_lock(key: str, fetch_fn):
    """Prevent cache stampede with locks"""
    
    # Try cache
    cached = r.get(key)
    if cached:
        return json.loads(cached)
    
    # Acquire lock
    lock_key = f"lock:{key}"
    if locks.get(lock_key) is None:
        locks[lock_key] = Lock()
    
    with locks[lock_key]:
        # Check cache again (another thread may have filled it)
        cached = r.get(key)
        if cached:
            return json.loads(cached)
        
        # Fetch and cache
        data = fetch_fn()
        r.setex(key, 3600, json.dumps(data))
        return data
```

### Pattern 9: Pub/Sub for Cache Invalidation
```python
# Publisher (when data changes)
def update_user(user_id: str, data: dict):
    db.execute("UPDATE users SET ... WHERE id = ?", user_id)
    
    # Notify all cache instances to invalidate
    r.publish("cache_invalidate", f"user:{user_id}")

# Subscriber (on each server)
def listen_for_invalidations():
    pubsub = r.pubsub()
    pubsub.subscribe("cache_invalidate")
    
    for message in pubsub.listen():
        if message["type"] == "message":
            key = message["data"]
            r.delete(key)
```

## Quality Checks
- [ ] Cache strategy documented (cache-aside, write-through, etc.)
- [ ] TTL configured for all cached data
- [ ] Cache invalidation on updates
- [ ] Cache stampede prevention
- [ ] Monitoring (hit rate, miss rate)
- [ ] Redis persistence configured
- [ ] Connection pooling enabled
- [ ] Cache warming for hot data
