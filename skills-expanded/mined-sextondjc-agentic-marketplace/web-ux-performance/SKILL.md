---
name: web-ux-performance
description: Use when implementing or reviewing web UX performance outcomes with deterministic responsiveness checks, perceived-latency evidence, abandonment-risk thresholds, and release-ready recommendations.
---

# Web UX Performance

## Specialization

Use this skill to produce expert-level, agent-usable web UX performance decisions grounded in measurable user experience outcomes.

This skill is bounded to UX performance evidence for web surfaces. It does not replace deep code-level profiling workflows, broad architecture performance studies, or accessibility and usability validation.

## Objective

Produce release-ready UX performance decisions by converting responsiveness and latency evidence into severity-ranked findings, abandonment-risk assessment, and explicit go or no-go recommendations.

## Trigger Conditions

- A web flow requires UX performance validation before merge or release.
- Teams need evidence for interaction responsiveness and perceived latency impact.
- Product owners need abandonment-risk based sign-off decisions for key journeys.
- A change introduces risk of degraded Core Web Vitals or interaction quality.

## Scope Boundaries

In scope:

- User-centric performance signals across desktop, tablet, and mobile web breakpoints.
- Task-level perceived latency and interaction responsiveness evidence.
- Abandonment-risk thresholds, severity classification, and remediation priority.

Out of scope:

- Backend-only optimization without UX impact evidence.
- Accessibility compliance certification.
- Pure visual design exploration without measurable performance outcomes.

## Inputs

- In-scope flows and user tasks.
- Intended UX behavior and loading-state expectations.
- Performance thresholds policy.
- Test environment details and traffic profile assumptions.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- UX performance findings report with severity and user-impact rationale.
- Performance evidence matrix with LCP, CLS, INP, task wait points, and step drop-off pressure.
- Abandonment-risk rubric with threshold decisions by key journey.
- Prioritized remediation backlog with owner and expected impact.
- Final recommendation: `go`, `go-with-exceptions`, or `no-go`.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Validate one journey baseline | One journey has complete UX performance evidence and findings |
| L2 Delivery | Validate core flow performance quality | Primary, edge, and error journeys have measured UX performance outputs |
| L3 Hardening | Enforce release-grade UX performance gates | High-risk latency and responsiveness findings are resolved or dispositioned |
| L4 Expert Standardization | Build reusable UX performance governance pattern | Reusable thresholds, scoring rubric, and evidence schema are documented |

## Deterministic Workflow

1. Lock scope: journeys, states, devices, and environment assumptions.
2. Define performance success criteria for each journey before measurement begins.
3. Capture baseline metrics for LCP, CLS, INP, and critical step wait points.
4. Measure perceived latency at user-visible transitions, including loading, submit, and navigation feedback.
5. Map performance observations to task outcomes, including retries, hesitation, and drop-off pressure.
6. Classify findings by severity and abandonment-risk band.
7. Assign disposition for each finding: fix-now, fix-next, defer-with-owner, or reject-with-rationale.
8. Re-validate high-risk journeys after remediation and record residual risk.
9. Produce recommendation: `go`, `go-with-exceptions`, or `no-go` with rationale.
10. Publish durable evidence artifacts and closure status.

## UX Performance Gate Checklist

- [ ] Each in-scope journey has explicit performance success criteria.
- [ ] LCP, CLS, and INP are measured and compared against policy thresholds.
- [ ] User-visible wait points are mapped and evaluated for perceived-latency impact.
- [ ] High and critical abandonment-risk findings are resolved or deferred with owner and due date.
- [ ] Residual risk and recommendation are explicit and artifact-backed.

## Severity and Risk Model

- Critical: performance prevents or effectively blocks completion of a core task.
- High: users can complete tasks only with significant delay, retries, or likely abandonment.
- Medium: measurable friction that increases completion time but usually remains recoverable.
- Low: minor degradation with limited task impact.

Abandonment-risk bands:

- Severe: clear behavioral signals of abandonment probability for core flows.
- Elevated: recurring hesitation or retries with material conversion risk.
- Watch: non-critical friction with trend risk if left unaddressed.
- Stable: no material evidence of abandonment pressure.

## Evidence Contract

Capture artifacts under one change scope path:

- `.docs/changes/<workstream-id>/ux-performance-findings.md`
- `.docs/changes/<workstream-id>/performance-evidence-matrix.md`
- `.docs/changes/<workstream-id>/abandonment-risk-rubric.md`
- `.docs/changes/<workstream-id>/release-recommendation.md`

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Deterministic UX performance execution | Deterministic Workflow |
| Objective responsiveness and latency evidence | Required Outputs + UX Performance Gate Checklist |
| Abandonment-risk thresholding | Severity and Risk Model |
| Durable sign-off artifacts | Evidence Contract |
| Explicit release recommendation | Required Outputs + Workflow step 9 |
| Source freshness governance | Source Governance Summary + Source Ledger |

## Reasoning Package

Assumptions:

- In-scope journeys and success criteria are known before validation.
- UX performance decisions should be based on user-impact evidence, not infrastructure metrics alone.

Trade-offs:

- Stricter thresholds reduce user risk but can increase release pressure.
- Broader device coverage increases confidence but adds execution time.

Open blockers:

- Missing production-like test conditions can distort perceived-latency outcomes.
- Undefined loading-state behavior reduces consistency of findings.

Recommendation:

- Use L3 by default for release-bound web UX changes and L4 when establishing reusable team governance.

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).
- Freshness threshold default is 30 days for active source checks.

## Companion Boundaries

- Use this skill for UX performance evidence and release decisions tied to speed and responsiveness.
- Keep accessibility compliance checks in the accessibility companion skill.
- Keep task-completion usability studies in the usability companion skill.

## Pragmatic Stop Rule

Stop when all in-scope journeys have measured UX performance evidence, all high and critical abandonment-risk findings are resolved or explicitly deferred with owner and due date, and the final recommendation is recorded with durable artifact links.

## Anti-Patterns

- Using backend metrics only without user-facing performance evidence.
- Declaring go status without abandonment-risk analysis.
- Deferring high-risk findings without owner and follow-up date.
- Expanding journey scope mid-run without resetting thresholds and evidence expectations.

## Done Criteria

- Trigger conditions are met for the request.
- Required outputs are complete and linked to durable evidence artifacts.
- L4 coverage matrix remains complete and current.
- Source ledger is current for this evaluation cycle.
- Final recommendation is explicit, evidence-backed, and auditable.

