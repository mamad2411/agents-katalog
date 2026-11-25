---
name: containers-compose-local-env
description: "One command brings up app plus dependencies with seeded data and sane defaults."
---
# Spin up reproducible local environments

> One command brings up app plus dependencies with seeded data and sane defaults.

**Track:** ☁️ DevOps & Cloud · **Domain:** Containers · **Level:** foundation · **~25 min**

**Who this is for:** DevOps Engineers, SREs, Cloud Architects, Platform Engineers

## When to Use This Skill

One command brings up app plus dependencies with seeded data and sane defaults.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Compose file includes app, database, cache, queue with healthchecks
2. Mount code for live reload; keep volumes out of production paths
3. Seed scripts run automatically on first boot, idempotent after
4. .env.example documents every variable; fail fast on missing ones
5. Pin service versions; document the one-command README entry
6. Add make targets: up, down, logs, reset-db

## Common Pitfalls

- Ports colliding with other projects; parameterize via env
- Seed data drifting from production shapes

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill containers-compose-local-env
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill containers-compose-local-env -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills