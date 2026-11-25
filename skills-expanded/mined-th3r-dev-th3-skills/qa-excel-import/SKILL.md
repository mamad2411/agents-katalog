---
name: qa-excel-import
description: >-
  QA an Excel-template import feature (a workbook with dropdowns → the portal's "import" modal →
  validate → submit): design the minimum test set from the template's dropdowns × the database's
  allowed combinations, build the workbooks, predict every verdict with a DB preflight, run them
  through the web with Playwright (validate for everything, submit only for real documents) and
  verify the created rows in the database. Use WHENEVER the work is "test the xlsx import", "write
  test cases for the import template", "are all dropdown values usable", "ทดสอบนำเข้า excel",
  "ออก test case import", or before a new template / dropdown list is handed to operators.
---

# QA an Excel template import

**In:** the template (`.xlsx` with its hidden dropdown sheet) + the documents to import, and an
**adapter** that knows your importer (`scripts/adapter_example.py` is the contract).
**Out:** a test matrix with expected verdicts, one `.xlsx` per case, a run log with actual
verdicts, and the created document ids checked in the database — all in one `report.xlsx`.

## 0. The contract lives in code — read it before designing

Find the importer's validator (the service behind the validate endpoint) and read it from the
branch the portal runs, not the local checkout. Note which functions decide the verdicts
(header parsing, required columns, grouping, the master lookups, the allowed-pairs check) and
encode them in the adapter's `check()`. The portal's own build (login footer / about page) may be
older than `develop`; **a mismatch between preflight and web is a finding, not noise.**

## 1. Derive the test dimensions from the dropdowns, not from imagination

Cross the template's dropdown columns with the database's allowed-pairs table and write the
decision table down (`references/test-design.md` has the method and the equivalence classes).
Three lists fall out of it and go first in the report: dropdown values that never pass, pairs
that pass but are missing from the dropdown, and pairs the importer refuses that real documents
already carry.

## 2. Minimum set — one file per verdict class, one row per pair

Two facts usually shrink the set:

- **One file = one document, many details.** Rows group by a signature of columns; each group is
  one detail and its error lands on the group's first row. So all pairs of one movement fit in one
  file as long as each row's signature differs.
- **DB lookups run only when the cheap checks are clean** (required cells, qty > 0, all-or-nothing
  groups). Never mix a blank-cell case into a pair file — it hides every pair error.

| id | kind | covers | expected |
|---|---|---|---|
| R* | real doc, **submit** | each transport type seen in real rows; multi-detail; multi-partner | VALIDATED, then created |
| V* | synthetic, validate only | all valid pairs per movement (+ pairs missing from the dropdown, typed) | VALIDATED |
| N* | synthetic, validate only | dead values + cross pairs · wrong-direction pairs · unresolvable header aliases | the exact error string |
| B* | synthetic, validate only | one cheap-check boundary per file (qty `0`, qty blank, half-filled group …) | that row's message, or VALIDATED for the in-range side |

Every movement and every transport value appears at least once in a passing file; every pair
appears exactly once. **Synthetic files are never submitted** — validate proves acceptance without
writing a document. Give every case a `scenario` (`Happy Case` / `Edge Case` / `Negative`) and a
`trace` (the requirement it proves); both print on the case's sheet in `report.xlsx`.

**Smoke vs full.** Smoke = one R* per transport type (validate only) + V1 + N1, rerun whenever the
portal build or the importer diff changes; if any fails, run the full set. Full = every case, when
the dropdowns change or before a template is handed to operators. When time is short, order by what
a miss costs: a dead pair that *passes* (wrong data written) → a valid pair that fails (operators
blocked) → header aliases → boundaries.

## 3. Build, then preflight every file

Build with openpyxl from the real template. **openpyxl drops extended (x14) data validations** —
re-add them as plain list validations pointing at the same master ranges, or the operator gets a
file without dropdowns. Header values go where the importer reads them (labels only beside them);
dates as the importer parses them (ISO text is safest).

Preflight (`adapter.check`) must equal the expected column before anything goes to the web. Also
flag a lookup that matches **more than one** master row — a `getOne()` would pick one silently.

## 4. Run on the web — Playwright

`cases.json` sits next to the files (`references/cases-example.json`):

```bash
S=skills/qa/excel-import/scripts
uv run $S/run_web.py login  --adapter adapter.py --account acme                  # headed; a PERSON signs in
uv run $S/run_web.py run    --adapter adapter.py --cases <dir>/cases.json --account acme            # validate only
uv run $S/run_web.py run    --adapter adapter.py --cases <dir>/cases.json --account acme --ids R4 --submit
uv run $S/run_web.py report --adapter adapter.py --cases <dir>/cases.json      # rebuild results/report.xlsx
```

Per case three checks must agree: **file** (preflight = expect, else the file is wrong, not the
web) → **web** (the real validate response *body* — Playwright sees bodies, a browser extension
does not) → **db** (only with `--submit` and `mode: submit`: refuse if the receipt already exists,
else confirm, read the submit body, check header / detail count / totals / partner rows).

Output: `<dir>/results/<stamp>-<account>.{md,json}` + every raw response body + a screenshot per
case, and **`results/report.xlsx`** rebuilt from *all* runs in that folder, self-contained
(screenshots embedded, links in-workbook only — check: unzip the copy, `xl/media/*.png` count =
cases run, zero `TargetMode="External"`). Hand that file to the team, not the `.md`.

Rules the script keeps — do not weaken them:
- **The agent never signs in.** `login` opens a headed browser and waits for a person; the session
  is saved at `~/.cache/qa-excel-import/<host>/<account>.json` (chmod 600, outside the repo).
- **The session's tenant is checked** against the cases' company before any upload.
- **Synthetic cases are never submitted** — only `mode: submit` cases, only with `--submit`, and
  only after the owner's go-ahead for that batch.
- The adapter's `connect()` must refuse a production database.

## 5. Verify in the database

For each submitted R*: header by its natural key, then count details, transactions and partners
against the expected column; check the per-detail lookups and dates. If the document is not found,
the portal may write to another instance than the one you query — move the check to the portal's
own read API rather than calling it a failure.

## 6. Report

Findings first: a dropdown value that can never pass, a pair the dropdown is missing, a
preflight/web mismatch, a real-data field the template cannot carry.

**Exit criteria — the run is done when all hold:** every valid pair has exactly one row with a
verdict and every dead value a negative row · no case reads "not run yet" in `report.xlsx` › Summary ·
preflight = web for every case, or the mismatch is a written defect · every submitted R* is found in
the DB with the expected counts · the zero-coverage list is empty or each gap is accepted by the owner.

**One defect per finding**, strings and numbers preserved exactly; if something was not measured,
say so:

```
[Excel import · validate] form type X never passes for any tax right
Severity: Major   Case: N1   Env: <portal> · build <sha> · tenant <id>
Steps:    upload N1_OUT_invalid-pairs.xlsx → Validate
Expected: (from cases.json) VALIDATION_ERROR · "does not match"
Actual:   verbatim error lines from the validate body
Evidence: report.xlsx › sheet N1 (screenshot) · results/<stamp>-N1-validate.json
```

Severity by what the miss does to data: **Critical** — a dead pair is accepted or a document lands
on the wrong tenant / right · **Major** — a valid pair or a dropdown value can never pass (operators
blocked) · **Minor** — rejected correctly but the message points at the wrong row or column ·
**Trivial** — label / wording.
