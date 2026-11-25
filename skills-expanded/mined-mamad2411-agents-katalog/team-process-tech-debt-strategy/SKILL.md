---
name: team-process-tech-debt-strategy
description: "Classify debt by interest rate, allocate fixed capacity, and tie paydown to business risk."
---
# Manage tech debt as a portfolio

> Classify debt by interest rate, allocate fixed capacity, and tie paydown to business risk.

**Track:** 🧭 Engineering Leadership · **Domain:** Team Process · **Level:** advanced · **~35 min**

**Who this is for:** Engineering Managers, Tech Leads, Staff Engineers, CTOs

## When to Use This Skill

Classify debt by interest rate, allocate fixed capacity, and tie paydown to business risk.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Inventory debts with interest rate: how much slower/costlier per month?
2. Tag principal risk: what breaks if this component fails?
3. Allocate 15-20% sprint capacity permanently, protected
4. Bundle paydown with adjacent feature work where paths cross
5. Kill dead code aggressively; deletion is the cheapest fix
6. Report debt burn-down alongside features to leadership

## Common Pitfalls

- Debt weeks that become bug-fix weeks
- Rewrite fantasies instead of incremental strangling

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill team-process-tech-debt-strategy
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill team-process-tech-debt-strategy -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills