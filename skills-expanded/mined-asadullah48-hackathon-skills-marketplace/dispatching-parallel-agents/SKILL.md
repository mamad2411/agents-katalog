---
name: dispatching-parallel-agents
description: Use when facing 2+ independent failures across different problem domains that can be investigated concurrently without shared state or sequential dependencies
---

# Dispatching Parallel Agents

## Overview

When multiple independent failures exist, investigate them in parallel rather than sequentially.

**Core principle:** One agent per independent problem domain, running concurrently.

**Announce at start:** "I'm using the dispatching-parallel-agents skill to investigate multiple independent failures."

## When to Use

**Use when:**
- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- Each problem can be understood without context from others
- No shared state between investigations

**Don't use when:**
- Failures are related (fixing one might fix others)
- Need to understand full system state
- Agents would interfere with each other

## The Pattern

### 1. Identify Independent Domains

Group failures by what's broken:
- File A tests: Tool approval flow
- File B tests: Batch completion behavior
- File C tests: Abort functionality

### 2. Create Focused Agent Tasks

Each agent gets:
- **Specific scope:** One test file or subsystem
- **Clear goal:** Make these tests pass
- **Constraints:** Don't change other code
- **Expected output:** Summary of findings and fixes

### 3. Dispatch in Parallel

Dispatch each agent task concurrently with the Task tool.

### 4. Review and Integrate

When agents return:
- Read each summary
- Verify fixes don't conflict
- Run full test suite
- Integrate all changes

## Agent Prompt Structure

Good agent prompts are:
1. **Focused** - One clear problem domain
2. **Self-contained** - All context needed
3. **Specific about output** - What should be returned?

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| "Fix all the tests" | "Fix agent-tool-abort.test.ts" |
| No context | Paste error messages and test names |
| No constraints | "Do NOT change production code" |
| Vague output | "Return summary of root cause and changes" |

## Key Benefits

1. **Parallelization** - Multiple investigations happen simultaneously
2. **Focus** - Each agent has narrow scope
3. **Independence** - Agents don't interfere
4. **Speed** - N problems solved in time of 1

## Red Flags - STOP

- Related failures that might affect each other
- Need for full system context
- Exploratory debugging without clear problem
- Shared state between investigations
