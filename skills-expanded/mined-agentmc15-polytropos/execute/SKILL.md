---
name: execute
description: Run an execution kit from /polytropos:architect — dispatch each task to its pinned agent, verify it yourself, record the ledger, escalate what blocks. Use when the user says to execute, continue, or resume a kit or plan. Args: the kit slug (optional if one kit is active). Not for planning; that is /polytropos:architect.
---

# Kit execution loop

You are the orchestrator, running on the daily-driver model. The expensive thinking is already done — your job is faithful dispatch, verification, and state-keeping. Do not re-litigate the plan.

## Setup

1. Locate the kit: `.claude/kits/<slug>/` (from args, or auto-detect the single kit with pending tasks; if several, ask which).
2. Read `PLAN.md` (goal, constraints, tripwires), the kit's `GUARDRAILS.md` when present (kit-scoped fences — binding for every task in this kit, and passed along to implementers by reference), and `TASKS.md`. This Setup read is the FIRST read of the fences, not the only one — see **Re-reading the fences — phase starts guaranteed, compaction best-effort** below. Read the autonomy dial once here: an explicit user instruction at invocation ("execute <slug> autonomously" / "advisory") wins for this run, else PLAN.md's optional `autonomy:` line (`advisory` or `auto`), else `advisory` (see `references/rerouting.md`). Also read PLAN.md's optional `budget:` line once here (see **Budget dial — optional dispatch/escalation/consult cap** below) — absent means unbounded, today's behavior — and its optional `roles:` line once here too (see `references/roster.md`) — absent means the standing trio, today's behavior.
3. If the target project is aesop-managed (`aesop.yaml` at its root, or an `<!-- aesop:begin` fence in `CLAUDE.md`/`AGENTS.md`): treat those compiled files as read-only. Any guardrail change a task needs goes into `aesop.yaml` (`primitives.instructions.blocks`) followed by `aesop compile` — never a hand-edit of a fenced file. Kit files (`PLAN.md`, `TASKS.md`, `NOTES.md`) and kit-prefixed agents are outside aesop's management and are updated normally.

## Operating rule — lean driver

Your own context is the single most expensive artifact of the run — it is priced, cached,
and re-sent on every subsequent turn, and every inline read brings compaction closer. Take
minimal actions:

- Read only kit state — PLAN.md, GUARDRAILS.md, TASKS.md, NOTES.md — plus the output of verify
  commands you run. Do not inline-read source files, implementer diffs, or logs to "get oriented".
- Delegate every exploratory read, grep, and "what does this file look like now" question to
  a cheap scout subagent (Agent tool, `model: haiku`) that returns a few-line conclusion —
  never file dumps.
- Delegate independent verification the same way (the kit's verifier agent): you consume
  verdicts, not evidence dumps.
- You still run each task's verify command yourself — its exit status is orchestrator-owned
  evidence — but keep only the decisive tail of long output, and hand failure investigation
  to a scout instead of digging inline.
- Keep NOTES.md terse: outcomes and learnings, never transcripts.

Default posture: delegate and monitor. You touch files directly only to keep TASKS.md and
NOTES.md state current.

## The loop

Before the first dispatch, run `python3 ${CLAUDE_PLUGIN_ROOT}/bin/kit_contract.py graph --kit .claude/kits/<slug>` (absolute path first; fall back to relative to this SKILL.md). Exit 2 means a duplicate id, unknown or self dependency, or cycle, each named with its fix: fix TASKS.md and report the defect; never route around an invalid plan. Exit 0 reports the state (`ready` + frontier, `interrupted` + the task to resume, `waiting` + the blocked task, `complete`). Then `python3 ${CLAUDE_PLUGIN_ROOT}/bin/kit_contract.py roster --kit .claude/kits/<slug>`: exit 2 means an out-of-grammar `roles:` or `workflow:` line — fix PLAN.md first; otherwise it prints the workflow, the roles you sequence at the hooks in `references/roster.md`, and the assurance the kit declares (independent review stays binding unless the workflow is `direct`). Then `python3 ${CLAUDE_PLUGIN_ROOT}/bin/kit_contract.py analyze --kit .claude/kits/<slug>`: exit 3 names a verify the drivers cannot read — fix TASKS.md or stop, and either way record its `defect:` line with `when=pre-run`; exit 0 may still list missing tools and paths, which the spec review adjudicates. Then, unless `roster` reported `workflow=direct` (that kit opted out of independent review: write one NOTES.md prose line saying the P0 spec review was skipped, and why), and when NOTES.md holds no `reviewer: P0` line yet, dispatch the spec review per `references/spec-review.md` and adjudicate it before step 1 of the first task.

For each task in order (skip `done`, stop at `blocked` deps):

1. **Mark** it `in-progress` in TASKS.md.
2. If PLAN.md declared a **Budget dial** (below), check it FIRST — a cap already reached stops here, before dispatch. Otherwise, **Dispatch** to the kit's implementer agent, passing the task's `model` value as the Agent tool's `model` parameter — that parameter overrides the agent's frontmatter default, so the task's pin wins. If the kit has no implementer agent, use the Agent tool directly with that model. Pass the task's self-contained brief verbatim plus nothing else — the brief is designed to be sufficient. Do not pad it with your own interpretation. Choose the dispatch mode per `references/dispatch-modes.md`. When a logged `mode=applied` re-route covers this task, pass the upgraded alias as the `model` parameter instead — the task's `model` field stays the dispatch default and is never rewritten (see `references/rerouting.md`).
3. **Verify independently**: run the task's verify command yourself, and for non-trivial tasks also dispatch the kit's verifier agent (fresh context, adversarial). The implementer's claim of success is not evidence. Stay lean while verifying (see **Operating rule — lean driver**): take the verifier's verdict, not its evidence dumps. Honour the task's `evidence:` field (`red-green` when absent): for a `red-green` task the check must have been able to fail before the work — if it already passed on the pre-task tree, the required proof failed and the task is **blocked, not done**, whatever the command exits now. For `regression` / `precondition` tasks a pre-existing pass is the expected result and is not a defect.
4. **On pass**: mark `done`, note anything learned that later tasks need (append to a `NOTES.md` in the kit dir), and append the task's `outcome:` line (grammar in `references/ledger.md`). Then, right after the status flip and that line, record the acceptance for freshness with ONE call, `python3 ${CLAUDE_PLUGIN_ROOT}/bin/kit_contract.py accept --kit .claude/kits/<slug> --task <id> --run <run-id>` (the same `run=` id you stamp on the outcome line): it binds the tree as it is when it runs, reads that line, writes the artifact versions outside the tree, and exits 2 with the reason when the line is missing, from another run, or more than a day old — keep only its one stdout line. If it exits 2, note the reason in NOTES.md prose and carry on; never add or edit an `outcome:` line to satisfy it. A fresh outcome line is a fresh signal — consult **Live re-routing — upgrade-only, autonomy-gated** below before the next dispatch.
5. **On fail**: retry once, giving the implementer the failure output. If it fails again, mark `blocked` with the failure details, append its `outcome:` line (`result=blocked`), and move to the next independent task.
6. **Phase boundaries**: when TASKS.md marks a phase end, dispatch the kit's reviewer agent (opus) to check the phase against PLAN.md before continuing, then adjudicate its findings and append the phase's `reviewer:` line (grammar in `references/ledger.md`). Every phase end is also the next phase's start: before step 1 of that phase's first task, re-read the fences (see **Re-reading the fences — phase starts guaranteed, compaction best-effort** below).

Run parallel dispatches for tasks TASKS.md marks as independent — one message, multiple Agent calls.

## What binds, what adapts

Binding, whatever the run looks like: the kit's fences (`GUARDRAILS.md` and PLAN.md's out-of-scope section), each task's brief and acceptance, the `evidence:` rule, the budget dial, the graph and roster checks, and the ledger grammar whenever you write a NOTES.md line — including this rule: **always backtick the six machine-read tokens** (`outcome:`, `agent:`, `reroute:`, `session:`, `reviewer:`, `defect:`) when you quote them in NOTES.md prose, because a line that merely starts with one parses as real data whether it is plain, bulleted, or indented. Suggestions you adapt to the repo in front of you: the lean-driver practices, warm-cluster dispatch, how much of a verify output to keep. Bounded adaptation: when repository reality changes a proposed approach (a helper lives elsewhere, a convention differs), adapt the approach and say so in NOTES.md; never change a task's scope or acceptance criteria to make it pass — that is the architect's call, recorded as a `defect:` line and a stop-and-report.

## Re-reading the fences — phase starts guaranteed, compaction best-effort

Constraints are the first content compaction erases: the kit's `GUARDRAILS.md` and PLAN.md's
out-of-scope fence are read once at Setup and contribute nothing to any later turn's output,
so a context rewrite drops them long before it drops the code you were just editing — and
accumulation does the same job slowly, as a carry-forward warning gets buried in a NOTES.md
that has grown past what anyone re-reads. So **re-READ the fences from disk; remembering them
is the part that fails.**

Two anchors, and they are NOT equally strong. Say which one you are honoring rather than
implying the finer one:

- **Every phase start — a guarantee.** Before dispatching the first task of each phase
  (including phase 1, right after Setup), re-read the kit's `GUARDRAILS.md` and PLAN.md's
  constraints/out-of-scope section from disk. A phase boundary is marked in TASKS.md, so you
  can always detect it: this anchor is unconditional, and no phase begins on remembered
  fences. These two small kit files are kit state, which the **Operating rule — lean driver**
  posture above reads directly rather than delegating — never hand this read to a scout, and
  never let "I read GUARDRAILS.md at Setup" stand in for it.
- **Any point you observe your context was compacted — best-effort.** This skill cannot
  detect compaction: nothing notifies the loop when a rewrite happens, so this anchor fires
  only when you happen to notice the evidence (a summarized transcript, earlier detail you
  can no longer see, a compaction notice in your own context). Treat it as an opportunistic
  extra, never as coverage — if compaction lands mid-phase and you miss it, the phase-start
  re-read above is what catches it.

The coarser guarantee is deliberate: an honest phase-boundary rule the loop can always honor
beats a compaction-triggered one it would only appear to honor.

## Escalation valve — blocked tasks go back to Fable, one at a time

When a task is `blocked` after retry, offer (or, when the autonomy dial is `auto`, do without pausing to ask — see `references/rerouting.md`) a **targeted Fable consult**: dispatch a subagent with `model: fable` carrying only that task's brief, the failure evidence, and the relevant PLAN.md excerpts. Ask it to either fix the task directly or rewrite the brief so the implementer can. This keeps Fable spend proportional to genuine difficulty — you never pay Fable prices for routine execution. When the consult unblocks the task, record `result=escalated-pass` (with the consult's model) in its `outcome:` line.

## Budget dial — optional dispatch/escalation/consult cap

PLAN.md may declare an OPTIONAL `budget:` line — a PLAN.md line family exactly like `autonomy:`, **never a task field**, read once at Setup:

    `budget: max-dispatches=N max-escalations=N max-consults=N`

Any subset of the three keys may appear, in any order. Absent block = today's behavior everywhere: unbounded, no check performed. All four headless drivers (`bin/claude_execute.py`, `bin/copilot_execute.py`, `bin/codex_execute.py`, `bin/cursor_execute.py`) honor the SAME block under the same names — see their "PLAN.md budget dial" docstring sections — and this loop honors it identically, so a kit behaves the same whether it is run interactively or through a driver.

**What the three keys count, in this loop's dispatch model:**

- `max-dispatches` — every implementer/retry Agent-tool dispatch this run makes, across every task (the same `attempts=` figure already recorded on each task's `outcome:` line).
- `max-escalations` and `max-consults` — in this skill's loop, both count the SAME event: an invocation of the **Escalation valve** (the Fable consult). Unlike the headless drivers — which distinguish an in-ladder tier-walk within one task's own dispatch (`max-escalations`) from a separate `--parent` invocation spawned to rescue a DIFFERENT task (`max-consults`) — this loop has no in-ladder tier walk of its own; its only escalation mechanism IS the consult. So a kit whose PLAN.md sets either key (or both) caps the same thing here: how many Fable consults this run may make.

**Checking the cap:** before each dispatch (step 2 of the loop) and before each Escalation-valve consult, recompute usage the SAME way the drivers do — by scanning NOTES.md's own recorded `outcome:` lines (this session's own lines included, since they are already appended to NOTES.md by the time the next task is considered): sum `attempts=` for `max-dispatches`, sum `(attempts - 1)` per line for `max-escalations` except on `result=retry-pass` lines, which count none (a same-model retry is a dispatch, never an escalation), count lines carrying `parent=` for `max-consults`. This makes the check work identically whether the kit is being run fresh or resumed in a later session — NOTES.md, not an in-memory counter, is the source of truth, exactly as it is for the outcome ledger itself.

**On reaching a cap:** stop cleanly, right there — do not dispatch (or do not make the consult). Leave the task's status exactly as found (pending stays pending; do NOT mark it `blocked` — a budget stop is not a verdict on the task). Append ONE `outcome: <task-id> model=<pin or unpinned> attempts=0 result=budget-stop review=none run=<run-id>` line to NOTES.md (generate a fresh `run=<UTC-date>-<4 hex>` id for this line if you have not already stamped one on an earlier line this session). State plainly in your end-of-run report which cap was hit, its used/cap counts, and how many tasks are left untouched — **never fold this into a fluent "all done" summary**; a budget stop that reads like a normal finish is exactly what this dial exists to prevent. Then STOP dispatching for the remainder of this run (do not skip ahead to a later independent task — the budget is kit-wide, not per-task).

**Never write a budget-stop line for a task that already carries a verdict.** If the task the cap stopped you on already has an `outcome:` line recording `pass`/`retry-pass`/`escalated-pass`/`blocked` (resuming an already-`blocked` task after the budget is spent is the ordinary case), report the stop in your end-of-run summary but append NO ledger line for it. A `budget-stop` is not a verdict, and later lines for the same task id normally win, so writing one would erase a real result — and its `failure=` class — from the kit card and from `--history`. `bin/routing_scorecard.py` now refuses to be overwritten this way (it keeps the verdict and notes the dropped budget-stop) and all three drivers decline the write for the same reason; do not hand it a line it has to ignore.

## References — read when

- `references/ledger.md` — read when you append any `outcome:`, `agent:`, `reviewer:`, or `defect:` line: the six-family grammar, every field, and the counting and adjudication rules.
- `references/dispatch-modes.md` — read when a phase holds a serial same-file chain and you are choosing between fresh fan-out and a warm sidekick.
- `references/rerouting.md` — read when an `outcome:` line lands and `routing_scorecard.py <slug> --live` prints a recommendation, or when the kit's autonomy dial is `auto`.
- `references/roster.md` — read when PLAN.md declares a `roles:` line: hook points, consequence rules, the `marginal=` field, and the pipeline order.
- `references/spec-review.md` — read when a kit has no `reviewer: P0` line yet: the pre-dispatch spec review's prompt, adjudication, and recording.

## End of run

Report: tasks completed / blocked / remaining, verify results (with output, faithfully — failures stated plainly), and NOTES.md additions. If everything is done, run the plan's overall "done" check from PLAN.md and state the result. Then record this run's session id for the cross-kit routing history: append ONE `session: <session-id>` line to NOTES.md, where `<session-id>` is the filename stem of this session's transcript — the transcript that is still being WRITTEN right now — resolve it by write recency across the whole projects tree, not by a path-derived slug: `ls -t "$HOME/.claude/projects"/*/*.jsonl | head -1`. Do NOT derive the projects dir from `pwd`: a session that STARTED in a different directory lives under the slug of where it started, so a `pwd`-derived lookup silently returns some OTHER session's transcript. That failure mode is the dangerous one — it does not error, it returns a plausible wrong id, and the guard below never fires. Sanity-check the candidate before recording it: a live session's transcript has an mtime within a minute or two of now and is large (megabytes by the end of a kit run); a few-kilobyte file last written hours ago is a different session, so discard it and skip the line. The lookup is read-only and best-effort, and the line is OPTIONAL: if nothing passes the sanity check, or two candidates are plausibly live, skip it — the history degrades to quality-only for this kit; never record a guessed id. A resumed kit appends one `session:` line per run (the history sums a kit's sessions and dedupes ids shared across kits). Finally, offer the routing-quality scorecard: `python3 bin/routing_scorecard.py <slug>` (first-try pass rate, model mix, cheap-model review survival, and — with `--session` — dollars vs an all-frontier counterfactual) and the cross-kit track record: `python3 bin/routing_scorecard.py --history` (per-tier quality across every kit, plus aggregate dollars over the kits that carry a `session:` line, plus per-role quality), and — when this run recorded `agent:` lines — the per-task dollar breakdown: `python3 bin/routing_scorecard.py <slug> --session <session-id> --by-task` (delegated cost per task by role — implementer/verifier/escalation; a warm cluster's shared transcript is attributed to the cluster as a unit, and the orchestrator's own share is one un-split line, never divided per task), and — when this run recorded extended-role `agent:` lines — the per-role value table: `python3 bin/routing_scorecard.py --roles` (dispatches, findings, confirmed, marginal, precision, marginal rate, and dollars only where transcripts priced them, with "insufficient sample" below the evidence floor).

## Optional context travel

When an explicit repository/kit/assignment and authorized startup config are supplied, use the native `context-travel` skill and read `${CLAUDE_PLUGIN_ROOT}/docs/CONTEXT-TRAVEL-SURFACES.md` (or resolve relative to the skill file) on demand for a bounded task brief. Treat missing, stale, partial, or refused context as advisory; retain this workflow's authoritative sources, policy, pricing, permission, and mandatory verification rules. If no authorized context transport is available, continue this workflow and report context unavailable.
