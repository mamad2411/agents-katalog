---
name: playbook-game-interactive-perf-rescue-game
description: "Budgets allocated, profiling cadence installed, top offenders fixed measurably."
---
# Playbook: Rescue a frame-rate crisis

> Budgets allocated, profiling cadence installed, top offenders fixed measurably.

**Track:** 🗺️ Game & Interactive Dev · **Domain:** Journey Playbooks · **Level:** journey · **~75 min**

**Who this is for:** Game Developers, Technical Designers, Live-Ops Engineers, Indie Devs

## When to Use This Skill

Budgets allocated, profiling cadence installed, top offenders fixed measurably.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Hold frame budgets under real content load: start with "Set frame budget per platform (e.g., 16.6ms console / 33ms mobile) day one"
2. Step 2 — Tune game feel with parameter discipline: start with "Expose movement/combat parameters to a runtime debug panel"
3. How it fits together: Profile on median player hardware. Fix #1 only, then re-measure.

### Referenced Skills

- `performance-liveops-frame-budget-profiling`
- `gameplay-systems-game-feel-tuning`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill performance-liveops-frame-budget-profiling && npx skills add aniruddhaadak80/skills --skill gameplay-systems-game-feel-tuning
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills