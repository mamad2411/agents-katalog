---
name: production-model-rollback-procedure
description: >
  Guides the incident-time procedure for rolling back a production model to
  a previous version after a bad deploy, with feature-schema compatibility
  verification against the rollback target as a required, non-skippable
  step. Use when the user says a new model deploy is "causing errors" or
  "bad predictions" and needs to roll back now, asks "how do I roll back a
  model version", needs to confirm an older model version still matches the
  current feature pipeline's schema before reverting to it, or is writing a
  tested rollback runbook for an on-call rotation.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: mlops
  maturity: stable
---

# Production Model Rollback Procedure

## Purpose

[model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md)
covers *designing* a registry promotion scheme where rollback is possible
in principle; this skill covers *executing* that rollback correctly under
incident pressure, when a bad deploy is actively hurting users and someone
needs to act in minutes, not review a design doc. The single most
dangerous shortcut at this moment is assuming "the previous version" is
automatically safe to restore: features evolve underneath a model version's
shelf life, and a model that served correctly a month ago can be
fed a feature schema today that has since gained, lost, or renamed columns
it depends on. A naive rollback can silently trade one bad model for a
model that errors or produces garbage on a schema it no longer recognizes,
turning a bad-deploy incident into a longer one. This skill makes the
feature-schema compatibility check a required gate in the rollback
procedure itself, not an optional nicety.

## When to use

- A newly deployed/promoted model version is causing elevated errors, bad
  predictions, or an active incident, and needs to be rolled back
  immediately.
- Executing a rollback runbook step by step during an incident, as opposed
  to designing the registry's promotion/rollback scheme in the abstract.
- Deciding whether it is actually safe to revert to a specific previous
  model version given how the feature pipeline/feature store has changed
  since that version last served production traffic.
- Validating a candidate rollback target's input schema against the
  current live feature output before flipping traffic back.
- Confirming, after a rollback, that the incident is genuinely mitigated
  and documenting the rollback for the postmortem.

## Prerequisites & environment

- A model registry where the previous production version was **archived,
  not deleted**, on promotion (see
  [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md))
  so it is retrievable in minutes, not hours.
- Serving infrastructure capable of a fast traffic cutover — canary/
  blue-green routing already configured per
  [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md), not a
  from-scratch redeploy.
- Recorded feature schema/feature-view version metadata for both the
  currently-serving (bad) version and every rollback candidate — if this
  wasn't captured at packaging time, this procedure is materially slower
  and riskier.
- Read access to the feature store's current schema (feature names,
  dtypes, categorical value sets) to diff against a candidate's expected
  input contract.
- Monitoring already wired to confirm whether the rollback resolves the
  issue (see
  [model-monitoring-and-drift-detection](../model-monitoring-and-drift-detection/SKILL.md)).
- An established incident command structure so the rollback decision is
  authorized and communicated, not a unilateral action taken in the dark
  (see
  [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md)).

## Step-by-step guidance

1. **Confirm the bad deploy is actually the cause.** Correlate the
   incident's start time precisely against the model's deployment/
   promotion timestamp before committing to a rollback — a coincident but
   unrelated cause (e.g. an infra outage, an upstream feature pipeline
   failure per
   [feature-pipeline-failure-investigation](../feature-pipeline-failure-investigation/SKILL.md))
   would make a rollback ineffective and waste the response window.
2. **Identify the actual rollback target from the registry**, not just
   "one version back" by assumption. Check version history/annotations —
   the immediately prior version may itself have been a rollback for a
   different bug, or may never have fully soaked in production. Find the
   most recent version with a *confirmed* healthy production track record.
3. **Required gate: diff the rollback target's expected feature schema
   against the feature pipeline's current live output.** Do not skip this
   step under time pressure — it is the check most likely to be skipped,
   and skipping it is exactly what turns a rollback into a second
   incident.
   ```python
   import json

   def schema_diff(old_version_schema: dict, current_feature_output_schema: dict) -> dict:
       old_fields = old_version_schema["features"]          # {name: dtype}
       current_fields = current_feature_output_schema["features"]
       missing = {k: v for k, v in old_fields.items() if k not in current_fields}
       type_changed = {
           k: (v, current_fields[k])
           for k, v in old_fields.items()
           if k in current_fields and current_fields[k] != v
       }
       new_unused = {k: v for k, v in current_fields.items() if k not in old_fields}
       return {"missing": missing, "type_changed": type_changed, "new_unused": new_unused}

   result = schema_diff(
       old_version_schema=json.load(open("registry/fraud-scorer/v13/input_schema.json")),
       current_feature_output_schema=json.load(open("feature_store/driver_stats/current_schema.json")),
   )
   if result["missing"] or result["type_changed"]:
       raise SystemExit("BLOCKED: rollback target's schema is incompatible with current feature output")
   ```
4. **If a mismatch is found, do not force the rollback.** Treat this as a
   blocked rollback requiring one of: an adapter/compatibility shim that
   maps the current feature schema to what the old version expects, a
   fallback further back to an even older version whose schema *is*
   compatible, or — if nothing compatible exists — a safe static/heuristic
   fallback response for the affected traffic while a proper fix is
   prepared, rather than serving an incompatible model.
5. **Execute the rollback through the registry's promotion path**, not a
   raw file/container swap — e.g. re-promoting the archived version back
   to `Production` (`mlflow models transition-stage ... --stage Production`
   or the equivalent SageMaker/Vertex AI action), so the audit trail and
   lineage stay intact.
6. **Cut traffic back progressively if the incident's severity allows it**
   — canary the rollback target at a smaller percentage first, per
   [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md),
   unless the severity demands an immediate 100% cutover.
7. **Verify via monitoring that the rollback resolved the issue** — error
   rate, latency, and prediction-quality proxies return to the
   pre-incident baseline — before declaring the incident mitigated.
8. **Keep the bad version archived, not deleted**, for post-incident
   forensic analysis; it is still needed to understand exactly what went
   wrong.
9. **Log the rollback event** — timestamp, decision-maker, schema-check
   outcome, and rollback target version — into both the incident record
   and the model's lineage/registry metadata so the audit trail is
   complete.

## Best practices

- Treat the feature-schema compatibility check as a mandatory gate in the
  rollback procedure, never an optional step skipped "because it's an
  emergency" — an incompatible rollback often creates a second incident on
  top of the first.
- Always execute rollback through the registry's stage-transition
  mechanism, never a raw file path swap or manual container edit that
  bypasses the audit trail.
- Game-day the rollback procedure periodically (a scheduled drill) rather
  than trusting it works because it's documented — an untested runbook
  frequently has a stale command or a missing permission that only
  surfaces during a real incident.
- Keep at least the last two production versions (N-1, N-2) warm/available
  in the registry with their input schemas recorded, not just the single
  immediately-prior version.
- Automate the schema-diff script so it runs in seconds under incident
  pressure, rather than requiring someone to manually compare JSON files
  by eye at 3 a.m.
- Route the rollback decision and its outcome through the incident's
  Communications/Scribe roles (see
  [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md))
  so it's part of the recorded timeline, not a silent action.

## Common pitfalls

- **Symptom:** The rollback "succeeds" — the previous model version is
  confirmed deployed — but predictions immediately start erroring or
  silently degrade, because the feature store now returns a schema the
  old version's preprocessing pipeline doesn't recognize (a column it
  expects was renamed or removed, or a categorical feature gained new
  values it was never trained on).
  **Warning:** This is the core risky action this skill exists to prevent.
  Never roll back to a previous model version without first diffing its
  expected input schema against the *current* feature pipeline/feature
  store output; if incompatible, treat the rollback as blocked and use a
  compatibility shim, an older compatible version, or a safe fallback
  instead of forcing it.

- **Symptom:** Someone rolls back by pointing the serving configuration at
  an old container image or file path directly, bypassing the model
  registry entirely, so there's no clean record of what changed or when.
  **Fix:** Always execute rollback as a registry stage transition (or its
  cloud-native equivalent), never a manual infrastructure edit — this is
  what keeps the rollback auditable and reversible.

- **Symptom:** The team assumes "the previous version" (N-1) is
  automatically safe, but that version had itself been rolled back once
  before for an unrelated issue and never fully re-validated in
  production.
  **Fix:** Check the registry's version history/annotations for a truly
  last-known-good version, rather than mechanically reverting one version
  back without checking its own track record.

- **Symptom:** The rollback target is cut over to 100% of traffic
  instantly, and a second, separate incident starts minutes later because
  the rollback target had its own latent issue nobody caught.
  **Fix:** Canary the rollback target at a smaller traffic percentage
  first whenever incident severity allows the extra minutes, rather than
  treating instant full cutover as always the safest option.

## Worked example

**Scenario:** `fraud-scorer` version 14 is promoted to production and
within 20 minutes the false-positive rate spikes sharply, blocking
legitimate transactions.

1. On-call confirms the spike started within two minutes of version 14's
   promotion timestamp — the deploy is the likely cause.
2. Registry history shows version 13 was in production for three weeks
   with a clean track record before version 14 replaced it — chosen as
   the rollback candidate.
3. **Required schema check:** the schema diff script compares version 13's
   recorded input schema against the feature store's *current* output for
   the `driver_stats` feature view. It finds that `driver_stats` was
   upgraded from `v3` to `v4` between version 13's retirement and now, and
   `v4` renamed `avg_txn_amount_30d` to `avg_txn_amount_rolling_30d` —
   version 13's preprocessing code still looks for the old name and would
   silently treat it as missing/null.
4. Because of the mismatch, the rollback is **not** executed naively.
   The team applies a lightweight compatibility shim in the serving layer
   that maps `avg_txn_amount_rolling_30d` back to the
   `avg_txn_amount_30d` name version 13 expects, then re-runs the schema
   diff to confirm compatibility.
5. Version 13 (with the shim) is re-promoted to `Production` via
   `mlflow models transition-stage`, canaried at 25% of traffic for ten
   minutes, then cut over to 100% once the false-positive rate returns to
   baseline.
6. Version 14 remains archived (not deleted) for root-cause analysis; the
   rollback, the schema mismatch found, and the shim applied are all
   logged in the incident record and handed to the postmortem process.

## Cross-references

- [model-packaging-and-versioning](../model-packaging-and-versioning/SKILL.md) — the registry promotion/archival design this rollback procedure executes against.
- [model-serving-and-scaling](../model-serving-and-scaling/SKILL.md) — canary/blue-green traffic-cutover mechanics used during rollback.
- [model-drift-alert-triage](../model-drift-alert-triage/SKILL.md) — the triage process that often precedes a decision to roll back.
- [feature-pipeline-failure-investigation](../feature-pipeline-failure-investigation/SKILL.md) — ruling out a feature pipeline failure as the real cause before rolling back the model itself.
- [data-and-model-lineage](../data-and-model-lineage/SKILL.md) — resolving exactly which feature view version a rollback candidate's schema was recorded against.
- [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md) — the incident command structure this procedure runs inside.
- [blue-green-canary-deployments](../../../devops/skills/blue-green-canary-deployments/SKILL.md) — general rollback/traffic-shift mechanics this procedure specializes for model deploys.
