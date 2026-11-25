---
name: lab-informatics-eln-sample-lineage
description: "Aliquots, derivations, and storage positions recorded so any result traces to its origin."
---
# Track sample lineage end to end

> Aliquots, derivations, and storage positions recorded so any result traces to its origin.

**Track:** 🧬 Biotech & Pharma · **Domain:** Lab Informatics · **Level:** intermediate · **~35 min**

**Who this is for:** Bioinformaticians, Lab Scientists, Regulatory Affairs, Genetic Engineers, Clinical Data Managers

## When to Use This Skill

Aliquots, derivations, and storage positions recorded so any result traces to its origin.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Assign unique IDs at receipt; barcode physically and digitally
2. Record every derivation event: parent ID, process, date, operator
3. Track storage position changes like transactions, not overwrites
4. Enforce required fields at entry; free-text only for observations
5. Reconcile physical inventory vs system quarterly
6. Enable one-click lineage tree per final sample

## Common Pitfalls

- Spreadsheet-as-LIMS with silent column drift
- Pooled samples losing constituent IDs

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill lab-informatics-eln-sample-lineage
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill lab-informatics-eln-sample-lineage -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills