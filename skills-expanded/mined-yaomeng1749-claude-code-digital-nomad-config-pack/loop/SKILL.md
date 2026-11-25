---
name: loop
description: Run a bounded autonomous work loop with explicit stop conditions, status checks, and verification. Use when the user asks to keep iterating, run a loop, monitor progress, continue until passing, or execute repeated improve-test-review cycles.
origin: ECC automation-pack
---

# Loop

Use this skill to run supervised autonomous loops without drifting from the user's goal.

## Loop Contract

Before starting, define:

- objective: the concrete target state
- cadence: how often to check or iterate
- max rounds or time limit
- stop conditions
- rollback or pause conditions
- verification signal

If the user did not specify limits, choose conservative defaults:

- max rounds: 5
- pause on destructive operations, unclear requirements, credential exposure, or repeated identical failure
- verify after every round with the closest reliable check

## Iteration Pattern

For each round:

1. Inspect current state and last failure.
2. Select the smallest next action.
3. Execute the action.
4. Run the agreed verification.
5. Record status:
   - `LOOP_CONTINUE`: progress made, more work remains
   - `LOOP_PASS`: objective met
   - `LOOP_BLOCKED`: needs user input or external resource
   - `LOOP_STOP`: unsafe or no useful progress

## When To Stop

Stop immediately when:

- the objective is met
- the same failure repeats after two different fixes
- a security or privacy issue appears
- changes would exceed the requested scope
- tests require unavailable external services and no safe mock exists
- continuing would require destructive file, database, or git operations not requested by the user

## Status Report

For long loops, provide compact updates:

- round number
- action taken
- verification result
- next action or stop reason

Final report should include:

- final status
- changed files or artifacts
- verification commands and results
- remaining risks or manual follow-up

## Related Skills

Combine with:

- `verification-before-completion` before claiming completion
- `systematic-debugging` when failures are unclear
- `requesting-code-review` for substantial code changes
- `simplify` when the loop is fighting unnecessary complexity
