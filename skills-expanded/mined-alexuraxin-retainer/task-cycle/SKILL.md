---
name: task-cycle
description: "Call FIRST on receiving any code task — before the plan and before the first edit. Trigger words (RU+EN): задача, сделай, почини, добавь фичу, issue NNN, берём в работу, доработай / task, do it, fix, add a feature, issue NNN, take it into work, refine. The mandatory cycle: intake and understanding → plan → plan check → code → review → doc update, with tool triggers BEFORE the work and a Definition of Done. The frame is portable; thresholds, epics and pitfalls come from the project's .retainer/PROJECT.md."
---

# Task cycle

Mandatory order; do not skip steps. The frame is portable; project thresholds, epics
and pitfalls the agent takes from `<project>/.retainer/PROJECT.md`.

## Task intake — confirm understanding BEFORE anything

**Got a task? First write, in one or two lines, HOW you understood it, and wait for "ok". Then
act.** Policy gate: `${CLAUDE_PLUGIN_ROOT}/bin/retainer-flow-policy.sh confirm_intake` — `auto`
(default at every level) or `off` (owner disabled it; start right away).

What is checked is the task BOUNDARY: what counts as the result, where it lives, what is out of
scope. Not the plan, not the forks inside it — one phrase "understood as: …", not a retelling of
the statement.

**Where confirmation is NOT needed:** the trivial and unambiguous ("show status", "run the suite",
"continue"), and a task taken from the tracker with a ready body — there the boundary is already
written and confirmed by the `ready` label. An extra round costs more. Confirmation is for a
statement that admits two readings.

**Read `references/intake-and-triggers.md` at intake** — why the boundary is confirmed first,
the table of the two questions that must not be mixed, how confirmation is asked, and what to do
when the scope is larger than one session (a map first, `/retainer:wayfinder`).

## Step 0 — Triggers: tool BEFORE, not AFTER

**Principle: a tool is turned on BEFORE the event that makes it needed** — so that new code is born
under the check rather than rewritten after the fact.

Before planning, check the project trigger table: **does the task fall under a trigger whose tool is
not yet on?** If so — turn the tool on first, then the task. This is not a recommendation, it is a
block.

**Heavy tools (agents/skills) go BY POLICY, not by mood:** at a trigger, ask
`${CLAUDE_PLUGIN_ROOT}/bin/retainer-tool-policy.sh <code_reviewer|plan_checker|tester|second_opinion>`
→ `off` (do not touch) · `ask` (**offer** and wait for "ok") · `auto` (call it yourself). **The
default is `ask` everywhere — OFFER, do not wait for the owner's command.** The overall `tools_mode`
(always_ask/always_auto/manual) and the per-tool `tool_*` overrides are written by the panel; the
autonomy level does not govern tools — except in an autonomous run, where review is on
unconditionally. Triggers: code_reviewer — before commit; plan_checker — before code;
tester — after UI/page edits; second_opinion — an important or irreversible step.

**Which model a role runs on is a setting, read at every role call:**
`${CLAUDE_PLUGIN_ROOT}/bin/retainer-role-model.sh <code_reviewer|plan_checker|merge_checker|tester|doc_updater>`
→ a model name: pass it as the call's `model` · `inherit`: pass no `model`, the role runs on the
session's · exit 3 (the setting holds no model): call without `model` and say in the report that the
setting is broken. This is an instruction to you, not a hook — nothing else passes the model.

**Read `references/intake-and-triggers.md` before planning** — the typical triggers, and the
skill triggers the four codes do not cover ([[complexity-budget]], [[diagnosing]],
[[frontend-taste]], [[graph-first]]): which of them a machine holds and which only that file holds.

## The cycle

0. **Issue-first** — no code without an issue in the tracker. Every task = an issue (an epic
   decomposes into issues with labels: priority · area · type · impact). Branch off main: `issue-<N>-<slug>`.
   Commits reference `#<N>`. Mechanically (the kit): the commit-msg hook rejects a commit without
   `#<N>`, and a BLOCKING bypass of discipline lands in the project's `.retainer/bypass.log`. No task is filed
   from it: the auto-filing went when the engine was cut back to protecting the irreversible, and the
   log is what gets read — a bypass is not "quietly allowed" either way. Hygiene observations (below)
   do not reach the log and do not fail the gate — they are not a bypass but an unmarked step.
   **Read `references/issue-first.md` before filing, grooming or taking a task** — the
   active-issue marker, readiness as a checked state, label changes as cycle steps, the intake
   check before acceptance, and who suffers (`impact-user` / `impact-maker`).
1. **Plan** — with explicit references to project documents (epic, status, spec section). An open
   question surfaced (ambiguity, missing data, a product choice) — do not guess; record it and
   continue with what is already decided.
   - **Recording is a greppable marker IN THE PLAN**, modeled on the deferred-simplification marker
     from [[complexity-budget]]. Without a set form, "record it" means "somewhere", and a silent
     assumption looks in the plan exactly like a deliberate decision:

         [CLARIFY: <what is ambiguous>; default: <what was assumed and why>]

     **The "default" field is mandatory.** A marker without it is a stop instead of
     work: an autonomous run must not halt, and an unnamed default can be neither checked nor
     reverted.
   **Read `references/plan.md` before writing the plan** — the rest of this step: where the marker
   also goes, the scope check, "same work, or another?", the input→output map, the task format,
   and the rule "A sample for every new kind of code" with project practices.
2. **plan-checker** — run the plan through the agent before showing the plan to the owner for "ok".
   Do not skip, even if the plan seems obvious.
   **The "plan checked" signal (advisory):** on a "plan ok" verdict the agent writes `<N>` to the
   path `retainer-state.sh path plan-checked` prints (with the Write tool; where that write is
   refused, a comment on the task with the line `plan-checked: <N>`). The route reads either as the
   plan step done; nothing blocks a code edit without it.
3. **The owner's "ok" on the plan — by the policy gate, not by habit.** Ask
   `${CLAUDE_PLUGIN_ROOT}/bin/retainer-flow-policy.sh ask_owner`: `auto` — wait for an explicit "ok",
   as usual; `off` — there is no one to wait for (a long autonomous run), the plan is not agreed but
   recorded in the issue body, forks go into `open-question` issues with a recorded default, work
   proceeds by the default.
4. **Code + migrations + tests.**
5. **Gate — one command** (see [[gate]]). A green run of the subject is mandatory. During edits it is
   judged by a targeted run and a mutation probe; the full run is one, on the head that leaves the
   machine (step 9), and it also closes DoD.
6. **code-reviewer** — run the diff before commit. Mandatory for changes with an EXECUTABLE diff,
   even small ones; a change with no executable diff (docs/specs/journal only) goes through the doc
   gates, not review rounds — see "When NOT to apply".
   Give the reviewer CRAFT context: diff + acceptance criteria + the task's stated goal + SHA range +
   the task number with repository (so the role opens its body itself) +
   **the sample address for every new kind of code, or the line «No new kinds of code»** (step 1),
   WITHOUT the session history and your train of thought, so the author's
   rationalizations do not infect the review (independence: [[second-opinion]] is cross-model,
   here it is context isolation). The address is mandatory: the sample-comparison axis has no input
   without it, and the reviewer either skips the check silently or raises a finding about a document
   it was not given.
   Blocking findings → label `review-revised`, fix, rerun; clean → `review-clean`.
   **Read `references/review-and-merge.md` before the review round** — two rounds by default, the
   `review-sha` record, naming who reviewed, the run on the head that is merged, and the conflict
   marker when the role cannot be called.
7. **Commit — by the step's gate** (`retainer-flow-policy.sh commit`): `ask` — an explicit "ok" from
   the owner specifically on the commit (approving the plan ≠ approving the commit, two different
   "ok"s); `auto` — you commit yourself, but only on a green run of the subject and a clean
   code-reviewer; the full run is held by step 9. Autonomy removes the question, not the checks.
8. **doc-updater** — update the working documents (epic status, checkboxes) right after the commit,
   do not wait to be reminded. The docs commit follows the already-approved code commit as a
   separate trail — it needs no separate "ok".
   **Read `references/review-and-merge.md` before this commit** — it moves the head and voids the
   review verdict, so every head move is batched before the final role run.
9. **PR → merge** — branch `issue-<N>` → push (`pre-push` runs what the project's gate declares) → Pull Request
   → CI/review green → merge → the issue closes on merge (close-on-merge). The epic milestone
   advances as merges land.
   **Read `references/review-and-merge.md` before the merge** — which head must carry `review-sha`,
   when a merge of `main` keeps the verdict, direct push closed by a mechanism, the two seams, the
   lock status per head, and why an outside service is not a required check.
   PR outcome labels `gate-passed`/`gate-failed` are set by **CI** (not by the agent by hand);
   closing the task is one command `${CLAUDE_PLUGIN_ROOT}/bin/retainer-task-close.sh <owner/repo> <N>`
   (removes `in-progress`/`ready`/`blocked`, closes, stops the clock), not three manual actions by
   memory. `closed` is an issue state (close-on-merge), not a label.
10. **Entry point for the next session** — at the end of a wave of work rewrite
   the handoff at the path `retainer-state.sh path handoff.md` prints — one per project, read by the
   next session's preflight (template — `presets/handoff.md.template`): where we are now, landmines
   with `file:line` addresses, exhausted budgets (limits at the threshold, counters with no slack),
   reverted decisions. This is STATE, not architecture: rewritten whole, not appended from below,
   otherwise it becomes that same report inside mandatory reading. A session that starts from
   "continue" and a link here spends minutes on reconnaissance instead of an hour — and without the
   list of reverted decisions it faithfully reproduces them from the document.
11. **Compound — knowledge capture** (otherwise the same mistakes again). There was a NON-OBVIOUS
   decision / pattern / pitfall → keep it in the cheapest form that stops the repeat — a check,
   then a rule, a note only for what is left — so FUTURE work meets it without being told. Memory
   is not a warehouse but a **loop**: the system gets smarter each task. `plan-checker` checks
   against past decisions/pitfalls before a new plan. **Read `references/compound.md` before
   writing the lesson:** the order of forms, when a check is kept, and the `retire_when` line.

## Working rules

**Read `references/working-rules.md` when the work reaches one of them:** where a task's
decisions and questions live (its issue body, edited in place); the deviation journal and its
three classes; decomposition into tracer bullets and expand–contract; what a comment answers;
deep modules.

## Definition of Done — a task is finished only if all of it is done

The DoD canon lives in the project regulations (`.retainer/PROJECT.md` or a tooling document); here
is the portable frame:

- triggers checked — the task does not fall under a tool that was not turned on;
- **full gate green — one run, on the head that leaves the machine** (see [[gate]]); during work the
  subject is judged by a targeted run and a mutation probe, not the full suite per hypothesis;
- not a single new linter relaxation (per-file-ignore) without a conscious entry in the debt journal
  (RATCHET);
- import contracts unbroken (bypassing by a "it's needed" comment is not an argument);
- **the test for a fixed bug fails on the old code** (otherwise it guards nothing);
- **every task edit that carries a use case is guarded by something** — an edit that changes what a
  user or the maker gets, a scenario, a branch of a condition, a boundary, wherever it lives: break
  it mentally one at a time and name the test that would redden. If none — the test for it is either
  missing or false. Text, comments, md, html, pictures, and what the framework or the database
  already does need no test, even when the md is a rule a project reads; a page or a picture is
  accepted by the owner on a rendered preview. This costs more than it sounds: on a real run eight
  mutations of ten survived a fresh green suite, and all eight were
  places where the check checked its own safety net, not behavior;
- **a task with the `discipline` label is not closed while its result is only text.** A rule written
  in prose in a document or as a review-checklist item is not enforced: review is busy with
  functional defects and misses the class. Closing is allowed only if there is a machine (a test or
  a gate step) or an explicit line in the error journal grounded in "review" — then the debt is
  visible and counted, not dissolved;
- **a model with parallel registries has a check of LISTS, not values.** A clone, a version
  snapshot, diff specs, serialization — each field must either be in the registry or be a NAMED
  exception with a reason. A value comparison catches only what the fixture happened to fill; a list
  comparison catches everything. The class "a field was added, the mechanism did not notice"
  recurred three times before such a guard appeared;
- **a query-counter threshold is not tuned to the fact.** Each increment is a separate comment line:
  what the query is, why it is legitimate. Otherwise "the test is in the way, I'll bump it by one"
  silently lets N+1 through: the batching guard's slack runs out unnoticed;
- **data left text for a field → in the SAME commit it has a place on the output artifact.**
  Otherwise it is dense in the database but empty in the client document;
- acceptance criteria from the issue/plan are met;
- state labels switched by cycle steps (start `in-progress`/remove `ready`; pause → `blocked`;
  review round `review-revised`→`review-clean`; finish → close via `retainer-task-close.sh`, which
  removes the working label in the same call; `gate-*` is set by CI). `retainer-preflight` enforces
  both sides: `in-progress`/`blocked` for an active issue (`active-label`) and the absence of a
  working label on closed ones (`closed-labels`);
- in `git diff` only the files declared in the plan, or declared as a widening in the issue body
  or a comment on it;
- code-reviewer with no blocking findings;
- migrations created and applied, if models changed;
- the actual-architecture document updated in the same commit, if facts changed;
- the code commit passed its gate: on `ask` an explicit owner "ok", on `auto` a green run of the
  subject and a clean code-reviewer (in an autonomous run these are the replacement for the manual
  "ok", not its removal); the full run holds the code leaving the machine, not each commit.

## Verification before claiming "done"

**No claims of success without fresh evidence.** Before "done/fixed/passes": by what command is it
proven → run it FULLY and fresh → read the whole output and exit code → only then claim, together
with the evidence. "Sure" ≠ evidence.

**Claim → what it requires → what is NOT enough:**

| Claim | Requires (fresh, in this same message) | NOT enough |
|---|---|---|
| "tests pass" | run output: 0 failures | "should pass", "didn't touch tests" |
| "bug fixed" | test of the original symptom: red on old code → green | "code changed", "looks right" |
| "gate green" | gate run on the head that leaves, exit 0 | "was green before the last edit" |
| "agent finished the task" | VCS diff + run of the stated command | "the agent reported success" |

**No satisfaction words before evidence.** "Done!/Great!/Works!" — not before the proving command is
run in THIS SAME message and its output read with the exit code. Satisfaction before a fresh run is
a signal of rationalization, not fact. A subagent's success report — verify independently
(diff/output), not on its word.

## When to stop and ask

**Policy gate first, then the question.** About to stop work with a question to the owner — ask
`${CLAUDE_PLUGIN_ROOT}/bin/retainer-flow-policy.sh ask_owner`. This is about a fork INSIDE the task;
a question about its BOUNDARY goes through a different gate and is not governed by the list in `references/stop-and-ask.md` (see
"Task intake"):

**Read `references/stop-and-ask.md` before ending a turn on a question, a wait or a handoff** — what
`auto` and `off` allow, the `handoff: <code>` line and its codes, the decision through the
question tool, and the list of cases that do stop the work.

## When NOT to apply

- **The edit does not change behavior** — a typo in text, a comment, formatting. The full cycle
  costs more than the edit here, and running it for form's sake devalues the cycle where it is
  needed.
- **No executable diff** — docs, specs or journal only. The doc gates already check these; the
  code-reviewer and second-opinion rounds add nothing. The `review-sha` record (a self-check) still
  stands — it is about the identity of what is merged, not a role run. HOW to tell there is no
  executable diff is a project-level selection (in retainer, `ci-scope`), not this portable skill.
- **Not for research or planning.** The cycle executes the decided; working out a decision is
  `/retainer:wayfinder`, gathering facts is `/retainer:research`. Both user-invoked: the agent
  offers them, the owner launches.
- **Not a replacement for the gate or the guard.** The cycle says WHAT to do in order; the machine
  checks, and a green cycle on a red gate means exactly nothing.
- **Not for someone else's project with an established process**: two processes over one piece of
  work give not double discipline but mutual exclusion.
