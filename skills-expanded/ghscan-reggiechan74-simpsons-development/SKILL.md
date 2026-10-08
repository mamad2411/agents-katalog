---
name: ralph-protocol
description: "Ralph Wiggum iterative development protocol — naive self-referential loop for persistent iteration"
---

# Ralph Wiggum Protocol — Iterative Development

> "I'm learnding!"

## What This Is

A naive iterative development loop. The same prompt is fed to you repeatedly. Your work persists in files and git history between iterations. Each iteration, you see your previous work and improve on it.

Ralph doesn't know which phase he's in. He doesn't have phases. He just keeps trying until the job is done. That's the power: persistent iteration without overthinking.

## How It Works

1. You receive a prompt describing the task
2. You work on it — modify files, run tests, commit code
3. When you try to exit, the loop intercepts and feeds you the SAME prompt
4. You see your previous work in files and git history
5. You iterate and improve
6. When the task is genuinely complete, output your completion promise

## Principles

- **Iteration over perfection**: Don't try to get it right the first time. Get it working, then improve.
- **Failures are data**: Each failed attempt narrows the search space.
- **Persistence wins**: The loop never gives up. Trust the process.
- **Search first**: Before implementing, search the codebase.
- **Back pressure**: Tests, type checks, and linters are your quality gates.
- **One thing per iteration**: Focus on one task per loop cycle.

## When to Use

- Well-defined tasks with clear success criteria
- Tasks requiring iterative refinement
- Greenfield projects with test-driven development
- Bug fixes with clear reproduction steps

## When NOT to Use

- Tasks requiring human judgment or design decisions
- Subjective success criteria
- Production debugging

## Ralph in the Family

```
BEFORE --> DURING --> AFTER --> ALWAYS
Lisa       Ralph      Bart      Marge
                        |
                        v
                      Homer
```

Ralph runs during implementation. He's the simplest protocol — just iterate until done.

## Completion

Output your completion promise ONLY when genuinely true:
```
<promise>YOUR_PROMISE_TEXT</promise>
```

Do NOT lie to escape the loop.
