---
name: operations-monitoring-performance-alert-triage
description: "Alert prioritization from energy-loss math, not alarm noise, with dispatch thresholds."
---
# Triage solar performance alerts by revenue impact

> Alert prioritization from energy-loss math, not alarm noise, with dispatch thresholds.

**Track:** 🔋 Energy & Renewables · **Domain:** Operations & Monitoring · **Level:** intermediate · **~25 min**

**Who this is for:** Solar Engineers, Energy Analysts, Project Developers, O&M Teams

## When to Use This Skill

Alert prioritization from energy-loss math, not alarm noise, with dispatch thresholds.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Convert each alert to estimated kW-loss × tariff = $/day priority
2. Group inverter/string faults by root-cause signature before dispatch
3. Set dispatch thresholds: immediate / next-truck / next-scheduled visit
4. Validate fixes by post-repair production against weather-adjusted expectation
5. Track repeat-offender sites for systemic causes (soiling? critters? PID?)
6. Review false-alarm rate quarterly; tune monitoring rules accordingly

## Common Pitfalls

- Truck rolls prioritized by loudest customer instead of dollars
- Weather unadjusted comparisons triggering phantom alerts

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill operations-monitoring-performance-alert-triage
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill operations-monitoring-performance-alert-triage -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills