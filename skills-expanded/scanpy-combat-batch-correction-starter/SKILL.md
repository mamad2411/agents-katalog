# Scanpy ComBat Batch Correction Starter

Use this skill to run a deterministic toy batch-correction pass with Scanpy's ComBat implementation and summarize how much the batch gap shrinks after correction.

## What it does

- Loads a toy count matrix and per-cell metadata with batch and cell-type labels.
- Builds an AnnData object, normalizes counts, and log-transforms the matrix.
- Runs `scanpy.pp.combat` on the `batch` column.
- Reports pre/post batch mean differences plus retained cell-type separation.

## When to use it

- You need a lightweight verified starter for single-cell batch correction.
- You want a local integration example before moving on to heavier `scvi-tools` workflows.

## Example

```bash
slurm/envs/scanpy/bin/python skills/transcriptomics/scanpy-combat-batch-correction-starter/scripts/run_scanpy_combat_batch_correction.py \
  --counts skills/transcriptomics/scanpy-combat-batch-correction-starter/examples/toy_counts.tsv \
  --metadata skills/transcriptomics/scanpy-combat-batch-correction-starter/examples/toy_metadata.tsv \
  --summary-out scratch/scanpy-combat/summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/transcriptomics/scanpy-combat-batch-correction-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase26_frontier_completion_skills -v`
