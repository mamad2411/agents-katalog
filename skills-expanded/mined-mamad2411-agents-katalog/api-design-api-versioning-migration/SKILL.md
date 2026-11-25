---
name: api-design-api-versioning-migration
description: "Run two versions in parallel, observe usage, and sunset safely with real telemetry."
---
# Migrate API versions without breaking clients

> Run two versions in parallel, observe usage, and sunset safely with real telemetry.

**Track:** ⚙️ Backend Engineering · **Domain:** API Design · **Level:** advanced · **~40 min**

**Who this is for:** Backend Engineers, API Developers, Platform Engineers, Full-Stack Developers

## When to Use This Skill

Run two versions in parallel, observe usage, and sunset safely with real telemetry.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Ship vN+1 alongside vN behind the same gateway; no big-bang cutover
2. Tag responses with version header so bug reports are attributable
3. Instrument per-client version adoption; email laggards with deadlines
4. Keep a contract test suite pinned per version in CI
5. Announce sunset twice: 90 days and 14 days before shutdown
6. Return 410 with migration guide URL after the date, not silent 404s

## Common Pitfalls

- Silent breaking changes hidden inside 'minor' fixes
- Sunsetting before the top-3 consumers migrate

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill api-design-api-versioning-migration
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill api-design-api-versioning-migration -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills