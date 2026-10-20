---
name: playbook-frontend-engineering-rendering-mastery
description: "Mode selection documented, workers offloading measured hot paths at 60fps."
---
# Playbook: Master rendering strategy per route

> Mode selection documented, workers offloading measured hot paths at 60fps.

**Track:** 🗺️ Frontend Engineering · **Domain:** Journey Playbooks · **Level:** journey · **~85 min**

**Who this is for:** Frontend Engineers, Full-Stack Developers, Design Engineers, UI Developers

## When to Use This Skill

Mode selection documented, workers offloading measured hot paths at 60fps.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Select rendering modes per route deliberately: start with "Classify routes: content volatility × personalization × interactivity"
2. Step 2 — Move heavy work off the main thread properly: start with "Profile first: identify tasks blocking main thread >50ms consistently"
3. How it fits together: Route-level decisions beat app-level defaults every time.

### Referenced Skills

- `rendering-strategy-rendering-mode-selection`
- `rendering-strategy-web-workers-architecture`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill rendering-strategy-rendering-mode-selection && npx skills add aniruddhaadak80/skills --skill rendering-strategy-web-workers-architecture
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills