---
name: web-ux-telemetry-instrumentation
description: Use when implementing or reviewing web UX telemetry outcomes with deterministic event-contract checks, measurement completeness gates, and evidence-backed release recommendations.
---

# Web UX Telemetry Instrumentation

## Specialization

Use this skill to produce expert-level, agent-usable telemetry and instrumentation outcomes for web UX flows.

## Objective

Ensure UX quality decisions are measurable by enforcing event-contract quality, coverage completeness, and reliable evidence paths.

## Trigger Conditions

- A release introduces or changes UX telemetry events.
- Teams need measurable event coverage for key tasks and failure paths.
- Quality gate decisions depend on event evidence integrity.

## Scope Boundaries

In scope:

- Event naming, schema completeness, key journey coverage, and error/recovery instrumentation.
- Measurement quality checks for completion, retries, drop-off, and recovery behavior.

Out of scope:

- Data warehouse modeling beyond event quality checks.

## Inputs

- In-scope journeys and task steps.
- Event schema or contract definitions.
- Analytics policy and privacy constraints.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Telemetry quality findings with severity and user-impact rationale.
- Instrumentation coverage matrix by task step and outcome.
- Prioritized remediation backlog for gaps and invalid event contracts.
- Final recommendation: `go`, `go-with-exceptions`, or `no-go`.

## Deterministic Workflow

1. Lock in-scope journeys and required telemetry outcomes.
2. Define required event contract fields and quality gates.
3. Map expected events to each task step, including error and recovery paths.
4. Validate event schema consistency and naming quality.
5. Classify missing or invalid instrumentation findings by severity.
6. Assign remediation disposition with owner and due date.
7. Publish evidence artifacts and final recommendation.

## Telemetry Gate Checklist

- [ ] Core task start, success, error, and recovery events are present.
- [ ] Event contracts include required identifiers and context fields.
- [ ] Event naming and taxonomy are consistent across flows.
- [ ] Drop-off and retry signals are measurable for key journeys.
- [ ] High and critical telemetry gaps are resolved or deferred with owner and due date.

## Severity Model

- Critical: key decision outcomes cannot be measured.
- High: major journey signals are incomplete or unreliable.
- Medium: partial coverage limits confidence in decisions.
- Low: minor schema hygiene issues.

## Evidence Contract

- `.docs/changes/<workstream-id>/telemetry-quality-findings.md`
- `.docs/changes/<workstream-id>/telemetry-coverage-matrix.md`
- `.docs/changes/<workstream-id>/release-recommendation.md`

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).

## Pragmatic Stop Rule

Stop when required journey telemetry is measurable, high and critical issues are resolved or dispositioned, and a final recommendation is published.

## Done Criteria

- Required outputs are complete and linked.
- Source ledger is current.
- Final recommendation is explicit and evidence-backed.

