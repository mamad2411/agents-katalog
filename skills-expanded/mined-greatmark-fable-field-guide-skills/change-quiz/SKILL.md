---
name: change-quiz
description: >-
  Generate one droppable self-contained HTML report (never a Cursor
  canvas) explaining a change set, ending with a quiz the user must pass
  before merging. Use when the user says "quiz me", "考考我",
  "change quiz", "变更测验", or, after a large change or session, wants
  to verify they truly understand it — e.g. "merge 之前考考我这轮改动",
  or says "review" meaning their own understanding, not bug-finding. The
  audience is the user themselves — selling it to reviewers is
  pitch-explainer; finding bugs is a code review. Not for writing tests
  or quizzes unrelated to a change set (general knowledge, interview
  prep).
---

# Change Quiz

After a long session, the diff alone undersells what changed, because much of
the behavior depends on existing code paths. Build the user's understanding,
then verify it.

## Workflow

1. **Determine scope**: the current session's changes by default, or the
   diff/branch/PR the user points at. If there is no discernible change set,
   ask what to quiz on instead of guessing (a pre-work worry with no changes
   yet is blindspot-pass territory, not a quiz). Read the touched code *and*
   the existing code paths it plugs into. If `implementation-notes.md`
   exists, mine its Deviations and Surprises sections first — they are
   pre-indexed quiz material.
2. **Write one self-contained HTML file** (`change-report.html` in the
   project root, in the language of the conversation; inline CSS/JS, no
   network). It describes the current change set only — if an existing
   report recorded a passed quiz, rename it `change-report-<YYYY-MM-DD>.html`
   before overwriting. The report must stay out of the change set it
   describes: do not commit it, and if this is a git repo, exclude it
   locally:
   `n=change-report.html; p="$(git rev-parse --git-path info/exclude 2>/dev/null)" && { mkdir -p "$(dirname "$p")" && { grep -qxF "$n" "$p" || echo "$n" >> "$p"; }; } 2>/dev/null || echo "note: could not exclude $n — leaving it untracked, never staging it"`
   (worktree-safe; if the write is blocked, tell the user to add it manually
   and continue). The deliverable is the file itself — never render the
   report or quiz as a Cursor canvas: the merge gate must live in a single
   shareable file that opens outside the IDE. Contents:
   - **Context & intent** — the problem, and the shape of the solution.
   - **What changed** — grouped by area, each linking file paths and
     explaining how the change interacts with pre-existing behavior.
   - **Behavior changes & risks** — what users/callers will observe
     differently; what could break and where to look if it does.
3. **End the file with a quiz**: 5-8 questions, answers hidden until clicked.
   Each question gets a "show answer" disclosure plus a self-check checkbox;
   a fixed score bar tracks N/total and turns green only when total > 0 and
   every box is checked — an empty quiz must never display as passed. State
   in the report that checkboxes are self-assessment only; the authoritative
   pass is the in-chat grading. Target the parts most likely to surprise:
   - behavior that depends on existing code paths, not just new code
   - edge cases and failure modes the change handles (or deliberately doesn't)
   - "what happens if X" tracing questions
   Avoid trivia answerable by skimming the diff (file names, line counts).
   A good question: "The new retry wrapper calls `fetchUser()` — what happens
   on the third failure, given the existing circuit breaker in
   `api/client.ts`?" — its answer lives in how the change interacts with a
   pre-existing code path, not in the diff itself.
4. **Hold the bar**: the rule is: merge only after a perfect score.
   - Primary path: the user answers in chat *before* opening the hidden
     answers; grade strictly — for any miss, explain the right answer, point
     to the exact code, then ask one fresh question on the same topic. After
     two consecutive misses on the same topic, stop replacing: explain it
     thoroughly, mark that question "passed by coaching", and say so
     honestly in the verdict. Passed = every question answered correctly or
     explicitly marked passed-by-coaching.
   - Self-serve path: if the user self-checks against the hidden answers,
     that is honor-system and does not establish a graded pass — say so. If
     they claim a pass and want it to count, spot-check by asking them to
     restate the key points of two questions in chat. A question whose
     answer was already revealed can only go this route; a graded pass
     requires answering before revealing.
   - For the rest of this session, if asked to merge before a pass, remind
     the user the quiz is unpassed before running the merge (advisory only —
     never refuse an explicit instruction).
   - After a pass: offer to delete `change-report.html`, or mark it passed
     by inserting `<!-- FIELD-GUIDE-QUIZ-PASSED <YYYY-MM-DD> -->` as the
     file's first line, so the merge-gate hook stops reminding. If the
     change now needs explaining to reviewers, that handoff is
     pitch-explainer.

## Rules

- Write questions from the reviewer's perspective ("will this break X?"), not
  the author's.
- Precedence when rules collide: the trivial escape below wins over the size
  downgrade — a change that is mechanical throughout (lockfile bumps, pure
  renames, formatting) is trivial regardless of line or file count.
- For very large change sets (roughly >30 files or >2000 changed lines),
  group by subsystem, quiz only the 2-3 riskiest areas with 3-5 questions
  total (not 5-8), and state in the report which areas the quiz does not
  cover. "Riskiest" means runtime blast radius, not diff size: prioritize
  changes to existing behavior, code without test coverage, and changes that
  are hard to roll back; production code outranks tests — test churn is
  usually the least risky.
- If the change is genuinely trivial, say a quiz is overkill and give a
  three-sentence summary instead. Trivial means zero behavior change, and
  you have verified that: one hidden logic change inside a "formatting only"
  diff makes it not trivial — quiz that line.
