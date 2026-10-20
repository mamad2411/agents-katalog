---
name: planning-inventory-demand-baseline-forecast
description: "Cleanse history, segment by variability, and benchmark naive forecasts before fancy models."
---
# Build a demand baseline you can beat

> Cleanse history, segment by variability, and benchmark naive forecasts before fancy models.

**Track:** 🚚 Supply Chain & Logistics · **Domain:** Planning & Inventory · **Level:** intermediate · **~35 min**

**Who this is for:** Supply Planners, Logistics Managers, Procurement, Operations Analysts

## When to Use This Skill

Cleanse history, segment by variability, and benchmark naive forecasts before fancy models.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Cleanse history: mark stockouts, promotions, one-time events explicitly
2. Segment SKUs by ABC volume × XYZ variability — different methods per class
3. Benchmark naive (last period / same-period-last-year) first, always
4. Only adopt complex methods that beat naive on YOUR data out-of-sample
5. Forecast at the grain decisions are made; aggregate for reporting only
6. Track bias separately from accuracy; systematic over/under is fixable

## Common Pitfalls

- Promotional spikes trained into base demand forever
- MAPE worship while every forecast runs systematically high

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill planning-inventory-demand-baseline-forecast
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill planning-inventory-demand-baseline-forecast -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills