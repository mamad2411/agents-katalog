---
skillx:
  name: did_causal_analysis
  purpose: Estimate demographic drivers for selected surge/slump categories using separated intensive and extensive margin DiD workflows and emit evaluator-compatible causal output.
  scope_in:
    - DiD driver analysis for categories pre-selected by anomaly ranking
    - dual-margin outputs (intensive + extensive) with statistical estimates
    - final structured report generation aligned with intermediate DiD tables
  scope_out:
    - not for selecting anomaly categories
    - not for cleaning or feature engineering
    - not for collapsing intensive and extensive panel logic into one table
  requires:
    - selected categories from `category_anomaly_index.csv`
    - respondent covariates from `survey_feature_engineered.csv`
    - cleaned transaction/respondent linkage from prior stages
  preferred_tools:
    - statsmodels-style DiD regressions
    - explicit sparse-vs-complete panel builders
    - schema-consistent JSON report writing
  risks:
    - intensive/extensive table construction errors
    - malformed joins between respondent IDs and category-period outcomes
    - direction/sorting mistakes for surge vs slump driver ranking
    - polished JSON that is inconsistent with computed intermediates
  examples:
    - input: Explain top surge/slump categories with top intensive/extensive demographic drivers.
      expected_behavior: produce consistent intermediate DiD artifacts and final `causal_analysis_report.json` with required structure.
---

# Stage Contract

## Input Artifacts
- `category_anomaly_index.csv` (category selection source)
- `survey_feature_engineered.csv` (numeric respondent covariates)
- cleaned transactional/respondent linkage artifacts from earlier stages

## Output Artifacts
- `did_intensive_analysis_data.csv`
- `did_extensive_analysis_data.csv`
- `causal_analysis_report.json`

## Handoff/Completion Rule
- This is the terminal analytic stage.
- Final report must be traceable to intermediate DiD tables and selection categories.

# Execution Guidance

1. Select target categories from anomaly artifact (top surge + top slump as required).
2. Build intensive margin table (participant-only sparse panel; continuous outcome).
3. Build extensive margin table (complete entity-period panel including nonparticipants; binary outcome).
4. Run DiD estimation for both margins with valid feature set.
5. Sort and extract top drivers in task-consistent direction, then write final JSON.

# Pre-Output Checks (Required)

- Intensive table excludes nonparticipants by design.
- Extensive table includes nonparticipants explicitly (0/1 participation outcome).
- Feature columns used in regressions are numeric and aligned to respondent IDs.
- Selected categories in analysis match anomaly artifact selections.
- `causal_analysis_report.json` schema is complete and internally consistent with intermediate outputs.

# Common Failure Modes

- Using complete panel logic for intensive margin (effect dilution).
- Using sparse panel logic for extensive margin (participation-rate bias).
- Feature-driver ranking inconsistent with estimated signs/statistics.
- Outputting correct-looking JSON with missing/misaligned category blocks.