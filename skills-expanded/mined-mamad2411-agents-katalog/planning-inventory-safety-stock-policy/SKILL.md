---
name: planning-inventory-safety-stock-policy
description: "Statistical buffers per SKU-class matching stated service levels and lead-time truth."
---
# Set safety stock from service targets and real variability

> Statistical buffers per SKU-class matching stated service levels and lead-time truth.

**Track:** 🚚 Supply Chain & Logistics · **Domain:** Planning & Inventory · **Level:** intermediate · **~30 min**

**Who this is for:** Supply Planners, Logistics Managers, Procurement, Operations Analysts

## When to Use This Skill

Statistical buffers per SKU-class matching stated service levels and lead-time truth.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Get REAL lead times: quoted vs actual distribution, not PO text
2. Set service levels deliberately by segment (A items higher than C)
3. Compute buffers from demand AND lead-time variability together
4. Review exceptions monthly: expedites and stockouts reveal policy misses
5. Cap total buffer investment; trade service level against working capital explicitly
6. Recalculate quarterly; yesterday's volatility isn't tomorrow's

## Common Pitfalls

- One blanket weeks-of-supply rule across all SKUs
- Buffers hiding chronic supplier reliability problems

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill planning-inventory-safety-stock-policy
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill planning-inventory-safety-stock-policy -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills