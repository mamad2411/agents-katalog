---
name: to-subtasks
description: Converts the current conversation context into an implementation-ready subtask plan with atomic, dependency-ordered steps and optional test pairing. Use when a planning/discovery conversation (including grill-me sessions) is complete and the next step is to break decisions into actionable subtasks for sequential implementation.
---

# To Subtasks

## Quick start

When the user asks to move from discussion to execution planning:

1. Read the current conversation context.
2. Extract decisions, constraints, assumptions, and open questions.
3. Produce a subtask list that can be implemented one by one.
4. If tests are agreed upon, pair test work with each relevant subtask.
5. Present the subtasks to the human for confirmation before execution.

## Workflow

### 1) Context digestion
- Identify final decisions from the conversation.
- Capture constraints (tech, scope, style, deadlines, dependencies).
- Detect whether a grill-me session has already been completed.
- If context came from a grill-me session, treat resolved branches as requirements.

### 2) Grill-me gate
- If no grill-me session is detected and important decisions are still unclear, do not present unresolved-items sections.
- Instead, recommend running a grill-me session first to resolve uncertainties before subtask planning.
- If a grill-me session is already completed, proceed directly to subtask generation.

### 3) Subtask generation
Create subtasks that are:
- Atomic: each can be implemented in one focused change set.
- Ordered: each step depends only on prior completed steps.
- Dependency-safe: every subtask appears only after all of its prerequisites are resolved.
- Reviewable: each step is scoped for clear implementation and validation.
- Traceable: each subtask maps back to one or more conversation decisions.

### 4) Test pairing (conditional)
If testing is requested or agreed:
- Attach test updates to each implementation subtask, not as one final bulk step.
- Specify test type per subtask (unit/feature/integration/e2e as appropriate).
- Define acceptance checks per subtask.

If testing is explicitly not desired:
- Note that in assumptions and proceed without test subtasks.

### 5) Human-ready presentation
Present subtasks as a structured numbered list only.
- If grill-me has already been run, output only the subtask list and nothing after it.
- Do not append sections after the list.

## Output format

Use this format when presenting to the human:

1. **Subtask N: <title>**
   - Goal:
   - Scope:
   - Deliverables:
   - Tests:

## Guardrails

- Do not start implementation; planning only.
- Do not combine unrelated concerns in one subtask.
- Prefer smaller subtasks when uncertain.
- Explicitly mark assumptions.
- Keep language concrete and execution-oriented.
- Always order subtasks so all dependencies are resolved before dependent work begins.
