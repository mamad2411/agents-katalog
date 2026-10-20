---
name: wp-site-operations-readiness
description: Assesses whether a WordPress site, environment, access model, backup path, monitoring coverage, and operating team are ready for maintenance, updates, or production diagnosis. Use before planning a risky operational change.
---

# wp-site-operations-readiness

Use this skill before update, restore, incident, migration-adjacent, or production-diagnostic work.

## Read-Only First

Start with:

- Exact site and environment identity.
- Installed WordPress and runtime versions.
- Hosting and deployment topology.
- Plugin, theme, must-use plugin, and drop-in inventory.
- Cache, scheduled-task, mail, storage, TLS, DNS, and monitoring ownership.
- Backup and restore evidence.
- Access roles, approvers, and escalation contacts.
- Critical visitor and administrator journeys.

Do not execute WordPress or reveal secrets merely to complete an inventory.

## Inspector

Run help before using the included script:

```powershell
python .agents/plugins/wp-site-operations/skills/wp-site-operations-readiness/scripts/inspect-wordpress-site.py --help
```

The inspector is filesystem-only. It cannot prove active plugin state, database health, runtime scheduler behavior, provider backups, or production health.

## Workflow

Use [`workflows/assess-wordpress-operations-readiness-workflow.md`](workflows/assess-wordpress-operations-readiness-workflow.md).

## Resource

Use [`resources/environment-inventory-template.md`](resources/environment-inventory-template.md).

## Example

Use [`examples/readiness-report-example.md`](examples/readiness-report-example.md) for report structure, not as evidence for another site.

## Completion Evidence

Produce a dated readiness record with target, owners, access, versions, topology, recovery evidence, monitoring, critical journeys, change risk, unresolved blockers, and a clear go/no-go recommendation.
