---
name: ml-tune
description: "Design a bounded hyperparameter search with a fixed evaluation protocol. Use for a bounded search under a valid protocol; ml-ablation isolates component contribution."
---

# ml-tune

Design a bounded hyperparameter search with a fixed evaluation protocol.

## Choose this workflow

Use for a bounded search under a valid protocol; ml-ablation isolates component contribution.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [ML experimentation methods](../../references/packs/ml-experiments.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan a search; apply for requested search code or a run with explicit resource limits.

**Pack prerequisites:** Dataset/split manifests, fixed objective/metric, environment/dependencies, baseline where applicable, and explicit compute limits. Record code revision, configuration, seeds, artifact paths, and resource use. Local smoke checks do not imply authorization for paid training. Never optimize on the held-out test set.

- **Infer from evidence:** Read framework, training entry point, loss/metric, split manifests and checkpoint conventions from supplied source.
- **Reasonable default:** In apply mode, implement requested code and tiny isolated smoke checks with existing tools, and otherwise propose them; leave unmeasured model quality explicit.
- **Ask only when needed:** Ask for unresolved objective/data semantics before encoding them, and environment/resource limits before launching training or a search; implementation alone does not need a hardware purchase decision.

Resolve any task-specific tools, target identity and evidence before dependent actions. No external connection is assumed.

## Scope

Bounded hyperparameter search; execution only within authorized resources.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: make the requested changes or execute the requested operation within its resolved target and limits. Local preparation does not authorize live, remote, destructive or paid actions; existing explicit session authorization still applies.

## Execute

1. Freeze the search space, split, objective, trial and resource caps and the selection rule before searching.
2. Select a search strategy with pruning and failure behavior, and log every trial, including failed and pruned ones.
3. Compare candidates under equal evaluation conditions and choose by the predeclared validation criterion; keep the confirmation set untouched.

## Technical method

- **Inspect:** Fix search space, metric direction, split, resource budget, pruning and selection rule.
- **Method:** Track every trial including failures and choose using validation only; reserve the held-out test for final evaluation.
- **Avoid misdiagnosis:** More trials can overfit the validation set; dropping failed runs understates cost and instability.
- **Check the result:** Enforce trial/time caps and inspect selection provenance; evaluate the chosen configuration once under the reserved protocol.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [ML experimentation worked example](../../references/examples/ml-experiments.md).


## Decision branches

- **When tuning repeatedly consults held-out test results:** Stop that selection loop and define fresh independent confirmation before reporting generalization.
- **When the request is for local preparation or implementation:** Implement search-space validation, trial accounting and interruption handling locally; do not submit a search job without its dataset and resource limits.

## Deliver and verify

- Search configuration and trial ledger with budgets consumed, the selected candidate, selection rationale, cost caveats and the untouched confirmation set.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Trial failures remain visible; test labels never influence parameter selection.

## Stop and recover

- Stop at any resource cap and preserve partial results. Do not enlarge the search merely because no improvement appears.

## Example requests

- **Normal (plan):** Plan at most 20 trials on validation PR-AUC; never tune on the test set.
- **Edge (plan):** Plan a search that tolerates failed trials under a strict GPU-hour cap.
- **Blocked (inspect):** Design tuning when compute is unavailable; do not fabricate winning hyperparameters.
