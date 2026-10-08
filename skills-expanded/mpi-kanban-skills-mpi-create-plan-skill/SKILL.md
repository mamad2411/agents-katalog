---
name: mpi-create-plan
description: MPI workflow pack - Create a compact/default MPI plan for normal work. Use when the user says "MPI create plan", "create an MPI plan", "create a plan", "make a plan", "$mpi-create-plan", or after brainstorming when the task can be implemented as one coherent flow with final verification.
---

# mpi-create-plan Skill

## Purpose

Create a compact plan in the JSON task workspace at
`.agents/mpi-kanban/tasks/<id>/plan.md` and reflect that plan on the task card.
This is the default planning path for normal work.

Invocation: Use the installed Agent Skills invocation for this agent, or ask naturally.

Use `mpi-create-large-plan` instead when the work needs investigation,
multiple phases, explicit parallel batches, or complex risk management. In
particular, if the work can be split into independent implementation tasks with
disjoint ownership, it belongs in a large plan: compact plans stay one coherent
flow and never carry `## Parallel Batch` sections.

## Plan shape

```markdown
# <Goal>

## Current State

Brief facts known at planning time.

## Implementation

- [ ] Implement the planned change end to end. **Verify:** <final verification>

## Completed

- [ ] Nothing yet.

## Remaining Work

- Implement the planned change end to end.

## Plan Drift

- None yet.

## Verification

**Verify mode:** auto | user-ux

`auto` = the agent fully self-verifies (tests, build, smoke, re-read) and does
not need the user to confirm a passing result. `user-ux` = the card has a UI/UX
surface the user must look at and feel in the running app before it is done.
Choose `user-ux` only when there is something a human must visually or
interactively judge; otherwise `auto`. `mpi-continue` reads this line to decide
whether to stop for the user after implementation.

Final verification instructions.

## Preservation Notes

Docs, rules, memory, or cleanup notes to consider before handoff/end-session.
```

Keep the plan compact. Do not split related work into many checklist items just
because several files may change.

## Workflow

1. Understand the goal or task from `mpi-brainstorm`.
2. **Load project knowledge if present.** Read
   `.agents/mpi-kanban/project-profile.md` and
   `.agents/mpi-kanban/project-knowledge-index.md` when they exist. Follow
   the context-budget rules in
   `${CLAUDE_PLUGIN_ROOT}/skills/mpi-lib/project-knowledge/indexing.md`: read pointer
   files first, then only the topic-matching docs/rules. Do not scan all
   rules and docs.
3. If the goal is clearly large or uncertain, or if independent parallel
   implementation looks likely (work splits into disjoint-ownership tasks),
   recommend `mpi-create-large-plan` instead and wait for confirmation.
4. **Front-load decisions (scalable-foundation).** When project mode is
   `scalable-foundation`, before writing the plan, exercise the mode's
   clarification and proactive-engineering behavior from
   `${CLAUDE_PLUGIN_ROOT}/skills/mpi-lib/project-intent/modes.md`: surface the architecture, pattern,
   and library decisions this work implies, push back where a stronger
   foundation is warranted, name future-proofing concerns the user has not
   raised, and resolve open questions with the user now. The goal is an
   implementable card that carries no unresolved decisions, so implementation
   does not stop mid-flight to ask.
5. Resolve or create the JSON board task. See "Task-board update" below.
6. Write the compact plan file to `.agents/mpi-kanban/tasks/<id>/plan.md`.
   Include project mode in `## Current State` when the profile exists
   ("Project mode: scalable-foundation"). Pull relevant conventions or
   commands from the matched topic block only. Set `**Verify mode:**` in
   `## Verification`: `user-ux` if the card has a UI/UX surface the user must
   judge in the running app, otherwise `auto`.
7. Update the task card's `maturity`, `status`, and `links.plan`.

## Task-board update

Lib pointers, read only when needed:

- `${CLAUDE_PLUGIN_ROOT}/skills/mpi-lib/task-board-ops/_schema.md` - JSON board and task-card shape.
- `${CLAUDE_PLUGIN_ROOT}/skills/mpi-lib/task-board-ops/read.md` - `findBoard`, `ensureBoard`,
  `loadTask`, `findTask`.
- `${CLAUDE_PLUGIN_ROOT}/skills/mpi-lib/task-board-ops/mutate.md` - `createTask`, `writeTask`,
  `ensureLinkedFiles`, `attachPlan`.

If `mpi-brainstorm` passed a task ID, call `loadTask(<id>)`. If it passed only
a title, call `findTask` by exact title and handle duplicates by asking the
user to choose the visible `MPI-*` ID. Otherwise ask:

```text
Does this work already have a task on the board? If yes, give the MPI ID or exact title. Reply "no" for a fresh To do task.
```

If an existing task matches:

1. If the task is in `done`, ask before reopening it into `todo`. On approval,
   call `moveTask(id, "todo", actor, "Reopened for a new plan.")`.
2. If the task is in `todo` or `doing`, leave it in its current column unless
   the user explicitly asks to move it.
3. Call `attachPlan(id, planMarkdown, actor)`.

If no task matches:

1. Call `createTask` with title, a short description, `column: "todo"`,
   `maturity: "planned"`, `status: "active"`, and the current actor.
2. Call `attachPlan(id, planMarkdown, actor)`.

Keep long-form plan content in `plan.md`. Do not embed the plan or a long
summary in `task.json`.

Confirm:

```text
Task: <id> "<title>" -> <To do | Doing>, planned. Plan: .agents/mpi-kanban/tasks/<id>/plan.md
Next: say "continue this plan" to start implementation. Implementation runs
through `mpi-continue`, which moves the card To do -> Doing before any edits.
```

## Hard rules

- Do not implement.
- Card-write preflight is mandatory before any `column`, `maturity`, or
  `status` write: read `${CLAUDE_PLUGIN_ROOT}/skills/mpi-lib/task-board-ops/_schema.md` and
  `${CLAUDE_PLUGIN_ROOT}/skills/mpi-lib/task-board-ops/mutate.md`. Do not derive legal values from
  existing cards.
- Do not let implementation begin from a `todo` card. Implementation must run
  through `mpi-continue`, which calls `beginImplementation` to move the card
  `To do -> Doing` and derive the checklist first. The lifecycle is always
  `To do -> Doing -> Done`; never `To do -> Done`.
- Do not create a large multi-step checklist in this skill.
- Do not add `## Parallel Batch` syntax to a compact plan.
- If the work obviously needs phased investigation, or splits into independent
  parallel implementation tasks, redirect to `mpi-create-large-plan`.
- Planning work uses `.agents/mpi-kanban/board.json` plus
  `.agents/mpi-kanban/tasks/<id>/plan.md`.
- Plan steps belong in the plan file under `## Implementation`. Implementation
  checklists belong in the task workspace and are derived later by
  `mpi-continue`; do not stuff checklist steps into `task.json`.
