---
name: lens-check-workflow
description: >
  Optional replay check for review lenses. Mode add: turns past pull requests or
  session gaps into approved replay cases under .claude/evals/cases/. Mode run:
  replays a candidate lens edit (working tree or ref) against those cases, with a
  budget the user gives, and reports an advisory verdict. Use through
  /aia-harness:lens-check, or when the retro workflow offers the check.
argument-hint: "[path] [add|run] [--candidate=worktree|<ref>]"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Lens check workflow

Input: a resolved absolute project path, a mode (`add` or `run`), then optional `--` arguments (`--candidate=worktree|<ref>`).

Every CLI call has this form. Use `--json`.

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/harness.mjs" <lens-command> "<path>" [flags] --json
```

## Hard rules

- The check is optional and advisory. A verdict never blocks anything.
- Never run `lens-run` without a budget the user gave. Show the estimate first.
- Never commit. Never run `git stash`, `git checkout`, `git reset` or `git clean`.
- Never send anything to the `aia-harness` repository.
- The check never changes the user's working tree, index, branch or settings.
- The human decides every gate with `AskUserQuestion`.
- Every value flag takes `=`: `--candidate=<value>`. A bare value (`--candidate my-branch`) exits 2 with `aia-harness: --candidate needs a value: use --candidate=<value>`.
- `lens-run` takes one positional argument. More than one exits 2.
- `--help` works on every `lens-*` and `sessions-*` subcommand. It prints that family's help and exits 0.
- `lens.json` limits must be numbers above 0. `trialWallSec` and `setupTimeoutSec` are at most 2147483. `trialMaxTurns` is an integer.

## Mode `add`

1. Run `lens-cases`. Show the candidate table. Ask which to add: 4 at most per round. `lens-cases --since` rejects impossible dates.
2. For a pull request candidate, run `lens-pr` with `--pr=<n>`. Show the external review comments. Propose the role (`gap`, `caught` or `clean`) and the head. The human confirms. `lens-pr` fetches PR objects with `git fetch`. It never prompts for credentials and stops after 120 s.
3. Run `lens-add` with `--id`, `--role`, and the source: `--pr=<n>`, `--base` and `--head`, `--patch=<file>`, or `--lens-gap=<sessionId>@<ts>`. Add `--head-source` or `--ledger-signature` when they apply. Add `--offline` only if the user asks.
   - Exit 1: show the reason. Offer the manual path (`--patch=<file>`). Do not retry the same call.
4. Write `expect.json` for the case with `Write`. Show it. The human reviews each one. On approval, run `lens-approve` with `--case=<id>`. Exit 1: show the reason, fix `expect.json` with the human, then retry once. `lens-approve` refuses a retired case (`case-retired`, exit 1) and an `expect.file` that names a directory (`expect-invalid`).
5. Controls: ask the human for clean pull requests (`clean`) and for findings that a lens already caught (`caught`). The goal is 3 of each. `lens-run` warns with `few-controls` below that.
6. End with a reminder: commit `.claude/evals/cases/`. The skill never commits.

## Mode `run`

1. Resolve the candidate: `--candidate=<worktree|ref>` if given, else `worktree`. A call from the retro workflow passes the edited tree (`Current branch`) or the `harness/<signature>` branch.
2. Estimate. This spends nothing. The run reuse key includes the plugin version and the review prompt block, so an upgrade re-runs trials.

   ```bash
   node "${CLAUDE_PLUGIN_ROOT}/bin/harness.mjs" lens-run "<path>" --candidate=<candidate> --estimate --json
   ```

   - Exit 1: show `candidate-refused`, `no-cases`, `no-op` or `infra` with its reason. Stop.
   - Exit 1 with `error: lens-not-found`: tell the user that `review.lensGlobs` in `.claude/evals/lens.json` matches no file, and stop.
   - Exit 2, 3 or 4: show stderr. Stop.
   - Exit 0: show the static check, the cases (mark `stale`), `runs.toRun`, `runs.reused`, `costUsd` and every warning. Note the names in `credentialEnv`, if any.
3. Ask with one `AskUserQuestion` call that holds these questions:
   - The budget in USD, or `Skip the check`. Do not suggest a budget the user did not state. On skip, stop.
   - Billing, only when `credentialEnv` is not empty: **Use the API key or provider** (`--billing=api`), **Use the subscription** (`--billing=subscription`), or **Cancel**. On cancel, stop.

   In the same message, before the call, tell the user:

   - The budget is a client-side estimate. With a subscription it limits plan usage, not money. With an API key or provider it is real money, and the total can pass the budget a little.
   - Each trial loads only the lens files, the `.claude/` files the lens cites, `review.contextGlobs`, and every harness file the candidate changed, in both arms. It runs with no project hooks, plugins or MCP servers, and only `runner.tools`. Skills stay off unless a kept file is a skill or command.
4. Run with the budget. Use Bash with `run_in_background: true` and `timeout` 600000. Wait for the completion notification. Do not poll.

   ```bash
   node "${CLAUDE_PLUGIN_ROOT}/bin/harness.mjs" lens-run "<path>" --candidate=<candidate> --budget=<usd> --json
   ```

   Add `--billing=<api|subscription>` when the user answered the billing question. Exit 0 with `stop` not null (`budget` or `infra`) is a partial report. Say so.

   Fallback: if `lens-run` exits 5 (`error: api-key-billing`), the estimate missed a credential. Show the `found` names. Ask one `AskUserQuestion` with three options: **Use the API key or provider**, **Use the subscription**, **Cancel**. Rerun the same command with the chosen `--billing=api` or `--billing=subscription`. Never choose for the user.
5. Report in chat: `verdict`, then a table per case (`role`, `base`, `cand`, `cited`), recall, false alarm, `lensLines`, `p` from `tests`. Show `reportPath`. `spentUsd` is live spend only. Reused records are in `reusedUsd` and never move the budget gate. A trial is charged the per-trial cap only when its `claude -p` session started and its cost is unknown (timeout, crash). If `flipped` is not empty and `K` is 1, offer a recheck with `--cases=<flipped> --trials=2`. It needs a new budget from the user.
6. The verdict is advice. Return it to the caller. The human still decides whether to apply the edit.
