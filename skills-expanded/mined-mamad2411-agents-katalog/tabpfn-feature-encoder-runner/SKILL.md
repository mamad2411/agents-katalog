---
name: tabpfn-feature-encoder-runner
description: Use when running, configuring, validating, or documenting the tabpfn-feature-encoder training repo, including conda setup, runner scripts, output artifacts, tests, and Git hygiene.
---

# TabPFN Feature Encoder Runner

## Repo Basics

- Repo root: `tabpfn-feature-encoder`.
- Main 12-class source residual config: `configs/source_residual_mlp.yaml`.
- Particle GNN config: `configs/source_gnn.yaml`.
- Particle transformer config: `configs/source_transformer.yaml`.
- Full workflow launcher: `bash scripts/run_full_workflow.sh`.
- Dispatcher spelling: `bash scripts/run full workflow`.
- Launcher: `bash scripts/run_source_encoder.sh`.
- Source transfer rerun: `bash scripts/run_source_transfer.sh`.
- CP transfer rerun: `bash scripts/run_cp_transfer.sh`.
- Open-data transfer rerun: `bash scripts/run_gamgam_transfer.sh`.
- Context comparison plots: `bash scripts/plot_context_comparison.sh`.
- Test runner: `bash scripts/run_tests.sh`.
- Package CLI: `tabpfn-encoder-train train --config configs/source_residual_mlp.yaml`.
- Output dir is configured by `output_dir`.

## Environment

Use the existing conda env:

```bash
conda activate tabpfn
python -m pip install -e ".[train,atlas,plots]"
```

The runner falls back to `conda run --no-capture-output -n tabpfn` if the console script is not on `PATH`.

## Runner Behavior

`scripts/run_full_workflow.sh`:

- Runs `configs/source_residual_mlp.yaml`, `configs/source_gnn.yaml`, and `configs/source_transformer.yaml` by default.
- For each config, trains the 12-class source encoder and then runs source-task, CP even/odd, and open-data transfer evaluations.
- Runs configs in parallel by default when multiple GPUs are visible, with one config per GPU.
- Streams per-config logs to the terminal and writes full logs to `runs/workflow_logs/<timestamp>/`.
- Set `TABPFN_WORKFLOW_STREAM_LOGS=0` to disable live log streaming.
- Select GPUs with `TABPFN_WORKFLOW_GPUS=0,1,2,3 bash scripts/run_full_workflow.sh`.
- Force sequential execution with `TABPFN_WORKFLOW_PARALLEL=0 bash scripts/run_full_workflow.sh`.
- Runs context comparison plotting at the end unless `TABPFN_WORKFLOW_PLOT=0` is set.
- Accepts optional config paths to restrict the workflow: `bash scripts/run_full_workflow.sh configs/source_residual_mlp.yaml`.

`scripts/run_source_encoder.sh`:

- Sets `TABPFN_MODEL_CACHE_DIR` to `$SCRATCH/tabpfn_model_cache` unless already set.
- Sets `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` unless already set.
- Reuses an existing checkpoint from `~/.cache/tabpfn` when available.
- Accepts an optional config path: `bash scripts/run_source_encoder.sh configs/other.yaml`.
- Runs the GNN with: `bash scripts/run_source_encoder.sh configs/source_gnn.yaml`.
- Runs the transformer with: `bash scripts/run_source_encoder.sh configs/source_transformer.yaml`.
- Reruns source-task transfer from a checkpoint with: `bash scripts/run_source_transfer.sh`.
- Reruns CP even/odd transfer from a checkpoint with: `bash scripts/run_cp_transfer.sh`.
- Reruns open-data transfer from a checkpoint with: `bash scripts/run_gamgam_transfer.sh`.
- Plots encoder comparison PDFs with: `bash scripts/plot_context_comparison.sh`.

## Model Layout

- Keep distinct encoder definitions in separate files under `src/tabpfn_feature_encoder/models/`.
- Current modules: `mlp.py`, `feature_gate.py`, `feature_mixer.py`, `gnn.py`, `transformer.py`.
- Keep model selection in `models/factory.py`.
- Keep PyTorch import helpers in `models/torch_utils.py`.
- Leave `models/encoders.py` as a compatibility re-export layer, not the place for new model logic.

## Source Training Expectations

- Training uses frozen TabPFN support/query episodes; only encoder weights are optimized.
- For the 12-class source task, the trainer uses binary ECOC by default:
  `encoder.tabpfn_max_classes: 2`, `encoder.many_class_redundancy: 4`.
- Default source configs use `output_dim: 72`, `learning_rate: 0.0002`,
  `grad_clip_norm: 1.0`, and `validation_episodes: 8`.
- Source embeddings are detached before fitting the TabPFN support prompt by
  default (`detach_support_gradients: true`) so the encoder learns from query
  gradients without differentiating through prompt construction.
- Validation is episodic and rotates through validation support/query contexts
  using the same 50/50 support/query split as training.
- Epoch logs should include `grad_norm_mean`, `grad_norm_max`, and
  `skipped_nonfinite_updates`.

## Validation Commands

Prefer these before finalizing code changes:

```bash
bash scripts/run_tests.sh
```

Pass pytest selectors through for focused checks, for example:

```bash
bash scripts/run_tests.sh tests/test_config.py
```

Clean generated Python/cache files before committing:

```bash
find . -type d -name __pycache__ -prune -exec rm -rf {} +
find src -maxdepth 2 -type d -name '*.egg-info' -prune -exec rm -rf {} +
```

## Artifacts

Training saves:

- `metrics.json`
- `training_summary.json`
- `epoch_metrics.csv`
- `encoder_classifier.pkl`
- `run_metadata.json`
- `source_generalization/source_12_class_generalization_metrics.json`
- `source_generalization/source_12_class_generalization_context_scan_metrics.csv`
- `source_generalization/source_12_class_generalization_context_scan_roc_auc.png`
- `source_generalization/source_12_class_generalization_baseline_proba.npy`
- `source_generalization/source_12_class_generalization_frozen_encoder_proba.npy`
- `cp_generalization/cp_even_odd_generalization_metrics.json`
- `cp_generalization/cp_even_odd_generalization_context_scan_metrics.csv`
- `cp_generalization/cp_even_odd_generalization_context_scan_roc_auc.png`
- `cp_generalization/cp_even_odd_generalization_baseline_proba.npy`
- `cp_generalization/cp_even_odd_generalization_frozen_encoder_proba.npy`
- `open_data_generalization_metrics.json` in `transfer.output_dir`
- `open_data_generalization_context_scan_metrics.csv` in `transfer.output_dir`
- `open_data_generalization_context_scan_roc_auc.png` in `transfer.output_dir`
- `open_data_generalization_baseline_proba.npy` in `transfer.output_dir`
- `open_data_generalization_frozen_encoder_proba.npy` in `transfer.output_dir`
- `context_scan_comparison/*_roc_auc_comparison.pdf`
- `context_scan_comparison/*_accuracy_comparison.pdf`

Terminal metrics print to three decimals; CSV/JSON keep full precision.
