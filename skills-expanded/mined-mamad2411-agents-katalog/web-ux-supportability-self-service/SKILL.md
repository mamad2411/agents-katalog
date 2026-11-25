---
name: web-ux-supportability-self-service
description: Use when implementing or reviewing web UX supportability outcomes with deterministic self-service, escalation, and recovery-guidance checks and evidence-backed release recommendations.
---

# Web UX Supportability Self Service

## Specialization

Use this skill to produce expert-level, agent-usable supportability and self-service outcomes for web experiences.

## Objective

Reduce support burden and increase user self-resolution by validating help entry points, escalation cues, recovery guidance, and support readiness with deterministic evidence.

## Trigger Conditions

- A release changes help surfaces, support flows, or self-service recovery experiences.
- Teams need objective supportability evidence before sign-off.
- Product scope includes complex workflows where users may need assistance or escalation.

## Scope Boundaries

In scope:

- Help entry points, contextual guidance, escalation cues, and self-service recovery support.
- Discoverability and usefulness of support pathways during failure or confusion.

Out of scope:

- Back-office support tooling implementation.

## Inputs

- In-scope journeys and support-relevant failure points.
- Support model, escalation rules, and self-service expectations.
- Help content or support entry policies.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Supportability findings with severity and user-impact rationale.
- Support evidence matrix for help entry, self-resolution, and escalation paths.
- Prioritized remediation backlog for support blockers.
- Final recommendation: `go`, `go-with-exceptions`, or `no-go`.

## Deterministic Workflow

1. Lock in-scope support and self-service journeys.
2. Define pass/fail checks for discoverability, relevance, and escalation clarity.
3. Validate contextual help, recovery guidance, and escalation options.
4. Classify findings by severity and support burden risk.
5. Assign remediation disposition with owner and due date.
6. Re-check high and critical issues after remediation.
7. Publish evidence artifacts and final recommendation.

## Supportability Gate Checklist

- [ ] Contextual help is available where users are likely to stall.
- [ ] Recovery guidance supports self-resolution before forced escalation.
- [ ] Escalation paths are clear when self-service is insufficient.
- [ ] Support entry points preserve or reference user task context where possible.
- [ ] High and critical issues are resolved or deferred with owner and due date.

## Severity Model

- Critical: users cannot recover or escalate from blocked core tasks.
- High: support friction materially harms self-resolution or completion.
- Medium: help exists but is inefficient or hard to discover.
- Low: minor supportability improvements.

## Evidence Contract

- `.docs/changes/<workstream-id>/supportability-findings.md`
- `.docs/changes/<workstream-id>/supportability-matrix.md`
- `.docs/changes/<workstream-id>/release-recommendation.md`

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).

## Pragmatic Stop Rule

Stop when support and self-service paths are validated, high and critical issues are resolved or dispositioned, and final recommendation is published.

## Done Criteria

- Required outputs are complete and linked.
- Source ledger is current.
- Final recommendation is explicit and evidence-backed.

