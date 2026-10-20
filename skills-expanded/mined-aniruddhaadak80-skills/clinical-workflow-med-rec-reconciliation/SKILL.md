---
name: clinical-workflow-med-rec-reconciliation
description: "Build one verified medication list at every admission, transfer, and discharge."
---
# Reconcile medications across transitions of care

> Build one verified medication list at every admission, transfer, and discharge.

**Track:** 🏥 Healthcare & Clinical · **Domain:** Clinical Workflow · **Level:** intermediate · **~30 min**

**Who this is for:** Nurses, Physicians, Clinical Managers, Health Informaticists

## When to Use This Skill

Build one verified medication list at every admission, transfer, and discharge.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Take best-possible medication history from patient plus pharmacy records
2. Clarify discrepancies with prescriber before transcribing orders
3. Flag high-risk meds (anticoagulants, insulin, opioids) for double-check
4. Document intentional changes vs errors distinctly in the record
5. Counsel at discharge with teach-back on changed medications
6. Send reconciled list to the next provider AND community pharmacy

## Common Pitfalls

- Copy-forward lists propagating stopped medications
- Herbals/OTC never asked about, interacting with new scripts

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill clinical-workflow-med-rec-reconciliation
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill clinical-workflow-med-rec-reconciliation -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills