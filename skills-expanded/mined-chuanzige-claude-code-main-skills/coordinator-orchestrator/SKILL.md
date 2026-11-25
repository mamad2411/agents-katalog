---
name: coordinator-orchestrator
description: Use when coordinating multi-step work across workers or subagents, especially when research, implementation, and verification should be split while the main agent stays responsible for synthesis and user communication
---

# Coordinator Orchestrator

## Overview

Act as the coordinator, not the extra pair of hands. Launch workers for research, implementation, and verification, but keep planning, synthesis, and user-facing judgment on the main thread.

This pattern is grounded in `src/coordinator/coordinatorMode.ts`: the coordinator owns decomposition, prompt quality, result synthesis, and communication.

## Core Rules

- Treat workers as specialists, not proxies for your own understanding.
- Delegate research, implementation, and verification. Keep prioritization, synthesis, and tradeoff decisions local.
- Do not send one worker to inspect another worker's work.
- Do not delegate trivial file reads or shell commands that you can do directly.
- After launching workers, tell the user what you launched and stop. Do not predict results before they arrive.

## Workflow

1. Decompose the task into research, synthesis, implementation, and verification.
2. Launch independent read-only research in parallel.
3. Read the findings yourself and decide what they mean.
4. Write a concrete implementation spec with file paths, line numbers, constraints, and done criteria.
5. Choose whether to continue an existing worker or spawn a fresh one.
6. Send verification to a fresh verifier when independence matters.
7. Summarize progress to the user as worker results arrive.

## Synthesis Duty

Your main job is to understand worker output before issuing follow-up work.

Never write prompts like:

- "Based on your findings, fix the bug."
- "The other worker found an issue. Please implement it."

Write prompts like:

- "Fix the null pointer in `src/auth/validate.ts:42`."
- "Update `src/foo.ts` and `src/foo.test.ts` to preserve the old error contract."
- "Run the relevant tests and report the commit hash."

If you cannot explain the change precisely, you have not finished the synthesis step.

## Continue Or Spawn

Continue the same worker when:

- it just researched the exact files that now need editing
- it just failed a test and already has the error context
- it is extending its own recent change

Spawn a fresh worker when:

- the previous context is broad or noisy
- the first attempt anchored on the wrong approach
- you want independent verification
- the new task is unrelated

## Anti-Patterns

- Lazy delegation: handing off understanding instead of synthesizing it
- Worker ping-pong: using one worker to check on another
- Context pollution: reusing a worker when a clean slate would be better
- Premature narration: telling the user results that have not arrived yet

## Prompt Checklist

Before sending work to a worker, include:

- the purpose of the task
- exact files or search area
- specific lines, symbols, or failure modes when known
- whether files may be modified
- the verification expected before reporting done
- the exact output you want back

## Done Condition

You have applied this skill correctly when the coordinator remains the decision-maker, workers receive self-contained tasks, and every follow-up prompt proves that you understood the previous results.
