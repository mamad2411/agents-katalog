---
name: ml-dataset
description: "Audit whether data can support the modeling task. Use to assess whether data supports a task; data-profile summarizes its columns."
---

# ml-dataset

Audit whether data can support the modeling task.

## Choose this workflow

Use to assess whether data supports a task; data-profile summarizes its columns.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [ML data methods](../../references/packs/ml-data.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; framed task, dataset version, collection process, and sampling budget.

**Pack prerequisites:** Task definition, dataset identity, field semantics, entity/time keys, and permission to inspect bounded data. Record prediction moment, label horizon, sampling, and provenance. Preserve held-out evaluation boundaries; no data upload, label alteration, or feature fitting across splits implicitly.

- **Infer from evidence:** Read prediction moment, label horizon, entity/time keys, split policy and dataset provenance from the task and manifests.
- **Reasonable default:** Use explicit synthetic examples for design when raw data is unavailable; do not infer missing labels or fit preprocessing across held-out boundaries.
- **Ask only when needed:** Ask when unresolved label timing, grouping or target semantics would change the split/features; do not demand a full dataset to explain the method.

Declared evidence requirements: `data.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Task suitability, population coverage, missingness, dependencies, and collection bias.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Compare the collection and selection process and follow-up windows with the task's needs and the deployment population.
2. Inspect coverage by cohort and time, identify censored or missing outcomes and missing-label patterns, and name deployment populations the data does not cover.

## Technical method

- **Inspect:** Inspect collection mechanism, row grain, entity coverage, duplicates, labels and permission to use the data.
- **Method:** Assess whether observations cover the intended deployment population and whether outcomes are observable without selection artifacts.
- **Avoid misdiagnosis:** More rows do not remove survivor bias or dependence between observations.
- **Check the result:** Reconcile sample membership and label coverage by important groups; distinguish observed gaps from unsupported population conclusions.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [ML data worked example](../../references/examples/ml-data.md).


## Decision branches

- **When training data excludes the intended deployment cohort:** Limit generalization claims and propose evidence collection before model complexity.

## Deliver and verify

- Dataset readiness report with a population/coverage table, missingness and selection risks, exclusions, supported deployment claims and needed collection or validation work.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A dataset missing outcome follow-up is not treated as fully labeled; a deployment cohort absent from training is flagged.

## Stop and recover

- Do not infer representativeness from sample size alone. Unsupported collection semantics remain unknown.

## Example requests

- **Normal (inspect):** Assess whether this dataset covers the intended deployment population.
- **Edge (inspect):** Assess a dataset with many rows but no labels for recently enrolled users.
- **Blocked (inspect):** Review dataset metadata without row access; avoid inferring representative coverage.
