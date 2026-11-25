---
name: ml-labels
description: "Inspect label definitions, noise, disagreement, and missing outcomes. Use for label construction and annotation quality; ml-leakage checks prediction-time information flow."
---

# ml-labels

Inspect label definitions, noise, disagreement, and missing outcomes.

## Choose this workflow

Use for label construction and annotation quality; ml-leakage checks prediction-time information flow.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [ML data methods](../../references/packs/ml-data.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; label definitions, annotation/outcome sources, timing, and permitted samples.

**Pack prerequisites:** Task definition, dataset identity, field semantics, entity/time keys, and permission to inspect bounded data. Record prediction moment, label horizon, sampling, and provenance. Preserve held-out evaluation boundaries; no data upload, label alteration, or feature fitting across splits implicitly.

- **Infer from evidence:** Read prediction moment, label horizon, entity/time keys, split policy and dataset provenance from the task and manifests.
- **Reasonable default:** Use explicit synthetic examples for design when raw data is unavailable; do not infer missing labels or fit preprocessing across held-out boundaries.
- **Ask only when needed:** Ask when unresolved label timing, grouping or target semantics would change the split/features; do not demand a full dataset to explain the method.

Declared evidence requirements: `data.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Label consistency, noise, disagreement, censoring, and missing outcomes.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Trace each label's source, construction, event horizon and maturity.
2. Compare annotations and outcomes, distinguishing true negatives, unobserved outcomes, contradictory annotations and policy ambiguity.
3. Propose adjudication and quality checks.

## Technical method

- **Inspect:** Read labeling policy, event identity, annotator agreement, outcome window and availability timestamps.
- **Method:** Separate absent, unresolved and negative labels; trace a disagreement to policy or observation error before changing it.
- **Avoid misdiagnosis:** Majority vote can erase systematic ambiguity; labels recorded after prediction may be valid outcomes but unavailable for historical fitting.
- **Check the result:** Hand-check boundary examples, censored cases and disagreement resolution; report which historical training rows were label-eligible.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [ML data worked example](../../references/examples/ml-data.md).


## Decision branches

- **When annotators disagree on an ambiguous definition:** Preserve disagreement, clarify policy and adjudicate within scope rather than silently majority-voting it away.

## Deliver and verify

- Label audit with the label definition, maturity/coverage checks, concrete patterns with rates and denominators, reproducible disagreement examples and corrective options.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Unobserved outcomes are not automatically negative; conflicting annotations are tracked rather than silently overwritten.

## Stop and recover

- Relabeling requires explicit policy and scope. Avoid exposing sensitive examples or claiming a single annotator is ground truth without justification.

## Example requests

- **Normal (inspect):** Audit how missing outcome follow-up and annotation disagreement affect labels.
- **Edge (inspect):** Audit labels when missing follow-up was encoded as no failure.
- **Blocked (inspect):** Assess annotation policy without identifiable raw examples or relabeling permission.
