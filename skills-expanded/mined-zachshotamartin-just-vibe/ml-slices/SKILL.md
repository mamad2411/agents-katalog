---
name: ml-slices
description: "Compare meaningful cohorts or operating conditions. Use for cohort performance comparisons; ml-error-analysis investigates individual failure mechanisms."
---

# ml-slices

Compare meaningful cohorts or operating conditions.

## Choose this workflow

Use for cohort performance comparisons; ml-error-analysis investigates individual failure mechanisms.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [ML evaluation methods](../../references/packs/ml-evaluation.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; predictions/labels, meaningful cohorts, minimum sample guidance, and operating context.

**Pack prerequisites:** Frozen model/artifact, evaluation dataset identity, labels where needed, metric definitions, and task/operating context. Report sample counts and uncertainty appropriate to dependencies; avoid repeated test-set tuning. Exploratory findings need fresh confirmation before strong generalization claims.

- **Infer from evidence:** Read frozen model/data identities, metric definitions, denominators and supplied predictions; separate validation from test use.
- **Reasonable default:** Compute only supported metrics on permitted samples and label missing labels or subgroup coverage as unknown.
- **Ask only when needed:** Ask when the operating cost/threshold or population changes the evaluation decision; do not fabricate labels to avoid a question.

Declared evidence requirements: `ml.artifacts`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Performance across cohorts/time/conditions and coverage gaps.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Predefine important slices and their overlap where possible, and account for dependent samples.
2. Compute counts and metrics consistently, flag small groups, and distinguish planned from exploratory comparisons.
3. For supplied run exports, import and compare them with the experiments guide as ml-experiments does.

## Technical method

- **Inspect:** Define meaningful cohorts, support counts, denominators, overlap and intended decision.
- **Method:** Compare performance and uncertainty within slices, including missing group attributes and intersectional cases where supported.
- **Avoid misdiagnosis:** Tiny slices and many comparisons can produce dramatic noise; aggregate improvement can hide a harmed cohort.
- **Check the result:** Report counts and uncertainty with each metric and verify membership logic on hand-labeled examples.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [ML evaluation worked example](../../references/examples/ml-evaluation.md).
- Comparing supplied MLflow, W&B or JSON runs with row-level predictions: [Recorded experiment comparisons](../../references/experiments.md).
- The task specifically involves recommender, ranking metrics, retrieval ranking, ml adoption; load only the matching method: [Retrieval, ranking and recommendation evaluation](../../references/methods/recommender-systems.md).

## Decision branches

- **When a cohort has no outcomes or very few positives:** Report unavailable/unstable evidence rather than a confident zero or perfect score.
- **When aggregate performance improves while a slice regresses:** Show denominators and both outcomes, inspect parity/temporal issues and avoid ranking an incompatible evaluation.

## Deliver and verify

- Slice table with definitions, denominators, metrics, uncertainty, worst-supported conditions, coverage gaps and follow-up data needs.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A tiny cohort's extreme score is qualified; missing cohorts are shown as no evidence rather than zero performance.

## Stop and recover

- Avoid causal or fairness guarantees from a metric table alone. Do not expose identifying small-group records.

## Example requests

- **Normal (inspect):** Compare operating-condition cohorts and report uncertainty for small slices.
- **Edge (inspect):** Compare overlapping cohorts with one tiny high-error subgroup.
- **Blocked (inspect):** Assess slice coverage without sensitive row-level records or causal fairness claims.
