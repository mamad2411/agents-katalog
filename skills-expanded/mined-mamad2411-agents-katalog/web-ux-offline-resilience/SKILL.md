---
name: web-ux-offline-resilience
description: Use when implementing or reviewing web UX offline and resilience outcomes with deterministic degraded-network, retry, sync-conflict, and recovery checks and evidence-backed release recommendations.
---

# Web UX Offline Resilience

## Specialization

Use this skill to produce expert-level, agent-usable offline and resilience outcomes for web experiences.

## Objective

Protect task continuity under degraded conditions by validating offline behavior, retry models, sync conflicts, and recovery UX with deterministic evidence.

## Trigger Conditions

- A release affects network-dependent workflows or offline-capable surfaces.
- Teams need objective resilience UX evidence before sign-off.
- Product scope includes intermittent connectivity, retries, or sync behavior.

## Scope Boundaries

In scope:

- Offline indicators, degraded-network behavior, retry paths, sync conflict handling, and recovery messaging.
- User confidence and continuity during disruption.

Out of scope:

- Infrastructure resilience engineering without UX implications.

## Inputs

- In-scope journeys and network-dependency assumptions.
- Offline behavior expectations and retry policy.
- Conflict and recovery scenarios.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Offline/resilience findings with severity and user-impact rationale.
- Resilience evidence matrix for disruption, retry, and recovery paths.
- Prioritized remediation backlog for task-continuity blockers.
- Final recommendation: `go`, `go-with-exceptions`, or `no-go`.

## Deterministic Workflow

1. Lock in-scope disruption and recovery scenarios.
2. Define pass/fail checks for offline signaling, retry quality, and conflict resolution.
3. Validate degraded-state behavior and continuity guidance.
4. Classify findings by severity and continuity risk.
5. Assign remediation disposition with owner and due date.
6. Re-check high and critical issues after remediation.
7. Publish evidence artifacts and final recommendation.

## Offline Resilience Gate Checklist

- [ ] Users are informed when the system is offline or degraded.
- [ ] Retry behavior is explicit and preserves task context.
- [ ] Sync conflicts or stale data conditions are understandable and recoverable.
- [ ] Critical user work is protected from silent loss where possible.
- [ ] High and critical issues are resolved or deferred with owner and due date.

## Severity Model

- Critical: users lose critical work or cannot recover essential tasks under disruption.
- High: degraded network conditions materially block task continuity.
- Medium: resilience behavior is recoverable but confusing or inefficient.
- Low: minor resilience UX improvements.

## Evidence Contract

- `.docs/changes/<workstream-id>/offline-resilience-findings.md`
- `.docs/changes/<workstream-id>/offline-resilience-matrix.md`
- `.docs/changes/<workstream-id>/release-recommendation.md`

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).

## Pragmatic Stop Rule

Stop when degraded-network scenarios are validated, high and critical issues are resolved or dispositioned, and final recommendation is published.

## Done Criteria

- Required outputs are complete and linked.
- Source ledger is current.
- Final recommendation is explicit and evidence-backed.

