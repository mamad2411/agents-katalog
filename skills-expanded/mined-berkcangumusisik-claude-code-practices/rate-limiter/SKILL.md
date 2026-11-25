---
name: rate-limiter
description: Adds rate limiting to API endpoints with Redis or in-memory storage
argument-hint: [endpoint-pattern]
user-invocable: true
allowed-tools: Read Glob Edit
effort: low
---

## Add Rate Limiting

Endpoint: **$1** (or all routes if not specified)

1. Check existing rate limiting:
```bash
cat package.json | grep -E '"express-rate-limit"|"@fastify/rate-limit"|"rate-limiter-flexible"|"upstash"'
grep -rn "rateLimit\|rateLimiter" src/ --include="*.ts" | head -5
```

2. Check if Redis is available (preferred for distributed deployments):
```bash
cat package.json | grep -E '"ioredis"|"redis"|"@upstash/redis"'
```

3. Implement appropriate rate limiter:

**Tiered limits by endpoint sensitivity:**
```ts
// Auth endpoints - strict
authLimiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 5 })

// API endpoints - moderate
apiLimiter = rateLimit({ windowMs: 60 * 1000, max: 100 })

// Public read endpoints - loose
publicLimiter = rateLimit({ windowMs: 60 * 1000, max: 300 })
```

4. Include:
   - Proper `Retry-After` header in 429 responses
   - Different limits for authenticated vs anonymous users
   - Whitelist for trusted IPs/service accounts
   - Graceful degradation if Redis is down (fall back to in-memory)

5. Apply to the specified endpoint or globally.
