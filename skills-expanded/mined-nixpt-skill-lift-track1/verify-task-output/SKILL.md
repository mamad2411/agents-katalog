---
name: verify-task-output
description: |
  Pre-submission and pre-finish verification for benchmark-style agent tasks.
  Use when you are about to claim success, write final artifacts, or stop: check
  that outputs match the instruction's required files, formats, schemas, and
  acceptance criteria. Also use after multi-step pipelines to catch silent
  partial completion. Not for temporary mid-exploration files, and never a
  reason to inspect grader/verifier internals — verify only against the
  instruction and your own workspace.
---

# verify-task-output

Load `safe-agent-scope` if you have not already — verification never licenses reading grader/harness paths or widening sharing.

Many agent failures are "almost done": wrong filename, wrong schema, empty
file, or a plot saved where a CSV was required. Verifiers are deterministic;
align to the instruction's stated end state before you exit.

## Why this exists

Paired skill evals reward procedures that finish cleanly. A strong intermediate
analysis that never writes the required artifact scores zero. This skill is a
short checklist, not a second solution method.

## Procedure

1. **Re-read the instruction's deliverables** — filenames, formats, columns,
   exit codes, plots vs tables, "overwrite in place" vs new path. Make an
   explicit checklist; do not stop until every item is checked off.
2. **Inventory the workspace** — confirm each required path exists and is
   non-empty (`wc -c`, `head`, schema check). The TASK workspace only —
   grader, harness, and verifier paths are off-limits even "to check".
3. **Schema / shape checks**
   - CSV/TSV: header names, dtypes sanity, row count > 0
   - JSON: required keys present; valid parse
   - Code: entrypoint runs (`python -m py_compile` or a quick smoke)
   - Images/PDF/DOCX: file opens; not a zero-byte stub
4. **Template / placeholder sweep** — if the task used a template (Word,
   HTML, mail merge, `{{TOKEN}}`, `${VAR}`, `__PLACEHOLDER__`), search the
   final artifact for leftover tokens and fill or remove them before exit.
   For `.docx`, unzip and search the **concatenated** `w:t` text (and
   headers/footers), not each run alone — Word splits tokens across runs.
   Also confirm every key from the provided data file appears in the output
   when the task is a fill/merge. "Mostly filled" is a fail when any
   placeholder remains.
5. **Semantic spot-check** — one or two rows / one assertion against a known
   example from the instruction (not against hidden tests).
6. **Run only task-provided checks** — if the workspace ships a script or
   unit tests the instruction says to run, run those. Never invent access to
   hidden graders to "confirm the format".
7. **Idempotence** — if you re-run, do you clobber a good artifact? Prefer
   write-then-replace atomically.
8. **Only then** stop or submit.

## When not to use

- Mid-exploration dumps that are explicitly temporary
- Tasks that only ask for an interactive diagnosis with no artifact

## Anti-patterns

- Trusting a library "success" print without checking the output file
- Writing `results.csv` when the instruction demanded `submission.csv`
- Leaving NaNs / #REF! / empty sheets / unreplaced `{{TOKENS}}` in finals
- Claiming done after fixing 90% of placeholders
