---
name: my-work
description: >-
  Show the Azure DevOps work items assigned to you as a clean, grouped table — open work
  first, sorted by state then priority, with the ticket number as a clickable link. Use
  whenever the user asks "what's on my plate", "my work items / my tasks", "what should I
  work on next", "show my backlog", "read my task hub", "daily standup prep", or starts the
  day wanting their remaining work. This is step 2 of the daily-work flow (read the task
  hub). Read-only — it lists, it never changes anything.
effort: max
---

# my-work

List everything assigned to you across the organization as a per-project table: **open items
first** (Active → New/To Do → Design), sorted by **Priority**, with the ticket `#` rendered as
a **clickable terminal hyperlink** that opens the work item. Completed items collapse to a
count. Entirely read-only.

## Run it

Prereqs: `az login` (or `$env:AZDO_PAT`), `$env:AZDO_ORG` set, .NET 10 SDK. (Run
`/ado-backlog:setup-check` if unsure.)

```powershell
$env:AZDO_ORG = "Cartagena365"      # your organization NAME (not a URL)
dotnet run "${CLAUDE_SKILL_DIR}/scripts/my-work.cs"
```

The `#` column is a clickable hyperlink (click / Ctrl+click in VS Code or Windows Terminal)
that opens `…/_workitems/edit/<id>` in the browser. Colors and links auto-disable when the
output is piped or redirected, so it stays clean in logs.

## Options

- `$env:AZDO_SHOW_DONE = "true"` — also print a table of completed (Done/Resolved) items.
- `$env:AZDO_INCLUDE_CLOSED = "true"` — include Closed/Removed too.
- `$env:NO_COLOR = "1"` — plain text (no color, no links).
- `$env:AZDO_PAT = "..."` — use a PAT (scope: Work Items = Read) instead of the az token; see **ado-auth**.

## After listing

The top row of each project group is the highest-priority actionable item — a good "do next".
If instead the user wants to turn a *findings source* (an audit/review/spreadsheet) into new
work items, hand off to **findings-to-ado-backlog**. For 401/403/org issues, see **ado-auth**.
