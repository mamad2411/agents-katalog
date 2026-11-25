---
name: mlp
description: >-
  Trains sklearn MLP and PyTorch embedding MLP on Adult Income data. Use for
  MODEL-005, mlp_torch.py, script 10, Figure 9 training curves.
---

# MLP Skill

## Workflow

1. Sklearn: `mlp_sklearn` via `pipelines.build_model_pipeline` + `05_tune_models` or `10_run_mlp_experiments`.
2. PyTorch: `mlp_torch.train_embedding_mlp` with categorical embeddings.
3. Save training curves to `results/metrics/mlp_*.json`.

## Rules

- Same train/test split as other models.
- Selection metric: macro F1 (5-fold CV on train).
