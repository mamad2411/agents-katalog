---
name: ml-ablation
description: "Measure contributions of features or model components. Use to estimate component contribution; ml-tune optimizes parameters, and ml-explain attributes existing predictions without retraining."
---

# ml-ablation

Measure contributions of features or model components.

## Choose this workflow

Use to estimate component contribution; ml-tune optimizes parameters, and ml-explain attributes existing predictions without retraining.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [ML experimentation methods](../../references/packs/ml-experiments.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan a controlled comparison; apply for requested experiment code or bounded execution.

**Pack prerequisites:** Dataset/split manifests, fixed objective/metric, environment/dependencies, baseline where applicable, and explicit compute limits. Record code revision, configuration, seeds, artifact paths, and resource use. Local smoke checks do not imply authorization for paid training. Never optimize on the held-out test set.

- **Infer from evidence:** Read framework, training entry point, loss/metric, split manifests and checkpoint conventions from supplied source.
- **Reasonable default:** In apply mode, implement requested code and tiny isolated smoke checks with existing tools, and otherwise propose them; leave unmeasured model quality explicit.
- **Ask only when needed:** Ask for unresolved objective/data semantics before encoding them, and environment/resource limits before launching training or a search; implementation alone does not need a hardware purchase decision.

Resolve any task-specific tools, target identity and evidence before dependent actions. No external connection is assumed.

## Scope

Isolate the contribution of specified components using controlled comparisons.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: make the requested changes or execute the requested operation within its resolved target and limits. Local preparation does not authorize live, remote, destructive or paid actions; existing explicit session authorization still applies.

## Execute

1. State the causal comparison: one meaningful variation at a time or a justified factorial design.
2. Hold data and evaluation protocol constant, and repeat seeds or matched runs where variance could overwhelm the effect.
3. Compare each variant's effect with its uncertainty and cost.

## Technical method

- **Inspect:** Identify the component claim, matched data/protocol, randomness and comparison metric.
- **Method:** Remove or vary one meaningful component while holding the rest fixed and repeat enough to expose relevant variance within budget.
- **Avoid misdiagnosis:** A changed preprocessing pipeline or compute budget can confound a claimed component improvement.
- **Check the result:** Compare paired outcomes where possible, report uncertainty and preserve a no-change control when evaluation noise matters.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [ML experimentation worked example](../../references/examples/ml-experiments.md).


## Decision branches

- **When removing a component changes another required contract:** Redesign the comparison or disclose the confound instead of attributing all change to one component.
- **When the request is for local preparation or implementation:** Implement isolated feature/configuration switches and comparable run metadata; defer result claims until comparable measurements exist.

## Deliver and verify

- Ablation protocol or run results as a variant matrix with attributable differences, uncertainty, cost/quality interpretation and caveats.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Data changes do not confound the component comparison; noisy score differences are not declared decisive.

## Stop and recover

- Do not remove interdependent components without explaining the changed model contract. Budget limits constrain repeats and confidence.

## Example requests

- **Normal (plan):** Plan a controlled comparison of the new features at fixed data and seed conditions.
- **Edge (plan):** Ablate a feature group while preprocessing depends on those columns.
- **Blocked (inspect):** Plan an ablation with insufficient run budget; state the confidence limitation.
