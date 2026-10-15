---
name: fire
description: Delegates a well-specified implementation task to Codex CLI (or Sonnet 5, GLM-5.2, or Grok 4.5 via --with). Use when the user asks to hand work to Codex, or for substantial spec-able work - features, refactors, migrations, boilerplate; offer first unless the routing policy is autonomous. Not for small fixes or ambiguous design; never fire silently.
---

# Fire - hand the ticket to the sous-chef

You are the head chef. Codex is your sous-chef: a strong implementer with no memory
of this conversation, executing exactly one written ticket per run. Two rules fall
out of that: everything the worker needs goes on the ticket, and everything the run
produces lands on disk - the job dir, not this conversation, is the record of the
run.

## When to fire vs. cook it yourself

Fire when ALL of these hold:
- The task is implementation, not design - you already know what the end state looks like.
- It spans multiple files or is mechanical bulk work (refactors, renames, migrations, boilerplate, test scaffolding).
- You can state "done" as checkable criteria (tests pass, command output, types compile).

Cook it yourself when ANY of these hold:
- One-file or few-line surgical fix - the delegation round trip costs more than doing it.
- The approach is still ambiguous - resolve design questions first, then fire.
- The task depends on conversation context that can't be written into a ticket.

Delegation sends code to another vendor and spends their quota: if the user didn't
explicitly ask for it, propose it in one line rather than firing silently. Exception -
an autonomous routing policy in the user's CLAUDE.md pre-authorizes the delegation;
the one-line announcement then replaces the proposal: announce and fire.

## Preflight (all deterministic, run before writing the ticket)

1. **Git repo with at least one commit** - `git rev-parse HEAD` succeeds. Codex refuses non-repos by default, and diff review needs a baseline. If not: tell the user to `git init` / make an initial commit first.
2. **Profile exists** - `test -f ~/.codex/sous-chef.config.toml`. This check is load-bearing: Codex **silently ignores a missing profile** (exit 0, runs under the user's own defaults - possibly no sandbox at all). If missing: stop and offer `/sous-chef:mise`.
3. **Job directory** - mint one per fire: `JOB=$(mktemp -d "$SCRATCHPAD/fire-XXXXXX")` (`$SCRATCHPAD` = your session scratchpad directory; substitute its absolute path). Never share ticket/result/log paths between jobs - fixed paths let concurrent or sequential runs clobber each other and serve a stale result as a fresh success.
4. **Snapshot the tree** - if `git status --porcelain` is non-empty, warn the user their uncommitted changes will share the tree with Codex's edits (suggest committing/stashing first), and either way save the baseline: `git diff > "$JOB/pre-fire.patch"; git status --short > "$JOB/pre-fire.status"`. At plating you review Codex's delta against this baseline, not the raw diff. One honest limit: the patch carries no *contents* for untracked files - the status file records their paths, so if untracked WIP shared the tree, content changes inside those paths cannot be attributed patch-style; say so at plating rather than guessing.
5. **Exclude and mark the notebook** - add `.sous-chef/` to `$(git rev-parse --git-path info/exclude)` if it isn't there (the ticket tells the worker to keep a milestone notebook at `.sous-chef/progress.md`; unexcluded, it would pollute the diff and trip the concurrent-edit check), then append a run marker to the notebook: `## fire <UTC ISO-8601> <$JOB basename>`. Ticks read only below this marker - without it, a previous run's milestones would masquerade as this one's.

## Writing the ticket

Write the ticket to `$JOB/ticket.md` using the template in [references/ticket-template.md](references/ticket-template.md). The contract is XML-block-structured because Codex follows explicit contracts far better than prose requests:

- `<task>` - the concrete job, with enough repo context to orient a fresh agent.
- `<done_when>` - checkable success criteria. Declarative beats imperative: give success criteria, not step-by-step instructions.
- `<files>` - files/dirs to create or modify, and files/dirs NOT to touch. Without this, Codex will make assumptions.
- `<interfaces>` - exact signatures, types, or API shapes other code depends on.
- `<constraints>` - hard rules (no new dependencies, match existing patterns, etc.).
- `<verification>` - exact commands Codex must run before finishing (test, typecheck, lint).
- `<output_contract>` - what the final message must contain: what changed, what was verified with actual command output, what was left undone and why.
- `<progress>` - the milestone notebook: one line appended to `.sous-chef/progress.md` per milestone. The worker knows its milestones better than any log parser; this file is what progress ticks read.
- `<follow_through>` - the default when routine questions come up: keep going, make the reasonable choice, record it; stop only on hard blockers.
- `<action_safety>` - stay narrow; no unrelated refactors; no deleting code it doesn't understand.

Repo-level standards (build commands, conventions, do-not-touch areas) belong in the repo's `AGENTS.md`, which Codex reads automatically on every run - don't duplicate them on the ticket. Run `/sous-chef:mise` once per repo to set that up.

## Choosing the worker - `--with`

The arguments may begin with `--with <worker>`; strip it before treating the
rest as the task description. Workers:

| `--with` | Worker | Route |
|---|---|---|
| *(absent)* / `codex` | GPT-5.6 via Codex CLI | the default invocation below |
| `sonnet` | Claude Sonnet 5, user's own subscription | `references/worker-routes.md` Route C |
| `glm` | GLM-5.2 | `references/worker-routes.md` Route A or B, whichever is installed |
| `grok` | Grok 4.5 via xAI's Grok Build CLI | `references/worker-routes.md` Route D |

Loose phrases ("fire with sonnet", "use GLM for this") mean the same thing -
`--with` is just the unambiguous spelling, immune to task text that happens
to mention a model name. The ticket, job dir, and plating contract are
identical for every worker; what changes is the invocation (and, on the
streaming routes, a stream.jsonl → result.md extraction at plating). Preflight
differs per worker:
step 2's Codex-profile stop applies to the Codex route only - Route C's
preflight is just `command -v claude`, and Route D's is `command -v grok`
plus its auth check (`grok models` exits 0).

## Firing

Run from the repo root (workspace-write scopes writes to the working directory), in the background - never in the foreground, where the Bash timeout ceiling kills long runs. Tool-level backgrounding is the only backgrounding: the command itself must NOT contain `&`, `nohup`, or `disown`, or Claude Code will track a wrapper that exits immediately, fire a false completion notification, and leave the real worker orphaned.

```
Bash (run_in_background: true), cwd = repo root:
env -u CODEX_API_KEY -u CODEX_ACCESS_TOKEN codex exec --profile sous-chef \
  --output-last-message "$JOB/result.md" \
  - < "$JOB/ticket.md" > "$JOB/job.log" 2>&1
```

Notes on the invocation:
- `--profile sous-chef` loads `~/.codex/sous-chef.config.toml` (workspace-write sandbox, approvals never - it never pauses for input that will never arrive). Model and reasoning effort deliberately fall through to the user's `~/.codex/config.toml` defaults.
- `env -u CODEX_API_KEY -u CODEX_ACCESS_TOKEN` pins the run to the user's `codex login` (ChatGPT subscription) auth - those two are the only env vars that override it in `codex exec`, and if either is set the run silently bills per-token instead. (`OPENAI_API_KEY` is NOT read for auth by current Codex, and unsetting it would break custom providers that use it as their `env_key`.)
- Prompt goes via stdin (`- <`) to avoid shell-quoting damage to the ticket.

**Then tell the user, in one or two lines:** what was delegated and to which model (read `model` from `~/.codex/config.toml` - don't assert a model you didn't check), that it typically takes 5–20+ minutes at high reasoning effort, a paste-ready `tail -f` on the run's live file (absolute path - `$JOB/job.log` on the Codex route, `$JOB/stream.jsonl` on the streaming routes, whose job.log is errors-only) to watch it cook - warning that stray MCP transport noise early in a Codex log is usually harmless, not the run failing - the ticket at `$JOB/ticket.md` for what was ordered, and that they can cancel anytime. Progress ticks (below) are on by default: say you'll post a one-line update every few minutes and that "stop ticks" silences them (honoring it means disarming the Monitor and the wakeup loop, not just staying quiet).

To route the ticket to GLM-5.2 (user opt-in), to Claude Sonnet 5 on the user's own subscription (no extra key - the natural fallback when Codex hits its usage limit mid-serve), or to Grok 4.5 via xAI's Grok Build CLI (the one non-Codex route with an OS sandbox), see [references/worker-routes.md](references/worker-routes.md) - same ticket, different worker invocation.

## While it cooks

Do NOT poll - polling loops against a running Codex job are the documented way to incinerate quota while producing nothing. Work on something else or end your turn; the backgrounded job re-invokes you when it exits.

A long run must not be a silent one. Unless the user said stop, keep ticks armed while the worker cooks, waking on events first and time second:

- **Event wakes (preferred when the harness offers a Monitor):** arm ONE Monitor with an until-loop watching `.sous-chef/progress.md` for growth below this run's marker (the worker appends a milestone line per the ticket's `<progress>` block; if a worker rewrote the file and the marker is gone - observed in the field - treat the tail as current and note it) OR the run's live file - `$JOB/job.log` on the Codex route, `$JOB/stream.jsonl` on the streaming routes - matching terminal states (completion AND error signatures like `ERROR:`, `stream disconnected`). A milestone wake reports the new line, re-arms, and ends the turn; ticks then land when something actually happened.
- **Timer fallback (always):** a self-paced wakeup loop - `/loop` with no interval, or whatever wakeup scheduler the harness offers - with the absolute `$JOB` and `.sous-chef/progress.md` paths in the armed prompt: a tick must not depend on conversation memory to find its files. Each tick, read the notebook's tail (and the stream/log for liveness on routes that have one) and report ONE distilled line ("three files edited, tests running now"). Dead air is still a tick: elapsed time plus the last milestone ("14 min in, still on the migration - last milestone: tests scaffolded"). Pace ticks a few minutes apart (under five, so each wakeup lands on a warm prompt cache).

A tick that finds a terminal state says nothing and does not re-arm - completion re-invokes you regardless, and reporting the outcome, like plating, belongs to that turn. This is not the forbidden polling: it is bounded by the run, disarms itself, reads local files, and never queries the worker. No wakeup facility at all? The `tail -f` handoff on the live file stands alone.

**If the user cancels:** kill the background task AND disarm the ticker (stop the Monitor, cancel the wakeup loop - a killed job writes no terminal state for the tick's self-disarm rule to find), then run `git status` + `git diff` - the workspace-write worker may have left a half-applied change. Show the user what's there and let them decide keep or revert.

## Plating - when the job exits

1. **Check the outcome before trusting the plate.** If the job exited non-zero, or `$JOB/result.md` is missing or empty, the run failed - read the tail of `$JOB/job.log`, show the user the error verbatim, and offer one rerun or taking over yourself. Three errors worth naming for the user: "You've hit your usage limit" means wait for the plan's 5-hour window to reset (or escalate plans) - or offer to continue now with `--with sonnet` (Route C); a persistent `401` means their `codex login` needs redoing; a reconnect-loop tail (`ERROR: Reconnecting... 5/5`, then `stream disconnected before completion`) is a mid-run network drop - transient-shaped, offer one immediate rerun (observed live: it can burn thousands of tokens and still leave result.md empty). Never present a missing result as a clean outcome. (MCP transport errors near the top of the log are usually harmless noise from the user's Codex-side MCP servers - the real signal is the last lines.)
2. Glance at the log's opening banner: its `sandbox:` line is ground truth for what actually ran. If it isn't `workspace-write`, say so.
3. Read `$JOB/result.md`, then compare the post-baseline changed file set (`git status`/`git diff` minus `$JOB/pre-fire.*`) to the ticket's `<files>` Touch list. Outside-list paths are unresolved until classified: paths confirmed as another session's concurrent edits must be named with the warning `concurrent edit detected - these changes are NOT part of this run's review` and excluded from the worker-attributed delta, while paths that are the worker's own out-of-scope changes must be reverted or explicitly flagged to the user before the run can be accepted. This is a path-level check: it cannot catch a concurrent session editing a file that *is* on the Touch list - those edits merge into the same file's diff and only the line-by-line read in step 4 will separate them, so treat a Touch-listed file that changed more than the ticket asked as suspect too. Then review Codex's actual delta against `$JOB/pre-fire.patch` - don't attribute the user's own WIP to Codex.
4. Review the diff carefully, line by line. Codex is a competent implementer that makes wrong assumptions without checking - that is exactly the failure mode you're here to catch.
5. Run the `<verification>` commands yourself. Codex's claims are not evidence; command output is.
6. Then either:
   - Accept - summarize what shipped and what you verified, plus the token usage
     from the log's closing summary when the log carries one (the `tokens used`
     block near the end of job.log; the streaming routes report usage in
     `$JOB/stream.jsonl`'s terminal event instead - each route names its
     fields) - quota spend is otherwise invisible to the user. Then add the job
     to the running tab: append one line to `~/.sous-chef/ledger.jsonl`
     (`mkdir -p ~/.sous-chef` first) of the form
     `{"ts":"<UTC ISO-8601>","repo":"<repo basename>","skill":"fire","model":"<model from the log banner>","tokens":<total from the closing summary>}`.
     If the run reports no token usage, skip the ledger line - never invent a
     number. (The streaming routes' usage lives in `$JOB/stream.jsonl`'s
     terminal event, not the log - each route maps its fields onto this same
     line.)
   - Send ONE delta: a fresh fire (new `$JOB`, short ticket that states what the previous run got wrong, quotes the failing output, and scopes the fix). Do NOT use `codex exec resume` - resumed sessions rebuild config from the user's defaults, silently dropping the sandbox, and `--last` may grab a different session entirely. Fresh run + state on disk is the reliable path.

Cap follow-ups at two rounds. If it's still not right after two deltas, take over and finish it yourself - further debate has diminishing returns.

## If Codex is unavailable

If `codex` is missing, unauthenticated, or the profile doesn't exist (preflight step 2), say so and offer to run `/sous-chef:mise` - don't silently implement the task yourself without telling the user the delegation failed.
