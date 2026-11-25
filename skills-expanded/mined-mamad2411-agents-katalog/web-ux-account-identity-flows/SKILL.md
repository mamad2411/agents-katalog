---
name: web-ux-account-identity-flows
description: Use when implementing or reviewing web UX account and identity outcomes with deterministic sign-in, sign-up, recovery, and session-management checks and evidence-backed release recommendations.
---

# Web UX Account Identity Flows

## Specialization

Use this skill to produce expert-level, agent-usable account and identity flow outcomes for web experiences.

## Objective

Reduce identity-friction and recovery failure by validating sign-in, sign-up, password reset, MFA, and session-management flows with deterministic evidence.

## Trigger Conditions

- A release changes authentication, registration, account recovery, MFA, or session behaviors.
- Teams need objective identity-flow evidence before sign-off.
- Product scope includes account security or recovery-critical journeys.

## Scope Boundaries

In scope:

- Sign-in, sign-up, password reset, MFA, session expiry, and recovery paths.
- Clarity, recovery success, and trust continuity in identity journeys.

Out of scope:

- Security architecture implementation.
- Backend identity provider configuration.

## Inputs

- In-scope identity journeys and account states.
- Authentication requirements and session policy.
- Recovery and MFA expectations.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Identity-flow findings with severity and user-impact rationale.
- Identity journey evidence matrix for success, failure, and recovery paths.
- Prioritized remediation backlog for blocking account issues.
- Final recommendation: `go`, `go-with-exceptions`, or `no-go`.

## Deterministic Workflow

1. Lock in-scope identity and recovery journeys.
2. Define pass/fail checks for entry, verification, failure, and recovery states.
3. Validate clarity, continuity, and recovery guidance across the journeys.
4. Classify findings by severity and account-access risk.
5. Assign remediation disposition with owner and due date.
6. Re-check high and critical issues after remediation.
7. Publish evidence artifacts and final recommendation.

## Identity Gate Checklist

- [ ] Sign-in and sign-up states clearly guide next steps.
- [ ] Password reset and recovery paths are discoverable and recoverable.
- [ ] MFA challenges are understandable and recovery options are explicit.
- [ ] Session expiry or interruption preserves user orientation where possible.
- [ ] High and critical issues are resolved or deferred with owner and due date.

## Severity Model

- Critical: users cannot access or recover a core account path.
- High: identity flow friction creates likely abandonment or lockout risk.
- Medium: measurable friction with recoverable path.
- Low: minor identity UX improvements.

## Evidence Contract

- `.docs/changes/<workstream-id>/account-identity-findings.md`
- `.docs/changes/<workstream-id>/account-identity-matrix.md`
- `.docs/changes/<workstream-id>/release-recommendation.md`

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).

## Pragmatic Stop Rule

Stop when all in-scope identity journeys are validated, high and critical issues are resolved or dispositioned, and a final recommendation is published.

## Done Criteria

- Required outputs are complete and linked.
- Source ledger is current.
- Final recommendation is explicit and evidence-backed.

