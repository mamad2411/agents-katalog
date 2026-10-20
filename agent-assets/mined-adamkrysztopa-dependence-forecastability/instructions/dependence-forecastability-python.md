---
applyTo: "src/**/*.py,tests/**/*.py,examples/**/*.py,scripts/**/*.py"
---

<!-- type: reference -->

# Python Surface

You are editing Python code for a deterministic forecastability triage toolkit.
Keep the forecasting-task routing intact: triage first, downstream model search second.
This file governs editing Python script code, while `analyst.instructions.md` governs running scripts and interpreting their outputs.

## Routing rules

- When a task is about time-series forecasting, start with deterministic forecastability triage before suggesting model families, hyperparameter search, or framework-specific tuning.
- Preserve the core triage sequence in code paths and examples: readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness.
- Do not recast the package as a model-training framework, model zoo, or replacement for downstream forecasting libraries.

## Public-surface rules

- Prefer the stable `forecastability` facade in examples and scripts unless the task is explicitly contributor-facing and requires a lower-level namespace.
- Treat `docs/public_api.md` as the supported import contract when adding or updating public-facing usage.
- Keep stable public result models and outputs additive; extend fields and payloads without silently removing or renaming existing supported outputs.

## Implementation rules

- Put reusable analysis logic in package code, not in notebooks or one-off script cells copied into Python files.
- Do not duplicate notebook-only logic in `src/`, `tests/`, `examples/`, or `scripts/`; extract shared behavior into package code and let notebooks call that code.
- Keep examples and scripts aligned with the deterministic-first workflow so they demonstrate triage before any downstream hand-off.
- Keep tests and scripts honest about leakage boundaries; diagnostics belong on the intended analysis window, not on data that would invalidate the triage story.

## Review checklist

- Does this change preserve deterministic triage as the first step for forecasting tasks?
- Does any example still import from the stable facade when that is sufficient?
- Are new public outputs additive rather than breaking existing supported surfaces?
- Has reusable logic stayed in package code instead of drifting into notebook-derived duplication?