---
name: ml-frame
description: "Define target, prediction moment, unit of analysis, and objective. Use to define the prediction problem; ml-baseline implements the first comparator after the task is defined."
---

# ml-frame

Define target, prediction moment, unit of analysis, and objective.

## Choose this workflow

Use to define the prediction problem; ml-baseline implements the first comparator after the task is defined.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [ML data methods](../../references/packs/ml-data.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan; decision to support, population, available data, prediction timing, and operational objective.

**Pack prerequisites:** Task definition, dataset identity, field semantics, entity/time keys, and permission to inspect bounded data. Record prediction moment, label horizon, sampling, and provenance. Preserve held-out evaluation boundaries; no data upload, label alteration, or feature fitting across splits implicitly.

- **Infer from evidence:** Read prediction moment, label horizon, entity/time keys, split policy and dataset provenance from the task and manifests.
- **Reasonable default:** Use explicit synthetic examples for design when raw data is unavailable; do not infer missing labels or fit preprocessing across held-out boundaries.
- **Ask only when needed:** Ask when unresolved label timing, grouping or target semantics would change the split/features; do not demand a full dataset to explain the method.

Resolve any task-specific tools, target identity and evidence before dependent actions. No external connection is assumed.

## Scope

Define the modeling problem before selecting algorithms.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. State one prediction row's entity (the unit of analysis), timestamp, information available at prediction time, label horizon and the action taken from predictions.
2. Compare a rule-based decision or other baseline before choosing a model, and state the cost of each error type.

## Technical method

- **Inspect:** Establish prediction entity/time, decision being supported, available information, outcome horizon and label maturity.
- **Method:** Translate product value into a measurable objective with a naive comparator and deployment population.
- **Avoid misdiagnosis:** Optimizing an available label can answer a different question from the real decision; missing follow-up is not a negative outcome.
- **Check the result:** Walk one positive, negative and censored example through feature availability, prediction and eventual label eligibility.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [ML data worked example](../../references/examples/ml-data.md).
- The task specifically involves recommender, ranking metrics, retrieval ranking, ml adoption; load only the matching method: [Retrieval, ranking and recommendation evaluation](../../references/methods/recommender-systems.md).

## Decision branches

- **When label timing or intervention changes the observed outcome:** Separate prediction from causal/intervention claims and identify the missing observation process.

## Deliver and verify

- Modeling brief and task card with row grain, prediction moment, outcome horizon, action, error costs, success metrics, eligibility/exclusions, deployment assumptions and unresolved policy choices.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Target and prediction time are unambiguous; a proxy label's mismatch with the real objective is explicit.

## Stop and recover

- Do not force an ML solution when deterministic rules suffice or invent business error costs without input.

## Example requests

- **Normal (plan):** Frame churn prediction 30 days before cancellation, including unit and label horizon.
- **Edge (plan):** Frame failure prediction for machines with delayed maintenance labels.
- **Blocked (inspect):** Define the task without business error costs; keep threshold selection undecided.
