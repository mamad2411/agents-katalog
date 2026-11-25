---
name: plan-and-scope
description: "Creating a structured, phased implementation plan before coding: goals, in/out scope, dependencies, risks. Apply at the start of any new feature, refactor, or project."
---

# Skill: Plan and Scope

## Purpose
Guide the creation of a structured, phased implementation plan before any code is written.

## When to Use
At the start of any new feature, refactor, or project. Always plan before executing.

## Process

### 1. Clarify the Goal
- What is the end-user outcome?
- What are the constraints (time, tech, compatibility)?
- What already exists that we're building on?
- If a PRD exists (`*-prd.md`), read it — scope and goals are already defined. Focus on dependencies, risks, and phasing.
- If a UX spec exists (`*-ux-spec.md`), read it — reference states, flows, and affordances when defining phase tasks.

### 2. Define the Scope
- List what IS in scope (be specific)
- List what is NOT in scope (be explicit — this prevents creep)
- Identify assumptions that need validation

### 3. Map Dependencies
- What existing code/APIs/services does this touch?
- Are there cross-repo dependencies (backend ↔ frontend)?
- What needs to exist before this can start?
- **Repo strategy:** Will this be a monorepo (single `fullstack` profile) or separate repos per concern (e.g., `django-api` + `nextjs`)? Ask the user — this affects how `/scaffold` creates sub-projects and how phases are organized.

### 4. Identify Risks
- What could go wrong?
- What are we unsure about technically?
- Where might the plan need to change?

### 5. Produce the Plan Document
Output a `plan.md` with this structure:

```markdown
# Plan: [Feature Name]

## Goal
One paragraph describing the desired outcome.

## Scope
### In Scope
- ...

### Out of Scope
- ...

## Phases
Grouping and ordering only. Each phase's internal structure — objective, input,
tasks, output, suggested skills, branch, verification checklist — follows the
`phase-breakdown` skill; don't duplicate those fields here. Tag every phase with
its `[directory/]` and mark parallel groups and sync points.

## Parallel Group A (Phases 1-2)
### Phase 1: [Backend — Name] [server/]
### Phase 2: [Frontend — Name] [web/]

## Sync Point: [e.g., Integration Summary]

## Phase 3: [Name] [directory/]
...

## Repo Strategy
Monorepo / Separate repos: [choice]
Sub-projects: [e.g., api (django-api), web (nextjs)]

## Dependencies
- ...

## Risks & Open Questions
- ...

## Cross-Repo Notes
- Backend contract changes needed: Y/N
- Frontend integration summary required: Y/N
```

## Key Principles
- Plans are living documents — update them as you learn
- Each phase should be independently reviewable (own branch, own PR)
- A plan that's too detailed upfront is as bad as no plan — aim for clarity on WHAT, flexibility on HOW
- Keep phases small — the `phase-breakdown` skill owns the sizing rule (target: 1-3 hours of focused execution, reviewable in a single PR). If a phase feels too big, split it.
