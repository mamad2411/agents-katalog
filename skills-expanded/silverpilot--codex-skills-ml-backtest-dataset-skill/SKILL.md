---
name: "ml-backtest-dataset"
description: "Codex-local skill bundle for ML inference, dataset scripts, backtests, and advisory-only model boundaries."
---

# ML Backtest Dataset

This is a Codex-local skill bundle, not a guaranteed auto-discovered official
Codex skill.

## Rules

- Scout first: map model inference code, dataset builders, feature generation,
  backtest scripts, stored artifacts, and tests.
- Keep ML output advisory unless a future explicitly approved task changes that
  product boundary.
- Avoid training/validation leakage and document any temporal split assumptions.
- Do not mutate production data or overwrite model artifacts without explicit
  user approval.
- Backtest evidence must include data range, assumptions, and limitations.
- Preserve risk-policy and paper-trading guardrails around predictions.

## Evidence

- Dataset and feature paths inspected.
- Inference/backtest entrypoints identified.
- Advisory-only boundary preserved.
- Validation or backtest command proposed or run.
