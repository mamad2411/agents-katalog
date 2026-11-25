---
name: agent-stop-conditions
description: Use when designing, reviewing or debugging the limits of an autonomous agent run - a headless claude -p job, an Agent SDK loop, a scheduled or unattended agent - or after a runaway run that looped, retried, overspent or never finished. Fires on "max turns", "max budget", "agent stuck in a loop", "keeps calling the same tool", "runaway agent", "cap agent spend", "retry policy for agent tool calls", "error_max_turns", "error_max_budget_usd". Not for retry or timeout settings of an ordinary HTTP client with no agent loop, and not for choosing which tools an agent may call (use tool-allowlist).
---

# Agent stop conditions

Every autonomous run needs a hard stop that the runtime enforces. A limit written into the prompt is a request the agent may ignore; a limit enforced by the loop, the launching process or a hook is a stop. Set it before the run starts, and decide in advance what the caller does when it fires.

## 1. Use the native knobs first

Both caps default to no limit: "Without limits, the loop runs until Claude finishes on its own, which is fine for well-scoped tasks but can run long on open-ended prompts." And: "Setting a budget is a good default for production agents."

| Knob | Exact behaviour (quoted) | What it produces | Caller must |
|---|---|---|---|
| SDK `max_turns` / `maxTurns` | "counts tool-use turns only" | `ResultMessage` subtype `error_max_turns` | treat as incomplete; never read `result`, which exists only on `success`; log `num_turns`, `total_cost_usd`, `session_id` |
| SDK `max_budget_usd` / `maxBudgetUsd` | caps the run "based on a spend threshold"; subagent spend counts toward it | subtype `error_max_budget_usd` | same; escalate rather than rerun with a bigger cap by default |
| CLI `--max-turns` | "Limit the number of agentic turns (print mode only). Exits with an error when the limit is reached." | the CLI exits with an error | check the exit status before reading any output |
| CLI `--max-budget-usd` | "Maximum dollar amount to spend on API calls before stopping (print mode only)." On `--continue` / `--resume`, "totals restored from earlier runs don't count toward it." | stop; then spawning another subagent fails with `Budget limit reached` (v2.1.217 or later) | keep your own total across a resume chain; each resumed run starts a fresh cap |
| Session crash | a streaming session emits a final `error_during_execution` and exits | subtype `error_during_execution` | do not auto-retry; inspect first |
| `PreToolUse` hook | runs before a tool executes; a hook that rejects a call prevents it from executing and Claude receives the rejection message | the call never runs | the place to enforce your own checks (sections 2 to 5) inside the run |
| `--permission-prompts none` (v2.1.259 or later) / `permissionMode` `"dontAsk"` | "Pass `none` when nobody can answer, and Claude Code denies them instead." | denied tool call | use on unattended runs so a prompt cannot stall the run forever |

All result subtypes: `success`, `error_max_turns`, `error_max_budget_usd`, `error_during_execution`, `error_max_structured_output_retries`. Branch on the subtype, not on whether text came back. A single-shot `query()` yields the result message and then raises (for example "Reached maximum number of turns"): catch the raise, keep the message. In a streaming session the budget accumulates across messages and "A `/clear` starts the budget over."

What you build yourself: a wall-clock limit for `claude -p` (none is documented; enforce it in the process that launches the run), a windowed error rate, idempotent retries, and loop detection. For LangGraph or any other framework, check the framework docs; do not assume an equivalent option exists.

## 2. Check the budget before the call, not after

Adding cost after a call and then comparing lets the call that crosses the cap run in full, so the run overshoots by up to one call. Reserve the most that call can cost, refuse if it does not fit, then settle the actual cost.

```js
function reserve(budget, maxCallUsd) {
  if (budget.spentUsd + budget.reservedUsd + maxCallUsd > budget.capUsd) {
    return null; // stop before spending; the caller escalates
  }
  budget.reservedUsd += maxCallUsd;
  return (actualUsd) => { budget.reservedUsd -= maxCallUsd; budget.spentUsd += actualUsd; };
}

const settle = reserve(budget, maxCallUsd); // maxCallUsd: input tokens x input price + max_tokens x output price
if (!settle) return stop('budget');
const res = await callModel(req);
settle(costOf(res.usage));
```

The docs do not say whether the native cap can be crossed by the call in flight. Treat it as a backstop and set it one call's cost below the amount you cannot exceed.

## 3. Count errors in a window, and decide in one place

A cumulative counter never forgets: three transient errors spread over six hours stop the run as surely as three in a row. A wrapper that counts and also rethrows makes two layers handle one failure. Keep the last N outcomes and return one decision.

```js
const recent = []; // true = ok, false = error
function record(ok, { size = 10, maxErrors = 3 } = {}) {
  recent.push(ok);
  if (recent.length > size) recent.shift();
  return recent.filter((x) => !x).length >= maxErrors ? 'stop' : 'continue';
}
```

## 4. Retry only what is safe to repeat

Retry reads and other idempotent calls a bounded number of times, with backoff. Never retry a write without an idempotency key: a timeout does not tell you whether the write landed, and a retry can apply it twice (two charges, two emails). Generate the key once per logical operation and reuse it on every attempt. A write with no key gets zero retries and is escalated.

## 5. Detect loops

A loop is the same tool called with the same arguments again and again, or the same 2 to 4 calls in a cycle (read, edit, read, edit). Each turn looks like progress, so turn and budget caps catch it late and at full price.

`scripts/detect-loop.mjs` checks a JSONL log of tool calls, one `{"tool": "...", "args": {...}}` per line. Arguments are compared with stable key order (`{"a":1,"b":2}` equals `{"b":2,"a":1}`). It flags a call repeated N times in a row, or a 2 to 4 call cycle repeated N times.

```
node scripts/detect-loop.mjs calls.jsonl --max-repeats 3 --window 20 [--json]
```

Exit 0: no loop. 1: loop, with the call, the count and the line numbers. 2: unreadable input. This is a heuristic over what the caller logs, not something the Claude runtime provides; the docs cited below describe no loop detection. To enforce it mid-run, append each call to the log from a `PreToolUse` hook and reject the call when the check exits 1.

## 6. Lint the stop config before the run

Describe the run's limits in JSON and lint them before launch or in CI:

```
node scripts/check-stop-config.mjs stop-config.json
```

`scripts/stop-config.example.json` passes clean. Exit 1 with `ERROR <field>: ... Fix: ...` when: `maxTurns` is not a positive integer or `maxBudgetUsd` is missing or not positive; `budgetCheck` is `after-call`, or `before-call` without `perCallReserveUsd`; `retry.max` is above 0 without `idempotentOnly: true`; retries can hit writes (`retry.writes` is not `false`) with no `idempotencyKey`; `errorWindow` is missing or its size is below 3; `loopDetection` is missing or its window is smaller than `4 * maxRepeats`; `onLimit` is not `stop` or `escalate`. A missing `wallClockSeconds` is a warning. Exit 2 means the file is not readable JSON.

Tests for both scripts, both directions: `node --test` from this skill folder (Node 18 or later, no dependencies).

## Before an autonomous run ships

- Turn and budget caps are set in the runtime; the caller branches on every result subtype.
- Budget is reserved before each call; errors are counted over a window.
- Retries are idempotent-only and keyed for writes; loop detection runs on the logged calls.
- Irreversible actions (deploys, deletes, payments) need a human approval the runtime enforces; an unattended run denies prompts rather than waiting on them.
- `check-stop-config.mjs` exits 0 on the run's config.

Verified against code.claude.com cli-reference and agent-sdk/agent-loop on 2026-10-05.
