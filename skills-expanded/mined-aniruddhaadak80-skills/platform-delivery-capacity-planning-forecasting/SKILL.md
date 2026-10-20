---
name: platform-delivery-capacity-planning-forecasting
description: "Headroom policies, load-shed tiers defined calmly, and procurement lead times respected."
---
# Plan capacity from growth curves, not incidents

> Headroom policies, load-shed tiers defined calmly, and procurement lead times respected.

**Track:** ☁️ DevOps & Cloud · **Domain:** Platform & Delivery · **Level:** advanced · **~40 min**

**Who this is for:** DevOps Engineers, SREs, Cloud Architects, Platform Engineers

## When to Use This Skill

Headroom policies, load-shed tiers defined calmly, and procurement lead times respected.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Forecast demand from sales pipeline + seasonality, reviewed monthly
2. Set headroom policy per tier (e.g., 40% at peak) with alert thresholds below it
3. Load-test at forecast+headroom levels, not last year's peak
4. Pre-negotiate procurement/reservation lead times into planning calendars
5. Define load-shed ladder in advance: which features drop first, who decides
6. Post-incident capacity reviews update curves and buffers formally

## Common Pitfalls

- Capacity added reactively at 95% utilization
- Shed-ladder improvised during the outage it was meant for

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill platform-delivery-capacity-planning-forecasting
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill platform-delivery-capacity-planning-forecasting -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills