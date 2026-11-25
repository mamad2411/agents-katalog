---
name: web-ux-content-clarity
description: Use when implementing or reviewing web UX content clarity outcomes with deterministic microcopy checks, error-message quality gates, and evidence-backed release recommendations.
---

# Web UX Content Clarity

## Specialization

Use this skill to produce expert-level, agent-usable content clarity outcomes for web interfaces, including labels, helper text, instructional copy, and error messages.

## Objective

Reduce comprehension friction by converting content quality checks into measurable findings, remediation priorities, and explicit release recommendations.

## Trigger Conditions

- A web flow includes new or changed user-facing copy.
- Teams need objective checks for label clarity, action language, and error-message quality.
- UX quality gates require explicit content clarity evidence before sign-off.

## Scope Boundaries

In scope:

- Labels, button text, helper text, validation messages, confirmation text, and empty-state copy.
- Readability, ambiguity, tone consistency, and action clarity checks.
- Severity-ranked findings and remediation disposition.

Out of scope:

- Localization completeness audits.
- Visual redesign decisions without content impact.

## Inputs

- In-scope flows and screens.
- Intended user tasks and success criteria.
- Content style guidance and terminology policy.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Content clarity findings with severity and user-impact rationale.
- Copy quality checklist outcome per in-scope flow.
- Prioritized remediation backlog for high-impact content issues.
- Final recommendation: `go`, `go-with-exceptions`, or `no-go`.

## Deterministic Workflow

1. Lock in-scope flows and copy surfaces.
2. Define pass/fail criteria for clarity, brevity, specificity, and actionability.
3. Evaluate each content surface against criteria and task intent.
4. Classify findings by severity and task impact.
5. Assign remediation disposition and owners.
6. Re-check high-impact findings after updates.
7. Publish evidence artifact paths and final recommendation.

## Content Clarity Gate Checklist

- [ ] Primary actions use explicit outcome-based language.
- [ ] Form labels and helper text remove ambiguity.
- [ ] Error messages identify issue and actionable recovery step.
- [ ] Empty and success states set clear next actions.
- [ ] High and critical clarity issues are resolved or deferred with owner and due date.

## Severity Model

- Critical: users are likely to complete the wrong action or abandon a core task.
- High: users can proceed only with repeated confusion or retries.
- Medium: wording friction slows completion.
- Low: minor wording improvements with limited task impact.

## Evidence Contract

- `.docs/changes/<workstream-id>/content-clarity-findings.md`
- `.docs/changes/<workstream-id>/content-clarity-checklist.md`
- `.docs/changes/<workstream-id>/release-recommendation.md`

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Deterministic content review | Deterministic Workflow |
| Objective quality gates | Content Clarity Gate Checklist |
| Severity-ranked findings | Severity Model |
| Durable evidence artifacts | Evidence Contract |
| Explicit release recommendation | Required Outputs |

## Reasoning Package

Assumptions:

- Copy changes materially affect task outcomes.

Trade-offs:

- Tight wording can improve speed but reduce context for new users.

Open blockers:

- Missing terminology standards can cause inconsistent outputs.

Recommendation:

- Use this skill at L3 for release-bound flows with copy changes.

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).

## Pragmatic Stop Rule

Stop when all in-scope content surfaces are evaluated, high and critical issues are resolved or dispositioned with owner and due date, and a final recommendation is published.

## Done Criteria

- Required outputs are complete and linked.
- Source ledger is current.
- Final recommendation is explicit and evidence-backed.

