---
name: ps-search
description: Search a Process Street org for workflows, runs, data sets, folders, pages, or users by keyword/criteria — PS MCP tools first, REST API as fallback. The "where is that thing" skill, not for building. Use when someone says "ps search", "search ps", "find that workflow", "find the workflow about [X]", "what runs are active for [company]", "search my ps org", "look up workflow", "find workflow run", or "find dataset".
---

# PS Org Search Skill

## Purpose

Search across a Process Street org for workflows, runs, data sets, folders, pages, or users by keyword/criteria. Uses the PS MCP server first — falls back to the REST API only when MCP can't filter the way you need.

This is the "where is that thing" skill. Not for building. Not for inspecting one workflow deeply (use `ps-audit` for that).

---

## When to Use

- "Find that workflow about onboarding"
- "Show me all active runs for [company]"
- "What's in the [folder name] folder"
- "Is there a data set for inspector assignments"
- "Which workflows have a code task that calls [external system]"
- "Find the run where the form field 'County' = 'Berkeley'"

---

## Reference Docs (read first if unsure of tool/endpoint)

- the API reference (`reference/api-reference.md`) — full endpoint list, MCP tools, and quirks

---

## Search Routing

| What you want | First-choice tool | Notes |
|---|---|---|
| Find workflow by name/keyword | `listWorkflows` (MCP) | Filter results client-side by name |
| List workflows in a folder | `listWorkflows` (MCP) | Pass `folderId` |
| Active runs for a company/keyword | `searchWorkflowRuns` (MCP) | **Max 200 results per call** — paginate |
| Runs by status (Active/Completed/Archived) | `searchWorkflowRuns` (MCP) | `status` param |
| Runs by form field value | `searchWorkflowRuns` (MCP) | Use `formFieldFilters` |
| Find data set by name | `listDataSets` (MCP) | Filter results client-side |
| Records inside a data set | `listDataSetRecords` (MCP) | Paginate by cursor |
| Find folder | `listFolders` (MCP) | |
| Find a page (SOP) | `listPages` (MCP) | |
| Find user by name/email | `listUsers` (MCP) | |
| Find scheduled workflows | `listScheduledWorkflows` (MCP) | |
| Find workflow incoming webhooks | `listWorkflowIncomingWebhooks` (MCP) | |
| Search inside task widget content | REST API + grep | MCP doesn't filter widget bodies — get workflow revision, walk widgets |

---

## Standard Flow

1. **Clarify scope** if ambiguous. ("All orgs? Just yours? A specific folder?")
2. **Pick the narrowest tool.** Don't call `listWorkflows` if the user gave a folder.
3. **Paginate.** `searchWorkflowRuns` caps at 200. Always check for `nextPageToken` / cursor.
4. **Return a tight table.** Columns: name, id, link, last activity, status. Hide stuff the user didn't ask for.
5. **Include the PS deep link** for each result so the user can click straight in.

---

## Output Shape

Default to a markdown table. Always include the PS deep link so the user can click in.

```
| Name | Folder | Status | Last activity | Link |
|------|--------|--------|---------------|------|
| Daily Inspection | Operations | Active | 2026-05-20 | [open](https://app.process.st/...) |
```

If 1 result → expand inline with id + folderId. If >20 results → ask the user to narrow before dumping.

---

## Common Gotchas

- `searchWorkflowRuns` `formFieldFilters` requires the form field ID, not label. Use the CLI `template-fields` (lists fields + IDs) first if the user gives a label.
- MCP `listWorkflows` returns archived workflows mixed in. Filter `archived: false` unless the user asks for archived.
- Workflow names are not unique across folders — show folder in the table.

---

## Related Skills

- `ps-audit` (or the CLI `template-export`) — read out one workflow in full
- the CLI `template-fields` (lists fields + IDs) — pull field IDs from a run before filtering by field value
- `data-set` — CRUD on the data sets you found here
