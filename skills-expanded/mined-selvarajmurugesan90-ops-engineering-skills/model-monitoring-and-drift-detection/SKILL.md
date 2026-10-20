---
name: model-monitoring-and-drift-detection
description: >
  Guides setting up production model monitoring for data drift, concept
  drift, prediction drift, and model quality decay, with concrete statistical
  tests, thresholds, and alerting/retraining triggers. Use when the user asks
  to "monitor a model in production", "detect data drift", "detect concept
  drift", set up dashboards/alerts for model quality, investigate a silent
  model performance regression, or decide when a model needs retraining.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: mlops
  maturity: stable
---

# Model Monitoring And Drift Detection

## Purpose

A deployed model does not fail loudly when the world changes underneath it —
it fails quietly, by making steadily worse predictions while every
infrastructure health check stays green. Model monitoring and drift detection
closes that gap: it tracks the statistical properties of inputs, outputs, and
(where ground truth eventually arrives) prediction quality over time, and
raises an alert or triggers retraining before silent degradation turns into a
business incident. This is operationally distinct from standard application
monitoring (latency, error rate, uptime) because the failure mode here is a
model that is "working" in every infrastructure sense while being wrong.

## When to use

- The user wants to set up monitoring for a model already in production
  (dashboards, alerts, SLOs on model quality, not just system health).
- The user asks to detect data drift (input feature distribution shift),
  concept drift (the relationship between features and label changes), or
  prediction drift (output distribution shift).
- The user is investigating a reported "the model seems worse lately" issue
  with no obvious infrastructure cause.
- The user wants to define thresholds that trigger a retraining pipeline or
  a page to on-call (tie-in with
  [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md)).
- The user needs to choose or implement a statistical drift test (PSI, KL
  divergence, KS test, chi-squared) and set sensible thresholds.
- The user is designing a feedback-loop system to capture delayed ground
  truth labels for online evaluation.

## Prerequisites & environment

- Logged inference inputs and outputs (with timestamps and a model version
  tag) at a sampling rate sufficient for statistical tests — logging 100% of
  traffic is ideal but sampling (e.g. 10–20%) is acceptable for high-QPS
  services if done without bias.
- A reference/baseline distribution to compare against — typically the
  training data distribution or a recent "known good" production window.
- A metrics/monitoring backend: Evidently AI, WhyLabs, Arize, Fiddler, or a
  homegrown pipeline computing statistics in a scheduled job (Airflow, cron)
  writing to Prometheus/Grafana, or a data warehouse + BI dashboard.
- Eventually-available ground truth labels if you intend to monitor actual
  model quality (accuracy/AUC/etc.) rather than only distributional proxies
  — note many production systems have delayed or partial labels (e.g. fraud
  chargebacks arrive weeks later); design monitoring to work with proxy
  signals in the interim.
- Access to the model registry and lineage metadata to attribute a drift
  signal to a specific model version and its training data (see
  [data-and-model-lineage](../data-and-model-lineage/SKILL.md)).

## Step-by-step guidance

1. **Establish a reference distribution** per feature and per model output,
   frozen at the time the currently-deployed model version was trained —
   not a constantly-shifting "last N days" window, which would mask gradual
   drift.
2. **Choose drift metrics appropriate to the data type:**
   - Numeric features: Population Stability Index (PSI) or
     Kolmogorov–Smirnov (KS) test statistic.
   - Categorical features: chi-squared test or PSI on category proportions.
   - Model output distribution (regression scores or class probabilities):
     KL divergence or PSI between reference and current output distributions.
   - Common PSI interpretation used in practice: `< 0.1` no significant
     shift, `0.1–0.25` moderate shift (investigate), `> 0.25` significant
     shift (treat as an actionable alert) — tune per feature's known
     volatility rather than applying one threshold blindly everywhere.
3. **Compute PSI concretely** for a feature `avg_rating_30d`:
   ```python
   import numpy as np

   def population_stability_index(expected, actual, bins=10):
       breakpoints = np.quantile(expected, np.linspace(0, 1, bins + 1))
       breakpoints[0], breakpoints[-1] = -np.inf, np.inf
       e_counts, _ = np.histogram(expected, bins=breakpoints)
       a_counts, _ = np.histogram(actual, bins=breakpoints)
       e_pct = np.clip(e_counts / len(expected), 1e-6, None)
       a_pct = np.clip(a_counts / len(actual), 1e-6, None)
       return float(np.sum((a_pct - e_pct) * np.log(a_pct / e_pct)))

   psi = population_stability_index(reference_ratings, current_week_ratings)
   # psi = 0.31 -> significant shift, alert
   ```
4. **Monitor prediction distribution and calibration** even without fresh
   ground truth: a sudden change in the mean predicted probability, the
   fraction of predictions above a decision threshold, or class balance is a
   proxy signal that something changed upstream (e.g. an input pipeline bug,
   not necessarily "real" drift).
5. **Monitor model quality directly once labels arrive**, on whatever delay
   is realistic for the domain (same-day for click-through, weeks for fraud
   chargebacks): recompute AUC/precision/recall/RMSE on a rolling window and
   compare against the value at validation time.
6. **Set alert thresholds with both a statistical bar and a business-impact
   bar** — e.g. alert on PSI > 0.25 *and* require it to persist for more
   than one monitoring window, to avoid paging on single-day noise from a
   holiday or a marketing campaign spike.
7. **Segment monitoring by relevant slices**, not just aggregate — drift
   often hides in a subpopulation (e.g. a new geographic market, a new
   device type) while aggregate statistics look stable.
8. **Wire alerts to action**: a sustained drift alert should either page
   on-call for investigation or automatically kick off a retraining pipeline
   run (see
   [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md))
   — decide which per use case's risk tolerance, and never auto-promote a
   retrained model straight to production as the automated response (see
   [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md)
   for the required gated promotion path).
9. **Log every alert and its resolution** (false alarm / real drift /
   retrained / rolled back) into the lineage record so the team builds a
   track record of which thresholds are well-calibrated over time.

## Best practices

- Freeze the reference distribution at training time and treat "drift" as
  divergence from that frozen baseline — do not silently recompute the
  baseline from recent production data, or you will normalize away exactly
  the drift you're trying to catch.
- Monitor inputs, outputs, and (when available) quality metrics together;
  input drift without output drift, or output drift without input drift, are
  both diagnostically meaningful and point to different root causes.
- Track drift and quality per model version, tied to the model registry
  entry that produced the predictions, so you can tell whether a regression
  correlates with a specific deployment.
- Build monitoring in from day one of production deployment, not as an
  afterthought added after an incident — retrofitting requires reconstructing
  a reference distribution you may not have preserved.
- Prefer a small number of well-understood, well-calibrated alerts over many
  noisy ones; alert fatigue causes real drift signals to get ignored.
- Version and test the monitoring code itself (drift computation logic) —
  a bug in a PSI calculation is indistinguishable from real drift until
  someone investigates, wasting on-call time.

## Common pitfalls

- **Symptom:** Model accuracy silently degrades over several months with no
  alert firing, discovered only when a business stakeholder notices declining
  outcomes.
  **Fix:** Don't rely solely on infrastructure health checks (uptime,
  latency, error rate) as a proxy for model health; instrument explicit
  distributional and (when available) quality monitoring from initial
  deployment, with a frozen training-time reference baseline.

- **Symptom:** A drift alert fires constantly on a highly seasonal feature
  (e.g. retail transaction volume around holidays), causing the team to
  start ignoring drift alerts altogether.
  **Fix:** Calibrate thresholds per feature based on its known seasonal/
  natural variance rather than one blanket threshold, and consider
  seasonally-adjusted or week-over-week (rather than static-baseline)
  comparisons for features with strong known cyclicality.

- **Symptom:** Aggregate drift metrics look fine, but a specific customer
  segment (e.g. a newly launched region) experiences materially worse model
  performance for weeks before anyone notices.
  **Fix:** Segment drift and quality monitoring by relevant slices (region,
  device, customer tier, new vs. established users), not only in aggregate;
  add slice-level dashboards as a standard part of monitoring setup, not an
  afterthought.

- **Symptom:** A retraining pipeline auto-triggers on a drift alert and
  auto-promotes the new model straight to production, and the new model
  turns out worse because the drift was actually caused by a temporary
  upstream data pipeline bug, not real distribution shift — so the
  retrained model learned from bad data too.
  **Fix:** Never let an automated drift-triggered retrain skip the gated
  promotion and human/automated evaluation checks described in
  [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md)
  and
  [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md);
  treat "retrain" and "promote to production" as distinct, separately gated
  actions.

## Worked example

A subscription-churn model, `churn-predictor-v3`, is deployed to production.

1. At deployment, the team snapshots the training feature distributions
   (e.g. `days_since_last_login`, `support_tickets_30d`, `plan_tier`) as the
   frozen reference baseline, tagged to model version 3.
2. A scheduled daily job computes PSI for each monitored feature against
   that baseline, plus KL divergence on the predicted churn-probability
   distribution, writing results to a Grafana dashboard backed by
   Prometheus.
3. Week 6 post-deployment: `days_since_last_login` PSI climbs from a
   steady ~0.04 to 0.29 over three consecutive days — flagged as a
   significant, persistent shift (exceeds the 0.25 threshold for more than
   one window).
4. On-call investigates and finds the login-tracking event pipeline changed
   timestamp semantics after an unrelated platform migration two weeks
   earlier — not a genuine behavioral change in users, but this pipeline
   change is exactly the kind of upstream issue that must be traced via
   [data-and-model-lineage](../data-and-model-lineage/SKILL.md).
5. The upstream pipeline is fixed; the team confirms PSI returns to baseline
   over the next three days and closes the alert as "resolved — upstream
   data bug, not model drift," logging this resolution for future
   threshold calibration.
6. Separately, four weeks later, `support_tickets_30d` PSI rises to 0.19
   alongside a real drop in retention-model recall (from labeled outcomes
   arriving on a 30-day delay) — this time judged genuine concept drift from
   a product change, and it triggers the scheduled retraining pipeline
   (see
   [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md)),
   whose output goes through the normal gated promotion before reaching
   production.

## Cross-references

- [data-and-model-lineage](../data-and-model-lineage/SKILL.md)
- [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md)
- [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md)
- [feature-store-design](../feature-store-design/SKILL.md)
