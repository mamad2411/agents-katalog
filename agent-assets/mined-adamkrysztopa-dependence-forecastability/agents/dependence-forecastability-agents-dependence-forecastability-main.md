# AGENTS

## Repository Identity

A deterministic forecastability triage toolkit for time series — univariate triage, covariate informativeness, fingerprinting, routing validation, and forecast-prep hand-off.

This repository is a deterministic forecastability triage toolkit for time series. When the task is time-series forecasting, do not jump directly to model fitting. Start with forecastability triage first: readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness. Only then recommend downstream model families or framework-specific settings.

AMI is the core mutual-information estimator. pAMI (partial AMI) is one extension. The toolkit also includes GCMI, transfer entropy, PCMCI-AMI causal screening, spectral predictability, forecastability fingerprinting, and the `ForecastPrepContract` hand-off surface.

Treat downstream forecasting frameworks as hand-off targets after triage, not as the core behavior of this repository.

## Navigation Order

1. `README.md`
2. `docs/quickstart.md`
3. `docs/public_api.md`
4. `docs/recipes/forecast_prep_to_external_frameworks.md`
5. `examples/minimal_python.py`
6. `examples/minimal_covariant.py`
7. `docs/examples_index.md`

## Forecasting-Task Routing Rules

1. Classify the request as univariate, covariate-aware, or batch triage.
2. Run deterministic forecastability triage before proposing model families.
3. Inspect readiness, leakage risk, informative horizons, primary lags, seasonality structure, and covariate informativeness.
4. Only then recommend downstream model-family or framework-specific settings.

## Public API

- Prefer imports from `forecastability` and `forecastability.triage`.
- Treat `docs/public_api.md` as the supported import contract.
- Avoid contributor-facing examples that depend on internals unless the task explicitly needs them.

## Editing Rules By Area

- Public result surfaces: keep stable Pydantic fields additive.
- Docs and examples: do not imply that this package performs model training.
- Notebooks: notebooks have moved to the `forecastability-examples` sibling repository. Do not add notebooks to this repo.
- Example scripts: keep them small and runnable.

## Repository Scope (binding)

See [docs/plan/aux_documents/developer_instruction_repo_scope.md](docs/plan/aux_documents/developer_instruction_repo_scope.md) for the full directive.

- The core package is **framework-agnostic**. Do not introduce `darts`, `mlforecast`, `statsforecast`, or `nixtla` as runtime, optional-extra, dev, or CI dependencies of the core repository.
- The forecast-prep contract (`ForecastPrepContract`) is a **hand-off boundary**. No `to_<framework>_spec()` / `fit_<framework>()` helpers ship as supported public API; framework mappings live as illustrative recipes only.
- Framework usage examples belong in `docs/recipes/**` (text only) and (from v0.4.0) in the sibling `forecastability-examples` repository, not in the core package or its `examples/` / `scripts/` / `tests/`.
- Prefer scripts and docs recipes. New notebooks and walkthroughs belong in the `forecastability-examples` sibling repository.

## Validation Commands

- `uv run pytest`
- `uv run pytest tests/test_api.py`
- `uv run python scripts/rebuild_diagnostic_regression_fixtures.py`
- `uv run python scripts/rebuild_covariant_regression_fixtures.py`
- `uv run python scripts/rebuild_fingerprint_regression_fixtures.py`
- `uv run python scripts/rebuild_forecast_prep_regression_fixtures.py`
- `uv run python scripts/rebuild_lagged_exog_regression_fixtures.py`
- `uv run python scripts/rebuild_routing_validation_fixtures.py`
- Run the relevant fixture rebuild script when result surfaces or examples change.

## Common Mistakes to Avoid

- Jumping directly from a forecasting prompt to model fitting.
- Describing the package as a model zoo or a replacement for downstream forecasting libraries.
- Breaking additive compatibility for stable Pydantic result fields.
- Introducing user-facing examples that depend on internal namespaces without an explicit contributor need.
- Moving reusable analysis logic into notebooks or scripts instead of package code.
