---
name: playbook-finance-fintech-payments-launch
description: "Double-entry ledger, reliable webhooks, and daily reconciliation live before scale."
---
# Playbook: Launch money movement safely

> Double-entry ledger, reliable webhooks, and daily reconciliation live before scale.

**Track:** 🗺️ Finance & Fintech · **Domain:** Journey Playbooks · **Level:** journey · **~115 min**

**Who this is for:** Fintech Engineers, Financial Analysts, Risk Teams, Controllers

## When to Use This Skill

Double-entry ledger, reliable webhooks, and daily reconciliation live before scale.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Design a double-entry ledger that balances forever: start with "Model money as immutable journal entries; never UPDATE amounts"
2. Step 2 — Process payment webhooks reliably: start with "Verify signatures first; reject before any parsing side effects"
3. Step 3 — Build daily reconciliation that catches drift: start with "Normalize all three sources to one canonical schema with IDs preserved"
4. How it fits together: Ledger correctness is non-negotiable day one; everything else can iterate around it.

### Referenced Skills

- `payments-engineering-ledger-design-double-entry`
- `payments-engineering-webhook-reliability-payments`
- `payments-engineering-reconciliation-flow`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill payments-engineering-ledger-design-double-entry && npx skills add aniruddhaadak80/skills --skill payments-engineering-webhook-reliability-payments && npx skills add aniruddhaadak80/skills --skill payments-engineering-reconciliation-flow
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills