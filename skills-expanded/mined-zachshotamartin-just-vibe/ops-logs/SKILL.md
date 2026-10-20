---
name: ops-logs
description: "Correlate available logs around a specific failure. Use for bounded log correlation; trace follows a particular execution path through source and telemetry."
---

# ops-logs

Correlate available logs around a specific failure.

## Choose this workflow

Use for bounded log correlation; trace follows a particular execution path through source and telemetry.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Operations methods](../../references/packs/operations.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; service/environment, time window, correlation identifiers, and question.

**Pack prerequisites:** Exact service/environment, time window, revision/configuration identity, authorized logs/metrics, and operational constraints. Prefer observation before intervention; live restarts, traffic changes, restores, and notifications require the requested target/action. Redact sensitive telemetry.

- **Infer from evidence:** Read service/environment, time window, revision, available telemetry and existing incident or recovery procedure.
- **Reasonable default:** Start from supplied logs and read-only observation; rank hypotheses without presenting an unexecuted intervention as recovery.
- **Ask only when needed:** Resolve the precise target and missing authority before restart, restore, notification or traffic changes; continue evidence analysis while waiting.

Declared evidence requirements: `telemetry.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Focused log correlation and anomaly explanation, not unrestricted telemetry export.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Normalize time zones and identify clock skew.
2. Follow stable request and job IDs across related services, redacting sensitive fields.
3. Distinguish original failures and root events from retry cascades and repeated symptoms.

## Technical method

- **Inspect:** Identify request/job IDs, service boundaries, clock skew, retention and redaction rules.
- **Method:** Query bounded windows and correlate the first causal failure across retries and asynchronous stages.
- **Avoid misdiagnosis:** Repeated downstream errors can all stem from one upstream failure; log absence can reflect sampling.
- **Check the result:** Trace one failed and one healthy operation and document missing spans or inaccessible sources without inventing continuity.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Operations worked example](../../references/examples/operations.md).


## Decision branches

- **When a relevant span or time range is missing:** Report the gap and query needed; absence is not proof the action never occurred.

## Deliver and verify

- Evidence-linked timeline with timestamps and correlation IDs, the likely causal sequence, redactions and gaps requiring metrics or traces.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Clock/time-zone differences are considered; missing logs are not proof that an event never occurred.

## Stop and recover

- Bound query range and volume. Do not dump entire production logs into the conversation or external storage.

## Example requests

- **Normal (inspect):** Correlate sanitized logs for this request ID and time window.
- **Edge (inspect):** Correlate logs across services with different clock offsets.
- **Blocked (inspect):** Analyze a redacted excerpt without querying or dumping full production logs.
