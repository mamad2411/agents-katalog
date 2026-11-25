---
name: playbook-healthcare-clinical-patient-edu
description: "Teach-back embedded in routine discharge and education flows."
---
# Playbook: Upgrade patient education outcomes

> Teach-back embedded in routine discharge and education flows.

**Track:** 🗺️ Healthcare & Clinical · **Domain:** Journey Playbooks · **Level:** journey · **~50 min**

**Who this is for:** Nurses, Physicians, Clinical Managers, Health Informaticists

## When to Use This Skill

Teach-back embedded in routine discharge and education flows.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Teach-back patient education that lands: start with "Chunk teaching to one concept at a time in plain language"
2. Step 2 — Reconcile medications across transitions of care: start with "Take best-possible medication history from patient plus pharmacy records"
3. How it fits together: Pair teach-back with reconciled med lists at discharge — readmission prevention compounds.

### Referenced Skills

- `quality-informatics-patient-teach-back`
- `clinical-workflow-med-rec-reconciliation`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill quality-informatics-patient-teach-back && npx skills add aniruddhaadak80/skills --skill clinical-workflow-med-rec-reconciliation
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills