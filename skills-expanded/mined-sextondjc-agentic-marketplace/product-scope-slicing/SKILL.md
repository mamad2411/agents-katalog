---
name: product-scope-slicing
description: Use when converting product intent, outcome statements, or discovery findings into prioritised, acceptance-ready delivery slices and release candidates.
---

# Product Scope Slicing

## Specialization

Convert product intent, user outcome statements, or discovery findings into a set of prioritised, acceptance-ready delivery slices. Each slice has a defined scope boundary, explicit acceptance criteria, and a release candidate assignment.

This skill bridges the gap between product discovery and delivery execution. It does not own discovery (that is `analysis-execution`) or backlog grooming tooling — it produces the structured slice artefacts that engineering, design, and release planning can act on without ambiguity.

## Trigger Conditions

- Product intent or outcome statements exist but have not been broken into delivery slices.
- A roadmap theme or epic needs to be decomposed into prioritised, acceptance-ready work items.
- Scope creep, unclear acceptance criteria, or ambiguous MVP boundaries are delaying delivery.
- A release candidate needs a defined scope boundary and stakeholder-confirmed acceptance baseline.
- Scope arbitration during implementation requires a structured decision record.

## Inputs

- Product intent inputs: outcome statements, opportunity framing, user problem descriptions, or PRD excerpts.
- Known constraints: delivery capacity, timeline, technical boundaries, compliance requirements.
- Discovery outputs: user research findings, stakeholder priorities, value hypotheses.
- Existing slice backlog (if iterating on a prior decomposition).
- Originating plan or workstream ID for traceability.

## Required Outputs

| Output | Description |
|---|---|
| Slice registry | Ordered list of delivery slices. Each slice: slice ID, description, scope boundary (in/out), primary value hypothesis, and release candidate assignment. |
| Acceptance criteria | Per-slice acceptance statements: testable, outcome-oriented, and unambiguous. Minimum one per slice. |
| Priority rationale | One-line rationale per slice explaining its position in the sequence relative to risk, value, and dependency order. |
| Deferral log | Items considered but deferred out of scope, each with a deferral reason. |
| Release candidate map | Which slices compose each release candidate, including the minimum viable set and any conditional additions. |

## Workflow

1. Collect and normalise all product inputs into a single intent statement. Confirm the primary outcome being targeted.
2. Identify constraints: capacity, timeline, technical, and compliance boundaries that bound the slicing space.
3. Decompose the intent into candidate slices. Each candidate must be independently deliverable and testable.
4. Apply priority ordering: sequence slices by risk reduction (de-risk first), value density (highest impact per effort), and dependency order.
5. Write acceptance criteria for each slice. Criteria must be testable and outcome-oriented — not implementation-prescriptive.
6. Populate the deferral log: record any candidates that were rejected or deferred and the reason.
7. Map slices to release candidates: identify the minimum viable set and any conditional additions per release.
8. Record the originating plan or workstream ID on all output artifacts.

## Slice Sizing Rules

- A slice must be deliverable without depending on another slice in the same release candidate.
- A slice that cannot have acceptance criteria written for it must be further decomposed.
- If a slice can only be accepted after another slice is accepted, it is a dependency — split or sequence accordingly.

## Done Criteria

- Slice registry exists with scope boundaries and release assignments for every slice.
- Every slice has at least one acceptance criterion.
- Priority rationale is recorded for each slice's position.
- Deferral log is present (may be empty if nothing was deferred).
- Release candidate map is present with a defined minimum viable set.
- Originating plan or workstream ID is on the output.

## Guardrails

- Do not assign a slice to a release candidate without acceptance criteria — incomplete slices must remain in the backlog.
- Do not combine slices to obscure scope ambiguity — ambiguous scope must be resolved before slicing, not after.
- Scope changes during implementation must be recorded as explicit decisions referencing the originating slice ID before implementation diverges.

## References

- Related skills: `analysis-execution`, `writing-plans`, `prd-generator`, `delivery-status-grid`, `acceptance-governance`
