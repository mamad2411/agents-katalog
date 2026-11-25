---
name: gapt
description: Work with isolated, persistent GAPT project / workspace / sandbox spaces — create projects, run commands in sandboxes, and deploy. Use whenever the task needs an independent project space.
allowed_tools:
  - gapt_overview
  - gapt_list_projects
  - gapt_create_project
  - gapt_list_workspaces
  - gapt_create_workspace
  - gapt_manage_workspace
  - gapt_run_command
  - gapt_list_environments
  - gapt_deploy
execution_mode: inline
---

# GAPT — independent project & sandbox spaces

GAPT gives you **isolated, persistent project spaces** separate from this chat
session: a place to create code that persists, run builds in an isolated
container, or deploy — distinct from your own per-session workspace.

## Pick your path

- **You have the `gapt_*` tools** → do it yourself. Start with `gapt_overview`
  to see what exists, then create a project / workspace and work in it.
- **You do NOT have the `gapt_*` tools but have a `gapt` sub-worker** →
  delegate the whole GAPT task to it with a clear, self-contained instruction,
  then relay its result.

Each project is fully isolated and **persists across sessions**.

## Detailed tool reference

For the exact arguments, return values, and step-by-step recipes for each
`gapt_*` tool (create/list/run/deploy, polling workspace status, the
project→workspace→command→deploy flow), load the bundled reference on demand:
call this skill again with `resource="REFERENCE.md"`. Don't pull it unless you
need the specifics — the summary above covers the common case.

## Scope
Use this only for **separate, named, persistent project spaces** — not for
ordinary file/shell work in your current session (that's your normal
Read/Write/Bash / your own workspace).
