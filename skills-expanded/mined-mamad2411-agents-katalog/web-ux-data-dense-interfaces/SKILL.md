---
name: web-ux-data-dense-interfaces
description: Use when implementing or reviewing web UX data-dense interface outcomes with deterministic table, filter, sorting, and bulk-action checks and evidence-backed release recommendations.
---

# Web UX Data Dense Interfaces

## Specialization

Use this skill to produce expert-level, agent-usable UX outcomes for data-dense web interfaces such as tables, dashboards, filters, and bulk-action surfaces.

## Objective

Improve task throughput and reduce operational mistakes by validating scanability, control clarity, and high-density interaction quality with deterministic evidence.

## Trigger Conditions

- A release changes data tables, dashboards, filtering, bulk actions, or analytical views.
- Teams need objective evidence for dense-interface usability before sign-off.
- Product scope includes high-volume or expert-user workflows.

## Scope Boundaries

In scope:

- Table scanability, sorting, filtering, faceting, selection, bulk actions, and density controls.
- Error prevention and recovery in high-density task workflows.

Out of scope:

- General flow-based UX that does not involve dense data interaction.

## Inputs

- In-scope dense-interface tasks and user roles.
- Column, filter, and action models.
- Success criteria for throughput, accuracy, and recovery.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Dense-interface findings with severity and user-impact rationale.
- Task evidence matrix for scan, select, filter, sort, and bulk-action flows.
- Prioritized remediation backlog for throughput or error-risk issues.
- Final recommendation: `go`, `go-with-exceptions`, or `no-go`.

## Deterministic Workflow

1. Lock in-scope tasks, views, and control sets.
2. Define pass/fail checks for scanability, control discoverability, and mistake prevention.
3. Validate sorting, filtering, selection, and bulk-action clarity.
4. Classify findings by severity and operational risk.
5. Assign remediation disposition with owner and due date.
6. Re-check high and critical issues after remediation.
7. Publish evidence artifacts and final recommendation.

## Data-Dense Gate Checklist

- [ ] Users can scan and compare records efficiently.
- [ ] Filters and sorts are visible, understandable, and reversible.
- [ ] Bulk actions clearly show scope and irreversible consequences.
- [ ] Error prevention and recovery are explicit for high-impact actions.
- [ ] High and critical issues are resolved or deferred with owner and due date.

## Severity Model

- Critical: dense-interface users cannot complete core operational tasks or may trigger harmful bulk actions.
- High: throughput or accuracy is materially degraded.
- Medium: moderate scanability or control friction.
- Low: minor density or layout improvements.

## Evidence Contract

- `.docs/changes/<workstream-id>/data-dense-findings.md`
- `.docs/changes/<workstream-id>/data-dense-matrix.md`
- `.docs/changes/<workstream-id>/release-recommendation.md`

## Source Governance Summary

- Source relevance, authority, freshness, and actionability are tracked in [source-catalog.md](./references/source-catalog.md).

## Pragmatic Stop Rule

Stop when dense-interface tasks are validated, high and critical issues are resolved or dispositioned, and final recommendation is published.

## Done Criteria

- Required outputs are complete and linked.
- Source ledger is current.
- Final recommendation is explicit and evidence-backed.

