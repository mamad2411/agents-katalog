---
name: ml-threshold
description: "Choose thresholds against explicit costs or capacity limits. Use to choose a decision cutoff under explicit costs/capacity; ml-evaluate measures fixed behavior."
---

# ml-threshold

Choose thresholds against explicit costs or capacity limits.

## Choose this workflow

Use to choose a decision cutoff under explicit costs/capacity; ml-evaluate measures fixed behavior.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [ML evaluation methods](../../references/packs/ml-evaluation.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan; scores/labels, explicit error costs or capacity, prevalence, and validation protocol.

**Pack prerequisites:** Frozen model/artifact, evaluation dataset identity, labels where needed, metric definitions, and task/operating context. Report sample counts and uncertainty appropriate to dependencies; avoid repeated test-set tuning. Exploratory findings need fresh confirmation before strong generalization claims.

- **Infer from evidence:** Read frozen model/data identities, metric definitions, denominators and supplied predictions; separate validation from test use.
- **Reasonable default:** Compute only supported metrics on permitted samples and label missing labels or subgroup coverage as unknown.
- **Ask only when needed:** Ask when the operating cost/threshold or population changes the evaluation decision; do not fabricate labels to avoid a question.

Declared evidence requirements: `ml.artifacts`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Select an operating point or decision policy; no production activation.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Compute validation tradeoffs with denominators and tie handling.
2. Translate them into expected workload under the stated volume, prevalence and capacity, with uncertainty, and choose using validation data.
3. Reserve independent confirmation.

## Technical method

- **Inspect:** Obtain score distribution, error costs, review capacity, protected requirements and selection data.
- **Method:** Choose an operating point using explicit constraints and uncertainty; keep threshold selection separate from final test reporting.
- **Avoid misdiagnosis:** A threshold maximizing F1 may violate a daily capacity or false-positive budget.
- **Check the result:** Compute the confusion matrix and workload at nearby thresholds, including tied scores and changing prevalence assumptions.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [ML evaluation worked example](../../references/examples/ml-evaluation.md).


## Decision branches

- **When no agreed cost or capacity preference distinguishes options:** Present the tradeoff curve and the missing decision rather than selecting an arbitrary optimum.

## Deliver and verify

- Threshold policy and recommendation with confusion and workload estimates, assumptions, sensitivity and the independent evaluation requirement.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A daily review cap is respected under declared volume assumptions; a changed prevalence is shown to affect workload/precision.

## Stop and recover

- Do not invent business costs or optimize against the held-out test set. Unresolved priorities yield a tradeoff curve rather than a forced value.

## Example requests

- **Normal (plan):** Choose validation thresholds when reviewers can inspect 200 transactions daily.
- **Edge (plan):** Select a daily review threshold with tied scores and a hard queue cap.
- **Blocked (inspect):** Compare cutoffs with unknown error costs; do not optimize on test labels.
