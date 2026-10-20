---
name: drift-monitor-designer
description: Design privacy-safe post-deployment monitoring for data, concept, prediction, bias, and feature-attribution drift on Kubernetes. Use for drift detection, model monitoring, SHAP drift, baseline and threshold selection, delayed-label joins, Evidently, Prometheus, alerting, or a monitor specification that connects production signals to rollback and evaluation workflows.
---

# Drift Monitor Designer

## Purpose
A model that passed every gate still rots in production as the world shifts under it. This skill designs the monitoring stack that detects that rot early — four complementary monitors, each with a baseline, a schedule, thresholds, and alert wiring — and feeds their signals back to the rollout's rollback triggers and to the eval harness so new failure modes become new eval cases. It translates the SageMaker/Azure-ML four-monitor pattern to OSS on Lambda managed Kubernetes.

## Core model to hold in your head

### First, capture the data
Nothing is monitorable that isn't recorded. Stand up **data capture** at the serving layer:
- Start with a privacy and threat-model gate: classify the traffic, identify regulated data and secrets, document the lawful purpose, and obtain required security/privacy approval before capture.
- Minimize by default. Prefer derived metrics, hashes, feature summaries, or redacted samples over raw prompts and responses. Never export regulated or tenant-confidential content to an external judge without explicit authorization and an approved data-processing path.
- When raw model **inputs** or **outputs** are necessary, redact PII/secrets before persistence; encrypt in transit and at rest; enforce tenant-scoped least-privilege access; record access; and set tested retention, deletion, and legal-hold rules.
- Set a **sampling rate** — 100% for low-volume research traffic, a fraction at scale.
- Enable it as part of the rollout, not after — a monitor with no captured history has no baseline to compare against on day one.

This capture is the raw material every one of the four monitors below consumes.

### Drift typology (name what you're watching for)
- **Data drift** — the input distribution shifts (e.g. new query patterns, new vocabulary, new categories) while the model is unchanged. Covariate shift.
- **Concept drift** — the relationship between inputs and the correct answer changes (e.g. adversaries adopt new techniques); only detectable with ground-truth labels.
- **Prediction drift** — the output distribution shifts even if you can't yet see inputs or labels moving.
- **Feature-attribution drift** — *which* features drive predictions changes (the importance ranking moves) even when distributions look stable.
- **Temporal patterns:** drift arrives as **instantaneous/sudden** (a deploy or upstream change), **gradual** (slow population shift), **periodic/recurring** (seasonality, daily cycles), or **temporary/blip** (a transient spike that self-corrects). Threshold and window design must match the pattern — a tight threshold on a periodic signal is an alarm generator.

### The four-monitor stack
| Monitor | Detects | Baseline | Needs labels? | Example metric |
|---|---|---|---|---|
| **Data quality** | Covariate shift, schema breaks, missing values, outliers | Statistics + constraints from **training data** | No | Per-feature distance vs baseline; missing/outlier rate; JS distance |
| **Model quality** | Concept drift (accuracy decay) | Metric thresholds from the **held-out eval/validation set** | **Yes** (delayed) | Accuracy, precision, recall, F1 vs baseline |
| **Bias drift** | Fairness eroding on live data | The release-gate **fairness audit** results | Yes | SPD / DI / group FPR gap drifting past threshold |
| **Feature-attribution drift** | Which features matter is changing | The release-gate **SHAP attribution** ranking | No | Ranking change of top-N attributions (NDCG-style compare) |

Run all four — they catch different, non-overlapping failures. Data-quality fires first and needs no labels (your early-warning monitor); model-quality is the ground-truth confirmation but lags (labels arrive late — allow an offset window to merge delayed labels with captured predictions); bias and attribution drift catch the subtle failures the first two miss.

### Per-monitor design (baseline · schedule · threshold · alert)
**1. Data-quality monitor** — the cheapest, label-free early warning; run it first and most often.
- *Baseline:* per-feature statistics and constraints from the training set (completeness, type, range, distribution).
- *Schedule:* frequent — hourly to daily.
- *Threshold:* per-feature distributional distance (Jensen–Shannon, or L-infinity/KS for the classic form) above a small value; missing/outlier rate above a fraction (e.g. 0.05).
- *Alert:* fire on a baseline-drift or data-type violation → notify and consider a retrain trigger.

**2. Model-quality monitor** — the ground-truth confirmation, but it lags.
- *Baseline:* the metric floors from the eval/validation set (accuracy, precision, recall, F1).
- *Schedule:* runs when ground-truth labels arrive (often delayed — humans/downstream systems label later); use a start/end offset window to merge late labels with the right captured predictions.
- *Threshold:* metric below the baseline floor.
- *Alert:* concept-drift alarm → the strongest signal to retrain.

**3. Bias-drift monitor** — fairness eroding on live data.
- *Baseline:* the fairness-audit metric values from `model-release-gate`.
- *Schedule:* periodic on captured predictions (merged with labels where the metric needs them).
- *Threshold:* SPD / DI / group-FPR-gap moving past the gate's accepted band.
- *Alert:* fairness-regression alarm → escalate; don't auto-retrain blindly (retraining on drifted data can worsen bias).

**4. Feature-attribution-drift monitor** — which features matter is changing.
- *Baseline:* the SHAP attribution ranking from the gate's explanation report (mean-abs aggregation over a baseline sample).
- *Schedule:* periodic.
- *Threshold:* a change in the **ranking** of top-N attributions past a tolerance (rank-agreement/NDCG-style).
- *Alert:* attribution-drift alarm — often the earliest sign of a subtle upstream data change distributions haven't yet revealed.

### The statistical machinery
Distributional distance is what every drift monitor ultimately computes. Match the measure to the data type — a chi-squared threshold on a numeric feature is a category error:
- **Jensen–Shannon distance** and **Population Stability Index (PSI)** — general distribution shift, any feature.
- **Kolmogorov–Smirnov** (two-sample) and **L-infinity** (max gap between CDFs; `linf_robust` for small samples) — numerical features.
- **Pearson's chi-squared** — categorical distribution shift.
- **Wasserstein** — continuous shape change.
- **KL divergence** — the asymmetric information-theoretic option.
- **Ranking-agreement (NDCG-style)** — for feature-attribution drift the "distance" is over the top-N attribution ranking, not a distribution metric.

### Threshold-setting discipline
**Start conservative — wide thresholds, then tighten** as you learn the signal's normal variance; this avoids a launch-day false-positive flood that trains the team to ignore alerts. Match the window to the temporal pattern (longer windows for periodic/seasonal signals). Track alert patterns and fix recurring root causes rather than re-tuning forever. Distinguish **model monitoring** (the four drift monitors here) from **infrastructure monitoring** (GPU/CPU/memory/network via Prometheus + DCGM) — both feed alerts, but only the latter drives autoscaling, and conflating them buries model-quality signals under resource noise.

### OSS mapping on Kubernetes
- **Evidently** — computes data-drift, prediction-drift, data-quality, and attribution reports; run it as a scheduled K8s **CronJob** over captured data, emit metrics.
- **Prometheus** — stores the monitor's emitted metrics as time series; **Alertmanager** wires thresholds → notifications (Slack/email/pager).
- **Custom jobs** — model-quality and bias monitors that need label joins run as K8s Jobs merging captured predictions with the (delayed) ground-truth store.
- Grafana dashboards visualize baseline-vs-current per monitor. This is the OSS translation of SageMaker Model Monitor / Azure ML monitoring signals.

### Closing the loop
Every confirmed drift alarm feeds two places—drift detection that only pages a human and stops there is half a loop:
- **Rollout controls** in `inference-rollout-strategist` — data or attribution drift halts expansion and pages by default. Automatic rollback is reserved for sustained quality, safety, bias, or performance harm that is correlated with candidate exposure against the incumbent over a documented confirmation window.
- **Eval dataset** in `llm-eval-harness` — the drifted inputs become new eval/regression cases so the next candidate is tested against exactly the distribution that broke the incumbent.

A confirmed concept-drift alarm additionally justifies a retraining trigger; a bias-drift alarm justifies re-running the release-gate fairness audit before any retrain, because retraining naively on drifted data can deepen the bias rather than fix it.

## Workflow
1. **Confirm safe capture**: approved purpose, classification, minimization/redaction, encrypted storage, identity-aware access, audit trail, retention/deletion, and restrictions on external judges.
2. **Classify the expected drift.** Which typology (data/concept/prediction/attribution) and temporal pattern matter for this research workload? This sizes windows and thresholds.
3. **Set baselines from upstream.** Training-set stats (data quality), eval floors (model quality), gate fairness results (bias), gate SHAP ranking (attribution) — reuse, don't recompute.
4. **Design each of the four monitors:** baseline, schedule (respecting label delay for model-quality/bias), threshold (conservative first), alert action.
5. **Wire the OSS stack.** Evidently CronJobs → Prometheus → Alertmanager → Grafana; custom label-join Jobs for the label-dependent monitors.
6. **Connect the loop.** Map each alarm to a rollback trigger and to an eval-dataset feedback action.
7. **Tune.** Start wide, tighten as normal variance is learned; suppress periodic-pattern false positives with window design.

## Output spec
Deliver a **Monitor Spec**: (1) safe data-capture config — purpose, classification, minimization/redaction, sampling, encrypted storage, access, audit, retention/deletion, and judge restrictions; (2) drift-typology assessment for this workload with the temporal patterns expected; (3) a per-monitor table — for each of the four: signal, baseline source, schedule (with label-delay offset where relevant), metric + threshold, alert action; (4) the OSS wiring diagram (Evidently CronJob → Prometheus → Alertmanager → Grafana, plus label-join Jobs); (5) the threshold-tuning plan (conservative start, tightening criteria); (6) the loop-closure map — each alarm → rollback trigger in `inference-rollout-strategist` and → eval-case feedback in `llm-eval-harness`. Note the Lambda managed-Kubernetes / OSS context throughout: Evidently + Prometheus + custom K8s jobs replace the managed SageMaker/Azure monitors; monitors run in-cluster on approved captured data.

## Siblings
`model-release-gate` (supplies the fairness and attribution baselines) · `inference-rollout-strategist` (consumes drift signals as rollback triggers) · `llm-eval-harness` (receives drifted inputs as new eval cases) · `inference-benchmark-runner` (performance metrics like TTFT/throughput can also be monitored for drift).
