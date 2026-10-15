---
name: delegate-agent
description: Delegate bounded work to an independent coding-agent harness — Antigravity, Claude Code, Codex, OpenCode, or Pi — as a subagent running outside this conversation. Use when the user names one of those harnesses, when a task can be briefed and handed off whole, when a second opinion from a different model would help, or when several harnesses should work in parallel.
---

# Delegate Agent

Treat every delegate as a **subagent in another harness**: it starts cold, works from the brief alone, and hands back a report the parent still owns.

Delegates: `antigravity` (`agy`), `claude`, `codex`, `opencode`, `pi`.

## Establish the delegate surface

Run:

```sh
scripts/delegate-agent list
scripts/delegate-agent run --help
```

Resolve `scripts/delegate-agent` relative to this file; under Claude Code, `${CLAUDE_SKILL_DIR}/scripts/delegate-agent` reaches it from any install location.

`list` reports each harness's executable and whether it is on PATH. The installed set is the source of truth — a harness named here but absent from `list` cannot run, so choose from what `list` returns. This step is complete when the installed harnesses and every flag the run needs are visible.

## Decide what to hand off

A delegate buys two things a same-harness subagent cannot: a different model's judgment, and a context window that never touches this one. Hand off work when either is worth the round trip:

- bounded work that can be briefed whole — an implementation, an investigation, a research question;
- work whose intermediate steps the parent never needs, only the result;
- a second opinion from a model that is not the parent's;
- the parent's own implementation or conclusion, put up for attack;
- several approaches developed separately, then compared.

Independence is the return on the cost, so pick a harness different from the parent — a delegate running the parent's own model rediscovers the same blind spots. When the user names a harness, use the one they named.

Send one delegate by default. Send a second when an independent counterexample is worth the cost, mostly for hard debugging and verification. Use `all` when the user asks for comparison or consensus across harnesses.

This step is complete when the chosen harness appears installed in `list`, and either differs from the parent or was named by the user.

## Choose the role

`--role` becomes the delegate's marching orders, so it shapes the answer more than the task wording does. The first three do work; the last three return judgment.

| Role | The delegate's job | Default mode |
|---|---|---|
| `implement` | Make a bounded change, run the relevant checks, report what changed | workspace-write |
| `solve` | Develop a solution or plan from the requirements | read-only |
| `research` | Answer a bounded technical question, separating verified fact from inference | read-only |
| `debug` | Diagnose root cause independently, with competing hypotheses and the smallest credible fix | read-only |
| `review` | Critique code or design, weighting correctness, security, maintainability, and test gaps over style | read-only |
| `verify` | Attack a stated claim — hunt counterexamples, edge cases, missing tests, false assumptions | read-only |

`--read-only` and `--write` override the default when a role needs the other mode.

## Brief it cold

`--task` is everything the delegate gets. It cannot see this conversation, the files already read, or the reasoning already done — state the objective, the files or symptoms to start from, the constraints, the evidence already gathered, and the shape of the answer wanted.

Two roles want the parent's own thinking handled differently: `verify` needs the parent's claim stated plainly so there is something to falsify, while `solve` produces a genuine alternative only when the parent's approach is left out of the brief.

The brief is complete when an agent with no access to this conversation could act on it without asking a question.

## Run in the narrowest mode

```sh
scripts/delegate-agent run codex --role implement \
  --task "Add the retry guard described in src/queue.ts:88 so enqueue is idempotent under duplicate delivery, with a test covering the duplicate case." --cwd "$PWD"

scripts/delegate-agent all --agents claude,codex,pi --role debug \
  --task "tests/integration/socket_test.py hangs on roughly 1 run in 20. Find the root cause." --cwd "$PWD"
```

`--dry-run` prints the exact command without running it — reach for it when a flag or model identifier is uncertain. Omitting `--agents` fans out to every installed harness.

Read-only is the default for every role but `implement`, and it is what makes fanout safe. Write mode takes one writer per checkout: parallel write fanout is blocked, so give each writer its own `git worktree` and its own `--cwd`.

For per-harness model identifiers, reusable profiles, and the isolation each harness actually provides, read [`references/adapters.md`](references/adapters.md) before selecting a model or running in write mode.

## Take delivery

What comes back is a report, not a fact. `result` holds the delegate's final text; `ok`, `exit_code`, and `stderr` describe the run rather than the answer — a harness exits 0 with a confident wrong conclusion as readily as it exits non-zero having produced a usable partial one. Read both, and treat an empty `result` as a failed delegation rather than a finding.

A long answer is capped and elided from the middle, with `elided_chars` reporting what was dropped. The conclusion and recommended next action survive at the ends; the supporting evidence between them is what goes. When a claim needs the evidence that went with it, re-run with a narrower task rather than a larger `--max-output-chars`.

After an `implement` delegation, the working tree changed and the delegate's account of it is a claim like any other:

```sh
git status --short
git diff
```

Read the diff before building on it, and run the checks yourself rather than trusting the report that they passed. A delegate that edited beyond the brief is the failure to look for.

For every other role, before the delegate's framing sets:

1. Separate its claims from its conclusion.
2. Check each claim the parent will rely on against the repository, the tests, the logs, or authoritative docs. A cited file path, line number, or test result is a claim until the parent has seen it.
3. Settle disagreement between delegates on evidence, so a majority of harnesses repeating one plausible error stays outvoted by the repository.
4. State the parent's own conclusion, naming any part that still rests on an unverified delegate claim.

A `verify` delegation earns its cost by returning a counterexample, a missing test, a false assumption, or an explicit account of what was checked and found sound; an unsupported "looks fine" means the task was too loose, and is worth re-running with a sharper claim to falsify.

The delegation is complete when the delegate's work has been inspected at the source — the diff for `implement`, the cited evidence otherwise — and the parent has stated its own conclusion.
