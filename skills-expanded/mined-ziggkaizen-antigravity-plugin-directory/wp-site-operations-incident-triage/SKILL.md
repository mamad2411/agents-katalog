---
name: wp-site-operations-incident-triage
description: Triages WordPress availability, integrity, performance, and suspected-security incidents while stabilizing service, preserving evidence, controlling changes, restoring safely, and escalating appropriately. Use when normal maintenance procedures are no longer sufficient.
---

# wp-site-operations-incident-triage

Use this skill when a WordPress site is unavailable, materially broken, losing data, severely degraded, or potentially compromised.

## First Decision

Classify the event as:

- Availability/functionality.
- Data integrity.
- Performance.
- Suspected compromise.
- Unknown combination.

This classification changes the order of evidence capture, containment, restoration, updates, credential rotation, and cleanup.

## Workflow

Use [`workflows/triage-wordpress-incident-workflow.md`](workflows/triage-wordpress-incident-workflow.md).

## Resource

Use [`resources/incident-severity-matrix.md`](resources/incident-severity-matrix.md).

## Completion Evidence

Produce an incident timeline, severity, affected scope, evidence locations, actions, approvals, restored services, data reconciliation, root cause or current hypotheses, security disposition, and follow-up owners.
