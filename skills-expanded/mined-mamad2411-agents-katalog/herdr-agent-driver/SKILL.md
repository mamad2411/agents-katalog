---
name: herdr-agent-driver
description: Drive interactive coding-agent harnesses (Claude Code, Codex, OpenCode, Pi, and similar terminal agents) from a parent orchestrator agent using the herdr CLI. Use when starting, prompting, monitoring, waiting on, reading output from, or coordinating one or more coding agents running in herdr panes — including parallel multi-agent setups with git worktrees.
---

# Driving coding agents with herdr

## Mental model

- The herdr server hosts sessions → workspaces → tabs → panes. Each pane runs a terminal; a coding harness (`claude`, `codex`, `opencode`, `pi`, …) runs interactively inside a pane.
- You drive everything through the `herdr` CLI, which talks to the server over the local socket API and prints JSON. Never attach interactively (`terminal attach` / `agent attach` are for humans).
- herdr detects known harnesses on screen and classifies their state as `idle`, `working`, `blocked`, or `unknown`. Official integrations improve this detection — install them first.
- Canonical loop: **baseline → start → prompt → wait for idle/done/blocked → read → independently verify → steer or stop.**
- The child agent's report is a claim, not evidence. The parent remains responsible for scope, repository state, verification, and acceptance.

## Prerequisites

```bash
herdr status                     # is the server up?
herdr integration status         # installed/outdated integrations
herdr integration install claude # run once per harness: claude, codex, opencode, pi, omp, copilot, devin, droid, kimi, kilo, hermes, qodercli, cursor, mastracode
```

If the harness has no official integration, state detection may stay `unknown`. Then either (a) launch it with no-prompt/auto-approve flags and use `herdr wait output` on its pane, or (b) report state from harness hooks via `herdr pane report-agent` (see references/harness-recipes.md).

## Core driving loop

```bash
# 0. Record the baseline before granting write access.
git status --short --branch
git rev-parse HEAD

# 1. Create a project workspace and read its initial pane ID from the JSON response.
herdr workspace create --cwd ~/src/app --label app --no-focus

# 2. Start a supported harness in that existing shell pane. Herdr supplies the executable;
#    arguments after `--` are harness arguments only.
herdr agent start claude-app --kind claude --pane <pane_id> -- --permission-mode acceptEdits

# 3. Submit one bounded task and wait for a settled state.
herdr agent prompt claude-app "Read TASK.md. Implement only phase 2, verify it, commit it, then stop." \
  --wait --until idle --until done --until blocked --timeout 1200000

# 4. Collect the report, then verify it against the repository yourself.
herdr agent read claude-app --source recent-unwrapped --lines 300
git status --short --branch
git diff --check
git show --stat --oneline HEAD
```

A wait timeout or an interrupted parent tool call does **not** mean the child stopped. Re-read state and output before acting:

```bash
herdr agent get claude-app
herdr agent read claude-app --source visible --lines 80
herdr agent wait claude-app --until idle --until done --until blocked --timeout 1200000
```

## Agent states

| State | Meaning | Your action |
|---|---|---|
| `idle` | At its input prompt, ready; result has been seen | Send the next prompt |
| `done` | Turn finished but not yet seen | Read and verify the result |
| `working` | Generating or running tools | Wait |
| `blocked` | Needs attention: permission prompt, question, error | Read `visible`, answer, or escalate to the human |
| `unknown` | Detection is unsure | Read `visible` yourself; do not trust blind waits |

`herdr agent wait <name> --until <idle|working|blocked|done|unknown> [--timeout MS]` blocks until a requested state. Repeat `--until` to accept multiple terminal states. With no `--until`, it matches `idle`, `done`, or `blocked`. The pane-level variant is `herdr wait agent-status <pane_id> --status <state>`.

## Prompting rules

1. **Use unique names** as targets (`herdr agent rename <target> <name>` if needed). Names/labels are identities; terminal/pane IDs are low-level escape hatches.
2. **Write long specs to a file** (e.g. `/tmp/task-123.md` or `TASK.md` in the repo) and send a one-line prompt referencing it. Multi-line pasted text is unreliable in TUI input boxes (Enter may submit early).
3. Use `herdr agent prompt <name> <text>` to submit a turn; add `--wait` when convenient. Verify submission through its state change or `agent read`. For harness slash commands or input widgets where submission is unreliable, use `herdr pane run <pane_id> "<text>"` or send text followed by `herdr agent send-keys <name> enter`.
4. **Only prompt while `idle`.** Sending mid-`working` queues or garbles input depending on the harness. To interrupt, use `herdr agent send-keys <name> esc`, then confirm the agent settled before prompting again.
5. Bound every implementation turn: name the phase or issue, allowed scope, required checks, commit expectation, and explicit stopping point. For follow-up steering, keep messages short and imperative.
6. Reset harness context at review/implementation or phase boundaries when supported. Stale context makes agents defend earlier work and blur scope; see the per-harness recipes.

## Handling blocked

```bash
herdr agent read claude-app --source visible --lines 60   # see the actual prompt
herdr agent send-keys claude-app enter                    # accept default choice
herdr agent send-keys claude-app down enter               # pick a menu option
herdr agent prompt claude-app "yes, proceed"              # answer a question
```

- Prefer launching with auto-approval flags (see references/harness-recipes.md) so `blocked` is rare.
- If you cannot resolve it, escalate to the human: `herdr notification show "claude-app blocked" --body "Permission prompt needs a human" --sound request`.

## Supervision and acceptance

Treat coding agents as implementers, not authorities:

1. **Establish a baseline.** Record HEAD, tracked/untracked state, active task status, and relevant failing tests before the turn. Explicitly name pre-existing files that must remain untouched.
2. **Inspect while working.** Read recent output at meaningful milestones. Do not wait blindly through a long autonomous loop, but do not inject prompts while the agent is working either.
3. **Distrust completion summaries.** Inspect the complete diff and commit, reconcile task ledgers/specs, and rerun the narrowest relevant checks yourself. A claimed “pre-existing” failure needs reproduction or history evidence.
4. **Separate review from fixing.** A read-only reviewer that edits has violated the task. Prefer a read-only tool configuration or disposable worktree; prompt-only prohibitions are weaker. Start accepted fixes in fresh context.
5. **Stop scope drift early.** Interrupt with Esc, inspect the dirty tree, preserve a potentially useful patch, and restore only identified out-of-scope paths. Never discard a mixed diff blindly.
6. **Attribute cross-change drift historically.** When stacked work is present, use `git log`, blame, and historical file views to determine which later change owns a mismatch. Do not create reverse dependencies or rewrite an earlier contract merely because current HEAD is ahead of it.
7. **Keep commits atomic.** One phase or review-fix set per commit. Verify only intended paths were staged. Unrelated baseline repairs belong in their own owning change.

A useful stopping prompt is: `Implement only <unit>; run <checks>; commit only scoped files with <message>; report unrelated failures without fixing them; then stop.`

## Reading output

| Source | Use for |
|---|---|
| `visible` | Current screen — prompts, dialogs, permission UIs |
| `recent` | Recent scrollback with terminal wrapping |
| `recent-unwrapped` | Logs and results — best default for parsing |
| `detection` | Exactly what the state classifier sees (debugging) |

`herdr agent read <name> --source recent-unwrapped --lines 300` (`--ansi` / `--format ansi` if you need colors). For non-agent panes (builds, servers, tests): `herdr wait output <pane_id> --match <text> [--regex] [--timeout MS]`.

## Parallel agents

- Isolate git state per agent with worktrees — `herdr worktree create` opens the checkout as its own workspace, grouped with the parent repo:
  ```bash
  herdr worktree create --workspace <ws_id> --branch feat-a --no-focus
  # Read the worktree workspace's pane ID from the returned JSON.
  herdr agent start claude-a --kind claude --pane <worktree_pane_id> -- --permission-mode acceptEdits

  herdr pane split --pane <parent_pane_id> --direction right --no-focus
  # Read the new sibling pane ID from the returned JSON.
  herdr agent start codex-b --kind codex --pane <sibling_pane_id> -- -a never -s workspace-write
  ```
- Create workspaces and panes with `--no-focus` when orchestrating; drive agents purely by name.
- Fan-in: loop over names, `agent wait`/`agent get` each, collect with `agent read`.
- Announce completion: `herdr notification show "All agents done" --sound done`.

## Troubleshooting detection

- `herdr agent explain <target>` — shows the matched rule, evidence, and why the state was classified. Add `--verbose` for the full rule evaluation.
- `herdr server agent-manifests` — check manifest sources/cache; `herdr server update-agent-manifests` to refresh; `herdr server reload-agent-manifests` after local override edits.
- If a harness upgraded and detection broke, restart/hand off the server after upgrading herdr before using `agent explain`.

## Cleanup

```bash
herdr pane close <pane_id>
herdr workspace close <workspace_id>            # closes herdr state only
herdr worktree remove --workspace <id>          # actually deletes the git checkout (--force if dirty)
```

## Safety

Auto-approval flags (`--dangerously-skip-permissions`, `-a never`, `--auto`, `--yolo`) remove the human from the loop. Use them only in sandboxes/disposable environments. Prefer least-privilege modes (e.g. Codex `-s workspace-write -a on-request`, Claude `--permission-mode acceptEdits`) plus prompt `blocked` handling when the work is destructive or the repo matters.

## Reference

Per-harness launch recipes, resume commands, and unsupported-harness state reporting: **references/harness-recipes.md**.
