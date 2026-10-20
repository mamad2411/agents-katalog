---
name: ml-report
description: "Document data, results, limitations, and intended use. Use to communicate established ML evidence; ml-evaluate creates evaluation results."
---

# ml-report

Document data, results, limitations, and intended use.

## Choose this workflow

Use to communicate established ML evidence; ml-evaluate creates evaluation results.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [ML evaluation methods](../../references/packs/ml-evaluation.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan; task, dataset/model manifests, evaluation results, intended use, and audience.

**Pack prerequisites:** Frozen model/artifact, evaluation dataset identity, labels where needed, metric definitions, and task/operating context. Report sample counts and uncertainty appropriate to dependencies; avoid repeated test-set tuning. Exploratory findings need fresh confirmation before strong generalization claims.

- **Infer from evidence:** Read frozen model/data identities, metric definitions, denominators and supplied predictions; separate validation from test use.
- **Reasonable default:** Compute only supported metrics on permitted samples and label missing labels or subgroup coverage as unknown.
- **Ask only when needed:** Ask when the operating cost/threshold or population changes the evaluation decision; do not fabricate labels to avoid a question.

Declared evidence requirements: `ml.artifacts`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Accurate model documentation and release assessment; no invented experiments or approval.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Reconcile every number with a run and denominator.
2. Describe training and evaluation conditions, separating validation selection from independent test evidence, and summarize baseline and slice results.
3. Document the deployment population, limitations, excluded uses and missing release evidence.

## Technical method

- **Inspect:** Collect intended use, dataset provenance, protocol, selected model, metrics, slices and deployment constraints.
- **Method:** Separate measured results from anticipated value and list excluded uses plus concrete monitoring/revisit conditions.
- **Avoid misdiagnosis:** Omitting failed runs or weak slices produces a misleading model story even if the best metric is correct.
- **Check the result:** Trace every numerical claim to an artifact and verify data/model/version identity and unresolved limitations are retained.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [ML evaluation worked example](../../references/examples/ml-evaluation.md).


## Decision branches

- **When evidence is missing for a key cohort or release gate:** Keep the limitation visible and withhold the corresponding suitability claim.

## Deliver and verify

- Model report or card with model/data/version provenance, metrics, baseline/slice evidence, operating assumptions, limitations, open risks and release gaps.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Every numerical claim traces to an actual run; missing cohort evidence is disclosed rather than generalized away.

## Stop and recover

- Do not present a report as deployment authorization or claim suitability for untested populations.

## Example requests

- **Normal (plan):** Write a model report using these actual runs and identify unsupported uses.
- **Edge (plan):** Write a model report with strong average performance but poor sparse-cohort evidence.
- **Blocked (inspect):** Draft a report with missing test results; do not invent metrics or deployment approval.
