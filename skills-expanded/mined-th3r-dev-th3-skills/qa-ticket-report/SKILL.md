---
name: qa-ticket-report
description: >-
  Post a QA test or retest result onto a Jira ticket in the team format. The header block is
  Test Result / Test Environment (<env> - Version <actual>) / Platform / Test Date / Test Data /
  Actual Result. A ticket with more than one case gets a `Test Case | Actual Result | Expected
  Result` table. Under that the comment explains what happened, with the screenshots inline in
  the comment, not as an attachment list. Use WHENEVER the work is "post the test result on the
  ticket", "test report for PROJ-123", "Test Result: PASSED/FAILED", "retest done, log it on
  Jira", "รายงานผลเทสลงตั๋ว", "QA report standard", or after a qa/export-evidence or page-timing
  run whose result belongs on a ticket. Draft first, post only after the owner says OK.
---

# QA result comment on a ticket

```bash
S=skills/qa/ticket-report/scripts
uv run $S/ticket_report.py draft <evidence dir> --ticket PROJ-123 --env dev|uat|master|prd \
    --platform "Web (admin app)" --account "<section of ~/.config/qa-ticket-report/accounts.ini>" \
    --release vX.Y.Z --actual "<1-2 sentences>" [--lang th|en]
# show <dir>/ticket-report.md to the owner · on OK:
export JIRA_BASE_URL=https://<site>.atlassian.net JIRA_EMAIL=<you> JIRA_API_TOKEN=<token>
uv run $S/ticket_report.py post <evidence dir> --ticket PROJ-123 [--update <comment id>]
uv run $S/ticket_report.py --selftest
```

`accounts.ini` holds `[Section]` → `UserName` / `Password` and lives **outside** any repo.
`--test-data "<text>"` prints a value as-is instead.

## The format

`references/format.md` holds the template, a filled `cases.json`, and the shapes that come up.

- **The six header labels stay in English, exactly as written.** The body follows the team's
  language (`--lang th` by default, Thai per the `kien-thai` rules; `--lang en`). **No emoji anywhere.**
- **Colour rule:** every result word is **bold and coloured**, in the header and in each table row:

  | Result | Colour | When |
  |---|---|---|
  | `PASSED` | green `#00875A` | the case did what Expected says |
  | `FAILED` | red `#DE350B` | it ran and did something else |
  | `BLOCKED` | orange `#FF8B00` | it could not run (env down, no data, no access) |
  | `NOT TESTED` | grey `#6B778C` | in scope but not run this round |

  Test Result takes the worst result among the judged cases, in the order FAILED > BLOCKED >
  NOT TESTED > PASSED. In wiki markup that is `{color:#00875A}*PASSED*{color}`.
- **Test Environment = `<Dev|UAT|Master|PRD> - Version <actual>`.** "Actual" means what the tested
  app reports about itself: `results.json` `version` if present, else a read-only GET of the login
  page matched with `--version-regex`. Pre-release builds report a sha, so pass `--release` and
  the header becomes `v1.2.22 (master-6ca0cf2)`. If the app says `v1.2.21` and `--release` says
  something else, the draft stops. No version at all stops it too.
- **Test Data.** On `dev`/`uat` it shows the username and the password. On `master`/`prd` the
  username only, and no flag overrides that. This is the one place a test password is printed;
  the drafts live in a gitignored work folder, and a leak check runs before any push.
- **More than one case = table.** Write `<dir>/cases.json` from the ticket's acceptance criteria.
  `evidence` paths are relative to `<dir>` (`../` is fine); every file has to exist.
  `baseline: true` marks a before-the-fix run kept for comparison: shown, not judged.
  With no `cases.json`, one case is built from `results.json` (page timing: every run 2xx within
  `--max-seconds` and the same row order) or from `steps.csv` (qa/export-evidence).
- **Write each case so a non-developer can read it in 30 seconds.** Use the structured fields:

  | field | what goes in | rule |
  |---|---|---|
  | `case` | what is tested, in plain words | no codes, ids or field names |
  | `expected` / `actual` | one sentence each | `actual` opens with the outcome |
  | `steps` | list, one action per item | what a tester clicks or enters, in order |
  | `why` | only when not PASSED; 1–2 short sentences | the cause in user terms |
  | `data` | list of `name: value` | document number, product, account, quantity |
  | `tech` | list, for the dev team | code paths, commit, API, table/column, ids |

  Never put code paths, API names, commit hashes or column names in `case` / `expected` /
  `actual` / `steps` / `why`: they go in `tech`. One fact per sentence, no sentence over ~25 words.
- **Images go inline**, each under its case with a one-line caption. Non-image files are listed
  under "attached files".
- **Actual Result** under the header is one or two sentences with the numbers. Left out, the draft
  puts `TODO` there and `post` refuses to send.

## How post works

1. Uploads every evidence file as `qa-<env>-<stamp>-c<case>-<name>`; a name already attached is
   skipped, so a rerun is safe. Jira stores inline images as issue attachments.
2. Sends `POST /rest/api/2/issue/{key}/comment` with a wiki-markup body (`!name|width=700!` for
   images, `||Test Case||…||` for the table). A markdown comment cannot embed images, which is
   why this goes through REST v2.
3. Reads the comment back (`expand=renderedBody`) and prints `inline images N/M`. N < M means an
   image name did not match — check the upload names.

## Traps

- **Every attachment must be previewable in Jira.** Jira previews images, PDF, video and
  `text/plain`; `application/octet-stream` or `application/json` only downloads. `preview_mime()`
  sends `.md .json .csv .log .txt .sql .tsv` as `text/plain`. Never hard-code a MIME type.
- **Draft and post are separate steps on purpose.** Nothing reaches Jira before the owner reads
  `ticket-report.md`.
- **A redraft keeps the upload names**, so a re-post skips files already on Jira. To fix a posted
  comment in place use `--update <comment id>` rather than posting a second one.
- **A gateway 504 at exactly 60 s is the ingress cutting the request, not the API answering 504.**
  Write it that way in `actual`.
