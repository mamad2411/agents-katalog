---
name: web-ux-accessibility
description: Use when implementing or reviewing web UX and frontend accessibility outcomes with deterministic WCAG/APG checks, evidence artifacts, and release-ready sign-off gates.
---

# Web UX Accessibility

## Specialization

Use this skill to deliver expert-level, agent-usable accessibility execution for web UX and frontend surfaces, from UX handoff validation through implementation verification and sign-off evidence.

This skill is specialized for accessibility execution and review. It should not be used for broad visual redesigns, backend implementation, or mobile-native UX.

## Objective

Produce accessibility-complete web UX outcomes with explicit pass/fail gates, durable evidence artifacts, and deterministic release readiness decisions.

## Trigger Conditions

- A web UX flow, page, or component must be validated for accessibility before merge or release.
- A frontend implementation needs WCAG 2.2 and ARIA pattern alignment with objective evidence.
- Accessibility defects must be severity-ranked and converted into actionable remediation.
- Accessibility sign-off is required for release governance artifacts.

## Scope Boundaries

In scope:

- Desktop and mobile web breakpoint accessibility checks.
- Keyboard interaction, focus behavior, semantic structure, naming, and state announcements.
- Severity-ranked findings, remediation decisions, and evidence bundle generation.

Out of scope:

- Brand refresh or non-accessibility visual exploration.
- Backend API changes.
- Native mobile platform accessibility outside web surfaces.

## Inputs

- Target flow or component list.
- UX handoff notes and intended interaction behavior.
- Runtime environment for validation.
- Acceptance threshold policy (default: no open critical/serious issues).
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Accessibility findings report with severity tags and disposition per issue.
- Pass/fail checklist mapped to WCAG/APG criteria used in scope.
- Keyboard and focus-order verification notes for all key interactions.
- Evidence bundle references (automated scan output + manual verification summary).
- Explicit sign-off recommendation: `go`, `go-with-exceptions`, or `no-go`.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Validate one page or component baseline | One scoped accessibility report with objective defects listed |
| L2 Delivery | Validate a complete user flow | All states covered: default, loading, empty, error, success |
| L3 Hardening | Enforce release-grade quality gates | No unresolved critical/serious issues and evidence bundle complete |
| L4 Expert Standardization | Build reusable accessibility execution pattern | Reusable checklist, evidence schema, and decision rubric produced |

## Deterministic Workflow

1. Confirm scope boundary: pages, components, states, and breakpoints.
2. Build criteria set from active standards in scope and map each criterion to a check.
3. Run automated accessibility scan and capture raw outputs.
4. Run manual keyboard/focus checks for tab order, traps, escapes, and visible focus.
5. Run semantic and naming checks for headings, landmarks, labels, and announced state changes.
6. Validate component interaction patterns against authoritative ARIA pattern guidance where applicable.
7. Classify findings by severity and create remediation disposition for each finding.
8. Re-run verification after fixes and record residual risks.
9. Produce release recommendation (`go`, `go-with-exceptions`, `no-go`) with rationale.
10. Publish durable evidence artifact paths.

## Accessibility Gate Checklist

- [ ] Contrast and text legibility checks meet policy threshold.
- [ ] All interactive controls are keyboard reachable with visible focus indicators.
- [ ] Forms expose programmatically determinable labels and error associations.
- [ ] Dialogs, menus, tabs, and other widgets follow expected keyboard behavior.
- [ ] Dynamic state updates are conveyed to assistive technologies where required.
- [ ] Critical and serious findings are fully resolved or explicitly deferred with owner and due date.

## Severity Model

- Critical: blocks task completion for assistive technology users or causes severe compliance risk.
- Serious: materially degrades completion success or introduces significant accessibility friction.
- Moderate: usability degradation with available workaround.
- Minor: low-impact issue with minimal task risk.

## Evidence Contract

Capture artifacts under a change scope path:

- `.docs/changes/<workstream-id>/accessibility-findings.md`
- `.docs/changes/<workstream-id>/accessibility-checklist.md`
- `.docs/changes/<workstream-id>/scan-results.json`
- `.docs/changes/<workstream-id>/release-recommendation.md`

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Deterministic expert workflow | Deterministic Workflow |
| Objective acceptance criteria | Accessibility Gate Checklist |
| Severity-ranked findings | Severity Model |
| Durable evidence bundle | Evidence Contract |
| Explicit go/no-go sign-off | Required Outputs + Workflow step 9 |
| Source freshness governance | Source Governance Summary + Source Ledger |

## Reasoning Package

Assumptions:

- The target surface is a web UI (not native mobile).
- Accessibility policy requires objective evidence before release decisions.

Trade-offs:

- Automated scans increase speed but miss interaction nuances; manual checks are mandatory.
- Strict no-critical/no-serious gates reduce risk but may delay releases.

Open blockers:

- Missing UX state definitions can reduce check completeness.
- Lack of test environment parity can invalidate some findings.

Recommendation:

- Use L3 by default for release-bound changes and escalate to L4 when building repeatable team standards.

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).
- Freshness threshold default is 30 days for active standards checks.

## Pragmatic Stop Rule

Stop when all in-scope criteria are checked, all critical/serious findings are resolved or dispositioned with owner and due date, and the evidence contract artifacts exist with a final recommendation.

## Anti-Patterns

- Relying on automated scans only.
- Declaring sign-off without durable artifacts.
- Deferring critical/serious findings without named owner and follow-up date.
- Mixing visual redesign goals into accessibility verification scope.

## Done Criteria

- Trigger conditions are satisfied for the request.
- Required outputs are complete and linked to durable artifacts.
- L4 coverage matrix entries remain fully mapped.
- Source ledger has current evaluation date and disposition.
- Final recommendation is explicit and evidence-backed.

