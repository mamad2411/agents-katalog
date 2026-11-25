---
name: atlassian-acli
description: >
  Use this skill for anything involving Jira from the command line, terminal, or shell. This includes
  creating Jira issues, searching Jira, editing tickets, changing statuses, listing projects, managing
  sprints, bulk operations, CSV imports to Jira, exporting Jira data, or automating Jira in scripts and
  CI pipelines. Trigger whenever the user wants to interact with Jira programmatically or without a
  browser — even if they don't mention "acli" or "CLI" explicitly. Any mention of Jira project keys like
  PROJ-123, OPS, INFRA, BUGS, RELEASE, QA, or TEAM should trigger this skill if the user wants to
  create, edit, search, transition, list, or automate issues. Also trigger for JQL queries, "acli", or
  "atlassian cli". Do NOT use this skill for: Python/requests scripts calling Jira REST API directly,
  Confluence pages, Trello, GitHub Issues, or Slack bots.
---

# Atlassian CLI (acli) for Jira

`acli` is Atlassian's official CLI for Jira Cloud. It follows a consistent pattern:

```
acli jira <subgroup> <command> [flags]
```

This skill teaches you how to use acli effectively for Jira automation. Authentication is assumed to be already configured — if you encounter auth errors, see the troubleshooting section at the end.

## Command Structure

All Jira commands live under `acli jira`. The subgroups are:

| Subgroup | Purpose |
|----------|---------|
| `workitem` | Create, edit, search, view, transition issues — the core of Jira work |
| `project` | List, create, view, update, archive projects |
| `board` | List and search boards |
| `sprint` | List sprint work items |
| `filter` | Manage saved filters |
| `field` | Inspect issue fields |
| `dashboard` | Manage dashboards |
| `auth` | Login, logout, status, switch accounts |

## Key Principles

### Always use `--json` for output
When running acli commands programmatically, always append `--json` to get structured output you can parse. This is critical for automation — human-readable table output is unreliable to parse.

### Use `--yes` to skip confirmation prompts
Commands that modify data (edit, transition, delete) prompt for confirmation by default. In automation, always pass `-y` or `--yes` to skip the interactive prompt.

### Use JQL for targeting work items
Many commands accept `--jql` to select which issues to act on. JQL (Jira Query Language) is powerful — learn the basics in the reference file.

### Prefer `--from-json` for complex creates/edits
For work items with many fields, generate a JSON template with `--generate-json`, fill it in, and pass it with `--from-json`. This is more reliable than passing many flags.

## Common Workflows

### 1. Search for issues

```bash
# Find all open bugs in project TEAM
acli jira workitem search --jql "project = TEAM AND type = Bug AND status != Done" --json

# Count issues matching a query
acli jira workitem search --jql "assignee = currentUser() AND sprint in openSprints()" --count

# Get specific fields only
acli jira workitem search --jql "project = TEAM" --fields "key,summary,status,assignee" --json

# Paginate through all results (no limit)
acli jira workitem search --jql "project = TEAM" --paginate --json
```

### 2. View issue details

```bash
# View a specific issue
acli jira workitem view KEY-123 --json

# View with specific fields
acli jira workitem view KEY-123 --fields "summary,status,description,comment" --json

# View all fields
acli jira workitem view KEY-123 --fields "*all" --json
```

### 3. Create a work item

```bash
# Simple creation
acli jira workitem create --project TEAM --type Task --summary "Implement login page" --json

# With description and assignee
acli jira workitem create \
  --project TEAM \
  --type Story \
  --summary "User authentication flow" \
  --description "As a user, I want to log in with email and password" \
  --assignee "dev@company.com" \
  --label "auth,frontend" \
  --json

# Create as subtask (set parent)
acli jira workitem create \
  --project TEAM \
  --type Task \
  --summary "Write unit tests for login" \
  --parent KEY-100 \
  --json

# Complex creation via JSON template
acli jira workitem create --generate-json > template.json
# Edit template.json with all fields...
acli jira workitem create --from-json template.json --json
```

### 4. Edit a work item

```bash
# Update summary
acli jira workitem edit --key KEY-123 --summary "Updated title" --yes --json

# Reassign
acli jira workitem edit --key KEY-123 --assignee "other@company.com" --yes --json

# Self-assign
acli jira workitem edit --key KEY-123 --assignee "@me" --yes --json

# Bulk edit via JQL
acli jira workitem edit --jql "project = TEAM AND labels = deprecated" --labels "archived" --yes --json

# Update description from file
acli jira workitem edit --key KEY-123 --description-file description.md --yes --json
```

### 5. Transition (move) a work item

```bash
# Move to In Progress
acli jira workitem transition --key KEY-123 --status "In Progress" --yes --json

# Move multiple issues to Done
acli jira workitem transition --key "KEY-1,KEY-2,KEY-3" --status "Done" --yes --json

# Transition all issues matching JQL
acli jira workitem transition --jql "project = TEAM AND status = 'In Review'" --status "Done" --yes --json
```

### 6. Comment on a work item

```bash
# Add a comment
acli jira workitem comment create --key KEY-123 --body "Deployment completed successfully" --json

# Comment from a file
acli jira workitem comment create --key KEY-123 --body-file notes.txt --json

# Comment on multiple issues
acli jira workitem comment create --key "KEY-1,KEY-2" --body "Blocked by infrastructure issue" --json
```

### 7. List projects

```bash
# List all projects
acli jira project list --paginate --json

# Recent projects
acli jira project list --recent --json

# Limited list
acli jira project list --limit 10 --json
```

### 8. Sprint work items

```bash
# List items in a sprint (use the board and sprint IDs)
acli jira sprint list-workitems --board-id 1 --sprint-id 5 --json
```

## Handling Output

Always use `--json` and parse the JSON response. Extract the fields you need. When searching, the default fields are: `issuetype, key, assignee, priority, status, summary`. Request additional fields with `--fields`.

For CSV output (useful for reports), use `--csv` instead of `--json`.

## Error Handling

When a command fails:
1. Check the error message — acli provides descriptive errors
2. For bulk operations, use `--ignore-errors` to continue past individual failures
3. Verify the issue key, project key, or status name exists
4. Status names must match exactly (case-sensitive) — use the project's workflow status names

## Detailed Command Reference

For full flag documentation on each command, read the reference files:
- `references/jira-commands.md` — Complete flag reference for all Jira commands
- `references/jql-guide.md` — JQL syntax and common query patterns

## Troubleshooting Auth

If you get authentication errors:
1. Check auth status: `acli jira auth status`
2. If not logged in, the user needs to run: `acli jira auth login --web` (browser OAuth) or pipe a token: `echo $ATLASSIAN_TOKEN | acli jira auth login --site "site.atlassian.net" --email "user@co.com" --token`
3. To switch accounts: `acli jira auth switch`
4. To re-authenticate: `acli jira auth logout` then login again

Do NOT attempt to run auth login commands automatically — these require user interaction (browser or token). Inform the user what command to run and let them execute it.
