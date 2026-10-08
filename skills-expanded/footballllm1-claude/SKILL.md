# CLAUDE.md

Project memory for Claude Code / Cowork sessions on this repo.

## What this project is

Closed-loop **LLM-distilled synthetic data** for a football injury prediction
task. The reference dataset is `data/raw/data.csv` (n=800, 19 cols, balanced
binary target `Injury_Next_Season`).

**Paper direction** (2026-05-08): "The Interpretability–Utility Frontier in
LLM-Distilled Synthetic Tabular Data."

Three contributions:
1. **LLM-as-statistical-spec-generator** — LLM emits JSON parametric spec
   (per-cell means, stds, correlations); local Gaussian copula sampler
   generates rows. This avoids LLM direct sampling (LLMs are provably bad
   at exact distribution sampling).
2. **SHAP fidelity as first-class metric** — ρ (Spearman on SHAP ranks)
   captures feature-attribution drift that standard metrics miss.
3. **Pareto frontier** — mixup between LLM and TVAE lets users choose any
   point on the interpretability–utility trade-off curve.

## Repo layout (high level)

```
configs/             YAML configs (base, llm, experiment)
data/raw/            real data.csv  (800 rows)
data/processed/      train/holdout/test splits (after 01_prepare_data.py)
data/synthetic/      per-round synthetic CSVs
prompts/             system prompt + Jinja2 round template (K/U split trust region)
src/footballllm/     library code (importable)
  data/              loader, schema, splits
  generators/        BaseGenerator, TVAEGen, LLMGen, MixupGen, sampler, llm_clients
  postprocess/       hard constraints (BMI, ranges, NaN/inf guard)
  models/            XGBoost wrapper
  feedback/          shap_gap, structure_gap, error_mining, prompt_builder
  metrics/           utility, fidelity, calibration, joint J
  pipeline/          round, loop, early_stop (GAM inverted-U)
  utils/             logging, seed, io
scripts/             entry points (01..06)
tests/               pytest unit tests
results/runs/        per-run artifacts; results/figures/ for plots
lunwen/              the two reference PDFs (DO NOT MODIFY)
```

## How to run

```bash
bash setup_env.sh                       # one-shot: conda env + deps + editable install
conda activate footballllm
export DEEPSEEK_API_KEY=sk-...          # DeepSeek V3 API key

# Data prep + baselines
python scripts/01_prepare_data.py       # split real data
python scripts/02_train_baseline.py     # Real / TVAE baselines

# Single run (debug)
python scripts/03_run_loop.py --rounds 10 --feedback joint

# Full ablation (4 modes × 5 seeds)
python scripts/04_run_ablations.py --seeds 0 1 2 3 4 --feedback joint k_only u_only alternating

# Pareto sweep (mixup λ)
python scripts/06_pareto_sweep.py --feedback u_only --seeds 0 1 2 3 4

# Figures
python scripts/05_make_figures.py
```

## Conventions Claude must follow when editing this repo

1. **No notebook-style scripts in `src/`.** Library code is import-only with
   typed signatures. All side effects live in `scripts/` or `tests/`.
2. **Configs over flags.** Long-lived knobs (J weights, round budget, batch
   sizes) belong in `configs/*.yaml`. Only run-specific overrides go on the
   CLI.
3. **One responsibility per module.** A new feedback signal goes in
   `src/footballllm/feedback/` as its own file with a `FeedbackSignal` dataclass.
4. **Determinism.** Every script accepts `--seed` and threads it through the
   `set_global_seed` util. Generators must seed their own RNGs.
5. **Don't touch `data/raw/data.csv`.** It is the canonical real dataset.
6. **Don't touch `lunwen/`.** Reference PDFs only.
7. **LLM keys** come from env vars (`DEEPSEEK_API_KEY` is the default;
   `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` are fallbacks). Never hardcode keys
   in configs.  `LLM_PROVIDER=mock` runs the pipeline end-to-end without
   network, useful for CI and tests.
8. **DeepSeek V3 (`deepseek-chat`) is the recommended model.** V4 Pro with
   thinking mode enabled is slower and less stable for this task.
9. **Pinned versions.** If you bump a dependency, update both `setup_env.sh`
   and `pyproject.toml` and verify the import sanity check still passes.

## Things explicitly out of scope (don't do unless asked)

- Federated / privacy budgets (DP-SGD etc.)
- Image/UAV modalities
- Custom CUDA / distributed training
- Deploying anything as a web service

## Status / known gotchas

- `Position` is categorical; do not silently label-encode it inside the
  generator — round-trip the string label.
- `BMI = Weight_kg / (Height_cm/100)**2` is a hard constraint enforced by
  `postprocess/constraints.py` after every generation.
- `pygam==0.12.0` is the GAM library used for inverted-U detection (matches
  Yamaguchi et al. 2025).
- ctgan 0.10.2 pulls in torch; the CPU wheel is fine on Apple Silicon.
- **openai==1.55.0** (bumped from 1.51.0) — fixes httpx≥0.28 `proxies` kwarg
  incompatibility.
- **NaN/inf guards** in both `generators/sampler.py` (clips mean/std, fills
  NaN after sampling) and `postprocess/constraints.py` (fills NaN/inf before
  `.astype("int64")`).
- **Markdown code-fence parsing** in `LLMGenerator._parse_spec` strips
  ```json``` wrappers and logs the specific parse error on failure.
- **Early stop** defaults: patience=3, min_rounds=3, gam_check_after=4.
- **violation_report** now runs AFTER `apply_constraints` — reports residual
  violations on the constrained batch, not the raw LLM output.
- **K/U split trust region** in `prompts/round_template.j2`: K uses tighter
  bounds (±15% mean, ±20% std), U uses wider bounds (±25% mean, ±30% std).
- **J weights** (2026-05-08): α=0.35 ρ, β=0.40 AUC, γ=0.25 (1−ECE), δ=0.00
  ( Σ term dropped — low discrimination across variants).

## Paper target venues

KDD 2027 / AAAI 2027.  NeurIPS 2026 workshop (SynData / D&B) for quick exposure.

## 2026-05-08 ablation results (k_only + joint + u_only + alt, 5 seeds)

| feedback | mean_J | best_J | best_ρ | best_AUC |
|----------|--------|--------|--------|----------|
| k_only | 0.806 | 0.934 | 0.890 | 0.965 |
| u_only | 0.754 | 0.822 | 0.808 | 0.927 |
| joint | 0.761 | 0.807 | 0.835 | 0.901 |
| alternating | 0.741 | 0.799 | 0.688 | 0.866 |
| TVAE | 0.788 | — | 0.580 | 0.926 |
| Real | 0.982 | — | 1.000 | 0.979 |
