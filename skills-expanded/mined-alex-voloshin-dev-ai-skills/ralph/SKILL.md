---
name: ralph
description: Use this skill when iterating a task until a binary success condition holds (test passes, schema validates, output matches a regex) and a power user wants a standalone RALF (Read-Act-Learn-Feedback) iteration loop — to wrap the task in a feedback loop with a mechanically-verifiable oracle and a kill-on signal. Not for open-ended exploration — use /spike for that.
context: fork
argument-hint: "<task description>"
---

# /ralph — RALF Iteration Loop

Standalone Read-Act-Learn-Feedback loop. Iterate any task until a mechanically-verifiable success signal triggers, or a kill-on signal halts the loop. Caps prevent runaway cost.

## When to use

- "Write code until `cargo test` exits 0"
- "Generate test cases until rubric scores ≥ 4.0"
- "Refactor until linter is clean"
- "Convert this YAML to JSON until schema validates"

**Not for:** open-ended exploration (use `/spike`), code where you'd rather review the plan first (use `/plan` then `/develop`), or anything without a binary success oracle.

## Invocation

```
/ralph "<task>" --oracle <type:value> --kill-on <type:value> [--max-iterations N] [--token-budget N] [--time-cap-minutes N]
```

Examples:
```
/ralph "write a Rust CLI that parses CSV" --oracle cli:./test-cli.sh --kill-on oracle-pass
/ralph "generate 100 test cases for /develop rubric" --oracle judge:test-case-rubric.md --kill-on oracle-pass --max-iterations 8
/ralph "fix flaky test in src/api/login.test.ts" --oracle cli:./run-tests.sh --kill-on same-error-repeats:3
```

## Required arguments

Both required — skill rejects invocation if either is missing per `ralph-budget.md` rule.

### `--oracle <type:value>`

| Type | Format | Pass condition |
|---|---|---|
| `cli` | `cli:./script.sh` | Exit 0 |
| `judge` | `judge:rubric-name.md` | `eval-judge` agent score ≥ rubric threshold |
| `regex` | `regex:./out.log:^DONE$` | Pattern matches in named file |
| `python` | `python:./check.py` | Exit 0 |

### `--kill-on <type:value>`

| Type | Format | Trigger |
|---|---|---|
| `oracle-pass` | (no value) | Happy stop on first oracle success |
| `same-error-repeats` | `same-error-repeats:N` | Same error string N iterations in a row |
| `regex` | `regex:PATTERN` | Pattern matches in latest model output |
| `python` | `python:./kill.py` | Custom predicate exits 2 |
| `no-progress` | `no-progress:N` | N iterations with no file diff |

## Caps (defaults from `userConfig`)

| Cap | Default | userConfig override |
|---|---|---|
| `--max-iterations` | 10 | `ralph_default_max_iter` |
| `--token-budget` | 200_000 | `ralph_default_token_budget` |
| `--time-cap-minutes` | 120 | `ralph_default_time_cap_minutes` |

Session-aggregate caps from `ralph-budget.md` HIGH-3 also apply (20 iter / 400K tokens / 180 min across all RALF runs in one session).

## State and logs

Every run writes to `<repo>/.ai-skills-memory/ralph/<run-id>/`:
- `config.json` — caps + oracle + kill-on as locked at start
- `active.lock` — presence = run is in progress
- `initial-prompt.md` — full init prompt (G10)
- `iter-NNN/` — one dir per iteration: `prompt.md`, `output.md`, `diff.patch`, `oracle-result.json`, `tokens.json`
- `budget.json` — final totals on exit

Per-iteration `tokens.json` (v0.1.6) records `tokens` spent that iteration plus `runaway: true` when a single iteration exceeds 3× the fair share (`token_budget / max_iterations`). Runaway warnings also append to `.ai-skills-memory/ralph-warnings.log`.

## Init vs continuation prompts

- **Iter 1 (init):** full task brief — goal, constraints, evidence, output contract, oracle definition, kill-on signal. Typically 5–15K tokens
- **Iter ≥ 2 (continuation):** state delta only — last-iter diff + oracle failure summary + top-3 active constraints + kill-on countdown. Typically 1–3K tokens (~70% savings)

Continuation template at `${CLAUDE_PLUGIN_ROOT}/skills/ralph/templates/continuation-prompt.md` — applied automatically by `ralph-stop.py` hook.

## Memory writes

| Layer | When | Shape |
|---|---|---|
| L4 | RALF terminal state | `.ai-skills-memory/ralph/<run-id>/budget.json` (iterations, tokens, exit reason) |
| L4 | After kill or oracle-pass | `.ai-skills-memory/ralph-history.jsonl` summary line |

## Failure modes

- **Missing `--oracle` or `--kill-on`:** rejected at arg validation with clear error
- **Oracle script crashes (exit ≠ 0 AND ≠ 2):** treated as `ORACLE_ERROR`, loop killed, diagnostic surfaced
- **Hard cap hit:** soft warn at threshold, hard pause at cap, user prompted to confirm continuation, raise budget, or abort
- **Buggy `ralph-stop.py` hook:** hook fails open per `failure-recovery.md`; never blocks Stop

## Integration

- **Hooks**: `ralph-stop.py` (Stop event) drives the loop, writes per-iter state, enforces budgets; `ralph-iter-meter.py` (PostToolUse, v0.1.6) estimates per-iter token spend
- **Rule**: `ralph-budget.md` (caps, oracle/kill-on contract, failure modes)
- **Schemas**: `plugin/schemas/spawn-payload.schema.json` if RALF spawns subagents
- **Templates**: `plugin/skills/ralph/templates/continuation-prompt.md` (G10)
- **Used by**: `/feature-design`, `/develop`, `/bugfix`, `/refactor`, `/migrate` for embedded RALF segments
