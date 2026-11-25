---
name: ml-reproduce
description: "Reproduce a result from code, data, and configuration. Use to repeat a specified run; ml-baseline defines a new benchmark."
---

# ml-reproduce

Reproduce a result from code, data, and configuration.

## Choose this workflow

Use to repeat a specified run; ml-baseline defines a new benchmark.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [ML experimentation methods](../../references/packs/ml-experiments.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Inspect reproduction evidence or plan the attempt; apply for requested reproduction code or bounded execution.

**Pack prerequisites:** Dataset/split manifests, fixed objective/metric, environment/dependencies, baseline where applicable, and explicit compute limits. Record code revision, configuration, seeds, artifact paths, and resource use. Local smoke checks do not imply authorization for paid training. Never optimize on the held-out test set.

- **Infer from evidence:** Read framework, training entry point, loss/metric, split manifests and checkpoint conventions from supplied source.
- **Reasonable default:** In apply mode, implement requested code and tiny isolated smoke checks with existing tools, and otherwise propose them; leave unmeasured model quality explicit.
- **Ask only when needed:** Ask for unresolved objective/data semantics before encoding them, and environment/resource limits before launching training or a search; implementation alone does not need a hardware purchase decision.

Resolve any task-specific tools, target identity and evidence before dependent actions. No external connection is assumed.

## Scope

Re-run a defined result with explicit reproducibility criteria.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: make the requested changes or execute the requested operation within its resolved target and limits. Local preparation does not authorize live, remote, destructive or paid actions; existing explicit session authorization still applies.

## Execute

1. Resolve exact data, artifact, code and dependency identities.
2. Reconstruct preprocessing and evaluation, and declare nondeterminism tolerances before execution.
3. Run authorized bounded work, compare outputs and metrics within the declared tolerance, and isolate deviations.

## Technical method

- **Inspect:** Resolve code revision, dependencies, artifacts, dataset access, hardware and claimed tolerance.
- **Method:** Recreate the stated protocol; document each unavoidable substitution and whether it affects exact reproduction or only qualitative comparison.
- **Avoid misdiagnosis:** Matching a seed or top-line metric does not establish the same data, selection process or training trajectory.
- **Check the result:** Compare artifacts and outputs under declared tolerances and preserve failures or inaccessible inputs as limits on the claim.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [ML experimentation worked example](../../references/examples/ml-experiments.md).
- The task specifically involves pytorch, autograd, ddp, cuda mismatch; load only the matching method: [PyTorch autograd, device and distributed debugging](../../references/methods/pytorch-debug.md).

## Decision branches

- **When original assets are unavailable and substitutes are necessary:** Label the result a reimplementation or approximate reproduction and list each substitution.
- **When the request is for local preparation or implementation:** Create the requested environment/configuration and synthetic smoke path; separate pipeline reproduction from matching a reported scientific result.

## Deliver and verify

- Reproduction record and manifest with matched and different conditions, the measured result, deviations and discrepancy analysis against the justified tolerance.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Data/version mismatch is discovered before claiming reproduction; nondeterministic hardware differences use declared tolerances.

## Stop and recover

- Missing original assets may make exact reproduction impossible. Do not silently substitute a different dataset or model and call it reproduced.

## Example requests

- **Normal (plan):** Plan reproducing this result with exact artifact identities and a two-hour budget.
- **Edge (plan):** Reproduce a GPU run on another supported device with explicit tolerances.
- **Blocked (inspect):** Assess reproducibility when the original dataset snapshot is missing.
