---
name: ml-calibrate
description: "Assess predicted probabilities against observed outcomes. Use to assess or fit probability calibration; ml-threshold maps scores to decisions."
---

# ml-calibrate

Assess predicted probabilities against observed outcomes.

## Choose this workflow

Use to assess or fit probability calibration; ml-threshold maps scores to decisions.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [ML evaluation methods](../../references/packs/ml-evaluation.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; predicted probabilities, labels, sampling/prevalence context, and intended use. Apply to fit a calibrator on a permitted split when requested.

**Pack prerequisites:** Frozen model/artifact, evaluation dataset identity, labels where needed, metric definitions, and task/operating context. Report sample counts and uncertainty appropriate to dependencies; avoid repeated test-set tuning. Exploratory findings need fresh confirmation before strong generalization claims.

- **Infer from evidence:** Read frozen model/data identities, metric definitions, denominators and supplied predictions; separate validation from test use.
- **Reasonable default:** Compute only supported metrics on permitted samples and label missing labels or subgroup coverage as unknown.
- **Ask only when needed:** Ask when the operating cost/threshold or population changes the evaluation decision; do not fabricate labels to avoid a question.

Declared evidence requirements: `ml.artifacts`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Probability reliability assessment; fitting a calibrator uses a separate held-out calibration protocol in apply mode.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: make the requested changes or execute the requested operation within its resolved target and limits. Local preparation does not authorize live, remote, destructive or paid actions; existing explicit session authorization still applies.

## Execute

1. Check probability semantics, then inspect reliability by range and cohort with proper scoring measures.
2. Fit any calibrator on permitted data separate from final evaluation, and compare it by cohort on untouched evaluation data.

## Technical method

- **Inspect:** Inspect probability outputs, class definition, prevalence, selection split and calibration metric/binning.
- **Method:** Fit calibration on permitted selection data and evaluate reliability on separate data; compare proper scoring rules and reliability curves.
- **Avoid misdiagnosis:** Ranking quality does not imply probability accuracy; coarse bins or shifted prevalence can conceal miscalibration.
- **Check the result:** Check perfect, constant and confidently wrong synthetic predictions, then evaluate held-out calibration with sample support per region.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [ML evaluation worked example](../../references/examples/ml-evaluation.md).


## Decision branches

- **When prevalence or sampling changed since calibration:** Assess transfer assumptions and recalibration evidence without claiming ranking quality proves reliable probabilities.

## Deliver and verify

- Calibration report or calibrated artifact with split provenance, the calibration protocol, reliability evidence and an independent comparison.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Good ranking is not mistaken for calibrated probability; fitting and evaluating a calibrator on identical records is rejected.

## Stop and recover

- Small samples and prevalence shift limit conclusions. Do not alter deployed probabilities without a rollout request.

## Example requests

- **Normal (inspect):** Assess probability calibration from the supplied held-out scores and outcomes.
- **Edge (apply):** Calibrate a model trained on oversampled positives.
- **Blocked (inspect):** Review probability outputs with too few outcomes to fit a reliable calibrator.
