---
name: trace
description: "Follow a request, event, or data value through the system. Use to follow one execution or data path across boundaries; map shows topology without reconstructing a particular flow; data-lineage maps where a field or metric comes from across transformations."
---

# trace

Follow a request, event, or data value through the system.

## Choose this workflow

Use to follow one execution or data path across boundaries; map shows topology without reconstructing a particular flow; data-lineage maps where a field or metric comes from across transformations.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [General methods](../../references/packs/general.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; request, event, identifier, or data value and optional environment/time window. Requires source or relevant sanitized telemetry.

**Pack prerequisites:** Resolve the user brief and inspect the relevant project or supplied evidence. External capabilities are optional unless the selected action actually needs them.

- **Infer from evidence:** Resolve the named files, existing scripts, current task and earlier corrections from the conversation and repository.
- **Reasonable default:** Use the narrowest interpretation that completes a reversible local task; state a consequential assumption once.
- **Ask only when needed:** Ask when competing targets or incompatible success conditions would change the result; continue independent inspection first.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

One end-to-end execution/data path, including service boundaries; no new instrumentation by default.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Identify the entry point and start from a concrete input or correlation ID.
2. Follow each transformation and dispatch, recording the hop's input, output, identity propagation and synchronous or asynchronous transition; mark missing spans where the path is unobserved.

## Technical method

- **Inspect:** Locate entry point, transformations, asynchronous handoffs, identity propagation and terminal effects.
- **Method:** Follow one concrete request/value, recording boundaries and error branches with file or runtime evidence.
- **Avoid misdiagnosis:** A static call graph does not prove which branch executed; queue handoffs can change identity and ordering.
- **Check the result:** Reconcile the trace against one success and one failure observation, marking any inaccessible runtime segment.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [General worked example](../../references/examples/general.md).


## Decision branches

- **When a queue or external service has no downstream evidence:** End the confirmed trace at that boundary and list the exact log or source needed to continue.

## Deliver and verify

- Ordered hop table with each hop's source or telemetry evidence, payload transformation, failure branches and gaps.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- An async job is separated from its triggering request; an absent downstream log is reported as a gap rather than proof of success.

## Stop and recover

- Do not scan unrelated tenant data or infer causation from timestamp proximity alone.

## Example requests

- **Normal (inspect):** Trace an order from the checkout route through the payment job.
- **Edge (inspect):** Trace a checkout request through a queued email and a failed payment callback.
- **Blocked (inspect):** Trace only these supplied logs; downstream worker logs are unavailable.
