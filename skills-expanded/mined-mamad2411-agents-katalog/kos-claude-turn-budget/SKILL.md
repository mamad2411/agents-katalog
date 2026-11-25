---
name: kos-claude-turn-budget
description: Stay inside the MAX_TURNS budget of a zai/Claude workflow run by phasing work (investigate/implement/verify) and cutting re-reads, so runs do not hit turn_limit_hit or zero_turns.
user-invocable: true
when_to_use: "Any task running inside a run-zai workflow with a turn limit, or when a run failed with turn_limit_hit / produced no output."
category: utilities
argument-hint: "[task and max-turns]"
keywords: [turns, max-turns, budget, turn-limit, scope, efficiency, phasing]
related: [kos-zai-agent-runtime-contract, kos-zai-run-failure-prevention, kos-gh-automation-tooling]
metadata:
  author: kos-workflow-improvement
  attribution: turn-budget failure modes from run logs; phasing pattern distilled from observed run prompts
  license: repo
  version: "1.1"
---

# Idea

Every zai workflow pins `MAX_TURNS` (commonly 50–100; targeted PR tasks lower). Hitting the ceiling with `is_error` is a classified hard failure (`turn_limit_hit`); using zero turns is `zero_turns`. The fix is **phased budgeting**: decide up front how many turns investigation, implementation, and verification each get, and never re-derive context you already hold.

> **Attribution note:** the `≤6 / ≤20 / ≤6` allocation below is a *reusable phasing pattern observed in run logs* — it is **not** quoted from the current `pr-improve.yml` prompt (that YAML has no explicit allocation). Treat it as a sensible default to scale from, not a prompt mandate. The prompt's own `MAX_TURNS` (read from the workflow env) is the real ceiling.

## When to invoke this skill directly
- Your task runs inside a workflow run and you know the turn ceiling.
- A run failed `turn_limit_hit` and you are re-scoping before re-dispatch.

## References
- `run-zai` outputs: `claude_num_turns`, `claude_turns_budget_pct`; the `MAX_TURNS` env in each workflow YAML.
- `scan-claude-logs.cjs` → `turn_limit_hit`, `zero_turns`.
- [[kos-zai-agent-runtime-contract]] — verify with the prompt's commands inside the budget.

## Communication Style
State the ceiling, then the phase allocation as three numbers that sum under it. One line.

## Core Principles
YAGNI / KISS / DRY. Don't read a file twice — cache it in context. Don't investigate broadly when the task is narrow. Verification is the first thing to cut, not the last.

## The phased budget (default; scale to the real MAX_TURNS)

| Phase | Default share | Allowed actions | Stop when |
|---|---|---|---|
| Investigate | ~20% | read logs, grep, reproduce, locate code | root cause + target file identified |
| Implement | ~60% | edit files, run fixes, iterate | change compiles/lints |
| Verify | ~20% | run the prompt's gate | green (or known-failing documented) |

For a ~32-turn targeted task that is roughly ≤6 / ≤20 / ≤6; scale linearly for 50/70/100-turn runs.

## Your Approach
1. Read the ceiling from the workflow `MAX_TURNS` env (not a guess).
2. Before the first tool call, state the phase allocation.
3. Investigate to a root cause, not to comprehension.
4. Implement the smallest change; batch edits; one compile/lint pass.
5. Reserve the verify phase; if over budget, cut scope, not verification of what you changed.

## Anti-patterns seen in failed runs
- Re-reading the same file each turn (use what is in context).
- Exploring unrelated modules "for completeness."
- Running heavy installs mid-investigation (defer to verify).
- Spending the whole budget investigating, leaving zero for the fix (→ `turn_limit_hit`).
- Producing no tool calls at all (→ `zero_turns`).

## Process Flow (Authoritative)
1. **Declare** the ceiling (from `MAX_TURNS`) and the three phase numbers.
2. **Investigate** to a root cause, not comprehension.
3. **Implement** the smallest fix.
4. **Verify** with the prompt's real gate (no mocks/cheats).
5. Over budget at a phase boundary → narrow scope, don't silently exceed.

## Output Format
Plan line: `CEILING=N  inv/impl/verify = a/b/c (a+b+c < N)`. On finish: `TURNS_USED=x/N  PHASE=verify`.

## Critical Constraints
- Read the ceiling from `MAX_TURNS`, never assume.
- Never fake verification (no mocks/cheats to "pass").
- If the task genuinely needs more than the ceiling, say so rather than burning the run.
