---
name: playbook-healthcare-clinical-safe-transitions
description: "Handoffs, medication reconciliation, and escalation thresholds operating as one system."
---
# Playbook: Make care transitions bulletproof

> Handoffs, medication reconciliation, and escalation thresholds operating as one system.

**Track:** 🗺️ Healthcare & Clinical · **Domain:** Journey Playbooks · **Level:** journey · **~75 min**

**Who this is for:** Nurses, Physicians, Clinical Managers, Health Informaticists

## When to Use This Skill

Handoffs, medication reconciliation, and escalation thresholds operating as one system.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Run structured shift handoffs with ISBAR: start with "Identify: name, age, location, attending team for each patient"
2. Step 2 — Reconcile medications across transitions of care: start with "Take best-possible medication history from patient plus pharmacy records"
3. Step 3 — Escalate deterioration early with objective triggers: start with "Track early-warning score trend, not single readings"
4. How it fits together: Most preventable harm concentrates at transitions — standardize all three together.

### Referenced Skills

- `clinical-workflow-shift-handoff-isbar`
- `clinical-workflow-med-rec-reconciliation`
- `clinical-workflow-deterioration-escalation`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill clinical-workflow-shift-handoff-isbar && npx skills add aniruddhaadak80/skills --skill clinical-workflow-med-rec-reconciliation && npx skills add aniruddhaadak80/skills --skill clinical-workflow-deterioration-escalation
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills