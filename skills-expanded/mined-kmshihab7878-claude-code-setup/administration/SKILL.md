---
name: administration
description: n8n instance administration — data tables, folder management, community packages, Docker deployment, environment variables, backup/restore, upgrades, CLI commands, and troubleshooting. Operations the MCP does NOT cover. Auto-triggers on n8n data tables, n8n folders, move workflow, community packages, n8n setup, n8n upgrade, n8n backup, and n8n instance management tasks.
---

# n8n Administration

Use this skill for n8n instance administration that the MCP and public API do not fully cover: data tables, folders, community packages, infrastructure, backups, CLI, upgrades, and troubleshooting.

Source basis: n8n GitHub repository, master branch. Verified 2026-03-30.

## When This Skill Is Invoked

Use this skill when the user asks about:

- n8n data tables, columns, rows, filters, CSV import, or storage limits.
- n8n folders, moving workflows, folder deletion, or folder transfers.
- Community package installation, update, or removal.
- n8n Docker deployment, environment variables, worker mode, or upgrades.
- Backup, restore, database migration rollback, or CLI administration.
- Instance troubleshooting that is not workflow-building or node-schema work.

For workflow building, node search, execution management, health checks, template deployment, and workflow validation, prefer MCP tools. For credential CRUD and credential tests, use the [credentials skill](../credentials/SKILL.md).

## Tool Selection Order

Use the narrowest safe surface:

1. MCP for workflows, nodes, executions, templates, validation, and health checks.
2. Public API for API-key-supported data table row operations.
3. Internal API only when the public API lacks the needed admin operation.
4. CLI for exports, imports, database operations, user/auth resets, and local instance administration.
5. Docker or infrastructure changes for deployment, upgrades, worker mode, and environment configuration.

See [admin-workflow.md](references/admin-workflow.md) for the full routing table and endpoint catalogs.

## Required Input Contract

Collect or infer:

- n8n base URL or container/service context, using placeholders when documenting.
- Target operation and resource: data table, folder, workflow, package, backup, restore, upgrade, or instance setting.
- Auth surface available: MCP, API key, session cookie, CLI shell, or Docker access.
- Instance type: local, self-hosted Docker, queue/worker mode, or managed instance.
- Project ID, table ID, folder ID, workflow ID, package name, or target version when required.
- Backup and rollback state before any destructive or irreversible operation.
- Whether the operation touches credentials, decrypted exports, encryption keys, production data, or shared infrastructure.

Ask for explicit approval before T2/T3 operations such as destructive writes, credential export, full restore, migration rollback, license clearing, user reset, production upgrade, or shared infrastructure changes.

## Core Administration Workflow

1. Classify the task and risk level.
2. Choose the narrowest safe surface using the tool order above.
3. Inspect current state before changing anything.
4. Preserve secrets: never print credentials, encryption keys, session cookies, API keys, tokens, or decrypted credential exports.
5. For data changes, prefer preview modes such as `dryRun: true` when available.
6. For folders, understand whether deletion will flatten/archive workflows or transfer them.
7. For backups, upgrades, restore, rollback, or DB work, verify backup availability first.
8. Execute the smallest safe operation.
9. Validate through API response, CLI output, health check, workflow state, logs, or exported artifact inspection.
10. Report actions, evidence, assumptions, remaining risk, and recommended next step.

## Safety and Security Constraints

- Do not expose secrets, decrypted credential values, API keys, session cookies, database passwords, encryption keys, or private environment values.
- Do not use real local paths, hostnames, project names, account IDs, or private data in tracked docs.
- Do not run destructive operations without explicit approval.
- Treat `n8n export:credentials --decrypted`, `import:entities --truncateTables`, `db:revert`, `license:clear`, `user-management:reset`, full folder delete, and production upgrade as approval-gated.
- Preserve `N8N_ENCRYPTION_KEY`; losing or changing it can invalidate credentials.
- Use placeholders such as `<n8n-url>`, `<container>`, `<project-id>`, `<table-id>`, `<folder-id>`, `<workflow-id>`, `<package-name>`, and `<backup-dir>`.
- Flag source-control protected instances, enterprise-only folder features, internal API session-cookie requirements, and production/shared-instance risk.
- Keep public-safety checks, validation, secret scanning, and approval posture intact.

See [security-and-validation.md](references/security-and-validation.md) for detailed safeguards, preflight checks, and review checklists.

## Validation Rules

Before completion, verify the operation with the most relevant evidence:

- API response, status code, returned IDs, counts, or `dryRun` result.
- CLI exit status and concise output summary without secret values.
- Health check: MCP `n8n_health_check` or `curl -s "<n8n-url>/healthz"`.
- Docker status, logs, or service restart confirmation for infrastructure work.
- Backup artifact existence before restore, upgrade, rollback, or migration work.
- Workflow active state, folder location, package installed state, or data table row count when applicable.

If validation fails, diagnose and fix the cause before claiming completion.

## Output Expectations

Report:

- Operation performed and risk tier.
- Surface used: MCP, public API, internal API, CLI, or Docker/infra.
- Inputs and placeholders used.
- Safety checks performed, including approval requirements and secret handling.
- Validation evidence.
- Any changes made, rollback path, and remaining risks.

## Minimal Critical Examples

Use placeholders and approval gates:

```bash
# Health check
curl -s "<n8n-url>/healthz"

# Non-secret workflow export
docker exec <container> n8n export:workflow --all --output=<backup-dir>/workflows.json

# Destructive full restore requires explicit approval first
docker exec <container> n8n import:entities --inputDir=<backup-dir> --truncateTables
```

## Reference Map

- Routing, data table endpoints, folder endpoints, community packages, and admin workflow: [admin-workflow.md](references/admin-workflow.md)
- CLI commands, Docker recipes, environment variables, backups, restores, upgrades: [commands-and-recipes.md](references/commands-and-recipes.md)
- Security rules, destructive-operation gates, validation checklists: [security-and-validation.md](references/security-and-validation.md)
- Troubleshooting matrix and gotchas: [troubleshooting.md](references/troubleshooting.md)
- Public-safe command and output examples: [examples.md](references/examples.md)
