---
name: loop-engineer
description: >-
  Set up, scaffold, and administer agentic loops in Claude Code — headless
  while-loops around `claude -p`, evaluator-optimizer (generator/critic) loops,
  meta / prompt-refinement loops (a loop that refines the prompts another loop
  runs), and orchestrator fan-out. Every loop ships with non-negotiable
  guardrails: a verifiable exit condition, a max-iteration cap, and in-code
  budget enforcement. Use whenever the user wants to build, design, run, wire,
  or supervise loops / agent loops / "loop engineering" / nested sub-loops, or
  asks how to make Claude prompt Claude on a schedule or until a goal is met.
---

# Loop Engineer

Loops are the third object of attention in coding: **source code → agent → loop.**
Your job with this skill is to turn a user's goal into the *right* loop pattern,
scaffolded with guardrails so it can't "loopmaxx" (run forever against a vague
objective and burn money).

## The one rule that prevents most disasters

**Refuse to build a loop without a binary, verifiable exit condition.** "Improve
the UX" has no pass/fail and produces infinite loops + large API bills. "Make
`npm test` exit 0" does. If the user's goal isn't binary, your first job is to
help them make it binary — not to scaffold the loop.

## Decision tree — pick the pattern

```
Is the goal one binary check the agent iterates toward (tests pass, lint clean)?
│
├─ YES, one agent is enough .......................... HEADLESS WHILE-LOOP
│        (templates/headless-loop.sh)                  or first-party /goal
│
├─ Quality matters & "done" is a judgment call ...... EVALUATOR-OPTIMIZER
│        (writing, code that must meet a bar)          (templates/evaluator-optimizer.sh)
│        → ALWAYS a separate critic agent
│
├─ You're improving the PROMPT itself, not the output  META / PROMPT-REFINEMENT
│        (a loop that rewrites the prompt another      (templates/meta-prompt-refine.sh)
│         loop runs, scored on a test set)             → needs holdout + anchor set
│
├─ Subtasks can't be predicted up front ............. ORCHESTRATOR FAN-OUT
│        (delegate dynamically, then verify each)      (templates/fanout-orchestrator.sh
│                                                        or the Workflow tool)
│
└─ Just run something on a schedule / interval ...... /loop or cloud Routines
         (poll, babysit PRs, recurring checks)         (reference/primitives.md)
```

Nest these: an **orchestrator** loop can spawn **evaluator-optimizer** inner loops;
a **meta** loop wraps a **headless** loop and rewrites its prompt between runs.

## Non-negotiable guardrail checklist

Before scaffolding ANY loop, confirm all five. See `reference/guardrails.md` for the why.

1. **Verifiable exit condition** — a command/check that returns binary done/not-done.
2. **Max-iteration cap** — a hard `for` bound, enforced in code, not in the prompt.
3. **Budget cap in code** — sum `total_cost_usd` from `--output-format json`; stop
   *before* the next call when over budget. Alerts are not enforcement.
4. **Sandbox** — loops that edit files/run commands run in a worktree, container,
   or branch — never unattended on `main`.
5. **Human checkpoint** — for anything outward-facing (push, deploy, send), the
   loop stops and asks, or only proposes.

A loop missing #1 or #2 is a bug, not a loop. Don't ship it.

## How to use this skill

1. Read the user's goal; map it to a pattern via the decision tree.
2. If the goal isn't binary/verifiable, fix that first (with the user).
3. Copy the matching template from `templates/`, fill the config block, and wire
   the real exit check. Keep the guardrails.
4. Walk the user through the five-point checklist for their specific loop.
5. Tell them how to run it, how to stop it, and what it costs per iteration.

## Reference (load as needed)

- `reference/primitives.md` — every Claude Code loop primitive: `claude -p`,
  `--continue`/`--resume`, `--output-format json` (cost), `/loop`, `/goal`,
  Tasks (`~/.claude/tasks`, `CLAUDE_CODE_TASK_LIST_ID`), cloud Routines.
- `reference/taxonomy.md` — the five patterns in depth + when to use each.
- `reference/guardrails.md` — failure modes (loopmaxxing, cost blowups, evaluator
  collusion/drift) and the mitigations, with the cautionary numbers.
- `templates/*.sh`, `templates/goal-loop.md` — runnable scaffolds.

## What NOT to claim

Anthropic's *Building Effective Agents* is the canonical taxonomy source, but it
does **not** officially endorse "shell fan-out loops" or "headless-in-CI with Task
tracking" — those are community patterns. Attribute them as such.
