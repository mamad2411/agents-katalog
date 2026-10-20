---
name: ml-batch
description: "Build resumable batch inference and output tracking. Use for resumable batch inference; ml-serving handles request/response service behavior."
---

# ml-batch

Build resumable batch inference and output tracking.

## Choose this workflow

Use for resumable batch inference; ml-serving handles request/response service behavior.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [ML deployment methods](../../references/packs/ml-deployment.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply for implementation; model/data versions, partitioning, output keys, checkpoint destination, and run budget.

**Pack prerequisites:** Versioned model and preprocessing artifacts, input/output schema, runtime/dependencies, operating targets, and authorized environment. Validate artifact trust before loading formats that can execute code. Packaging or writing monitoring configuration does not deploy a model or enable a hosted service.

- **Infer from evidence:** Read artifact format/trust, preprocessing schema, serving runtime, compatibility and existing rollout controls.
- **Reasonable default:** Prepare packaging/configuration and isolated checks without treating them as a live deployment.
- **Ask only when needed:** Resolve the target, rollback compatibility and operating limits before rollout or load generation; missing production access does not block packaging.

Declared evidence requirements: `ml.artifacts`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Resumable batch inference; real dataset execution must be part of the request.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Freeze model and input snapshot identity, validate schemas, and partition by stable row keys.
2. Stage outputs and commit a manifest or checkpoint only after durable complete partitions, tracking failures and model versions.
3. Test resume and replay on controlled input.

## Technical method

- **Inspect:** Identify input snapshot, stable record IDs, model version, partitioning and output commit/checkpoint policy.
- **Method:** Write resumable idempotent partitions with provenance and reconcile partial output before advancing progress.
- **Avoid misdiagnosis:** Restarting with a different model under the same output partition silently mixes incompatible predictions.
- **Check the result:** Interrupt before/after output commit and retry; verify full membership, no duplicate records and consistent model/data identity.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [ML deployment worked example](../../references/examples/ml-deployment.md).


## Decision branches

- **When a restart finds partial output or a different model version:** Reconcile or isolate it before resuming; never silently mix incompatible predictions.

## Deliver and verify

- Batch job with its partition/model manifest, progress and output reconciliation, error policy, failure counts and resume evidence.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Restart does not duplicate completed outputs; invalid records are accounted for rather than silently lost.

## Stop and recover

- No unbounded full-dataset inference. Do not mix predictions from incompatible model versions in one unlabeled output.

## Example requests

- **Normal (apply):** Implement resumable batch inference with stable output keys and model-version tracking.
- **Edge (apply):** Resume inference after output writes succeeded but checkpointing failed.
- **Blocked (inspect):** Plan batch prediction without scanning the full dataset or launching unbounded compute.
