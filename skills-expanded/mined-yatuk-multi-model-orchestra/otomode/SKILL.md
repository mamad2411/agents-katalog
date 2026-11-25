---
name: otomode
description: "Unattended work mode for when the user is away. `otomode 6h` asks everything up front in one round (tasks, how to check each, permissions), writes OTOMODE.md, turns on a hook that denies every permission prompt and question and logs it to QUESTIONS.md, then works task by task through subagents (Claude, DeepSeek), verifies each with its own check and commits each separately, pauses at 85% usage and resumes by cron after the reset, with an hourly watchdog. `otomode off` turns the hook off, reports and asks the saved questions. Also handles `otomode resume`, `otomode watchdog`, `otomode status`."
---

# otomode

The user is away. Work through an agreed task list without ever waiting on
them, and leave everything reviewable: one commit per task, a plan file, a
question log.

Helper script (all state, the hook, the log and the usage readout):

```bash
OTO="python $HOME/.claude/skills/otomode/scripts/otomode.py"   # python3 where python is not on PATH
$OTO on --project "<repo root>" --hours <N>   # hook ON for this session
$OTO off                                      # hook OFF; prints cleanup_left_for_you
$OTO status                                   # state + usage
$OTO log "<text>"                             # "- HH:MM <text>" into the OTOMODE.md log
$OTO gate [--percent P --reset ISO]           # go / stop / unknown before each task
$OTO usage                                    # usage from the statusline file (CLI)
```

`$OTO` is shorthand here: shell variables do not survive between tool calls,
so write the full command each time, exactly as in its allow rule.

Setup, once: `$OTO install` registers the hook in `~/.claude/settings.json`
(PermissionRequest `*`, PreToolUse on Bash, PowerShell, ask tools and
`mcp__.*`; `$OTO uninstall` removes it). It does nothing while otomode is off.
For usage in the CLI, use `scripts/statusline.py` as the status line (or call
it from yours); in the desktop app you read usage with `get_usage` and pass it
to the gate (section 3). While on, for this session only, the hook:

- denies every permission prompt, `AskUserQuestion`, `EnterPlanMode` and
  `ExitPlanMode`, and appends each one to `<repo>/QUESTIONS.md`;
- denies delete, deploy, push and send commands outright (rm, git push,
  branch or worktree removal, reset --hard, kubectl/terraform/az/aws, ssh/scp,
  POST requests, gh pr/issue writes, publish, mail, `| sh`) and MCP tools named
  send, post, delete, submit, upload and the like, also logged and kept for
  the end report. For Bash it judges only commands that would run (first word
  of each segment, through sudo/env/xargs/timeout, `bash -c`, `eval`, `$(...)`,
  `find -exec`, heredocs fed to a shell); writing those words with echo, a
  quoted heredoc or a commit message is fine. Lines it cannot parse, and all
  PowerShell, are judged by whole-text regex.

A denial is not a failure to retry: read the reason, take the safe default or
mark the task blocked, and move on.

## Hard rules (whole run)

- Never wait on the user. Never call AskUserQuestion after the start round.
- Never delete, deploy, push or send messages, even if a task seems to need it.
  Write what would be needed into the task's notes instead.
- Never remove worktrees or branches you created; list them in the report.
- Commit only on the otomode branch, one commit per task, task id in the
  subject. Follow the repo's CLAUDE.md and commit trailer rules.
- Every subagent call names its model explicitly (`model: "sonnet"` or
  `"opus"`); no subagent asks questions or commits.
- Every lane works on the otomode branch's code, never the default branch's
  (section 2, steps 2 and 4).
- A check's exit code decides, so never let a pipe hide it: run
  `<check> > <repo>/.otomode/T<n>.check.log 2>&1; echo "exit=$?"` and read the
  log's tail in a separate call. If you must pipe, start with `set -o pipefail`.
- Never write a time from memory. Log lines go through `$OTO log`; any other
  time comes from `date +%H:%M`.

## 1. Start: `otomode <duration>` (e.g. `otomode 6h`)

1. If the message already lists tasks and checks, use them and ask only what is
   missing. Otherwise ask **one** round, as a plain numbered message (not
   AskUserQuestion, so free text fits), and wait for the answer:
   1. The tasks, in priority order.
   2. For each task, how to check it is done: a command (test, build, lint,
      script) whose exit code decides. Offer a concrete check per task. Also
      the repo's **quick check** (its fast gate, run after every merge) and
      **full check** (what CI runs), e.g. from CLAUDE.md or the CI config.
   3. The permissions the run will need. Read `.claude/settings*.json` and
      `~/.claude/settings.json`, derive the commands from the tasks and checks
      (test runners, build, git checkout/add/commit/merge/merge-base/
      cherry-pick/worktree add, `date`, lane CLIs), and list the allow rules
      still missing, e.g. `Bash(go test:*)`. Always include file edits:
      `Edit(<repo>/**)`, `Edit(<repo-parent>/wt-*/**)` for DeepSeek worktrees
      and `Edit(<repo>/.claude/worktrees/**)` for Claude worktrees, unless the
      session already runs in auto or acceptEdits mode. Always include the
      helper itself: `Bash(python <home>/.claude/skills/otomode/scripts/otomode.py:*)`
      (the exact command string you will run), and if DeepSeek is allowed
      `Bash(bash <home>/.claude/skills/orchestra/scripts/mmo-run:*)`.
      Also `Read(<home>/.claude/skills/**)` so the run can read the lane
      skills it routes to. Run every command alone (no `cd x && ...` chains),
      since a compound command needs its own approval; use absolute paths or
      `git -C`. Everything not allowed now will be denied later, so be
      generous within the repo. Ask whether to add them to
      `.claude/settings.local.json`.
   4. Anything off limits (files, directories, services), and whether DeepSeek
      may be used.
   5. If the work tree is dirty: leave it, or include it in the first commit?
2. After the answer: add the approved allow rules to
   `.claude/settings.local.json` (merge, never replace; use the Write or Edit
   tool, not a shell heredoc, so the user sees one approval). If a write is
   refused here, the user is still present: say exactly which approval is
   needed and stop; do not turn the hook on with setup unfinished. Add
   `.otomode/` and `QUESTIONS.md` to `.git/info/exclude`. Create the branch
   `otomode/<YYYY-MM-DD-HHMM>` from HEAD unless the user said otherwise.
3. Smoke-test every lane and model id the plan uses, while the user is still
   there: one tiny read-only prompt each (e.g.
   `mmo-run <provider> -m <id> --mode ro --brief <tiny> --out <file> -t 120`,
   after the orchestra skill's `mmo-preflight`; a one-line Agent call per
   Claude model). Record the ids that answered on the `Lanes:` line of
   OTOMODE.md and drop the ones that did not.
4. Run the quick check once on the new branch, so a later failure is known to
   be the run's. Note a failure that was already there in OTOMODE.md.
5. Write `OTOMODE.md` at the repo root (format below), commit it as the first
   commit `otomode: plan`.
6. Turn the hook on: `$OTO on --project "<repo root>" --hours <N>`.
7. Schedule the watchdog with CronCreate: cron `17 * * * *`, recurring, prompt
   `otomode watchdog`. Record the job id in OTOMODE.md.
8. Say in one line that otomode is on and until when, then start working.

### OTOMODE.md

```markdown
# Otomode run
Started: <time> · Ends: <time> · Branch: otomode/<stamp> · Usage stop: 85%
Watchdog cron: <id> · Resume cron: <id or none>
Quick check: `<cmd>` · Full check: `<cmd>` · Lanes: sonnet, opus, deepseek/<id> (smoke ok <time>)

## Rules from the user
- <off limits, DeepSeek yes/no, dirty tree decision>

## Tasks
| # | Task | Check | Lane | Status | Tries | Commit | Notes |
|---|------|-------|------|--------|-------|--------|-------|
| T1 | ... | `go test ./internal/x/...` | sonnet | todo | 0 | | |

## Log
- <HH:MM from $OTO log> T1 started (sonnet, worktree ...)
```

Status values: `todo`, `running`, `done`, `blocked`, `failed`. Update the
table after every step and add a log line with `$OTO log`; this file is how a
resumed or compacted session knows where it is.

## 2. Work loop

Before each task: run the usage gate (section 3) and the deadline check (past
`Ends` means no new tasks: go to step 7 of the loop).

For each `todo` task, in order:

1. Pick the lane (see the `orchestra` skill), cheapest that can carry it, from
   the smoke-tested `Lanes:` only:
   - DeepSeek first for easy, well-specified work when the user allowed it
     (any `mmo-run` provider works the same way: `codex`, `kimi`, `deepseek`;
     it saves Claude usage). Write the brief to `<repo>/.otomode/T<n>.brief.md`, then
     `git worktree add <repo-parent>/wt-ds-T<n> -b otomode-ds/T<n> otomode/<stamp>`
     and, with Bash `run_in_background`:
     `bash ~/.claude/skills/orchestra/scripts/mmo-run deepseek --mode rw -C <repo-parent>/wt-ds-T<n> --brief <repo>/.otomode/T<n>.brief.md --out <repo>/.otomode/T<n>.out.md -t 1200`.
     Exit 6 means a limit or no credit: move the task, and the rest of the
     run, to Claude lanes. `model_not_found` (or an unknown-model error) is
     not a try: smoke-test the provider's ids again, switch to one that
     answers, update `Lanes:` and rerun. Any other non-zero exit is a failed try.
   - `sonnet` for scoped, clear work; `opus` for multi-file or debugging work.
2. Write the brief. Its **first line** is: "First run `git merge otomode/<stamp>`
   in your worktree (or confirm `git merge-base --is-ancestor <otomode head> HEAD`);
   if that fails, stop and say so." Claude lanes run with `isolation: "worktree"`,
   which starts from the default branch, not the otomode branch. Then: goal,
   exact files, steps, the check command, the repo's rules, "do not commit, do
   not push, do not ask questions; use the Bash tool, not PowerShell, and only
   simple commands; never pipe a check without `set -o pipefail`; if blocked,
   stop and say why". Independent tasks may run in parallel (at most 3 lanes).
3. When the lane returns, check it yourself: read the diff, run the task's
   check command in the worktree. The subagent's word is not the check. A lane
   that stops "waiting on background work" (a long test run) is not resumed:
   read its log or output file and finish the verification yourself.
4. Pass: commit the change in the lane's worktree (`otomode T<n>: <task>`),
   then check the base: `git merge-base --is-ancestor <otomode head when the
   lane started> <lane branch>` must succeed (note that head in the task's
   Notes at launch), and `git log --oneline otomode/<stamp>..<lane branch>`
   must list only the lane's own commit (plus the merge from step 2). Anything
   else means the lane started from the wrong base: do not merge the branch.
   Bring the change over with `git cherry-pick <commit>` onto the otomode
   branch; if the lane worked on stale code, retry it (a try) instead.
   Then run the **quick check** on the otomode branch. If it fails, fix it now
   (a follow-up commit, or `git revert`, never reset) before the next merge.
   Record the commit hash, set `done`, `$OTO log` it.
5. Fail: increment Tries, note the failing output (short), and retry with the
   failure in the brief, escalating sonnet to opus or DeepSeek to sonnet. After
   3 failed tries, or when the task is blocked (a needed permission was denied,
   a needed decision is the user's, something off limits), set `blocked` or
   `failed`, write why in Notes and in QUESTIONS.md, and move on.
6. Runs longer than about 3 hours: run the **full check** once around the
   middle on the otomode branch, not only at the end, and fix what it finds
   (architecture tests, golden files, lint) as its own commit.
7. When no `todo` task is left or the deadline passed: run the full check,
   write the summary into OTOMODE.md (with its result), commit it
   (`otomode: summary`), stop the watchdog only if every task is settled, and
   stay idle. Keep the hook on until the user says `otomode off`.

## 3. Usage gate

Run the gate before **every** new task and in every watchdog run. Do not skip it.

1. If `mcp__ccd_session_mgmt__get_usage` exists (desktop app; load it via
   ToolSearch), call it, take the window with the highest `percentUsed` among
   the 5-hour and weekly ones, and run
   `$OTO gate --percent <percentUsed> --reset <resetsAt>`.
   Otherwise (CLI) run `$OTO gate`, which reads the statusline file.
2. Act on `decision`:
   - `go`: start the task.
   - `unknown`: start at most one task, then gate again.
   - `stop` (85% or more): start nothing new. Let running lanes finish, verify
     and commit what is ready. Then CronCreate with `cron` = the gate's
     `resume_cron`, `recurring: false`, prompt `otomode resume`; write its id,
     `resume_at` and the percent into OTOMODE.md, and stop. If the gate's note
     says the reset is after the run ends, write the summary instead.

## 4. `otomode resume`

Run `$OTO status`. If otomode is off, do nothing. Otherwise re-read OTOMODE.md,
run the usage gate, and continue the work loop from the first unsettled task.
A task left `running` from before is checked first: if its worktree has a
change, verify it; otherwise restart it (it counts as a try).

## 5. `otomode watchdog` (hourly cron)

Quick and cheap, no new work unless the loop has stalled:

1. `$OTO status`: if off, CronDelete the watchdog and stop.
2. Usage gate. Over 85% with no resume cron scheduled: schedule it.
3. If no lane is running, tasks are still `todo`, usage is fine and no resume
   cron is pending: the loop stalled; continue it (as in resume).
4. A lane past its expected run time (90 minutes at most), or idle-waiting on
   its own background work: read its log or output. If the work is done, run
   the verification yourself (loop step 3); if it is stuck, stop it
   (TaskStop) and count a try.
5. Past `Ends`: no new tasks; finish step 7 of the work loop.
6. `$OTO log` one line.

## 6. End: `otomode off`

In this order:

1. `$OTO off` first, so the hook stops denying before anything else. Keep its
   `cleanup_left_for_you` list.
2. CronDelete the watchdog and any resume cron (CronList to find them).
3. A short report, under 15 lines: tasks done (commit hashes), blocked or
   failed with the reason, the branch name, the full check's result, how many
   prompts were denied, usage at the end. Nothing is pushed or merged.
   Then a **Cleanup left for you** block with the exact commands, one per
   line: the blocked housekeeping from `cleanup_left_for_you` (test
   containers, files) and the removal of the worktrees and lane branches this
   run created (`git worktree remove <path>`, `git branch -D <branch>`).
4. Then ask the saved questions from QUESTIONS.md: group them, skip ones that
   no longer matter or are already in the cleanup block, and ask with
   AskUserQuestion (up to 4 per call) where there are clear options, as plain
   text otherwise. Offer to redo the blocked tasks with the answers.

## `otomode status`

`$OTO status`, then a three-line summary from OTOMODE.md: tasks by status,
usage, next cron.
