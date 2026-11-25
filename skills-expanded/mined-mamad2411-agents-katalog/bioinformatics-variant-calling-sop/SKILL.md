---
name: bioinformatics-variant-calling-sop
description: "Consistent callers, filters, and annotation sources so variant lists compare across runs."
---
# Standardize variant calling and annotation

> Consistent callers, filters, and annotation sources so variant lists compare across runs.

**Track:** 🧬 Biotech & Pharma · **Domain:** Bioinformatics · **Level:** advanced · **~50 min**

**Who this is for:** Bioinformaticians, Lab Scientists, Regulatory Affairs, Genetic Engineers, Clinical Data Managers

## When to Use This Skill

Consistent callers, filters, and annotation sources so variant lists compare across runs.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Fix caller versions and filter thresholds in writing before processing
2. Normalize representations (left-align, split multiallelics) consistently
3. Annotate against versioned databases recording exact release dates
4. Apply depth/quality filters appropriate to assay type
5. Validate a truth-set sample each run before trusting outputs
6. Store VCFs with full provenance: sample, pipeline hash, references

## Common Pitfalls

- Annotation databases drifting between analyses
- Filter tuning per-run destroying comparability

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill bioinformatics-variant-calling-sop
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill bioinformatics-variant-calling-sop -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills