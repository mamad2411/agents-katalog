---
name: redis-patterns
description: Redis caching strategies, cache invalidation, write-through/write-behind, TTL management, and cache stampede protection. Grok-native with hooks and compound.
when-to-use: When adding caching, rate limiting, sessions, queues, or pub/sub to backend services. Pair with backend-dev, caching-expert, or redis-expert.
---

# Redis Patterns (Grok Port)

Production caching, queue, and real-time patterns for Redis. Emphasis on invalidation discipline, stampede protection, and integration with Grok flywheel (friction for bad cache decisions, compound for reusable strategies, palace for "why we chose this TTL").

## Core Strategies
- **Cache-Aside (Lazy)**: Read from cache; on miss load from DB and set. Simplest, most common.
- **Write-Through**: Write to cache + DB in same transaction (or async). Strong consistency, higher write cost.
- **Write-Behind (Write-Back)**: Write to cache immediately, flush to DB async. High write perf, risk of loss on crash.
- **Refresh-Ahead**: Proactive refresh before TTL expiry for hot keys.

## Invalidation & TTL
- Always set TTL (never eternal keys in prod unless deliberate).
- Invalidation on write: delete or update cache key after successful DB write.
- Versioned keys for complex objects: `user:123:v2` or append hash of dependent data.
- Cascade invalidation: when parent changes, invalidate dependent list/detail keys (use tags or key patterns + SCAN with care).

## Stampede Protection (thundering herd)
```python
# Python (redis-py) example with lock
import redis
r = redis.Redis()

def get_user(user_id):
    key = f"user:{user_id}"
    val = r.get(key)
    if val: return json.loads(val)
    lock_key = f"lock:{key}"
    if r.set(lock_key, "1", nx=True, ex=5):  # 5s lock
        try:
            user = db.load_user(user_id)
            r.set(key, json.dumps(user), ex=300)
            return user
        finally:
            r.delete(lock_key)
    else:
        # wait or fallback to DB
        time.sleep(0.05)
        return get_user(user_id)  # retry
```

## Rate Limiting (token bucket / sliding window)
Use `INCR` + `EXPIRE` or Redis Sorted Sets for precise windows. Never roll your own without tests.

## Pub/Sub & Streams (for real-time)
- Pub/Sub for fire-and-forget fanout (presence, notifications).
- Streams (XADD / XREAD / XGROUP) for durable, replayable, consumer-group processing (like Kafka lite).
- Use consumer groups + pending list for at-least-once with ack.

## Grok Integration (Production Contract)
- Primary: backend-dev + redis-expert (or caching specialist).
- Fire on_db_change, on_api_feature, on_infra_change when cache keys, invalidation logic, or Redis config changes.
- Pre-Flight (mandatory for any caching): "What is the invalidation strategy? TTL chosen based on what freshness requirement? Stampede protection in place for hot keys? How do we monitor hit rate / evictions? What happens on Redis outage (degraded or fail-closed)?"
- Ledger: record cache key design, TTL rationale, invalidation rules, and any stampede incidents with task_id.
- Handoff: key naming convention, invalidation paths (code locations), TTL table, load test results (hit rate, p99), fallback behavior on cache miss or Redis down.
- Friction + compound: every "cache stampede killed DB on deploy" or "stale data because no invalidation on related table write" → compound to preflight checklist or shared cache helper.
- Palace: "Chose write-through + 5min TTL for user profile because profile changes rarely and we need strong consistency for billing; rejected cache-aside because race on update caused over-charge".
- Claim-verification: Two-pass. Grep "cache.set" or "r.set" → read_file actual code + run with cache disabled in test → "Invalidation on user update exists at services/userService.ts:87 and test 'profile update invalidates cache' passes ✓VERIFIED". Never claim "cache is safe" without reading the real invalidation + observing behavior.
- Pair with: backend-patterns, api-patterns, caching-patterns (higher level), test-enforcement (test with cache on/off), sast-patterns (no secrets in keys), observability (cache metrics in Grafana).

## When to Activate
- Adding any Redis usage (cache, rate limit, session, queue, pub/sub, streams).
- Swarm Phase 2 backend/caching tracks + Phase 3 review.
- Before deploys that introduce or change caching behavior.
- PRs touching cache logic or Redis config.
- Performance or correctness reviews.

See .grok/skills/caching-patterns/SKILL.md, backend-patterns, aws-patterns (ElastiCache), preflight, compound-learnings, memory-palace (store cache decision rationale). Always test cache-off path. Production Contract: ledger + handoff + preflight + friction on caching changes.

Cache is a performance optimization, not a correctness layer. Invalidation bugs are silent data corruption. Make invalidation explicit, versioned, and tested.
