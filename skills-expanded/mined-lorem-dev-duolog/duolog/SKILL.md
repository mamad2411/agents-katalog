---
name: duolog
description: >-
  Use only in a project that has .duolog/config.yaml. Delegate bounded
  tasks to Claude or Codex for short answers or second opinions.
metadata:
  duolog-version: "1.11.1"
---

Stop unless this project has `.duolog/config.yaml`.

# duolog

## First

1. Run `duolog version`. If not found, tell the user and offer the command
   below; run it only if they agree.

   macOS/Linux:

   ```sh
   curl -fsSL https://github.com/lorem-dev/duolog/releases/download/v1.11.1/install.sh | sh -s -- --version v1.11.1 && duolog install --scope project
   ```

   PowerShell:

   ```powershell
   $env:DUOLOG_VERSION = 'v1.11.1'; irm https://github.com/lorem-dev/duolog/releases/download/v1.11.1/install.ps1 | iex
   ```

   Windows: add the printed directory to PATH; run
   `duolog install --scope project`.
2. Run `duolog doctor` once per session. If rules are off, tell the user
   what it names (`/hooks`) first.

## Hand over

Do settled steps without explaining them; report results.
If a PR is requested or required, batch small changes into one.

1. Give whole features to `planner`; small fixes: yourself.
2. First record the starting checkout, branch and existing edits.
   Write task.md text: Goal, Read, Write (ranges, edited docs),
   Limits, Run (optional), Check.
3. Background `duolog delegate <role> -` (stdin); await notice.
4. Read only summary, `git diff --stat`, marked hunks and `answer.json`'s
   `decisions=`; skip full suites.
   Batch nameable reads in parallel.
5. Keep hard parts. Finish with `review_final` (`review_cross` for big
   batches) without asking; check worker results first. Return findings
   to the worker or fix them.
   End only with results or decisions only the person can make.
   Start closing questions with the decision.

Worker rules: `.duolog/brief.md`. Multiple leads: SessionStart's `--lead <id>`.
Learning: `duolog task start` first.
Same-vendor subagents use your tools, not duolog.

## Running from Codex

Run `duolog delegate` outside the sandbox, or workers cannot start. Old
`duolog version`: use full path.

## On `run here`

- `run here: self`: read only the listed ranges.
- `run here: subagent model=M effort=E`: call `spawn_agent` with model M,
  reasoning_effort E and fork_turns "none", then `wait_agent`. Pass task
  text. Never start another duolog session.

## Asks

For `"p":true` asks, tell the person to answer; rewrite the task if needed,
but never answer yourself.

Foreground delegates deny asks; workers list commands in `needs`.
For ordinary asks use `duolog allow <n>` or `duolog deny <n>`, or
`duolog remember '<command>'` after the user's approval.

## Live sessions (Rex)

Answer `duolog peer wait` with
`duolog peer answer <id> <option>`. Run each peer or CI wait as its own
background command. Run independent tasks in parallel, one worker per
`.worktrees/` worktree; stack dependent work on that task's branch.

Before reporting done, review and bring the peer's task changes into the
starting checkout on its original branch, unless the person requested another
branch or PR. Merge, cherry-pick or apply the diff. Keep changes
uncommitted unless a commit was requested or required; preserve existing
staged, unstaged and untracked work. If integration conflicts, report the
blocker instead of completion. Verify the integrated result there and tell
the person its path, branch and commit status.

Never send `/model` or `/effort` to a Claude pane; they change its session.
