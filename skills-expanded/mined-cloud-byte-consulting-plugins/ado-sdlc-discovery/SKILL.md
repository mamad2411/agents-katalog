---
name: ado-sdlc-discovery
description: >-
  Read-only Azure DevOps full-SDLC discovery using Azure CLI and the
  azure-devops extension first, Azure DevOps MCP only for gaps, and
  Microsoft Learn MCP for product behavior questions. Inventories projects,
  teams, repos, branch policies, pipelines, boards, environments, service
  connections, artifacts, test plans, and wiki. Use for Azure DevOps audits,
  brownfield CI/CD discovery, and evidence gathering before architecture work.
---

# Azure DevOps SDLC Discovery

## Purpose

Collect verifiable evidence about an Azure DevOps organization and project
before prescribing CI/CD architecture. Discovery is read-only.

## Non-negotiable defaults

1. Discover before prescribing. Do not design from assumptions when live data is available.
2. Keep discovery read-only. Never create, update, queue, approve, or delete Azure DevOps resources without explicit user approval.
3. Tool order: **Azure CLI + `azure-devops` extension first**; Azure DevOps MCP only for gaps or when CLI is unavailable; Microsoft Learn MCP for current product behavior (not as live org evidence).
4. Distinguish observed facts, access gaps, and not-assessed areas.
5. Never interpret an authorization failure, missing tool, or incomplete result as proof that a resource does not exist.
6. No em dashes in ADO-facing notes or pasted evidence summaries.

## Required context

Establish before detailed discovery:

- Azure DevOps organization URL
- Project or portfolio scope
- Azure DevOps Services or Azure DevOps Server version
- Teams and repositories in scope
- Assessment window for pipeline, pull request, and work-item metrics

Verify CLI context without exposing credentials:

```bash
az account show --output json
az extension show --name azure-devops --output json
az devops configure --list
```

Use explicit placeholders:

```text
ORG=https://dev.azure.com/<organization>
PROJECT=<project>
```

Do not print or inspect PAT environment variables.

## Workflow

1. Confirm scope and exclusions.
2. Read [references/discovery.md](references/discovery.md) and execute the CLI-first sequence.
3. Cover planning, code, integration, testing, artifacts, delivery, security, operations, metrics, and documentation.
4. Query narrowly first; expand based on evidence. Avoid large logs or full repo trees until a finding requires them.
5. Emit an evidence pack: inventory tables, policy coverage, pipeline shape, board/PR process notes, access gaps, and not-assessed domains.

## Safety

- Do not queue builds as a discovery technique.
- Do not update a Wiki because Wiki-ready output was requested later.
- Never display tokens, service-connection credentials, variable-group secrets, secure-file contents, or secret-bearing logs.
- Report permission boundaries and partial coverage explicitly.
