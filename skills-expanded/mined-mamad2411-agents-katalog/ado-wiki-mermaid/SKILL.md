---
name: ado-wiki-mermaid
description: >-
  Produce Azure DevOps Wiki-ready Mermaid diagrams and Markdown using the
  ::: mermaid container fence (not GitHub triple-backtick fences). Enforces
  ADO-safe dialect (graph not flowchart, short node IDs, no unsupported
  arrows/HTML). Use for Wiki pages, PR comments, and work-item descriptions
  that must render in Azure DevOps.
---

# Azure DevOps Wiki Mermaid

## Purpose

Generate diagrams and surrounding Markdown that render correctly in Azure
DevOps Wiki, PR comments, and work-item descriptions.

## Non-negotiable defaults

1. For ADO-bound content, use `::: mermaid` ... `:::` containers. Do **not** use GitHub-style triple-backtick `mermaid` fences.
2. Use ADO-safe dialect: `graph` not `flowchart`; short node IDs; no unsupported long arrows, HTML, Font Awesome, or subgraph links.
3. No em dashes anywhere in agent/skill output destined for ADO surfaces (labels, titles, prose, table cells).
4. Re-verify dialect against Microsoft Learn MCP for the target Azure DevOps Services or Server version at runtime.
5. Wiki-ready output is not permission to publish. Publishing requires explicit approval.

## Workflow

1. Confirm the destination (Wiki page, PR comment, work item) and platform version.
2. Read [references/wiki-mermaid.md](references/wiki-mermaid.md).
3. Emit at least current-state and target-state diagrams unless the user opts out.
4. Validate unique node IDs and declared references before delivery.
5. For Wiki publication: show full Markdown, confirm org/project/wiki/path, then apply only after approval.

## Authoritative reference

- Azure DevOps Wiki Markdown and Mermaid: `https://learn.microsoft.com/azure/devops/project/wiki/markdown-guidance?view=azure-devops`

Always retrieve the current version through Microsoft Learn MCP instead of relying only on this URL.
