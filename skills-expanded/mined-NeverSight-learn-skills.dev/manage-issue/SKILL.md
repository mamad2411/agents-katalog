---
name: manage-issue
description: Create, query, update, close, and link issues
argument-hint: "<create|list|status|update|close|link> [options]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, request_user_input
---

<purpose>
Issue CRUD operations: create, list, status, update, close, and link issues to tasks.
All data stored in `.workflow/issues/issues.jsonl` with auto-created directory on first use.

**Closed-loop workflow**: issue → `$maestro-analyze --gaps <ISS-ID>` (root cause analysis) → `$maestro-plan --gaps` (solution planning) → `$maestro-execute` (implementation). For automated issue discovery, use `$manage-issue-discover`.
</purpose>

<required_reading>
Read `~/.maestro/workflows/issue.md` before executing any subcommand. This file defines the issue.json schema, ID format, field validation rules, and JSONL storage conventions.
</required_reading>

<context>
$ARGUMENTS — subcommand followed by options.

```bash
$manage-issue "create --title 'Auth token expiry bug' --severity high --source manual"
$manage-issue "list --status open --severity high"
$manage-issue "status ISS-20260318-001"
$manage-issue "update ISS-20260318-001 --priority critical --tags auth,security"
$manage-issue "close ISS-20260318-001 --resolution fixed"
$manage-issue "link ISS-20260318-001 --task TASK-003"
```

**Subcommands**: `create`, `list`, `status`, `update`, `close`, `link`.
</context>

<execution>

### Step 1: Parse Subcommand

Extract first token as subcommand. Valid: `create`, `list`, `status`, `update`, `close`, `link`.
If missing or invalid, display usage and prompt user (E_NO_SUBCOMMAND, E_INVALID_SUBCOMMAND).

### Step 2: Ensure Storage

If `.workflow/issues/` does not exist, auto-create the directory and write an empty `issues.jsonl` file. Log as E_ISSUES_DIR_MISSING (warning, non-blocking).

### Step 3: Execute Subcommand

**create**: Read `~/.maestro/templates/issue.json` for schema. Generate ID `ISS-{YYYYMMDD}-{NNN}`. If required fields are missing, prompt via `request_user_input`:
```json
{ "questions": [{ "id": "issue_title", "header": "New Issue", "question": "What is the issue title?" }, { "id": "issue_severity", "header": "Issue Severity", "question": "What severity level?", "options": [{ "label": "high (Recommended)", "description": "Production-impacting or blocking" }, { "label": "medium", "description": "Degraded functionality" }, { "label": "low", "description": "Minor or cosmetic" }] }] }
```
Append JSON line to `issues.jsonl`.

**list**: Read `issues.jsonl`, filter by `--status`, `--phase`, `--severity`, `--source`. Display as table:
```
ID              | Severity | Status | Title
ISS-20260318-001 | high     | open   | Auth token expiry bug
```

**status**: Find issue by ID in `issues.jsonl`. Display all fields in detail format.

**update**: Find issue by ID, merge provided fields, rewrite the line in `issues.jsonl`. Track `updated_at` timestamp.

**close**: Find issue by ID, set status to `closed`, add `resolution` and `closed_at`. Move line from `issues.jsonl` to `issue-history.jsonl`.

**link**: Bidirectional cross-reference between issue and task:
1. Find issue by ID in `issues.jsonl`, add task ID to issue's `linked_tasks[]` array, rewrite the line
2. Read task JSON at `.workflow/.task/{TASK-ID}.json` (or `.task/{TASK-ID}.json`). Edit the task's `linked_issues` field — append the issue ID to the array. If `linked_issues` field does not exist, create it as `[ISS-ID]`
3. Both writes must succeed for the link to be considered complete
</execution>

<error_codes>
| Code | Severity | Description |
|------|----------|-------------|
| E_NO_SUBCOMMAND | error | No subcommand provided -- display valid subcommands |
| E_INVALID_SUBCOMMAND | error | Unrecognized subcommand |
| E_ISSUES_DIR_MISSING | warning | `.workflow/issues/` not found — auto-create directory and empty issues.jsonl |
</error_codes>

<success_criteria>
- [ ] Subcommand parsed and validated
- [ ] Storage directory and files auto-created on first use
- [ ] create: generates unique ISS-id, prompts for required fields, appends to JSONL
- [ ] list: filters by status/phase/severity/source, renders table
- [ ] status: displays full detail for given ISS-id
- [ ] update: merges fields, tracks updated_at timestamp
- [ ] close: sets status closed, moves to history file
- [ ] link: bidirectional cross-reference between issue and task
</success_criteria>
