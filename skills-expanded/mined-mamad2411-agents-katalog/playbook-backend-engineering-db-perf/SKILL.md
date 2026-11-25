---
name: playbook-backend-engineering-db-perf
description: "Cut p95 query times on a growing table set before the next traffic spike."
---
# Playbook: Fix database performance under load

> Cut p95 query times on a growing table set before the next traffic spike.

**Track:** 🗺️ Backend Engineering · **Domain:** Journey Playbooks · **Level:** journey · **~70 min**

**Who this is for:** Backend Engineers, API Developers, Platform Engineers, Full-Stack Developers

## When to Use This Skill

Cut p95 query times on a growing table set before the next traffic spike.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Optimize the slow queries actually hurting you: start with "Pull top-10 queries by total time from pg_stat_statements or slow log"
2. Step 2 — Layer caching with explicit invalidation: start with "Classify data: immutable (cache forever), mutable-TTL, never-cache (money)"
3. How it fits together: Measure → index → cache, in that order. Caching a bad query hides it until invalidation day.

### Referenced Skills

- `databases-query-optimization`
- `caching-queues-cache-strategy-layers`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill databases-query-optimization && npx skills add aniruddhaadak80/skills --skill caching-queues-cache-strategy-layers
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills