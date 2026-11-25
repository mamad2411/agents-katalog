---
name: performance-liveops-frame-budget-profiling
description: "Per-system millisecond budgets enforced from prototype through ship on target hardware."
---
# Hold frame budgets under real content load

> Per-system millisecond budgets enforced from prototype through ship on target hardware.

**Track:** 🎮 Game & Interactive Dev · **Domain:** Performance & Live-Ops · **Level:** advanced · **~40 min**

**Who this is for:** Game Developers, Technical Designers, Live-Ops Engineers, Indie Devs

## When to Use This Skill

Per-system millisecond budgets enforced from prototype through ship on target hardware.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Set frame budget per platform (e.g., 16.6ms console / 33ms mobile) day one
2. Allocate sub-budgets: rendering, gameplay logic, physics, UI, audio
3. Profile weekly on MINIMUM-spec hardware, not dev machines
4. Fix the top offender only; re-measure; repeat — no speculative optimization
5. Track draw calls, GC spikes, and load times in CI perf snapshots
6. Gate releases on budget regressions beyond agreed tolerance

## Common Pitfalls

- Smooth on flagship phones, slideshow on median hardware
- GC death spirals from per-frame allocations

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill performance-liveops-frame-budget-profiling
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill performance-liveops-frame-budget-profiling -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills