---
name: ps-build
description: Build a new Process Street workflow from a description, document, or structured plan. Use when the user wants to create a workflow/template/process in Process Street.
---

# Build a Process Street workflow

Turn a description (or pasted process / document) into a live Process Street workflow via the public API.

**CLI:** `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/process_street.py" <command>` (when installed as a plugin) or `python3 scripts/process_street.py` from the repo. Needs `PROCESS_STREET_API_KEY` set. Capability + field-type detail: `reference/api-reference.md`. Design guidance: `reference/best-practices.md`.

> **Use the CLI even if the Process Street MCP is connected.** `build-workflow` orchestrates the whole multi-step build (tasks, widgets, logic, rules) in one call and records a **rollback** target — raw MCP calls don't. Don't substitute MCP create-ops for the build flow.

## 1. Understand the process

Get: the workflow name and outcome, the steps in order (who does what), decision points (branches), approvals/sign-offs, data to capture (and at which step), SLAs, stop gates, and anything conditional. If the user pasted a document or transcript, extract this from it. Ask one clarifying question only if something essential is missing.

## 2. Draft a build plan (JSON)

Apply best practices (`reference/best-practices.md`): outcome-based name, 6–15 verb-named steps, the *right field type* per datum (Select for fixed choices, Date, Number, Members, Email — not all free text), conditional logic to hide irrelevant steps, stops/approvals only where they earn the friction, dynamic due dates, an owner per task.

Build-plan shape (see api-reference.md for all 17 field types, due-date/assignment rules, content widgets):

```json
{
  "name": "Customer Onboarding",
  "folderId": "<folderId>",
  "shareLevel": "Run",
  "tasks": [
    {"name": "Intake", "taskType": "Standard", "dueOffset": "P1D", "widgets": [
      {"fieldType": "Text", "label": "Company Name"},
      {"fieldType": "Select", "label": "Plan Tier", "options": ["Starter", "Pro", "Enterprise"]},
      {"fieldType": "Number", "label": "Seats", "constraints": {"minValue": 1, "decimalPlaces": 0}}
    ]},
    {"name": "Manager Approval", "taskType": "Approval", "stop": true,
     "assignmentRules": [{"email": "manager@company.com"}],
     "dueDateRule": {"sourceType": "PreviousTaskCompletedDate", "offsetDirection": "After", "dueOffset": "P1D", "businessDaysHandlingMode": "BusinessDaysOnly"}}
  ],
  "logicRules": [
    {"action": "Show",
     "condition": {"or": [{"and": [{"widgetId": "$widget:Intake:Plan Tier", "operator": "Is", "value": "Enterprise"}]}]},
     "targets": {"taskIds": ["$task:Enterprise Setup"]}}
  ]
}
```

Use `$task:Step Name` and `$widget:Step Name:Field Label` symbolic refs. Logic operators: `Is`, `IsNot`, `HasAnyValue`, `HasNoValue`, `IsGreaterThan`, `IsLessThan`.

**You need a `folderId`.** List folders: `process_street.py folders`. Create one: `process_street.py folder-create --name "..."`.

## 3. Confirm, then build

Show the user a plain-English summary (steps, types, fields, logic, what's manual). Get a yes. Then:

```bash
echo '<plan-json>' | python3 "${CLAUDE_PLUGIN_ROOT}/scripts/process_street.py" build-workflow [--draft-only]
```

**Use `--draft-only` if the plan has AI or Code tasks** (they can't publish until configured). Then configure them and publish:
- AI: `task-config <wf> <rev> <taskId> --type Ai --prompt "..."`
- Code: `task-config <wf> <rev> <taskId> --type Code --code 'outputData["x"]=inputData["y"]' --input-mapping '{"y":"<fieldId>"}' --output-mapping '{"x":"<fieldId>"}'`
- Approval (so it's completable in a run): `task-config <wf> <rev> <approvalTaskId> --type Approval --subject-task-ids <taskId>`
- Then: `publish-revision <wf> <rev>`

## 4. Polish (recommended)

Make it look professional and on-brand with `add-media <wf> <rev> <taskId>` (create a draft first if already published):
- `--logo-domain <client-domain>` (company logo), `--text '## Welcome…'` on step 1
- `--stock "keyword,keyword"` topic image, `--video <youtube-url>`, `--embed <url>` (a relevant live resource)
Make assets relevant to the use case. Brand colors/cover/fonts are UI-only — mention that if asked.

## 5. Verify

`process_street.py template-export <workflowId>` — confirm steps, fields, logic. Give the user the workflow URL: `https://app.process.st/workflows/<workflowId>`.

## Manual (UI-only) items to flag
Required-field flag, brand theming (colors/cover/fonts), org/SSO settings, deep native-integration config. `File` fields are created as `MultiFile`.
