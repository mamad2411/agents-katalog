---
description: Run Backend Latency and Caching Strategy Checks
globs:
  ['src/app/api/**/*.ts', 'src/pages/api/**/*.ts', 'src/lib/cache/**/*.ts', 'src/services/**/*.ts']
---

# Performance: Backend Latency & Caching

<audit_rules>

- You MUST implement caching for read-heavy API routes or database queries using Redis or Next.js Data Cache to minimize backend latency.
- You MUST configure explicit Cache-Control headers (`stale-while-revalidate`, `s-maxage`) for public data endpoints.
- You MUST enforce fallback mechanisms if the caching layer (e.g., Redis) is unavailable to prevent application crashes.
- You MUST verify that cache keys are deterministic and appropriately scoped (e.g., incorporating `userId` for private data).
- You MUST monitor external API calls and ensure they have strict timeout configurations (e.g., < 5000ms) to prevent cascading latency failures.
- You MUST invalidate or revalidate caches (`revalidatePath` or `revalidateTag` in Next.js) upon data mutation.
  </audit_rules>

<example_good>

```typescript
import { redis } from '@/lib/redis'
import { db } from '@/lib/db'

export async function getUserProfile(userId: string) {
  const cacheKey = `user:profile:${userId}`

  try {
    const cached = await redis.get(cacheKey)
    if (cached) return JSON.parse(cached)
  } catch (error) {
    console.warn('Redis unavailable, falling back to DB')
  }

  const profile = await db.user.findUnique({ where: { id: userId } })

  try {
    // Cache for 1 hour
    await redis.setex(cacheKey, 3600, JSON.stringify(profile))
  } catch (e) {
    /* ignore cache write errors */
  }

  return profile
}
```

</example_good>

<example_bad>

```typescript
export async function getUserProfile(userId: string) {
  // BAD: Every request hits the database, increasing latency
  return await db.user.findUnique({ where: { id: userId } })
}
```

</example_bad>
