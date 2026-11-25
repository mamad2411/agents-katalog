---
name: tdd2
description: Issue-driven TDD for a single local issue file (issues/issue-#.md) — red-green-refactor, then write regression-tests/verify-issue-#.sh, run ruff+pyright+pytest+regression scripts (project's own run-*.sh if present, else this package's defaults), do UI verification when the issue calls for it, update the issue's 구현 결과 section, stop at git add. With no issue number, detects an in-progress issue to resume or picks the smallest pending one to start, and asks first. Use when the user says "/tdd2", "tdd2 #", or asks to implement a numbered local issue test-first.
---

# tdd2 — issue-driven TDD, local-file SDLC

**Dependency**: the red→green→refactor discipline itself (test at
agreed seams, no implementation-coupled or tautological tests, one
slice at a time) is Matt Pocock's `tdd` skill — this skill assumes
`tdd` (`~/.claude/skills/tdd/`) is installed and wraps it with this
project family's local-file SDLC: issues live in `issues/issue-#.md`
(never GitHub/GitLab), and implementation stops at `git add` — merging
is a separate step, handled by the `acpd` skill (directly, or chained
per-issue by `/autotdd`, which also checks that `tdd` is present
before starting — see that skill if `tdd` turns out to be missing).

No script of its own. For the `run-ruff` / `run-pyright` /
`run-unit-tests` / `run-regression-tests` / `run-pyright-full` checks
in the procedure below, this skill shares `acpd`'s resolution
convention and bundled defaults (`../acpd/defaults/`, a sibling skill
directory — both ship together in this package) rather than
duplicating them.

## Argument parsing

`tdd2 issue-280`, `tdd2 issue 280`, `tdd2 280` are all the same thing:
extract the digits from the first token, normalize to `#`, read
`issues/issue-#.md`.

## No issue number given — resume or pick, then ask

Run when the user says `/tdd2` with no number:

1. **Look for an in-progress issue** — one whose `## 구현 결과` is still
   the `(미정)` placeholder but that already has a draft
   `regression-tests/verify-issue-#.sh` (written in step 4 below,
   before an issue is finished — its presence means work started but
   didn't reach completion):

   ```bash
   for f in issues/issue-*.md; do
     n=$(basename "$f" .md | sed 's/^issue-//')
     if grep -q '\*\*구현 완료 일시\*\*: *(미정)' "$f" \
        && [ -f "regression-tests/verify-issue-${n}.sh" ]; then
       echo "$n"
     fi
   done
   ```

   Found one (or more — take the smallest) → ask: "issue #N looks
   in-progress — resume it?"

2. **Nothing in-progress** → pick the smallest-numbered not-yet-started
   issue:

   ```bash
   for f in issues/issue-*.md; do
     n=$(basename "$f" .md | sed 's/^issue-//')
     grep -q '\*\*구현 완료 일시\*\*: *(미정)' "$f" \
       && [ ! -f "regression-tests/verify-issue-${n}.sh" ] \
       && echo "$n"
   done | sort -n | head -1
   ```

   Ask: "no issue in progress — start with issue #N (smallest
   pending)?"

3. No candidates either way → report `issues/` has nothing left to do.

This is the only place `tdd2` asks anything. Given an explicit issue
number, it just starts — no confirmation.

## Execution mode

**Stop at `git add`.** Implement, verify, update the issue file, stage
everything — then stop. Do not commit, push, archive, or deploy. A
human (or the `acpd` skill, or `/autotdd` looping both) takes it from
there. This boundary matters for `/autotdd`: each issue must be fully
merged (`tdd2` → `acpd`) before the next one starts, so a mid-batch
failure has an unambiguous line between what's live and what isn't.

## Procedure

1. Read `issues/issue-#.md` to understand what's being built.
2. Implement via red→green→refactor: write the failing test first,
   then only enough code to pass it, at pre-agreed seams (the public
   boundary you test at — never internals). No implementation-coupled
   tests (mocking internal collaborators, testing private methods), no
   tautological assertions (expected value computed the same way the
   code computes it) — expected values come from an independent source
   of truth. Work in vertical slices: one seam, one test, one minimal
   implementation, repeat. Refactoring happens at review time, not
   inside this loop.
3. **DB DDL changes only**: run `./upgrade_db.sh --env dev`. (qa/prod
   DDL is applied by a human separately — never touch those here.)
4. Write `regression-tests/verify-issue-#.sh`: mechanical checks for
   *this issue's* acceptance criteria only (grep for required
   functions/CSS/HTML, check migration files exist, etc). Do **not**
   put `ruff check`, `pyright`, or the full `pytest` suite in this
   script — those run separately in steps 5–8. A targeted
   `uv run pytest tests/some_file.py` for this issue's own test file is
   fine to include. `chmod +x` it. (This file's existence is also what
   the no-arg resume-detection above looks for.)
5. **Python projects only** (repo has `pyproject.toml`): run `run-ruff`
   and `run-pyright`. For each, prefer the project's own
   `./run-<name>.sh` if present; otherwise use this package's bundled
   default at `../acpd/defaults/run-<name>.sh` (relative to this skill
   directory — invoke with `bash`, CWD at the repo root; never copy it
   into the project). `run-pyright` is scoped to `src/`, fast.
   Failure → fix code, restart from 5.
6. `uv run python -m compileall . -q`. Failure → fix code, restart from 5.
7. `run-unit-tests` (full suite) — same project-or-default resolution
   as step 5. Failure → fix code, restart from 5.
8. Run `./regression-tests/verify-issue-#.sh` directly (this is the
   issue-specific script from step 4, not the `run-regression-tests`
   wrapper). Exit 0 → continue. Non-zero → fix implementation, restart
   from 5.
9. `run-regression-tests` — same project-or-default resolution as step
   5; runs every *other* existing `regression-tests/verify-issue-*.sh`
   in order.
   - All pass → continue.
   - A failure is either: (a) a real bug in the new code — fix and
     restart from 5; or (b) that script's own criteria are now
     obsolete because this issue intentionally changed behavior —
     update that script, then write
     `regression-tests/verify-issue-<old#>.conflict-with-<this#>.md`
     documenting what changed and why (a human reviews and resolves
     that file later; stage it with the rest).
   - **Python projects only**: also run `run-pyright-full` (whole
     project, no path restriction — slower than step 5's `run-pyright`)
     before moving on. Same failure handling as above.
10. **UI verification** — only if the issue has a `### UI 검증`
    section:
    - `agent-browser` MCP available → drive the golden path and error
      cases directly, confirm no console errors.
    - Not available → print the issue's manual-verification checklist
      and ask the user to check it. Wait up to 2 minutes (a response
      interrupts the wait and its content is used to continue). No
      response after 2 minutes → post a 30-second countdown warning,
      wait 30s more, then fall back to the `agent-browser` skill for
      automated verification.
    - This step is never skipped — only the *method* varies. **Exception:
      when running as part of `/autotdd`**, that skill's
      fully-automatic mode forbids waiting on a human — if
      `agent-browser` isn't available, stop and report instead of
      prompting-then-waiting.
11. Update `issues/issue-#.md`'s `## 구현 결과` section: completion
    timestamp (ISO 8601), changed files, deviation from plan (or
    "없음"), and the verify result (this script's pass/fail +
    regression suite status).
12. `git add` everything: migration files, code, the updated issue
    file, any `.conflict-with-` notes.
13. **Stop.** Report what was implemented and that it's ready for
    `acpd #` (or, mid-batch under `/autotdd`, that it will be chained
    automatically).

Both a human and an agent use the same completion bar:
`verify-issue-#.sh` exits 0 *and* every existing regression script
still passes.
