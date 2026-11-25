---
name: rebuttal
description: Plan and draft the ARR author response from the reviews in reviews/, following the current ARR author guidelines. Writes rebuttal.md.
disable-model-invocation: true
argument-hint: "[word or character limit, if known]"
---

This skill is ARR-only. When `paper.config.json` has `venue` `semeval`, say that SemEval has no ARR response process and stop.

Help the authors answer their reviews. The authors decide what to concede, what to argue and what to promise; this skill organizes the reviews, checks each point against the paper and drafts the answers.

`PK` means `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/paperkit.py`, run from the project root.

## 1. Inputs

- Reviews and meta-review: one file per review in `reviews/` (`R1.md`, `R2.md`, ..., `meta.md`), pasted from OpenReview. No folder yet: create it and ask the user to paste the reviews.
- Rules: run `PK guidelines rebuttal`. It fetches the ARR author guide (the section on responding to reviews, and on reporting review issues) and the reviewer guidelines. On ⚠️ say which rules are missing. Read the response section in full: length limits, what may and may not go in a response, how the process works this cycle. A limit the user gives in the argument wins.
- Context: ask with AskUserQuestion what the files do not show: the response deadline and format (OpenReview comment per reviewer, general response, character limit), whether new experiments can still be run, and whether this is a resubmission (then also the previous reviews and how they were addressed).

## 2. Triage

Split every review into atomic points. For each point record: reviewer, quote, type (misunderstanding, missing experiment, missing related work, clarity, presentation, factual error by the reviewer, question), and what the paper actually says (section, line, quote).

Check each point against the paper and, for related work, against the papers themselves (`literature` skill; fetch with the source skills when the reviewer names a paper). Mark points that the reviewer guidelines treat as unhelpful (e.g. "not novel" without a reference, demanding comparisons to work after the deadline) and point the user to the issue-reporting route the fetched guide describes. Name each such point with the issue code the fetched guide uses (e.g. `H9`) and the guide's URL as `PK guidelines` prints it, so the report to ARR can be pasted as is. The answers to the reviewers in `rebuttal.md` carry no such references.

Show the triage to the user as a table. Then ask with AskUserQuestion, point by point for the important ones: concede, argue, or answer with new results, and which new results exist. Wait for the answers.

## 3. Draft

Write `rebuttal.md`: per reviewer, the points in order of importance, each with a short quote of the point and a direct answer. Answers cite sections, tables and line numbers of the paper, report only numbers the authors gave you, and promise only the changes the authors agreed to. Polite, specific, no thanks paragraphs beyond one line. Follow the `writing` skill.

Add a general response for points several reviewers share, if the fetched rules allow one. Check the length against the limit and report the count.

## 4. Follow-up

List the promised changes as items in `report.md` (category `Review`, 🔴), so the camera-ready or resubmission version keeps the promises.
