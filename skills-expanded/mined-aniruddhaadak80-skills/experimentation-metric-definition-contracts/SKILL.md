---
name: experimentation-metric-definition-contracts
description: "One canonical definition per metric, versioned and documented, killing dashboard wars."
---
# Write metric definitions as contracts

> One canonical definition per metric, versioned and documented, killing dashboard wars.

**Track:** 📊 Data Science & Analytics · **Domain:** Experimentation & A/B Testing · **Level:** intermediate · **~30 min**

**Who this is for:** Data Scientists, Analysts, Research Scientists, Product Analysts

## When to Use This Skill

One canonical definition per metric, versioned and documented, killing dashboard wars.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Create a metric catalog entry per KPI: formula, grain, filters, owner
2. Specify inclusion/exclusion rules explicitly (bots, refunds, internal staff)
3. Implement once in the semantic layer; dashboards reference it
4. Version definitions; changelog when business logic changes
5. Backfill check: recompute last 12 months after any change
6. Review catalog quarterly; archive dead metrics loudly

## Common Pitfalls

- 'Active users' meaning three things in three dashboards
- Revenue defined differently between finance and product

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill experimentation-metric-definition-contracts
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill experimentation-metric-definition-contracts -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills