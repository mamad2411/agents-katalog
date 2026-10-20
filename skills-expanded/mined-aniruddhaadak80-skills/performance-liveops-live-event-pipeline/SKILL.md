---
name: performance-liveops-live-event-pipeline
description: "Server-driven event configuration, remote flags, and staged rollouts keeping content fresh safely."
---
# Ship live-ops events without client patches

> Server-driven event configuration, remote flags, and staged rollouts keeping content fresh safely.

**Track:** 🎮 Game & Interactive Dev · **Domain:** Performance & Live-Ops · **Level:** advanced · **~45 min**

**Who this is for:** Game Developers, Technical Designers, Live-Ops Engineers, Indie Devs

## When to Use This Skill

Server-driven event configuration, remote flags, and staged rollouts keeping content fresh safely.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Model events as server config consumed by generic client systems
2. Validate configs against schema + simulation harness before publish
3. Stage rollout: internal → 5% players → full, with kill switch per feature
4. Monitor KPIs during events in real-time dashboard with alert thresholds
5. Rehearse emergency shutdown path quarterly like fire drill
6. Post-mortem each event: participation, revenue, bug classes, config errors

## Common Pitfalls

- 'Small' hotfix patches required per event, defeating live-ops
- Timezones ignored, events ending at wrong local hour

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill performance-liveops-live-event-pipeline
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill performance-liveops-live-event-pipeline -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills