---
name: blueprint-write-report
description: "Report what was written, what was checked, and what could not be."
---

# Report

Write `.blueprint/write-report.md` for the person, in their language and in plain words:

- `## 書いたもの` / `## What was written` — every part's file, in reading order, with one line on what it
  covers. The check looks for each file's path.
- `## 確かめたこと` / `## What was checked` — every part raises no chaff finding under the style; how many
  quotations were checked against their sources; every key point of the brief is covered, and where.
- `## 確かめきれなかったこと` / `## Not checked` — facts stated without a source; open questions from the
  brief that are still open; anything in `STYLE.md` you were unsure how to apply; every finding set aside
  (`dismissed`), **one line each**, giving the part, the rule, the line number and its `why` quoted word for
  word, and whether chaff misread the text or fixing it would have changed a quotation (the check looks for a
  line per dismissal with its rule, line number and `why`).

## Drafts for chaff

First run `node <usecase pack>/checks/feedback.mjs` (with `BLUEPRINT_BASE` and `BLUEPRINT_USECASE` set). It
drafts one report to chaff for each finding set aside because chaff misread the text (`"because": "wrong"`),
with `chaff feedback`, which sends nothing and puts only a few lines of the document in each draft. The drafts
are `.blueprint/chaff-feedback/<id>.md`; `index.json` beside them lists them.

- When `index.json` says `"supported": true` and there are drafts, add `## chaff への報告の下書き` /
  `## Drafts for chaff`. Name each draft file, say in one line what chaff misread, and say that **nothing was
  sent**. The person may read a draft, remove anything they do not want to share, and file it at
  https://github.com/isamu/lab/issues/new, or not at all. Do not send one yourself.
- When it says `"supported": false`, mention in one line under `## 確かめきれなかったこと` / `## Not checked`
  that the chaff in use cannot draft reports.
- When nothing was set aside because chaff misread it, leave the section out.

Then tell the person where the document is.
