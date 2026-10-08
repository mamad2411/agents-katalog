---
name: removebatch
description: >-
  Remove batch effects from phyloseq with MMUPHin::adjust_batch using the BATCH
  variable while preserving the biological TARGET covariate. Use when the user
  mentions removebatch, MMUPHin, batch correction, or adjust_batch on phyloseq.
disable-model-invocation: true
---

# Remove Batch (MMUPHin)

## Purpose

Optional post-import correction: remove batch effect with MMUPHin based on the BATCH variable solving for the real variable.

Reference implementation: `/mnt/tank/scratch/dsmutin/ixodes/Metananalysis/ticks_metaanalyse.Rmd` (`adjust_batch`).

Follow project rules: **validation-first**, **reproducibility**, **method-decision-tracking**, **slurm-execution-policy** for large jobs.

## Inputs

| Arg | Meaning | Default |
|-----|---------|---------|
| `--rds` | Phyloseq `.rds` or list with `$phyloseq` | required |
| `--outdir` | Output directory | `test/removebatch/run` |
| `--batch-var` | BATCH column name | from RDS `$batch` or `batch` |
| `--covariate` | Real / TARGET column to preserve | from RDS `$target` or `grazing` |
| `--diagnostic-plot` | Path for MMUPHin diagnostic PDF/PNG | `{outdir}/mmuphin_diagnostic.pdf` |

## Workflow

```
Removebatch:
- [ ] Step 1: Load RDS; resolve phyloseq + batch_var + covariate
- [ ] Step 2: Validate ≥2 batch levels; covariate present; sample overlap
- [ ] Step 3: Relative-abundance matrix (features × samples) as in ticks_metaanalyse
- [ ] Step 4: MMUPHin::adjust_batch(batch=BATCH, covariates=TARGET)
- [ ] Step 5: Rebuild phyloseq keeping tax/sam/**original tree** (tip-pruned only; never drop/rebuild); save RDS + structure report
- [ ] Step 6: Register artifact; render diagnostic if produced
```

## Executable

```bash
Rscript .cursor/skills/removebatch/scripts/removebatch.R \
  --rds test/code-review-phyloseq/grazing_phyloseq.rds \
  --outdir test/removebatch/grazing \
  --batch-var batch \
  --covariate grazing

Rscript .cursor/skills/removebatch/scripts/removebatch.R --self-test
```

Thin hook: `.cursor/hooks/removebatch.sh`

## Outputs

| Artifact | Content |
|----------|---------|
| `phyloseq_batchadj.rds` | Adjusted phyloseq (relative abundances) |
| `removebatch-report.json` | Parameters, levels, structure of tax/otu/sam/tree |
| `mmuphin_diagnostic.pdf` | Optional MMUPHin diagnostic |

## Notes

- Does **not** invent batch labels; missing/single-level BATCH → exit.
- Does **not** drop or reconstruct `phy_tree`; insufficient tip overlap → fail.
- Prefer SLURM for very large feature×sample matrices.
