---
name: feature-pipeline-failure-investigation
description: >
  Guides diagnosing and mitigating an overnight/scheduled feature pipeline
  failure that is causing predictions to run on stale or missing features,
  focused on fast triage and interim mitigation before the full root-cause
  fix lands. Use when the user says a "feature pipeline failed overnight",
  "predictions are running on stale features", a scheduled feature
  materialization job is failing or partially failed, or asks how to
  mitigate degraded predictions right now while the real fix is still in
  progress.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: mlops
  maturity: stable
---

# Feature Pipeline Failure Investigation

## Purpose

[training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md)
covers designing a resilient, idempotent training DAG; this skill covers
the specific overnight-failure moment: a scheduled feature computation/
materialization job broke, and right now predictions are being served on
data that is stale, partially missing, or null-heavy — quietly, because
the serving system has no idea the features underneath it went bad. The
operational job here is not writing the permanent fix (that may take
hours), it's answering three questions fast: how stale/broken is the data
right now, how much does that matter for this model, and what is the
safest thing to do with live traffic in the next fifteen minutes.

## When to use

- An overnight or scheduled feature computation/materialization job failed
  or partially failed, and predictions may currently be running on stale
  or missing features.
- On-call is paged for a feature-freshness SLA breach or a feature store's
  online-store lag alert.
- Deciding between pausing predictions, falling back to cached
  last-known-good feature values, or serving degraded predictions while a
  root-cause fix is prepared.
- Diagnosing why a feature view's online-store timestamps are older than
  expected, or why a job's row counts look wrong.
- A drift alert triage (see
  [model-drift-alert-triage](../model-drift-alert-triage/SKILL.md)) has
  pointed at an upstream pipeline problem rather than genuine model drift.

## Prerequisites & environment

- A feature store or materialization layer that exposes per-feature-view
  freshness metadata (last-successful-materialization timestamp, row
  counts) — Feast, Tecton, or a homegrown store with equivalent
  observability. Without this, "how stale is it right now" requires manual
  querying under time pressure.
- Access to the orchestrator's job run history and logs (Airflow, Kubeflow
  Pipelines, Argo Workflows, or equivalent) to see exactly which step
  failed and why.
- Visibility into upstream data source health — did the source table land
  on schedule, is an upstream ingestion job itself failing.
- Known feature importance/sensitivity for the model(s) consuming the
  affected feature view, so mitigation urgency can be triaged by impact
  rather than uniformly.
- An existing (or about-to-be-built) feature-freshness SLA and alert —
  if this failure mode wasn't monitored before, add it as part of the
  permanent fix.

## Step-by-step guidance

1. **Scope the blast radius first.** Identify exactly which feature
   view(s)/tables are affected, since what timestamp, and which models
   and serving endpoints consume them — a single feature view often feeds
   several models.
2. **Pull the orchestrator's run history for the failed job.** Determine
   whether the failure is a late-arriving upstream source, a code bug, a
   resource issue (OOM, disk, quota), or an infra outage — the mitigation
   differs depending on whether the underlying data is even available yet.
3. **Quantify current staleness per affected feature**, comparing the
   feature store's last-materialized timestamp against now and against
   that feature's specific staleness tolerance (a fraud-scoring feature
   tolerating minutes of staleness is very different from a weekly
   aggregate that tolerates a day):
   ```python
   from datetime import datetime, timezone

   def freshness_report(feature_view_metadata: dict, tolerance_minutes: int) -> dict:
       last_materialized = feature_view_metadata["last_success_ts"]
       age_minutes = (datetime.now(timezone.utc) - last_materialized).total_seconds() / 60
       return {
           "feature_view": feature_view_metadata["name"],
           "age_minutes": age_minutes,
           "within_tolerance": age_minutes <= tolerance_minutes,
           "row_count": feature_view_metadata.get("row_count"),
       }

   report = freshness_report(driver_stats_metadata, tolerance_minutes=180)
   # {"feature_view": "driver_stats", "age_minutes": 410, "within_tolerance": False, "row_count": 812004}
   ```
4. **Decide mitigation based on staleness severity and feature
   importance**, not a single blanket response:
   - Within tolerance: no action needed beyond monitoring the fix.
   - Beyond tolerance for a low-importance feature: flag predictions as
     degraded in logs/monitoring, but continue serving.
   - Beyond tolerance for a high-importance feature: serve last-known-good
     cached values with an explicit expiration, degrade to a simpler
     fallback (a rule-based heuristic or a simpler model less sensitive to
     the stale feature), or pause predictions for the affected segment —
     choose based on the cost of a wrong prediction versus no prediction
     for this specific use case.
   - Never silently continue serving indefinitely-staling features with no
     flag and no expiration on the mitigation.
5. **Communicate the degraded state** to downstream consumers and, if
   customer-facing impact is plausible, loop in incident response (see
   [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md)).
6. **Once the root cause is fixed, backfill the missed window
   idempotently** — rerun the materialization job for the exact gap,
   writing to a versioned output rather than mutating a shared location in
   place, so a retried backfill can't double-write or corrupt data (see
   [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md)
   for the idempotent-retry pattern this mirrors).
7. **Verify recovery** — confirm feature freshness is back within
   tolerance, and confirm any drift alerts that fired during the outage
   (see
   [model-drift-alert-triage](../model-drift-alert-triage/SKILL.md))
   were staleness-driven and resolve on their own once fresh data flows
   again, rather than being separately misdiagnosed as model drift.
8. **Close the loop**: add or tighten the feature-freshness SLA/alert if
   this failure mode wasn't caught in time, and remove any interim
   mitigation (cached fallback, paused segment) once the permanent fix is
   confirmed — an interim mitigation left in place indefinitely is its own
   form of technical debt.

## Best practices

- Treat feature freshness as an explicit SLA with its own alert, separate
  from model-quality monitoring — staleness and drift look similar from a
  distance but need different responses.
- Prefer explicitly flagging degraded predictions over silently serving
  stale data with no signal to consumers or monitoring.
- Make backfills idempotent by construction (write to a run-scoped or
  timestamp-partitioned output), so a retried backfill after a second
  failure can't corrupt or duplicate data.
- Rank features by importance to serving decisions ahead of time, so
  mitigation urgency during an incident is a quick lookup, not a debate.
- Time-box and ticket any interim mitigation (cached fallback, paused
  segment) with an explicit expiration, and confirm removal once the real
  fix lands.
- Periodically test the failure/fallback path deliberately (a controlled
  chaos-style drill) rather than discovering how the fallback behaves for
  the first time during a real overnight failure.

## Common pitfalls

- **Symptom:** Predictions silently serve day-old features for a
  real-time fraud-scoring model, and nobody notices until customer
  complaints arrive.
  **Fix:** Add an explicit feature-freshness SLA and alert per feature
  view, and default to flagging or falling back rather than silently
  continuing on stale data past the tolerance window.

- **Symptom:** On-call assumes a drift alert means the model itself
  degraded and pages the ML team for an emergency retrain, when the real
  cause is this feature pipeline silently failing overnight.
  **Fix:** Always check upstream feature pipeline freshness as an early
  step whenever a drift alert fires — see
  [model-drift-alert-triage](../model-drift-alert-triage/SKILL.md) — before
  concluding the model needs retraining or rollback.

- **Symptom:** After the root cause is fixed, the job simply resumes going
  forward, leaving a permanent gap in historical feature values for the
  window it missed — and a later retrain silently trains on data with that
  hole in it.
  **Fix:** Always backfill the missed window explicitly and idempotently
  once the root cause is fixed, rather than only resuming forward
  execution; verify the backfill closes the gap before declaring the
  incident resolved.

- **Symptom:** The fastest available "fix" is muting the freshness alert
  itself rather than addressing the actual feature computation problem,
  so the same failure recurs silently the following week.
  **Fix:** Never treat silencing the alert as the mitigation — the alert
  should stay active; only the underlying job or its resource allocation
  should change.

- **Symptom:** An emergency mitigation (serving cached last-known-good
  values) is put in place during the incident and is still running three
  months later because nobody tracked it as temporary.
  **Fix:** Ticket every interim mitigation with an explicit owner and
  expiration date at the time it's applied, and confirm its removal once
  the permanent fix is verified — an untracked "temporary" fallback tends
  to become permanent by default.

## Worked example

**Scenario:** The overnight Spark job that materializes the `driver_stats`
feature view for `fraud-scorer` fails at 02:14 UTC with an out-of-memory
error partway through, leaving the online feature store with data no
fresher than 22:00 UTC the previous day by the time on-call is paged at
07:00 UTC.

1. **Scope:** `driver_stats` is confirmed as the only affected feature
   view; it feeds `fraud-scorer` and one other model, `chargeback-risk`.
2. **Run history:** Airflow's task logs show the Spark executor was
   OOM-killed on a larger-than-usual daily partition — a resource issue,
   not a code bug, and the upstream source table landed on time.
3. **Freshness check:** the freshness report shows `driver_stats` is 9
   hours stale against a 3-hour tolerance for `fraud-scorer` — beyond
   tolerance, and `driver_stats` is a high-importance feature view for
   fraud scoring.
4. **Mitigation:** on-call switches `fraud-scorer`'s serving path to serve
   the last-known-good cached `driver_stats` snapshot from 22:00 UTC with
   predictions explicitly flagged as `feature_staleness: degraded` in logs
   and monitoring, rather than either serving silently or pausing scoring
   entirely — chosen because a slightly stale fraud signal is safer than
   no fraud scoring at all for this use case. The mitigation is ticketed
   with a same-day expiration.
5. **Fix and backfill:** engineering bumps the Spark executor's memory
   allocation and reruns the failed job, writing to a fresh
   run-ID-partitioned output; the backfill fills the exact missed window
   without touching the already-materialized earlier partitions.
6. **Verification:** freshness returns to within tolerance; the interim
   cached-fallback routing is removed; a drift alert that had briefly
   fired on `avg_rating_30d` during the stale window is confirmed
   staleness-driven (per
   [model-drift-alert-triage](../model-drift-alert-triage/SKILL.md)) and
   resolves on its own once fresh data flows again.
7. **Close the loop:** a freshness SLA/alert is added for `driver_stats`
   specifically, since this failure mode wasn't previously monitored.

## Cross-references

- [feature-store-design](../feature-store-design/SKILL.md) — the feature store/materialization design this investigation diagnoses failures within.
- [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md) — the idempotent-retry and DAG design patterns this skill's backfill step relies on.
- [data-and-model-lineage](../data-and-model-lineage/SKILL.md) — tracing exactly which models and downstream artifacts consume the affected feature view.
- [model-drift-alert-triage](../model-drift-alert-triage/SKILL.md) — the triage process that often routes here when a drift alert turns out to be staleness, not drift.
- [production-model-rollback-procedure](../production-model-rollback-procedure/SKILL.md) — the escalation path if the pipeline outage's downstream impact is severe enough to warrant rolling back the model itself rather than mitigating features.
- [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md) — incident structure for customer-facing impact from a feature pipeline outage.
