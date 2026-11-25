---
name: bioinformatics-seq-qc-pipeline
description: "Read-level QC, adapter trimming, contamination screens, and reproducible QC reporting."
---
# Quality-control sequencing data before analysis

> Read-level QC, adapter trimming, contamination screens, and reproducible QC reporting.

**Track:** 🧬 Biotech & Pharma · **Domain:** Bioinformatics · **Level:** intermediate · **~45 min**

**Who this is for:** Bioinformaticians, Lab Scientists, Regulatory Affairs, Genetic Engineers, Clinical Data Managers

## When to Use This Skill

Read-level QC, adapter trimming, contamination screens, and reproducible QC reporting.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Run read-level QC: per-base quality, GC bias, duplication profiles
2. Trim adapters/low-quality tails with documented parameter versions
3. Screen contamination against expected organism panels
4. Verify reference genome build matches annotation versions exactly
5. Emit multi-sample QC summary tables for batch comparison
6. Pin tool versions in a workflow manager (Snakemake/Nextflow) for reruns

## Common Pitfalls

- Mixed genome builds between alignment and annotation
- Batch effects mistaken for biological signal

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill bioinformatics-seq-qc-pipeline
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill bioinformatics-seq-qc-pipeline -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills