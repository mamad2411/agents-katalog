---
name: task-breaker
description: "Converts spec + implementation plan into ordered, agent-executable tasks with dependency chains. Use when decomposing a plan into actionable work items."
---

# Task Breaker

## Overview

Transform a specification and implementation plan into ordered, bite-sized tasks that an AI coding agent can execute independently. Each task is self-contained, has a clear goal, specifies exact files, and orders by strict dependency chain.

**Core principle:** A TASK THAT CAN'T BE COMPLETED IN ONE SESSION IS NOT A TASK — IT'S A PROJECT.

## The Iron Law

```
EVERY TASK MUST BE COMPLETABLE IN A SINGLE AGENT SESSION WITH FULL CONTEXT
```

If a task requires knowledge from a task that hasn't been completed yet, it's ordered wrong. If it can't be verified independently, it's not a task.

## When to Use

**Use this when:**
- Spec + implementation plan are complete
- Before any coding begins (tasks feed the agent)
- User asks "break this into tasks"
- You need to estimate effort or assign work

## Project Context

Before significant work, check for a project glossary and decision log:
- If `CONTEXT.md` exists, use its ubiquitous-language glossary for all naming, and respect the decisions recorded in `docs/adr/`.
- If they are missing and the work is non-trivial, consider `/senior-dev-squad:grill` (alignment + glossary/ADR capture) or `/senior-dev-squad:setup-senior-dev-squad` first.

## Task Structure

Every task follows this format:

```markdown
### Task N: [Verb] [Component]

**Files:**
- Create: `src/path/to/file.ts`
- Modify: `src/path/to/existing.ts:45-78`
- Test: `tests/path/to/test.ts`

**Depends on:** Task N-1 (or: None)

**Goal:** What this task achieves in one sentence.

- [ ] Step 1: Write the failing test (if TDD)
- [ ] Step 2: Implement the minimal solution
- [ ] Step 3: Verify tests pass
- [ ] Step 4: Commit with conventional commit message
```

## Task Granularity Rules

| Scope | Task Count | Task Duration |
|-------|-----------|---------------|
| Weekend project | 15-30 tasks | 2-5 minutes each |
| MVP (1 month) | 50-100 tasks | 2-10 minutes each |
| Full product | 100-300 tasks | 5-15 minutes each |
| Enterprise | 300+ tasks | 10-30 minutes each |

## Phase Structure

Group tasks into phases with milestones:

```markdown
## Phase 1: Foundation (Tasks 1-5)
Project init, config, database schema, core types

## Phase 2: Core Features (Tasks 6-20)
Authentication, main CRUD operations

## Phase 3: UI (Tasks 21-40)
Pages, components, forms, states

## Phase 4: Integration (Tasks 41-50)
API integration, error handling, testing

## Phase 5: Polish (Tasks 51-60)
Performance, accessibility, edge cases, docs
```

## Red Flags — STOP

Tasks that say "implement all" instead of naming specific components. Tasks with vague files or no test step. Tasks ordered incorrectly (back-end references UI before it exists). Tasks that require "research" without a specific deliverable.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The tasks are obvious from the spec, no need to be granular" | Agents executing vague tasks make architectural decisions that conflict with each other. Granularity prevents drift. |
| "This is a small feature, one task is enough" | A single large task gives the agent no checkpoints. It will make ten micro-decisions you never approved. |
| "I'll add the file paths when I know what the structure looks like" | Without exact file paths, agents create their own structure. Divergence compounds across every subsequent task. |
| "The test step can be at the end of the phase" | Tests written after implementation verify the implementation as-built, not the acceptance criteria as-specified. |
| "Dependencies are implied by the task order" | Implicit dependencies get violated. Every task must state its dependency explicitly so the agent cannot reorder execution. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Why did the agent create a new folder instead of using the existing one?" — File paths were not specified in the task, so the agent improvised a structure.
- "Task 12 failed because Task 8 wasn't finished" — The dependency chain was not explicit, allowing tasks to be run out of order.
- "This is a massive commit, I can't review it" — Tasks were too coarse-grained; each task should produce a small, reviewable commit.
- "The agent skipped testing and went straight to the next task" — The test step was missing or optional-sounding rather than a required checklist item.
- "We're only halfway done but the task list is exhausted" — Scope was underestimated; phases were not sized against the actual feature surface area.

**When you see these:** STOP. Return to the task list, identify the structural deficiency (missing paths, missing dependency, missing test step, wrong granularity), correct those tasks, and re-run the verification checklist before continuing execution.

## Related Skills

- **spec-first-development** — provides spec this skill breaks down
- **architecture-planner** — provides file structure this skill references
- **agent-prompt-builder** — synthesizes tasks into execution prompt

## Verification

- [ ] Every task is completable in one session
- [ ] Tasks are in strict dependency order
- [ ] Each task specifies exact files (Create/Modify/Test)
- [ ] No task says "implement all" or similar vagueness
- [ ] Phases have clear milestones
- [ ] Test step exists for every implementation task
