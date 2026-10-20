---
name: ops-observability
description: "Add useful logs, metrics, and traces to unclear execution paths. Use to implement requested diagnostic telemetry; ops-alerts turns signals into actionable notifications."
---

# ops-observability

Add useful logs, metrics, and traces to unclear execution paths.

## Choose this workflow

Use to implement requested diagnostic telemetry; ops-alerts turns signals into actionable notifications.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Operations methods](../../references/packs/operations.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply; unclear path, diagnostic goals, telemetry stack, privacy, and overhead constraints.

**Pack prerequisites:** Exact service/environment, time window, revision/configuration identity, authorized logs/metrics, and operational constraints. Prefer observation before intervention; live restarts, traffic changes, restores, and notifications require the requested target/action. Redact sensitive telemetry.

- **Infer from evidence:** Read service/environment, time window, revision, available telemetry and existing incident or recovery procedure.
- **Reasonable default:** Start from supplied logs and read-only observation; rank hypotheses without presenting an unexecuted intervention as recovery.
- **Ask only when needed:** Resolve the precise target and missing authority before restart, restore, notification or traffic changes; continue evidence analysis while waiting.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Useful logs, metrics, traces, correlation, and error context in the selected path.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Start with the questions operators must answer.
2. Propagate correlation across boundaries, and choose stable bounded-cardinality metrics plus redacted structured events.
3. Verify normal and error instrumentation locally.

## Technical method

- **Inspect:** Identify a specific unanswered operational question, request lifecycle and data sensitivity/cardinality.
- **Method:** Instrument useful stage timing, failure categories and correlation while bounding labels, volume and overhead.
- **Avoid misdiagnosis:** User IDs in metric labels cause unbounded cardinality; logging full payloads can expose credentials or private data.
- **Check the result:** Exercise success/error/cancellation and inspect exported telemetry, redaction, label bounds and instrumentation overhead.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Operations worked example](../../references/examples/operations.md).


## Decision branches

- **When proposed labels contain user IDs or arbitrary payload values:** Move needed detail to controlled logs/traces or aggregate dimensions instead of unbounded metric labels.

## Deliver and verify

- Instrumentation changes with a question/signal/location table, field and metric definitions, privacy/overhead decisions and success/error telemetry checks.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A failed operation can be traced across the intended boundary; raw user payloads or unbounded IDs do not become unsafe metric labels.

## Stop and recover

- No provider provisioning or production configuration rollout implicitly. Do not add high-volume logging without overhead consideration.

## Example requests

- **Normal (apply):** Add focused tracing without logging raw user payloads or high-cardinality labels.
- **Edge (apply):** Add tracing across a queue while keeping sensitive payloads out of logs.
- **Blocked (inspect):** Design observability without provisioning a vendor or changing production configuration.
