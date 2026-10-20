<!-- type: reference -->

# Copilot Instructions

A deterministic forecastability triage toolkit for time series — univariate triage, covariate informativeness, fingerprinting, routing validation, and forecast-prep hand-off.

This repository is a deterministic forecastability triage toolkit for time series. When the task is time-series forecasting, do not jump directly to model fitting. Start with forecastability triage first: readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness. Only then recommend downstream model families or framework-specific settings.

AMI is the core mutual-information estimator. pAMI (partial AMI) is one extension. The toolkit also includes GCMI, transfer entropy, PCMCI-AMI causal screening, spectral predictability, forecastability fingerprinting, and the `ForecastPrepContract` hand-off surface.

CLI, API, notebooks, MCP, and agents are optional access or narration layers around the same deterministic outputs.

## Start Here

- `README.md`
- `docs/quickstart.md`
- `docs/public_api.md`
- `docs/recipes/forecast_prep_to_external_frameworks.md`
- `examples/minimal_python.py`
- `examples/minimal_covariant.py`
- `docs/examples_index.md`

## Repository Rules

- Prefer the stable facade from `forecastability` unless a lower-level namespace is explicitly needed.
- Treat `docs/public_api.md` as the supported import contract.
- Keep additive compatibility for stable Pydantic result fields.
- Do not describe the package as a model zoo or a replacement for downstream forecasting libraries.

## Repository Scope (binding)

See [docs/plan/aux_documents/developer_instruction_repo_scope.md](../docs/plan/aux_documents/developer_instruction_repo_scope.md) for the full directive.

- The core package is **framework-agnostic**. Do not add `darts`, `mlforecast`, `statsforecast`, or `nixtla` as runtime, optional-extra, dev, or CI dependencies of the core repository.
- The forecast-prep contract (`ForecastPrepContract`) is a **hand-off boundary**. Stop at the contract; do not add `to_<framework>_spec()` or `fit_<framework>()` helpers as supported public API.
- Framework usage examples belong in `docs/recipes/**` as illustrative snippets, never executed by core CI, and (from v0.4.0) in the sibling `forecastability-examples` repository.
- Notebooks live in the `forecastability-examples` sibling repository. Do not add notebooks to this repo. Prefer scripts in `scripts/`, examples in `examples/`, and pages in `docs/recipes/`.
- Reusable analysis logic belongs in package code (`src/forecastability/`), not in notebooks or scripts.