---
name: ops-incident
description: "Organize symptoms, evidence, impact, hypotheses, and immediate actions. Use for current operational triage; ops-postmortem reconstructs the completed incident."
---

# ops-incident

Organize symptoms, evidence, impact, hypotheses, and immediate actions.

## Choose this workflow

Use for current operational triage; ops-postmortem reconstructs the completed incident.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Operations methods](../../references/packs/operations.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; symptoms, affected service/environment, incident window, and known impact. Apply for a specific mitigation the user authorizes.

**Pack prerequisites:** Exact service/environment, time window, revision/configuration identity, authorized logs/metrics, and operational constraints. Prefer observation before intervention; live restarts, traffic changes, restores, and notifications require the requested target/action. Redact sensitive telemetry.

- **Infer from evidence:** Read service/environment, time window, revision, available telemetry and existing incident or recovery procedure.
- **Reasonable default:** Start from supplied logs and read-only observation; rank hypotheses without presenting an unexecuted intervention as recovery.
- **Ask only when needed:** Resolve the precise target and missing authority before restart, restore, notification or traffic changes; continue evidence analysis while waiting.

Declared evidence requirements: `telemetry.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Organize triage and recommend immediate actions; an authorized mitigation runs in apply mode.

Inspect/plan: triage and recommend; save requested artifacts only. Apply: carry out only the specific mitigation the user authorized, such as a rollback, restart, flag change or queue drain, against its resolved target after capturing the state it may erase; one step at a time, each verified and recorded. Customer messages, failovers and unrelated changes need their own exact request.

## Execute

1. Establish impact, time window, affected revision, and recent changes and dependencies.
2. Keep a timestamped ledger separating facts, hypotheses and actions.
3. Prefer reversible mitigations within scope.

## Technical method

- **Inspect:** Resolve incident window/timezone, service/revision, customer impact and available logs/metrics/traces.
- **Method:** Maintain a timeline separating observation, hypothesis and intervention; preserve evidence before state-changing recovery.
- **Avoid misdiagnosis:** A nearby deployment is correlation, not proof; missing telemetry cannot establish no impact.
- **Check the result:** Tie each conclusion to timestamped evidence and record whether the proposed mitigation actually changed the observed symptom.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Operations worked example](../../references/examples/operations.md).
- The incident involves a Kubernetes rollout, crash loop or failing readiness: [Kubernetes release and readiness](../../references/methods/kubernetes-release.md).
- Environment drift between hosts or releases may explain the failure: [Reproducible environments](../../references/methods/reproducible-environments.md).
- The incident involves BGP, VLAN, VPN or other network device state: [Network operations](../../references/methods/network-operations.md).

## Decision branches

- **When an intervention may erase evidence or duplicate effects:** Capture relevant state and define its observation/abort condition before acting.
- **When the user authorizes a specific mitigation:** Resolve the exact target and action, capture the state it may erase, state the expected observation and abort condition, run it once, verify the symptom changed, and record the step in the incident ledger.

## Deliver and verify

- Current incident brief with impact and timeline, supported hypotheses, next diagnostic steps, mitigation options and observed recovery.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A coincident deployment is a hypothesis until supported; unknown customer impact is not reported as zero.

## Stop and recover

- No unrequested restarts, failovers, or customer messages. Preserve evidence before interventions that may erase it.

## Example requests

- **Normal (inspect):** Organize this incident's impact, timeline, and next diagnostic actions without restarting services.
- **Edge (inspect):** Triage rising errors after a deployment with an unrelated provider incident.
- **Blocked (inspect):** Inspect supplied incident evidence without restarting services or sending customer messages.
- **Additional (apply):** Roll back checkout-api to the previous release and restart the payment worker; I authorize both.
