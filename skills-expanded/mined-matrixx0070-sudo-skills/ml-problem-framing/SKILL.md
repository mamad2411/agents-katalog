---
name: ml-problem-framing
version: 1.0.0
description: Frame a classic ML problem by fixing target, prediction unit, metric, baseline, feasibility, and leakage risk before any modeling.
author: matrixx0070
tags: [ml, framing, target, metric, baseline]
capabilities: []
---

## When to use

Use this before touching a model, when someone hands you a business goal ("reduce churn", "predict fraud") and you must convert it into a supervised learning problem with a measurable target and an honest feasibility read.

**Not for:** building LLM applications, prompting, or agents (see `ai-agent-design`, `ai-prompt-design`) — those frame around instructions, not labeled targets. Not for descriptive analytics or "what happened" questions with no prediction (see `data-explore`, `data-analyze`).

## Method

1. Write the decision the prediction serves. If no downstream action changes, stop — you want analytics, not ML.
2. Define the prediction unit: exactly one row = one (entity, timestamp) you score. Decision point: per-user, per-event, or per-(user, day)? This fixes everything downstream.
3. Define the target precisely, including the label window. Decision point: classification (churn in next 30d), regression (LTV), or ranking? Write the SQL that would compute the label.
4. Pick the metric from the decision cost. Decision point: imbalanced + ranked action → PR-AUC / precision@k; calibrated probabilities needed → log loss / Brier; symmetric error → RMSE/MAE.
5. Set a baseline: majority class, last-value, or a simple rule. Any model must beat this to justify itself.
6. Audit feasibility: is the signal in the data available AT PREDICTION TIME? List features and their as-of availability.
7. Flag leakage risk: any feature computed using post-outcome data (refund flags, resolution timestamps) is leakage. Mark each candidate as safe / suspect.

## Example

Goal: "reduce churn." Unit = one subscriber per month-end. Target = `cancels within 30 days of snapshot` (binary). Metric = precision@top-5% (retention team can only call 5% of the base), baseline = "flag anyone with a support ticket last week" (precision 0.11). Feasibility: usage, tenure, tickets all known at snapshot — OK. Leakage flag: `cancellation_reason` is populated only after churn → excluded.

## Pitfalls

- **Metric mismatch.** Optimizing accuracy on a 2%-positive problem — a "predict no" model scores 98%. Match the metric to the action.
- **Fuzzy label window.** "Will churn" with no horizon is unlearnable. Always bound the target in time.
- **Silent leakage.** Using columns that only exist after the outcome. Audit as-of availability per feature.
- **No baseline.** Declaring success with no reference. A rule-based baseline reframes what "good" means.

## Output format

```
# ML Problem: <name>
DECISION: <action the prediction drives>
UNIT: one row = <entity @ timestamp>
TARGET: <definition + label window> | TYPE: <clf|reg|rank>
METRIC: <primary> because <cost>; guardrail: <secondary>
BASELINE: <rule> -> <score>
FEASIBILITY: <signal available at predict-time? y/n + notes>
LEAKAGE RISK: <feature: safe|suspect|excluded>
```
