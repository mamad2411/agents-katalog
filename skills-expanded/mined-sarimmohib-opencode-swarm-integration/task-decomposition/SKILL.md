---
name: task-decomposition
description: Break a complex coding task into file-level subtasks with acceptance criteria. Use when planning multi-file work, or when the user says decompose, break down, subtasks, or plan the implementation.
---

# Task Decomposition

Turn an ambiguous goal into an ordered list of executable subtasks, each
sized for one subagent in one round.

## Protocol

1. EXPLORE FIRST - Read the relevant code (read/glob/grep) before writing
   the plan. Every subtask must reference real files, not assumed ones.
2. Each subtask gets:
   - goal: one sentence, verifiable.
   - scope: exact files/functions it may touch.
   - acceptance criteria: how to confirm it is done (test, command, behavior).
   - dependencies: earlier subtasks it needs (empty = parallelizable).
3. Keep it minimal - smallest change satisfying the goal. Split along file
   boundaries so independent subtasks share no files and no state.
4. FLAG - Ambiguities, risky areas, and decisions needing the user. Never
   bury a guess inside a subtask; surface it.

The planner is read-only: describe changes in the plan, never attempt them.

## Output shape

Ordered list: parallelizable subtasks first (marked PARALLEL, group A/B),
then dependent ones. End with risks/open questions.
