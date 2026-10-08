---
name: forge-mcp
description: >-
  Use Forge MCP tools to create and manage Sarray Forge issues from repo work.
  Trigger when the user asks to file Forge issues, triage commits into issues,
  or use forge_create_issue / forge_search MCP tools.
---

# Forge MCP Workflow

## Prerequisites

1. Create an API key in Forge: **Settings → API Keys**
2. Global MCP config at `~/.cursor/mcp.json` (or project `.cursor/mcp.json`)
3. Set `FORGE_TOKEN` to the `forge_…` secret (never commit it)
4. Set `FORGE_WORKSPACE` to the default workspace key (e.g. `FORGE`)

## Workspace selection

Every workspace-scoped tool accepts an optional `workspace` param (e.g. `"ALFA"`, `"FORGE"`). When omitted, `FORGE_WORKSPACE` from env is used. No config change needed to work across workspaces in one session.

## When to create issues from repo work

Use this workflow when the user wants follow-up tasks tracked in Forge after code changes:

1. Inspect git history or diffs (`git log`, `git diff`, read changed files)
2. Call `forge_search` for each candidate title to avoid duplicates
3. Call `forge_list_users` in the target workspace to resolve assignee IDs
4. Call `forge_create_issue` with:
   - **title**: concise action item
   - **description**: markdown with commit SHA, file links, and context
   - **labels**: include `agent` when created by automation
   - **priority**: `high` for bugs/regressions, `medium` for normal follow-ups
   - **workspace**: target workspace key when not the default

## Available MCP tools

| Tool | Use for |
|------|---------|
| `forge_list_workspaces` | Discover workspace keys |
| `forge_list_users` | Workspace members (assignee lookup) |
| `forge_list_all_users` | All active users (admin) |
| `forge_list_issues` | See existing board items (optional `parentId` or `"root"`) |
| `forge_get_issue` | Read one issue before updating (by ID or code) |
| `forge_create_issue` | File new work (labels, priority, assignee, `parentId`) |
| `forge_update_issue` | Change status, assignee, labels, parent, etc. |
| `forge_delete_issue` | Remove an issue (optional `cascade`) |
| `forge_list_docs` | List docs (optional `parentId` or `"root"`) |
| `forge_get_doc` | Read doc by ID or slug |
| `forge_create_doc` | Create documentation page |
| `forge_update_doc` | Edit doc title/content/parent |
| `forge_delete_doc` | Remove a doc |
| `forge_search` | Dedup before creating |
| `forge_create_invite` | Generate expiring invite link for new user (admin) |
| `forge_list_invites` | List pending invites (admin) |
| `forge_revoke_invite` | Cancel a pending invite (admin) |
| `forge_add_workspace_member` | Add existing user to workspace (admin) |

All scoped tools accept optional `workspace` (defaults to `FORGE_WORKSPACE` env).

Issue tools accept either the numeric `id` (`47`) or the human-readable code shown in the UI and URLs (`"FORGE-12"`). A code already names its workspace, so `forge_get_issue({ id: "ALFA-3" })` resolves in `ALFA` without passing `workspace`. Note `forge_move_issue`'s `beforeId`/`afterId` remain numeric ids.

## Subtickets

Break a large issue into subtickets by passing `parentId` — either on
`forge_create_issue` for new work, or on `forge_update_issue` to adopt an issue
that already exists. `forge_update_issue({ parentId: null })` detaches one.

**Nesting is one level deep.** A subticket cannot have subtickets of its own, and
an issue that already has subtickets cannot be given a parent; both come back as
a 400. Plan the split one level at a time rather than building a tree.

A subticket is a full issue — its own code, status, assignee and comments — so
list and read them exactly like any other. `forge_list_issues({ parentId: 12 })`
returns one issue's subtickets; `{ parentId: "root" }` returns only top-level
issues. Deleting a parent leaves its subtickets behind as top-level issues unless
you pass `cascade: true`.

## Onboarding new users

1. Call `forge_create_invite` with `username`, `workspaceKeys`, optional `fullName` and `expiresInDays` (1 or 2)
2. Share the returned `inviteUrl` with the new team member
3. They open the link, set a password, and land in their workspace

For existing users who need access to another workspace, use `forge_add_workspace_member`.

## Example issue description

```markdown
## Context
Follow-up from commit abc1234.

## Changes reviewed
- `internal/handlers/workspace.go` — workspace scoping

## Suggested work
- Add integration test for invalid workspace header
```

## Example: create issue in ALFA with labels

```json
{
  "workspace": "ALFA",
  "title": "Fix barcode scan",
  "description": "Regression in POS module",
  "labels": ["bug", "agent"],
  "priority": "high",
  "assigneeId": 1
}
```

## Do not

- Store API keys in the repository
- Create duplicate issues without searching first
- Use browser login/session cookies for automation — use API keys
