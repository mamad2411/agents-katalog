# PyDESeq2 Differential Expression Starter

Use this skill to run a deterministic toy bulk RNA-seq differential-expression pass with PyDESeq2 and summarize the ranked genes.

## What it does

- Loads a tiny count matrix and sample-condition table.
- Fits a DESeq2-style model with PyDESeq2.
- Runs the Wald test for the requested contrast.
- Returns compact JSON with the top adjusted-p-value hits and effect sizes.

## When to use it

- You need a minimal local bulk RNA-seq differential-expression starter in Python.
- You want a verified template for PyDESeq2 counts, metadata, and contrast handling.

## Example

```bash
slurm/envs/transcriptomics/bin/python skills/transcriptomics/pydeseq2-differential-expression-starter/scripts/run_pydeseq2_differential_expression.py \
  --counts skills/transcriptomics/pydeseq2-differential-expression-starter/examples/toy_counts.tsv \
  --metadata skills/transcriptomics/pydeseq2-differential-expression-starter/examples/toy_metadata.tsv \
  --out scratch/pydeseq2/differential_expression_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/transcriptomics/pydeseq2-differential-expression-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase24_frontier_closure_skills -v`
