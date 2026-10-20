---
name: caching-queues-background-jobs
description: "Queue async work with retries, dead-letters, and observability so failures surface instead of vanishing."
---
# Build trustworthy background job processing

> Queue async work with retries, dead-letters, and observability so failures surface instead of vanishing.

**Track:** ⚙️ Backend Engineering · **Domain:** Caching & Queues · **Level:** intermediate · **~35 min**

**Who this is for:** Backend Engineers, API Developers, Platform Engineers, Full-Stack Developers

## When to Use This Skill

Queue async work with retries, dead-letters, and observability so failures surface instead of vanishing.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Make handlers idempotent; assume at-least-once delivery
2. Set exponential backoff with jitter; cap retries at sane counts
3. Dead-letter poison messages with full context for triage
4. Separate queues by latency class and priority; prevent head-of-line blocking
5. Emit metrics: depth, age of oldest job, success rate, duration percentiles
6. Alert on oldest-job-age, not just queue depth

## Common Pitfalls

- Long jobs blocking a shared queue of quick tasks
- Silent retries masking a permanently failing handler

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill caching-queues-background-jobs
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill caching-queues-background-jobs -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills