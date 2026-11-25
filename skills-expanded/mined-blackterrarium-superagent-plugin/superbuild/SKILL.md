---
name: superbuild
description: Use when superrun must execute a leaf implementation plan's tasks — the native task loop: a fresh implementer per task, a spec + quality review of each task, a capped fix loop, one whole-branch review, and a progress ledger that survives compaction. Invoked by superrun Step 3; not a standalone entry point.
license: MIT
related skills: superrun, superloop
---

# Superbuild

The task loop `superrun` Step 3 runs to turn a leaf plan into reviewed code. You are the
**controller**: you dispatch one subagent per role, hand each its inputs as files, and keep a
ledger. You write no source code and fix no finding yourself — controller edits skip review and
fill the context you need for coordination.

superbuild owns B1–B7 (including B2a) below and nothing else. The caller (`superrun`) owns target selection, the
workspace (Step 2), the execution profile (role models and efforts, test-evidence mode, CI
scheduling, repo notes, the acceptance agreement), integration (Step 3a), and closeout. Where a
clause says *per the profile*, read it from superrun's **Execution profile**.

**You must be the top-level agent of your process.** Every dispatch is a foreground, synchronous
call: you wait for the child's final message. One implementing subagent at a time — never two
writers in one workspace, never a background or parallel run.

**Run to the end.** Do not pause between tasks, ask "should I continue?", or post progress
summaries. Exactly three things end the loop early: a **BLOCKED** outcome under B5, a role
dispatch that cannot be made (missing definition, missing subagent tool — a hard error per the
profile), or a **CHECKPOINT** yield at a task boundary because the dispatch deadline is near (B4.6).

**Keep investigation out of the delivery.** Instrumentation, probes, timing hooks or other tooling
written to diagnose a failure never enter this branch's commits unless the plan's scope names them as
a deliverable. Keep them uncommitted in the plan's scratch directory, or on a separate throwaway
branch outside this worktree's branch; if a diagnostic run needs CI, push the throwaway branch, never
the stage's PR. Their tests must never join the suite the stage delivers.

## B1 — Workspace and ledger

Conversation memory does not survive compaction; a controller that lost its place re-dispatches
whole completed task sequences. The ledger, not your recollection, is the record.

1. Resolve this plan's scratch directory:
   `bash "${CLAUDE_PLUGIN_ROOT}/scripts/superbuild.sh" workspace <leaf plan>`, run from the
   execution workspace. It prints `<workspace>/.superagent-runtime/build/<plan-slug>/` (git-ignored;
   one directory per plan — another plan's directory is never yours to read or write). In
   `SUPER_GIT_MODE=none`, set `SUPERBUILD_ROOT` to the recorded physical `REPO` on every
   `superbuild.sh` call so it runs no git command.
2. The ledger is `<dir>/progress.md`, first line `# superbuild ledger — plan: <leaf plan path>`.
   Create it if absent. If it exists and names this plan, **resume**: a task with a
   `Task <N>: complete` line is DONE — never re-dispatch it; a task whose last line is a fix round
   resumes at the next round; `Final review: dispatched` means resume B6; a
   `Final review: fix wave <W>/2 started` line means that wave was interrupted — resume it as B6
   step 5 says; a `Final review: fix wave <W>/2 (…)` line means that wave and its re-review are
   spent — resume B6 at the decision that follows it, reading the open findings from the file the
   line names; a `Final review: clean` or `Final review: <K> parked` line means the loop already
   finished — go straight to B7. A last line `CHECKPOINT: … — next: <step>` means an earlier
   dispatch yielded at its deadline (B4.6): resume at the step it names, applying the rule above for
   the ledger line before it (a spent or started fix wave, an open-findings file).
   After compaction, trust the ledger and (in `github`) `git log` over your memory.
3. Read the leaf plan once. Note its Global Constraints, its approved acceptance rows and their
   source, and track one todo per task. If the plan names a spec or source agreement, read that
   too — it is the authority the plan argues from.

## B2 — Pre-flight scan

Before dispatching Task 1 (skip on resume if the ledger already holds the table), scan the plan
once and write the result to the ledger as a table, not a verdict:

- one row per pair of tasks that share a file or an interface — what one produces against what the
  other consumes, and what you found;
- one row per task — whether its own text agrees with itself (its tests against its code, the files
  it creates against the files it later touches) and with the Global Constraints;
- one row per task whose files match `SUPER_PROTECTED_PATHS` (`superagent_protected_match`), with
  the authority the plan cites for changing them — a source document or a recorded owner answer.
  A protected file with no cited authority is a conflict for B5.

Route every conflict the scan finds through **B5** before execution begins. A clean scan proceeds
without comment. The review loop remains the net for conflicts that only emerge in implementation.

## B2a — Review plan: scale task review to risk (keyed by `SUPER_REVIEW_DEPTH`)

The whole-branch review (B6) always runs. What varies is whether a task also gets its own review
(B4.3) before the next task starts. Decide this once, before dispatching Task 1 (skip on resume if
the ledger already holds the review plan), and write it to the ledger.

- **`SUPER_REVIEW_DEPTH=full`** — every task gets its own review. Ledger
  `Review plan: full (SUPER_REVIEW_DEPTH=full)` and continue.
- **`SUPER_REVIEW_DEPTH=risk`** (the shipped default) — **you classify each task.** The
  determination is the controller's: it runs on the model the profile pins for the executor
  (`SUPER_MODEL_EXECUTOR`), never on an implementer or reviewer tier, and is never delegated to a
  subagent. Write a table — task, depth, reason — where depth is `task` (its own review) or
  `branch` (reviewed only as part of the whole-branch review).

A task is **`task`** depth when any of these holds:

- a later task consumes what it produces (a row in the B2 table) — a defect here would be built on;
- it touches security-sensitive code, authentication or secrets, destructive or irreversible
  operations, data migration, concurrency or locking, or a public or cross-stage contract;
- it is written from a prose description rather than complete code in the plan, or it coordinates
  changes across several files;
- you cannot tell.

A task is **`branch`** depth only when **all** of these hold: nothing later consumes it (or it is
the last task); it is mechanical — transcription of code the plan gives in full, configuration,
scaffolding, documentation, or verification that changes no tracked file; and none of the `task`
criteria apply. A **single-task leaf** is `branch` unless a `task` criterion other than the first
applies: its task review and its whole-branch review would read the identical diff.

Each reason cites the criterion that decided it. Classification is a judgment about risk, not a
way to shorten the run: "small" or "simple" alone is not a reason, and the batch rule in B3 does
not change a batch's depth — a batch takes the highest depth of its members.

**A `branch` task is upgraded to `task`, never the reverse.** Upgrade it, and ledger
`Task <N>: review upgraded to task — <reason>`, when its implementer reports DONE_WITH_CONCERNS
about correctness or scope, when the task needed a re-dispatch (NEEDS_CONTEXT, BLOCKED, or a
crashed child), or when its change touches files its brief does not list. A `task` classification
is never lowered once written.

## B3 — Roles and dispatch

| Role | Does | Prompt |
|---|---|---|
| IMPLEMENTER | implements one task, tests it, writes the report | `templates/build-implementer.md` |
| TASK_REVIEWER | spec + quality verdicts on one task's diff | `templates/build-task-reviewer.md` |
| FIX_APPLIER | applies a given list of findings or a fix plan | `templates/build-implementer.md` + findings |
| RE_REVIEWER | verdicts the findings against the fix diff | `templates/build-re-reviewer.md` |
| FIX_PLANNER | fix rounds 4–5: diagnoses why the fixes are not landing; read-only | inline, B4.4 |
| BRANCH_REVIEWER | the one whole-branch review | `templates/build-branch-reviewer.md` |

Templates live under `${CLAUDE_PLUGIN_ROOT}/templates/`. Read each once, on first use. Dispatch
every role on the model and effort the profile assigns it — never on an unpinned default, and never
on a substitute tier when a pin cannot be honored.

**Hand artifacts over as files.** Everything you paste into a dispatch, and everything a child
prints back, stays in your context for the rest of the run. A dispatch describes one task, not the
session's history: the task, the interfaces it touches, the constraints that bind it. Never paste
accumulated prior-task summaries, and never make a child read the whole plan.

Two blocks are substituted into every prompt, chosen by the profile:

- `[WORKSPACE_RULES]`
  - `SUPER_GIT_MODE=github`: *"Work only inside the directory above (a git worktree on its feature
    branch). Commit your work there. Do not push, open or merge a PR, switch branches, or touch any
    other checkout."* — reviewers get only the directory sentence.
  - `SUPER_GIT_MODE=none`: *"Git mode: none. Work in the recorded project under inherited workspace
    ownership. Run no git, gh, worktree, commit, push, PR, or merge operation, even if a `.git`
    directory exists. Report the files you changed instead of commits."*
- `[TEST_EVIDENCE_RULES]`
  - `SUPER_TEST_EVIDENCE=local`: *"Test evidence is local. Where the task specifies a test-first
    cycle, report RED (the command, the failing output before implementation, why that failure was
    expected) and GREEN (the command and passing output after). Run the focused test while
    iterating and the full suite once before you finish."* Reviewers: *"The implementer ran the
    tests; run one only for a specific doubt no existing run answers, and then a focused test."*
  - `SUPER_TEST_EVIDENCE=ci`: *"Test evidence is CI. Run no test runner and no build locally. Push
    exactly as your task step specifies and report each run id and its conclusion."* Reviewers:
    *"Judge the code and the reported CI results; execute nothing."*

**Batch small same-shape work.** When several tasks are each the same small independent edit
repeated across files, send them as ONE brief listing every file and its change to one implementer
and review the result as one unit.

## B4 — The task loop

For each task without a completion line, in plan order:

### B4.1 Dispatch the implementer

1. Record the review base: in `github`, `BASE=$(git rev-parse HEAD)`; in `none`, a fresh
   `workspace-state.py snapshot` manifest.
2. `bash "${CLAUDE_PLUGIN_ROOT}/scripts/superbuild.sh" brief <leaf plan> <N>` writes
   `<dir>/task-<N>-brief.md`. Exact values appear only in the brief.
3. Fill `build-implementer.md`: the brief path, the Global Constraints verbatim, the task's
   approved acceptance rows verbatim, the context only you hold, the report path
   `<dir>/task-<N>-report.md`, `[PROTECTED_PATHS]` (the `SUPER_PROTECTED_PATHS` globs, or `none`),
   and the two blocks. Dispatch as IMPLEMENTER and keep the child's
   identity for the fix loop.

### B4.2 Handle the report

- **DONE** → B4.3.
- **DONE_WITH_CONCERNS** → read the concerns. Correctness or scope concerns are resolved before
  review (route a plan problem through B5); observations are ledgered and you proceed to B4.3.
- **NEEDS_CONTEXT** → supply the missing context and re-dispatch.
- **BLOCKED** → change something, never just retry: more context; a smaller slice of the task; or,
  if the plan itself is wrong, B5.
- A crashed child or a reply beginning `BRIDGE-FAILED` → retry once, then **BLOCKED**, quoting the
  `log=` path.

### B4.3 Review the task

This step runs for every task whose depth in the review plan (B2a) is `task` — which is every task
under `SUPER_REVIEW_DEPTH=full`. Never skip it for such a task and never accept a review missing
either verdict. Implementer self-review does not replace it.

For a `branch`-depth task, first check the B2a upgrade conditions. If none applies, do not dispatch
a task reviewer: confirm the report file exists and carries the test evidence the profile requires
(send it back to the implementer if not), build the review package as in step 1 so the range is
recorded, and go to B4.5.

1. Build the review package as a file. `github`:
   `bash "${CLAUDE_PLUGIN_ROOT}/scripts/superbuild.sh" package <leaf plan> "$BASE" HEAD` — always
   the base you recorded, never `HEAD~1`, which drops all but the last commit of a multi-commit
   task. `none`: snapshot again, `workspace-state.py compare` the two manifests, and write the
   compare result plus a content diff of each changed file to `<dir>/review-task-<N>.diff`.
2. Dispatch TASK_REVIEWER with the brief, the report, the package, the Global Constraints and the
   acceptance rows. Add no open-ended directive ("check all uses") without a task-specific reason,
   and **never pre-judge**: do not tell a reviewer to ignore or downgrade something. A finding you
   believe is a false positive is raised and then adjudicated.
3. **Filter by confidence** (the profile's `SUPER_REVIEW_CONFIDENCE_FILTER=controller`): act on
   high-confidence findings. Ledger every other finding as
   `Task <N>: deferred (<severity>, <confidence>): <one-liner>` for the final review to triage —
   never drop one silently.
4. Resolve each `⚠️ Cannot verify from diff` item yourself — you hold the cross-task context. A
   confirmed gap is a failed spec review.
5. Ledger high-confidence Minor findings as `Task <N>: minor (deferred): <one-liner>`; they never
   enter the fix loop.

The fix loop triggers on spec ❌, any high-confidence Critical or Important finding, or a confirmed
⚠️ gap. A finding that is labeled **plan-mandated**, or that collides with what the plan text
requires, goes to **B5** first — never dismiss it because the plan mandates it, and never dispatch
a fix that contradicts the plan.

### B4.4 The fix loop — five rounds maximum per task

A round is one fix dispatch plus one scoped re-review.

- **Rounds 1–3.** Send the open findings verbatim to the original implementer if your harness can
  continue a finished subagent and wait for it synchronously; otherwise dispatch a fresh
  FIX_APPLIER with the brief, the report file and the findings. The report file is the persistent
  memory either way.
- **Rounds 4–5.** Three failed rounds usually mean the fixer cannot see its own problem. Dispatch
  FIX_PLANNER, read-only, with the brief, the report file, the open findings and the latest review
  package: *"A prior implementer attempted this [R-1] times. Diagnose why the fixes are not
  landing and write a concrete fix plan — files, changes, covering tests — to
  `<dir>/task-<N>-fixplan-<R>.md`. Change nothing. Reply with the path and one line."* Then
  dispatch a fresh FIX_APPLIER with that plan.
- **Every round.** The fixer re-runs the tests covering the amended code and appends a fix report.
  Confirm the report names the covering tests, the command and the output (or the CI run and
  conclusion) before re-reviewing. Build the package over `FIX_BASE..HEAD` — FIX_BASE is the head
  the previous review saw — and dispatch RE_REVIEWER with the findings list. New high-confidence
  Critical/Important breakage in the fix diff joins the open findings; out-of-scope observations
  go to the ledger as deferred.
- After each round, ledger:
  `Task <N>: fix round <R>/5 (<X> addressed, <Y> open — <one-liners>; <base7>..<head7>)`.

**The breaker.** If round 5 leaves findings open, stop dispatching and adjudicate each one under
**B5**. Adjudicate only at the cap — ending a loop early by adjudication is pre-judging under
another name. First write a **cap summary** (B5) for the open findings to
`<dir>/cap-summary-task-<N>.md`.

### B4.5 Complete the task

When the review is clean, or every open finding is parked with a ruling at the cap, append
`Task <N>: complete (<base7>..<head7>, review clean | <K> parked)` and move on. For a
`branch`-depth task append
`Task <N>: complete (<base7>..<head7>, review: branch)`. Never start the next
task while a Critical or Important finding is neither fixed nor parked with a ruling.

**Long commands.** Whenever a single command you or a child ran took more than 10 minutes — a full
test gate, a build, a local stress run — ledger `Long command: <command> — <minutes> min`. The
deadline check below and a supervisor recovering from a timed-out dispatch both read these lines.

### B4.6 Deadline check — yield before the wall clock

A dispatched executor runs under a hard wall-clock limit. When it is passed one, the environment
holds `SUPER_EXECUTOR_DEADLINE_EPOCH` (Unix seconds) and `SUPER_EXECUTOR_TIMEOUT_MIN`. At every task
boundary — after a `Task <N>: complete` line, and before dispatching the final review or a final fix
wave — compute the time left (`$(( SUPER_EXECUTOR_DEADLINE_EPOCH - $(date +%s) ))`) and the
margin: 20% of the limit, or the longest `Long command` in the ledger, whichever is larger. If the
time left is below the margin, do not start the next unit of work: ledger
`CHECKPOINT: <tasks done>/<tasks total> — next: <the next ledger step>`, commit nothing extra, and
return a **CHECKPOINT** outcome to superrun with the ledger path and the next step. Work in the
workspace stays in place; the next dispatch resumes from the ledger (B1). With no deadline in the
environment (a human running superrun), skip this check.

When the dispatch carries **single-step guidance** (the supervisor's response to repeated timeouts),
run exactly the next ledger step — one task with its review, or one final-review stage — then return
CHECKPOINT regardless of the time left.

## B5 — Conflicts: rule on the minor, block on the load-bearing

A conflict is anything the plan does not settle or settles two ways: a pre-flight contradiction, a
plan-mandated finding, an ambiguity an implementer raises, a finding still open at the breaker.
Classify each one by what depends on it. Check the body-against-commitments rule below
first: a conflict it covers is fixed under a ruling even when a later task builds on the same code.

**Load-bearing → BLOCKED.** A conflict is load-bearing when any of these holds:

- a later task, another stage, or a consumer of a produced contract builds on the disputed point;
- resolving it would change the plan's Global Constraints, an approved acceptance row, a contract
  ID or revision, or the stage's scope — acceptance is never silently widened or weakened;
- the plan's **commitments** themselves are wrong or contradict each other — its acceptance rows,
  Global Constraints, contracts, or scope against its spec or source agreement — so that no
  implementation could satisfy them all;
- it is a real defect, open at the breaker, that later work depends on;
- the resolution needs an irreversible, destructive, or security-sensitive action, or a side
  effect outside the execution workspace that Step 3a does not already authorize;
- the resolution would change a **protected surface** (superrun's Execution profile item 7): a file
  matching `SUPER_PROTECTED_PATHS`, or a value the project's own instructions pin. Name the exact
  change — file, old value, new value, and the evidence — in the BLOCKED packet so the caller can
  ask for exactly that; an owner approval passed in as guidance authorizes that change only;
- you cannot tell whether it is load-bearing.

Stop the loop. Ledger `BLOCKED: <conflict> — <the plan text it collides with>` and return a BLOCKED
outcome to superrun carrying the finding, the colliding plan text, the tasks completed so far, and
the ledger path. Leave the workspace and ledger in place. The caller — a `superagent` loop's
escalation ladder, or the human running superrun — decides; never ask the user from inside the
loop. For an upfront stage, a broken source, stage, predecessor, or contract assumption is
`REPLAN-REQUIRED` as superrun Step 1 defines it, never an in-place ruling. That includes a provider
that cannot return a result an acceptance case needs (a success, a complete verdict, a supported
input): never fake the result in a production path or through an interface that refuses
caller-supplied results. The REPLAN-REQUIRED packet names the case, the provider and its limitation,
and lists superreplan's remedies 1–5 (*Prefer the smallest unblocking change*) with which appear to
apply.

**The plan's body against the plan's own commitments → fix under a ruling.** When code or steps
the plan prescribes — even "exactly this content" — fail an approved acceptance row, a Global
Constraint, or a contract that the same plan commits to, the commitments win and the body is the
defect. This is not load-bearing: nothing the plan promised changes. Dispatch the fix through the
normal fix loop (or the final fix wave), smallest change that satisfies the commitment, and ledger
`Ruling: depart from the plan body at <where> — <which commitment it failed> — <what it costs if
wrong>`. It becomes BLOCKED only if the fix is not determinable from the commitments, would itself
change one of them, or is still failing when the fix loop's cap or the final fix waves (B6) are
spent.

**Constraint origin.** A restriction in the plan may carry an origin tag: `[source: …]` (a cited
project document or protected surface), `[owner: …]` (a cited recorded answer), or `[planner]`
(added by a planner, refiner or replanner on its own judgment). When a constraint tagged
`[planner]` stands in the way of the best-supported fix — a diagnostic budget, a ban on rerunning a
job, an excluded log source — you may relax it under a ruling, without the owner:
`Ruling: relax [planner] constraint "<text>" — <why the evidence needs it> — <what it costs if
wrong>`. A `source` or `owner` constraint is never relaxed this way; a conflict with one is
load-bearing. An untagged constraint is not `[planner]` for this purpose.

**At a cap, report the cheapest unblock.** Whenever a cap ends work with findings still open — the
breaker after round 5, or the final review with no wave left — write a **cap summary** before you
adjudicate. For each open finding:

- what was tried, round by round;
- why it did not land;
- the smallest change that would close it (files and the change itself);
- whether that change is in this stage's scope, and whether it touches a protected surface.

A BLOCKED packet issued at a cap carries the cap summary's path and content. It lets the caller
choose between one more targeted round on exactly that change, a protected-change request, or a
re-plan — with the information in hand instead of a bare "cap reached".

**Everything else → rule and continue.** A local ambiguity nothing downstream consumes, a
contestable reviewer point, a real but isolated defect at the breaker: decide it, with the spec as
the binding authority and the plan as its argument, and ledger
`Ruling: <what you decided> — <why> — <what it costs if wrong>` (at the breaker,
`Task <N>: parked — <finding> — Ruling: …`). Carry the ruling into the dispatches it affects. A
silent discard is forbidden: every decision you take is a ledger line and reaches the Final Report.

## B6 — Final review

1. Build the whole-change package: `github`,
   `superbuild.sh package <leaf plan> <MERGE_BASE> HEAD` with MERGE_BASE the commit the branch
   started from; `none`, the compare of the Step 2 pre-task manifest against a fresh snapshot.
2. Dispatch BRANCH_REVIEWER with the package, the plan path, the full acceptance agreement and
   this leaf's assigned IDs, `[PROTECTED_PATHS]` (as in B4.1), every `deferred`, `minor (deferred)` and `parked` ledger line, and —
   as `[UNREVIEWED_TASKS]` — each `review: branch` task with its brief path, report path and
   commit range. Those tasks have had no reviewer: the branch reviewer checks each against its
   brief. Ledger `Final review: dispatched`.
3. Filter by confidence as in B4.3. If high-confidence Critical or Important findings remain, or a
   deferred item is marked must-fix, run **fix wave 1**:
   - Write the complete list, each finding verbatim, to `<dir>/final-findings-1.md`, and ledger
     `Final review: fix wave 1/2 started (from <base7>)` — the head the review saw (in `none`, the
     snapshot it was built from).
   - Dispatch **ONE** FIX_APPLIER with that file — not one fixer per finding — then exactly one
     RE_REVIEWER over the fix range.
   - Write what the re-review leaves open — unresolved findings, new high-confidence
     Critical/Important breakage in the fix diff, and any must-fix deferred item still unfixed —
     verbatim to `<dir>/final-findings-2.md` (an empty file if nothing is open), then ledger
     `Final review: fix wave 1/2 (<X> addressed, <Y> open — <one-liners>; <base7>..<head7>; open: final-findings-2.md)`.
4. **A second wave, once, for residuals that are only implementation defects.** If
   `final-findings-2.md` is not empty, run one more wave only when **every** entry in it passes
   all three tests:
   - **No commitment moves.** Fixing it changes no approved acceptance row, Global Constraint,
     contract ID or revision, and not the stage's scope.
   - **The fix is determinable.** It follows from the plan's commitments without a ruling on a
     load-bearing conflict — an ordinary defect, or the plan's body failing its own commitments
     (B5).
   - **The wave converged.** The first wave addressed at least one finding, and
     `final-findings-2.md` lists strictly fewer findings than `final-findings-1.md`. A wave that fixed
     nothing, or that left as many findings open as it was given, did not converge.

   Then ledger `Final review: fix wave 2/2 started (from <base7>)`, dispatch **ONE** FIX_APPLIER
   with `final-findings-2.md` and exactly one RE_REVIEWER over the second fix range, write what is
   still open to `<dir>/final-findings-3.md`, and ledger `Final review: fix wave 2/2 (…)` in the
   same form. If any entry fails a test, skip the second wave. There is no third wave: write a
   **cap summary** (B5) for whatever is still open to `<dir>/cap-summary-final.md`, then adjudicate
   it under B5 (a residual load-bearing finding is BLOCKED).
5. **Resuming an interrupted wave.** When the ledger's last line is
   `Final review: fix wave <W>/2 started (from <base7>)`, the wave is neither spent nor to be
   started over: re-dispatch its FIX_APPLIER with `final-findings-<W>.md`, telling it that earlier
   work on these findings may already be in the workspace and to finish what is missing; then
   dispatch the RE_REVIEWER over `<base7>..HEAD` — the whole wave, not only the new work — and
   write the wave's closing ledger line. An interrupted wave counts once.
6. Ledger `Final review: clean | <K> parked`.

## B7 — Hand back to superrun

Return to superrun Step 3 with:

- the outcome — complete, BLOCKED with the B5 packet (and the cap summary when a cap ended it), or
  CHECKPOINT with the ledger path and the next step (B4.6);
- **every** ledger line containing `Ruling:`, in the order made, each with what it costs if wrong —
  this list is exhaustive and is the only place decisions taken on the user's behalf reach them;
- the deferred and parked items the final review left standing;
- the review depth actually applied: how many tasks had their own review, how many were reviewed at
  branch level only, and any upgrades;
- the review range (`<MERGE_BASE>..<HEAD>`, or the manifests in `none`).

Leave the scratch directory in place: a BLOCKED recovery or a post-CI resume in a fresh process
reads the rulings and progress from the ledger. superrun Step 5 removes it once the leaf is
integrated and closed out.

| Thought | Reality |
|---|---|
| "I'll fix this one-liner myself" | NO. Controller fixes skip review and pollute your context. Dispatch the fixer. |
| "The fix was small, skip the re-review" | NO. Every round ends with a scoped re-review. |
| "This finding is obviously wrong, I'll drop it" | NO. Adjudicate only at the cap, and ledger the ruling. |
| "One more round will converge" | NO. Past five rounds the failure is structural — adjudicate under B5. |
| "A later task depends on this, but I'm fairly sure of the answer" | NO. Load-bearing is BLOCKED; your confidence is not the test. |
| "The plan says 'exactly this content', and that content fails acceptance — BLOCKED" | NO. Acceptance is the authority; the body is the defect. Fix it under a ruling. BLOCKED is for commitments that must change. |
| "It's only an ambiguity — I'll stop and report to be safe" | NO. A minor conflict nothing consumes gets a ledgered ruling; a parked loop costs a tick. |
| "This task is small, I'll mark it `branch`" | NO. Size is not a criterion. If a later task consumes it, or you cannot tell, it is `task`. |
| "The review plan said `task`, but the diff turned out trivial — skip it" | NO. A `task` classification is never lowered. |
| "Ledger bookkeeping is overhead" | NO. It is what survives compaction and a CI-PENDING resume. |
| "I'll commit this timing hook so CI can tell us more" | NO. Diagnostic tooling stays in scratch or on a throwaway branch; the stage's PR carries only what its scope names. |
| "The cap is reached — report BLOCKED and stop" | Write the cap summary first: what was tried, why it did not land, the smallest change that would close it. |
| "Only 15 minutes left, but this task is small — start it" | NO. Below the margin, return CHECKPOINT. A killed dispatch loses the work; a checkpoint keeps it. |

---

The task loop is adapted from the superpowers plugin's `subagent-driven-development` skill
(MIT, Copyright (c) 2025 Jesse Vincent).
