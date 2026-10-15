---
name: github-extract-findings
description: >-
  Normalize ANY input into findings.json — the first step toward turning review
  notes into a GitHub Issues backlog. Use whenever someone hands you a list of
  issues, discrepancies, gaps, review notes, or audit results they want to act
  on: an Excel/CSV/TSV audit sheet, a Word/PDF/Markdown spec, or chat/text pasted
  into the conversation. Trigger even when the user does NOT say "extract" — e.g.
  "here's a naming audit", "these are the problems we found", "turn this
  spreadsheet into GitHub issues", "I reviewed the code and noted these gaps",
  "make a backlog from this doc". If the goal is eventually GitHub Issues, this
  runs first. Hands off to github-triage-findings (then classify-github-issues,
  github-create-issues). Driven end-to-end by the findings-to-github-issues orchestrator.
effort: max
---

<!-- generated: third-party requirements -->
> **Requires:** `pip install openpyxl` — this skill's scripts import `openpyxl`.

# github-extract-findings

Turn whatever the user has — a spreadsheet, a doc, or pasted text — into a clean
`findings.json`. This is the entry point of the github-backlog pipeline: every later
step (triage, classify, create, write-back) keys off the fields you produce here,
so the value is a faithful, lossless normalization, not interpretation.

Output contract: `findings.json` shape in
`references/data-contracts.md`. Read it before writing —
the field names are load-bearing and the bundled scripts depend on them.

## Schema (target)

Each finding normalizes to these fields (full table in data-contracts.md):

- `key` — **required.** Stable id per finding; carried through every later file so
  the created issue can be written back to the right source row.
- `current` / `expected` — **required.** Observed value vs the canonical/correct one.
- `section`, `recommendation`, `notes` — optional context; carried into the issue body.
- `kind` — optional: `rename | disambiguation | missing | other`. Helps the
  classifier pick labels.
- `severity` — optional: `Critical | High | Medium | Low`. Drives priority label + triage.
- `status` — optional free text (`confirmed`, `needs-review`, ...). A useful triage filter.

Top level also records `source` (a human-readable origin) and `keyColumn` (which
source column became `key`).

## 1. Get the content in front of you

**Spreadsheets** (`.xlsx`, `.xlsm`, `.csv`, `.tsv`) are binary or crash the Windows
cp1252 console, so don't open them blind — dump them to UTF-8 text first. The helper
forces UTF-8 so the rows survive intact:

```powershell
python "${CLAUDE_SKILL_DIR}/scripts/read_source.py" "<path-to-file>"
```

Then read the printed dump. For a big sheet, write it to a file and Read that
(default cap is 200 rows; pass `--max-rows 0` for everything):

```powershell
python "${CLAUDE_SKILL_DIR}/scripts/read_source.py" "<path-to-file>" --out "<workdir>/source-dump.txt" --max-rows 0
```

The dump prefixes each row with its index — `[0]` is usually the header row, `[1]`
onward the data. Multiple sheets are emitted under `=== SHEET: ... ===` markers.

**Non-tabular input** (`.docx`, `.pdf`, `.md`, `.txt`, or text pasted into the chat)
needs no helper — read it directly with the Read tool, or just use the pasted text.

## 2. Map source columns to schema fields

Look at the header row / structure and decide which column means `current`, which
means `expected`, etc. **When a column's meaning is unclear, ask the user rather
than guess silently.** A wrong mapping corrupts every downstream issue.

- `key`: prefer an existing stable column (a `#`, `ID`, or row-number column). If
  none exists, assign `"1","2","3",...` in row order. Record your choice in `keyColumn`.
- `kind` and `severity`: infer **only if the source actually supports it.**
- Keep `current`/`expected` verbatim — later steps put them in the issue body.

## 3. Write findings.json

Write it to a working directory **next to the source** so all pipeline artifacts
stay together. Tell the user the exact path you wrote.

## 4. Summarize and confirm before handoff

Show the user:
- the column → field mapping you used (and what `key` came from),
- counts: total findings, and a breakdown by `severity`/`kind` if you set them,
- the first 3–5 normalized findings.

Once the user confirms the mapping looks right, hand off to **github-triage-findings**.

## Notes

- `key` uniqueness matters — duplicate keys break write-back.
- Write-back to the source only works for spreadsheets.
- One finding per actionable discrepancy. Don't merge unrelated rows.
