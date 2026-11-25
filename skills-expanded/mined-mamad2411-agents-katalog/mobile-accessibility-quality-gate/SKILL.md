---
name: mobile-accessibility-quality-gate
description: Use when a MAUI mobile change needs an expert, evidence-first accessibility decision with deterministic checks, durable artifacts, and release-ready sign-off.
---

# Mobile Accessibility Quality Gate

## Specialization

Use this skill to deliver expert-level, agent-usable accessibility execution for MAUI mobile surfaces, from design handoff validation through release-ready evidence and sign-off.

This skill is specialized for native mobile accessibility execution and review. It does not perform product implementation and it does not replace general UX design work.

## Objective

Produce accessibility-complete MAUI mobile outcomes with explicit pass or fail gates, durable evidence artifacts, and deterministic release readiness decisions.

## Trigger Conditions

- A MAUI mobile flow, screen, or component must be validated for accessibility before merge or release.
- A mobile implementation needs objective evidence for labels, focus behavior, touch targets, dynamic type, and state announcements.
- Accessibility defects must be severity-ranked and converted into actionable remediation.
- Accessibility sign-off is required for a release artifact.

## Scope Boundaries

In scope:

- Screen reader, switch, voice, and keyboard-adjacent accessibility behavior where applicable.
- Focus order, semantic naming, labels, hints, and announced state changes.
- Touch-target sizing, contrast, dynamic type or larger text, and motion sensitivity checks.
- Severity-ranked findings, remediation decisions, and evidence bundle generation.

Out of scope:

- Broad visual redesign.
- Backend API changes.
- Non-mobile web accessibility validation.

## Inputs

- Target flow, screen, or component list.
- Intended interaction behavior and UX handoff notes.
- Runtime environment and device mix for validation.
- Acceptance threshold policy (default: no unresolved critical or serious issues).
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Accessibility findings report with severity tags and disposition per issue.
- Pass or fail checklist mapped to criteria used in scope.
- Assistive-technology verification notes for screen readers, larger text, and focus order.
- Evidence bundle references for automated and manual validation.
- Explicit sign-off recommendation: `go`, `go-with-exceptions`, or `no-go`.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Validate one screen baseline | One scoped accessibility report with objective defects listed |
| L2 Delivery | Validate a complete flow | Default, loading, empty, error, and success states are covered |
| L3 Hardening | Enforce release-grade quality gates | No unresolved critical or serious issues and evidence bundle complete |
| L4 Expert Standardization | Build reusable mobile accessibility execution pattern | Reusable checklist, evidence schema, and decision rubric are documented |

## Deterministic Workflow

1. Confirm scope boundary: screens, components, states, and representative device classes.
2. Build criteria set from active mobile accessibility guidance and map each criterion to a check.
3. Run automated accessibility checks where available and capture raw outputs.
4. Run manual verification for screen-reader order, visible focus where applicable, labels, hints, and announced state changes.
5. Validate larger text or dynamic type behavior, reduced-motion handling, and touch-target sizing.
6. Validate critical interactions with native assistive technologies and platform inspectors where available.
7. Classify findings by severity and create remediation disposition for each finding.
8. Re-run verification after fixes and record residual risk.
9. Produce release recommendation: `go`, `go-with-exceptions`, or `no-go` with rationale.
10. Publish durable evidence artifact paths.

## Accessibility Gate Checklist

- [ ] Text remains readable under larger text settings and does not truncate critical content.
- [ ] All actionable elements expose meaningful labels or hints.
- [ ] Focus order and announcement order match the intended task flow.
- [ ] Touch targets meet policy threshold and are not crowded.
- [ ] Dynamic state updates are conveyed to assistive technologies when required.
- [ ] Critical and serious findings are resolved or explicitly deferred with owner and due date.

## Severity Model

- Critical: blocks completion for assistive technology users or creates severe compliance risk.
- Serious: materially degrades completion success or introduces significant accessibility friction.
- Moderate: usability degradation with an available workaround.
- Minor: low-impact issue with minimal task risk.

## Evidence Contract

Capture artifacts under one change scope path:

- `.docs/changes/<workstream-id>/mobile-accessibility-findings.md`
- `.docs/changes/<workstream-id>/mobile-accessibility-checklist.md`
- `.docs/changes/<workstream-id>/mobile-accessibility-scan-results.json`
- `.docs/changes/<workstream-id>/mobile-accessibility-release-recommendation.md`

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Deterministic expert workflow | Deterministic Workflow |
| Objective acceptance criteria | Accessibility Gate Checklist |
| Severity-ranked findings | Severity Model |
| Durable evidence bundle | Evidence Contract |
| Explicit go or no-go sign-off | Required Outputs + Workflow step 9 |
| Source freshness governance | Source Governance Summary + Source Catalog |

## Reasoning Package

Assumptions:

- Mobile accessibility quality requires both automated and manual verification.
- Release decisions need durable evidence, not verbal confirmation.

Trade-offs:

- Strict no-critical and no-serious gates reduce risk but can delay release.
- Broader device and assistive-technology coverage increases confidence but adds execution time.

Open blockers:

- Missing state definitions reduce check completeness.
- Lack of representative device coverage can invalidate findings.

Recommendation:

- Use L3 by default for release-bound MAUI changes and L4 when building a repeatable mobile accessibility operating model.

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).
- Freshness threshold defaults to 30 days for active standards and platform checks.

## Pragmatic Stop Rule

Stop when all in-scope criteria are checked, all critical and serious findings are resolved or dispositioned with owner and due date, and the evidence contract artifacts exist with a final recommendation.

## Anti-Patterns

- Relying on automated scans only.
- Declaring accessibility sign-off without durable artifacts.
- Deferring critical or serious findings without named owner and follow-up date.
- Mixing broad redesign goals into accessibility verification scope.

## Done Criteria

- Trigger conditions are satisfied for the request.
- Required outputs are complete and linked to durable artifacts.
- L4 coverage matrix remains fully mapped.
- Source catalog has current evaluation date and disposition.
- Final recommendation is explicit and evidence-backed.
