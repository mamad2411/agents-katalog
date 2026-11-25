---
name: subagent-driven-development
description: Dispatch fresh subagents per task with precisely crafted instructions. Two-stage review (spec compliance + code quality) ensures high-quality output.
invoke_when: Use when implementing a plan with multiple tasks, dispatching independent tasks for isolated execution, or when the user requests subagent-driven development.
---

# Subagent-Driven Development

## Why Subagents?

Fresh subagents per task provide:
- **Context isolation** — no accumulated confusion from prior tasks
- **Precise instructions** — each agent gets exactly what it needs
- **Parallel execution** — independent tasks run simultaneously
- **Quality gates** — two-stage review catches issues early

## Dispatch Pattern

For each task in the plan:

### 1. Craft the Subagent Prompt

Include:
- **Task description** — what to build, with exact file paths
- **Architecture constraints** — relevant Mandatory Rules from architecture.md
- **Testing requirements** — what tests to write (TDD: test first)
- **Verification command** — what to run to prove it works
- **Boundaries** — what files NOT to touch, what patterns to follow

### 2. Launch the Subagent

Use the Agent tool with a clear, complete prompt. The subagent should be able to work autonomously without asking questions.

### 3. Two-Stage Review

#### Stage 1: Spec Compliance
- Does the output match the task requirements?
- Are all specified files created/modified?
- Do the tests cover the required behavior?

#### Stage 2: Code Quality
- Does it follow architecture.md conventions?
- Is error handling proper?
- Are there security concerns?
- Is the code readable and maintainable?

### 4. Fix Loop

If either stage fails:
1. Identify specific issues
2. Send fixes back to a new subagent (or fix directly)
3. Re-review until both stages pass

## When to Use Subagents vs Direct Execution

- **Subagents**: independent tasks, well-defined scope, tasks that benefit from fresh context
- **Direct**: quick fixes, tasks that depend on conversation context, exploratory work

## Key Rule

Each subagent gets the FULL context it needs. Never assume a subagent knows something from the parent conversation.
