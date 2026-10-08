# Repository Guidelines

## Scope
This file is the single operating guide for AI and human contributors in `omnifinan`.  
It reflects current code behavior, especially macro data sourcing, cache semantics, output stability, and verification rules.

## Source Policy Boundary
- Do not change macro fixed-source policy unless explicitly requested.
- China macro baseline: AkShare official channels.
- International macro baseline: FRED / IMF / World Bank.
- Singapore may use stable fixed sources not identical to CN/US mix.
- Keep one reliable provider per metric; avoid duplicate parallel providers.

## Runtime Data Boundary
- Repository stores code and cold/static assets only.
- Runtime hot data must not be written into the repo.
- Runtime base path: `OMNIX_PATH/omnifinan/`.
- Required runtime directories:
- `request_cache/`
- `datasets/`
- `reports/`
- `logs/`
- Master macro dataset path:
- `OMNIX_PATH/omnifinan/datasets/macro_indicators_history/fixed_sources_with_dbnomics_proxies__master.json`

## Macro Cache and Refresh Rules
- `UnifiedDataService.get_macro_indicators` is datasets-first:
- master payload stored directly in `datasets/macro_indicators_master/`;
- **not** stored in `request_cache/` (immune to TTL-based `cleanup_expired`);
- query windows are filtered subsets of one master payload.
- Stale policy is series-level:
- threshold = `3 * inferred_cycle_days`;
- fallback = `30 days` if cycle cannot be inferred.
- Anti-loop guard:
- if non-empty cache refreshed within 24h, skip stale refresh and return local data.
- Keep history snapshots for longitudinal tracking.

## Output and Compatibility Contract
- Preserve unified API external structures.
- Structured macro output keys must stay stable:
- `meta`, `dimensions`, `metrics`, `chart_data`.
- Preserve derived metric fields used downstream:
- `yoy`, `mom`, `qoq`, `trend_short`, `trend_medium`, `volatility`.
- Maintain backward-compatible aliases; do not silently break existing keys.
- Prefer alias cloning over duplicate pulls.
- For unavailable fixed-source metrics that remain part of the active interface, return explicit errors:
- `source = fixed_sources_unavailable`
- clear `error` message
- never silent NA.
- If a metric is explicitly retired from the active interface, remove the key entirely and record it in the register below.

## Operational and Modification Constraints
- Do not broaden scope beyond the user request.
- Do not revert unrelated local changes.
- Keep edits minimal, deterministic, and technically concise.
- Avoid repeated full refresh loops when sources have no delta.
- Prefer subset refresh when supported.
- Prefer local cached payload for repeated analysis/report generation.

## Required Verification
After macro logic changes, run:
- `pytest tests/test_macro_source_policy.py`
- `pytest tests/test_macro_structured.py`
- `pytest tests/test_macro_visualize.py`

After factor mining / backtest changes, run:
- `pytest tests/test_factor_mining.py`
- `pytest tests/test_factor_backtest.py`

## Typical Macro Usage
1. `get_macro_indicators(start_date, end_date)`
2. `get_macro_indicators_structured(start_date, end_date)`
3. Build reports from `metrics` fields (`yoy`, `mom`, trends, volatility, source/error).

## Proxy / Degradation Register (Macro data sources)

When a macro series cannot be fetched from its intended upstream and we apply a proxy, we **retire the legacy key** and expose the proxy as a new canonical key. Record the breaking change here so we can revert later.

- Date: 2026-03-05

  - Retired: `china_caixin_pmi_manufacturing` → New canonical: `china_pmi_manufacturing`
    - DBnomics series_id: `NBS/M_A0B01/A0B0101`
    - Rationale: Caixin feed not found/available via DBnomics; AkShare caixin feed stalled around 2025-09.
    - Semantics: PMI (50 = expansion) but **not the same survey** as Caixin.
    - Revert path: if Caixin source becomes available, reintroduce Caixin under a *new* explicit key (e.g., `china_caixin_pmi_manufacturing`) and keep NBS key.

  - Retired: `china_caixin_pmi_services` → New canonical: `china_pmi_services`
    - DBnomics series_id: `NBS/M_A0B02/A0B020C`
    - Rationale: Caixin services PMI not found/available via DBnomics; AkShare caixin feed stalled around 2025-09.
    - Semantics: PMI-like index; label indicates seasonal adjustment.
    - Revert path: same as above.

  - Retired: `eu_pmi_manufacturing` → New canonical: `eu_industrial_confidence_indicator`
    - DBnomics series_id: `Eurostat/EI_BSSI_M_R2/M.BS-ICI-BAL.SA.EA20`
    - Rationale: Euro area PMI not found via DBnomics search; AkShare euro PMI feed stalled around 2025-09.
    - Semantics: Confidence balance (not PMI 0-100 scale); sign/scale differ.
    - Revert path: prefer true PMI series once a reliable source is added; reintroduce PMI under explicit key.

  - Retired: `china_m2_yoy` → New canonical: `china_m2_yoy`
    - DBnomics series_id: `NBS/M_A0D01/A0D0102`
    - Rationale: AkShare M2 feed stalled around 2025-09; NBS series available via DBnomics.
    - Note: trailing `NA` may exist; use last valid observation.
    - Revert path: if AkShare resumes timely updates, reintroduce it under explicit key (e.g., `china_m2_yoy_akshare`).

  - Retired: `china_fx_reserves` → New canonical: `china_fx_reserves`
    - DBnomics mapping: provider=`IMF`, dataset=`IFS`, REF_AREA=`CN`, INDICATOR=`RAXGFX_USD`
    - Rationale: NBS annual FX reserves series is too lagged; SAFE/ORA dataset appears to only cover 2020 in DBnomics API.
    - Semantics: proxy; verify indicator definition before hard-depending.
    - Revert path: use SAFE/NBS monthly series if/when available; reintroduce under explicit key.

- Date: 2026-03-06

  - Temporarily removed from active macro interface: `china_cpi_yoy`
    - Prior source: `akshare:china_official:nbs`
    - Rationale: upstream latest row is published with `NaN`, causing the last valid observation to stall at 2025-08 while continuing to trip staleness checks.
    - Interface behavior: do not emit this key in `get_macro_indicators()` or structured views until a reliable fixed source is restored.
    - Revert path: reintroduce only after a fixed source returns timely non-null observations.

  - Temporarily removed from active macro interface: `china_industrial_production_yoy`
    - Prior source: `akshare:china_official:nbs`
    - Rationale: no reliable replacement found in current fixed-source set; AkShare latest valid observation is stale.
    - Interface behavior: do not emit this key in `get_macro_indicators()` or structured views until a reliable fixed source is restored.
    - Revert path: restore once a timely fixed source is verified.

  - Temporarily removed from active macro interface: `china_imports_yoy`
    - Prior source: `akshare:china_official:customs`
    - Rationale: upstream latest row is published with `NaN`, leaving the last valid observation stale and no suitable replacement exists in the current fixed-source set.
    - Interface behavior: do not emit this key in `get_macro_indicators()` or structured views until a reliable fixed source is restored.
    - Revert path: restore once a timely fixed source is verified.
