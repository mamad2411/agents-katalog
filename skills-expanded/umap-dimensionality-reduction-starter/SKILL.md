# UMAP Dimensionality Reduction Starter

Use this skill to embed a tiny labeled feature matrix with UMAP and summarize the resulting 2D geometry.

## What This Skill Does

- reads a toy feature matrix with labels
- computes a deterministic 2D UMAP embedding
- summarizes per-label centroids and separation
- emits machine-readable point coordinates for downstream plotting

## Run

```bash
./slurm/envs/statistics/bin/python skills/statistical-and-machine-learning-foundations-for-science/umap-dimensionality-reduction-starter/scripts/run_umap_dimensionality_reduction.py --input skills/statistical-and-machine-learning-foundations-for-science/umap-dimensionality-reduction-starter/examples/toy_embedding_input.tsv --out scratch/statistics/umap_embedding_summary.json
```
