---
name: databases-zero-downtime-migrations
description: "Expand-contract deployments so schema changes ship without locking tables or breaking running code."
---
# Run zero-downtime schema migrations

> Expand-contract deployments so schema changes ship without locking tables or breaking running code.

**Track:** ⚙️ Backend Engineering · **Domain:** Databases · **Level:** advanced · **~40 min**

**Who this is for:** Backend Engineers, API Developers, Platform Engineers, Full-Stack Developers

## When to Use This Skill

Expand-contract deployments so schema changes ship without locking tables or breaking running code.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Expand: add nullable columns/tables first; deploy code writing both paths
2. Backfill in batches with sleep/throttling; monitor replication lag
3. Switch reads to the new shape behind a flag; verify parity metrics
4. Contract: remove old columns only after N days of clean telemetry
5. Never rename or drop during peak; schedule low-traffic windows
6. Test every migration against a production-size snapshot first

## Common Pitfalls

- CREATE INDEX without CONCURRENTLY blocking writes
- Deploying code that assumes new column before migration runs

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill databases-zero-downtime-migrations
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill databases-zero-downtime-migrations -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills