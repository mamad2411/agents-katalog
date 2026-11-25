---
name: caching-strategy
description: Adds caching to expensive operations - Redis, in-memory, HTTP cache headers
argument-hint: [file-or-endpoint]
user-invocable: true
allowed-tools: Read Grep Glob Edit
effort: medium
---

## Caching Strategy

Target: **$1** (or analyze top bottlenecks if not specified)

1. Identify cacheable operations:
```bash
grep -rn "db\.\|prisma\.\|fetch\|axios" ${1:-src/} --include="*.ts" | grep -v "test\|spec" | head -20
```

What's cacheable?
- Query results that change infrequently (user profile, product catalog)
- Expensive computations (aggregations, reports)
- External API responses (weather, exchange rates)

What's NOT cacheable?
- User-specific real-time data
- Transactional operations
- Anything that must be consistent

2. Choose caching layer by use case:
   - **Redis**: shared across instances, TTL, pub/sub invalidation
   - **In-memory (`Map`)**: single instance, fastest, lost on restart
   - **HTTP `Cache-Control`**: browser/CDN caching for GET responses
   - **React Query / SWR**: client-side data caching

3. Implement with proper cache keys:
```ts
const cacheKey = `user:${userId}:profile`
const cached = await redis.get(cacheKey)
if (cached) return JSON.parse(cached)

const result = await db.user.findUnique(...)
await redis.set(cacheKey, JSON.stringify(result), 'EX', 300) // 5min TTL
```

4. Add cache invalidation on mutations.

5. Show estimated performance improvement.
