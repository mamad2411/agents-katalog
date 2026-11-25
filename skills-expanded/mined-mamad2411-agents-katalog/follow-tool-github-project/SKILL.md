---
name: follow-tool-github-project
description: Manage GitHub Projects via the `gh project` CLI, interactively and scripted
argument-hint: "[scope]"
related:
  - list-github
  - delete
---

## Goal

Use `gh project` to create, view, edit, and manage items/fields in GitHub Projects via the CLI, choosing interactive mode or flags per situation

## Scope
- For related skills: `list-github`

Works with GitHub Projects (Projects v2) of a user, organization, or linked repository; it does not directly cover `gh issue` or `gh pr`

- Latest: `gh@2.101.0` (github.com/cli/cli, verified 2026-09-26)
- References: [cli](references/cli.md) | [apis](references/apis.md) 
## Execute

### 0. Setup

> Goal: install the `gh` CLI and log in

1. Install `gh`:
   - `mise use -g gh`
   - or `brew install gh`
   - or Windows: `winget install --id GitHub.cli`
   - or Linux: `apt install gh`
2. Verify: `gh --version`
3. Login: `gh auth login`
4. Request the `project` scope: `gh auth refresh -s project`
5. If install fails → run `/deep-research setup gh`

### 1. Verify Authentication And Scope

> Goal: check permissions before using `gh project`

1. Run `gh auth status` to verify current scopes
2. If the `project` scope is missing, run `gh auth refresh -s project`
3. If not logged in yet, run `gh auth login` first

### 2. List And View Projects

> Goal: find and inspect projects

1. Run `gh project list --owner "@me"` to see your own projects
2. Run `gh project list --owner <org>` to see an organization's projects
3. Run `gh project view <number>` to see a project in the terminal
4. Run `gh project view <number> --web` to open it in the browser

### 3. Create And Edit Projects

> Goal: create or tune a project

1. Run `gh project create --title "<title>" --owner "@me"` to create a project
2. On a TTY without the required flags, `gh` prompts interactively
3. Run `gh project edit <number> --title "<title>"` to change the title
4. Run `gh project edit <number> --description "<desc>" --visibility PUBLIC` to change details
5. Run `gh project close <number>` or `gh project close <number> --undo` to close/reopen a project
6. Use `gh project copy <number>` to duplicate a project and `gh project mark-template <number>` to make it a template
7. Use `gh project link <number> <repo>` / `gh project unlink <number> <repo>` to link/unlink a repo
8. Never delete a project with `gh project delete <number>` without user permission

### 4. Manage Project Items

> Goal: add, remove, or edit items in a project

1. Run `gh project item-list <number> --owner "@me"` to see items
2. Run `gh project item-list <number> --query "assignee:@me is:open"` to filter items
3. Run `gh project item-add <number> --url <issue-or-pr-url>` to add an issue/PR to the project
4. Run `gh project item-create <number> --title "<title>" --body "<body>"` to create a draft item
5. Use `gh project item-edit --id <item-id> --field-id <field-id> --project-id <project-id> --text "..."` to edit an item's field
   - Or the name-based form (no node IDs needed): `gh project item-edit <number> --owner "@me" --url <issue-or-pr-url> --field "Status" --value "In Progress"` — `--field`/`--field-id`, `--url`/`--id`, `--value`/typed flags cannot be combined
6. Run `gh project item-archive <number> --id <item-id>` or `gh project item-archive <number> --id <item-id> --undo`
7. Run `gh project item-delete <number> --id <item-id>` with caution

### 5. Inspect And Create Fields

> Goal: view or create custom fields

1. Run `gh project field-list <number> --owner "@me"` to see fields and field IDs
2. Run `gh project field-create <number> --name "<name>" --data-type "TEXT"` to create a field — data types: `TEXT`, `SINGLE_SELECT`, `DATE`, `NUMBER`; for SINGLE_SELECT add `--single-select-options "a,b,c"`
3. Run `gh project field-delete <number> --id <field-id>` when a field must be removed (destructive — ask the user first)
4. Use field IDs from the JSON output to reference them in `item-edit`

### 6. Use Output And Automation

> Goal: use `gh project` output in scripts

1. Use `--format json` or `-q/--jq <expression>` to get JSON output (`gh project` uses `--format`, not `--json`)
2. Use `-t/--template "<go-template>"` to format output
3. Use `gh project item-list <number> --query "..."` to filter items with Projects syntax
4. For automation, specify all flags and never rely on interactive prompts

## Rules

### 1. Authentication

- `gh project` requires the token `project` scope before use
- Verify with `gh auth status`, then run `gh auth refresh -s project` if it's missing

### 2. Owner And Project Number

- Use `--owner "@me"` for the current user
- Use `--owner <org>` for an organization
- Many commands take the project `number` (per-owner sequence), not the GraphQL ID

### 3. Interactive Mode

- On a TTY with missing required flags, `gh` shows an interactive prompt
- In scripts or CI, specify all flags to avoid interactive prompts
- Use `--web` to open the project page in the browser when needed

### 4. Item And Field IDs

- `item-edit` supports two modes: ID-based (`--id`, `--field-id`, `--project-id`) or name-based (`<number>` + `--owner` + `--url` + `--field` + `--value`); `field-delete` requires `--id`
- Use `--format json` with `item-list` or `field-list` to pull exact IDs
- Use `--text`, `--number`, `--date`, `--single-select-option-id`, `--iteration-id`, `--clear` per field type

### 5. Safety

- Project delete/close commands (`delete`, `close`) are destructive — ask the user first — follow the `/delete` flow
- Verify owner and project number before deleting/closing
- Use `gh project close <number> --undo` instead of deleting when the goal is temporary hiding

- Use `/list-github` to find the project number/owner before running commands
- Use the `/delete` flow for destructive commands (`delete`, `close`)

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Able to create, view, edit, and manage GitHub Projects via `gh project`
- Works both interactively (TTY) and scripted (flags)
- Token has the `project` scope and the owner is specified correctly
- No project is deleted or closed without permission

