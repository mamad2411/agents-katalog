---
name: playbook-biotech-pharma-sample-lineage
description: "Any result traces to origin sample through every derivation event."
---
# Playbook: Achieve full sample traceability

> Any result traces to origin sample through every derivation event.

**Track:** 🗺️ Biotech & Pharma · **Domain:** Journey Playbooks · **Level:** journey · **~60 min**

**Who this is for:** Bioinformaticians, Lab Scientists, Regulatory Affairs, Genetic Engineers, Clinical Data Managers

## When to Use This Skill

Any result traces to origin sample through every derivation event.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Track sample lineage end to end: start with "Assign unique IDs at receipt; barcode physically and digitally"
2. Step 2 — Version protocols like software: start with "Store protocols in controlled repo with semver-style versions"
3. How it fits together: IDs and event logging at entry beat reconciliation archaeology later.

### Referenced Skills

- `lab-informatics-eln-sample-lineage`
- `lab-informatics-protocol-versioning`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill lab-informatics-eln-sample-lineage && npx skills add aniruddhaadak80/skills --skill lab-informatics-protocol-versioning
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills