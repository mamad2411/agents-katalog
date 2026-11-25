---
name: power-analysis
description: >
  Perform statistical power analysis for A/B experiments — sample size calculation,
  experiment duration estimation, minimum detectable effect (MDE), and power computation.
  Use when the user mentions power analysis, sample size, MDE, experiment duration,
  statistical power, or needs to size an A/B test.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
---

# Power Analysis for A/B Experiments

Guide the user through a rigorous statistical power analysis for A/B/n experiments.

## Workflow

### 1. Gather inputs

Ask the user for:
- **Metric type**: proportion (conversion rate), continuous (revenue, duration), or ratio (revenue per session)
- **Baseline value**: current metric value
- **Baseline variance** (continuous/ratio metrics): standard deviation or variance
- **Minimum detectable effect (MDE)**: smallest lift worth detecting
- **Number of variants**: default 2
- **Traffic split**: default equal split
- **Significance level (alpha)**: default 0.05
- **Power (1 - beta)**: default 0.80
- **Test sidedness**: default two-sided
- **Daily traffic/enrollment rate** (optional): for duration estimation

### 2. Compute

Write and execute a self-contained Python script using `scipy.stats` and/or `statsmodels`.

**Proportions:** n = (Z_{alpha/2} + Z_beta)^2 * (p1*(1-p1) + p2*(1-p2)) / (p2 - p1)^2
**Continuous:** n = (Z_{alpha/2} + Z_beta)^2 * 2 * sigma^2 / delta^2
**Ratio metrics:** Use the delta method for variance estimation.

For multiple variants or metrics, adjust alpha using Bonferroni or Holm-Bonferroni.

### 3. Present results

Display a summary table with all parameters, sample size per variant, total sample size, and estimated duration.

### 4. Sensitivity analysis

Show how required sample size varies across a range of MDE values (+/- 50% around target).

### 5. Document

Offer to write the analysis to a markdown file for experiment proposals.

## Reverse calculations

Support three directions: sample size (given MDE), MDE (given n), power (given n and MDE).
