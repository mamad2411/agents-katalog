---
name: ml-monitor
description: "Define operational and model-quality monitoring, including delayed labels. Use to design or implement requested ML telemetry; ops-alerts designs response-worthy alert behavior."
---

# ml-monitor

Define operational and model-quality monitoring, including delayed labels.

## Choose this workflow

Use to design or implement requested ML telemetry; ops-alerts designs response-worthy alert behavior.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [ML deployment methods](../../references/packs/ml-deployment.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan monitoring; apply for requested instrumentation or configuration in the identified environment.

**Pack prerequisites:** Versioned model and preprocessing artifacts, input/output schema, runtime/dependencies, operating targets, and authorized environment. Validate artifact trust before loading formats that can execute code. Packaging or writing monitoring configuration does not deploy a model or enable a hosted service.

- **Infer from evidence:** Read artifact format/trust, preprocessing schema, serving runtime, compatibility and existing rollout controls.
- **Reasonable default:** Prepare packaging/configuration and isolated checks without treating them as a live deployment.
- **Ask only when needed:** Resolve the target, rollback compatibility and operating limits before rollout or load generation; missing production access does not block packaging.

Declared evidence requirements: `telemetry.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Operational health, data quality, model performance, and label-arrival monitoring.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: make the requested changes or execute the requested operation within its resolved target and limits. Local preparation does not authorize live, remote, destructive or paid actions; existing explicit session authorization still applies.

## Execute

1. Separate service, feature, prediction and delayed-outcome signals, distinguishing leading signals from outcome metrics.
2. Define stable joins, label-lag windows and model-version attribution, and choose thresholds and runbook actions.
3. Implement only requested instrumentation or configuration.

## Technical method

- **Inspect:** Trace prediction IDs to model/data versions, outcomes, label delay, errors and operational measurements.
- **Method:** Define quality windows based on matured labels and connect each alert to a diagnosis/recovery action.
- **Avoid misdiagnosis:** Missing outcomes can bias observed accuracy; unchanged inputs do not prove unchanged target relationships.
- **Check the result:** Simulate delayed/missing labels, a model revision and an outage; verify denominators, routing and unknown-quality states.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [ML deployment worked example](../../references/examples/ml-deployment.md).


## Decision branches

- **When recent predictions have not had time to receive labels:** Exclude them from matured quality denominators and report pending follow-up separately.
- **When the request is for local preparation or implementation:** Implement drift/quality monitors against synthetic windows; treat unlabeled proxy drift as a signal, not demonstrated accuracy loss.

## Deliver and verify

- Monitoring design or code with the signal/window/join/threshold/action contract, metric definitions, privacy controls and delayed-label and alert tests.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Delayed labels do not make recent unlabeled cases look correct; model-version changes remain distinguishable.

## Stop and recover

- Do not activate external alerts or promise ongoing observation without an actual authorized runtime/scheduler.

## Example requests

- **Normal (plan):** Design quality monitoring with delayed labels and model-version separation.
- **Edge (plan):** Monitor a model whose outcomes arrive thirty days after prediction.
- **Blocked (inspect):** Plan monitoring without activating alerts or claiming an ongoing watcher exists.
