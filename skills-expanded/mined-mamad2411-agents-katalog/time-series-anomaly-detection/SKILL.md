---
skillx:
  name: time_series_anomaly_detection
  purpose: Detect and rank category-level March 2020 spending surges/slumps using pre-March history as the counterfactual training basis.
  scope_in:
    - per-category daily anomaly detection from cleaned transaction data
    - tasks requiring directional anomaly ranking (positive surge, negative slump)
    - strict baseline (pre-March) vs treatment window (March 2020) separation
  scope_out:
    - not for causal attribution
    - not for feature engineering
    - not for training with treatment-window leakage
  requires:
    - `transactions_cleaned.csv` with valid datetime, category, and numeric value fields
    - explicit cutoff and prediction window definitions
  preferred_tools:
    - Prophet-style per-category forecasting
    - explicit train/eval split control
    - signed anomaly index computation
  risks:
    - leakage from March data into model fit
    - wrong aggregation grain or wrong value column
    - producing only one-sided ranking (surge only / slump only)
    - sign inversion in anomaly interpretation
  examples:
    - input: Rank unusual category behavior during March 2020 from pre-March history.
      expected_behavior: output signed anomaly index artifact usable for selecting top surge and top slump categories.
---

# Stage Contract

## Input Artifact
- `transactions_cleaned.csv`

## Output Artifact
- `category_anomaly_index.csv`

Minimum columns expected:
- category field
- signed `Anomaly_Index` (or equivalent directional index)
- support metrics (e.g., total_actual, total_predicted, coverage days)

## Handoff Rule to DiD Stage
- DiD stage uses this artifact only to select target categories (top surge, top slump).
- This stage must not make causal claims; ranking only.

# Execution Guidance

1. Aggregate transactions to the model-ready daily category grain.
2. Fit per-category forecasting models on pre-March data only.
3. Score March window observations against forecast intervals.
4. Compute directional anomaly index and rank categories.
5. Preserve enough metadata for deterministic top/bottom selection.

# Pre-Handoff Checks (Required)

- Training data excludes March 2020 treatment window.
- Prediction/evaluation window corresponds to March 2020 as required.
- Value column used for aggregation is numeric and semantically correct.
- Ranking output includes both positive and negative anomalies.
- Category identifiers match those needed by downstream DiD filtering.

# Common Failure Modes

- Counterfactual trained on contaminated time windows.
- Wrong grain (e.g., non-daily or mixed groups) yielding unstable ranks.
- Ranking by absolute anomaly only, losing surge/slump direction.
- Producing plausible table shape with evaluator-incompatible category labels.