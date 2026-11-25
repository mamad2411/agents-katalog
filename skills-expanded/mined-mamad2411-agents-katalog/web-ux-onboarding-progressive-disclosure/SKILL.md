---
name: web-ux-onboarding-progressive-disclosure
description: Use when implementing or reviewing web UX onboarding outcomes with deterministic first-run, progressive-disclosure, and setup-friction checks and evidence-backed release recommendations.
---

# Web UX Onboarding Progressive Disclosure

## Specialization

Use this skill to produce expert-level, agent-usable onboarding and progressive-disclosure outcomes for web experiences.

## Objective

Reduce first-run friction and learning overload by validating guidance sequencing, reveal timing, setup burden, and recovery support with deterministic evidence.

## Trigger Conditions

- A release changes onboarding, setup, tours, hints, or progressive-disclosure behavior.
- Teams need objective evidence for first-run or learning-path quality.
- Product scope includes guided setup or staged capability reveal.

## Scope Boundaries

In scope:

- First-run guidance, setup steps, tours, hint systems, and staged reveal patterns.
- Task sequencing, cognitive load, and user control over guidance.

Out of scope:

- Long-form training content systems.

## Inputs

- In-scope onboarding journeys and user types.
- Setup and first-run success criteria.
- Guidance models and dismissal behavior.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Onboarding findings with severity and user-impact rationale.
- Onboarding evidence matrix for entry, guidance, completion, and skip/recovery paths.
- Prioritized remediation backlog for setup and reveal friction.
- Final recommendation: `go`, `go-with-exceptions`, or `no-go`.

## Deterministic Workflow

1. Lock in-scope onboarding and guided-disclosure journeys.
2. Define pass/fail checks for sequencing, clarity, user control, and setup burden.
3. Validate reveal timing, dismissibility, and task continuity.
4. Classify findings by severity and adoption risk.
5. Assign remediation disposition with owner and due date.
6. Re-check high and critical issues after remediation.
7. Publish evidence artifacts and final recommendation.

## Onboarding Gate Checklist

- [ ] First-run guidance is timely and relevant to user goals.
- [ ] Progressive disclosure avoids overwhelming users with premature detail.
- [ ] Users can dismiss, defer, or revisit guidance where appropriate.
- [ ] Setup burden is proportionate to immediate user value.
- [ ] High and critical issues are resolved or deferred with owner and due date.

## Severity Model

- Critical: users cannot complete setup or first-run success path.
- High: onboarding friction materially harms adoption or completion.
- Medium: notable learning friction with recoverable path.
- Low: minor guidance-quality improvements.

## Evidence Contract

- `.docs/changes/<workstream-id>/onboarding-findings.md`
- `.docs/changes/<workstream-id>/onboarding-matrix.md`
- `.docs/changes/<workstream-id>/release-recommendation.md`

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).

## Pragmatic Stop Rule

Stop when onboarding and progressive-disclosure journeys are validated, high and critical issues are resolved or dispositioned, and a final recommendation is published.

## Done Criteria

- Required outputs are complete and linked.
- Source ledger is current.
- Final recommendation is explicit and evidence-backed.

