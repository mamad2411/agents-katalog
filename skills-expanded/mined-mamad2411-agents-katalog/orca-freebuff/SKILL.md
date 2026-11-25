---
name: orca-freebuff
description: >-
  Dispatch a task to a free (ad-supported) Freebuff coding agent as a
  terminal-driven TUI worker — freebuff.com CLI has no headless mode, so the
  orchestrator launches it in a task worktree terminal, injects the task prompt
  with a completion-marker contract, polls terminal reads for the marker, and
  impersonates worker_done from the cockpit (--from <worker_handle>). Use when
  the worker team should include zero-cost agents (DeepSeek V4 Flash 07/31,
  unlimited) alongside opencode/Claude Code. Orchestrator sessions only. Invoke
  with /orca-freebuff.
disable-model-invocation: true
argument-hint: "Task objective for the freebuff worker?"
---

# Freebuff terminal-driven worker

Drive a **free** coding agent (freebuff.com CLI, ad-supported) as an Orca worker. Freebuff is
built on Codebuff but ships **no headless mode and no free SDK**: every flag that would make it
scriptable (`--print`, `-p`, `--json`, `--non-interactive`, `--batch`, `--exec`, `--auto`,
`--script`, `--prompt`) is rejected with `unknown option`. The `@codebuff/sdk` path requires a
**paid** API key — out of scope for a free worker. The only integration is the one this skill
codifies: treat the freebuff TUI in a task-worktree terminal as the worker, and let the
orchestrator type into it, watch its screen, and settle the dispatch.

This is a **coordinator-driven** pattern (orchestrator sessions only): every step below runs
from the cockpit. There is no worker agent in the freebuff terminal — anything you `terminal
send` goes into the model prompt, never to a shell.

Freebuff is **one of three worker runtimes** (`opencode`, `claude-code`, `freebuff`), chosen at
setup and overridable per task in the plan. It is the only one that is not a supervised agent, and
that is its whole cost: it reports nothing itself, verifies nothing itself, and cannot run while
you are away. Use it where free matters more than autonomy — and reach for `/orca-orchestrate`
with an agent runtime for everything else.

## Re-orient first

`/orca-resume` if fresh. Verify the worktree guardrail: `orca worktree current --json` →
`isMainWorktree` must be `true`. Then load the guides and read them before running anything:

```text
orca skills get orchestration
orca skills get orca-cli
```

Prefer `--json` for agent-driven calls. Never guess subcommands or flags from memory.

## Pre-flight

1. CLI present and recent: `freebuff --version` (installed globally, e.g. `~/.local/bin/freebuff`).
2. Authenticated: `~/.config/manicode/credentials.json` exists with a `default` account
   (Freebuff needs no account to *download*, but a logged-in session is what unlocks the model
   picker and "unlimited" DeepSeek V4 Flash). If absent, run `freebuff login` once in a regular
   terminal before the run.
3. Session quotas: freebuff is ad-funded with per-day premium sessions; outside full-access
   regions it falls back to **limited mode** (DeepSeek V4 Flash / MiMo 2.5, 6 one-hour sessions
   per day). Check the banner in the TUI at launch ("unlimited" vs a session counter). Plan the
   run so a limited-mode fallback is acceptable.
4. Confirm the run/task shape: this pattern works with an Orca Run + Tasks (from `/orca-tasks`
   or the quick path).
5. Read `docs/agents/setup.md` → `## Merge gate`. The freebuff model verifies nothing, so **you**
   satisfy that gate before settling the dispatch (see "Settle the dispatch"). If the marker is
   missing, route to `/orca-setup`: a free worker whose output nobody checks is worse than no
   worker, and this is the one skill where the coordinator personally signs the result.

## Dispatch recipe

One task = one branch = one worktree, never the primary. Create the worktree + terminal, wait
for the TUI, then bind the dispatch **without injection** (Freebuff is not a recognized agent,
so both `worker-start` and `dispatch --inject` refuse it with `agent_unconfigured`; the runtime
itself suggests "dispatch without --inject and send the prompt manually").

```bash
# bind the run (planned path) or create it (quick path)
orca orchestration run-use --id <run_id> --json
orca orchestration task-create --spec "<plan task id>: <task brief>" --json   # if not already cut

# 1. task worktree + terminal running the freebuff TUI
orca worktree create --name <slug> --no-parent --json
orca terminal create --worktree id:<newWorktreeId> --title <slug> --command "freebuff" --json
orca terminal wait --terminal <handle> --for tui-idle --timeout-ms 90000 --json
# the welcome screen ("Freebuff will run commands on your behalf") is non-blocking:
# the first message sent is accepted as a prompt. The welcome screen sometimes includes a
# model picker — an Enter confirms the pre-selected model (typically DeepSeek V4 Flash,
# "UNLIMITED"); read the screen once to confirm the banner before sending the prompt.

# 2. bind the dispatch WITHOUT --inject (creates the dispatch, assigns the terminal)
orca orchestration dispatch --task <task_id> --run <run_id> --to <handle> --json
# note: returns dispatch.id (e.g. ctx_...) — capture it for the worker_done.

# 3. inject the task prompt manually with the completion-marker contract (see below)
orca terminal send --terminal <handle> --text "<task prompt with marker contract>" --enter --json
```

There is often a fallback shell in the same worktree (bare `worktree create` opens one before
`terminal create` adds the agent). Target only the freebuff handle; close an unused fallback
shell only after `orca terminal list --worktree id:<id> --json` confirms it is unused.

## The prompt and the marker contract

Freebuff stays open after answering — there is no exit-on-done. **`terminal wait --for
tui-idle` is NOT a completion signal**: it satisfies during streaming micro-pauses and while the
model thinks. The only reliable end-of-task signal is a unique marker the model is told to emit.

Every task prompt must end with the marker contract verbatim:

```text
When your work is complete, end your reply with exactly this line on its own:
FREEBUFF_TASK_DONE
Do not modify any files unrelated to the task.
Do not push or open pull requests yourself.
```

Additional work instructions to include per task: stay on the current branch, run the project's
tests/checks, keep the diff minimal, report a short summary before the marker.

## Completion loop (marker + polling)

Do not trust a single idle. Loop until the marker appears or the task timeout is hit:

```bash
orca terminal wait --terminal <handle> --for tui-idle --timeout-ms 120000 --json
orca terminal read --terminal <handle> --json    # grep the buffer for FREEBUFF_TASK_DONE
```

- The TUI renders ASCII-art, prompt echoes, and the model's thinking over the same screen lines,
  so plain-text extraction is unreliable — grep for the marker in the read buffer, not for the
  "final answer".
- Repeat: wait → read → grep. Bounded windows (60-120 s) per iteration; an overall per-task
  timeout (e.g. 30-60 min for coding tasks) is the guard rail.
- The marker can first appear as the prompt echo — require it *after* a completed turn:
  simplest reliable check is the marker present in a read taken when the TUI is idle AND the
  freebuff terminal shows no active "Thinking"/spinner state; if ambiguous, poll again.
- If the model drifts (never emits the marker) and the TUI is idle, send one bounded
  re-request: "Finish your reply with the marker line FREEBUFF_TASK_DONE." Then keep polling.

## Settle the dispatch (worker_done impersonated)

Because nothing in the freebuff terminal executes shell commands, the **orchestrator** sends the
worker_done from the cockpit, impersonating the worker terminal via `--from <handle>`. This is
the one deliberate deviation from `/orca-orchestrate`, where the worker reports itself.

Before sending, verify the work is real — **the coordinator is the gate here, because nothing in
the freebuff terminal can be trusted to verify itself**. The model can claim success it did not
achieve, and unlike an Orca worker it never ran a `worker_done` contract. Check `git status` /
`git diff` in the task worktree, then satisfy the mode recorded in `docs/agents/setup.md` under
`## Merge gate` yourself: run the `ci: local <command>` command, or push and watch
`gh pr checks` under `ci: github-actions` (remembering that `no checks reported` exits 0 and is a
failed gate, not a pass). Quote the evidence in the `worker_done` body — you are signing it in the
worker's name.

```bash
orca orchestration send --type worker_done --subject succeeded --outcome succeeded \
  --body "<done, found, left>" --task-id <task_id> --dispatch-id <dispatch_id> \
  --from <worker_handle> --run <run_id> --json
```

The lifecycle marks the task completed automatically (`action: completed`, provenance
`reportedBy: <worker_handle>`). Do **not** follow with `task-update --status completed`. The
worker_done also **auto-settles the dispatch**: a later `worker-release --dispatch ...` returns
`dispatch_not_found` — that is the expected outcome of this pattern, skip the release step.

Then merge green work as the coordinator always does (github: `gh pr merge --squash
--delete-branch` after CI; local/linear: squash-merge into the cockpit main), then:

```bash
orca worktree rm --worktree <task_worktree_id> --force --json
orca terminal close --terminal <handle> --json    # freebuff terminals are external; close them
```

(`worker-release` is intentionally omitted: the impersonated worker_done already settled the
dispatch — see "Settle the dispatch".)

## Failures

- **Marker never appears** within the task timeout and the TUI is idle → the model stalled or
  drifted. One bounded re-request (above), then a **decision gate to the user** (retry / fix
  forward / abandon). Never silently redispatch.
- **Model edits unrelated files** → gate with the diff shown.
- **Session cap hit** (limited-mode counter exhausted) → surface to the user before more tasks;
  either wait for the next window or plan fewer premium sessions.

## Why this pattern (and not the alternatives)

| Option | Verdict |
| --- | --- |
| Freebuff CLI headless flags | None exist — all rejected as `unknown option` (verified on 0.0.149). |
| `@codebuff/sdk` | Paid API key required — contradicts the free-worker goal. |
| `worker-start` / `dispatch --inject` | Refuse non-agent terminals (`agent_unconfigured`). |
| `dispatch --to` without injection + manual prompt | **Works** — this skill. |
| Trusting `tui-idle` alone | Not a completion signal — marker + polling required. |

## Done when

- A task was dispatched to a freebuff TUI worker, the marker appeared, `worker_done` (impersonated)
  settled it as `completed`, and the worktree/terminal are cleaned up.
- The user saw the task result and the merged (or gated) outcome.
