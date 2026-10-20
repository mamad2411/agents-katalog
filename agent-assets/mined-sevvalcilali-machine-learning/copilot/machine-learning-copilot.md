<!-- .github/copilot-instructions.md - Guidance for AI coding agents for this repo -->
# Avazu CTR — Copilot instructions

This file gives concise, actionable guidance to AI coding agents working on this repository. Focus on discoverable, reproducible patterns and concrete entry points.

## Big picture
- Purpose: binary CTR prediction on Avazu dataset (target: `click`).
- Main components:
  - `src/train_streaming.py` — primary streaming trainer (SGDClassifier + BernoulliNB ensemble, partial_fit, MLflow logging, periodic joblib checkpoints).
  - `src/train_baseline.py` — quicker baseline (FeatureHasher -> SGDClassifier) used for fast iteration.
  - `src/predict.py` — simple post-training smoke-check that expects an artifact containing a model and a hasher.
  - `src/feature_utils.py` — canonical feature pipeline: token format, cross features, missing-value handling, escaping and performance notes.

## Key workflows & commands ✅
- Local dev environment: create and activate the venv, then install packages:
  - `python3 -m venv .venv && source .venv/bin/activate`
  - `pip install -r requirements.txt` (or use `make install` which installs core libs)
- Quick checks:
  - `make sanity` → runs `src/sanity_check.py` to validate `data/train.gz` columns and cardinalities.
  - `make predict` → runs `src/predict.py` (reads `models/sgd_hashing.joblib` by default).
  - `make streaming` → runs `src/train_streaming.py` (takes longer; use small CHUNK_SIZE / MAX_TRAIN_CHUNKS for fast iterations).

## Project-specific conventions & gotchas ⚠️
- Data expectation: `data/train.gz` is the canonical CSV.gz input; scripts read it directly (no explicit downloader).
- Feature encoding: `to_feature_dict(df, ...)` produces token dicts of the form `"col=value": 1` and cross tokens `"cross:colA=valA|colB=valB": 1`.
  - Escaping: `|` and `=` are percent-escaped (see `_escape_token_part`).
  - Default behaviour: `skip_missing=True` (NaNs are omitted).
- Hashing size: default `n_features = 2**20` (1,048,576). Keep consistent hasher at training and inference; models saved include a `hasher` object when possible.
- Artifact shapes vary:
  - `models/sgd_hashing.joblib` (used by `src/predict.py`) expects keys `"model"` and `"hasher"`.
  - `train_streaming.py` saves `models/ctr_ensemble_hashing.joblib` with keys `"sgd"`, `"nb"`, `"hasher"` (ensemble). Be careful when switching artifacts — adapt `predict.py` accordingly.

## Debugging & iterative experimentation tips 🔧
- For fast experiments, reduce `nrows` in `train_baseline.py` or set in-script constants:
  - Lower `CHUNK_SIZE` and `MAX_TRAIN_CHUNKS` in `train_streaming.py` to run small end-to-end checks.
- Resume training: `train_streaming.py` supports `RESUME_FROM` pointing to a checkpoint (`models/checkpoints/ckpt_chunk_*.joblib`). Checkpoint dict contains `sgd`, `nb`, `hasher`, `trained_rows`, `chunk_idx`.
- Validation: first `VAL_ROWS` rows are used as a fixed validation set; changing this number changes the held-out set (affects reproducibility of metrics).

## MLflow & metrics 📊
- Streaming experiment logs to MLflow (`avazu_ctr_streaming`) and writes `metrics/metrics.json`. Key params logged: `n_features`, `cross_list`, `class_weight`, and `ensemble`.
- Unit of evaluation: prefer AUC / LogLoss (class imbalance handled via `class_weight='balanced'`).

## What to change when adding features or models
- If you add new cross features, update `CROSS_PAIRS` in `train_streaming.py` and mirror changes in `to_feature_dict` calls.
- When adding a new model type, ensure saved artifact includes a `hasher` and that `predict.py` or a new inference script expects the artifact shape.

## Examples to follow (concrete snippets)
- Inference using existing artifact (see `src/predict.py`): load artifact, extract `hasher`, transform `to_feature_dict(..., add_feature_cross=False)` for prediction.
- Streaming checkpoint structure (from `train_streaming.py`) — preserve keys when saving/loading to support `RESUME_FROM`.

---
If any section above is unclear or you want more detail (e.g., example unit tests, CI commands, or artifact format normalization), tell me which part to expand and I will update this file. ✅
