---
name: "mindforge-remove-workspace"
description: "Remove a MindForge workspace and clean up worktrees"
---

<context>
**Arguments:**
- `<workspace-name>` (required) — Name of the workspace to remove
</context>

<objective>
Remove a workspace directory after confirmation. For worktree strategy, runs `git worktree remove` for each member repo first. Refuses if any repo has uncommitted changes.
</objective>

<execution_context>
@.agent/workflows/mindforge-remove-workspace.md
@docs/References/ui-brand.md
</execution_context>

<process>
Execute the remove-workspace workflow from @.agent/workflows/mindforge-remove-workspace.md end-to-end.
</process>
