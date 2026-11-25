# Scanpy Cell-Type Annotation Starter

Use this skill to score marker-gene programs with Scanpy and assign simple cell-type labels on a deterministic toy single-cell matrix.

## What it does

- Loads a small count matrix, marker sets, and optional truth labels.
- Normalizes counts, log-transforms them, and applies `scanpy.tl.score_genes`.
- Assigns the top-scoring label per cell and reports per-cell scores plus optional accuracy.

## When to use it

- You need a verified starter for marker-based cell-type annotation.
- You want a compact example of `scanpy.tl.score_genes` before moving to larger reference-mapping workflows.
- You need deterministic JSON output for tests or downstream demos.

## Example

```bash
slurm/envs/scanpy/bin/python skills/transcriptomics/scanpy-cell-type-annotation-starter/scripts/run_scanpy_cell_type_annotation.py \
  --counts skills/transcriptomics/scanpy-cell-type-annotation-starter/examples/toy_counts.tsv \
  --markers skills/transcriptomics/scanpy-cell-type-annotation-starter/examples/toy_markers.json \
  --truth skills/transcriptomics/scanpy-cell-type-annotation-starter/examples/toy_truth.tsv \
  --summary-out scratch/scanpy-cell-annotation/summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/transcriptomics/scanpy-cell-type-annotation-starter/tests -p 'test_*.py'`
- Expected summary: `accuracy == 1.0` and the predicted label counts split `3` vs `3`
