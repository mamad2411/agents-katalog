---
name: ml-train
description: "Implement training with checkpoints and recorded configuration. Use for bounded training implementation/execution; ml-debug-training diagnoses a failed optimization process."
---

# ml-train

Implement training with checkpoints and recorded configuration.

## Choose this workflow

Use for bounded training implementation/execution; ml-debug-training diagnoses a failed optimization process.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [ML experimentation methods](../../references/packs/ml-experiments.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan the training design; apply for requested pipeline implementation or an authorized bounded run.

**Pack prerequisites:** Dataset/split manifests, fixed objective/metric, environment/dependencies, baseline where applicable, and explicit compute limits. Record code revision, configuration, seeds, artifact paths, and resource use. Local smoke checks do not imply authorization for paid training. Never optimize on the held-out test set.

- **Infer from evidence:** Read framework, training entry point, loss/metric, split manifests and checkpoint conventions from supplied source.
- **Reasonable default:** In apply mode, implement requested code and tiny isolated smoke checks with existing tools, and otherwise propose them; leave unmeasured model quality explicit.
- **Ask only when needed:** Ask for unresolved objective/data semantics before encoding them, and environment/resource limits before launching training or a search; implementation alone does not need a hardware purchase decision.

Resolve any task-specific tools, target identity and evidence before dependent actions. No external connection is assumed.

## Scope

Reproducible training with checkpoint/resume and declared stopping criteria.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: make the requested changes or execute the requested operation within its resolved target and limits. Local preparation does not authorize live, remote, destructive or paid actions; existing explicit session authorization still applies.

## Execute

1. Validate shapes and pipeline, run a small smoke test, record configuration/environment, train within bounds, checkpoint, and evaluate only the permitted validation protocol.
2. For resumable training inventory model, optimizer, scheduler, scaler when used, step, RNG and sampler/data position; checkpoint atomically and compare interrupted versus uninterrupted continuation under declared tolerances.

## Technical method

- **Inspect:** Inspect framework/version, shapes, loss semantics, device/dtype, optimizer, scheduler and data/sampler state.
- **Method:** Run a bounded smoke batch, then checkpoint at a defined boundary including continuation state; load the training scenario for the actual framework.
- **Avoid misdiagnosis:** Restoring weights alone is not exact resume; a seed alone does not guarantee deterministic kernels or data order.
- **Check the result:** Compare interrupted and uninterrupted short runs under stated tolerances and verify atomic checkpoint recovery after an incomplete write.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [ML experimentation worked example](../../references/examples/ml-experiments.md).
- Selecting classical, tensor or distributed/resumable methods: [Training scenarios](../../references/scenarios/training.md).
- The task specifically involves pytorch, autograd, ddp, cuda mismatch; load only the matching method: [PyTorch autograd, device and distributed debugging](../../references/methods/pytorch-debug.md).

## Decision branches

- **When only weights were saved:** Treat loading as initialization unless all required continuation state is available; label the run a restart rather than exact resume.
- **When implementation is requested but a training run is not:** Implement configuration, checkpoint and resume paths against local synthetic fixtures; ask for hardware, data access and resource limits only before a real training run.
- **When distributed training changes workers or accumulation boundaries:** Verify sampler/metric aggregation and checkpoint ownership; declare approximate continuation if exact state cannot be restored.

## Deliver and verify

- Training code or run record with configuration, resource cap, artifact/state manifest, checkpoints, metrics and demonstrated resume conditions.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Interrupted training can resume with identified state; NaNs or budget exhaustion stop clearly without a false completed result.

## Stop and recover

- No paid hardware provisioning implicitly. Do not label the best validation checkpoint as independently test-validated.

## Example requests

- **Normal (plan):** Plan checkpointed training on one GPU for at most six hours; do not provision compute.
- **Edge (apply):** Implement checkpointed training that resumes mid-epoch without silently changing sample order.
- **Blocked (inspect):** Plan training with no authorized hardware budget; do not provision or launch a run.
