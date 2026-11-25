---
name: ps-edit
description: Edit or maintain an existing Process Street workflow using natural language — add/remove steps and fields, change logic, due dates, assignments, or add media. Use when the user wants to change a workflow they already have.
---

# Edit a Process Street workflow

Translate a natural-language change request into safe API operations with a draft → publish → rollback flow.

**CLI:** `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/process_street.py" <command>` (plugin) or `scripts/process_street.py` (repo). Needs `PROCESS_STREET_API_KEY`. Detail: `reference/api-reference.md`.

> **Use the CLI even if the Process Street MCP is connected.** `edit-workflow` runs draft → publish → **rollback** and prints a `restore-revision` command; raw MCP edits skip that safety net. Don't substitute MCP ops for the edit flow.

## 1. Load current state

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/process_street.py" template-export <workflowId>
```
This returns steps, fields, logic rules, and the current published revision (the **rollback target** — note it).

## 2. Interpret the request → operations

Map the ask to edit-plan ops:

| op | does |
|----|------|
| `add-task` / `update-task` / `delete-task` | add, change (name/type/stop/hidden/dueOffset), or remove a step |
| `add-widget` / `update-widget` / `delete-widget` | add a field (any of 17 types) or content widget; change; remove |
| `add-rule` / `delete-rule` | conditional logic |
| `set-due-date-rule` / `set-checklist-due-date-rule` | dynamic due dates |
| `set-assignment-rules` / `set-task-permissions` | who owns / who can see a task |

Positioning: `"afterTask": "Existing Step Name"`. Field types & operators: see `reference/api-reference.md`.

## 3. Preview, confirm, apply

Show a before/after of the operations and the rollback command. After the user confirms:

```bash
echo '<edit-plan-json>' | python3 "${CLAUDE_PLUGIN_ROOT}/scripts/process_street.py" edit-workflow
```

Edit-plan shape:
```json
{"workflowId": "<id>", "operations": [
  {"op": "add-task", "name": "QA Review", "taskType": "Approval", "stop": true, "afterTask": "Build"},
  {"op": "add-widget", "taskName": "Intake", "fieldType": "Select", "label": "Region", "options": ["EU", "US"]},
  {"op": "set-assignment-rules", "taskName": "QA Review", "rules": [{"email": "qa@company.com"}]},
  {"op": "add-rule", "rule": {"action": "Show",
     "condition": {"or": [{"and": [{"widgetId": "$widget:Intake:Region", "operator": "Is", "value": "EU"}]}]},
     "targets": {"taskIds": ["$task:GDPR Step"]}}}
]}
```

The CLI creates a draft, applies ops, publishes, and prints a **rollback** command. Relay it to the user.

## Adding media / polish
`add-media <wf> <rev> <taskId> --logo-domain <domain> | --stock "kw" | --video <url> | --embed <url> | --text '<md>'`. Create a draft revision first; publish after.

## Limits to flag
Required-field flag, brand theming, org/SSO, deep integration config are UI-only. Editing existing embedded instruction text in place is limited (you can add new content widgets). `File` → use `MultiFile`.

## Rollback
If a change looks wrong after publish: `process_street.py restore-revision <workflowId> <previousRevisionId>`.
