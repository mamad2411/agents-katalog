---
name: oat-agents-cli
description: Guide a human through starting, observing, and taking over an oat-agents Run — git worktrees, tmux sessions, and the file-based Run inbox. Use when the user asks how to use oat-agents, wants to start a Run from a goal with meta fire, inspect a Dispatch, or handle Run inbox lifecycle commands.
---

# oat-agents CLI

`oat-agents` runs a supervised team of coding agents on one machine. This skill covers the
commands a human uses to start, observe and take over a Run.

## Starting a Run

`oat-agents meta fire --prompt "<the goal>" [--repo <path>] [--name <run-name>]
[--base-branch <branch>] [--agent claude|codex] [--trust-workspace]`

This is the human entry point: it creates the Run, the meta-agent's (`oat-meta`) worktree
and branch, and launches its tmux session. Exactly one of `--prompt` or `--input-file` is
required. `--agent` picks the Run's backend; without it, the repository's `.oat/roles.toml`
does (`backend` under `[oat-meta]`), then Claude Code. With no model set anywhere, a role runs
on its backend's own default.

Every agent runs on a private tmux server, so a plain `tmux attach` does not find it. `meta
fire` and every launched `role fire` report the agent's tmux `session` and the exact `attach`
command for it; the live view (`oat-agents tui`) reaches the same sessions without attaching.

## Delegating inside a Run

`role fire <role> [--from <worktree> | --at <commit>] [--name <launch-name>] --prompt <text> |
--input-file <path>` belongs to the meta-agent's own session — it fails with
`run_not_bound` outside one, because it reads `OAT_RUN_ID` from the environment. A role that
starts in an existing worktree needs one of two: `--from` runs it inside an existing
Dispatch's worktree, and `--at` gives it a new worktree of its own at that commit (any
branch, tag or commit id of the Run's repository, resolved when you fire it and reported as
`at`), for work that no Dispatch's worktree holds, such as reviewing a whole epic branch.
Both are refused for a role that starts fresh.

A role can be limited in how many of its Dispatches run at once in one Run: the plugin's
`role.toml` sets a default `max_concurrent`, and the repository overrides it in
`.oat/roles.toml`. A `role fire` beyond the limit is queued, not refused — it answers
`"queued": true` with the Dispatch's id and its place in line, and the CLI starts it when a
place comes free. The limits a Run started with are in `meta fire`'s output under
`role_limits`.

`.oat/roles.toml` can also give a role its own `backend` and, under
`[<role>.model.<backend>]`, its `model` and `reasoning_effort`, replacing the plugin's. A role
fire runs on `--agent` if given, else the role's backend there, else the Run's; each launch
reports the backend it got. What a Run settled is in `meta fire`'s output under
`role_settings`.

## Observing a Run without taking it over

- `dispatch show --dispatch <id> [--run <id>]` — a Dispatch's record and whether its session
  is still alive.
- `dispatch read --dispatch <id> [--source auto|transcript|terminal] [--limit <n>]` — its
  transcript or terminal screen.
- `log show [--run <id>] [--agent <name>] [--event <name>] [--since <ts>] [--limit <n>]
  [--format text|json]`, `log agents`, `log runs` — the workflow log, the one place an
  observer reads a Run from.
- `goal show [--run <id>]`, `goal list` — the goal a Run was fired with.

None of these consume the Run inbox. **The Run inbox has exactly one consumer: that Run's
`oat-meta`.** Taking a delivery from it as an observer leaves the meta-agent waiting for a
message that is already gone.

## Taking over the Run inbox

Only do this in place of the meta-agent, deliberately — for example when it has stalled and
you are stepping in:

- `run wait --run <id> [--ack] [--timeout-ms <ms>]` — blocks for the next delivery; on
  timeout it carries a liveness report.
- `run ack --run <id> --delivery <id>` — acknowledges a delivery so it is not redelivered.
- `run reply --run <id> --message <seq> --prompt <text> | --input-file <path>` — answers one
  message so its sender's `dispatch ask` unblocks.

## Releasing and finishing

- `dispatch release --dispatch <id> [--run <id>] [--remove-worktree] [--force]` — ends a
  Dispatch's session; `--remove-worktree` also removes its worktree, subject to the same
  terms as `run clean` (kept, with a reason, if it is not clean). This is not free: a
  released Dispatch's worktree is gone, along with anything in it nobody committed.
- `meta finish --run <id>` — closes the Run, prints its receipt, removes the Run's execution
  environments (pods), and cleans up.
- `run clean --run <id> | --all --force` — removes every settled Run's remaining worktrees;
  fails with `run_still_open` on a Run that has not been finished yet.

## Errors

Every failure is JSON on stderr with a stable `code` and a nonzero exit status. Common ones:
`run_not_bound` / `dispatch_not_bound` (missing `--run`/`--dispatch` and no matching
environment variable), `already_settled` (a second `dispatch done` or `meta finish`),
`run_still_open` (`run clean` on an unfinished Run), `unknown_role`, `invalid_role_option` /
`role_source_required` (`--from` or `--at` misused), `skill_conflict` (a repository already has a
project-level skill of the name a role declares), `tmux_missing`.

## Claude Code workspace trust

Pass `--trust-workspace` to `meta fire` or `role fire` to have the launch record its worktree
as trusted instead of leaving the dialog for the agent to hit.
