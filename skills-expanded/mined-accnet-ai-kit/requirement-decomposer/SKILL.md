---
name: requirement-decomposer
description: Break an approved requirements brief into atomic, dependency-ordered tasks with verifiable acceptance criteria, registered through ai-kit add-task/plan. Bridges requirements-intake's WHAT into G1's actual task record.
version: 0.1.0
tier: core
stack: [any]
owner: planner
gates: [G1]
related: [.ai/engine/state-schema.md, requirements-intake, system-designer]
---

# Skill: requirement-decomposer

## Purpose
Turn `.ai-work/requirements/brief.md`'s acceptance criteria into a task graph
the Scheduler can actually run. `requirements-intake` establishes WHAT is
wanted; this skill's job stops at turning that WHAT into atomic,
dependency-ordered `ai-kit` tasks — it does not re-derive or expand scope.

## When to use
After a requirements brief exists (or immediately in `ai-kit plan --idea` for
a small change that skips a standalone brief), before any task is dispatched.

## Procedure
1. **Start from the brief's acceptance criteria and out-of-scope list.** Do
   not add scope the brief doesn't state; an ambiguity goes back to the
   brief/user, not into an assumption baked into a task.
2. **One task = one verifiable acceptance criterion**, or a tightly coupled
   minimal set. Reject any task whose "done" can only be settled by further
   discussion rather than a check.
3. **Order by real dependency, not convenience** — and use the right field
   for what you mean:
   - `--needs <task-id>`: workflow ordering. The task cannot leave `todo`
     until every needed task is `done`.
   - `--depends-on <path>`: a contract/interface file this task's
     correctness relies on (a schema, an API contract, a migration). The
     engine hashes it at creation time; `ai-kit drift` flags the task when
     that file changes later. This is drift tracking, not ordering — do not
     use it as a substitute for `--needs`.
4. **Tag `--context`** only with a context already registered in
   `.ai-config/contexts.yaml` (see `system-designer`). Do not invent a
   context tag inline; an unregistered context tag is inert, not enforced.
5. **Tag `--epic`** when tasks share a Specification doc, and register the
   epic (`ai-kit epic add <name> --spec <path>`) so `epic_revision` drift
   tracking applies.
6. For a qualified basic edit (all Planner fast-path conditions hold), create
   one direct `add-task` record and do not create a plan draft. For all other
   collaborative planning, wait for both explicit user decisions before
   making runtime tasks: finalize the approved draft with
   `plan-draft finalize --confirmed-by-user`, then only materialize after a
   separate “create tasks” answer using `plan-draft materialize
   --create-tasks`. Use `ai-kit plan --idea ... --owner ... --acceptance ...`
   for the legacy direct path; use `ai-kit add-task` for every task after the
   first.
7. Before handing off, confirm the graph actually resolves: `ai-kit ready`
   returns at least one task, and nothing errors as a dependency cycle.
8. **Re-plan, don't silently extend**, when the brief's acceptance criteria
   change after tasks exist — use `ai-kit update-task --add-acceptance` (or
   `--add-files`/`--add-tags`) to amend the existing task record.

## Checklist
- [ ] Every task traces to a specific acceptance criterion in the brief
- [ ] No task's "done" bar is only a further conversation, not a check
- [ ] `--needs` used for ordering, `--depends-on` used for drift-tracked
      contract files — not the other way around, not both for the same fact
- [ ] `--context` set only to an already-registered context, or omitted
- [ ] `--epic` set and registered when tasks share a Specification doc
- [ ] `ai-kit ready` returns at least one runnable task before handoff

## Anti-patterns
- One giant task standing in for the whole feature ("implement checkout")
- Using `--depends-on` to express ordering the engine already gets from
  `--needs` — duplicates the dependency in two mechanisms with different
  failure modes
- Inventing a `--context`/`--epic` tag ad hoc instead of registering it,
  which silently drops G6 module-boundary checks and drift tracking
- Re-decomposing a task that is already dispatched instead of
  `update-task`, or `reject` + redo through the proper transition

## Output
`.ai-work/tasks/tasks.md` entries created via `add-task`/`plan`, each
resolvable by `ai-kit ready` / `ai-kit graph` / `ai-kit board`.
