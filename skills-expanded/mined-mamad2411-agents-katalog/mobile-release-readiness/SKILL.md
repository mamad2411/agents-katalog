---
name: mobile-release-readiness
description: Use before promoting a MAUI mobile build when you need an expert, evidence-first gate for signing, store readiness, smoke evidence, rollback, and go or no-go sign-off.
---

# Mobile Release Readiness

## Specialization

Drive a MAUI mobile release from code-complete to go or no-go sign-off by producing a mobile-specific gate checklist result, evidence bundle, rollback confirmation, and named sign-off record.

This skill satisfies mobile release governance needs. It does not perform deployment. It organizes and validates the evidence that authorizes promotion.

## Objective

Produce one release-ready mobile recommendation with explicit store, signing, testing, rollback, and approval evidence before promotion begins.

## Trigger Conditions

- A MAUI build is a candidate for TestFlight, internal testing, staged rollout, or production release.
- A release or deployment window is scheduled and evidence must be collated before the go or no-go call.
- Store metadata, privacy disclosures, or mobile-specific entitlements must be confirmed before release.
- Rollback readiness must be explicitly confirmed before promotion proceeds.

## Scope Boundaries

In scope:

- Mobile release gate checklist and evidence collation.
- Signing, packaging, smoke validation, telemetry readiness, and deep-link confirmation.
- Store listing readiness, privacy disclosures, accessibility labels when required, and approval chain capture.
- Rollback and hold or no-go documentation.

Out of scope:

- Running the deployment itself.
- Replacing general product release governance outside the mobile slice.
- Implementing code fixes discovered during the gate.

## Inputs

- Release target: environment, store or distribution lane, and workstream or release ID.
- Smoke evidence or planned smoke execution details.
- Security or compliance sign-off reference when required.
- Rollback procedure or path to it.
- Approval chain with named engineering owner and product or delivery owner.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

- Mobile release gate checklist result.
- Evidence bundle with named artifact references.
- Rollback confirmation with owner and execution summary.
- Store-readiness matrix covering packaging, metadata, and platform-specific disclosures.
- Final sign-off record with `go`, `hold`, or `no-go` disposition.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Prepare one build for internal review | One gate checklist and one evidence bundle exist |
| L2 Delivery | Prepare one app for managed release | Store, smoke, rollback, and sign-off evidence are complete |
| L3 Hardening | Enforce release-grade governance | No blocking gate is unresolved without waiver or owner |
| L4 Expert Standardization | Build reusable mobile release operating model | Reusable gate schema, evidence bundle, and decision rubric are documented |

## Deterministic Workflow

1. Confirm release target, originating workstream, and release lane.
2. Populate the mobile gate checklist and retrieve named evidence for each gate.
3. Validate signing, packaging, environment configuration, and distribution prerequisites.
4. Confirm smoke evidence, telemetry hooks, crash reporting, and deep-link handling.
5. Validate rollback procedure, named rollback owner, and executable rollback summary.
6. Review store or release metadata readiness, privacy disclosures, and accessibility labeling when applicable.
7. Obtain named approvals with role and timestamp.
8. Produce final decision: `go`, `hold`, or `no-go`.
9. If decision is not `go`, document blocking gates and required resolution before the next review.

## Mobile Release Gate Checklist

- [ ] Signed package or build artifact exists for the target lane.
- [ ] Smoke evidence is present and dated.
- [ ] Crash reporting and telemetry hooks are enabled for the release build.
- [ ] Deep links, notifications, and environment configuration are validated for the release lane.
- [ ] Store metadata, privacy disclosures, and accessibility labeling obligations are complete when applicable.
- [ ] Rollback steps are current, executable, and owned.
- [ ] Named engineering and product or delivery approvals are recorded.

## Decision Rules

- `go`: all gates pass or are formally waived with rationale.
- `hold`: one or more non-trivial gates are open but resolvable in the active release cycle.
- `no-go`: one or more blocking gates remain unresolved.

## Evidence Contract

- `.docs/changes/<workstream-id>/mobile-release-gate-checklist.md`
- `.docs/changes/<workstream-id>/mobile-release-evidence-bundle.md`
- `.docs/changes/<workstream-id>/mobile-store-readiness-matrix.md`
- `.docs/changes/<workstream-id>/mobile-release-decision.md`

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Deterministic mobile release gate | Deterministic Workflow |
| Objective gate checklist | Mobile Release Gate Checklist |
| Durable evidence bundle | Evidence Contract |
| Explicit release decision | Required Outputs + Decision Rules |
| Rollback confirmation | Required Outputs + Workflow step 5 |
| Source freshness governance | Source Governance Summary + Source Catalog |

## Reasoning Package

Assumptions:

- Mobile releases need additional packaging and store-facing evidence beyond generic service releases.
- Rollback evidence must exist before promotion begins.

Trade-offs:

- Strong mobile gate control reduces release surprises but adds pre-release coordination work.
- Store-readiness checks improve safety but can slow internal-only lanes when over-applied.

Open blockers:

- Missing signing or store metadata can invalidate a planned release.
- Unowned rollback steps or open smoke failures block safe promotion.

Recommendation:

- Use L3 by default for release-bound MAUI work and L4 when standardizing the mobile release operating model across repositories.

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).
- Freshness threshold defaults to 30 days for active release-source checks.

## Pragmatic Stop Rule

Stop when all required mobile gates are passed or explicitly waived, rollback is confirmed, approvals are recorded, and one explicit release decision artifact is published.

## Done Criteria

- Gate checklist is complete with no hidden open items.
- Evidence bundle references all required artifacts.
- Rollback confirmation is explicit and owned.
- Final decision is recorded with approvals and rationale.
- Source catalog is current for this evaluation cycle.
