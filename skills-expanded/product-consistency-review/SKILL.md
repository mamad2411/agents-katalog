---
name: product-consistency-review
description: "Use when code, UI and docs may disagree. Audit read-only."
version: 1.1.0
author: coder role of hermes-fleet-apps
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [review, audit, consistency, ux, docs, read-only]
---

# Product consistency review

The job: find every rule the product decides for the user in two different ways. A
rule can drift between two code paths, between the CLI and the window, between the
window's text and the behaviour, or between a doc and the code. The audit is
read-only. The deliverable is one private findings file plus a short chat report.
Assume the owner is not a developer: write every finding in plain words, framed as
"how would the owner notice this in the window".

## When to Use

- A brief asks you to find "rule drifts" or "inconsistent product rules", or to
  cross-read code, UI and docs.
- A bug turned out to be two surfaces disagreeing, and the rest of that kind must
  be found.
- A gated fix plan follows such a review (see Follow-on fixes).

## Procedure

1. **Read the brief, then the repo's AGENTS.md, then the latest fixes log.** The
   fixes it describes are the model for what a finding looks like.
2. **Load once, grep many.** In one persistent execute_code kernel, read every
   tracked text file (`git -C <repo> ls-files`; skip tests/ and binary assets) into
   a dict of path -> lines. Define `grep(pattern, files)` and `show(path, a, b)`.
   This means no repo writes and no repeated reads. The kernel can be fresh after a
   compaction, so check the helpers exist before calling them, and rebuild them
   if not.
3. **Hunt per axis, not per file.** Read the core rule modules (config, matcher) in
   full, then grep each rule across every surface:
   - every limit or threshold constant: who uses it, and where its number is
     hand-typed in UI or docs instead
   - the same action through each door (CLI, window, browser page): the same gate,
     the same plan-is-stale guard, the same undo?
   - UI and help text compared with what the code really does ("clearest", "best N")
   - one word used for two outcomes, or two words for one outcome
   - parallel input paths compared with each other (e.g. two media types)
   - undo coverage of every write door
   - empty and first-run states, and CLI error text that leaks into a GUI
     (terminal commands shown to a window user)
   - dead names left in docstrings, CSS, tests and docs after a rule changed
   - documented flags that the code refuses
4. **Re-show every cite right before writing.** Tool outputs are demoted at context
   compaction, so remembered file:line numbers are unreliable. Re-run `show()` on
   both sides of each key finding just before the file is written.
5. **Write the findings file** (private tree, e.g. `_private/review-<date>.md`).
   One entry per finding:
   - a plain-words title
   - Where: file:line for each side
   - what each side does
   - how the owner notices it
   - severity: WRONG RESULT, CONFUSING or COSMETIC
   - a one-line proposed rule, with no code

   Sort the entries by severity and end with a 5-line summary.
6. **Report in exactly the size asked for** (often 10 plain lines), then STOP. Fix
   nothing.

## Follow-on fixes (gated, one step at a time)

An approved plan runs one step at a time: shape -> coordinator/owner go -> tests -> code ->
stop before commit.
- Append the shape as exactly the number of lines asked for, under `Step N shape`,
  at the end of the same findings file. Then stop and wait for the go.
- The shape names a single source of truth: one function computes the decision and
  every surface reads that one field. Patching each surface on its own is what
  produced the drift.
- Put any real rule change hidden inside the fix on its own line, needing an
  explicit go. For example, a tie-break that changes which name gets suggested.
- Plan the tests as RED first. Rewrite the old-rule tests rather than deleting them,
  because they pin the scenario. Give each rewritten test a one-line "Was: ..."
  in its docstring, so the old behaviour stays on record. If UI JS logic needs a
  real test and node is already installed, run the extracted functions under
  node rather than only checking the source text. Recipe:
  `references/js-under-node.md`.
- A glossary/words-only step (rename user-facing terms across window, CLI and
  docs): inventory, the never-renamed list and the dropped-words guard test are
  in `references/wording-sweep.md`.

Executing an approved step:
1. Before coding, grep the WHOLE tests tree for the old rule's assertions, not
   just the files named in the shape. Old-rule tests hide in files named after
   other features, and the full run will flag them late.
2. Write the new test file and run it to show it fails (RED) on the unchanged
   HEAD. Then add the single field in the deciding function, carry it through the
   data (queue item / --json), and make every surface read it.
3. Grep the old word and the old field (e.g. `is_primary`, "subject") across
   src, docs, the agent skill, CSS, and the generator sources of shipped
   assets. A shipped copy that a generator writes (house CSS) is tested
   byte-for-byte against its source: edit both identically, or re-run the
   generator.
4. Run both gates: the full pytest, plus the repo's own check script.
   AGENTS.md names it; it may live in the private tree, not the repo root.
5. Run `git diff --stat` and `git ls-files --eol` on the changed files, then
   `git status`. Stop before commit and report in the size asked for. Say what
   was NOT verified (the real window, the sabotage/guard script).

Closing a step once the commit is approved (then shape the next one):
1. Follow the repo's commit order from AGENTS.md: `git add -A --dry-run` plus
   `git check-ignore -v` on the private paths, commit with the given message,
   append the dated log entry (bytes, the file's own line endings). Backup and
   counts follow the repo's own procedure.
2. Mark the finding `— DONE <sha> (<date>)` on its heading in the findings file,
   so the file stays the single list of what is left. Never delete the entry.
3. Re-copy the private file to the backup after EVERY later edit to it (the
   next step's shape too), not only right after the commit.
4. Shape the next step from a fresh read of the code it touches, not from the
   review's cites. Grep each finding's cited words first: an earlier step often
   fixed part of it already. Say so in the shape, fix only the remainder, and add
   the pin test the finding proposed (it is green from the start; report it as
   "already true", not as a red-then-green test). When the reviewer pre-approves
   a step ("go without waiting"), still write the shape first, then build.
   Under a "words only, no logic" go, any gain-only JSON field the words need
   (a `source` folder for History) gets named in the report as the one exception.
   After a wording change to one row of a list, read the sibling rows in the
   shot: a capitalised new row beside an old lower-case one reads as two styles. Shaping is where hidden drifts surface (a settings box whose
   value a later step silently caps); fold them into the shape and name them.
5. Give each of these its own line in the shape, marked as needing a go:
   - a behaviour change the user will feel (something that used to be
     accepted is now refused)
   - any change to a settled rule written in AGENTS.md (e.g. "X has no undo")
   - a case where the obvious gate would block a legitimate single-item door,
     with a proposal for whether that door is inside or outside the gate
6. When the brief warns about context size, state in the report whether a
   compaction happened before or during the shaped work.

## Pitfalls

- **Replacing "the first/largest item" with "the best-scoring item" needs an
  explicit tie-break** (e.g. earlier index wins). `max()` over equal scores is
  otherwise order-dependent, and the card or plan could change between runs.
- **Leave foreign scratch files alone.** Files that predate the session, or belong
  to another agent, stay. Report them with their timestamps instead, because deleting
  them breaks that agent's work.
- **Check which temp dir the rule means.** On some hosts `$TMPDIR` can be the system
  temp. The "scratch must be empty" rule means the Hermes scratch dir.
- **Never open forbidden data paths named in the brief,** not even read-only:
  no sqlite connect, no file read. Cite the code, not the data. A `stat -c '%s
  %y'` of the db and its `-wal`/`-shm` is metadata, not an open, and is how the
  brief's size claim is checked before and after.
- **Scripted edits flip line endings on Windows.** `Path.write_text` and
  `open(..., "w")` turn `\n` into `\r\n`. In a repo stored with LF line endings,
  every file you edit then shows as wholly changed, and byte-exact tests fail. Write
  with `newline=""` or use the patch tool. Afterwards, `git ls-files --eol` must
  show `w/lf`.
- **Run the project's tests from the terminal with its own venv**
  (`.venv/Scripts/python -m pytest`), not as a subprocess of the execute_code
  kernel. The kernel's environment leaks its own site-packages into the child, so
  compiled packages fail to import.
