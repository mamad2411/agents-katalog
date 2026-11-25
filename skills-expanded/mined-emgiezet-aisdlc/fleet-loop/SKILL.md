---
name: fleet-loop
description: >
  Run the unattended issue-to-PR loop from inside an agent session — labelled issues in, reviewed
  draft pull requests out, every pipeline phase kept. Use when asked to "take issues from the
  tracker and ship PRs on their own", to keep `aisdlc loop` ticking under omp or Claude Code, or
  to explain why a tick pulled nothing. Not for one ticket with a spec (`aisdlc add`) or one
  issue by number (`aisdlc add --issue`).
---

# The fleet loop

`aisdlc loop` is one tick: `pull` the oldest open issue that carries the approval label and that
nobody holds and this repo has not built, then `run --once` — triage → root-cause → implement →
qa → scope-check → verify → ship → review, in a worktree of its own. The runner selects and
labels; the model never chooses what to work on. This skill runs that tick, repeatedly, from a
session instead of from cron.

## Which binary

`aisdlc` on PATH may be another plugin's runner without `pull` or `loop`. Use the one beside this
skill — `<plugin>/bin/aisdlc`, two levels up from this skill's directory — for every call below.
Under omp the directory resolves from the skill URL:

```bash
AISDLC="$(realpath skill://fleet-loop)/../../bin/aisdlc"
"$AISDLC" help | grep -q 'aisdlc loop' || echo "wrong runner: $AISDLC"
```

## Before the first tick

Each check is one command; a failure is reported to the user, not worked around.

| Check | Command | Failure means |
|---|---|---|
| tracker | `grep 'Tracker descriptor' .claude/sdlc.md` | none → run `/sdlc:init`; `pull` needs `local` or `github` |
| tracker auth | `gh auth status` (github only) | nothing can be listed or claimed |
| runtime | `command -v claude` (or `omp`) | phases cannot run |
| verify commands | `jq .verify .aisdlc/config.json` | empty → every task ends `verify FAIL`, nothing ships |
| claimable work | `"$AISDLC" pull --repo . --dry-run` | "nothing to pull" is a valid state, not an error |

`--dry-run` prints the candidates and claims nothing. Read it before spending tokens.

## Running it

```bash
"$AISDLC" loop --repo . --once                   # one tick: pull, then run --once
"$AISDLC" loop --repo . --interval 900           # tick every 15 min until interrupted
"$AISDLC" loop --repo . --runtime omp --model sonnet   # any add flag passes through
```

The continuous form is a long-lived job: run it with no deadline, never inside a subagent — the
tick is a process to supervise, not a task to delegate. After every tick read `"$AISDLC" status`
and `"$AISDLC" inbox` and report one line per task that changed state. Task logs are under
`.aisdlc/tasks/<id>/`.

## What the loop decides, and what it does not

- The approval label (`bug` by default; `pull_label` in `.aisdlc/config.json`) **is** the
  approval. A human puts it on the issue; `triage` writes `status: approved` only while it is
  there, and the spec gate refuses the task before `implement` if it is gone. **Never add the
  label yourself to make the loop take an issue.**
- An issue with an assignee or `in-progress` is someone's. `pull` skips it; `add --issue` on it
  dies. Do not clear another agent's claim.
- An issue that already has a task record — any status — or an `ai/GH-<n>-*` branch is never
  pulled twice. A failed one is `aisdlc retry <id>`'s business, and only when asked.
- Nothing here merges. `review` ends at `merge-ready` or `changes-requested`; `/sdlc:merge` is
  a person's command.

## Stop and tell the user when

- `gh` reports a rate limit or an auth failure
- `verify FAIL` on every task — the config is wrong, not the work
- the same task fails twice for the same reason (read `aisdlc logs <id>` first)
- three consecutive ticks pull nothing: there is no work, stop polling

## Overlays

An organisation's plugin that changes the selection rule — its own labels, its own queue, extra
steps around `deliver` — ships a **second** skill named `<org>-fleet-loop` that opens with
`read skill://fleet-loop` and lists only what differs. It must not reuse this name: under omp
both plugins load side by side, and a same-named overlay pushes this copy under a namespace
that differs per host, so neither can address the other reliably. Its runner may be its own;
the binary rule above still applies — resolve it from the overlay's skill directory.

## Related

- `pipeline-contracts` — the claim lock, labels, verdict tokens, the bugfix approval rule
- `harness-eval` — when the loop ships bad PRs on a cheap model, fix the instructions
