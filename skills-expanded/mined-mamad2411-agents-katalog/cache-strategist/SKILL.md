---
name: cache-strategist
description: "Design comprehensive caching strategies across all layers: browser cache, CDN, application cache, database query cache, and Redis. Maximize performance while maintaining data freshness."
category: php-frameworks
tags: ['cache', 'redis', 'memcached', 'cdn', 'strategy']
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# Cache Strategist

## Purpose
Design and implement a multi-layer caching strategy that dramatically improves application performance while ensuring appropriate data freshness.

## Operating Mode
You are a **performance and caching engineer**. You identify what to cache, for how long, and design invalidation strategies that prevent stale data.

## Caching Layers

### 1️⃣ Cache Layer Architecture
```
Client Browser Cache
        ↓
    CDN Cache (Cloudflare, CloudFront)
        ↓
    Application Cache (Redis, Memcached)
        ↓
    Database Query Cache
        ↓
    Database (MySQL, PostgreSQL)
```

### 2️⃣ What to Cache (Decision Matrix)
| Data Type | Cache? | TTL | Reason |
|---|---|---|---|
| Static assets (JS/CSS/images) | ✅ Yes | 1 year + CDN | Never changes (content hash) |
| Public page HTML | ✅ Yes | 5-60 min | High traffic, slow to generate |
| User session | ✅ Yes | 2 hours | Every request needs it |
| Auth tokens | ✅ Yes | Token lifetime | Speed, avoid DB per request |
| Search results | ✅ Yes | 5 min | Expensive queries |
| Product catalog | ✅ Yes | 1 hour | Changes infrequently |
| User-specific data | ⚠️ Selective | 30 min | Risk of stale user data |
| Financial totals | ❌ No | 0 | Must be accurate |
| Real-time stock | ❌ No | 0 | Always fresh |

### 3️⃣ Cache Patterns

**Cache-Aside (Lazy Loading)**
```php
function getUser(int $id): User
{
    $key = "user:{$id}";
    
    if ($cached = Cache::get($key)) {
        return $cached;  // Cache hit
    }
    
    $user = User::find($id);  // Cache miss - hit DB
    Cache::put($key, $user, ttl: 3600);
    return $user;
}
```

**Write-Through**
```php
function updateUser(int $id, array $data): User
{
    $user = User::findOrFail($id)->update($data);
    Cache::put("user:{$id}", $user, 3600);  // Always update cache
    return $user;
}
```

**Read-Through (pattern with Repository)**
```php
class CachedUserRepository
{
    public function find(int $id): ?User
    {
        return Cache::remember("user:{$id}", 3600, fn() => 
            $this->db->find($id)  // Only fetches when cache misses
        );
    }
}
```

**Cache-Aside with Stampede Prevention**
```php
function getExpensiveData(string $key): mixed
{
    // Use atomic lock to prevent stampede
    return Cache::lock("lock:{$key}", seconds: 10)
        ->block(seconds: 5, callback: fn() =>
            Cache::remember($key, 300, fn() => computeExpensiveData())
        );
}
```

### 4️⃣ Cache Invalidation Strategies

**Tag-Based Invalidation**
```php
// Store with tags
Cache::tags(['posts', "user:123"])->put("post:456", $post, 3600);

// Invalidate user's cached posts when user updates
public function updateUser(User $user, array $data): void
{
    $user->update($data);
    Cache::tags(["user:{$user->id}"])->flush();  // Clears all user's cached data
}
```

**Event-Driven Invalidation**
```php
// Listen to model events
class Post extends Model
{
    protected static function booted(): void
    {
        static::saved(fn($post) => Cache::forget("post:{$post->id}"));
        static::deleted(fn($post) => Cache::forget("post:{$post->id}"));
    }
}
```

### 5️⃣ CDN Configuration (Cloudflare)
```
# Page rules for caching:

# Cache static assets for 1 year
*.js, *.css, *.png, *.woff2
Cache-Control: public, max-age=31536000, immutable

# Cache API responses for 60 seconds
/api/v1/products*
Cache-Control: public, s-maxage=60, stale-while-revalidate=300

# Never cache
/api/v1/cart, /api/v1/auth/*
Cache-Control: no-store

# Vary header for content negotiation
Vary: Accept-Encoding, Accept
```

### 6️⃣ Redis Cache Configuration
```php
// config/cache.php
'redis' => [
    'driver'     => 'redis',
    'connection' => 'cache',    // Separate Redis DB for cache
    'lock_connection' => 'default',
],

// Separate Redis connection for cache vs sessions vs queues
'connections' => [
    'default' => ['url' => env('REDIS_URL'), 'database' => 0],  // Default/sessions
    'cache'   => ['url' => env('REDIS_CACHE_URL'), 'database' => 1],  // Cache
    'queue'   => ['url' => env('REDIS_QUEUE_URL'), 'database' => 2],  // Queues
],
```

### 7️⃣ Monitoring Cache Performance
```bash
# Redis cache hit rate monitoring
redis-cli info stats | grep keyspace_hits
redis-cli info stats | grep keyspace_misses

# Target: > 95% hit rate for frequently accessed data
# Formula: hits / (hits + misses) * 100

# Monitor memory usage
redis-cli info memory | grep used_memory_human

# List largest keys (find memory hogs)
redis-cli --bigkeys
```

## Outputs
1. Multi-layer caching strategy document
2. Cache implementation code (per framework)
3. Invalidation strategy for each entity type
4. CDN configuration
5. Cache monitoring dashboard queries
6. Performance baseline and targets
