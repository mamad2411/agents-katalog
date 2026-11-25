---
name: web-ux-quality-gate
description: Use when one deterministic intake must coordinate web UX quality dimensions and produce a unified release recommendation artifact.
---

# Web UX Quality Gate

## Specialization

Use this skill to orchestrate one deterministic, evidence-first web UX quality gate across core and extended dimensions.

This skill is specialized for intake, phase ownership, and unified decision synthesis. It does not replace domain execution guidance for each dimension, and it does not perform product code implementation.

## Objective

Produce one release-ready web UX recommendation from a single intake by combining severity-ranked evidence from all in-scope UX quality dimensions.

## Trigger Conditions

- A release-bound web change requires one consolidated UX quality decision.
- Teams need one intake instead of separate review workflows by dimension.
- UX evidence exists or must be collected across in-scope UX quality dimensions before sign-off.
- Governance requires explicit ownership mapping and auditable pass/fail outcomes.

## Scope Boundaries

In scope:

- Deterministic intake and phase planning for core and extended UX quality dimensions.
- Phase-output ownership matrix with exactly one owner per required output.
- Unified recommendation synthesis with explicit residual-risk accounting.

Out of scope:

- Implementing remediation code.
- Running unrelated backend, DBA, or architecture workflows.
- Replacing domain-specific deep-dive execution guidance.

## Inputs

- Change objective and in-scope journeys.
- Target environments and devices.
- Release timeline and threshold policy.
- Known risks, waivers, and prior findings.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Intake contract with objective, boundaries, and required outputs.
- Phase-output ownership matrix for all in-scope dimensions.
- Dimension evidence index linking all produced artifacts.
- Unified release recommendation artifact with `go`, `go-with-exceptions`, or `no-go` disposition.
- Rejected-candidate table with reason codes for excluded scope or capabilities.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Orchestrate one journey quality gate | One complete intake and one unified recommendation artifact |
| L2 Delivery | Orchestrate core flow set | All in-scope journeys have evidence in all selected dimensions |
| L3 Hardening | Enforce release-grade governance | No unresolved high/critical findings without owner and due date |
| L4 Expert Standardization | Build reusable quality-gate operating model | Reusable intake schema, ownership matrix, and decision rubric are documented |

## Deterministic Workflow

1. Lock intake scope: journeys, environments, thresholds, and release window.
2. Build phase plan with one owned phase per selected dimension from the capability catalog.
3. Create ownership matrix mapping each required output to exactly one phase owner.
4. Execute or ingest dimension evidence and verify artifact completeness.
5. Normalize severity and risk language across dimensions.
6. Build consolidated findings table with impact, owner, and disposition.
7. Identify conflicts where one dimension passes but another blocks release.
8. Resolve conflicts using policy thresholds and explicit exception handling.
9. Produce one unified recommendation: `go`, `go-with-exceptions`, or `no-go`.
10. Publish final artifact and closure status with all linked evidence paths.

## Phase-Output Ownership Matrix Template

| Required Output | Owning Phase | Evidence Artifact |
|---|---|---|
| Accessibility findings and disposition | Accessibility | `.docs/changes/<workstream-id>/accessibility-findings.md` |
| Usability task evidence and disposition | Usability | `.docs/changes/<workstream-id>/task-evidence-matrix.md` |
| Performance and abandonment-risk evidence | Performance | `.docs/changes/<workstream-id>/performance-evidence-matrix.md` |
| Motion and animation findings and disposition | Motion Animation | `.docs/changes/<workstream-id>/motion-animation-findings.md` |
| Responsive design findings and disposition | Responsive Design | `.docs/changes/<workstream-id>/responsive-design-findings.md` |
| Notification and alert findings and disposition | Notification Alerts | `.docs/changes/<workstream-id>/notification-alert-findings.md` |
| Content clarity findings and disposition | Content Clarity | `.docs/changes/<workstream-id>/content-clarity-findings.md` |
| Information architecture findings and disposition | Information Architecture | `.docs/changes/<workstream-id>/ia-findings.md` |
| Forms conversion findings and disposition | Forms Conversion | `.docs/changes/<workstream-id>/forms-conversion-findings.md` |
| Experimentation evidence and decision disposition | Experimentation Evidence | `.docs/changes/<workstream-id>/experiment-decision-log.md` |
| Telemetry and instrumentation quality disposition | Telemetry Instrumentation | `.docs/changes/<workstream-id>/telemetry-quality-findings.md` |
| Localization findings and disposition | Localization | `.docs/changes/<workstream-id>/localization-findings.md` |
| Visual consistency findings and disposition | Visual Consistency | `.docs/changes/<workstream-id>/visual-consistency-findings.md` |
| Trust and risk-signal findings and disposition | Trust Risk Signals | `.docs/changes/<workstream-id>/trust-risk-findings.md` |
| Privacy and consent findings and disposition | Privacy Consent | `.docs/changes/<workstream-id>/privacy-consent-findings.md` |
| Feedback-state findings and disposition | Feedback Status | `.docs/changes/<workstream-id>/feedback-status-findings.md` |
| Account and identity-flow findings and disposition | Account Identity Flows | `.docs/changes/<workstream-id>/account-identity-findings.md` |
| Data-dense interface findings and disposition | Data Dense Interfaces | `.docs/changes/<workstream-id>/data-dense-findings.md` |
| Onboarding and progressive-disclosure findings and disposition | Onboarding Progressive Disclosure | `.docs/changes/<workstream-id>/onboarding-findings.md` |
| Offline and resilience findings and disposition | Offline Resilience | `.docs/changes/<workstream-id>/offline-resilience-findings.md` |
| Supportability and self-service findings and disposition | Supportability Self Service | `.docs/changes/<workstream-id>/supportability-findings.md` |
| Consolidated recommendation and residual risk | Synthesis | `.docs/changes/<workstream-id>/ux-quality-gate-recommendation.md` |

## Capability Catalog

Use one or more of these dimensions based on change scope:

- Accessibility
- Usability
- Performance
- Motion Animation
- Responsive Design
- Notification Alerts
- Content Clarity
- Information Architecture
- Forms Conversion
- Experimentation Evidence
- Telemetry Instrumentation
- Localization
- Visual Consistency
- Trust Risk Signals
- Privacy Consent
- Feedback Status
- Account Identity Flows
- Data Dense Interfaces
- Onboarding Progressive Disclosure
- Offline Resilience
- Supportability Self Service

## Unified Decision Rules

- `go`: no unresolved critical findings and no unresolved high findings without approved exception.
- `go-with-exceptions`: limited high findings remain with named owner, due date, and accepted risk rationale.
- `no-go`: unresolved critical findings, or unresolved high findings without approved exception controls.

## Evidence Contract

Required minimum artifacts:

- `.docs/changes/<workstream-id>/accessibility-findings.md`
- `.docs/changes/<workstream-id>/task-evidence-matrix.md`
- `.docs/changes/<workstream-id>/performance-evidence-matrix.md`
- `.docs/changes/<workstream-id>/ux-quality-gate-recommendation.md`

Additional artifacts are required when those dimensions are in scope:

- `.docs/changes/<workstream-id>/content-clarity-findings.md`
- `.docs/changes/<workstream-id>/ia-findings.md`
- `.docs/changes/<workstream-id>/forms-conversion-findings.md`
- `.docs/changes/<workstream-id>/experiment-decision-log.md`
- `.docs/changes/<workstream-id>/telemetry-quality-findings.md`
- `.docs/changes/<workstream-id>/localization-findings.md`
- `.docs/changes/<workstream-id>/visual-consistency-findings.md`
- `.docs/changes/<workstream-id>/trust-risk-findings.md`
- `.docs/changes/<workstream-id>/privacy-consent-findings.md`
- `.docs/changes/<workstream-id>/motion-animation-findings.md`
- `.docs/changes/<workstream-id>/responsive-design-findings.md`
- `.docs/changes/<workstream-id>/notification-alert-findings.md`
- `.docs/changes/<workstream-id>/feedback-status-findings.md`
- `.docs/changes/<workstream-id>/account-identity-findings.md`
- `.docs/changes/<workstream-id>/data-dense-findings.md`
- `.docs/changes/<workstream-id>/onboarding-findings.md`
- `.docs/changes/<workstream-id>/offline-resilience-findings.md`
- `.docs/changes/<workstream-id>/supportability-findings.md`

Recommended synthesis template:

- [unified-release-recommendation-template.md](./references/unified-release-recommendation-template.md)

Worked example:

- [ux-quality-gate-recommendation.md](../../../.docs/changes/web-ux-quality-gate-example/ux-quality-gate-recommendation.md)
- [ux-quality-gate-recommendation.md](../../../.docs/changes/web-ux-quality-gate-full-example/ux-quality-gate-recommendation.md)

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| One intake across all selected dimensions | Deterministic Workflow steps 1 to 3 |
| Explicit ownership and no ambiguity | Phase-Output Ownership Matrix Template |
| Unified recommendation artifact | Required Outputs + Evidence Contract |
| Deterministic release decision rules | Unified Decision Rules |
| Auditable residual-risk handling | Workflow steps 6 to 10 |
| Source freshness governance | Source Governance Summary + Source Ledger |

## Reasoning Package

Assumptions:

- Dimension evidence can be produced within release timeline.
- Decision thresholds are known before synthesis begins.

Trade-offs:

- One umbrella decision improves consistency but requires stronger coordination.
- Strict blocking rules lower risk but can increase release friction.

Open blockers:

- Missing evidence in any dimension prevents unified recommendation.
- Inconsistent severity language across dimensions can delay synthesis.

Recommendation:

- Use L3 for release-bound work and L4 when institutionalizing a standard operating model.

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).
- Freshness threshold default is 30 days for active source checks.

## Pragmatic Stop Rule

Stop when the ownership matrix has no unowned outputs, all required artifacts are present, and one explicit release recommendation is published with residual-risk accountability.

## Anti-Patterns

- Running isolated dimension checks without unified synthesis.
- Publishing recommendation without ownership matrix validation.
- Allowing unresolved high or critical findings without owner and due date.
- Treating missing evidence as implicit pass.

## Done Criteria

- Trigger conditions are satisfied.
- Required outputs are complete and linked.
- Ownership matrix is complete with single-owner mapping per required output.
- Source ledger is current for the evaluation cycle.
- Final recommendation is explicit, evidence-backed, and auditable.

