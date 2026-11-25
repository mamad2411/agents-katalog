---
name: ml-debug-training
description: "Investigate exploding loss, unstable gradients, NaNs, or failure to learn. Use for NaNs, shape/device errors or non-learning; ml-error-analysis studies generalization failures."
---

# ml-debug-training

Investigate exploding loss, unstable gradients, NaNs, or failure to learn.

## Choose this workflow

Use for NaNs, shape/device errors or non-learning; ml-error-analysis studies generalization failures.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [ML experimentation methods](../../references/packs/ml-experiments.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; failing run logs/configuration, batches, model, and training symptom. Apply for requested bounded probes or a minimal corrective change.

**Pack prerequisites:** Dataset/split manifests, fixed objective/metric, environment/dependencies, baseline where applicable, and explicit compute limits. Record code revision, configuration, seeds, artifact paths, and resource use. Local smoke checks do not imply authorization for paid training. Never optimize on the held-out test set.

- **Infer from evidence:** Read framework, training entry point, loss/metric, split manifests and checkpoint conventions from supplied source.
- **Reasonable default:** In apply mode, implement requested code and tiny isolated smoke checks with existing tools, and otherwise propose them; leave unmeasured model quality explicit.
- **Ask only when needed:** Ask for unresolved objective/data semantics before encoding them, and environment/resource limits before launching training or a search; implementation alone does not need a hardware purchase decision.

Declared evidence requirements: `ml.artifacts`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Numerical instability, shape/device issues, data/target mismatch, gradients, and failure to learn.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: make the requested changes or execute the requested operation within its resolved target and limits. Local preparation does not authorize live, remote, destructive or paid actions; existing explicit session authorization still applies.

## Execute

1. Isolate a small batch and inspect its shapes, labels, scale, loss and gradients against expected scales, and check optimizer state.
2. Locate the first non-finite value and compare optimizer updates with the intended objective.
3. Propose overfit and gradient probes that test the leading cause, running them in apply mode.

## Technical method

- **Inspect:** Capture the first divergent batch, activations/loss, gradient finiteness and parameter update.
- **Method:** Check objective/target semantics and preprocessing before tuning; use a tiny-batch overfit probe to distinguish plumbing from generalization.
- **Avoid misdiagnosis:** Switching architecture can conceal a detached graph, wrong target scale or optimizer that never updates parameters.
- **Check the result:** Verify finite forward/backward values and actual parameter changes on the smallest failing input before a longer run.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [ML experimentation worked example](../../references/examples/ml-experiments.md).
- Language/runtime semantics, concurrency or resource ownership can change the result: [Language and runtime review methods](../../references/scenarios/language-review.md).
- The task specifically involves pytorch, autograd, ddp, cuda mismatch; load only the matching method: [PyTorch autograd, device and distributed debugging](../../references/methods/pytorch-debug.md).

## Decision branches

- **When a tiny-batch overfit probe fails:** Investigate data/loss/gradient/update plumbing before larger architectures or more epochs.

## Deliver and verify

- Diagnosis with the first divergent tensor or step, hypothesis evidence, and a bounded corrective probe or, in apply mode, a minimal corrective change.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- NaNs are localized to their first source; an inability to overfit a tiny batch prompts pipeline investigation rather than a larger model.

## Stop and recover

- No unbounded retraining or random parameter changes. Preserve failed-run evidence and distinguish numerical repair from generalization improvement.

## Example requests

- **Normal (inspect):** Diagnose NaNs from this run's first failing batch and gradient logs.
- **Edge (inspect):** Debug a loss that becomes NaN only after mixed-precision updates.
- **Blocked (inspect):** Inspect saved training logs without retraining or guessing a learning-rate cure.
