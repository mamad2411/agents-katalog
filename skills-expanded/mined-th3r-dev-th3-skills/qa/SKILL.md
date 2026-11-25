---
name: qa
description: >-
  QA toolkit for web portals, built from a Thai-government integration project and generalised:
  (1) answer-review — review the prepared answers in a meeting Q&A sheet through four lenses
  (business · program · data · operation) and write one Remark per row; (2) export-evidence —
  walk every export button (CSV / Excel / PDF / Print) on a signed-in Chrome, verify the files,
  and build the team's .xlsx evidence report; (3) excel-import — design, preflight, run and
  verify a test set for an Excel-template import (validate → submit → database); (4)
  ticket-report — post a QA / retest result on a Jira ticket in the team format with screenshots
  inline. Use WHENEVER the work is test evidence, a QA report, test case design for an import,
  a pre-meeting answer review, "ทดสอบ", "หลักฐานการทดสอบ", "test report", "ลงผลเทสในตั๋ว", or
  "review the Q&A before the meeting". Read the sub-skill's SKILL.md before acting.
---

# qa — sub-skills

| When the work is… | Read | Scripts |
|---|---|---|
| "are these prepared answers safe to say in the meeting", "review the Q&A tab", "ลง remark ให้ Q&A" | [`answer-review/SKILL.md`](answer-review/SKILL.md) + one lens per agent under [`answer-review/lenses/`](answer-review/lenses/) | `answer-review/scripts/qa.py` (`pull` · `merge` · `selfcheck`) |
| "test the Export Excel/PDF/CSV buttons", "QA evidence workbook", "ทดสอบปุ่ม Export" | [`export-evidence/SKILL.md`](export-evidence/SKILL.md) | `export-evidence/scripts/collect_export.py` (CDP walk) · `make_qa_report.py` (xlsx) |
| "test the xlsx import", "test cases for the import template", "are all dropdown values usable" | [`excel-import/SKILL.md`](excel-import/SKILL.md) + [`references/test-design.md`](excel-import/references/test-design.md) | `excel-import/scripts/run_web.py` (login · run · report) with a project `adapter.py` (contract: `adapter_example.py`) |
| "post the test result on PROJ-123", "retest done, log it on Jira", "รายงานผลเทสลงตั๋ว" | [`ticket-report/SKILL.md`](ticket-report/SKILL.md) + [`references/format.md`](ticket-report/references/format.md) | `ticket-report/scripts/ticket_report.py` (`draft` · `post` · `--selftest`) |

They chain: `export-evidence` and a page-timing run produce the evidence folder that
`ticket-report` drafts from (`steps.csv` / `results.json` → one case); `excel-import`'s
`report.xlsx` and screenshots become a ticket's `cases.json` evidence.

## Rules every sub-skill keeps

- **A person signs in; the agent never types a password into a login form.** Sessions are
  reused from a signed-in CDP Chrome or a saved Playwright storage state outside the repo.
- **Read-only on production.** Click only filters, query buttons, export buttons and queue
  downloads; never save, submit, confirm or delete on prod. Synthetic import files are
  validated, never submitted.
- **Evidence over claims.** Every PASS carries a screenshot and a parsed file or a response
  body; every FAIL carries the cause (`run.json` → `net`, the validate body, the DB row). An
  empty table is not a pass without a row count on screen.
- **Draft, show, then post.** Nothing lands on a ticket or a shared sheet before the owner has
  read the draft (`ticket-report.md`, `plan.json`).
- **Secrets stay out of the repo and out of the output.** Account files live under `~/.config`
  or a gitignored folder; the one exception (dev/uat Test Data on a ticket) is explicit and
  cannot be switched on for master/prd.
- **Scripts run with `uv run <script>`** (PEP 723 inline dependencies) from the repo root;
  Playwright needs an installed Chrome (`channel="chrome"`) or `playwright install chromium`.

## Tests

```bash
cd skills/qa && python -m pytest -q     # needs: pytest openpyxl pillow
```
