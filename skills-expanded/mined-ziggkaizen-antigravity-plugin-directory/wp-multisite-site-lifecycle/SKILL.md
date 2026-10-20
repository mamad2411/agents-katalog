---
name: wp-multisite-site-lifecycle
description: Plans and reviews WordPress Multisite site creation, status changes, ownership, domain mapping, migration, import, export, retirement, and deletion. Use for any operation that changes a subsite's lifecycle or identity.
---

# WordPress Multisite Site Lifecycle

Use this skill for site creation, activation, deactivation, archive/spam state, domain or path changes, import/export, migration, ownership transfer, retirement, emptying, or deletion.

## Core Principles

- Resolve both site ID and canonical URL before mutation.
- Separate reversible status changes from destructive content/table removal.
- Inventory users, owners, domains, uploads, plugins, themes, cron, integrations, and retention obligations.
- Prefer archive or deactivate before delete when requirements are uncertain.
- Keep exports and backups until retention and restore validation are complete.
- Treat domain changes as DNS/TLS/cookie/cache/redirect changes, not only a database edit.

## Workflow

Use `workflows/site-lifecycle-workflow.md`.

## Resource

Use `resources/site-lifecycle-checklist.md`.

## Example

Use `examples/site-retirement-plan.md`.
