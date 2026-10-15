---
name: simple-plan
description: Analyzes a small task, explores only the directly relevant context, asks clarifying questions only when necessary, and produces a single-phase implementation plan in `PLAN.md` or `plans/<task-name>.md`. Use for simple, low-risk changes that should be implemented in one focused pass.
metadata:
  author: gurbakhshish
  source: adapted from https://github.com/singh-gur/agent_skills/tree/main/super-plan
  spec: https://agentskills.io/specification
---

# Simple Plan

Create a concise, single-phase implementation plan only. Do not implement code while this skill is active unless the user explicitly changes the task.

## When to use

Use this skill when:

- the task is simple enough to implement in one focused phase
- the work is low-risk and has a clear expected outcome
- the user asks for a lightweight plan, short plan, simple plan, or single-phase plan
- a future executor should be able to complete the task without a multi-phase roadmap

Do not use this skill for complex features, broad refactors, migrations, architectural changes, or work that should be split into multiple reviewable phases. If the user explicitly chose this skill for a task that appears too complex, warn that the task may be too large for a simple single-phase plan, then keep the plan constrained to the safest useful single phase instead of switching workflows automatically.

## Core behavior

- Plan only. Do not silently switch from planning to implementation.
- Keep the plan single-phase. If the full task cannot fit safely in one phase, say so and plan only the safest useful single-phase slice unless the user asks to change workflows.
- Explore before planning, but keep exploration proportional to the task.
- Ask focused clarifying questions only when missing information would materially change the plan.
- Prefer practical, execution-ready steps over exhaustive analysis.
- Keep the skill harness-agnostic. Refer to capabilities generically, not by product-specific tool names.
- After writing the plan, summarize it for the user without pasting the entire file back into chat unless asked.

## Planning workflow

1. Understand the request
   - Identify the expected outcome, likely files, success criteria, and obvious constraints.
   - Confirm the task is suitable for one implementation phase.
   - If the full task is not suitable for one phase, explain why and warn that the task may be too complex for a simple plan. Do not switch workflows automatically; constrain the output to the safest useful single-phase plan.

2. Explore the directly relevant context
   - Inspect the files, structure, conventions, dependencies, and tests directly related to the task.
   - Avoid broad repository surveys unless needed to avoid a bad plan.
   - Base the plan on observed repository facts, not guesses.

3. Choose the plan destination
   - Ask the user where to save the plan before writing it.
   - Offer:
     - `PLAN.md` in the repository root
     - `plans/<task-name>.md` for organized multi-plan workflows
   - If using the `plans/` option, generate a kebab-case filename from the task and let the user adjust it.

4. Write exactly one plan file
   - The plan file is the main deliverable.
   - Keep it concise, concrete, and easy to execute in one pass.
   - For optional sections with no content, write `None` instead of leaving them blank.

5. Summarize for the user
   - Give a concise recap of the objective, key steps, verification, open questions if any, and saved file path.

## Plan requirements

Structure the plan so it can be executed without extra planning.

### Recommended sections

```md
# Simple Implementation Plan: <Task Name>

## Overview

## Relevant Context

## Assumptions

## Single-Phase Plan

## Files

## Implementation Tasks

## Verification

## Risks

## Questions for User
```

Use `None` for optional sections that do not apply, especially `Assumptions`, `Risks`, `Outputs`, and `Questions for User`.

### Compact output template

```md
# Simple Implementation Plan: <Task Name>

## Overview

<1-3 sentences describing the desired outcome.>

## Relevant Context

- <Observed repository fact or directly relevant file/pattern.>

## Assumptions

- <Assumption, or `None`.>

## Single-Phase Plan

- Objective: <single objective>
- Status: Not Started
- Complexity: <Low|Medium>
- Estimated Time: <estimate>
- Context: <brief execution context>

## Files

| Path     | Purpose               |
| -------- | --------------------- |
| `<path>` | <inspect/change/test> |

## Implementation Tasks

- [ ] <Concrete task>
- [ ] <Concrete task>

## Verification

- [ ] <Command, test, or manual check>

## Completion Gate

<User review and explicit confirmation that the single phase is complete.>

## Outputs

- <Expected changed files, tests, or deliverables.>

## Risks

- <Risk, or `None`.>

## Questions for User

- <Question, or `None`.>
```

### Single-phase template

The single phase should include:

- `Objective`
- `Status: Not Started`
- `Complexity`
- `Estimated Time`
- `Context`
- `Files` table
- `Implementation Tasks` as markdown checkboxes
- `Verification`
- `Completion Gate`
- `Outputs`

### Execution tracking rules

Write the plan so it can be updated during implementation:

- Initial status must be `Not Started`.
- When execution begins, the phase status should become `In Progress`.
- Completed tasks should be checked off.
- Skipped or superseded tasks should be struck through rather than falsely marked done.
- The phase should become `Complete` only after the user reviews the result and explicitly confirms it is done.

## Quality bar

A good plan produced by this skill should:

- fit in one implementation phase
- reflect the directly relevant repository context
- make assumptions and open questions explicit
- list concrete files likely to change or inspect
- include objective verification steps where possible
- avoid vague tasks such as "update code as needed"
- stay brief enough to be useful for simple work

## Important rules

- Do not implement code while acting in planning mode.
- Do not invent repository details you have not inspected.
- Ask at most the focused questions needed to remove meaningful ambiguity.
- Do not create multiple phases. If multiple phases seem necessary, warn the user that the task may be too complex for a simple plan and constrain the output to the safest useful single-phase plan.
- Do not include phase dependency graphs, version-control strategies, broad architecture decision records, migration plans, or multi-phase roadmaps unless the user explicitly asks.
- Do not mention product-specific tool names unless the user explicitly asks for a harness-specific variant.
- After saving the plan, respond with a concise summary and the saved path.
