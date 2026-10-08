---
name: write-task-todo
description: Use after task analysis when a non-trivial repository task needs a structured docs/todolist.md with [x]/[ ] items, data/type/interface-first ordering, explicit non-goals, tests, and loop-ready execution slices.
---

# Write Task Todo

Use this skill after `analyze-task` **and after the analysis has been discussed and aligned** when a task is large enough to need multiple implementation loops, commits, reviews, or cross-layer coordination.

This skill turns an analysis result into a **single working task document**:

- `docs/todolist.md`

## Purpose

Create a todo that is:

- structured
- execution-friendly
- test-aware
- biased toward definitions and interfaces before UI

This skill is **not** for coding and **not** for long-form design writing.

## Core rules

1. Use a single working todo file
   - default path: `docs/todolist.md`

2. Do **not** create a parallel source-of-truth doc at the start
   - put evolving definitions in the todo first
   - once a concept becomes stable and long-lived, promote that part into `docs/source-of-truth/*`
   - after promotion, the todo should reference the source-of-truth rather than maintain a second truth

3. Prefer **definitions before implementation**
   - source-of-truth impact
   - data model
   - types / interfaces
   - tests
   - then implementation layers

4. Use `[x]` and `[ ]` strictly
   - `[x]` only for confirmed facts, fixed decisions, or completed work
   - `[ ]` for pending work
   - never mark assumptions as `[x]`

5. The todo must be **loop-ready**
   - break work into mainline slices that can be implemented, verified, reviewed, and committed independently
   - every meaningful implementation loop should include an explicit unchecked `codex review` item
   - use the repository's existing review profile instead of redefining model, reasoning, or timeout in the todo

6. If the task is too small to justify a todo
   - say so explicitly
   - do not create `docs/todolist.md`

7. Do not generate a todo while key alignment questions are still unresolved
   - if scope, semantics, host/scope boundaries, or architecture direction are still under discussion, stop and ask for alignment first

## Required structure

Use this shape unless a task has a strong reason to be simpler:

```md
# <Feature Name> Todo

## 0. Context and Boundary

### 0.1 Confirmed facts
- [x] ...

### 0.2 Goals
- [ ] ...

### 0.3 Non-goals
- [x] ...

## 1. Definitions First

### 1.1 Source of Truth
- [ ] align with existing source-of-truth docs
- [ ] decide whether a new source-of-truth doc will be needed later

### 1.2 Data model
- [ ] ...

### 1.3 Types / Interfaces
- [ ] ...

## 2. Backend / Platform
- [ ] core
- [ ] contracts
- [ ] db
- [ ] app
- [ ] routes

## 3. Frontend Boundary
- [ ] schema
- [ ] repo
- [ ] service
- [ ] runtime
- [ ] ui

## 4. Tests
- [ ] schema tests
- [ ] repo tests
- [ ] service tests
- [ ] runtime tests
- [ ] ui tests

## 5. Recommended Execution Order

### Loop 1
- [ ] ...
- [ ] run `codex review` for this loop after targeted verification passes

### Loop 2
- [ ] ...
- [ ] run `codex review` for this loop after targeted verification passes
```

## Adaptation rules

- Drop sections that truly do not apply, but keep the ordering principle.
- If the task is backend-only or frontend-only, simplify the irrelevant half instead of filling it with noise.
- If the task is documentation-only, keep the todo much smaller and avoid fake engineering sections.
- If the prior analysis still has unresolved `Alignment Questions`, do not write the todo yet.

## What good looks like

A good todo should:

- make the next implementation loop obvious
- make verification obvious
- make loop-level review explicit
- show where tests belong
- prevent UI-first drift
- make it easy to know when the todo is done
- reflect aligned decisions rather than unresolved debate

## Review rule

When writing `## 5. Recommended Execution Order`:

- include a `codex review` checkbox in every meaningful implementation loop
- place the review item after the loop's targeted verification step
- keep the item unchecked unless that loop has actually been completed
- prefer wording like `- [ ] run \`codex review\` for this loop`
- do not restate model, reasoning, or timeout settings if the repository already defines a single-source-of-truth review profile

## Completion rule

When the work is finished:

1. stable long-lived facts should live in `docs/source-of-truth/*`
2. `docs/todolist.md` should be deleted
3. no parallel definitions should remain behind
