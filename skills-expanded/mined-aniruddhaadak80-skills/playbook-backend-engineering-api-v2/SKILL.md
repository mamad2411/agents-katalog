---
name: playbook-backend-engineering-api-v2
description: "Introduce breaking API improvements while every existing client keeps working."
---
# Playbook: Ship an API v2 safely

> Introduce breaking API improvements while every existing client keeps working.

**Track:** 🗺️ Backend Engineering · **Domain:** Journey Playbooks · **Level:** journey · **~80 min**

**Who this is for:** Backend Engineers, API Developers, Platform Engineers, Full-Stack Developers

## When to Use This Skill

Introduce breaking API improvements while every existing client keeps working.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Migrate API versions without breaking clients: start with "Ship vN+1 alongside vN behind the same gateway; no big-bang cutover"
2. Step 2 — Run zero-downtime schema migrations: start with "Expand: add nullable columns/tables first; deploy code writing both paths"
3. How it fits together: Expand-contract thinking applies to both schema AND endpoint surface. Parallel-run is the whole game.

### Referenced Skills

- `api-design-api-versioning-migration`
- `databases-zero-downtime-migrations`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill api-design-api-versioning-migration && npx skills add aniruddhaadak80/skills --skill databases-zero-downtime-migrations
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills