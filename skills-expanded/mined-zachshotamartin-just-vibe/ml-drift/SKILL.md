---
name: ml-drift
description: "Design checks for input or prediction-distribution changes. Use for observed input/prediction distribution change; ml-evaluate requires outcomes to establish quality, and ml-parity or ml-leakage explain an offline-versus-production gap that is not population change; ml-monitor implements production drift and quality monitors and alert wiring."
---

# ml-drift

Design checks for input or prediction-distribution changes.

## Choose this workflow

Use for observed input/prediction distribution change; ml-evaluate requires outcomes to establish quality, and ml-parity or ml-leakage explain an offline-versus-production gap that is not population change; ml-monitor implements production drift and quality monitors and alert wiring.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [ML deployment methods](../../references/packs/ml-deployment.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan; reference/current data or prediction windows, features, seasonality, and sensitivity requirements.

**Pack prerequisites:** Versioned model and preprocessing artifacts, input/output schema, runtime/dependencies, operating targets, and authorized environment. Validate artifact trust before loading formats that can execute code. Packaging or writing monitoring configuration does not deploy a model or enable a hosted service.

- **Infer from evidence:** Read artifact format/trust, preprocessing schema, serving runtime, compatibility and existing rollout controls.
- **Reasonable default:** Prepare packaging/configuration and isolated checks without treating them as a live deployment.
- **Ask only when needed:** Resolve the target, rollback compatibility and operating limits before rollout or load generation; missing production access does not block packaging.

Declared evidence requirements: `ml.artifacts`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Distribution-change detection and investigation; no automatic retraining.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Align schemas, sampling and seasonal windows of the baseline and current data.
2. Choose meaningful per-feature and aggregate checks, and compare effect sizes and support changes in light of sample size.
3. Separate data-pipeline changes from population changes, and define follow-up on signals.

## Technical method

- **Inspect:** Establish a reference population, feature semantics, seasonality, sample sizes and missing-data behavior.
- **Method:** Monitor meaningful distribution changes with declared windows and thresholds; separate drift alerts from proven quality degradation.
- **Avoid misdiagnosis:** A small p-value on a huge sample can flag irrelevant change, while missing labels prevent conclusions about accuracy.
- **Check the result:** Inject a known distribution shift and a stable control, then check alert volume, cohort mix and delayed-label follow-up.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [ML deployment worked example](../../references/examples/ml-deployment.md).


## Decision branches

- **When drift is statistically significant but outcomes are unavailable:** Report a monitoring signal and follow-up, not confirmed accuracy degradation.

## Deliver and verify

- Drift protocol or report with baseline/current identities, shift measures and thresholds, sample sizes, uncertainty and the next evidence needed.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A changed categorical support is detected; a statistically significant tiny shift is not automatically called model failure.

## Stop and recover

- Drift is not proof of accuracy degradation without outcome evidence. Baseline refresh requires explicit policy, not silent adaptation.

## Example requests

- **Normal (plan):** Plan distribution checks that account for seasonality and sample size.
- **Edge (plan):** Investigate a new categorical value and a seasonal traffic shift.
- **Blocked (inspect):** Assess drift from aggregates without inferring model failure or silently refreshing the baseline.
