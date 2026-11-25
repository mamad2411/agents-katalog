---
name: wp-multisite-update-and-rollback
description: Plans and reviews WordPress Multisite Core, plugin, theme, network database, configuration, and deployment updates with canaries, backups, rollback, and command gating. Use before shared-code or network-wide changes.
---

# WordPress Multisite Update and Rollback

Use this skill for shared WordPress Core, plugin, theme, must-use plugin, network database, deployment, or configuration updates.

## Update Order

Choose an order based on official compatibility guidance and project evidence. A common controlled flow is:

1. inventory and health baseline
2. full backup plus tested restore
3. staging update
4. compatibility and data-change review
5. representative canary validation
6. shared code deployment
7. network database dry run when supported
8. approved network database update
9. cache and cron verification
10. network-wide validation and observation

Do not treat code rollback as sufficient when an update changes data or schema.

## Command Guard

The root `hooks.json` calls:

```text
scripts/guard-wp-multisite-command.py
```

The guard is conservative. It allows obvious read-only WP-CLI commands and asks for approval around destructive, privilege-changing, topology-changing, network-wide, or database-mutating commands.

Run it with `--help` before manual use.

## Workflow

Use `workflows/network-update-workflow.md`.

## Resource

Use `resources/network-update-runbook-template.md`.
