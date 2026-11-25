---
name: ml-leakage
description: "Find target leakage, temporal leakage, and split contamination. Use to audit demonstrated information leakage; ml-split designs the evaluation protocol, and ml-parity or ml-drift own train/serve skew and population change."
---

# ml-leakage

Find target leakage, temporal leakage, and split contamination.

## Choose this workflow

Use to audit demonstrated information leakage; ml-split designs the evaluation protocol, and ml-parity or ml-drift own train/serve skew and population change.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [ML data methods](../../references/packs/ml-data.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; task/prediction moment, features, preprocessing, labels, and split lineage.

**Pack prerequisites:** Task definition, dataset identity, field semantics, entity/time keys, and permission to inspect bounded data. Record prediction moment, label horizon, sampling, and provenance. Preserve held-out evaluation boundaries; no data upload, label alteration, or feature fitting across splits implicitly.

- **Infer from evidence:** Read prediction moment, label horizon, entity/time keys, split policy and dataset provenance from the task and manifests.
- **Reasonable default:** Use explicit synthetic examples for design when raw data is unavailable; do not infer missing labels or fit preprocessing across held-out boundaries.
- **Ask only when needed:** Ask when unresolved label timing, grouping or target semantics would change the split/features; do not demand a full dataset to explain the method.

Declared evidence requirements: `data.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Target proxies, future information, cross-split fitting, duplicates, and entity contamination.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Identify the prediction moment, label horizon, feature availability, split membership and intended deployment population from supplied evidence. Mark missing definitions as unknown.
2. Trace suspicious features to when their values could actually have been available. Distinguish future-derived values from valid point-in-time historical features.
3. Inspect preprocessing fit/transform boundaries when code or fit records exist. Their absence means unverified, not proof of correct or incorrect fitting.
4. For each finding record the exact observed rows or source paths, the conclusion those observations support, and any assumptions needed for a stronger conclusion. Separate confirmed defects, conditional risks and missing evidence in the report.
5. Quantify entity, interval and outcome-horizon overlap. Do not infer identical raw measurements or a shared outcome event from metadata alone. Determine group separation from whether deployment targets known entities, new entities or new groups.
6. Check label maturity against the simulated model-fit and prediction times. State the historical-deployment assumption when applying temporal cutoffs or an embargo; choose gaps from actual availability and overlap instead of a universal duration.
7. Before delivering, check every claim labeled proven against its cited evidence. Correct unsupported absolutes, including assertions that all scores are invalid or a split is always wrong. Identify which scores would be affected under which assumptions, and require re-evaluation after confirmed leakage is corrected.
8. Build a compact evidence ledger: field or row, availability time, prediction/fit time, observed violation, affected score and assumptions; keep overlap metadata separate from shared measurements or events.

## Technical method

- **Inspect:** Trace suspicious features, fit transforms, revisions, event time, availability time and split membership.
- **Method:** Resolve the latest visible record version before applying historical windows; fit learned transforms within each training fold.
- **Avoid misdiagnosis:** Correlation or overlapping metadata alone does not prove leakage; filtering versions before selecting the visible revision can resurrect stale data.
- **Check the result:** Test late correction, boundary timestamps, duplicate versions and labels unavailable at fit time; state precisely which evaluation is invalidated.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [ML data worked example](../../references/examples/ml-data.md).


## Decision branches

- **When no raw measurements, event IDs or fitting history establish dependence:** Report conditional risk or unknown, not proven shared events, mandatory gap length or universal score invalidity.
- **When the symptom is an offline-versus-production gap:** Run one discriminating check per cause before concluding and report which causes each check excludes: recompute offline metrics on production-logged features for the same rows (skew, ml-parity), compare evaluation-window and production feature and prediction distributions (drift, ml-drift), and audit feature availability and split lineage (leakage, ml-leakage).

## Deliver and verify

- Evidence-backed leakage audit and finding ledger separating confirmed defects, conditional risks and unknowns; each finding names the supporting rows or source, assumptions, the bounded affected evaluation and the correction or missing evidence.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Future-only features and immature training labels are flagged against the stated prediction/fit times; cross-split preprocessing fitting is detected only when source or fit history establishes it.
- Metadata-only overlap is quantified without asserting identical sensor values or a shared failure event. Group separation is conditional on the intended deployment population.
- Missing labels remain unknown outcomes, unavailable pipeline evidence remains unverified, and score invalidation is limited to affected evaluation assumptions rather than invented results.

## Stop and recover

- Do not claim absence of leakage when provenance is missing. Remediation must invalidate affected scores rather than preserve misleading results.

## Example requests

- **Normal (inspect):** Audit churn features for values unavailable 30 days before cancellation.
- **Edge (inspect):** Audit overlapping windows whose metadata does not prove shared sensor values or outcome events.
- **Blocked (inspect):** Review lineage with missing preprocessing code and event IDs; leave unsupported claims unknown.
