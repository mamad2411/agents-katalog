---
name: web-ux-forms-conversion
description: Use when implementing or reviewing web UX form and conversion outcomes with deterministic completion-friction checks, validation quality gates, and evidence-backed release recommendations.
---

# Web UX Forms Conversion

## Specialization

Use this skill to produce expert-level, agent-usable form and conversion outcomes for web flows.

## Objective

Increase completion quality by measuring form friction, validation behavior, and abandonment points with deterministic release decisions.

## Trigger Conditions

- A release affects form structure, validation rules, or conversion-critical steps.
- Teams need objective evidence for completion friction and drop-off causes.
- UX quality gates require conversion-risk disposition.

## Scope Boundaries

In scope:

- Form field clarity, validation timing, error recovery, progressive disclosure, and submit feedback.
- Completion, error, recovery, and drop-off evidence.

Out of scope:

- General IA or navigation audits outside form flows.

## Inputs

- In-scope form journeys and business-critical tasks.
- Validation rules and field specifications.
- Baseline completion and abandonment data when available.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Form-conversion findings with severity and user-impact rationale.
- Conversion evidence matrix with completion, error, recovery, and drop-off rates.
- Prioritized remediation backlog for blocking and high-impact issues.
- Final recommendation: `go`, `go-with-exceptions`, or `no-go`.

## Deterministic Workflow

1. Lock in-scope forms, steps, and success criteria.
2. Define measurable conversion thresholds and validation quality gates.
3. Evaluate field flow, error handling, and submit feedback behavior.
4. Capture completion, error, recovery, and abandonment signals.
5. Classify findings by severity and conversion risk.
6. Assign remediation disposition with owner and due date.
7. Re-run key conversion paths after remediation.
8. Publish final recommendation and evidence paths.

## Conversion Gate Checklist

- [ ] Required fields and labels are explicit and minimally burdensome.
- [ ] Validation timing avoids premature interruption and silent failures.
- [ ] Error messages provide direct recovery instructions.
- [ ] Submit state feedback is visible and unambiguous.
- [ ] High and critical conversion blockers are resolved or deferred with owner and due date.

## Severity Model

- Critical: core conversion path cannot be completed.
- High: completion requires repeated retries or is likely abandoned.
- Medium: measurable friction with recoverable path.
- Low: minor UX polish opportunities.

## Evidence Contract

- `.docs/changes/<workstream-id>/forms-conversion-findings.md`
- `.docs/changes/<workstream-id>/forms-conversion-matrix.md`
- `.docs/changes/<workstream-id>/release-recommendation.md`

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).

## Pragmatic Stop Rule

Stop when all in-scope form paths are measured, high and critical issues are resolved or dispositioned with owner and due date, and a final recommendation is published.

## Done Criteria

- Required outputs are complete and linked.
- Source ledger is current.
- Final recommendation is explicit and evidence-backed.

