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

**Warning:** On Windows, multiline comment bodies get truncated during bash-to-cmd
translation. Content after the first newline may be silently lost. Always flatten
comments to a single line (use periods/semicolons as separators instead of newlines),
or write the comment body to a temp `.cmd` file and execute that.

### List Project Components

```bash
jira-w --components <PROJECT_KEY>
```

Returns all components defined in the project, one name per line.
Use this to validate component names before create/edit operations.
Falls back to `.jira-config.md` if the API call fails.

### Set/Change Component

```bash
jira-w issue edit <ISSUE-KEY> --component "<ComponentName>" --no-input
```

## Error Handling

Non-zero exit codes indicate failure — always check stderr. Match against these patterns:

| Stderr pattern | Cause | Action |
|----------------|-------|--------|
| `401 Unauthorized` | Token expired/invalid | Tell user to regenerate token. **Never retry.** |
| `403 Forbidden` | Insufficient permissions | Tell user their account lacks this permission. |
| `429` or `rate limit` | API rate-limited | Wait 1-2 minutes before retrying. |
| `token file not found` | Missing credential file | Direct user to setup procedure. |
| `Component name` + `not valid` | Bad component | List valid components via `jira-w --components <KEY>`. |
| `Issue type` + `not valid` | Wrong type string | Check case: `Sub-task` not `Subtask`. |
| `Project` + `does not exist` | Bad project key | Verify key in `.jira-config.md`. |
| `timeout` / `connection refused` | Network failure | Report to user, do not retry. |

**Rules:**
- Never retry auth (401) or permission (403) failures
- For validation errors, provide correct values immediately
- For rate limits, wait and retry once — escalate on second failure
- For network errors, report once and stop

## Output Guidelines

- Return concise results: issue key, summary, and status
- For queries: compact table, max 20 results unless asked for more
- Never include raw JSON API responses
- Always confirm create/update operations with the resulting issue key

## Platform Notes

- On Unix (Linux/macOS): `jira-w` is a bash script
- On Windows: `jira-w` or `jira-w.cmd` is a batch script
- Both behave identically — always invoke as `jira-w` (shell resolves the extension on Windows)
