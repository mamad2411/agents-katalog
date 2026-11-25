---
name: web-ux-information-architecture
description: Use when implementing or reviewing web UX information architecture outcomes with deterministic findability checks, navigation-depth limits, and evidence-backed release recommendations.
---

# Web UX Information Architecture

## Specialization

Use this skill to produce expert-level, agent-usable information architecture outcomes for web applications.

## Objective

Improve findability and task flow by validating navigation structure, taxonomy clarity, and wayfinding behavior with measurable evidence.

## Trigger Conditions

- A release changes navigation, hierarchy, or content grouping.
- Teams require objective findability and wayfinding evidence.
- UX quality gates require IA risk assessment before sign-off.

## Scope Boundaries

In scope:

- Navigation structure, taxonomy labels, page hierarchy, and step discoverability.
- Click depth, recovery routes, and orientation cues.

Out of scope:

- Copy tone and microcopy quality checks.
- Visual styling decisions without structural impact.

## Inputs

- In-scope journeys and top-find tasks.
- Site map, route map, and intended hierarchy.
- Evidence from search queries, support signals, or task sessions.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- IA findings with severity and user-impact rationale.
- Findability evidence matrix for top tasks.
- Prioritized IA remediation backlog.
- Final recommendation: `go`, `go-with-exceptions`, or `no-go`.

## Deterministic Workflow

1. Lock in-scope tasks and target destinations.
2. Define measurable findability criteria and acceptable navigation depth.
3. Validate taxonomy, hierarchy, and wayfinding cues against tasks.
4. Record task path length, detours, and dead-end occurrences.
5. Classify findings by severity and user-impact risk.
6. Assign remediation disposition and owner.
7. Re-validate high-impact IA paths after changes.
8. Publish final recommendation and evidence paths.

## IA Gate Checklist

- [ ] Top tasks are reachable through predictable paths.
- [ ] Navigation depth and branching remain within policy thresholds.
- [ ] Labels are unambiguous and reflect user mental models.
- [ ] Recovery from wrong path is possible within one step.
- [ ] High and critical IA findings are resolved or deferred with owner and due date.

## Severity Model

- Critical: users cannot find core functionality.
- High: users find tasks only after major detours.
- Medium: findability friction causes measurable delay.
- Low: minor structure improvements with limited impact.

## Evidence Contract

- `.docs/changes/<workstream-id>/ia-findings.md`
- `.docs/changes/<workstream-id>/ia-findability-matrix.md`
- `.docs/changes/<workstream-id>/release-recommendation.md`

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Deterministic IA execution | Deterministic Workflow |
| Objective findability gates | IA Gate Checklist |
| Severity-ranked findings | Severity Model |
| Durable evidence artifacts | Evidence Contract |
| Explicit release recommendation | Required Outputs |

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).

## Pragmatic Stop Rule

Stop when in-scope tasks meet findability checks, high and critical IA issues are resolved or dispositioned with owner and due date, and final recommendation is published.

## Done Criteria

- Required outputs are complete and linked.
- Source ledger is current.
- Final recommendation is explicit and evidence-backed.

