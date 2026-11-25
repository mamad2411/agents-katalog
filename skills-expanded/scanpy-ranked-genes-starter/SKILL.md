# Scanpy Ranked Genes Starter

Use this skill to run a deterministic toy differential-expression pass with Scanpy and extract top marker genes per group from a small count matrix.

## What it does

- Loads a toy count matrix and per-cell group labels.
- Normalizes counts, log-transforms the matrix, and runs `scanpy.tl.rank_genes_groups`.
- Returns compact JSON with top ranked genes for each group.

## When to use it

- You need a minimal, local, verified Scanpy starter beyond QC.
- You want a template for marker ranking or toy single-cell differential-expression checks.

## Inputs

- `--input`: tab-separated count matrix
- `--groups`: tab-separated `cell/group` labels
- `--method`: Scanpy ranking method, default `t-test`
- `--top-n`: number of genes per group, default `3`
- `--out`: optional JSON output path

## Example

```bash
slurm/envs/scanpy/bin/python skills/transcriptomics/scanpy-ranked-genes-starter/scripts/run_scanpy_ranked_genes.py \
  --input skills/transcriptomics/scanpy-ranked-genes-starter/examples/toy_counts.tsv \
  --groups skills/transcriptomics/scanpy-ranked-genes-starter/examples/toy_groups.tsv \
  --top-n 2 \
  --out scratch/scanpy-ranked-genes/summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/transcriptomics/scanpy-ranked-genes-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_local_skills -v`
