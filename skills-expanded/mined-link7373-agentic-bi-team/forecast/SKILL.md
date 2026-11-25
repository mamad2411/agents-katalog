---
name: forecast
description: Build a time-series forecast for a business metric — baselines first, rolling-origin backtest, calibrated prediction intervals, bias check, and a monitoring plan — and report it separately from the target and the plan. Use for revenue, demand, signups, capacity, or any "what will this be next quarter" question.
---

# Forecast

Owner: `data-scientist`, with `analytics-engineer` for the history and `performance-monitor` for tracking it afterwards. Args name the metric, horizon, and grain, e.g. `/forecast monthly MRR for the next two quarters by segment`.

Read `analytics.md` Part 6 first. For a predictive model about entities (which customers will churn) use `/build-model`; this skill is for a series over time.

## Procedure

1. **Frame the use.** Who will act on this forecast, on what decision, and how wrong can it be before the decision changes? That sets the horizon, the grain, and how much effort the intervals deserve. Ask whether they want a **forecast** (what we expect), and keep it separate from the **target** and the **plan** — if a number is going to be adjusted to match a goal, it is not a forecast and should not be labelled one.

2. **Define the series exactly.** The metric from `knowledge/metrics-catalog.md`, its grain, its period boundaries (`knowledge/business-context.md` fiscal calendar), and whether the latest period is complete. Forecasting from a partial period is the most common silent error.

3. **Check the history** with `data-quality-engineer`'s lens: gaps, duplicates, definition changes, tracking migrations, and outages. Mark every known event from the change ledger on a plot of the series. Decide, and log, how each break is handled: truncate the history, model the break, or adjust the affected periods. Never interpolate over a data outage silently.

4. **Look before modelling.** Plot the series, its seasonal pattern, and its year-over-year view. Is there enough history — at least two full seasonal cycles to estimate seasonality at all? If not, say what the forecast can and cannot capture.

5. **Baselines.** Compute naive, seasonal naive, and drift forecasts. These are the bar, and often the answer.

6. **Backtest — rolling origin, at the real horizon.** Pick several cut-off dates across the last one or two years; for each, fit on data before it and forecast the horizon the stakeholder needs. Score WAPE (or MAE), and bias, per horizon step. Record the table. No random splits, no features unknown at forecast time.

7. **Candidate models, simplest first.** Exponential smoothing / ETS, a seasonal ARIMA-class model, or a regression on trend, seasonality, and known drivers. Where the environment has one available, a pretrained time-series model may be added as another candidate — it goes through the same backtest. Add complexity only where the backtest says it pays. **A model that does not beat seasonal naive in the backtest is not used**; report the baseline as the forecast and say why.

8. **Intervals — and check them.** Produce an 80% interval (and 95% if the decision needs it). Then measure **empirical coverage** in the backtest: the share of actuals that fell inside. If coverage is short of nominal, replace the model's interval with a **conformal** one built from the backtest's own error quantiles at each horizon step. Report the coverage achieved.

9. **Reconcile hierarchies.** If the forecast is by segment or region, the parts must sum to the total. Forecast where the signal is best and reconcile, then check each level's backtest error still holds.

10. **Sanity-check against the business.** Does the forecast imply a growth rate, a market share, or a capacity that is implausible? Does it contradict a known committed change (a price rise next month, a contract ending)? Known future events that the history cannot contain are added as explicit, labelled adjustments — never folded in invisibly.

11. **Write `models/<name>/FORECAST.md`** (and add a row to `models/README.md`):
    - **Headline:** the central forecast and its range, in one sentence a planner can use
    - Forecast table: period, point, 80% low/high — beside, and separate from, any target
    - **What drives it** and what it assumes continues
    - **Backtest results** vs seasonal naive: error and bias by horizon, interval coverage
    - **Known risks not in the model**, and explicit adjustments made
    - **How wrong it has been before** — the plain-English version of the backtest ("at three months out, typically within ±6%")
    - Retraining cadence, owner, and the provenance footer (`standards/reporting-standards.md`)

12. **Ship the scoring path.** A reproducible script: fresh history in, forecast table out (`models/<name>/forecast.py`), seeds set, versions pinned. Schedule via {{ORCHESTRATOR or "documented manual run"}}.

13. **Monitor.** Hand `performance-monitor` the query that compares each realised period to its forecast, and the trigger: error outside the backtest range, or bias in one direction, for three consecutive periods means re-fit. Realised error goes on the monthly scorecard beside the metric.

## Reporting rules

- Never a point forecast without a range. Never a range that stays the same width as the horizon grows.
- Round to the precision the uncertainty supports. A forecast of "$4,318,207" with a ±8% range is "$4.3M".
- State the as-of date of the data on every chart and table.
- When the forecast changes materially from the last one, say what moved it — new data, a changed assumption, or a model change — and by how much each.

## Environment

Baselines, a backtest loop, and conformal intervals need only SQL plus a short Python script on the standard library. Statistical models need {{ML_ENVIRONMENT}} with `statsmodels` or similar; install on demand and pin versions in `models/<name>/requirements.txt`.

---

> Created by Colin Beck — https://www.linkedin.com/in/beckcolin/
