---
name: monitor-ml-drift
description: Monitors a production ML model for input data drift, prediction drift, and performance decay against delayed labels — using PSI/KS/Chi-square drift tests, train/serve skew checks, alert thresholds, and scheduled-or-drift-triggered retraining with a champion/challenger loop — so a silently degrading model is caught before it costs.
when_to_use: A deployed model needs ongoing statistical health monitoring or has quietly degraded. Distinct from serve-deploy-ml-model (rollout/canary/autoscale), train-evaluate-ml-model (initial build + offline metrics), observability-instrument (service latency/error RED metrics), and validate-data-quality (rule assertions, not distribution shift).
---

## When to Use

Reach for this skill when the concern is **the model's statistical health in production**, not whether the service is up:

- "Accuracy looked fine at launch but the model feels worse now — is it drifting?"
- "Our feature distributions shifted (new user segment, seasonality, upstream schema change) — did the model degrade?"
- "Set up drift + performance monitoring and an alert when a retrain is warranted"
- "Labels arrive 2 weeks late — how do I track real accuracy/AUC over time?"
- "Detect train/serve skew — the model scores differently offline vs online on the same row"
- "Wire a champion/challenger so a candidate retrain only ships if it beats prod"

NOT this skill:
- Shipping/rolling out the model artifact, canary, autoscaling → serve-deploy-ml-model
- The original training run, offline eval, hyperparameter search, test-set metrics → train-evaluate-ml-model
- Service-level latency/error-rate/RED metrics, traces, dashboards, p99 alerts → observability-instrument
- Rule assertions on the data pipeline (not-null, unique, freshness, range) → validate-data-quality (drift is *distributional*; a column can pass every range rule and still have shifted its whole distribution)

## Steps

1. **Log every prediction as an immutable event — no logging = no monitoring.** Per request, write one row: `prediction_id`, `ts`, `model_version`, the **raw feature vector actually scored** (post-transform, exactly what the model saw), the output (`pred_proba` + `pred_label`), and a `label_join_key`. Land it in a columnar store (Parquet on S3, BigQuery, Delta). Labels arrive later out-of-band → write them to a separate table keyed by `label_join_key` and **left-join on arrival**; never block scoring on a label. Snapshot the **training reference** (a held-out slice of the training data + its predictions) once and pin it — every drift test compares live vs this fixed reference.

2. **Pick the drift test per feature type — do not PSI everything.**

   | Signal | Test | Fires when | Default threshold |
   |---|---|---|---|
   | Numeric / continuous feature | **PSI** (population stability index) | Binned distribution shifted vs reference | PSI > 0.2 = significant; 0.1–0.2 = watch |
   | Numeric, distribution shape | **KS** (Kolmogorov–Smirnov) 2-sample | Max CDF gap large | p < 0.05 |
   | Categorical feature | **Chi-square** / PSI on category freqs | Category mix shifted, new/unseen level | p < 0.05 / PSI > 0.2 |
   | Prediction output (proba) | **PSI / KS** on `pred_proba` | Output distribution drifts | PSI > 0.2 |
   | Multivariate / overall | **Domain classifier** (ref vs live, AUC) | Classifier separates ref from live | AUC > 0.7 |

   Compute over a **rolling window** (default: last 7 days or 10k preds, whichever larger) vs the pinned reference. Use a fixed reference for stable populations; switch to a **trailing-window reference** only if the population legitimately evolves (and document that you've given up detecting slow drift). Apply **Bonferroni/BH correction** across features — with 200 features at p<0.05 you get ~10 false alarms per run by chance.

3. **Separate the three drift types — they mean different things and trigger different actions.**
   - **Data (input) drift** — features moved. Model may still be fine; this is an *early warning*, not proof of decay. Page only if widespread.
   - **Prediction drift** — output distribution moved without a known input cause → upstream feature pipeline broke, or real population shift. Higher signal than single-feature input drift.
   - **Concept drift / performance decay** — the input→output relationship changed. **Only measurable once labels land.** This is the one that actually justifies a retrain. Track the real metric (AUC/F1/MAE — whatever you optimized) per cohort window vs a **baseline window** (e.g. first 2 weeks post-deploy, or last known-good).

4. **Run it with a library — don't hand-roll the stats.** Evidently for reports + tests, whylogs for lightweight profile logging at scale, NannyML for *estimating* performance **before** labels arrive (CBPE/DLE). Pin `evidently==0.4.*` and use its `Report` / `metric_preset` API:

   ```python
   from evidently.report import Report
   from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
   from evidently import ColumnMapping

   cm = ColumnMapping(prediction="pred_proba")
   report = Report(metrics=[
       DataDriftPreset(stattest="psi", stattest_threshold=0.2),  # per-feature input drift
       TargetDriftPreset(),                                       # prediction-column drift
   ])
   report.run(reference_data=ref_df, current_data=live_df, column_mapping=cm)
   res = report.as_dict()

   drift = res["metrics"][0]["result"]                # DataDriftPreset summary
   if drift["share_of_drifted_columns"] > 0.3:        # >30% of features drifted → alert
       fire_alert("data_drift", detail=drift)
   ```

   For pre-label performance estimation when labels lag:
   ```python
   import nannyml as nml
   est = nml.CBPE(problem_type="classification_binary", y_pred="pred_label",
                  y_pred_proba="pred_proba", y_true="label",
                  metrics=["roc_auc"], chunk_size=5000)
   est.fit(reference_df)                 # reference must include matured labels
   estimated = est.estimate(live_df)     # estimated AUC + confidence band, no live labels needed
   ```

5. **Detect train/serve skew explicitly — it's a silent killer.** Re-score a sample of logged production feature vectors through the **offline** model and assert `abs(online_proba − offline_proba) < 1e-4`. Mismatch = a transform diverged between training and serving (different encoder fit, a default-fill applied online only, version skew in a preprocessing lib). Also compare **training-time** feature distributions vs **serving-time** for the same feature: skew shows up as a step change at deploy, not a gradual drift. Run this nightly on a sample.

6. **Set thresholds and a retraining trigger — opinionated defaults, then tune to your false-alarm budget.**
   - **Trigger retrain** when *any* holds: estimated/actual primary metric drops > **5% relative** below baseline for ≥2 consecutive windows; OR prediction-drift PSI > 0.2 sustained; OR > 30% of top-importance features drifted. One noisy window ≠ retrain — require **persistence** (2+ windows) to kill flapping.
   - **Schedule** a baseline retrain regardless (weekly/monthly) so you never rely solely on drift detection catching it.
   - On trigger, retrain a **challenger** and gate promotion through a champion/challenger comparison (step 7) — never auto-promote on a drift signal alone; drift can be benign.

7. **Champion/challenger before promotion.** Train challenger on fresh data, evaluate **both** on the same recent labeled window (and ideally a shadow/online split). Promote only if challenger beats champion on the primary metric by a margin **beyond noise** (bootstrap CI on the metric, or a paired test) — not a single point estimate. Log the decision + metrics to a model registry. Hand the actual rollout (canary, traffic shift, rollback) to **serve-deploy-ml-model**; this skill decides *whether*, that skill does *how*.

8. **Alert routing, not just detection.** Page on **performance decay** and **prediction drift** (high signal). Send **input drift** to a dashboard/digest, not a pager — single-feature input drift is frequent and usually benign; paging on it trains everyone to ignore the channel. Every alert carries: which signal, which features/metric, the value vs threshold, the window, and a link to the drift report.

## Common Errors

- **Logging transformed-then-re-derived features instead of what the model scored.** You then compare a reconstruction, not reality, and miss real skew. Log the exact post-transform vector at inference time.
- **Reference set = the whole training data including the part the model trained on.** Leaks optimism. Use a **held-out** slice as reference.
- **PSI/KS run with no multiple-comparison correction.** 200 features × p<0.05 ≈ 10 false "drifts" every run → alert fatigue. Apply Bonferroni/BH and a `share_of_drifted_columns` gate, don't alert per feature.
- **Treating any data drift as "model is broken."** Features can shift while accuracy holds. Only **performance decay** (or prediction drift with a cause) justifies a retrain; input drift is a watch signal.
- **Computing "live accuracy" the moment predictions are made.** Labels are delayed — that number is empty until labels land. Use NannyML CBPE/DLE to *estimate* performance pre-label, and report actual metric only over windows whose labels have matured.
- **Joining labels to predictions on timestamp.** Late/duplicate/reordered labels corrupt the join. Join on a stable `label_join_key`, and bucket by **prediction** time, not label-arrival time.
- **Comparing windows of wildly different size.** PSI/KS are sensitive to n; a 200-row window vs a 50k reference flags noise as drift. Fix a minimum window size and equal-ish bins.
- **Fixed reference forever on a legitimately evolving population.** Everything reads as drift and the signal dies. Either accept slow drift goes undetected with a trailing reference, or re-baseline deliberately on each retrain — and write down which.
- **Auto-retrain + auto-promote on a single drift spike.** Promotes a worse model on a benign blip or a data outage. Require persistence (2+ windows) and a champion/challenger win beyond noise.
- **No train/serve skew check.** The most common production regression — an encoder/imputer that differs online — is invisible to distribution drift. Re-score logged rows offline and assert equality.

## Verify

1. **Inject a known input shift:** take a held-out reference, build a `current` where one numeric feature is multiplied (e.g. ×1.5) or a category's frequency is swapped → the per-feature drift test (PSI/KS) for *that* feature fires and the others stay green. Proves sensitivity *and* specificity.
2. **Inject prediction drift:** shift `pred_proba` for the current window → prediction-drift alert fires while input features are unchanged. Proves the output monitor is independent.
3. **Replay a known-degraded period:** feed a window whose labels you know are bad (mislabel a slice or use a historically-bad date range) → the performance tracker shows the metric dropping > 5% below baseline and the **retrain trigger** fires after the 2nd consecutive bad window (not the 1st).
4. **Negative control:** feed `current = reference` (resampled) → **no** alert fires. If a same-distribution sample trips an alert, your thresholds/correction are too tight.
5. **Skew check:** re-score a sample of logged prod vectors offline → `max|online − offline| < 1e-4`. Then deliberately break one transform and confirm the skew check catches it.
6. **Delayed-label join:** insert labels out of order / late → actual-metric windows recompute correctly keyed by prediction time, and pre-label estimated metric (CBPE) tracks the eventual actual within its confidence band.
7. **Champion/challenger gate:** feed a challenger that's worse on the recent window → promotion is **rejected**; feed one that's better beyond the CI → promotion is approved and logged to the registry.

Done = an injected input shift fires only the right feature's drift alert (negative control stays silent), prediction drift is detected independently, the performance tracker reflects the known-degraded period and trips the retrain trigger after sustained (not single-window) decay, train/serve skew is caught, and champion/challenger blocks a worse model from promoting.
