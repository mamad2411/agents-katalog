# GWAS Summary Statistics QC Starter

Use this skill to run a deterministic local pass over GWAS summary statistics, flag common QC issues, and emit a compact interpretation plan for downstream clumping, heritability, and functional follow-up.

## What This Skill Does

- reads a GWAS summary-statistics table with common header aliases
- standardizes core fields such as chromosome, position, alleles, effect size, p-value, sample size, EAF, and INFO
- flags malformed rows, low-information variants, duplicate variant identifiers, and ambiguous palindromic SNPs
- writes a flagged TSV plus a JSON summary with top hits and recommended downstream tools

## When To Use It

- when you need a reusable starter for `gwas` beyond a notes-only frontier placeholder
- when a dataset needs fast summary-statistics QC before LDSC, fine-mapping, PRS, or interpretation work
- when you want a stable local contract that does not depend on large reference panels or remote services

## Run

```bash
python3 skills/genomics/gwas-starter/scripts/run_gwas_summary_qc.py \
  --input skills/genomics/gwas-starter/examples/toy_sumstats.tsv \
  --config skills/genomics/gwas-starter/examples/qc_config.json \
  --out-tsv scratch/gwas/gwas_qc.tsv \
  --summary-out scratch/gwas/gwas_qc_summary.json
```

## Notes

- The starter is intentionally local and deterministic. It surfaces issues that should be resolved before genome-wide downstream tools consume the file.
- Header normalization supports common aliases such as `CHR`, `BP`, `EA`, `NEA`, `BETA`, `OR`, `P`, `N`, `EAF`, and `INFO`.
- For allele harmonization against reference genomes, SSF export, or LD-based follow-up, read [`refs.md`](refs.md) and use the cited canonical tools.
