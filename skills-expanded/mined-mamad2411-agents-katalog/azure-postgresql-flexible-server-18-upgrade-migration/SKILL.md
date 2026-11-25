---
name: azure-postgresql-flexible-server-18-upgrade-migration
description: Plans and reviews migrations or major-version upgrades to Azure Database for PostgreSQL Flexible Server 18. Use for upgrade rehearsals, PITR clones, extension compatibility, dump/restore, logical replication, cutover, rollback, and post-upgrade validation.
license: MIT
compatibility: Requires Azure CLI for Azure upgrade planning. Optional psql is needed for database compatibility checks.
---

# Azure PostgreSQL Flexible Server 18 Upgrade and Migration

## When to Use This Skill

Use this skill for:

- Upgrading an existing Flexible Server to PostgreSQL 18.
- Migrating another PostgreSQL workload to Azure Flexible Server 18.
- Reviewing extension compatibility.
- Planning dump/restore, logical replication, or application cutover.
- Validating post-upgrade behavior.

## Core Guidance

- Treat production major-version upgrades as high-risk and irreversible for the upgraded server.
- Always rehearse on a restored nonproduction copy.
- Confirm extension compatibility before upgrade or migration.
- Confirm application, driver, ORM, query, function, procedure, and migration compatibility with PostgreSQL 18.
- Validate backup and restore before cutover.
- Ensure rollback criteria are explicit.

## Workflows

- [major-version-upgrade-to-18-workflow](workflows/major-version-upgrade-to-18-workflow.md)
- [migration-cutover-workflow](workflows/migration-cutover-workflow.md)

## Resources

- [upgrade-safety-checklist.md](resources/upgrade-safety-checklist.md)

## Scripts

- `scripts/check-extension-compatibility.sh`

## Examples

- [pre-upgrade-sql-checks.sql](examples/pre-upgrade-sql-checks.sql)
