---
name: autopilot
description: "Autonomous multi-phase loop over a plan.md — execute, lint/test, verify, and commit each phase."
disable-model-invocation: true
---

# Autopilot: Autonomous Phase Orchestration

You are the lead agent for autonomous multi-phase execution. You orchestrate a team of an executor and a reviewer through each phase of a plan: execute → lint/test → verify → commit → next phase.

## 1. Find the Plan and Discover Phases

Look for `plan.md` in the current directory, then `../plan.md`. If not found, ask the user.

Parse all phases from the plan. Each phase has a number, name, objective, and task list.

If the user specified a starting phase (e.g., `/autopilot 3`), skip phases before that number. Otherwise start from Phase 1.

## 2. Discover Test and Lint Commands

Check the project's CLAUDE.md plus any Makefile, package.json, pyproject.toml, or docker-compose.yml for test and lint commands. If you cannot determine them, ask the user once. Store them for reuse across all phases.

Typical patterns:
- Python: `pytest`, `ruff check .`
- Node/TS: `npm test`, `npm run lint`
- Django + Docker: `docker compose exec api pytest`, `docker compose exec api ruff check .`

## 3. Spawn the Agents

Spawn two named agents using the Agent tool (called Task in older Claude Code versions). Give each a `name:` so you can address it with SendMessage:

**Executor** (name: "executor", subagent_type: "general-purpose"):
> You are an execution agent. Read the executor agent definition in `.claude/agents/executor.md` (or `agents/executor.md`) for your role. You will receive messages assigning you phases to implement. For each assignment: read plan.md, find the phase, and implement all tasks. Do NOT enter plan mode — the plan is pre-approved. Do NOT commit. When done, send the lead a message summarizing what you implemented, files changed, and any deviations or concerns.

**Reviewer** (name: "reviewer", subagent_type: "general-purpose"):
> You are a review agent. Read the reviewer agent definition in `.claude/agents/reviewer.md` (or `agents/reviewer.md`) for your role. You will receive messages assigning you phases to verify. For each assignment: read plan.md, find the phase, and verify the implementation. Do NOT commit — the lead commits. Write the verification report to the project root's `docs/verification/phase-N-[name].md` (one level above the sub-project) and send the lead a message with the verdict (PASS, PASS WITH WARNINGS, or FAIL) and a summary of findings.

### Models and progress files

<!-- Maintainer note: this block is duplicated in skills/orchestrator/SKILL.md (§5). Change both when you touch it. -->

- **Executors and reviewers run on Opus.** Pass `model: "opus"` when spawning them. A model override the user gives for a task wins.
- **The lead runs the final review** (see Completion) on the session model. If the session model hits a usage limit or is unavailable, spawn a reviewer on Opus to do it instead, without asking.
- **Every teammate keeps a progress file** at `~/.claude/progress/<repo>/<agent-name>.md`, where `<repo>` is the basename of the git root. Add this to every spawn prompt:
  > Keep a progress file at <path>. After each meaningful step, overwrite it with: your assignment, what is done, what is next, and the files you touched. If you are restarted, read it first and continue from it.

  It lives outside the repo, so it never dirties the tree. Progress files plus commits are what let a plain "continue" resume after a reset.

Before the first assignment, record `git rev-parse HEAD` as the run's start sha, and write the run file `~/.claude/progress/<repo>/RUN.md`:

```
skill: autopilot
start_sha: <short sha>
status: running
```

Set `status: complete` once every phase has passed, and `status: stopped` if the run stops early. The optional `orchestration` hook profile reads this file: after a compaction or resume it tells you to reload the run, and once the run is `complete` it holds the final report until the combined check is recorded.

### Arm the watchdog

<!-- Maintainer note: this watchdog block is duplicated in skills/orchestrator/SKILL.md (§5). Change both when you touch it. -->

A subagent's completion arrives as a notification. A hung subagent sends nothing, and the lead waits in silence with no timeout. Before sending the first assignment, arm a stall watchdog with the Monitor tool so silence has a deadline. Run it from the repo root. Do not use a background Bash loop for this; those get killed.

Monitor with `timeout_ms: 1800000` (the cap), description `"autopilot watchdog: stall/commit events in <repo>"`, and this command:

```bash
STALL_MIN=10; INTERVAL=60; quiet=0
stamp=$(mktemp); head=$(git rev-parse HEAD 2>/dev/null)
while true; do
  sleep $INTERVAL
  now=$(git rev-parse HEAD 2>/dev/null)
  changed=$(find . -name .git -prune -o -name node_modules -prune -o -type f -newer "$stamp" -print -quit 2>/dev/null)
  touch "$stamp"
  if [ "$now" != "$head" ]; then echo "COMMIT ${now:0:8}"; head=$now; quiet=0
  elif [ -n "$changed" ]; then quiet=0
  else quiet=$((quiet + 1)); m=$((quiet * INTERVAL / 60)); [ $((m % STALL_MIN)) -eq 0 ] && echo "STALL ${m}m: no file or commit activity"
  fi
done
```

It emits `COMMIT <sha>` on each new commit and `STALL <n>m` after every ten minutes with no file changes and no commits. On the events:

- `COMMIT`: informational. Your own commits show up here too.
- First `STALL`: check every agent with TaskOutput. An agent that is still running but silent gets one SendMessage asking for a one-line status. A long test run or build can look like a stall, so confirm before acting.
- Second `STALL` (about 20 minutes) with no reply and no activity: send the stall push (see Heartbeat). If the agent died on a usage limit, recover it as Error Handling describes. Otherwise this is the timeout in Error Handling: stop and report. Never kill agents automatically.
- Monitor expiry (30 minutes): re-arm immediately if the run is still going. On completion, stop it with TaskStop.

### Heartbeat

<!-- Maintainer note: this block is duplicated in skills/orchestrator/SKILL.md. Change both when you touch it. -->

The user should never have to ask "status?" or "ETA?".

- **Status line** after every wave or phase, and in every report: `x/N done · <current step> · ETA ~<duration>`, for example `3/7 done · Phase 4 verifying · ETA ~35m`. ETA is the average time per completed unit times the units left. Before the first one lands, write `ETA ?`.
- **Push notification** with PushNotification, if the tool is available (load it with ToolSearch if it is deferred; skip silently if it does not exist). Keep each one under 200 characters. Send one:
  - at each phase or wave PASS or FAIL: `Phase 3 PASS · 3/7 done · ETA ~40m`
  - on a stall past ~20 minutes (the second watchdog `STALL`): `Stalled 20m in Phase 4 (executor silent) · 3/7 done`
  - at completion or any stop: `Done · 7/7 · 7 commits` or `Stopped at Phase 4: reviewer FAIL, needs you`

## 4. Create Tasks

Create all tasks upfront using TaskCreate with dependencies. For each phase create four tasks in sequence:
- Execute Phase N → Lint/Test Phase N → Verify Phase N → Commit Phase N

Each task is blocked by its predecessor. This provides progress visibility and supports resume.

## 5. Phase Loop

<!-- Maintainer note: this execute → lint/test → verify → commit loop is duplicated in skills/orchestrator/SKILL.md (§7b Phased Mode). Change both when you touch loop behavior. -->

Before executing each phase, run `git status`. If the working tree is dirty (uncommitted changes from a previous phase, a crash, or manual edits), stop and ask the user how to proceed — stash, reset, or commit — before continuing. A clean tree at each phase boundary keeps commits reviewable one phase at a time.

Durable state lives in per-phase commits, not in the in-session task list: if this session dies, the committed phases survive and you resume with `/autopilot N`, but the in-session tasks do not. Treat the last commit as the source of truth for where you are. If the user says "continue" after a reset, read the progress files in `~/.claude/progress/<repo>/` alongside `git log` to see where each teammate was.

For each phase (starting from the start phase):

### 5a. Execute
Assign the execute task to "executor" and send a message:
> Execute Phase N: [Name]. Objective: [objective from plan]. Implement all tasks for this phase. Do not commit.

Wait for the executor's completion report.

If the executor reports it is **blocked** or that the plan is stale/wrong (as opposed to "done, with notes"), pause immediately and escalate to the user. Do NOT proceed to lint/test — a blocked executor means the phase isn't implemented, and running checks on a half-done tree only produces confusing failures.

### 5b. Run Tests and Lint
Run the test and lint commands yourself. If any fail:
1. Analyze failures and fix simple issues (lint errors, imports, formatting) yourself
2. If still failing, send the executor a message describing what to fix and wait for the fix
3. Re-run checks after each fix attempt
4. **Stop after 3 failed attempts** — report to the user with full test output

### 5c. Verify
Assign the verify task to "reviewer" and send a message:
> Verify Phase N: [Name]. Implementation is complete and tests/lint pass. Review against the plan. Produce a verification report. Do not commit.

Wait for the reviewer's verdict.

### 5d. Handle Verdict

**PASS or PASS WITH WARNINGS:**
- Stage and commit all changes: `feat(scope): implement phase N — [name]`
- Include the verification report in the commit
- If the commit fails (hook rejection, nothing staged, git error): do NOT mark the phase complete. Surface the git error to the user and stop — the work is verified but uncommitted, and advancing would bury it.
- Log any warnings for the final summary
- Mark tasks completed, print the status line, send the PASS push (see Heartbeat), move to next phase

**FAIL:**
- Stop the loop immediately and send the FAIL push
- Report to the user: which phase failed, what the issues are, reviewer's recommendations
- Do NOT attempt to fix FAIL verdicts — they represent design or correctness issues needing human judgment
- Tell the user: fix the issues, then run `/autopilot N` to resume

## 6. Completion

After all phases pass:
1. Send both agents a final message that all phases are complete so they can wrap up, and stop the watchdog with TaskStop
2. **Final review and combined check**: set `status: complete` in the run file, then read `git diff <start-sha>..HEAD` yourself as a whole. Confirm each phase's accepted change is still present (a later phase can undo an earlier one while both reviews read clean), and look for what per-phase review misses: cross-phase inconsistency, duplicated helpers, leftover debug code, a plan goal no phase delivered. Run the project's lint/test once on the combined tree. Fix trivial issues in a follow-up commit; send anything bigger back to an agent or report it. Then add `final_check: <short HEAD sha>` and set `status: done` in the run file.
3. Send the completion push
4. Report summary: phases completed, warnings logged, commits made, suggested next steps

## Error Handling

- Teammate dies on a usage limit (its output or a notification names a usage or rate limit, or says the model is unavailable): do not stop and do not ask. Respawn it on Opus with the same role and assignment, plus: "You are resuming after a restart. Read your progress file at <path> and your last report below, run `git status`, and continue from there." Paste its last report. Restart a teammate at most once per phase or wave. If the restart dies too, stop and report.
- Teammate crash or timeout from any other cause: stop and report. Do not retry. Two watchdog `STALL` events with no agent reply count as a timeout.
- Test failures after 3 fix attempts: stop and report with failing output.
- Commit failure: do not mark the phase complete. Surface the git error and stop.
- Unexpected errors: stop and report with full context. Never silently continue.
