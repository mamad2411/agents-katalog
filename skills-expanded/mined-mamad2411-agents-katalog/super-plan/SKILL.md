---
name: super-plan
description: Analyzes a task, explores the codebase, asks clarifying questions, and produces a phased implementation plan in `PLAN.md` or `plans/<task-name>.md`. Use for complex features, refactors, migrations, architectural work, or any multi-step change that needs balanced phases, dependencies, risks, and execution-ready tasks.
metadata:
  author: gurbakhshish
  source: adapted from /home/gurbakhshish/dev/src/github/opencode/agents/super-plan.md
  spec: https://agentskills.io/specification
---

# Super Plan

Create an implementation plan only. Do not implement code while this skill is active unless the user explicitly changes the task.

## When to use

Use this skill when:

- the task is complex enough to benefit from phased execution
- the work spans multiple files, systems, or decision points
- the user asks for a plan, roadmap, breakdown, or implementation strategy
- the change includes refactors, migrations, architecture updates, or risky edits
- a future executor should be able to complete the work phase by phase with minimal extra context

Do not use this skill for tiny one-step changes unless the user explicitly wants a written plan.

## Core behavior

- Plan only. Do not silently switch from planning to implementation.
- Explore before planning. Base the plan on the actual repository, not guesses.
- Ask focused clarifying questions when requirements, constraints, or priorities are ambiguous.
- Break work into balanced phases that are meaningful, reviewable, and independently executable.
- Prefer plans that can survive handoff: each phase should contain enough context for another agent or human to execute it.
- Keep the skill harness-agnostic. Refer to capabilities generically, not by product-specific tool names.
- After writing the plan, summarize it for the user without pasting the entire file back into chat unless asked.

## Planning workflow

1. Understand the request
   - Restate the planning goal internally.
   - Identify unknowns, constraints, and success criteria.
   - If a missing decision materially changes the plan, ask the user before finalizing it.

2. Explore the codebase
   - Inspect relevant files, structure, conventions, dependencies, and existing patterns.
   - Look for architecture boundaries, integration points, risk areas, and any related tests or docs.
   - Prefer evidence from the repository over assumptions.

3. Detect repository context
   - Check whether the project appears to use version control.
   - If version control is relevant to execution planning, ask the user which checkpointing strategy they prefer.
   - Keep the wording generic and workflow-oriented rather than tied to a specific harness.

4. Design balanced phases
   - Each phase should usually represent roughly 30-90 minutes of focused work.
   - A phase must be self-contained, have clear prerequisites, define outputs, and include verification criteria.
   - Avoid micro-phases that create coordination overhead without producing a meaningful checkpoint.
   - Split oversized phases that mix unrelated outcomes or become difficult to review.
   - Mark phases that can run in parallel.

5. Choose the plan destination
   - Ask the user where to save the plan before writing it.
   - Offer:
     - `PLAN.md` in the repository root
     - `plans/<task-name>.md` for organized multi-plan workflows
   - If using the `plans/` option, generate a kebab-case filename from the task and let the user adjust it.

6. Write exactly one plan file
   - The plan file is the main deliverable.
   - Keep it structured, concrete, and updateable during execution.

7. Summarize for the user
   - Give a concise recap of the overall approach, main phases, major risks or open questions, and saved file path.

## Plan requirements

Structure the plan so it is easy to execute and maintain during implementation.

### Recommended sections

```md
# Implementation Plan: <Task Name>

## Overview
## Global Context
## Architecture Decisions
## Assumptions
## Phase Strategy
## Phases
## Phase Dependencies
## Risks
## Questions for User
```

### Phase template

Each phase should include:

- `Objective`
- `Status: Not Started`
- `Complexity`
- `Estimated Time`
- `Prerequisites`
- `Context for this Phase`
- `Files` table
- `Implementation Tasks` as markdown checkboxes
- `Execution Tracking Rules`
- `Verification`
- `Completion Gate`
- `Outputs`

### Execution tracking rules

Write phases so the plan can be updated during implementation:

- Initial status must be `Not Started`.
- When execution begins, the phase status should become `In Progress` before phase-specific workflow setup.
- Completed tasks should be checked off.
- Skipped or superseded tasks should be struck through rather than falsely marked done.
- A phase should become `Complete` only after the user reviews the result and explicitly confirms it is done.
- If the project uses a checkpointing workflow, cleanup/finalization for that phase should happen immediately after user-confirmed completion.

## Version-control guidance

If the repository uses version control and the user wants workflow guidance, include one strategy section matching their choice. Keep the terminology universal and describe the workflow by intent.

Possible strategies:

- separate working directories for each phase
- separate feature branches for each phase
- checkpoint tags on a shared branch
- decide the strategy separately when each phase starts

For the chosen strategy, explain:

- how execution starts for a phase
- how dependencies affect later phases
- what must happen when the user confirms the phase is complete
- how to avoid leaving unfinished phase state behind

Do not depend on harness-specific commands or tool names in the skill text.

## Quality bar

A good plan produced by this skill should:

- reflect real repository findings
- surface important assumptions and risks
- provide enough context for handoff to another executor
- keep sibling phases reasonably balanced
- give objective verification criteria where possible
- avoid vague steps such as "update code as needed"

## Important rules

- Do not implement code while acting in planning mode.
- Do not invent repository details you have not inspected.
- Ask at most the focused questions needed to remove meaningful ambiguity.
- Keep plan instructions executable across different agentic environments.
- Do not mention product-specific tool names unless the user explicitly asks for a harness-specific variant.
- After saving the plan, respond with a concise summary and the saved path.
