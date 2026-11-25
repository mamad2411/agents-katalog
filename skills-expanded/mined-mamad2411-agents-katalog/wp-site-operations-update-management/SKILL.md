---
name: wp-site-operations-update-management
description: Plans and controls WordPress core, plugin, and theme updates with release review, compatibility evidence, staging, recovery points, maintenance windows, smoke tests, monitoring, and rollback criteria. Use for any update that may affect a live site.
---

# wp-site-operations-update-management

Use this skill for WordPress core, plugin, theme, language, dependency, or database-upgrade operations.

## Safety

- Inventory the exact target and current versions.
- Read release, security, deprecation, and compatibility notes.
- Verify licenses and artifact access before the window.
- Test representative data and integrations in staging.
- Create and verify a fresh recovery point.
- Define database migration and rollback behavior.
- Apply the smallest reasonable batch.
- Stop when evidence differs materially from the plan.

## Command Guard

Run help before using the included hook helper:

```powershell
python .agents/plugins/wp-site-operations/skills/wp-site-operations-update-management/scripts/wordpress-command-safety.py --help
```

The guard does not replace authorization, backup, target verification, or a change plan.

## Workflow

Use [`workflows/run-wordpress-update-workflow.md`](workflows/run-wordpress-update-workflow.md).

## Resource

Use [`resources/update-risk-matrix.md`](resources/update-risk-matrix.md).

## Completion Evidence

Produce a change record with versions before/after, release notes, staging evidence, backup set, approvals, commands/actions, database changes, cache actions, smoke tests, monitoring, rollback decision, and follow-up.
