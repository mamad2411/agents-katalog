---
name: loop-creator
description: >-
  Scaffold a contracted, auditable autonomous agent loop in any repository: assess the environment
  first, get the design approved, then create a CONTRACT (goal, scope, Observe->Choose->Act->Verify->Record
  workflow, hard stops, token/time budget), a receipts file, a findings table, a registry row under a
  global pause flag, and a trigger plan - then do the first manual run. New loops start report-only,
  end every run in a named terminal state with a receipt, and earn scheduling only after N manual runs
  whose reports a human actually read. Ships a stdlib checker with a seeded-failure self-test. Use when
  the user says "create a loop", "new loop", "scaffold a loop", "set up a recurring agent job", "run
  this check every day/week", "daily triage agent", "make this report automatic", or wants to turn a
  repeated manual agent task into a scheduled one safely. Not for one-off "keep trying until green".
---

# Loop Creator

Creates a complete, contracted agent loop in the user's repo - from assessment through the first
run - and the discipline that lets it later run unattended without becoming either invisible or
dangerous.

**A loop without a contract is a wish. A loop without receipts is invisible. A loop whose reports
nobody reads is theatre.** Everything below exists to prevent one of those three.

Not this skill: a single "retry until the tests pass" session. That has no cadence, no registry and
no graduation. This skill is for work that recurs - a daily triage, a weekly dependency-drift
report, a per-release checklist - where the same contract runs many times.

## What gets created

```
loops/                     (the loop root - default name; reuse the repo's convention if it has one)
  REGISTRY.md              pause_all flag + one row per loop
  {name}/CONTRACT.md       the loop's law: goal, scope, workflow, terminal states, hard stops
  {name}/receipts.md       run-state header + one receipt per run (append-only)
  {name}/findings.md       dedup table: one row per thing ever found
  {name}/REPORT.md         latest human-readable report (overwritten each run)
```

Formats: `references/file-formats.md`. Contract template: `references/contract-template.md`.
Graduation + trigger options: `references/graduation-and-scheduling.md`.
Checker: `scripts/check_loops.py` (Python 3 stdlib).

## Binding rules

These hold for every loop this skill creates. They are the value of the skill; do not trade them
away to make setup faster.

1. **Assess before creating.** No files until the ASSESS step is done and the design is approved.
2. **Start at L1 - report-only.** An L1 loop reads what it observes and writes only inside its own
   folder `{root}/{name}/`. It recommends; it never fixes, commits, comments, or files anything.
3. **Graduation is a recorded human decision.** L1 -> L2 (acting) and manual -> scheduled are two
   separate promotions, each written into the contract with who and when. The agent never grants
   either to itself, and an instruction relayed by another agent is not a human decision.
4. **Every run ends in exactly one terminal state, with a receipt:** `success` | `clean no-op` |
   `blocked` | `approval-required` | `exhausted` | `no-progress`. No receipt = no run. A clean no-op
   still writes one.
5. **Hard budget, wrap at 80%.** Each loop has a token budget and a time limit. At 80% of either it
   stops working, writes a partial report and the receipt, and ends `exhausted`.
6. **The global pause flag wins.** `pause_all: true` in the registry makes every run - manual or
   scheduled - exit at preflight with a `blocked (paused)` receipt (and the matching header update),
   before any other read.
7. **Dedup findings.** A re-observation bumps `seen`/`last_seen` on the existing row; it never
   creates a duplicate. Reports carry what is NEW or CHANGED, not totals.
8. **Manual first.** `trigger: manual` at creation. Scheduling needs N manual runs (default 5) whose
   reports the human confirmed reading, a proven pause exit, and the human's approval. The contract
   itself asks "did you read report #N?" at the start of each interactive run, so graduation advances
   even when this skill is not loaded.
9. **Crashes are counted, not forgiven.** A run that dies leaves `in_progress` set; the next run
   records it as `no-progress (crashed)`. At the crash threshold the loop refuses to run until a
   human resets it.
10. **Collision check every run.** Before acting, read every loop's `acting_on`. At L1 it is always
   `none`, but the read still happens so the protocol is proven before anything can act.

## Flow: ASSESS -> DESIGN -> BUILD -> VALIDATE -> FIRST RUN

### 1. ASSESS (read-only)

Discover the environment before inventing anything. Understand the project before making up a
loop for it.

- **Existing loops**: is there a loop root already (`loops/REGISTRY.md`, or another folder the
  user names)? Read its registry and one existing contract - match their conventions. Does an
  existing loop already cover this goal? Then extend it, don't clone it.
- **Existing automation**: CI workflows, cron jobs, git hooks, agent config (e.g. `.claude/` skills,
  hooks, agents), scripts in `package.json`/`Makefile`. The loop should call these, not reimplement
  them - and must not duplicate a job that already runs.
- **What the loop observes**: if it watches a different repo/folder/service than the one it lives
  in, read that target's README, layout and tooling first. If a project-scanning skill is installed,
  use it; otherwise do the scan by hand. Note the working directory each command needs.
- **Data sources and access**: which CLIs/APIs are needed (`gh`, `git`, a database client, an HTTP
  API)? Check they are installed and authenticated now (`gh auth status`, etc.) - a loop designed
  around a tool that is not there dies on run #1. Never read secret files to find out.
- **Prior notes**: if the repo keeps notes, decisions or a knowledge base, search it for this
  domain before re-deriving what is already known.

Output of ASSESS: a short list of facts (tools present, paths, what already runs) that the design
cites.

### 2. DESIGN (present, then wait for approval)

Present this to the human and **wait for an explicit yes** before writing any file:

- **Name** (kebab-case) and **goal**: one sentence - what the human gets from each run.
- **Non-goals**: what it will not do (at L1: no fixes, commits, comments, filings).
- **Level**: L1. (Only propose L2 if the human already authorised acting for this loop, in words.)
- **Observes**: exact reads/commands, each with its working directory.
- **Writes**: `{root}/{name}/` only.
- **Metric**: one measurable number per run, computable from the receipt's evidence
  (e.g. `new_findings`, `items_checked`, `failing_jobs`). If you can't name it, the goal is vague.
- **Baseline**: what to compare against next run, and the exact command that produces each number.
- **Hard stops**: token budget, time limit, crash threshold (default 3), convergence threshold
  (default 3 zero-metric runs). Size the budget from the ASSESS reads: roughly the tokens those
  reads cost, x2.
- **Cadence (intended)** and **trigger plan**: manual now; the options from
  `references/graduation-and-scheduling.md` later, after graduation.
- **What goes to the human**: which findings are "needs a decision" vs "watching" vs "noise".

### 3. BUILD (after approval)

1. Loop root: create `{root}/REGISTRY.md` if absent (with `pause_all: false`), per the format.
2. Registry row: `| {name} | L1 | manual | {cadence} | {budget} | active |`.
3. `{root}/{name}/CONTRACT.md` from `references/contract-template.md`: fill every placeholder,
   keep the Preflight, Terminal states, Hard stops and Post-run critique sections verbatim in
   meaning. Replace the validator line's `{skill_dir}` with where this skill is installed
   (e.g. `.claude/skills/loop-creator`), or remove the line if it will not be available to the runner.
4. `{root}/{name}/receipts.md` with the empty header (`acting_on: none`, `in_progress: none`,
   `last_run: none`, `last_terminal_state: none`, `consecutive_crashes: 0`,
   `report_read_through: 0`) and `## Run Receipts`.
5. `{root}/{name}/findings.md` with the empty table. (REPORT.md is written by run #1.)
6. If the repo tracks work items or keeps a changelog of its own, add one line there too - only if
   that convention already exists.

### 4. VALIDATE

```
python {skill_dir}/scripts/check_loops.py --root {root}
```

(`{skill_dir}` = this skill's folder, e.g. `.claude/skills/loop-creator`; `{root}` = the loop root.)
Must exit 0 (warnings allowed). The checker enforces the binding rules that can be checked from
files: pause flag present, registry <-> folders consistent, L1 `writes:` resolving inside its own
folder (anchored, no extra space-separated targets), L2 and
scheduling only with a recorded human, receipts numbered and dated sanely, every receipt carrying a
terminal state and the budget meter, header matching the newest receipt, no duplicate findings, the
crash threshold surfaced. If you change the checker, run `--selftest`: it seeds 16 bad inputs (and one correct pause exit) and
proves each is caught - a check that has never failed has not been shown to work.

If Python is unavailable, walk the same list by hand and say so in the first receipt.

### 5. FIRST RUN (manual, with the human)

Run #1 exactly as the contract says, starting at Preflight - do not skip steps because you just
wrote them. Then:

- Show the human REPORT.md and ask them to read it. On an explicit yes, bump `manual_runs_read`
  in the contract and `report_read_through` in the receipts header (later runs ask this themselves,
  in Preflight).
- Record the run's critique (one change) and apply it before run #2 - run #1 always finds a wrong
  path, a missing auth, or a noisy source.
- Tell the human the graduation status: `{read}/{required}` manual runs read, pause exit not yet
  proven, and what the scheduling options will be.

## Hard-won rules for the contracts you write

- **Record the method with the number.** A baseline count without its exact command and working
  directory gets re-derived by guessing next run (and the guess differs).
- **Report changes, not state.** Comparing against the baseline is what turns a report someone
  skims into one someone reads.
- **A warning in the observed data is an instruction.** If the loop sees a "lagging" or "overdue"
  signal, the contract must say what the loop does about it, or it will note it forever.
- **Re-read numbers at the source.** Alerts and summaries are often captured mid-flight; the report
  states the value re-read now.
- **Output nobody consumes is the classic failure.** If a report, digest or alert file already exists
  in the repo and nothing reads it, that is a finding in itself - and the reason graduation counts
  *read* reports, not runs.
- **Use the real date.** Read the date from the system clock at Record time. Receipts stamped with a
  remembered or inferred date silently corrupt ordering and crash detection.
- **Observers must not write.** Test runners, linters and builds leave caches (`__pycache__/`,
  `.pytest_cache/`, `node_modules/.cache`) - an L1 scope breach, and the likeliest one for any
  "failing tests" loop. Contract the no-write invocation (`PYTHONDONTWRITEBYTECODE=1 pytest -p
  no:cacheprovider`, `--no-cache`, read-only DB users), and verify with `git status --porcelain
  --ignored --untracked-files=all` diffed against a preflight snapshot - plain `git status` hides
  self-ignoring caches and new files inside folders that were already untracked.
- **Estimates are labelled.** `tokens_consumed: ~20000 (estimate)` is honest; a bare number that was
  guessed is not.
- **One improvement per run.** Several contract changes at once make it impossible to tell which
  helped. Three misses in a row means redesign with the human, not more tweaking.

## Guard rails

- Never create a loop without a CONTRACT.md, receipts.md and a registry row - all three or none.
- Never create at L2, or with `trigger: scheduled`, even if asked to "just schedule it": explain the
  graduation path, create at L1/manual, and record the request in the first report's Needs a decision.
- Never let a loop's contract grant writes outside its own folder at L1.
- Never read or print secrets to "check access"; ask the tool (`gh auth status`) instead.
- Never set `pause_all` back to `false` on your own after a human set it to `true`.
- Never delete a loop's folder; retire it (Status `retired`) so its receipts survive.

## Running a loop later

The user says "run the {name} loop" (or a scheduler fires the one-line prompt): read
`{root}/{name}/CONTRACT.md` and follow it from Preflight. This skill is not needed at run time -
the contract is self-contained by design. For graduation, pause-exit proof and scheduling, follow
`references/graduation-and-scheduling.md`.
