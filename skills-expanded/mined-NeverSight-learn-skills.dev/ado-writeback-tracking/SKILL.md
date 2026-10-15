---
name: ado-writeback-tracking
description: >-
  Add traceability columns to a spreadsheet source and write created Azure
  DevOps ticket IDs/URLs back into it, matched row-by-row by key. Use this
  right after creating work items — when you have a backlog_result.json and the
  original source was a spreadsheet (xlsx/csv). Triggers on "write the ticket
  links back", "track which row got which ticket", "update the spreadsheet with
  the ADO IDs", "fill in the ticket column", "close the loop on the audit
  sheet", or any request to record created-item IDs back onto the source rows.
  Runs the bundled tracking.py (add-columns + writeback). For doc/pasted-text
  input there are no rows to write to — in that case just report the created
  links instead.
effort: max
---

<!-- generated: third-party requirements -->
> **Requires:** `pip install openpyxl` — this skill's scripts import `openpyxl`.

# ado-writeback-tracking

Closes the loop: once items exist in ADO, stamp their IDs and URLs back onto the
spreadsheet the findings came from, so every row shows which ticket it became.
This makes the source self-tracking — anyone reopening the sheet sees status
without cross-referencing ADO. The link between a row and its ticket is the
**`key`** field (see `references/data-contracts.md`),
carried from [[extract-findings]] (`keyColumn`) through `backlog_result.json`.

## When this applies

- **Spreadsheet sources only** (`.xlsx` / `.csv` / `.tsv`). There must be one
  row per finding to write back to.
- **Doc / pasted-text sources have no rows** — skip the script entirely and just
  report the created ticket links (parent + per-item URLs) from
  `backlog_result.json` in chat. Don't fabricate a spreadsheet to write to.
- You need `backlog_result.json` from [[ado-create-work-items]] (which runs
  `create-backlog.cs`). Each `items[].id` is the created work item; rows whose
  key has no matching created `id` are simply skipped.

## Before you write

Back up the user's source file first — `tracking.py` edits it **in place** and
overwrites it. A quick copy keeps you safe if a key mismatch or wrong `--key`
sends links to the wrong rows:

```powershell
Copy-Item "<file>.xlsx" "<file>.bak.xlsx"
```

## Step 1 — add tracking columns (idempotent)

Appends `Ticket ID`, `Ticket URL`, `WI State`, `Created` after the last used
column. Safe to run repeatedly — columns that already exist are not duplicated.
Run this once before the first writeback so the target columns exist:

```powershell
python "${CLAUDE_SKILL_DIR}/scripts/tracking.py" add-columns --source "<file>" --key "#"
```

It prints which columns map to which letters (xlsx) or confirms they're ensured
(csv). `--key` defaults to `#` if omitted, but pass it explicitly to match.

## Step 2 — write the ticket links back (idempotent)

Matches each `backlog_result.json` item's `key` to the value in the source's key
column and fills the four tracking columns. Rows that **already hold a Ticket
ID are left as-is**, so re-running after a partial create only fills the new
rows:

```powershell
python "${CLAUDE_SKILL_DIR}/scripts/tracking.py" writeback --source "<file>" --result "<path>/backlog_result.json" --key "#"
```

Per row it writes:

- `Ticket ID` ← `items[].id`
- `Ticket URL` ← `https://dev.azure.com/{org}/{project}/_workitems/edit/{id}` (built from the `org`/`project` in `backlog_result.json`)
- `WI State` ← `New` (the state freshly created items land in)
- `Created` ← a `YYYY-MM-DD HH:MM` timestamp

It logs each `key -> #id`, prints the parent link if one exists, and ends with
`wrote N ticket links back to source`.

## The `--key` must line up across all three files

This is the single most common failure. The `--key` you pass here must be the
**same column name** as:

- `keyColumn` chosen in [[extract-findings]] (e.g. `#`, `ID`, `Row`), and
- the `key` value carried in `backlog_input.json` and `backlog_result.json`.

Values are compared as strings. If the script prints
`warn: key <x> not found in source`, the `key` in the result doesn't match any
value in that column — re-check `--key` (right column?) and that the source
hasn't been re-sorted or had rows removed since extraction. If it raises
`missing column '<name>' — run add-columns first`, you skipped Step 1 (or pointed
`--key` at a column that isn't in the sheet).

## Tiny example

`backlog_result.json` (abridged):

```json
{ "org": "Cartagena365", "project": "GlassHull",
  "items": [ { "key": "1", "id": 6073, "type": "Bug", "title": "..." } ] }
```

After writeback, the source row whose `#` column is `1` gains:
`Ticket ID=6073`, `Ticket URL=https://dev.azure.com/Cartagena365/GlassHull/_workitems/edit/6073`,
`WI State=New`, `Created=2026-06-02 14:05`.

## Notes

- No ADO auth or network call happens here — this step only reads the JSON
  result and edits the local file. (Auth lives in [[ado-auth]] / the create step.)
- The bundled Python forces UTF-8, so accented/Thai text survives even on a
  cp1252 PowerShell console.
- This is the final stage of the [[findings-to-ado-backlog]] pipeline:
  [[extract-findings]] → [[triage-findings]] → [[classify-work-items]] →
  [[ado-create-work-items]] → **ado-writeback-tracking**.
