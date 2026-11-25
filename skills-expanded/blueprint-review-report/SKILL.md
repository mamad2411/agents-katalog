---
name: blueprint-review-report
description: "Report what was found, what was checked, and what could not be checked."
---

# Report

Write `.blueprint/review-report.md` for the person, in their language and in plain words:

- `## 見つけたこと` / `## Findings` — every finding by its `id`, most severe first: what is wrong, where
  (named as the document does: 第4条第2項, Section 3.2(a), or a section's heading in 「」, "…" in an English report — not chaff's
  index such as `4.2` or `h1.3`), and the proposal when there is one. The check looks for each `id`.
- `## 確かめたこと` / `## What was checked` — every quotation was found in the document by `chaff cite`;
  every structure problem chaff reported was addressed or dismissed with a reason; the originals are
  unchanged; with proposals, each corrected copy's name and that it has no more structure problems than the
  original.
- `## 確かめきれなかったこと` / `## Not checked` — what a machine cannot confirm: that the reading is
  complete, that a proposal is what the parties mean, anything that depends on law or documents outside
  these files. Recommend a professional's review where the stakes call for it.

## Drafts for chaff

First run `node <usecase pack>/checks/feedback.mjs` (with `BLUEPRINT_BASE` and `BLUEPRINT_USECASE` set). It
drafts one report to chaff for each structure problem chaff got wrong (one you dismissed) and each one it
missed (a structure finding you made that chaff did not report). It uses `chaff feedback`, which sends
nothing and puts only a few lines of the document in each draft. The drafts are
`.blueprint/chaff-feedback/<id>.md`; `index.json` beside them lists them.

- When `index.json` says `"supported": true` and there are drafts, add `## chaff への報告の下書き` /
  `## Drafts for chaff`. Name each draft file, say in one line what chaff got wrong or missed, and say that
  **nothing was sent**. The person may read a draft, remove anything they do not want to share, and file it
  at https://github.com/isamu/lab/issues/new, or not at all. Do not send one yourself.
- When it says `"supported": false`, the chaff in use cannot draft reports yet. Mention in one line under
  `## 確かめきれなかったこと` / `## Not checked` how many cases there were, and leave it at that.
- When there were no cases, leave the section out.
