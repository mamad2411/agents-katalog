---
name: mobile-performance-quality-gate
description: Use when a MAUI mobile change needs an expert, evidence-first performance decision with deterministic startup, rendering, memory, and release-quality checks.
---

# Mobile Performance Quality Gate

## Specialization

Use this skill to produce expert-level, agent-usable performance decisions for MAUI mobile experiences grounded in measurable startup, rendering, responsiveness, and memory outcomes.

This skill is bounded to mobile performance evidence and release decisions. It does not replace deep code-level optimization or architecture-wide performance research.

## Objective

Produce release-ready mobile performance decisions by converting startup, rendering, and memory evidence into severity-ranked findings, user-impact assessment, and explicit go or no-go recommendations.

## Trigger Conditions

- A MAUI flow or release candidate requires performance validation before merge or release.
- Teams need evidence for startup time, scroll smoothness, interaction responsiveness, or memory behavior.
- Product owners need performance-based sign-off decisions for key mobile journeys.
- A change introduces risk of degraded startup, resume, rendering, or app-size behavior.

## Scope Boundaries

In scope:

- User-centric performance signals for startup, resume, navigation, rendering, scrolling, and memory stability.
- Task-level performance impact and release-quality risk.
- Severity classification and remediation priority.

Out of scope:

- Backend-only performance work with no mobile impact.
- Accessibility certification.
- Generic benchmark design unrelated to the mobile app behavior.

## Inputs

- In-scope flows, states, and devices.
- Intended UX behavior and loading-state expectations.
- Performance threshold policy.
- Test environment details and evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

- Mobile performance findings report with severity and user-impact rationale.
- Performance evidence matrix covering startup, resume, navigation, scroll, and memory behavior.
- Threshold rubric with decision outcome by key journey.
- Prioritized remediation backlog with owner and expected impact.
- Final recommendation: `go`, `go-with-exceptions`, or `no-go`.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Validate one journey baseline | One journey has complete performance evidence and findings |
| L2 Delivery | Validate core flow performance quality | Primary, edge, and recovery journeys have measured outputs |
| L3 Hardening | Enforce release-grade performance gates | High-risk startup, rendering, or memory findings are resolved or dispositioned |
| L4 Expert Standardization | Build reusable mobile performance governance pattern | Reusable thresholds, scoring rubric, and evidence schema are documented |

## Deterministic Workflow

1. Lock scope: journeys, states, devices, and environment assumptions.
2. Define performance success criteria for each journey before measurement begins.
3. Capture baseline metrics for cold start, resume, navigation latency, list rendering, and memory growth.
4. Measure user-visible latency at loading, submit, navigation, and resume transitions.
5. Map performance observations to task outcomes such as retries, hesitation, or abandonment pressure.
6. Classify findings by severity and risk band.
7. Assign disposition for each finding: fix-now, fix-next, defer-with-owner, or reject-with-rationale.
8. Re-validate high-risk journeys after remediation and record residual risk.
9. Produce recommendation: `go`, `go-with-exceptions`, or `no-go` with rationale.
10. Publish durable evidence artifacts and closure status.

## Mobile Performance Gate Checklist

- [ ] Each in-scope journey has explicit performance success criteria.
- [ ] Cold start, resume, and navigation latency are measured and compared against thresholds.
- [ ] List rendering or scrolling quality is measured for representative screens.
- [ ] Memory stability is checked across repeated navigation cycles.
- [ ] High and critical performance findings are resolved or deferred with owner and due date.
- [ ] Residual risk and final recommendation are explicit and artifact-backed.

## Severity and Risk Model

- Critical: performance effectively blocks completion of a core task.
- High: users can complete tasks only with major delay, repeated retries, or likely abandonment.
- Medium: measurable friction that increases completion time but remains recoverable.
- Low: minor degradation with limited task impact.

Risk bands:

- Severe: clear performance pressure on completion of core flows.
- Elevated: recurring hesitation, retries, or frame drops with material risk.
- Watch: non-critical friction with trend risk if left unaddressed.
- Stable: no material evidence of performance pressure.

## Evidence Contract

- `.docs/changes/<workstream-id>/mobile-performance-findings.md`
- `.docs/changes/<workstream-id>/mobile-performance-evidence-matrix.md`
- `.docs/changes/<workstream-id>/mobile-performance-threshold-rubric.md`
- `.docs/changes/<workstream-id>/mobile-performance-release-recommendation.md`

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Deterministic mobile performance workflow | Deterministic Workflow |
| Objective performance thresholds | Mobile Performance Gate Checklist |
| Severity and risk classification | Severity and Risk Model |
| Durable evidence artifacts | Evidence Contract |
| Explicit release recommendation | Required Outputs + Workflow step 9 |
| Source freshness governance | Source Governance Summary + Source Catalog |

## Reasoning Package

Assumptions:

- Mobile performance decisions should be based on user-visible task impact, not infrastructure metrics alone.
- Startup, navigation, and memory stability are the minimum reusable gate set for MAUI mobile quality.

Trade-offs:

- Stricter thresholds reduce user risk but can increase release pressure.
- Broader device coverage increases confidence but adds execution time.

Open blockers:

- Missing production-like test conditions can distort performance outcomes.
- Undefined loading or resume behavior reduces consistency of findings.

Recommendation:

- Use L3 by default for release-bound MAUI changes and L4 when establishing reusable mobile performance governance.

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).
- Freshness threshold defaults to 30 days for active performance-source checks.

## Pragmatic Stop Rule

Stop when all in-scope journeys have measured performance evidence, all high and critical findings are resolved or explicitly deferred with owner and due date, and the final recommendation is recorded with durable artifact links.

## Done Criteria

- Trigger conditions are met for the request.
- Required outputs are complete and linked to durable evidence artifacts.
- L4 coverage matrix remains complete and current.
- Source catalog is current for this evaluation cycle.
- Final recommendation is explicit, evidence-backed, and auditable.
