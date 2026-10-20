---
name: "mindforge-list-workspaces"
description: "List active MindForge workspaces and their status"
---

<objective>
Scan `~/mindforge-workspaces/` for workspace directories containing `WORKSPACE.md` manifests. Display a summary table with name, path, repo count, strategy, and MindForge project status.
</objective>

<execution_context>
@.agent/workflows/mindforge-list-workspaces.md
@docs/References/ui-brand.md
</execution_context>

<process>
Execute the list-workspaces workflow from @.agent/workflows/mindforge-list-workspaces.md end-to-end.
</process>
