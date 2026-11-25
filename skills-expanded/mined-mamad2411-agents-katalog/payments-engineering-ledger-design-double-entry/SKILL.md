---
name: payments-engineering-ledger-design-double-entry
description: "Immutable journal entries, balanced postings, and derived balances keeping money math provable."
---
# Design a double-entry ledger that balances forever

> Immutable journal entries, balanced postings, and derived balances keeping money math provable.

**Track:** 💰 Finance & Fintech · **Domain:** Payments Engineering · **Level:** advanced · **~45 min**

**Who this is for:** Fintech Engineers, Financial Analysts, Risk Teams, Controllers

## When to Use This Skill

Immutable journal entries, balanced postings, and derived balances keeping money math provable.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Model money as immutable journal entries; never UPDATE amounts
2. Enforce sum(debits) = sum(credits) per transaction at DB level
3. Store original currency + rate snapshot per entry, not converted-only
4. Derive balances from entries; materialize views for speed, recompute nightly
5. Reconcile internal ledger to processor reports daily with diff alerts
6. Freeze periods: no edits into closed accounting periods, adjustments are new entries

## Common Pitfalls

- Mutable balance columns drifting from entry truth
- FX conversion applied twice across services

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill payments-engineering-ledger-design-double-entry
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill payments-engineering-ledger-design-double-entry -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills