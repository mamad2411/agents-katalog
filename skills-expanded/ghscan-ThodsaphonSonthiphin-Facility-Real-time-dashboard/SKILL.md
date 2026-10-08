---
name: extract-findings
description: "Normalize ANY input into findings.json — the first step toward
  turning review notes into an Azure DevOps backlog. Use whenever someone hands
  you a list of issues, discrepancies, gaps, review notes, or audit results they
  want to act on: an Excel/CSV/TSV audit sheet, a Word/PDF/Markdown spec, or
  chat/text pasted into the conversation. Trigger even when the user does NOT
  say \"extract\" — e.g. \"here's a naming audit\", \"these are the problems we
  found\", \"turn this spreadsheet into tickets\", \"I reviewed the portal and
  noted these gaps\", \"make a backlog from this doc\". If the goal is
  eventually ADO work items, this runs first. Hands off to triage-findings (then
  classify-work-items, ado-create-work-items). Driven end-to-end by the
  findings-to-ado-backlog orchestrator."
---
<!-- generated: third-party requirements -->
> **Requires:** `pip install openpyxl` — this skill's scripts import `openpyxl`.

# extract-findings

Turn whatever the user has — a spreadsheet, a doc, or pasted text — into a clean
`findings.json`. This is the entry point of the ADO-backlog pipeline: every later
step (triage, classify, create, write-back) keys off the fields you produce here,
so the value is a faithful, lossless normalization, not interpretation.

Output contract: `findings.json` shape #1 in
`references/data-contracts.md`. Read it before writing —
the field names are load-bearing and the bundled scripts depend on them.

## Schema (target)

Each finding normalizes to these fields (full table in data-contracts.md):

- `key` — **required.** Stable id per finding; carried through every later file so
  the created ticket can be written back to the right source row.
- `current` / `expected` — **required.** Observed value vs the canonical/correct one.
- `section`, `recommendation`, `notes` — optional context; carried into the work item.
- `kind` — optional: `rename | disambiguation | missing | other`. Helps the
  classifier pick a work-item type.
- `severity` — optional: `Critical | High | Medium | Low`. Drives Priority + triage.
- `status` — optional free text (`confirmed`, `needs-review`, ...). A useful triage filter.

Top level also records `source` (a human-readable origin) and `keyColumn` (which
source column became `key`).

Tiny example:

```json
{
  "source": "Downloads/CRM_Portal_Naming_Audit.xlsx (sheet 'CRM-Portal Audit')",
  "keyColumn": "#",
  "findings": [
    { "key": "1", "section": "Cargo Classification", "current": "Auto",
      "expected": "Automotive Cargo", "kind": "rename", "severity": "Critical",
      "status": "confirmed", "recommendation": "Rename to: Automotive Cargo",
      "notes": "'Auto' loses the word 'Cargo'." }
  ]
}
```

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
onward the data. Multiple sheets are emitted under `=== SHEET: ... ===` markers; if
several look relevant, ask the user which sheet holds the findings.

**Non-tabular input** (`.docx`, `.pdf`, `.md`, `.txt`, or text pasted into the chat)
needs no helper — read it directly with the Read tool, or just use the pasted text.
`read_source.py` only handles tabular types and will reject the rest by design.

## 2. Map source columns to schema fields

Look at the header row / structure and decide which column means `current`, which
means `expected`, etc. The mapping is the one genuinely ambiguous step, and a wrong
guess corrupts every downstream ticket — so **when a column's meaning is unclear,
ask the user rather than guess silently.** Typical traps: a single "Issue" column
that mixes current+expected; "Comment"/"Notes" vs "Recommendation"; a "Status"
column that's really severity.

- `key`: prefer an existing stable column (a `#`, `ID`, or row-number column). If
  none exists, assign `"1","2","3",...` in row order. Record your choice in
  `keyColumn` (use the column header, or `"row-index"` when you assigned them).
- `kind` and `severity`: infer **only if the source actually supports it.** If the
  sheet has no severity signal, leave `severity` off — do not invent one. Same for
  `kind`: only set it when the row clearly reads as a rename/disambiguation/missing
  item; otherwise omit or use `other`.
- Keep `current`/`expected` verbatim. Don't summarize away the exact strings — later
  steps put them in the ticket body and write them back beside the source row.

## 3. Write findings.json

Write it to a working directory **next to the source** (e.g. the source's folder, or
a `backlog/` subfolder there) so the whole pipeline's artefacts — `findings.json`,
later `backlog_input.json`, `backlog_result.json` — stay together with the data they
came from. Tell the user the exact path you wrote.

## 4. Summarize and confirm before handoff

Show the user a short recap so they can catch a bad mapping now, not after tickets
exist:

- the column → field mapping you used (and what `key` came from),
- counts: total findings, and a breakdown by `severity`/`kind` if you set them,
- the first 3–5 normalized findings.

Once the user confirms the mapping looks right, hand off to **triage-findings**
(which filters/prioritizes before **classify-work-items** turns findings into
`backlog_input.json`). If the user is running the **findings-to-ado-backlog**
orchestrator, it will carry the confirmed `findings.json` forward automatically.

## Notes

- `key` uniqueness matters — duplicate keys break write-back. If the chosen column
  has dupes, fall back to assigned `"1","2",...` and say so.
- Write-back to the source only works for spreadsheets (there's a row to write into).
  For docs/pasted text, assigned keys are fine but `tracking.py` write-back won't apply.
- One finding per actionable discrepancy. Don't merge unrelated rows; don't split a
  single row into several findings unless it genuinely lists multiple distinct issues.
