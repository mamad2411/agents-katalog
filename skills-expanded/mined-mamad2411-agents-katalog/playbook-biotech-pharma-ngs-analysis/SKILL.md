---
name: playbook-biotech-pharma-ngs-analysis
description: "QC-passed, versioned, inspection-ready sequencing results with provenance."
---
# Playbook: Deliver an NGS analysis package

> QC-passed, versioned, inspection-ready sequencing results with provenance.

**Track:** 🗺️ Biotech & Pharma · **Domain:** Journey Playbooks · **Level:** journey · **~120 min**

**Who this is for:** Bioinformaticians, Lab Scientists, Regulatory Affairs, Genetic Engineers, Clinical Data Managers

## When to Use This Skill

QC-passed, versioned, inspection-ready sequencing results with provenance.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Quality-control sequencing data before analysis: start with "Run read-level QC: per-base quality, GC bias, duplication profiles"
2. Step 2 — Standardize variant calling and annotation: start with "Fix caller versions and filter thresholds in writing before processing"
3. Step 3 — Version protocols like software: start with "Store protocols in controlled repo with semver-style versions"
4. How it fits together: Reference builds and tool versions recorded everywhere. Future-you and auditors both say thanks.

### Referenced Skills

- `bioinformatics-seq-qc-pipeline`
- `bioinformatics-variant-calling-sop`
- `lab-informatics-protocol-versioning`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill bioinformatics-seq-qc-pipeline && npx skills add aniruddhaadak80/skills --skill bioinformatics-variant-calling-sop && npx skills add aniruddhaadak80/skills --skill lab-informatics-protocol-versioning
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills