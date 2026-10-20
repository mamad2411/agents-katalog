---
name: databases-query-optimization
description: "Find top offenders from real traffic, read plans, add targeted indexes, verify improvements."
---
# Optimize the slow queries actually hurting you

> Find top offenders from real traffic, read plans, add targeted indexes, verify improvements.

**Track:** ⚙️ Backend Engineering · **Domain:** Databases · **Level:** intermediate · **~35 min**

**Who this is for:** Backend Engineers, API Developers, Platform Engineers, Full-Stack Developers

## When to Use This Skill

Find top offenders from real traffic, read plans, add targeted indexes, verify improvements.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Pull top-10 queries by total time from pg_stat_statements or slow log
2. Read EXPLAIN (ANALYZE) for each; find seq scans on growing tables
3. Index to match predicates AND sorts (composite order matters)
4. Cover hot read paths with covering indexes where sensible
5. Re-measure p95 after deploy; drop indexes that nobody uses
6. Guard CI against new seq-scan regressions on core tables

## Common Pitfalls

- Indexing every column 'just in case', tanking write throughput
- Functions wrapping indexed columns, silently disabling them

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill databases-query-optimization
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill databases-query-optimization -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills