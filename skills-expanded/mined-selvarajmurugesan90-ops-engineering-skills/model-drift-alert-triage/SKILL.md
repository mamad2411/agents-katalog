---
name: model-drift-alert-triage
description: >
  Guides the fast, time-boxed triage of a drift-monitoring alert that has
  already fired: deciding whether it is genuine data/concept drift, a
  monitoring code bug, a stale/broken upstream feature pipeline, or normal
  seasonality — before deciding whether to retrain, roll back, silence, or
  escalate. Use when the user says a drift alert "just fired", asks "is this
  real drift or a false positive", needs a triage runbook for an on-call
  PSI/KS/KL threshold breach, or is deciding what to do in the first 15-30
  minutes after being paged for a model-quality alert.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: mlops
  maturity: stable
---

# Model Drift Alert Triage

## Purpose

[model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md)
covers how to *build* drift monitoring; this skill covers the five-alarm
moment after that monitoring already paged someone. A fired drift alert is
not self-explanatory — the same PSI-over-threshold signal can mean the world
genuinely changed under the model, a marketing campaign shifted a seasonal
feature for a week, a feature pipeline silently broke and is now feeding
stale or null-heavy data, or the monitoring job itself has a bug. Each of
those has a completely different correct response (retrain, ignore and
tune, fix an upstream pipeline, or fix monitoring code), and picking the
wrong one wastes an on-call engineer's time at best and triggers a bad
retrain or an unnecessary rollback at worst. This skill is a decision tree
for reaching the right classification inside a time-boxed window, not a
lecture on drift statistics.

## When to use

- A drift/data-quality alert (PSI, KS, KL divergence, chi-squared, or a
  prediction-distribution check) just fired and someone needs to decide
  within minutes whether it's actionable.
- On-call has been paged for a threshold breach and needs a checklist
  before waking up the wider ML team or declaring an incident.
- Deciding whether a drift alert is genuine distribution shift versus a
  monitoring pipeline bug (schema change, duplicated join rows, a timezone
  bug in timestamp handling, a sampling bias in what got logged).
- Deciding the next action: silence/tune the alert, hand off to
  [feature-pipeline-failure-investigation](../feature-pipeline-failure-investigation/SKILL.md),
  kick off a retrain via
  [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md),
  or roll back via
  [production-model-rollback-procedure](../production-model-rollback-procedure/SKILL.md).
- Writing or refining a runbook for a drift-monitoring on-call rotation.

## Prerequisites & environment

- Access to the monitoring backend's per-feature *history*, not just the
  single alert value — a dashboard that only shows "PSI = 0.31 today" with
  no trend line makes triage far slower.
- Access to the raw logged inference inputs/outputs (with timestamps and
  model version tag), not only pre-aggregated statistics, so a suspicious
  number can be re-derived independently.
- Read access to the model registry and lineage metadata to identify
  exactly which model version, training data snapshot, and feature view are
  implicated (see
  [data-and-model-lineage](../data-and-model-lineage/SKILL.md)).
- Read access to the upstream feature pipeline's/orchestrator's recent run
  history (success/failure, row counts, last-materialized timestamp) — a
  large share of "drift" alerts are actually pipeline staleness.
  See [feature-pipeline-failure-investigation](../feature-pipeline-failure-investigation/SKILL.md).
  for the freshness-check mechanics.
- A defined escalation path and severity framework already in place for
  when triage concludes the alert is genuine and urgent (see
  [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md)).
- A time box for the triage itself (15-30 minutes is typical) so an
  inconclusive investigation escalates instead of running indefinitely.

## Step-by-step guidance

1. **Sanity-check the alert is real before doing anything else.** Re-derive
   the flagged metric independently from a fresh pull of the same
   underlying data, rather than trusting the dashboard number at face
   value — a bug in the monitoring computation itself is indistinguishable
   from real drift until checked:
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

   # Pull raw values directly rather than trusting the dashboard aggregate
   psi_recheck = population_stability_index(reference_values, current_window_values)
   sample_size_ok = len(current_window_values) >= 500  # flag if the alert fired on a tiny sample
   ```
2. **Check the alert's breadth.** Is it a single feature or many at once?
   A single model version's consumers or every model that reads the same
   feature view? A single geography/segment or the aggregate? A sudden
   shift across *everything* fed by one feature view points at an upstream
   pipeline problem, not organic behavioral drift in users.
3. **Check freshness of the underlying feature pipeline first**, before
   assuming the signal is behavioral. Query the feature store/orchestrator
   for the last successful materialization timestamp per affected feature.
   A PSI spike that lines up exactly with a failed or partial overnight job
   is staleness, not drift — hand off immediately to
   [feature-pipeline-failure-investigation](../feature-pipeline-failure-investigation/SKILL.md)
   rather than treating it as a model problem.
4. **Check timing correlation with known events**: a recent model
   deployment/promotion, a recent feature pipeline schema change, a
   marketing campaign, a known seasonal calendar event (holidays, fiscal
   quarter-end), or an unrelated platform migration that changed upstream
   event semantics.
5. **Classify input drift vs. output drift vs. quality drift** — they
   point at different causes:
   - Input drift with stable output drift: possibly a robust model
     absorbing the shift, or a delayed effect not yet visible.
   - Output drift with stable input drift: a code/config change in the
     model or its post-processing, not the world changing.
   - Both together, persisting across multiple monitoring windows: the
     strongest signal of genuine drift requiring action.
6. **Require persistence, not a single data point**, before treating the
   alert as actionable — a threshold breach that reverts within a day is
   frequently a holiday, a traffic spike, or noise on a small sample.
7. **Classify the alert into one of four buckets** and route accordingly:
   - **False positive / noise** → tune the threshold or add
     seasonal adjustment; log the resolution.
   - **Monitoring bug** → fix the monitoring computation; do not touch the
     model or pipeline.
   - **Upstream pipeline problem** → hand off to
     [feature-pipeline-failure-investigation](../feature-pipeline-failure-investigation/SKILL.md);
     the model itself is very likely fine.
   - **Genuine drift** → decide urgency: moderate degradation with time to
     spare schedules a retrain via
     [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md);
     active, severe harm to users triggers
     [production-model-rollback-procedure](../production-model-rollback-procedure/SKILL.md)
     to the last known-good version while a proper retrain is prepared.
8. **Time-box the investigation.** If classification is still unclear after
   the agreed window, escalate to a wider incident per
   [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md)
   rather than continuing to investigate solo indefinitely.
9. **Log the resolution back into the monitoring system** — false
   positive, monitoring bug, pipeline issue, or genuine drift — so
   thresholds and playbooks improve over time instead of staying static
   after every alert.

## Best practices

- Never classify an alert as "real drift" without first checking feature
  pipeline freshness — staleness masquerading as drift is one of the most
  common false alarms in practice.
- Keep a running log of past alert resolutions per feature so recurring
  false positives (seasonal features, known noisy segments) get their
  thresholds tuned instead of re-triaged from scratch every time.
- Prefer independently re-deriving a suspicious metric over trusting a
  single dashboard number — dashboards can have their own bugs.
- Segment the triage by slice (region, device, customer tier) whenever the
  aggregate signal is ambiguous; drift often hides in or is diluted by a
  subpopulation.
- Treat "retrain" and "roll back" as distinct decisions with different
  urgency profiles — a moderate, slow-building drift usually wants a
  retrain; a sudden, severe quality drop wants an immediate rollback while
  retraining happens in parallel.
- Make the four-way classification (false positive / monitoring bug /
  pipeline issue / genuine drift) an explicit, written-down decision in the
  incident record, not an implicit call someone made in their head.

## Common pitfalls

- **Symptom:** On-call immediately assumes "real drift" and pages the ML
  team for an emergency retrain based on a single day's PSI spike that
  quietly reverts to baseline the next day.
  **Fix:** Require persistence across more than one monitoring window
  before treating a threshold breach as actionable, per
  [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md);
  a single-day spike on a seasonal or campaign-affected feature is common
  and expected.

- **Symptom:** The team spends over an hour debating whether a spike is
  "real" because the monitoring dashboard only shows aggregate statistics,
  and it turns out a single newly-launched region is driving the whole
  signal.
  **Fix:** Always drill into slice-level breakdowns (region, device,
  customer tier) as a standard early triage step, not a last resort after
  aggregate analysis stalls.

- **Symptom:** A drift alert triggers a full retrain-and-promote cycle, and
  the retrained model is worse, because the "drift" was actually a feature
  pipeline job that had been silently emitting stale or null-heavy values
  for three days — the retrain learned from the same bad data.
  **Fix:** Always check upstream feature pipeline health and freshness
  before concluding drift is genuine; route suspected pipeline issues to
  [feature-pipeline-failure-investigation](../feature-pipeline-failure-investigation/SKILL.md)
  first, and never let an automated drift-triggered retrain skip the
  gated promotion checks in
  [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md).

- **Symptom:** Triage concludes the alert is genuine and severe, and
  on-call immediately rolls back to the previous model version without
  checking whether that older version's expected feature schema still
  matches what the feature pipeline emits today.
  **Warning:** Rolling back a production model without verifying
  feature-schema compatibility is a risky action in its own right — hand
  off to
  [production-model-rollback-procedure](../production-model-rollback-procedure/SKILL.md),
  which makes that compatibility check a required step, rather than
  executing an ad hoc rollback under time pressure.

## Worked example

**Scenario:** A PSI alert fires at 03:14 UTC on `days_since_last_login`, a
feature feeding the `churn-predictor-v3` model, breaching the 0.25
threshold at 0.29.

1. **Sanity check:** On-call re-derives PSI from a fresh pull of the last
   24 hours of raw feature values against the frozen training-time
   baseline — confirms 0.29, sample size 40,000 rows, not a monitoring bug
   or tiny-sample artifact.
2. **Breadth check:** Only `days_since_last_login` is flagged; other
   monitored features (`support_tickets_30d`, `plan_tier`) are stable.
   Points at something specific to this one feature's pipeline, not a
   broad behavioral shift.
3. **Freshness check:** Querying the feature store shows
   `days_since_last_login` was last materialized correctly, but its
   *source* login-event table's timestamp semantics changed two weeks
   earlier during an unrelated platform migration — this is an upstream
   pipeline change, not user behavior changing.
4. **Classification:** Routed as an **upstream pipeline problem**, handed
   to [feature-pipeline-failure-investigation](../feature-pipeline-failure-investigation/SKILL.md)
   rather than triggering a retrain or rollback.
5. **Resolution:** The upstream timestamp bug is fixed; PSI returns to
   baseline over the next three days. On-call logs the resolution as
   "pipeline bug, not model drift" back into the monitoring system for
   future reference.
6. Four weeks later, a separate alert on `support_tickets_30d` persists
   across multiple windows *and* correlates with a real recall drop once
   delayed labels arrive — this time correctly classified as genuine
   concept drift and routed to a scheduled retrain via
   [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md).

## Cross-references

- [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md) — how the monitoring and thresholds this skill triages were built.
- [feature-pipeline-failure-investigation](../feature-pipeline-failure-investigation/SKILL.md) — the destination when triage points at a broken/stale upstream pipeline rather than genuine drift.
- [production-model-rollback-procedure](../production-model-rollback-procedure/SKILL.md) — the destination when triage concludes genuine, severe drift requiring an immediate rollback.
- [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md) — the destination when triage concludes genuine drift warranting a scheduled retrain.
- [data-and-model-lineage](../data-and-model-lineage/SKILL.md) — tracing an implicated feature/model back to its source data during triage.
- [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md) — escalation path when triage is inconclusive within its time box.
