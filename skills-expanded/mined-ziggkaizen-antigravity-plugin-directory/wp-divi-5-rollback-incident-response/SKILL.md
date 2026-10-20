---
name: wp-divi-5-rollback-incident-response
description: Contains Divi 5 incidents and selects between Migrator content restore, previous-version rollback, manual Divi 4 reinstall, or full-site backup restore while preserving evidence and minimizing data loss.
---

# Divi 5 Rollback and Incident Response

Use this skill when a migration, update, rendering failure, or compatibility issue threatens a critical journey or exceeds the approved change window.

## Immediate Priorities

1. Protect visitors and data.
2. Stop unrelated mutation and content editing.
3. Capture current evidence and exact versions.
4. Determine whether the failure is content, theme files, database, cache, extension, or infrastructure.
5. Choose the least-destructive recovery path that restores a known-good state.

## Rollback Paths

- Migrator content restore for original Divi 4 content preserved by the Migrator.
- Built-in previous-version rollback when still available.
- Manual Divi 4 reinstall after restoring Divi 4 content.
- Full-site backup restore when the failure exceeds Migrator/theme scope or data integrity is uncertain.
- Forward fix only when the cause is proven, the change is smaller than rollback risk, and the approved window remains open.

## Critical Caveats

- Divi 5-created content is not restored as Divi 4 content by the Migrator.
- Built-in rollback may be unavailable after two or more Divi 5 updates.
- Continued Divi 5 editing increases divergence and rollback complexity.
- Cache clearing cannot recover lost or incorrectly converted content.
- A theme-only rollback does not restore database, plugin, upload, or configuration state.

## Workflow

Use [rollback-and-incident-response-workflow.md](workflows/rollback-and-incident-response-workflow.md).

## Resources

- [rollback-decision-matrix.md](resources/rollback-decision-matrix.md)
- [incident-checklist.md](resources/incident-checklist.md)
- [incident-timeline-example.md](examples/incident-timeline-example.md)

## Output

Return:

- Severity and affected journeys.
- Containment actions.
- Evidence and current state.
- Selected recovery path and rationale.
- Data-loss exposure.
- Verification results.
- Follow-up actions and owners.
