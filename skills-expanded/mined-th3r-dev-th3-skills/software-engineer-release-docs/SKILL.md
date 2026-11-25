---
name: software-engineer-release-docs
description: >-
  The release report: one PDF that tells the PM, the BA and QA what goes up in release vX.Y.Z, what each
  change looks like before and after, which questions the BA still has to answer, and the test plan QA
  runs on staging. Written from a fixed template (Thai or English), checked by `check_report.py`, rendered
  through documentation's doc-style builder with a release layout (cover, one page per section, before/after
  screenshot tables). Use WHENEVER the work is "the release report", "release document", "release docs for
  the PM", "สรุปรายการที่จะขึ้น release เป็นเอกสาร", "เอกสาร release", "แผนเทส release", "what's in vX.Y.Z as a
  PDF", "test plan for the release", or a release scope (devops-release-scope's scope.md) has to become a
  document other people read.
---

# software-engineer-release-docs

The facts come from `devops-release-scope` (`scope.md`: what is new against prod, what is half shipped,
what is pending) and from the tickets and retest results. This skill turns them into the document.

```bash
S=skills/software-engineer/release-docs
D=skills/documentation/doc-style
cp $S/references/template-th.md work/release/v1.4.0/release-v1.4.0.md      # or template-en.md; fill it in
mkdir -p work/release/v1.4.0/img                                           # copies of the screenshots
python3 $S/scripts/check_report.py work/release/v1.4.0/release-v1.4.0.md   # fix every finding first
uv run $D/scripts/build_doc.py work/release/v1.4.0/release-v1.4.0.md --no-date --formats pdf \
  --css $S/assets/release.css                                              # -> release-v1.4.0.pdf beside it
```

`build_doc.py` needs pandoc on PATH and Chromium for Playwright once. Its theme gives the tables their look
(black borders, a grey header repeated on every page, rows that never split, an empty header row = a
key/value table). `release.css` adds the cover, a new page per `#` section, and screenshots capped at 34 mm
high so two ticket blocks fit on a page. Set column widths with the dash counts in each separator line.

## The pages

1. **Overview**: one paragraph with the verdict (ready for which environment, how many user-visible changes,
   how many BA questions), what prod runs today, then four tables: in this release, waiting on a merge or
   partly shipped, not in this release, and **tell the customer**.
2. **BA Decision**: only open choices that a ticket or a retest result already states, with what each blocks.
   Anything already answered in meeting notes, a ticket comment or a retest stays out. Never invent options.
3. **Change details**: heading only, then one `## N. KEY-xxx` block per ticket: a key/value table (empty
   header row `| | |`: ticket, PR with its author, owner, status, what changes, test cases), then a
   `before | after` table with one screenshot each.
4. **The user group being rolled out** (optional): its items in this release, the ones that are not, and the
   go-live date.
5. **Test plan**: a key/value header (environment and version, platform, blank test date, accounts and roles,
   test documents, evidence, how a ticket is closed), then case tables `TC | Ticket | Test Case | Expected
   Result | Actual Result | Status` in groups: full cases (tickets in Testing), re-checks (tickets waiting for
   deploy), cases waiting on a merge, and not tested this round.

The cover title is only `Release vX.Y.Z`. No appendix, no investigation, no commit list: commits, migrations
and rollback belong in the change record (`devops-change`).

## Rules

- **Written for PM, BA and QA, not developers.** Say what the user sees change. Leave out spec file names,
  unit test counts, guards, query wording and PR-to-branch routing.
- **Every number comes from a ticket or a retest.** Never invent one, and read the retest verdicts before
  writing a status: "passed 4 of 5 cases" is not "still broken".
- **Screenshots are evidence.** Take the after shot and its caption from the retest result, the before shot
  from the ticket's attachments or the failing run; copy each to `img/<KEY>-before.png` / `-after.png`.
  Never write "no screenshot yet". With only an after shot, use a two-column `after | what it shows` table
  and add an "original symptom" (or "original request") row from the ticket text. With no shot at all, drop
  the picture table and show other evidence under `Evidence:`: rows of a file the system produced, a timing
  measured in the PR, a test result.
- **Expected Results are checkable**: a number, a count, the text on screen, or a timing with a reference value.
  Never "same as before" alone. If a case compares with the state before deploy, the Test Case says what to
  record first. Actual Result and Status stay blank for QA.
- **Test data names accounts and roles only.** No passwords, and not where they are kept.
- **Partly shipped items are never promised.** A ticket whose fix is in one repo of the release and not the
  other goes under "waiting on a merge or partly shipped" and in "tell the customer" as not fixed yet.
- **Deploy blockers do not go in the report.** What is not merged, what fails and who unblocks it go to the
  release owner in conversation, each with a proposal.
- Thai prose goes through a Thai-writing skill such as `kien-thai` if one is installed; keep technical terms
  practitioners say in English (`deploy`, `release`, `ticket`, `branch`).
- **Never hand-edit the PDF.** Fix the Markdown and rebuild.

## Check before handing over

`check_report.py` must print `ok`: front matter titled `Release v<version>`, the four fixed pages, no
template text left (`<...>`, `vX.Y.Z`, `DD/MM/YYYY`, `#NN`), no "no screenshot yet", every image present,
Expected Results checkable, QA columns blank, no password. Then look at the PDF: the cover alone on page 1,
every section on a new page, no table heading orphaned at the bottom of a page, screenshots readable.
