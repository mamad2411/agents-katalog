---
name: draft-document
description: Create or revise a presentation or written document for a project deliverable. Routes to one branch and runs only that one.
disable-model-invocation: true
---

# familiar — Draft a Document

A **menu, not a procedure**. It names the output formats familiar can build (decks, documents, workbooks), plus review of a team-owned Word file, and hands
off to exactly one of them. It reads no project state itself and writes nothing.

## Context contract

- **Required context:** this menu only
- **Conditional context:** exactly one file under `references/`, only when step 1 selects that branch. The selected branch's own context contract governs from that point; nothing else in `references/` is opened.
- **Excluded context:** `5-System/Memory/`, `4-Trackers/`, `Knowledge`, `Inputs`, other projects, and undeclared extension content — the menu itself opens no project content.
- **Updates:** `nothing`. Every write belongs to the selected branch and is declared in that branch's own contract
- **Capabilities:** file-read. Optional capabilities must degrade as the procedure states.
- **Completion:** One branch is selected, its reference file is loaded, and its procedure runs under its own contract — or the user is told no branch fits and nothing is opened.

## Step 1 — Select the branch

If the user already named a format ("build me a deck", "draft the memo as a Word doc"), skip the
question and go straight to it. Otherwise ask which:

| Branch | Reference | What it does |
|---|---|---|
| **Deck** | `references/deck.md` | A presentation for a project start, status update, recommendation, or review — built and visually validated with `scripts/build_pptx.py`. |
| **Document** | `references/document.md` | A written deliverable — memo, report, or Word file — built and validated with `scripts/build_docx.py` when the format is `.docx`, or written directly for Markdown/plain text. |
| **Review** | `references/review.md` | An existing team-owned Word file, edited in review passes as tracked changes and comment replies by "AI Review", never rebuilt — via `scripts/tracked_edit.py`. |
| **Workbook** | `references/workbook.md` | An Excel deliverable — tracker, screening or extraction tool, register, summary — planned sheet by sheet, built readable, and checked with `scripts/xlsx_check.py` so nothing its source had is lost. |

If the request matches none of them, say so and stop. Do not pick the nearest branch, and do not open a
reference file to find out whether it fits — the table above is the whole basis for the match.

## Step 2 — Run the selected branch

Load that one reference file. From there its own **Context contract** governs — its Required,
Conditional, Excluded, Updates, Capabilities, and Completion declarations replace this file's, which
covered only the menu. Do not load a second branch.

## Guardrails

- **Every branch here is user-started.** This skill carries `disable-model-invocation: true`, so a
  route match never opens it and never opens anything under `references/` — `routes.md` Resolution
  rule 3 applies to the menu, which is what keeps it applying to every branch. Identify the branch
  that fits, tell the user the command, and stop.
- The menu never performs a branch's work itself, never partially applies one, and never substitutes
  a lighter action because a branch looked heavy.
- Nothing under `references/` is a skill. Each is a procedure this menu selects; none is separately
  invocable, and none may be opened without a selection in step 1.
