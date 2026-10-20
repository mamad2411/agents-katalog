---
name: mobile-offline-resilience
description: Use when a MAUI mobile change affects network-dependent flows and you need deterministic offline, retry, sync-conflict, and recovery evidence before sign-off.
---

# Mobile Offline Resilience

## Specialization

Use this skill to produce expert-level, agent-usable offline and resilience outcomes for MAUI mobile experiences.

This skill is specialized for degraded-network, local-state, retry, sync-conflict, and recovery behavior from the user perspective. It does not replace deeper infrastructure reliability engineering.

## Objective

Protect task continuity under degraded conditions by validating offline behavior, retry models, stale-data handling, lifecycle interruption, and recovery UX with deterministic evidence.

## Trigger Conditions

- A release affects network-dependent workflows or offline-capable mobile surfaces.
- Teams need objective resilience evidence before sign-off.
- Product scope includes intermittent connectivity, retries, caching, queueing, or sync behavior.
- Mobile lifecycle events such as suspend, resume, or background interruption may affect task continuity.

## Scope Boundaries

In scope:

- Offline indicators, degraded-network behavior, retry paths, sync conflict handling, stale data signaling, and recovery messaging.
- Lifecycle interruption and resume continuity where it affects task completion.
- User confidence and continuity during disruption.

Out of scope:

- Infrastructure resilience engineering without mobile UX implications.
- Backend retry logic with no user-visible consequence.

## Inputs

- In-scope journeys and network-dependency assumptions.
- Offline behavior expectations and retry policy.
- Local persistence, cache, queue, and conflict scenarios.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Offline and resilience findings with severity and user-impact rationale.
- Resilience evidence matrix for disruption, retry, resume, and recovery paths.
- Prioritized remediation backlog for task-continuity blockers.
- Final recommendation: `go`, `go-with-exceptions`, or `no-go`.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Validate one disrupted journey baseline | One disrupted journey has complete evidence and findings |
| L2 Delivery | Validate core offline-capable flows | Primary and recovery paths are evidence-backed |
| L3 Hardening | Enforce release-grade continuity gates | High and critical continuity risks are resolved or dispositioned |
| L4 Expert Standardization | Build reusable mobile resilience governance pattern | Reusable disruption matrix, thresholds, and evidence schema are documented |

## Deterministic Workflow

1. Lock in-scope disruption, cache, retry, and recovery scenarios.
2. Define pass or fail checks for offline signaling, retry quality, stale-data clarity, and conflict resolution.
3. Validate degraded-state behavior during loss of connectivity, high latency, and app interruption or resume.
4. Verify task context is preserved across retries, resume, and recoverable failures.
5. Classify findings by severity and continuity risk.
6. Assign remediation disposition with owner and due date.
7. Re-check high and critical issues after remediation.
8. Publish evidence artifacts and final recommendation.

## Offline Resilience Gate Checklist

- [ ] Users are informed when the app is offline or degraded.
- [ ] Retry behavior is explicit and preserves task context.
- [ ] Stale data and sync conflicts are understandable and recoverable.
- [ ] Critical user work is protected from silent loss where possible.
- [ ] Resume after interruption preserves task continuity or clearly signals recovery.
- [ ] High and critical issues are resolved or deferred with owner and due date.

## Severity Model

- Critical: users lose critical work or cannot recover essential tasks under disruption.
- High: degraded conditions materially block task continuity.
- Medium: resilience behavior is recoverable but confusing or inefficient.
- Low: minor resilience UX improvements.

## Evidence Contract

- `.docs/changes/<workstream-id>/mobile-offline-resilience-findings.md`
- `.docs/changes/<workstream-id>/mobile-offline-resilience-matrix.md`
- `.docs/changes/<workstream-id>/mobile-offline-remediation-backlog.md`
- `.docs/changes/<workstream-id>/mobile-offline-release-recommendation.md`

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Deterministic resilience workflow | Deterministic Workflow |
| Objective continuity gates | Offline Resilience Gate Checklist |
| Severity-ranked disruption findings | Severity Model |
| Durable evidence artifacts | Evidence Contract |
| Explicit recommendation | Required Outputs + Workflow step 8 |
| Source freshness governance | Source Governance Summary + Source Catalog |

## Reasoning Package

Assumptions:

- Mobile reliability issues often surface as UX continuity failures rather than infrastructure metrics.
- Resume and interruption behavior matter as much as network loss for mobile task continuity.

Trade-offs:

- Strong offline resilience gates reduce user-risk but add scenario-testing effort.
- Broader disruption coverage increases confidence but lengthens validation time.

Open blockers:

- Missing offline expectations or recovery rules reduce check quality.
- Weak local-state handling can invalidate otherwise good retry behavior.

Recommendation:

- Use L3 by default when a MAUI release depends on networked tasks, cached data, or resumable workflows.

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).
- Freshness threshold defaults to 30 days for active resilience-source checks.

## Pragmatic Stop Rule

Stop when degraded-network and interruption scenarios are validated, high and critical continuity risks are resolved or dispositioned, and a final recommendation is published with durable artifacts.

## Done Criteria

- Required outputs are complete and linked.
- Source catalog is current.
- Final recommendation is explicit and evidence-backed.
