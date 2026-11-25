---
name: playbook-energy-renewables-fleet-ops
description: "Revenue-weighted alert triage plus storage dispatch that respects warranties."
---
# Playbook: Operate the fleet for revenue

> Revenue-weighted alert triage plus storage dispatch that respects warranties.

**Track:** 🗺️ Energy & Renewables · **Domain:** Journey Playbooks · **Level:** journey · **~60 min**

**Who this is for:** Solar Engineers, Energy Analysts, Project Developers, O&M Teams

## When to Use This Skill

Revenue-weighted alert triage plus storage dispatch that respects warranties.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Triage solar performance alerts by revenue impact: start with "Convert each alert to estimated kW-loss × tariff = $/day priority"
2. Step 2 — Operate storage within warranty and market reality: start with "Model degradation cost per cycle at CURRENT replacement prices"
3. How it fits together: Dollars per day orders the dispatch board; warranty cycles are real money too.

### Referenced Skills

- `operations-monitoring-performance-alert-triage`
- `operations-monitoring-storage-cycling-strategy`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill operations-monitoring-performance-alert-triage && npx skills add aniruddhaadak80/skills --skill operations-monitoring-storage-cycling-strategy
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills