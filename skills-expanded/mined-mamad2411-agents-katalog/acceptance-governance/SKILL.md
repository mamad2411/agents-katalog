---
name: acceptance-governance
description: Use when reviewing completed implementation, design, test, or release artifacts against acceptance criteria and producing severity-tagged findings with explicit sign-off disposition.
---

# Acceptance Governance

## Specialization

Evaluate artifacts across any discipline against the active acceptance criteria for that phase, produce a severity-tagged finding set, and record an explicit sign-off disposition. This skill is the shared review contract that makes cross-discipline review outputs comparable and auditable.

This skill does not perform the primary discipline review — it standardises the intake, checklist application, finding structure, and disposition output that all discipline reviews must produce.

## Trigger Conditions

- A Review lane task must produce a sign-off or rejection decision.
- Findings from multiple disciplines need a consistent severity taxonomy and disposition format.
- A release, design, or implementation review must generate durable evidence of acceptance or deferral.
- An existing review has informal findings that need to be hardened into a structured disposition.

## Inputs

- Artifact under review (code, design doc, ADR, test evidence, release bundle, or configuration artifact).
- Acceptance criteria for the artifact: plan-level, spec-level, or stated inline.
- Discipline context: Architecture, Engineering, Security, Performance, UX, Product, or Governance.
- Phase context: Design, Implementation, Test, or Release.
- Originating plan or workstream ID for traceability.

## Required Outputs

| Output | Description |
|---|---|
| Checklist result | Discipline-specific checklist applied against the artifact. Each item: Pass / Fail / N/A with brief evidence note. |
| Finding set | Severity-tagged findings: Critical / Major / Minor / Advisory. Each finding includes location, description, and recommended action. |
| Evidence summary | One-paragraph description of what was reviewed, what evidence was examined, and what was not in scope. |
| Disposition | Explicit outcome: `Approved` / `Approved with conditions` / `Rejected`. Conditions must be listed. |
| Follow-up list | Any deferred findings that do not block sign-off, each with an owner and target resolution date. |

## Workflow

1. Confirm the artifact, acceptance criteria, discipline, and phase are all identified before starting.
2. Select the discipline checklist for the context (see checklist reference below).
3. Apply the checklist line by line. Mark each item Pass / Fail / N/A and note the evidence examined.
4. Classify each Fail item by severity: Critical (blocks sign-off), Major (conditional), Minor (advisory), or Advisory (note only).
5. Write the finding set. Each finding must include: severity, location or artifact section, description, and recommended action.
6. Write the evidence summary: what was reviewed, what was examined, what was out of scope.
7. Record the disposition: Approved, Approved with conditions (list conditions), or Rejected (list blocking items).
8. Populate the follow-up list with any non-blocking items needing resolution.
9. Attach the originating plan or workstream ID to the output artifact.

## Discipline Checklist Reference

| Discipline | Core checklist areas |
|---|---|
| Architecture | Boundary conformance, coupling risk, ADR coverage, change safety |
| Engineering | Standards conformance, test coverage, plan fidelity, security baseline |
| Security | Control implementation, validation points, exposure surface, secrets handling |
| Performance | Budget compliance, regression risk, instrumentation coverage |
| UX | Accessibility baseline (WCAG AA), fidelity to approved design, journey completeness |
| Product Management | Acceptance criteria coverage, value delivery, scope conformance |
| Governance | Policy conformance, evidence completeness, audit trail integrity |

## Done Criteria

- Checklist result covers every applicable line item with a Pass / Fail / N/A entry.
- Every Fail item appears in the finding set with a severity tag.
- Evidence summary exists and identifies scope boundaries.
- Disposition is explicit: one of Approved, Approved with conditions, or Rejected.
- Follow-up list is present (may be empty if no non-blocking items exist).
- Originating plan or workstream ID is recorded on the output.

## Guardrails

- Do not record Approved disposition when any Critical finding is open.
- Do not omit findings to reach a cleaner disposition — all Fail items must be recorded.
- Do not merge findings from separate disciplines into a single checklist pass without labelling discipline context.

## References

- Related skills: `code-reviewer`, `manual-code-reviewer`, `request-code-review`, `remediate-review`, `test-design-review`, `release-readiness`
