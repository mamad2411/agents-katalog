---
name: server-caching-handbook
description: Next.js revalidateTag stampedes unstable_cache external Redis and fetch cache hierarchy for production traffic
tags:
  - caching
  - nextjs
  - redis
version: 1.1.0
category: development
outcomes:
  - Tag naming plan and invalidation map after mutations
  - Stampede mitigation choice singleflight SWR or jitter per use case
  - When external Redis complements vs replaces Next data cache
stack:
  - next
  - redis
  - typescript
last_reviewed: 2026-05-20
risk_level: medium
tools_allowed: read-only
requires_user_approval: false
compatibility:
  - generic-markdown
  - skills-sh
  - cursor
  - claude-code
  - antigravity
  - codex
  - github-copilot
  - windsurf
  - gemini-cli
  - cline
  - amp
  - opencode
  - roo
  - goose
  - kilo
  - kiro-cli
  - droid
  - openclaw
  - trae
references:
  - references/server-caching-patterns.md
  - references/stack-nextjs.md
  - references/skill-safety.md
---

# Instructions

## When to Use

- Use for revalidateTag, stampedes, Redis, fetch cache hierarchy.
- Prefer `next-server-patterns` for where caching sits in the tree.
- Prefer `client-data-fetching` for TanStack Query caches.

Design **server-side caching** for **Next.js** under load. Pair with **`next-server-patterns`**. Read [server-caching-patterns.md](../../references/server-caching-patterns.md).

### Hierarchy

| Layer | Use for | Invalidate with |
|-------|---------|-----------------|
| Full route static | Public marketing pages | rebuild / `revalidatePath` |
| `fetch` / data cache tags | Shared public data | `revalidateTag` |
| `unstable_cache` / `cache` | Expensive server compute | key + tags |
| External Redis | Cross-instance / cross-runtime | TTL + explicit delete |
| TanStack Query | Client interactive data | `client-data-fetching` |

1. Classify data: **public static**, **public dynamic**, **per-user** - different keys and invalidation.
2. **Tags:** granular `revalidateTag` keys; document which Server Actions invalidate which tags.
3. **Stampedes:** on expiry, many misses hit origin - **singleflight**, **stale-while-revalidate**, or **TTL jitter**.
4. **`unstable_cache` / `cache`:** wrap DB or HTTP fan-out; keys must include tenant and all inputs that affect output; verify API name against installed Next.
5. **External Redis:** cross-region or cross-runtime shared cache; serialization, TTL, namespacing; degrade vs fail-closed on Redis down.
6. **Personalization:** never cache HTML that embeds private user data under a shared URL.
7. **Metrics:** log cache hit/miss rates without PII (`observability-handbook`).

## Outcomes

- Tag table + invalidation flow + stampede strategy paragraph per hot route.

## Output Rules

State Next version from lockfile; behavior differs by minor - say “verify against installed Next”.

## Scope and boundaries

- **In scope:** Next cache APIs, tags, external cache integration design.
- **Out of scope:** CDN full-page rules at an edge provider unless the user names the product.

## Safety

- read-only design; no production Redis URLs in output.

## Troubleshooting

- **Stale UI after mutation:** missing `revalidatePath` / tag typo.
- **Redis memory:** TTL mandatory; max entry size cap.
- **Per-user leak:** shared tag used for personalized HTML - split keys.
- **Stampede after deploy:** cold cache - warm critical tags or use SWR.

## Related skills

- [`next-server-patterns`](../next-server-patterns/SKILL.md) - cache placement
- [`client-data-fetching`](../client-data-fetching/SKILL.md) - client vs server cache
- [`observability-handbook`](../observability-handbook/SKILL.md) - cache miss metrics
- [`edge-runtime-handbook`](../edge-runtime-handbook/SKILL.md) - Edge cache limits

**GitHub:** https://github.com/bh611627/skillcodex/tree/main/skills/server-caching-handbook/SKILL.md  
**npm:** https://www.npmjs.com/package/@skillcodex/skills
