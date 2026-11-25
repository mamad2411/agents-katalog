---
name: build-model
description: Scoped machine-learning model development — framing, leakage-safe dataset construction, baseline, training, business-terms evaluation, model card, scoring pipeline, and monitoring plan. Use for churn/propensity, forecasting, segmentation, or any predictive modelling.
---

# Build Model — ML Development

Owner: `data-scientist`, with `analytics-engineer`/`data-engineer` for data plumbing. Args describe the goal, e.g. `/build-model churn prediction for monthly subscribers`.

## Procedure

1. **Frame — and screen.** Define: prediction target (unit, horizon, exact label definition), how predictions will be used (who acts, at what threshold, scored how often), success criterion in business terms ("flag 60% of churners in the top decile we can call"). A model earns its keep only once it drives an action — a modest model wired into a decision beats a brilliant one nobody uses, and beating the current guess is usually enough. Then the screening question: **would a heuristic or segmentation answer this well enough?** If yes, deliver that instead and stop — say why. If the goal is to *change* behaviour with a treatment (offer, outreach), consider **uplift modelling** — rank persuadables by incremental effect, not raw propensity — which needs a randomised control group (design via `/experiment`).

2. **Privacy screen.** If the model uses data about people or its output will be attached to a person, run `/privacy-review` before building the dataset. It sets the risk tier (minimal / limited / high), which features are off the table, and whether a human must be able to override the output. A feature that proxies for a protected characteristic (postcode for ethnicity, first name for gender) is a design decision to make now, not a finding to explain later.

3. **Confirm feasibility.** Enough labelled history? (rule of thumb: hundreds of positive examples minimum). Features available *at prediction time*? Environment ready ({{ML_ENVIRONMENT}})? If data is missing, route ingestion to data-engineer before modelling.

4. **Build the modelling dataset — leakage-safe.** Point-in-time correct features only; document label window vs feature window with a timeline diagram in the README. Train/validation/test split: time-based for temporal problems, grouped by entity where entities repeat. Persist the dataset-building code; never hand-edit data.

5. **Baseline first.** Majority class / last value / seasonal naive / simple regression — whichever fits. All later models are judged against this.

6. **Train.** Start interpretable-and-boring (logistic regression, gradient-boosted trees; ETS/ARIMA-class for forecasts); reach for **ensembles** (random forests, boosting, stacking) only when the accuracy gain is worth the interpretability cost. Wrap all preprocessing (impute/scale/encode/select/resample) in a **pipeline fit on the training fold only** — no fitting on the full data before splitting. Tune modestly (grid/randomized/successive-halving); use **nested CV** when tuning and reporting on the same data. For **class imbalance** (churn, fraud), use class weights or train-fold resampling and threshold-tune to the business cost — never optimise raw accuracy. Seeds set, versions pinned in `models/<name>/requirements.txt`.

7. **Evaluate in business terms.** Primary: the success criterion from step 1 (e.g. precision/recall at the actionable threshold, MAPE at the planning horizon). Secondary: calibration if probabilities are consumed, per-segment performance (does it fail a key segment?), stability across time slices, and honest uncertainty (forecast intervals). Always shown alongside the baseline.

8. **Document.** `models/<name>/MODEL_CARD.md`: purpose and **intended use** (the decision it supports, and uses it is *not* validated for), owner, data and date ranges, features, algorithm, performance vs baseline, segment caveats, known limitations, retraining cadence and trigger. Where the model scores or decides about people, the card also carries: the **risk tier** from the privacy review; a **fairness evaluation** — error rates and predictive value by the groups that matter, with the criterion you optimised and the trade-off stated (`analytics.md` Part 1: you cannot equalise both when base rates differ); the **human oversight** arrangement — who can override a prediction and how a person affected can contest it; and the personal data used with its classification.

9. **Ship the scoring path.** A reproducible script: fresh data in → predictions out to a warehouse table or file the team can consume (`models/<name>/score.py` or equivalent). Schedule per the use case via {{ORCHESTRATOR or "documented manual run"}}.

10. **Monitoring plan.** Input drift checks, fresh-label performance tracking, per-group performance where the fairness evaluation applies, and the retraining trigger — handed to `performance-monitor` as queries/thresholds.

11. **Review, then confirm before automation.** `analysis-reviewer` checks the evaluation before results are presented — leakage and an optimistic split are the defects it is looking for. If model outputs will drive automated customer-affecting decisions, get explicit user sign-off on thresholds and failure modes before wiring anything up; a `high` risk tier also needs the privacy contact named in `knowledge/governance-policy.md`.

For a forecast of a metric over time, use `/forecast` — it has the backtesting and interval-calibration procedure this skill does not.

---

> Created by Colin Beck — https://www.linkedin.com/in/beckcolin/
