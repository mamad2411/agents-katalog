---
name: classify-work-items
description: >-
  Map triaged findings to the correct Azure DevOps work item types for the
  TARGET project's process, and emit backlog_input.json ready for creation.
  Use this AFTER triage and BEFORE creating items — when the user asks "what
  type should these be", "make these into work items / tickets", "turn these
  findings into a backlog", "classify these for ADO", or "build the backlog
  input". The type you choose MUST exist on the target board: a Basic-process
  project has no Bug or User Story, so picking those silently fails at creation
  time. This skill discovers the project's process first, applies industry
  typing rules (defect vs new capability vs grouping parent), maps severity to
  Priority, builds the per-type fields (titles, tags, repro/description as
  escaped HTML), carries each finding's `key` through, and hands off to
  ado-create-work-items.
effort: max
---

# classify-work-items

Turn findings (from `extract-findings` + `triage-findings`) into a `backlog_input.json`
that `ado-create-work-items` can create. The hard part is **typing**: an ADO work item
type only exists if the project's process defines it. Get this wrong and creation fails
on the board, so we discover the process *before* we decide types.

Schemas live in `references/data-contracts.md` — read it for the exact
`findings.json` / `backlog_input.json` shapes. Don't duplicate them here.

## 1. Discover the project's process and valid types — FIRST

You cannot pick a type blind. Basic has no `Bug` and no `User Story`; Scrum uses
`Product Backlog Item` instead of `User Story`; CMMI uses `Requirement`. Picking a type
the board doesn't have is the #1 cause of create failures. So query the process up front.

Get a token (see the **ado-auth** skill — `az login` once, then):

```powershell
$org     = $env:AZDO_ORG       # e.g. Cartagena365
$project = $env:AZDO_PROJECT   # e.g. GlassHull
$token = az account get-access-token --resource 499b84ac-1321-427f-aa17-267ca6975798 --query accessToken -o tsv
$headers = @{ Authorization = "Bearer $token" }

$proj = Invoke-RestMethod -Headers $headers `
  "https://dev.azure.com/$org/_apis/projects/$project?includeCapabilities=true&api-version=7.1"
$proj.capabilities.processTemplate.templateName    # -> Agile | Scrum | Basic | CMMI
```

(With a PAT instead: `$headers = @{ Authorization = "Basic " + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$env:AZDO_PAT")) }`.)

Once you know the process name, **use the process→types table in `references/data-contracts.md`**
to map it to valid types. Do *not* try to `ConvertFrom-Json` the full
`/_apis/wit/workitemtypes` payload in PowerShell 5.1 — that response has case-duplicate
keys (e.g. `URL` vs `url`) and the 5.1 parser throws on them. The table is the reliable source.

If `AZDO_ORG` / `AZDO_PROJECT` aren't set, ask the user which org/project this backlog
targets before going further — the process is project-specific.

## 2. Type each finding — the rules, and why

Map by the *nature* of the work, not by the finding's `severity`. Using the table for the
discovered process (columns: defect / new capability / grouping parent):

- **Wrong, ambiguous, or mismapped existing thing** → the **defect** type
  (`Bug` on Agile/Scrum/CMMI). A field that exists but shows the wrong label, or a value
  that's mislabeled, is a correctness defect — it should be fixed, not "built". Most
  rename / disambiguation findings (`kind: rename` | `disambiguation`) land here.
  *Basic has no dedicated defect type* — on the Basic process, defects and new capabilities
  both collapse to `Issue` (its only non-Epic/Task type), matching the table in
  `references/data-contracts.md`.

- **A capability that doesn't exist yet** (e.g. `kind: missing` — a field, view, or feature
  that's absent) → the **new-capability** type: `User Story` (Agile),
  `Product Backlog Item` (Scrum), `Requirement` (CMMI), `Issue` (Basic). Filing "add a new
  field/feature" as a Bug is an anti-pattern — it's net-new scope, not a regression, and
  teams plan/estimate it differently.

- **The initiative itself** → one **grouping parent**: a `Feature` (or `Epic`) that all the
  children link under. This keeps the audit traceable as one body of work rather than a
  scatter of orphan tickets. See step 4.

When a finding is genuinely ambiguous between defect and new capability, ask the user rather
than guess — the type drives which team queue it lands in.

## 3. Map severity → Priority

`severity` becomes `Microsoft.VSTS.Common.Priority` (an integer 1–4). Lower number = higher
priority, matching ADO:

| severity | Priority |
|---|---|
| Critical | 1 |
| High | 2 |
| Medium | 3 |
| Low | 4 |

If a finding has no severity, default to `3` (Medium) and note it.

## 4. Build the fields for each item

`fields` are raw ADO reference names (strings or numbers). Build per type:

- **`System.Title`** (required) — specific and self-contained. Name the thing and the
  expected state, e.g. `Portal label "Auto" should display CRM-canonical "Automotive Cargo"`,
  not `Fix naming`. Someone scanning the board should understand it without opening it.
- **`System.Tags`** — semicolon-separated, `"initiative; status"` form, e.g.
  `"naming-audit; crm-portal; review-confirmed"`. Tag the initiative (so the whole batch is
  filterable) plus the triage status. ADO splits on `;`.
- **`Microsoft.VSTS.Common.Priority`** — the integer from step 3.
- **`System.AssignedTo`** (optional) — a user identity (UPN/email, e.g. `name@cartagena.no`).
  A fresh backlog is usually left *unassigned* (assigned later in planning), so omit it unless
  the user wants these owned now — **ask them**. To assign the whole batch instead of per item,
  use the `AZDO_ASSIGNED_TO` env var at create time. An invalid identity fails the dry run, so
  a typo never reaches the board.
- **Body — depends on type:**
  - `Bug`: `Microsoft.VSTS.TCM.ReproSteps`.
  - `User Story` / `Product Backlog Item` / `Requirement`: `System.Description` **plus**
    `Microsoft.VSTS.Common.AcceptanceCriteria`.
  - **Basic `Issue`**: `System.Description` **only** — Basic's `Issue` defines neither
    `Microsoft.VSTS.TCM.ReproSteps` nor `Microsoft.VSTS.Common.AcceptanceCriteria`, and adding
    them fails `validateOnly` at dry run (the very failure this skill exists to prevent).
- These body fields are **HTML**. Escape `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`, and use
  `<br>` / `<b>` for layout. Unescaped `<` / `>` either render wrong or get stripped. Pull the
  finding's `current` / `expected` / `recommendation` / `notes` into the body so the ticket is
  actionable on its own.

**Carry the finding's `key` onto every item** (top-level `"key"`, alongside `"type"`). That
`key` is the thread back to the source row — `ado-create-work-items` echoes it into
`backlog_result.json` and `ado-writeback-tracking` uses it to write the ticket link onto the
right row. Drop it and write-back can't match.

Tiny example (one defect item; full shape in `references/data-contracts.md`):

```json
{
  "key": "1",
  "type": "Bug",
  "fields": {
    "System.Title": "Portal label \"Auto\" should display CRM-canonical \"Automotive Cargo\"",
    "Microsoft.VSTS.Common.Priority": 1,
    "System.Tags": "naming-audit; crm-portal; review-confirmed",
    "Microsoft.VSTS.TCM.ReproSteps": "<b>Current:</b> Auto<br><b>Expected:</b> Automotive Cargo"
  }
}
```

## 5. Optional: define the grouping parent

If these findings are one initiative, add a top-level `parent` object with a `Feature` (or
`Epic`) `type` and its own `fields` (`System.Title`, `System.Tags`, optional `Priority`).
`create-backlog.cs` creates the parent first and links every item under it via
`System.LinkTypes.Hierarchy-Reverse`. One parent per backlog run.

## 5b. Estimate time — a child Task per item

Attach a **time estimate** to each item as a **child Task** that carries the hours. (Agile's
User Story has no hours field — only Story Points — so the hour estimate lives on a Task,
uniformly under every Bug/Story; see `docs/adr/0001`.) Add an `estimate` object per item
(schema in `references/data-contracts.md`).

Estimate with **work-kind anchors**, adjusted for the detail. There is no team history to
calibrate from, so anchors are the baseline:

| kind | baseline | bump up when… |
|---|---|---|
| rename (one spot) | 1–2h | appears across many screens / variants |
| rename (multi) | 3–4h | |
| disambiguation / mapping | 4–8h | maps to many CRM fields (e.g. 5) → top of band |
| missing field (UI + submit) | 6–8h | + validation; + compliance/regulatory → +2–4h |
| structural (new column / split) | 4–6h | |

Round to whole hours. If an item exceeds ~16h (2 days), **propose splitting it** instead of
estimating one big block.

**Estimate in detail:** break each item into steps with hours that sum to the total. Put the
total in the Task's `Microsoft.VSTS.Scheduling.OriginalEstimate` and `RemainingWork`, and the
**breakdown** (each step + hours, then the total) as HTML in the Task's `System.Description`.

**Suggest, then confirm — never silently apply.** Show the user a table and wait:

```
#     Type        kind            Est    why
6078  User Story  missing+comply  8h     new field + submit + compliance check
...                               ────
                                  ~41h   (~5–6 days)
```

Let the user adjust any value ("6078 = 6h"), then write the agreed numbers into each item's
`estimate.task`. Optionally set the parent Feature's `Microsoft.VSTS.Scheduling.Effort` to the
batch total so it rolls up on the Feature.

## 6. Write backlog_input.json and hand off

Assemble `{ org?, project?, parent?, items: [...] }` per the contract and write it (e.g.
`backlog_input.json` next to the findings). `org` / `project` are optional in the file —
`AZDO_ORG` / `AZDO_PROJECT` override them — but include them for clarity.

Sanity-check before handing off: every item has a `key`, a `type` valid for the discovered
process, a non-empty `System.Title`, and properly escaped HTML in body fields.

Then hand off to **ado-create-work-items**, which dry-runs first (`AZDO_DRY_RUN=true`,
`validateOnly`) to catch any remaining type/field problems against the live board before a
real run. If a type still fails validation there, the process likely doesn't have it — come
back to step 1.
