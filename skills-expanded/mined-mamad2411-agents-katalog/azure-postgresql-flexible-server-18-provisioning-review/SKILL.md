---
name: azure-postgresql-flexible-server-18-provisioning-review
description: Reviews Azure Database for PostgreSQL Flexible Server 18 provisioning plans and existing server configuration. Use when checking Azure CLI, Bicep, ARM, Terraform, portal settings, version, SKU, storage, HA, backup, tags, authentication, networking, and production readiness.
license: MIT
compatibility: Requires Azure CLI for Azure resource checks. Optional psql is useful for database-level validation.
---

# Azure PostgreSQL Flexible Server 18 Provisioning Review

## When to Use This Skill

Use this skill when the task involves:

- Creating or reviewing a PostgreSQL 18 Flexible Server.
- Reviewing Azure CLI, Bicep, ARM, Terraform, or portal-equivalent settings.
- Validating an existing server against expected version, security, HA, backup, storage, and tagging policy.
- Checking whether planned commands are risky before execution.

## Core Guidance

- Confirm the service is Azure Database for PostgreSQL Flexible Server.
- Confirm the target PostgreSQL major version is `18`.
- Prefer private access and avoid broad public access.
- Require backup and restore-test policy before production launch.
- Make HA, zone, storage, maintenance window, authentication, tags, and monitoring explicit.
- Keep application-specific component names out of this technology plugin.
- Run included scripts with `--help` before use.

## Workflows

- [provisioning-review-workflow](workflows/provisioning-review-workflow.md): Use to review a new or changed provisioning plan.
- [configuration-validation-workflow](workflows/configuration-validation-workflow.md): Use to validate an existing Flexible Server with read-only checks.

## Resources

- [provisioning-review-checklist.md](resources/provisioning-review-checklist.md)
- [mcp-toolbox-postgres-readonly.example.yaml](resources/mcp-toolbox-postgres-readonly.example.yaml)

## Examples

- [private-server-cli-example.md](examples/private-server-cli-example.md)

## Scripts

- `scripts/validate-server-configuration.sh`: Read-only Azure CLI validation for existing server settings.
- `scripts/review-run-command.sh`: Hook helper that checks planned shell commands for version, public access, backup, and destructive-operation risks.
