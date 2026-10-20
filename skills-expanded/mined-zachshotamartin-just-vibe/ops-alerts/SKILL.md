---
name: ops-alerts
description: "Design actionable alerts with ownership and response guidance. Use to design response-worthy alerts; ops-observability supplies reliable signals."
---

# ops-alerts

Design actionable alerts with ownership and response guidance.

## Choose this workflow

Use to design response-worthy alerts; ops-observability supplies reliable signals.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Operations methods](../../references/packs/operations.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan by default; apply to write requested alert-rule files and rule tests without enabling notification routes. Requires service objectives, telemetry, response ownership, notification destination, and noise tolerance.

**Pack prerequisites:** Exact service/environment, time window, revision/configuration identity, authorized logs/metrics, and operational constraints. Prefer observation before intervention; live restarts, traffic changes, restores, and notifications require the requested target/action. Redact sensitive telemetry.

- **Infer from evidence:** Read service/environment, time window, revision, available telemetry and existing incident or recovery procedure.
- **Reasonable default:** Start from supplied logs and read-only observation; rank hypotheses without presenting an unexecuted intervention as recovery.
- **Ask only when needed:** Resolve the precise target and missing authority before restart, restore, notification or traffic changes; continue evidence analysis while waiting.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Actionable alert rules and response guidance; enabling/sending notifications requires an explicit request.

Inspect/plan: design alerts; save requested artifacts only. Apply: write only the requested alert-rule files and rule tests. Notification destinations, enablement and test pages stay out of scope unless explicitly requested.

## Execute

1. Tie each alert to impact and a responder action.
2. Define evaluation and recovery windows, thresholds, missing-data behavior and noise suppression.
3. Test with historical or synthetic events.

## Technical method

- **Inspect:** Establish user-impact signal, window, baseline, missing-data semantics and response owner.
- **Method:** Define actionable thresholds, recovery and deduplication; distinguish page-worthy sustained failure from diagnostic events.
- **Avoid misdiagnosis:** A threshold without a responder action creates noise; no samples must not silently become healthy.
- **Check the result:** Replay healthy, failing, transient and missing-data sequences, checking firing, recovery and notification routing only within requested scope.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Operations worked example](../../references/examples/operations.md).


## Decision branches

- **When signal quality cannot distinguish failure from missing telemetry:** Add an explicit missing-data state instead of silently treating absence as healthy.
- **When a service level objective exists:** Derive page and ticket rules from error-budget burn rate over paired long and short windows (for a 30-day SLO: page at 14.4 times over 1 hour confirmed over 5 minutes, and 6 times over 6 hours confirmed over 30 minutes; ticket at 1 times over 3 days confirmed over 6 hours). Without an SLO, state the rationale for each threshold.

## Deliver and verify

- Alert definitions as a contract with rationale, trigger/recovery examples, owner/destination assumptions, runbook links and false-positive/missed-event checks.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Sustained harmful failure triggers; expected brief transients do not page indiscriminately.

## Stop and recover

- Do not invent owners or send test pages implicitly. Missing signal quality is a prerequisite, not something thresholds can hide.

## Example requests

- **Normal (plan):** Design actionable error-rate alerts with recovery behavior; do not enable notifications.
- **Edge (plan):** Design alerts that ignore brief spikes but detect sustained customer failures.
- **Blocked (inspect):** Draft alerts without sending pages or inventing response ownership.
- **Additional (apply):** Add a Prometheus alert rule for queue age to monitoring/alerts.yml with rule tests, leaving notifications disabled.
