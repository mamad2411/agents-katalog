---
name: payments-engineering-reconciliation-flow
description: "Three-way match between internal ledger, processor settlement, and bank statements."
---
# Build daily reconciliation that catches drift

> Three-way match between internal ledger, processor settlement, and bank statements.

**Track:** 💰 Finance & Fintech · **Domain:** Payments Engineering · **Level:** intermediate · **~35 min**

**Who this is for:** Fintech Engineers, Financial Analysts, Risk Teams, Controllers

## When to Use This Skill

Three-way match between internal ledger, processor settlement, and bank statements.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Normalize all three sources to one canonical schema with IDs preserved
2. Match on reference IDs first, then fuzzy-match residuals by amount+date window
3. Categorize breaks: timing, fees missing, duplicates, true mismatches
4. Auto-resolve known-benign classes (settlement T+1) with aging limits
5. Route aged breaks to humans with full context attached
6. Publish break-rate trend weekly; sudden spikes mean upstream change

## Common Pitfalls

- Manual spreadsheet reconciliation hiding systemic issues
- Fee lines unmatched forever, polluting true mismatch counts

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill payments-engineering-reconciliation-flow
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill payments-engineering-reconciliation-flow -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills