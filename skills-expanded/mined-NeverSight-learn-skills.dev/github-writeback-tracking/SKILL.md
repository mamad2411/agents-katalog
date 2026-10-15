---
name: github-writeback-tracking
description: >-
  Add traceability columns to a spreadsheet source and write created GitHub issue
  numbers/URLs back into it, matched row-by-row by key. Use this right after
  creating issues — when you have a github_backlog_result.json and the original
  source was a spreadsheet (xlsx/csv). Triggers on "write the issue links back",
  "track which row got which issue", "update the spreadsheet with the GitHub IDs",
  "fill in the issue column", "close the loop on the audit sheet".
effort: max
---

<!-- generated: third-party requirements -->
> **Requires:** `pip install openpyxl` — this skill's scripts import `openpyxl`.

# github-writeback-tracking

Closes the loop: once issues exist in GitHub, stamp their numbers and URLs back onto
the spreadsheet the findings came from. The link between a row and its issue is the
**`key`** field, carried from [[github-extract-findings]] through `github_backlog_result.json`.

## When this applies

- **Spreadsheet sources only** (`.xlsx` / `.csv` / `.tsv`).
- **Doc / pasted-text sources**: skip the script; just report the created issue links from `github_backlog_result.json` in chat.
- You need `github_backlog_result.json` from [[github-create-issues]].

## Before you write

Back up the user's source file first — `github_tracking.py` edits it **in place**:

```powershell
Copy-Item "<file>.xlsx" "<file>.bak.xlsx"
```

## Step 1 — add tracking columns (idempotent)

Appends `Issue #`, `Issue URL`, `State`, `Created` after the last used column. Safe
to run repeatedly — columns that already exist are not duplicated.

```powershell
python "${CLAUDE_SKILL_DIR}/scripts/github_tracking.py" add-columns --source "<file>" --key "#"
```

## Step 2 — write the issue links back (idempotent)

Matches each `github_backlog_result.json` item's `key` to the source key column and
fills the four tracking columns. Rows that already hold an `Issue #` are left as-is.

```powershell
python "${CLAUDE_SKILL_DIR}/scripts/github_tracking.py" writeback `
  --source "<file>" `
  --result "<workdir>/github_backlog_result.json" `
  --key "#"
```

Per row it writes: `Issue #` ← `items[].number`, `Issue URL` ← `items[].url`,
`State` ← `open`, `Created` ← `YYYY-MM-DD HH:MM`.

## The `--key` must line up

The `--key` column name must match the `keyColumn` chosen in [[github-extract-findings]] and
the `key` values in `github_backlog_result.json`. Values are compared as strings.

If the script prints `warn: key <x> not found in source`, the key in the result
doesn't match any value in that column — re-check `--key` and that the source hasn't
been re-sorted since extraction.
