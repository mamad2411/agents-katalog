---
name: dispatching-parallel-agents
description: Run independent agents concurrently for unrelated tasks. Maximizes throughput when tasks have no shared state.
invoke_when: Use when multiple independent tasks need executing simultaneously, such as fixing unrelated bugs, implementing features in separate modules, or running parallel research.
---

# Dispatching Parallel Agents

## When to Parallelize

Tasks are safe to parallelize when:
- They touch **different files** (no merge conflicts)
- They have **no shared state** (no race conditions)
- They are **independently verifiable** (each has its own test)
- The **order doesn't matter** (no dependency chain)

## Dispatch Pattern

### 1. Identify Independent Tasks
From the plan, group tasks by independence. Tasks that modify the same files are NOT independent.

### 2. Craft Parallel Prompts
Each agent gets:
- Its specific task with full context
- Architecture constraints relevant to its scope
- Clear file boundaries (what it owns, what it must not touch)
- Its own verification command

### 3. Launch Simultaneously
Use multiple Agent tool calls in a single message. This is critical — sequential launches waste time.

### 4. Collect and Review
When all agents complete:
- Review each result independently
- Check for unintended overlaps
- Run the full test suite (not just individual tests)
- Verify the combined changes work together

## Anti-Patterns

- Parallelizing tasks that share files (creates merge conflicts)
- Launching agents sequentially when they could be parallel
- Not running integration tests after combining parallel results
- Giving agents overlapping file ownership

## Example

Two bugs in separate modules:
```
Agent 1: Fix user service validation bug (src/services/user.ts, tests/user.test.ts)
Agent 2: Fix order API pagination (src/routes/orders.ts, tests/orders.test.ts)
```
These are safe to parallelize — different files, different concerns.
