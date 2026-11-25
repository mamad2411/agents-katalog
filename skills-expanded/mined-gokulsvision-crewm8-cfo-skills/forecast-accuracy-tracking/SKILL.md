---
name: forecast-accuracy-tracking
description: Tracks forecast accuracy over time — measures forecast vs actuals, identifies systematic biases, improves forecasting processes, and builds a culture of accountability. Use when the user mentions "forecast accuracy," "forecast vs actuals," "why were we off," "improve forecasting," "forecast bias," "MAPE," or asks about "how accurate were our forecasts" or "what's our forecast track record."
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, forecast-accuracy, variance-analysis, forecasting-process, continuous-improvement]
related_skills: [revenue-forecasting, budget-creation-management, cash-forecasting, scenario-planning, board-reporting]
inputs_required: [historical-forecasts-with-dates, actual-results-for-each-forecast, forecast-assumptions-register, contextual-notes-per-forecast]
deliverables: [forecast-accuracy-dashboard, bias-analysis, root-cause-for-top-3-variances, process-improvement-recommendations]
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Forecast Accuracy Tracking

Measure how good the company's forecasts actually are. Track forecast vs actuals over time, identify where and why you're consistently wrong, and improve the forecasting process. Goal: forecasts get more accurate over time, not less, and the business learns from its mistakes.

## Purpose

Most startups track whether they hit their plan, but almost none track whether their forecasts are actually getting better. Systematic forecasting errors — consistently overestimating new logo revenue, consistently underestimating churn — compound over time and lead to bad decisions. This skill provides the methodology to measure forecast accuracy, identify persistent biases, and improve the process so decisions are made on increasingly reliable numbers.

## When to Use

- "How accurate were our forecasts?"
- "Track forecast vs actuals over time"
- "Why were we off last quarter?"
- "Improve our forecasting process"
- "What's our forecast track record?"
- "Analyze forecast bias"

## Inputs Required

1. **Historical forecasts** — for each forecasting exercise: what was forecast, when, for what period, and the forecast value.
2. **Actual results** — the realized values for each forecasted metric (revenue, costs, cash, headcount).
3. **Forecast assumptions** — the key assumptions that drove each forecast (growth rate, churn, hiring velocity, etc.).
4. **Contextual notes** — what was happening in the business when each forecast was made (new product launch, market shift, team changes).

## Quick Reference

| Metric | Formula | Target |
|--------|---------|--------|
| MAPE | Average of \|Actual − Forecast\| / \|Actual\| across periods | < 10% excellent, 10-25% decent |
| Forecast Bias | Average of (Forecast − Actual) / Actual | Near 0 (neutral) |
| FE (Forecast Error) | Actual − Forecast | Positive = conservative, Negative = optimistic |
| Horizon MAPE | MAPE broken out by 1mo/3mo/6mo/12mo horizons | Higher for longer horizons |

| MAPE Range | Interpretation |
|---|---|
| < 10% | Excellent forecasting |
| 10-25% | Decent — room for improvement |
| 25-50% | Concerning — systematic issues likely |
| > 50% | Forecasting is essentially guessing |

## Procedure

### 1. Collect Historical Forecasts

For each forecasting exercise, record:
- What was forecast (revenue, costs, cash, headcount, specific metric).
- When it was forecast (date).
- What period it covers (month, quarter, year).
- The forecast value.
- The actual value (once known).

### 2. Calculate Core Accuracy Metrics

#### Forecast Error (FE)

```
Forecast Error = Actual - Forecast
```

Sign matters: positive = you underestimated (conservative), negative = you overestimated (optimistic).

#### Absolute Percentage Error (APE)

```
APE = |Actual - Forecast| / |Actual|
```

#### Mean Absolute Percentage Error (MAPE)

```
MAPE = Average of APEs across all periods / categories
```

#### Forecast Bias

```
Bias = Average of (Forecast - Actual) / Actual
```

- **Bias > 0**: consistently overestimating (optimistic)
- **Bias < 0**: consistently underestimating (conservative)
- **Target**: bias close to 0, with random (not systematic) errors

### 3. Calculate Accuracy by Horizon

Forecasts get worse the further out they look:

| Forecast Horizon | MAPE (Revenue) | MAPE (Costs) | MAPE (Cash) |
|---|---|---|---|
| 1 month out | 5% | 3% | 2% |
| 3 months out | 15% | 10% | 12% |
| 6 months out | 25% | 18% | 22% |
| 12 months out | 40% | 30% | 35% |

### 4. Identify Systematic Errors

Where are you consistently wrong?

| Category | Bias Direction | Magnitude | Root Cause Hypothesis |
|---|---|---|---|
| New logo revenue | Overestimate | ~30% too high | Overly optimistic pipeline conversion rates |
| Churn | Underestimate | ~20% too low | Not factoring in seasonal churn patterns |
| Engineering hiring | Overestimate | ~40% too high | Assuming hiring happens at plan, but it's always slower |
| AWS costs | Underestimate | ~15% too low | Growth-driven usage increasing faster than modeled |

### 5. Root Cause Analysis

For each material variance (>10% or >$10k):

1. **Was the assumption wrong, or was there an unforeseeable event?**
2. **Structural issue** (the model is wrong) or **execution issue** (the model was right but you didn't execute)?
3. **Did you ignore a known risk** that materialized?

### 6. Process Improvements

Based on findings, recommend changes:

| Finding | Recommendation |
|---|---|
| New logo forecast consistently 30% too high | Reduce pipeline conversion rates by 25% across all stages in the model |
| Churn always worse than forecast | Add a 1-2% "unexpected churn" buffer to every forecast |
| Hiring always slower than plan | Cap hiring at 70% of plan for forecasting purposes |
| Enterprise sales cycles getting longer | Update cycle time assumptions quarterly, not annually |

### 7. Build the Accuracy Dashboard

A rolling 12-month view:

```
===== FORECAST ACCURACY DASHBOARD =====

Revenue Forecast Accuracy (MAPE, last 12 months):
  This month: 8%  |  Q avg: 12%  |  Trend: IMPROVING ↓

Cost Forecast Accuracy (MAPE, last 12 months):
  This month: 5%  |  Q avg: 7%  |  Trend: STABLE →

Cash Forecast Accuracy (MAPE, last 3 months):
  This month: 3%  |  Q avg: 4%  |  Trend: IMPROVING ↓

Current Bias:
  Revenue: -5% (conservative) ✓
  Costs: +2% (slightly optimistic) −
  Headcount: +25% (overly optimistic) ✗

Top Improvement This Quarter:
  Adjusted pipeline model → revenue MAPE improved from 18% to 12%
```

## Output Format

- Forecast accuracy dashboard (MAPE by metric, by horizon)
- Bias analysis (where you're consistently wrong)
- Root cause for top 3 largest variances
- Process improvement recommendations
- Trend: is forecasting getting better or worse?

## Done Criteria

The skill is complete when:
1. MAPE is calculated for each forecast category (revenue, costs, cash, headcount).
2. Bias is analyzed — are you consistently optimistic, conservative, or neutral?
3. Accuracy is broken out by forecast horizon (1-month, 3-month, 6-month, 12-month).
4. Root cause is identified for the top 3 largest variances.
5. Specific process improvement recommendations are made with rationale.
6. An accuracy dashboard is produced showing trend over time.

## Pitfalls

1. **Measuring accuracy without considering forecast horizon** — calling a 30% error on a 12-month forecast "terrible" when the industry benchmark for 12-month revenue forecasts is 25-40% MAPE sets an impossible standard. Always horizon-adjust your expectations.
2. **Chasing accuracy at the expense of speed** — a forecast that's 5% MAPE but takes three weeks to produce is useless for decision-making. A 15% MAPE forecast delivered in 2 days on Friday afternoon is actionable. Speed has value; don't optimize accuracy in a vacuum.
3. **Treating all forecast errors as equally important** — overestimating revenue by 20% (you planned spend that doesn't materialize) is far more dangerous than underestimating costs by 20% (you have a buffer). Weight errors by their cash consequence, not just their percentage.
4. **Using MAPE alone without bias analysis** — you can have a 10% MAPE every quarter but be 10% high every single time (systematic optimism). MAPE hides the direction; bias shows whether you're learning or just consistently wrong in the same way.
5. **Rewarding conservative forecasts** — if the implicit incentive is "never miss your forecast" rather than "be accurate," forecasters will sandbag (forecast low, beat consistently). A 3% MAPE with a -10% bias (constant sandbagging) is worse than a 12% MAPE with near-zero bias. Measure both.

### Heuristics

- **The goal isn't perfect forecasts — it's improving forecasts**: a 15% MAPE that's trending down is better than a 10% MAPE that's trending up.
- **Track at multiple horizons**: the 1-month forecast tells you about operational execution. The 12-month forecast tells you about strategic planning.
- **Separate structural from random errors**: don't change the model for one-time events. Do change it for patterns.
- **Build forecast ranges, not point estimates**: "Revenue will be $1.2-1.4M" with 80% confidence is better than "Revenue will be $1.3M."

### Edge Cases

- **Very early stage with no track record**: can't measure accuracy yet. Just document assumptions and revisit.
- **Major business model change**: historical accuracy is irrelevant. Old forecast patterns don't apply. Reset the baseline.
- **External shocks** (COVID, SVB): don't let one event distort the analysis. Exclude it or flag it separately.

## Verification

Can you answer "Are our forecasts getting better or worse over time?" and "What are we consistently wrong about?" Can you point to specific model changes this quarter that were driven by last quarter's accuracy analysis? If not, the accuracy tracking isn't driving improvement.

## Example

1. > **User**: "How accurate have our revenue and cost forecasts been over the last 12 months?"
   > **Expected behavior**: You collect the last 12 months of forecast-vs-actual pairs for revenue and costs, calculate MAPE and bias by metric and by forecast horizon (1-month, 3-month, 6-month, 12-month), present the dashboard with trend indicators, and flag the top 2 categories where you're consistently wrong with root cause hypotheses.

2. > **User**: "We missed our Q3 revenue forecast by 25%. Figure out why."
   > **Expected behavior**: You isolate Q3 forecast methodology (was it pipeline-based? cohort-based? top-down?), compare individual assumptions against actuals (new logos projected vs actual, churn projected vs actual, expansion projected vs actual, deal timing projected vs actual), identify which specific assumption broke, and recommend exactly what parameter to change in the model going forward — e.g., "Enterprise pipeline conversion was modeled at 8.4% but actual was 5.2%. Reduce stage-level conversion rates by 35%."

3. > **User**: "Improve our forecasting process based on what we've learned."
   > **Expected behavior**: You review the full historical accuracy dataset, identify the 2-3 most persistent systematic errors (not one-off misses), propose specific model parameter changes with rationale, suggest process changes (e.g., "update churn assumptions monthly instead of quarterly"), and establish a lightweight accuracy review cadence — monthly dashboard review, quarterly deeper root cause analysis.

## Linked Skills

- Revenue forecast creation → `revenue-forecasting`
- Budget creation → `budget-creation-management`
- Cash forecast → `cash-forecasting`
- Scenario planning (accuracy of ranges) → `scenario-planning`
- Board reporting (what to say about variances) → `board-reporting`
