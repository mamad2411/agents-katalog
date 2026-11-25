---
name: ml-rollout
description: "Prepare shadow, canary or staged rollout of a model version with rollback criteria. Use for a scoped model promotion plan or transition; ml-report documents offline evidence."
---

# ml-rollout

Prepare shadow, canary or staged rollout of a model version with rollback criteria.

## Choose this workflow

Use for a scoped model promotion plan or transition; ml-report documents offline evidence.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [ML deployment methods](../../references/packs/ml-deployment.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan rollout; apply for requested rollout configuration or an explicitly requested promotion.

**Pack prerequisites:** Versioned model and preprocessing artifacts, input/output schema, runtime/dependencies, operating targets, and authorized environment. Validate artifact trust before loading formats that can execute code. Packaging or writing monitoring configuration does not deploy a model or enable a hosted service.

- **Infer from evidence:** Read artifact format/trust, preprocessing schema, serving runtime, compatibility and existing rollout controls.
- **Reasonable default:** Prepare packaging/configuration and isolated checks without treating them as a live deployment.
- **Ask only when needed:** Resolve the target, rollback compatibility and operating limits before rollout or load generation; missing production access does not block packaging.

Declared evidence requirements: `ml.artifacts`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Shadow/canary/staged rollout and recovery; execution only on explicitly authorized targets.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: make the requested changes or execute the requested operation within its resolved target and limits. Local preparation does not authorize live, remote, destructive or paid actions; existing explicit session authorization still applies.

## Execute

1. Check feature, schema, package and artifact compatibility, and preserve a usable fallback artifact and traffic-switch mechanism.
2. Define shadow or canary cohort routing, comparison metrics and predeclared stop criteria as staged gates.
3. Verify authorized transitions against evidence.

## Technical method

- **Inspect:** Resolve candidate/baseline models, compatibility, routing identity, shadow side effects and rollback conditions.
- **Method:** Compare shadow or canary traffic under a stable assignment policy; define operational stops and enough label maturity for quality claims.
- **Avoid misdiagnosis:** Shadow requests must not duplicate real effects; early unlabeled traffic only establishes operational behavior.
- **Check the result:** Exercise rollback with in-flight requests, verify model attribution and keep operational acceptance separate from delayed quality acceptance.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [ML deployment worked example](../../references/examples/ml-deployment.md).


## Decision branches

- **When fallback cannot consume the new schema or features:** Resolve that compatibility before describing rollback as available.
- **When the request is for local preparation or implementation:** Prepare gates, shadow/canary configuration and recovery checks locally; require target identity and current evidence before promotion.

## Deliver and verify

- Rollout plan or execution record with the cohort/gate/metric plan, candidate and fallback identities, actual traffic/version state and rollback criteria.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Canary failures halt progression; rollback accounts for incompatible feature/schema changes.

## Stop and recover

- No automatic full rollout from good offline metrics. Shadow traffic may incur cost and privacy obligations covered by the requested scope.

## Example requests

- **Normal (plan):** Prepare a canary rollout and rollback plan for the new ranking model; do not change production traffic.
- **Edge (plan):** Plan a canary when the previous model expects an older feature schema.
- **Blocked (inspect):** Assess rollout readiness without live routing access or shadow-inference budget.
