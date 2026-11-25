---
name: ml-imbalance
description: "Evaluate sampling, weighting, metrics, and thresholds for rare outcomes. Use when rare outcomes affect metrics or training; ml-threshold selects operational decisions."
---

# ml-imbalance

Evaluate sampling, weighting, metrics, and thresholds for rare outcomes.

## Choose this workflow

Use when rare outcomes affect metrics or training; ml-threshold selects operational decisions.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [ML data methods](../../references/packs/ml-data.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan; prevalence, class definitions, error costs/capacity, and split protocol.

**Pack prerequisites:** Task definition, dataset identity, field semantics, entity/time keys, and permission to inspect bounded data. Record prediction moment, label horizon, sampling, and provenance. Preserve held-out evaluation boundaries; no data upload, label alteration, or feature fitting across splits implicitly.

- **Infer from evidence:** Read prediction moment, label horizon, entity/time keys, split policy and dataset provenance from the task and manifests.
- **Reasonable default:** Use explicit synthetic examples for design when raw data is unavailable; do not infer missing labels or fit preprocessing across held-out boundaries.
- **Ask only when needed:** Ask when unresolved label timing, grouping or target semantics would change the split/features; do not demand a full dataset to explain the method.

Declared evidence requirements: `data.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Sampling/weighting, evaluation, and operating-point options for rare outcomes.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Compute baseline prevalence, naive baselines and class counts by split.
2. Choose task-relevant precision/recall measures, and compare resampling or weighting only within training folds.
3. Assess how deployment prevalence changes the metrics and the threshold.

## Technical method

- **Inspect:** Measure prevalence, minority counts per split, error costs and operational capacity.
- **Method:** Apply resampling or weighting only within training folds; evaluate ranking, precision/recall and probability interpretation separately.
- **Avoid misdiagnosis:** Accuracy can hide zero minority recall; resampling changes prevalence and can distort uncorrected probabilities.
- **Check the result:** Compare with an appropriate naive baseline, retain minority denominators and verify thresholds on untouched selection/evaluation data.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [ML data worked example](../../references/examples/ml-data.md).


## Decision branches

- **When prevalence differs between sampled training and deployment:** Separate learned ranking from probability calibration and expected operational workload.

## Deliver and verify

- Imbalance strategy with baselines, per-class denominators, the resampling protocol, bounded experiments, threshold considerations and uncertainty limits.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A high-accuracy all-negative model is not accepted as useful; resampled training prevalence is not confused with deployed probability calibration.

## Stop and recover

- Do not synthesize across validation/test boundaries or invent business tradeoffs. Low positive counts require uncertainty disclosure.

## Example requests

- **Normal (plan):** Compare weighting and metrics for rare fraud with limited review capacity.
- **Edge (plan):** Compare a high-accuracy all-negative baseline against a rare-event model.
- **Blocked (inspect):** Assess imbalance with few positives; do not invent stable confidence or business costs.
