---
name: qa-export-evidence
description: >-
  Build QA test evidence for a web app's export buttons (CSV / Excel / PDF / Print) and turn it
  into an .xlsx test report: walk each page on a signed-in CDP Chrome, screenshot every step
  (page → filter → result → export button → queued alert → queue modal → the downloaded file
  opened), verify the file with a real parser, then write a workbook with a Summary sheet and one
  sheet per case (B2 title · B4 Test Result · B5 Test Environment · B6 Test Date · B7 Actual Result ·
  captioned screenshots in a 2-column grid). Use WHENEVER the work is "test evidence for export",
  "test the Export Excel/PDF/CSV buttons", "QA test report xlsx", "ทดสอบปุ่ม Export", "หลักฐานการทดสอบ
  export", "make_qa_report", or a request to rebuild a QA report workbook from an evidence folder.
---

# QA evidence for export buttons

**In** a list of pages × formats on one environment · **Out** `<run>/` with `cases.json`,
`evidence/` (one folder per case: `steps.csv`, `run.json`, the downloaded file, `screenshots/`),
and the report `.xlsx`.

```bash
RUN=qa-reports/<run>                      # change this line only
S=skills/qa/export-evidence/scripts

# a Chrome with remote debugging, signed in by a person:
#   chrome --remote-debugging-port=9222 --user-data-dir=~/.cache/qa-chrome [--headless=new]
uv run $S/collect_export.py $RUN/cases.json $RUN/evidence                 # all cases
uv run $S/collect_export.py $RUN/cases.json $RUN/evidence <slug>          # re-run one; the others stay
uv run $S/make_qa_report.py $RUN/evidence --out $RUN/<name>.xlsx \
    --title "<Summary title>" --env UAT --date "NOV 9, 2026" \
    [--only-sheets "reports export excel"] [--labels references/labels-th.json]
```

Both scripts only read and write **inside the folder they run from** (`cases.json`, the evidence dir, `--out`, `--labels`); run them from the repo root.

1. **Inventory from source, not from clicking around.** The app's menu / route config plus the page
   templates show which pages carry an export bar. Write the list down with the kind of export each
   one uses (see below) — the page set changes between releases, so re-check before each run.
2. **Write `cases.json`.** One case per page × format. `sheet` names the group a case belongs to
   (`--only-sheets` splits one run into several workbooks). `references/cases-example.json` has the
   shape; `references/ui-th.json` shows the `ui` block for a Thai UI (SweetAlert + Bootstrap modal
   defaults are built in).
3. **Sign in first.** A person signs the CDP profile into the app. An agent never types a password
   into a login form unless the owner authorised that exact run — and then it reads the value from a
   local, gitignored config and never prints, logs or screenshots it.
4. **Collect, then read every FAIL.** The cause sits in `run.json` → `net` (the enqueue status and
   body, the queue row text, the export GET error). Fix what is on our side first: the date range,
   the selector, waits, row selection. Then re-run that slug. If the cause is a real app bug, the
   case stays FAIL with that evidence; nobody patches the app to make the test pass.
5. **Build the report and hand it over.** If it goes to a shared drive, upload through the drive's
   own file chooser, then confirm the file is in the folder at the same size.

## Evidence contract (what the builder reads)

| file | columns |
|---|---|
| `evidence/index.csv` | `no,title,folder,result` required · `sheet` (group) · `actual` (B7 text) · any other column shows on Summary |
| `evidence/environment.csv` | `key,value` → Summary header block |
| `evidence/<folder>/steps.csv` | `step,action,result,evidence` (+ anything) · `evidence` = PNG path relative to `<folder>` |

The collector writes all three, so a hand-made run (manual test, another tool) only has to follow
the same columns to get the same workbook.

## Two export mechanisms that look identical on screen

- **Queued**: the click sends `POST …<ui.enqueue_path>` with the report type and format → an alert
  ("queued") → a queue modal → download from the queue row once it says success. Each export leaves
  a job in the queue, which is the only side effect. `kind: auto` detects it.
- **Direct**: a synchronous blob `GET <url><ui.export_path>?format=…`. PDF is often labelled
  **"Print"** here, not "Export PDF" — the default button regex covers both.
- **Viewer** (`kind: stimulsoft`): a row button opens a report viewer; its Save menu → a PDF item →
  an export-settings dialog → OK is the download. Set `open` to the row button text.

## Traps

- **An empty table has three indistinguishable causes** — genuinely empty, a scope clamp returning
  200 with zero rows, or a 403. Never record "no data" as a pass without a row count on screen
  (`ui.rows_regex` picks it up from the page text).
- **Pick a date range that returns rows** before blaming the export; test data is sparse.
- **Prod safety.** Click only the filter, the query button, row checkboxes, the export button, the
  alert's OK and the queue download. Never save, submit, confirm or delete. Never press Enter outside
  the date inputs. Prod downloads hold real data: they stay local, only the workbook is shared, and
  `~/Downloads` is cleaned afterwards.
- **One collector at a time.** Every CDP client sets Chrome's download behaviour, so a second client
  sends the first one's files to `~/Downloads` and leaves it a 0-byte copy.
- **"not successful" contains "successful".** The queue status check looks for the failure words
  first (`ui.failure_words`), in any language.
- **Large tables need a narrow range.** Too wide a range returns a "too much data" 400, and a PDF of
  thousands of rows can stay at "PROCESSING 100%" forever while Excel works. Record it as a finding.
- Put each FAIL's cause into `cases.json` `"note"`, then run `collect_export.py … --index-only`: that
  rewrites `index.csv` without opening a browser, and the note becomes the case's Actual Result text.
- Screenshots are embedded in the `.xlsx`; gitignore `evidence/**/screenshots/` and re-run the
  collector before rebuilding from a fresh clone.
