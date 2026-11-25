---
name: wp-cli-2-operations
description: Runs safe WordPress database and maintenance operations with WP-CLI 2. Use when planning exports, imports, queries, search-replace, core/plugin/theme updates, database schema updates, rollback, cache work, cron checks, or post-change verification.
license: MIT
compatibility: Requires WP-CLI 2.x; guidance is validated against WP-CLI 2.12.0.
---

# WP-CLI 2 Operations

Use this skill for operational changes after the target and command risk have been established.

## Operating Principles

- Start with read-only inventory and health checks.
- Use application-aware commands before direct SQL.
- Export the database before destructive or broad data mutations.
- Treat database export presence as insufficient until the destination and restore path are verified.
- Do not invent dry-run flags. Use official preview support where documented.
- Plan rollback before core/plugin/theme/database changes.
- Verify both WP-CLI state and user-visible application behavior.

## Database Guidance

- Use `wp db export` for a pre-change export and protect the resulting file.
- Use `wp search-replace ... --dry-run` before mutation; review table, network, and column scope.
- Use `wp db query` read-only queries for targeted inspection. Treat input from files, redirects, substitutions, or unknown custom SQL as unclassified until reviewed.
- Treat imports and schema/data-changing SQL as destructive.
- Never use a database password as a literal command-line argument.

## Update Guidance

- Inventory available/current versions before changing anything.
- Use plugin/theme update dry runs when supported.
- Core updates require separate preflight because `wp core update` has no equivalent dry-run.
- Account for maintenance mode, PHP/WordPress compatibility, database migrations, caches, cron, and rollback artifacts.

## Workflows

- [Database change workflow](workflows/database-change-workflow.md)
- [Update and rollback workflow](workflows/update-and-rollback-workflow.md)

## Resource

- [Operations verification checklist](resources/operations-verification-checklist.md)
