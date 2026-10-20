---
name: backend-caching
description: Design backend caching layers. Use when speeding up reads or
  reducing load on sources.
metadata:
  tags: backend, caching
---

# Backend Caching

## Use this skill when
- Caching queries and API responses
- Choosing cache tiers (in-memory, Redis, CDN)
- Invalidation strategies

## Do not use this skill when
- The data changes every request (caching is a liability)
- Frontend/browser caching

## Instructions
1. Cache only data that is read-heavy and tolerates staleness.
2. Key caches by full query context; include version in keys where schemas evolve.
3. Choose scoped invalidation: explicit evict on write, or TTL with tolerance.
4. Use cache-aside vs write-through deliberately.
5. Protect from stampede: single-flight/mutex on cache miss.
6. Set TTLs with business-appropriate staleness.
7. Monitor hit-rate and correctness (a wrong cache is worse than no cache).

## Checklist
- Stale data tolerance is explicit
- No cross-tenant key collisions
- Hit rate is measured

## Output Format
- Data | access pattern | tier | TTL | invalidation

## Common Mistakes
- Caching every query without a hit-rate check
- Zero invalidation on writes
- Per-user caches filling memory
