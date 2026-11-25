---
name: run
description: Start an unattended run on an approved plan, in a project that has a .foreman.toml. Takes a plan file, or several plan files to run as a chain one after the other, and optionally the units to run; with no units it runs everything from each plan's resume point to the end. Use when the user says "run W8 to W10", "run this plan", "start a run", "work through these units unattended", or invokes /foreman:run.
---

# Foreman run

A run tells the stop gate to keep you working through the named units instead of stopping to ask what comes next.

## Start

A run is best started in a fresh session (quit and start `claude` again, or `/clear`, then `/foreman:run`): everything already in the session is carried through the whole run. Clearing before the start is safe; the run binds to a session only when it starts. Never `/clear` during a run: it starts a new session the run is not bound to.

1. Run the doctor: `uv run --no-project --python 3.12 "${CLAUDE_PLUGIN_ROOT}/hooks/doctor.py" --cli`
   If it prints anything except `foreman: ok`, show the output and stop. Never start a run while Foreman is weakened.
2. Take the plan file from the user's message. Ask only if it is missing. Several plan files make a chain: they run in the order given, in this one run.
3. Work out the units:
   - If the user named units, use those.
   - If not, read the plan, find its resume point, and take every unit from there to the end of the plan, in plan order. In a chain, do this for each plan. Tell the user in one line which units that is, then carry on without waiting for an answer.
4. Start the run from the project root:
   `uv run --no-project --python 3.12 "${CLAUDE_PLUGIN_ROOT}/hooks/run.py" start --plan <plan file> <unit> <unit> ...`
   For a chain, repeat `--plan` for each plan, in order: `start --plan <first plan> <unit> ... --plan <second plan> <unit> ...`
   If the user asked for a plain run, add `--plain` before `--plan`. A plain run skips the simplify pass; the doctor repeats this at every session start and after compaction.

## Work

Follow the run contract that `run.py start` printed; it applies until the run ends, and the doctor repeats it after compaction. Each unit gets a fresh subagent, so your own context only grows by a report per unit. Work natively only if the plan says so.

For each unit, in plan order:

1. Hand the unit to a subagent (general-purpose). Never start the next unit's subagent before this unit is committed: units share one working tree, so they never run in parallel. Its brief is the only context it has, so give it:
   - the unit's section of the plan, verbatim, and the plan file's path
   - the working directory and branch
   - the decisions log's path, and the rule: a choice cheap to undo, make it and add one line there; a choice expensive to undo or client-facing, do not make it, report it back
   - not to commit, push, or edit the plan file, the decisions log or the parked file: those are yours
   - to run /simplify on its changes before reporting (leave this out in a plain run)
   - for a frontend change, to open the changed screen in a browser and save a screenshot to `.foreman/walkthrough/`
   - to report back briefly: files changed, decisions logged, anything it could not decide, check output if it ran it
   - the local ports tunnels hold, if `run.py start` listed any, and the rule: check a localhost port is free before a test or service uses it

   Claude Code runs the subagent in the background and returns at once. End your turn with one line ("Task 3 is with a subagent") and wait: its report wakes you, and the stop gate lets a stop through while a subagent you launched is still working. Do not poll its output file, do not wait with `sleep`, and do nothing else in the working tree meanwhile.
2. Read the report when it arrives. Add anything it could not decide to the parked file.
3. Run the project's check command (it is in `.foreman.toml`). If it fails, send the failure back to the same subagent, or fix small things yourself.
4. Commit, update the resume point in the plan file, push the working branch.

Do not run /foreman:init or edit `.foreman.toml` during a run, even when the doctor says the audit is stale (a unit that adds build files makes it stale). Note it for the hand-back; the user re-runs init and approves it once, after the run.

When the stop gate tells you to continue, continue. Do not run `run.py stop`: the run ends by itself when your final message opens with `Run complete:`.

## Chains

- Work the plans in order. Start the next plan when the current one is complete, or when everything left in it is parked. If the current plan ends blocked (a failing check you cannot fix, `Blocked on you:`), stop there: do not build the next plan on top of it.
- Branches are stacked: each plan after the first branches from the tip of the previous plan's branch, not from `main`, whatever the plan's own branch step says. Merging into a protected branch is the user's job, never the run's.
- A plan's build-file changes make the audit stale; that goes in the hand-back like any other stale audit.

## Hand-back

Open the final message with `Run complete:`, `Blocked on you:` or `Decision needed:`, then give:

- units done, with commit hashes (in a chain, one section per plan)
- decisions you made (they are in the decisions log)
- questions parked (they are in the parked file)
- check status
- Foreman follow-ups (for example: audit stale, re-run /foreman:init)
- for a chain: each plan's branch, and for every plan after the first the command that moves it onto `main` once the previous one is squash-merged: `git rebase --onto main <previous branch> <this branch>` (re-lock and run the check if a lock file conflicts)
- what you need from the user
