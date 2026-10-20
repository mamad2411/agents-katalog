---
name: risk-modeling-financial-model-hygiene
description: "Structure assumptions, flows, and outputs so anyone can trace every number."
---
# Keep financial models auditable

> Structure assumptions, flows, and outputs so anyone can trace every number.

**Track:** 💰 Finance & Fintech · **Domain:** Risk & Modeling · **Level:** foundation · **~30 min**

**Who this is for:** Fintech Engineers, Financial Analysts, Risk Teams, Controllers

## When to Use This Skill

Structure assumptions, flows, and outputs so anyone can trace every number.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Separate inputs / calculations / outputs into distinct sections or sheets
2. One assumption cell referenced everywhere; no hardcoded duplicates
3. Color convention: blue inputs, black formulas, green cross-links
4. Sanity-check row: units, period alignment, growth vs inflation consistency
5. Stress test: flex the two biggest drivers ±30% and observe covenants
6. Version with changelog tab; archive prior versions read-only

## Common Pitfalls

- Circularity hacks breaking recalculation
- Someone typing over a formula cell during a busy close

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill risk-modeling-financial-model-hygiene
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill risk-modeling-financial-model-hygiene -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills