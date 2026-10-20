---
name: streaming-modeling-dimensional-modeling-refresh
description: "Facts, dimensions, SCD strategy, and grain declarations serving analytics for years."
---
# Apply dimensional modeling pragmatically

> Facts, dimensions, SCD strategy, and grain declarations serving analytics for years.

**Track:** 🛢️ Data Engineering · **Domain:** Streaming & Modeling · **Level:** intermediate · **~35 min**

**Who this is for:** Data Engineers, Analytics Engineers, Platform Data Teams

## When to Use This Skill

Facts, dimensions, SCD strategy, and grain declarations serving analytics for years.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Declare the grain of every fact table in its documentation header
2. Conform shared dimensions across facts before building marts
3. Pick SCD type deliberately: type-2 for history that matters, nothing else
4. Prefer wide tables for specific products over generic mega-marts
5. Add surrogate keys where natural keys churn
6. Model for the top 10 analyst questions; revisit quarterly

## Common Pitfalls

- Mixed-grain fact tables producing wrong aggregates forever
- Type-1 updates silently erasing history compliance needed

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill streaming-modeling-dimensional-modeling-refresh
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill streaming-modeling-dimensional-modeling-refresh -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills