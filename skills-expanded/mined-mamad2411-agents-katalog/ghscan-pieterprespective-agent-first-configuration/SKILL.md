# Jira CLI Skill — Implementation Files

This document contains the complete contents of every file to create. Each section is a file
with its target path relative to the project root. Copy each file to its path, then fill in
the project-specific placeholders in `.jira-config.md`.

---

## 1. Skill: `jira-manage/SKILL.md`

```markdown
---
name: jira-manage
description: >
  Manage Jira Cloud issues via jira-cli bash commands. Use this skill when the task involves:
  creating Jira issues or subtasks, updating issue descriptions or fields, adding comments to issues,
  querying/searching issues with JQL, setting or validating component fields, or any Jira project
  management operation. Triggers on mentions of "Jira", "ticket", "issue", "subtask", "sprint",
  "component", or Jira issue keys (e.g., PROJ-123).
---

# Jira Issue Management via jira-cli

Manage Jira Cloud issues using the `jira-w` wrapper command through Bash.

## Security Model

Authentication is handled entirely outside the agent context:
- A wrapper script `jira-w` reads the API token from a local credential file and injects it
  into the environment only for the `jira` child process.
- **Never** attempt to read, echo, print, or reference the token file, its path, or its contents.
- **Never** attempt to read `~/.config/.jira.yml`, `%APPDATA%\.jira.yml`, or any auth config.
- **Never** run `echo $JIRA_API_TOKEN` or equivalent — the token must not appear in output.
- If auth fails (401 errors), tell the user to re-run `jira init` or regenerate their token
  externally. Do not attempt to debug auth yourself.

All commands use `jira-w` (not `jira` directly).

## Prerequisites

- `jira-w` wrapper installed and on PATH (see `scripts/` for reference copies)
- `jira init` completed externally (one-time setup)
- Project-specific config in `.jira-config.md` at project root

## Before Any Operation

1. Read `.jira-config.md` from the project root for project keys, valid components, conventions.
2. For full CLI syntax, read `references/cli-ref.md` in this skill directory.

## Core Operations

### Query Issues

```bash
jira-w issue list -q "<JQL>" --plain --columns key,summary,status,assignee,priority
```

Always use `--plain` for machine-readable output. Use `--no-headers` when parsing.

### Create Issue

```bash
jira-w issue create \
  -t"<Type>" \
  -s"<Summary>" \
  -b"<Description>" \
  -C"<Component>" \
  -p <PROJECT_KEY> \
  --no-input
```

- **Type**: `Task`, `Bug`, `Story`, `Epic` (case-sensitive, project-dependent)
- **Component**: Must match a valid component from `.jira-config.md` — verify before using
- `--no-input` is mandatory to prevent interactive prompts

### Create Subtask

```bash
jira-w issue create \
  -t"Sub-task" \
  -P"<PARENT-KEY>" \
  -s"<Summary>" \
  -b"<Description>" \
  -C"<Component>" \
  -p <PROJECT_KEY> \
  --no-input
```

- Type must be exactly `Sub-task` (hyphenated, capital S and lowercase t)
- `-P` (capital P) sets the parent issue key

### Update Description

```bash
jira-w issue edit <ISSUE-KEY> -b"<New description>" --no-input
```

### Add Comment

```bash
jira-w issue comment add <ISSUE-KEY> -b"<Comment body>"
```

### Set/Change Component

```bash
jira-w issue edit <ISSUE-KEY> --component "<ComponentName>" --no-input
```

## Error Handling

- Non-zero exit codes indicate failure — check stderr
- If stderr contains "401 Unauthorized": tell the user their token may have expired
- If stderr contains "not valid" for a component: list valid components from `.jira-config.md`
- If `jira-w` reports "token file not found": tell the user to run the setup procedure
- Never retry auth-related failures silently

## Output Guidelines

- Return concise results: issue key, summary, and status
- For queries: compact table, max 20 results unless asked for more
- Never include raw JSON API responses
- Always confirm create/update operations with the resulting issue key

## Platform Notes

- On Unix (Linux/macOS): `jira-w` is a bash script
- On Windows: `jira-w` or `jira-w.cmd` is a batch script
- Both behave identically — always invoke as `jira-w` (shell resolves the extension on Windows)
```

---

## 2. Wrapper Script (Unix): `jira-manage/scripts/jira-w`

> **Note:** These wrapper scripts will be extended in Phase 0b (see `ELOM-15-P0_B-component-retrieval.md`)
> to add a `--components <PROJECT_KEY>` subcommand that queries the Jira REST API directly,
> since jira-cli has no built-in component listing command.

```bash
#!/usr/bin/env bash
# jira-w — Wrapper for jira-cli that reads the API token from a secure file.
# Install to ~/.local/bin/jira-w and ensure ~/.local/bin is on PATH.
#
# Token file: ~/.config/jira-skill/token
# Permissions: chmod 600
#
# The token is injected into the environment ONLY for the jira child process
# via exec. It never exists in the parent shell's environment.

set -euo pipefail

TOKEN_FILE="${HOME}/.config/jira-skill/token"

if [[ ! -f "$TOKEN_FILE" ]]; then
  echo "ERROR: Jira token file not found at ${TOKEN_FILE}" >&2
  echo "" >&2
  echo "Setup:" >&2
  echo "  mkdir -p ~/.config/jira-skill" >&2
  echo "  echo -n 'YOUR_API_TOKEN' > ~/.config/jira-skill/token" >&2
  echo "  chmod 600 ~/.config/jira-skill/token" >&2
  exit 1
fi

# Verify permissions (warn if too open, but don't block)
if [[ "$(uname)" != "MINGW"* ]] && [[ "$(uname)" != "MSYS"* ]]; then
  PERMS=$(stat -f "%Lp" "$TOKEN_FILE" 2>/dev/null || stat -c "%a" "$TOKEN_FILE" 2>/dev/null || echo "unknown")
  if [[ "$PERMS" != "600" ]] && [[ "$PERMS" != "unknown" ]]; then
    echo "WARNING: Token file permissions are ${PERMS}, expected 600. Run: chmod 600 ${TOKEN_FILE}" >&2
  fi
fi

export JIRA_API_TOKEN
JIRA_API_TOKEN="$(cat "$TOKEN_FILE")"
exec jira "$@"
```

---

## 3. Wrapper Script (Windows): `jira-manage/scripts/jira-w.cmd`

```batch
@echo off
REM jira-w.cmd — Wrapper for jira-cli that reads the API token from a secure file.
REM Install to %LOCALAPPDATA%\jira-skill\jira-w.cmd and add that directory to user PATH.
REM
REM Token file: %APPDATA%\jira-skill\token
REM Permissions: icacls "%APPDATA%\jira-skill\token" /inheritance:r /grant:r "%USERNAME%:(R,W)"

setlocal EnableDelayedExpansion

set "TOKEN_FILE=%APPDATA%\jira-skill\token"

if not exist "%TOKEN_FILE%" (
    echo ERROR: Jira token file not found at %TOKEN_FILE% >&2
    echo. >&2
    echo Setup ^(PowerShell^): >&2
    echo   New-Item -ItemType Directory -Force -Path "$env:APPDATA\jira-skill" >&2
    echo   Set-Content -Path "$env:APPDATA\jira-skill\token" -Value "YOUR_API_TOKEN" -NoNewline >&2
    echo   icacls "$env:APPDATA\jira-skill\token" /inheritance:r /grant:r "$env:USERNAME:(R,W)" >&2
    exit /b 1
)

set /p JIRA_API_TOKEN=<"%TOKEN_FILE%"
jira %*
set "JIRA_API_TOKEN="
endlocal
```

---

## 4. Reference: `jira-manage/references/cli-ref.md`

```markdown
# jira-cli Command Reference

Complete syntax for all Jira operations used by this skill.
Read this file when you need exact flag names, option syntax, or edge-case handling.

## Authentication Context

Auth is handled by the `jira-w` wrapper script. It reads a token from a platform-specific
credential file and injects it for the `jira` child process only.

- **Unix token file**: `~/.config/jira-skill/token`
- **Windows token file**: `%APPDATA%\jira-skill\token`
- **jira config**: `~/.config/.jira.yml` (Unix) / `%APPDATA%\.jira.yml` (Windows)

**Never read, echo, or reference these files or their contents.**

## Issue Creation

```
jira-w issue create [flags]
```

| Flag | Short | Description | Required |
|------|-------|-------------|----------|
| `--type` | `-t` | Issue type: Task, Bug, Story, Epic, Sub-task | Yes |
| `--summary` | `-s` | Issue title | Yes |
| `--body` | `-b` | Description (Markdown supported) | No |
| `--component` | `-C` | Component name (must exist in project) | No* |
| `--project` | `-p` | Project key (overrides default) | No |
| `--priority` | `-y` | Priority: Highest, High, Medium, Low, Lowest | No |
| `--assignee` | `-a` | Assignee (account ID or "Default") | No |
| `--label` | `-l` | Label (repeatable for multiple) | No |
| `--parent` | `-P` | Parent issue key (required for Sub-task) | Sub-task |
| `--no-input` | | Disable interactive prompts | Always use |
| `--custom` | | Custom field: `--custom "field=value"` | No |

*Required by team convention for subsidy logging — see `.jira-config.md`.

### Multi-value fields

```bash
# Multiple components
jira-w issue create -t"Task" -s"Title" -C"Backend" -C"API" --no-input

# Multiple labels
jira-w issue create -t"Task" -s"Title" -l"sprint-12" -l"tech-debt" --no-input
```

### Subtask creation

Type string must be exactly `Sub-task` (hyphenated, capital S):

```bash
jira-w issue create -t"Sub-task" -P"PROJ-100" -s"Subtask title" -p PROJ --no-input
```

## Issue Editing

```
jira-w issue edit <ISSUE-KEY> [flags]
```

| Flag | Short | Description |
|------|-------|-------------|
| `--body` | `-b` | Replace description |
| `--summary` | `-s` | Replace summary/title |
| `--component` | | Set component (replaces existing) |
| `--priority` | `-y` | Change priority |
| `--assignee` | `-a` | Change assignee |
| `--label` | `-l` | Set labels |
| `--no-input` | | Disable interactive prompts |

Remove a component by prefixing with `-`:

```bash
jira-w issue edit PROJ-123 --component "Backend" --component "-Frontend" --no-input
```

## Comments

```bash
# Add comment
jira-w issue comment add <ISSUE-KEY> -b"Comment text here"

# List comments (last 10)
jira-w issue comment list <ISSUE-KEY> --plain
```

## Querying / Searching

```bash
jira-w issue list -q "<JQL>" [flags]
```

| Flag | Description |
|------|-------------|
| `-q` | JQL query string |
| `--plain` | Machine-readable output (no colors/borders) |
| `--no-headers` | Omit column headers |
| `--columns` | Comma-separated: key,summary,status,type,priority,assignee,reporter,created,updated,resolution |
| `-a <N>` | Max results (default: 20, `-a0` for unlimited) |
| `-p <KEY>` | Filter by project (alternative to JQL project clause) |

### Common JQL patterns

```bash
# Open issues in project
jira-w issue list -q "project = PROJ AND status != Done" --plain

# My open issues
jira-w issue list -q "assignee = currentUser() AND status != Done" --plain

# Recently updated
jira-w issue list -q "project = PROJ AND updated >= -7d ORDER BY updated DESC" --plain

# By component
jira-w issue list -q "project = PROJ AND component = Backend" --plain

# Subtasks of an issue
jira-w issue list -q "parent = PROJ-100" --plain

# Unresolved high-priority bugs
jira-w issue list -q "project = PROJ AND type = Bug AND priority in (High, Highest) AND resolution = Unresolved" --plain
```

## Viewing a Single Issue

```bash
jira-w issue view <ISSUE-KEY> --plain
```

## Transitions

```bash
# List available transitions
jira-w issue move <ISSUE-KEY> --list

# Move to status
jira-w issue move <ISSUE-KEY> "In Progress"
```

## Project Info

```bash
# List all accessible projects
jira-w project list --plain
```

Note: `jira-cli` has no dedicated component-list command. Maintain valid components
in `.jira-config.md` or use the project config template to document them.

## Exit Codes & Error Patterns

| Pattern in stderr | Meaning | Action |
|-------------------|---------|--------|
| "401 Unauthorized" | Token expired or invalid | Tell user to regenerate token |
| "Component name '...' is not valid" | Bad component | List valid ones from config |
| "Issue type '...' is not valid" | Wrong type string | Check case: `Sub-task` not `Subtask` |
| "token file not found" | Wrapper can't find credential file | Tell user to run setup |
| "Project '...' does not exist" | Bad project key | Check `.jira-config.md` |
```

---

## 5. Reference: `jira-manage/references/project-config-template.md`

```markdown
# Project Jira Configuration Template

Copy this file to `.jira-config.md` at your project root and fill in the values.
This file is read by the Jira skill to know which projects, components, and conventions apply.
This file contains NO credentials — it is safe to commit to version control.

---

## Projects

| Key | Name | Default Issue Type |
|-----|------|--------------------|
| PROJ | My Project | Task |

## Valid Components (per project)

### PROJ

Components must match exactly (case-sensitive). The component field is **required** for
all issues to support subsidy logging.

| Component | Description |
|-----------|-------------|
| Backend | Server-side code, APIs, databases |
| Frontend | Client-side code, UI components |
| DevOps | CI/CD, infrastructure, deployment |
| Documentation | Docs, READMEs, wikis |

## Issue Type Conventions

| Type | When to use |
|------|-------------|
| Task | General development work |
| Bug | Defect in existing functionality |
| Story | User-facing feature |
| Sub-task | Breakdown of a parent Task/Story (always requires parent) |

## Subtask Conventions

- Every Task or Story with estimated effort > 4h should be broken into Sub-tasks
- Sub-tasks inherit the parent's component unless explicitly overridden
- Sub-task summaries: prefix with work type — "Test: ...", "Implement: ...", "Review: ..."

## Description Template

When creating issues, use this structure:

```
## Context
<Why this work is needed>

## Acceptance Criteria
- [ ] <Criterion 1>
- [ ] <Criterion 2>

## Technical Notes
<Implementation hints, relevant files, dependencies>
```

## Labels (optional, common)

- `tech-debt` — Refactoring, cleanup
- `spike` — Research/investigation
- `blocked` — Waiting on external dependency
```

---

## 6. Subagent: `.claude/agents/jira.md`

```markdown
---
name: jira
description: Manage Jira issues — create, update, query, comment, and add subtasks via jira-cli.
model: sonnet
tools:
  - Bash(jira-w *)
  - Read
---

You are a Jira issue management agent. You execute Jira operations by running `jira-w`
CLI commands via Bash.

## Security Rules (non-negotiable)

1. **Never read the token file.** Do not `cat`, `type`, `head`, `tail`, `less`, `more`, `Get-Content`, or otherwise read the contents of any credential file (`~/.config/jira-skill/token`, `%APPDATA%\jira-skill\token`, `~/.config/.jira.yml`, `%APPDATA%\.jira.yml`).
2. **Never echo credentials.** Do not run `echo $JIRA_API_TOKEN`, `printenv`, `env`, `set` (to dump env), or any command that would expose tokens.
3. **Never reference token paths in output.** Do not mention the token file path to the user unless they encounter a "token file not found" error, in which case direct them to run the setup procedure externally.
4. **Only invoke `jira-w`.** Never invoke `jira` directly (it won't have auth) and never invoke `curl` with auth headers against the Jira API.

## General Rules

1. **Always use `--no-input`** on create and edit commands.
2. **Always use `--plain`** on list and view commands.
3. **Validate components** against `.jira-config.md` before creating/editing issues.
4. **Return concise results**: issue key + summary + link. Do not dump raw CLI output.

## Startup

1. Read `.jira-config.md` from the project root.
2. If missing, warn the caller and ask which project key to use.

## Operations

**Create an issue:**
- Require: project key, summary, type, component
- Use description template from project config if no description given
- Return: created issue key and confirmation

**Create a subtask:**
- Require: parent issue key, summary
- Type = `Sub-task` exactly (hyphenated)
- Inherit component from parent if not specified (view parent first)
- Return: created subtask key

**Update an issue:**
- `jira-w issue edit` for fields (description, summary, component, priority)
- `jira-w issue comment add` for comments
- Return: confirmation with issue key

**Query issues:**
- Construct JQL from natural language
- `--columns key,summary,status,assignee,priority`
- Max 15 results unless asked for more
- Return: formatted table

**Move/transition an issue:**
- List available transitions first, then apply
- Return: confirmation with new status

## Error Handling

- If a command fails, read stderr and provide a clear explanation
- If a component is invalid, list valid ones from `.jira-config.md`
- If auth fails (401), tell the caller to regenerate their token externally
- If "token file not found", tell the caller to run the setup procedure
- Never retry auth failures silently
```

---

## 7. Slash Command: `.claude/commands/jira-create.md`

```markdown
# Create Jira Issue

Create a new Jira issue or subtask based on the current development context.

## Instructions

Use the `jira` subagent to create a Jira issue with the following details from the user's input: $ARGUMENTS

Steps:
1. Dispatch to the `jira` subagent
2. The subagent reads `.jira-config.md` for project keys and valid components
3. The subagent creates the issue with `jira-w issue create`
4. Return the issue key and a one-line confirmation

If the user provides a parent issue key, create a Sub-task instead.
If the user does not specify a component, ask them to choose from the valid list.
If the user does not specify a description, generate one from the development context using the template in project config.
```

---

## 8. Slash Command: `.claude/commands/jira-update.md`

```markdown
# Update Jira Issue

Update an existing Jira issue's description, add a comment, change fields, or transition status.

## Instructions

Use the `jira` subagent to update the Jira issue based on: $ARGUMENTS

Steps:
1. Dispatch to the `jira` subagent
2. Parse whether the user wants to: update description, add comment, change component/priority, or transition status
3. Execute the appropriate `jira-w` CLI command
4. Return a confirmation with the issue key and what changed

If no issue key is provided, ask for one.
```

---

## 9. Slash Command: `.claude/commands/jira-query.md`

```markdown
# Query Jira Issues

Search for Jira issues using natural language or JQL.

## Instructions

Use the `jira` subagent to search Jira based on: $ARGUMENTS

Steps:
1. Dispatch to the `jira` subagent
2. The subagent translates the natural language query to JQL (or uses raw JQL if provided)
3. Execute `jira-w issue list` with the constructed query
4. Return a compact formatted summary of matching issues (max 15 unless asked for more)

Common query patterns to support:
- "my open issues" → assignee = currentUser() AND status != Done
- "open bugs in PROJECT" → project = PROJECT AND type = Bug AND resolution = Unresolved
- "recent updates" → updated >= -7d ORDER BY updated DESC
- "subtasks of PROJ-123" → parent = PROJ-123
```

---

## 10. Settings: `.claude/settings.json`

```json
{
  "permissions": {
    "allow": [
      "Bash(jira-w *)"
    ]
  }
}
```

This allowlists only `jira-w` wrapper invocations. The subagent cannot run arbitrary bash, cannot invoke `jira` directly (which would lack auth), and cannot `cat` credential files.

**Important:** Merge with existing settings if the file already exists — do not overwrite other permissions.

---

## 11. Project Config: `.jira-config.md`

Copy from `jira-manage/references/project-config-template.md` to the project root and fill in real values. This file **should be committed** to version control — it contains no credentials, only project structure metadata.

---

## File Creation Order

Execute in this order to allow incremental testing:

```
Phase 1a — Skill core:
  mkdir -p jira-manage/scripts jira-manage/references
  # Create jira-manage/SKILL.md
  # Create jira-manage/scripts/jira-w
  # Create jira-manage/scripts/jira-w.cmd
  # Create jira-manage/references/cli-ref.md
  # Create jira-manage/references/project-config-template.md

Phase 1b — Project config:
  # Copy template to .jira-config.md and fill in real values

Phase 1c — Subagent + permissions:
  mkdir -p .claude/agents .claude/commands
  # Create .claude/agents/jira.md
  # Create/merge .claude/settings.json

Phase 1d — Slash commands:
  # Create .claude/commands/jira-create.md
  # Create .claude/commands/jira-update.md
  # Create .claude/commands/jira-query.md

Phase 2 — Testing:
  # Run test matrix from 00-PLAN.md Phase 2
```

---

## Verification Checklist

After creating all files, verify:

- [ ] `echo $JIRA_API_TOKEN` / `echo %JIRA_API_TOKEN%` returns empty (token not in env)
- [ ] `jira-w issue list -q "project = <KEY>" --plain -a1` works from terminal
- [ ] Token file has correct permissions (`stat` / `icacls`)
- [ ] `claude` starts without errors in the project directory
- [ ] `/jira-query my open issues` returns results via the subagent
- [ ] `/jira-create Task in <PROJ>: Test issue -C Backend` creates an issue
- [ ] Created issue shows correct component in Jira web UI
- [ ] `/jira-update <KEY> add comment: Testing skill` adds a comment
- [ ] `/jira-create subtask of <KEY>: Sub-item` creates a linked subtask
- [ ] Main agent context (`/cost`) is not inflated by Jira operations
- [ ] Asking the subagent to "print the token file" is refused
- [ ] No credential values appear in any project file
