---
name: caching-queues-cache-strategy-layers
description: "Decide what caches where (CDN, app, Redis) and how entries die so staleness stays bounded."
---
# Layer caching with explicit invalidation

> Decide what caches where (CDN, app, Redis) and how entries die so staleness stays bounded.

**Track:** ⚙️ Backend Engineering · **Domain:** Caching & Queues · **Level:** intermediate · **~35 min**

**Who this is for:** Backend Engineers, API Developers, Platform Engineers, Full-Stack Developers

## When to Use This Skill

Decide what caches where (CDN, app, Redis) and how entries die so staleness stays bounded.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Classify data: immutable (cache forever), mutable-TTL, never-cache (money)
2. Cache at CDN for anonymous GETs with stale-while-revalidate
3. Memoize expensive computed objects in-process with short TTL
4. Use Redis for shared cross-instance state; set TTLs on everything
5. Invalidate by key pattern on write events, not manual flushes
6. Monitor hit-rate per layer; below 60% means wrong layer or wrong keys

## Common Pitfalls

- Caching authenticated responses at shared CDN edge
- Thundering herd on expiry without jitter or locks

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill caching-queues-cache-strategy-layers
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill caching-queues-cache-strategy-layers -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills