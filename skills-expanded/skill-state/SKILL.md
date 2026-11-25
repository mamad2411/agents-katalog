---
name: skill-state
license: MIT
description: >
  Long-horizon execution skill for Claude. Use this skill when a task is
  multi-step, stateful, procedural, or tool-heavy. Maintain a compact structured
  execution state, update it every step, and discard intermediate reasoning after
  each validated transition. Suitable for workflows where future action depends
  on the current world state rather than full conversation history.
---

# SKILL.state

You are executing a procedural skill using explicit structured execution state.

## When to use
Use this skill automatically when the task:
- spans multiple steps or turns,
- depends on remembered facts, inventory, files, hypotheses, or active entities,
- requires tool calls over time,
- needs reliable recovery from interruptions, noise, or changing state,
- benefits from a bounded prompt instead of replaying full history.

## Core principle
The current structured state is the source of truth for future action.

Do not depend on prior transcript history unless the needed information has already been committed into the current state.

## Inputs each turn
You will receive:
1. Immutable task instructions.
2. Current structured execution state.
3. Latest observation from the environment.

You will not receive useful prior history beyond what is in the current state.

## What you must do
At every turn:
1. Read the current observation and state.
2. Reason about what changed and what should happen next.
3. Produce a minimal state patch containing only information needed for future execution.
4. Produce the next action.
5. Never preserve irrelevant reasoning, commentary, or obsolete observations.

## Output format
Return exactly one JSON object with these two keys:

```json
{
  "state_patch": {},
  "action": ""
}
