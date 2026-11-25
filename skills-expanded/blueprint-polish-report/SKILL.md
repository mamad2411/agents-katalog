---
name: blueprint-polish-report
description: "Report what was polished, what was checked, and what was left as it was."
---

# Report

Write `.blueprint/polish-report.md` for the person, in their language and in plain words:

- `## 整えたもの` / `## What was polished` — every polished file, with how many findings it had before and
  after, and one line on the kind of change. The check looks for each file's path. When the list was empty,
  say that nothing needed polishing and which documents were measured.
- `## 確かめたこと` / `## What was checked` — for every polished file, the headings, the structure's
  addresses, code blocks and link targets are unchanged, and chaff reports nothing under the style — naming
  the kind of document it was measured as when the answer `kind` gave one (as the person chose it, e.g.
  「報告書」). The
  originals are in `.blueprint/originals/`; in a git repository, `git diff` shows every change.
- `## 直さずに残したもの` / `## Left as it was` — skipped files and why; every finding set aside
  (`dismissed`), **one line each**, giving the file, the rule, the line number and its `why` quoted word for
  word, and whether chaff misread the text or fixing it would have changed the meaning (the check looks for a
  line per dismissal with its rule, line number and `why`); files over the agreed number, for another
  run.

When the answer `shelved` asked for the shelved findings too, say under `## 整えたもの` / `## What was polished`
that the counts include them. Their entries stay in `.chaff-baseline.json`; a fixed sentence no longer matches one,
so there is nothing to clean up.

With the folder's style, the style is its `chaff.yaml`. `STYLE.md` belongs to the answer `scope` only, so when
`scope` did not ask for the guide, a folder without `STYLE.md` lacks nothing: do not mention it.

When `.blueprint/viewpoints.json` records a `writer` verdict for a polished file, add
`## 書いた人に確かめてほしいこと` / `## For the writer` **right after** `## 整えたもの` / `## What was polished` — it is
the part the person has to act on, so it comes before what was checked and what was left: one item per verdict, giving the file, what was read
for (the viewpoint's `title` in `<usecase pack>/viewpoints.json`), the `quote` word for word, and the `note` as
the question. The check looks for every quotation. Under `## 整えたもの` / `## What was polished`, name the
viewpoints you fixed in the same way as the other changes.

## Drafts for chaff

First run `node <usecase pack>/checks/feedback.mjs` (with `BLUEPRINT_BASE` and `BLUEPRINT_USECASE` set). It
drafts one report to chaff for each finding set aside because chaff misread the text (`"because": "wrong"`),
with `chaff feedback`, which sends nothing and puts only a few lines of the document in each draft. The drafts
are `.blueprint/chaff-feedback/<id>.md`; `index.json` beside them lists them.

- When `index.json` says `"supported": true` and there are drafts, add `## chaff への報告の下書き` /
  `## Drafts for chaff`. Name each draft file, say in one line what chaff misread, and say that **nothing was
  sent**. The person may read a draft, remove anything they do not want to share, and file it at
  https://github.com/isamu/lab/issues/new, or not at all. Do not send one yourself.
- When it says `"supported": false`, mention in one line under `## 直さずに残したもの` / `## Left as it was`
  that the chaff in use cannot draft reports.
- When nothing was set aside because chaff misread it, leave the section out.
