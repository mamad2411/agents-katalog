---
name: revision
description: Write the revision notes for a resubmission, a document that says what changed between the previous version (an uploaded PDF) and the current LaTeX sources. Output is Markdown or a LaTeX-built PDF.
disable-model-invocation: true
argument-hint: "[path to the previous version's PDF]"
---

This skill is ARR-only. When `paper.config.json` has `venue` `semeval`, say that SemEval has no ARR resubmission and stop.

Explain to reviewers and editors what changed since the previous version. The previous version is a PDF, the current one the LaTeX sources; a script aligns the two, you judge what the differences mean, and the authors settle what stays unclear. The notes state only changes the comparison shows.

`PK` means `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/paperkit.py`, run from the project root.

## 1. Reviews

Ask first, with AskUserQuestion, whether reviews exist for the previous version.

- `reviews/` exists: use its files and ask whether they are complete.
- Otherwise offer: paste them now (write `reviews/R1.md`, `R2.md`, ..., `meta.md`), they live elsewhere (ask for the path), or there are none. With none, the notes follow the paper's sections.

## 2. Previous version

The argument, or a path you ask for, names the previous version's PDF. Without one, stop here.

```
PK revision-prepare <pdf>
```

It stores `revision/previous.pdf` and its text `revision/previous.txt`. On ⚠️ report it and stop.

## 3. Rules and format

- `PK guidelines revision` fetches the ARR author guide. On ⚠️ say which rules are missing. When you report to the user which rules apply, name them with their section heading and the guide's URL as `PK guidelines` prints it; the notes themselves carry none. Read the parts on resubmission and revision notes in full: what the notes must contain, where they are submitted, length limits. A limit the user gives wins.
- Ask with AskUserQuestion: Markdown (`revision/revision.md`, recommended) or LaTeX (`revision/revision.tex`, built to `revision.pdf`). Ask again on every run.
- LaTeX: run `PK latex-check`. On ⚠️ show what is missing and the install hint it prints, then ask: write only the `.tex` without building (recommended, it compiles in Overleaf), switch to Markdown, or stop so the user can install LaTeX first. Copy `${CLAUDE_PLUGIN_ROOT}/templates/revision.tex` to `revision/revision.tex`; its header comment lists the macros. Fill in the title lines and body, leave the layout alone.

## 4. Compare

```
PK revision-diff
```

It prints, per section of the current sources, the paragraphs that are `changed`, `minor`, `new`, `moved` and passages that were `removed`, with file and line. Wording is lowercase tokens. Unchanged paragraphs are only counted. The reference list, math, citations and figure images are not compared.

Settle every item by reading the `.tex` at the given line:

- `minor`: wording without effect. Summarize together as small wording changes.
- `changed`, `new`: describe what the paragraph now says and what it said before.
- `moved`, `removed`: say where it went, or that it is gone.
- Flagged `numbers differ`, or `table/figure`: the paragraph is unclear until the old and the new values sit side by side. Render the old page, `pdftoppm -png -r 80 -f N -l N revision/previous.pdf <scratchpad>/old`, find the page by the section's words in `previous.txt`, and read the image. Look at the current `.tex` of the table.

Collect everything you still cannot call (a value you cannot read, a removed passage that may be an extraction artifact, a change whose reason only the authors know, a change in a figure image) and ask about all of it in one AskUserQuestion round. Show old and new side by side for each item. Reasons for changes come from the reviews or from the authors; supply none yourself.

## 5. Write

Write the notes in the chosen format: a short summary, an overview of changes per section, then per section each change as added, changed, removed or moved with where it is (section, line). With reviews, name for each review point the change that answers it (`\revpoint` in LaTeX) and say which points no change answers. Follow the `writing` skill. Check the length against the fetched limit and report the count.

LaTeX: build with `latexmk -pdf -interaction=nonstopmode -output-directory=revision revision/revision.tex`, fix errors, and report the page count.

## 6. Follow-up

- Changes promised in `rebuttal.md` or `report.md` (category `Review`) that the comparison does not show: list them to the user as open. Never write them up as done.
- Add the open ones to `report.md` (category `Review`, 🔴).
