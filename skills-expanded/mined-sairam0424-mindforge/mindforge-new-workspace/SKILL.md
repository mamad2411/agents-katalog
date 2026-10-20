---
name: "mindforge-new-workspace"
description: "Create an isolated workspace with repo copies and independent .planning/"
---

<context>
**Flags:**
- `--name` (required) — Workspace name
- `--repos` — Comma-separated repo paths or names. If omitted, interactive selection from child git repos in cwd
- `--path` — Target directory. Defaults to `~/mindforge-workspaces/<name>`
- `--strategy` — `worktree` (default, lightweight) or `clone` (fully independent)
- `--branch` — Branch to checkout. Defaults to `workspace/<name>`
- `--auto` — Skip interactive questions, use defaults
</context>

<objective>
Create a physical workspace directory containing copies of specified git repos (as worktrees or clones) with an independent `.planning/` directory for isolated MindForge sessions.

**Use cases:**
- Multi-repo orchestration: work on a subset of repos in parallel with isolated MindForge state
- Feature branch isolation: create a worktree of the current repo with its own `.planning/`

**Creates:**
- `<path>/WORKSPACE.md` — workspace manifest
- `<path>/.planning/` — independent planning directory
- `<path>/<repo>/` — git worktree or clone for each specified repo

**After this command:** `cd` into the workspace and run `/mindforge-new-project` to initialize MindForge.
</objective>

<execution_context>
@.agent/workflows/mindforge-new-workspace.md
@docs/References/ui-brand.md
</execution_context>

<process>
Execute the new-workspace workflow from @.agent/workflows/mindforge-new-workspace.md end-to-end.
Preserve all workflow gates (validation, approvals, commits, routing).
</process>
