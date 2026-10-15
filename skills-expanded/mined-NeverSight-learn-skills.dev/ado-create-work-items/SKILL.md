---
name: ado-create-work-items
description: >-
  Create Azure DevOps work items from a backlog_input.json (the output of
  classify-work-items) via the bundled create-backlog.cs script. Always does a
  dry-run validation first and only creates real items after the user explicitly
  approves. Use this whenever there is a backlog_input.json or any file of items
  to file in ADO, or when the user says "create these work items", "file the
  backlog", "push these to Azure DevOps", "create the tickets/bugs/stories",
  "make the work items", or asks to turn a classified list of findings into a
  real ADO backlog. This is the step that actually writes to the org, so prefer
  it over hand-rolling REST/MCP calls when a backlog_input.json exists. After
  creating, it writes backlog_result.json for ado-writeback-tracking.
effort: max
---

# ado-create-work-items

Take a `backlog_input.json` and create the work items in Azure DevOps by driving
the bundled `create-backlog.cs`. The script creates an optional parent
(Feature/Epic), then every item linked under it, and writes a
`backlog_result.json` mapping each `key` to its new `id`/`url`.

Creating items in a live org is outward-facing and effectively un-undoable (delete
is manual, links and notifications already fired). So this skill is built around a
hard gate: **dry-run always, real run only on an explicit "yes".**

For the exact JSON shapes (`backlog_input.json`, `backlog_result.json`, the `key`
field that threads source row → ticket, and the process→types table) see
`references/data-contracts.md`. Don't duplicate schemas here.

## Prerequisites

- **Auth** — sign in once: `az login` (the script fetches an Entra token for the
  Azure DevOps resource). Alternatively set `$env:AZDO_PAT` (PAT with Work Items
  Read & Write). See the `ado-auth` skill for token/PAT details and tenant.
- **Org/project** — set `$env:AZDO_ORG` / `$env:AZDO_PROJECT`, or include `org` /
  `project` in the JSON. Env vars override the JSON.
- **.NET 10 SDK** — `create-backlog.cs` is a .NET 10 file-based program.
- Unsure if prereqs are met? Run the checker:
  `powershell -ExecutionPolicy Bypass -File "${CLAUDE_SKILL_DIR}/scripts/setup_check.ps1"`

Confirm the `type` of each item is valid for the target project's **process**
(Agile vs Scrum vs Basic vs CMMI) — see the table in data-contracts.md. A type that
doesn't exist on the board is the most common dry-run failure.

## Step 1 — DRY RUN (default; creates nothing)

`AZDO_DRY_RUN` defaults to dry-run unless it is the literal string `false`, so we
set it explicitly to be safe. In this mode the script PATCHes each item with
`validateOnly=true` — ADO checks types, required fields, and field values without
persisting anything.

```powershell
$env:AZDO_ORG     = "Cartagena365"   # or rely on the JSON / already-set env
$env:AZDO_PROJECT = "GlassHull"
$env:AZDO_DRY_RUN = "true"
dotnet run "${CLAUDE_SKILL_DIR}/scripts/create-backlog.cs" -- "<path>/backlog_input.json"
```

The script prints a `PASS` / `FAIL` line per item (and per parent), then a summary
like `DRY RUN done. valid=N invalid=M. No work items were created.` Relay that
list to the user. **If anything is FAIL, stop and fix the input** (usually a bad
`type` for the process, a missing `System.Title`, or unescaped `& < >` in an HTML
field like `Microsoft.VSTS.TCM.ReproSteps` / `System.Description`) before going on.

## Step 2 — REAL RUN (only after explicit approval)

Do **not** proceed until the user has clearly said yes (e.g. "create them",
"go ahead"). A clean dry-run is necessary but not sufficient — the human owns the
decision to write to their org.

Point `BACKLOG_RESULT` at your working directory so the writeback step can find it,
then flip the gate to `false`:

```powershell
$env:AZDO_DRY_RUN  = "false"
$env:BACKLOG_RESULT = "<your-working-dir>/backlog_result.json"
dotnet run "${CLAUDE_SKILL_DIR}/scripts/create-backlog.cs" -- "<path>/backlog_input.json"
```

What happens: if the input has a `parent`, it is created first; every item is then
created and linked to it via `System.LinkTypes.Hierarchy-Reverse` (child → parent). If an item
has an `estimate`, a **child Task** carrying the hours (Original/Remaining Work + the breakdown
in its description) is created under that item — so the hierarchy is Feature → Bug/Story → Task.
`AZDO_AREA_PATH` and `AZDO_ASSIGNED_TO`, if set, are stamped on every item
(`AZDO_ASSIGNED_TO` only on items that didn't already set their own `System.AssignedTo`).
The script prints
`key … -> <type> #<id>` per item and writes `backlog_result.json`
(`key` → `id` / `url` / `type` / `title`). Failures are recorded per-item with an
`error` field instead of an `id`, so a partial run is visible rather than silent.

## After creating — verify

Confirm the items landed as intended. Query the new ids in one batch and check
`System.WorkItemType`, `System.State`, and the parent link. Pull the ids from
`backlog_result.json` and use the ADO MCP `wit_get_work_items_batch_by_ids` (or the
workitemsbatch REST endpoint). Spot-check that children show the expected parent.

## Idempotency — don't double-create

`create-backlog.cs` is **not** idempotent: re-running the REAL run on the same
`backlog_input.json` creates a second set of items (duplicates). After a successful
real run, hand off to **ado-writeback-tracking** to stamp `Ticket ID` / `Ticket URL`
back onto the source rows (matched by `key`). Once a row carries a Ticket ID, treat
it as done. If you must re-file a subset, prune the input to only the un-filed
`key`s first.

## Windows notes

- The install path can contain spaces — always wrap `"${CLAUDE_PLUGIN_ROOT}/..."`
  and the JSON path in double quotes.
- Console is cp1252; the .cs program emits ASCII status lines, so output is safe.
  (The bundled Python scripts force UTF-8 for source dumps / writeback.)
