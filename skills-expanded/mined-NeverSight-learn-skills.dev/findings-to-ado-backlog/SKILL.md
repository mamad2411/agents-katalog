---
name: findings-to-ado-backlog
description: >-
  End-to-end orchestrator that turns findings from ANY input (audit spreadsheet, code/security
  review, QA report, meeting notes, a pasted list of issues) into an Azure DevOps backlog of
  linked work items. Drives the six sibling ado-backlog skills in order with safety gates.
  Trigger whenever the user says "turn this audit/spreadsheet/review/list of issues into ADO
  work items", "create a backlog from these findings", "file these as ADO tickets/bugs/stories",
  "import this xlsx/csv into Azure DevOps", "make work items from this report", or hands you a
  source document and asks for it to land in ADO. This is the headline, one-shot entry point
  (/ado-backlog:run wraps it). Prefer this over running the sub-skills piecemeal when the user
  wants the whole pipeline. Not for editing existing items individually — use ado-create-work-items.
argument-hint: "[path-to-findings-file]"
effort: max
---

<!-- generated: third-party requirements -->
> **Requires:** `pip install openpyxl` — this skill's scripts import `openpyxl`.

# findings-to-ado-backlog (orchestrator)

Run the full pipeline: a source document in, an ADO backlog out. You coordinate six
sibling skills; each owns its step and its data contract. Your job is to sequence them,
keep the working files together, and enforce the safety gates so nothing irreversible
happens without the user seeing it first.

**Why an orchestrator:** the value is in the gates, not the glue. Creating work items is a
write the user cannot easily undo, so the pipeline is deliberately staged: read-only
extraction and classification first, a dry run that creates nothing, an explicit human
approval, then the real write. Each sub-skill is reusable on its own; this skill is the
teachable happy path that ties them together.

## Data flow

Three small JSON files carry state between steps. They share a stable **`key`** per finding
(a row number or ID column) so a created ticket can be traced back to its source row.
Full shapes live in `references/data-contracts.md` — read it once; do
not duplicate schemas here.

```
extract-findings      -> findings.json
classify-work-items   -> backlog_input.json   (consumed by create-backlog.cs)
ado-create-work-items -> backlog_result.json  (consumed by tracking.py writeback)
```

**Working directory:** create one beside the source (e.g. next to the xlsx) and keep all
three JSON files there. This keeps a run self-contained and re-runnable.

## Process

### 0. Prereqs + auth (optional but recommended on first run)

Confirm the toolchain is present before you invest in extraction. This is read-only.

```powershell
powershell -ExecutionPolicy Bypass -File "${CLAUDE_SKILL_DIR}/scripts/setup_check.ps1"
```

It checks `az login`, .NET >= 10, Python + openpyxl, and the `AZDO_ORG` / `AZDO_PROJECT`
env vars. For auth specifics (Entra token vs `AZDO_PAT`, org/project), delegate to
**ado-auth**. The create script defaults to an Entra token via
`az account get-access-token --resource 499b84ac-1321-427f-aa17-267ca6975798 --query accessToken -o tsv`.

### 1. Extract → `findings.json` (delegate to **extract-findings**)

Have **extract-findings** read the source (it uses
`${CLAUDE_SKILL_DIR}/scripts/read_source.py` for xlsx/csv; docs and pasted text are read
directly) and normalize it to `findings.json`. **Confirm the column mapping with the user**
before moving on — which column is the `key`, which are `current` / `expected`, where
`severity` and `status` come from. A wrong mapping silently poisons everything downstream.

### 2. Triage → scoped subset (delegate to **triage-findings**)

Don't file everything blindly. Have **triage-findings** filter `findings.json` to the wave
worth creating now. **Recommend Critical + confirmed first** — it is the smallest defensible
batch and proves the pipeline before you fan out. Hold `needs-review` items for a later wave
and tell the user you are doing so.

### 3. Classify → `backlog_input.json` (delegate to **classify-work-items**)

Have **classify-work-items** map the scoped findings to ADO work items. It must:

- **Discover the target project's process** (Agile / Scrum / Basic / CMMI) and pick
  **industry-standard types that actually exist on that board** — e.g. a defect is `Bug` on
  Agile/Scrum/CMMI but Basic has no Bug (use `Issue`). See the process→types table in
  `data-contracts.md`.
- Optionally add a **`Feature` or `Epic` parent** to group the batch; every item links under
  it via `System.LinkTypes.Hierarchy-Reverse`.
- **Decide assignment — ask the user who these go to.** A fresh backlog is usually created
  *unassigned* (assigned later in planning), but ask: leave unassigned, assign to the user
  themselves, assign the batch to one person, or map a per-row owner. Set `System.AssignedTo`
  (a UPN like `name@domain`) on each item, or assign the whole batch at create time with the
  `AZDO_ASSIGNED_TO` env var. The dry run validates the identity before any real write.
- Emit raw ADO field reference names (`System.Title`, `Microsoft.VSTS.Common.Priority`,
  `System.Tags`; Bug body `Microsoft.VSTS.TCM.ReproSteps`; Story/PBI body `System.Description`
  + `Microsoft.VSTS.Common.AcceptanceCriteria`). HTML fields must be valid HTML.
- **Estimate time** per item and attach it as a **child Task** (hours in Original/Remaining
  Work; the detailed breakdown in the Task description) — see `classify-work-items`.

> **GATE — estimates.** classify proposes the hours per item as a table. **Show it and get the
> user's OK / adjustments before the dry run.** Estimates are cheap to fix now, annoying to fix
> across already-created Tasks.

### 4. DRY RUN → validate, create nothing (delegate to **ado-create-work-items**)

This is the first gate. The create script defaults to dry run, which sends each item to ADO
with `validateOnly=true` — it catches a bad type, a missing required field, or a wrong
area/iteration path **without creating anything**.

```powershell
$env:AZDO_DRY_RUN = "true"
dotnet run "${CLAUDE_SKILL_DIR}/scripts/create-backlog.cs" -- "<workdir>/backlog_input.json"
```

Show the user the validated PASS/FAIL list (type, title per `key`). Fix any FAIL in
`backlog_input.json` and re-run until clean.

> **GATE — stop here.** Do not proceed to the real run until the user has explicitly
> approved the validated list. Present the count, the types, and the parent, and wait for a
> clear yes.

### 5. REAL RUN → `backlog_result.json` (delegate to **ado-create-work-items**)

Only after approval. Setting `AZDO_DRY_RUN` to `false` creates the parent (if any), every
child, **and a child Task (with the hour estimate) under each item**, links them all, and writes
`backlog_result.json`.

```powershell
$env:AZDO_DRY_RUN = "false"
dotnet run "${CLAUDE_SKILL_DIR}/scripts/create-backlog.cs" -- "<workdir>/backlog_input.json"
```

Then **verify the created items** — confirm each `key` got an `id` and `url` in
`backlog_result.json`, and that any rows logged `FAILED` are surfaced to the user, not buried.

### 6. Write-back tracking — spreadsheets only (delegate to **ado-writeback-tracking**)

**Only if the source is a spreadsheet** (a row per finding). For docs/pasted text there is no
row to write to — skip this step.

> **GATE — back up the source first.** Write-back mutates the user's spreadsheet in place.
> Copy the file before running it.

Have **ado-writeback-tracking** drive `${CLAUDE_SKILL_DIR}/scripts/tracking.py`: first
ensure the `Ticket ID | Ticket URL | WI State | Created` columns exist (`add-columns`), then
match each result `key` to the source key column and fill them (`writeback`). Both subcommands
are idempotent — rows that already have a Ticket ID are left as-is — so a re-run is safe. Pass
`--key` matching the key column you confirmed in step 1.

### 7. Report back

Summarize the run for the user:

- **Created:** count + clickable links (the `url` per item, and the parent if any).
- **Held / skipped:** the triage wave you deferred (e.g. `needs-review`), plus any dry-run
  FAILs or real-run errors and why.
- **Follow-ups:** the obvious next wave (run steps 2–6 again on the deferred subset), and any
  ambiguous findings that need a human decision before they can be classified.

## Safety gates (the whole point)

1. **Dry run before real** — step 4 always precedes step 5; the script defaults to dry run.
2. **Explicit approval before any write** — never jump from validation to creation on your own.
3. **Back up the source before write-back** — step 6 edits the user's file in place.

If anything is ambiguous (column mapping, which process, which parent), ask rather than
guess — a wrong guess multiplies across every item in the batch.
