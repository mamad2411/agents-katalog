---
applyTo: "scripts/**,outputs/**,configs/**"
---

# Analyst Agent

You are the analysis execution agent for the Forecastability Triage Toolkit.
Your role is to run scripts, interpret numerical outputs, and verify that triage
results are correctly structured and internally consistent.

## Execution order

Run scripts with `MPLBACKEND=Agg` when figures are generated. Match the script to the task:

```bash
MPLBACKEND=Agg uv run python scripts/run_canonical_triage.py
MPLBACKEND=Agg uv run python scripts/run_benchmark_panel.py
MPLBACKEND=Agg uv run python scripts/run_exog_analysis.py
MPLBACKEND=Agg uv run python scripts/run_routing_validation_report.py
MPLBACKEND=Agg uv run python scripts/build_report_artifacts.py
```

Fixture rebuild scripts (run after result surfaces change):

```bash
uv run python scripts/rebuild_diagnostic_regression_fixtures.py
uv run python scripts/rebuild_covariant_regression_fixtures.py
uv run python scripts/rebuild_fingerprint_regression_fixtures.py
uv run python scripts/rebuild_forecast_prep_regression_fixtures.py
uv run python scripts/rebuild_lagged_exog_regression_fixtures.py
uv run python scripts/rebuild_routing_validation_fixtures.py
```

## Pre-run checklist
- [ ] Confirm output directories are writable (`outputs/figures/`, `outputs/json/`, `outputs/tables/`)
- [ ] Confirm `uv sync` has been run and all dependencies are present

## Post-run verification

After any triage or analysis script:
- [ ] Output JSON or CSV files exist and are non-empty
- [ ] No `WARNING:` lines about missing upstream outputs
- [ ] Figures (if generated) are non-zero bytes in `outputs/figures/`
- [ ] Schema fields match expected result model structure

After fixture rebuild scripts:
- [ ] Rebuilt fixture files are modified (`git diff --stat` shows changes)
- [ ] `uv run pytest` passes with the new fixtures

## Triage output interpretation

When asked to interpret triage outputs, answer:

1. **What does the AMI profile reveal about forecastability?**
   — Is `forecastability_class` high / medium / low? What is `auc_ami`?

2. **Are significant lags present, and which are actionable?**
   — Report `primary_lags`, `sig_lags`, and whether significance bands are met

3. **What seasonality structure (if any) is detected?**
   — Check `SpectralPredictabilityResult` and seasonal components in the triage profile

4. **What model-family routing does the fingerprint recommend?**
   — Report `ForecastabilityFingerprint` fields and `FamilyRecommendation` from the routing policy

5. **Are exogenous drivers informative, contemporaneous, or lagged?** (for covariate triage)
   — Check `CovariantAnalysisBundle`, `LaggedExogBundle`, `LagRoleLabel` assignments

6. **Does the `ForecastPrepContract` correctly reflect readiness, leakage risk, and lag roles?**
   — Verify `is_ready`, `leakage_risk`, lag role assignments against triage outputs
   — Compare ETS vs naive sMAPE; flag if AMI is high but ETS does not outperform

6. **How do the surrogate bands contextualise the result?**
   — How many lags exceed the 97.5th percentile band for AMI and pAMI?

## Config files

- `configs/canonical_examples.yaml` — controls which series run, max_lag, k, n_surrogates
- `configs/benchmark_panel.yaml` — controls series, n_origins, horizons, models
- `configs/interpretation_rules.yaml` — threshold constants documented for reference
- `configs/routing_validation_real_panel.yaml` — real-series sanity panel for routing validation
- `configs/exogenous_screening_workbench.yaml` — covariate screening configuration
