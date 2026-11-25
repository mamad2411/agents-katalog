---
name: mpi-create-large-plan
description: MPI workflow pack - Create an adaptive, investigation-backed MPI plan for large or uncertain work. Use when the user says "MPI create large plan", "create a large MPI plan", "large plan", "complex plan", "adaptive plan", "multi-phase implementation", "$mpi-create-large-plan", or asks for non-trivial investigation or a parallel-safe plan.
---

# mpi-create-large-plan Skill

## Locating shared references

Shared reference docs live in the sibling skill `mpi-lib`. At first use, find the first existing directory from this candidate list:

1. `~/.agents/skills/mpi-lib`
2. `.agents/skills/mpi-lib`
3. `~/.claude/skills/mpi-lib`
4. `.claude/skills/mpi-lib`

Cache that root path for the rest of this session. All references below resolve as `<mpi-lib-root>/<sub/path>.md`. If no candidate exists, stop and tell the user to reinstall the complete pack with:

`npx skills add MadPonyInteractive/mpi-kanban --all -y -g`

## Purpose

Create a large adaptive plan in the JSON task workspace at
`.agents/mpi-kanban/tasks/<id>/plan.md` and reflect that plan on the task card.
Use this for work with unclear root cause, multiple subsystems, meaningful
risk, or enough moving pieces that a compact plan would hide important
decisions.

Invocation: Use the installed Agent Skills invocation for this agent, or ask naturally.

Large plans are living documents. They guide work, but `mpi-continue` may
revise the remaining work as implementation reveals new facts.

## Core principles

1. Default to parallel read-only sub-agents for independent investigation
   areas, not just "where useful." Use a single agent only when investigation
   areas are not independent or the work is trivial.
2. Implementation is adaptive through `mpi-continue`.
3. Default to explicit `## Parallel Batch` sections whenever implementation
   tasks have disjoint, declarable ownership and batch-safe verification.
   Parallel implementation runs only through these sections (executed by
   `mpi-execute-parallel`), but writing them is the default for splittable work,
   not an opt-in extra. When work is large but cannot be split safely, keep
   normal phases and state in the plan why no batch was created.
4. Every executable task or batch must include a concrete `**Verify:**` line.
5. No forward dependencies inside a task or parallel batch. If verification
   depends on later work, merge the work or move it later.

## Plan shape

Use this structure unless the project has a stronger local convention:

```markdown
# <Goal>

## Current State

What is known now, including relevant files, constraints, and open risks.

## Completed

- [ ] Nothing yet.

## Remaining Work

## Phase 1: <name>

- [ ] <task>. **Verify:** <testable check at this stage>

## Parallel Batch: <name>

- [ ] <task>. Ownership: <files/modules>. Briefings: <rule names or bundle>. **Verify:** <batch-safe check>
- [ ] <task>. Ownership: <files/modules>. Briefings: <rule names or bundle>. **Verify:** <batch-safe check>

## Plan Drift

- None yet.

## Verification

Final end-to-end verification criteria.

## Preservation Notes

Docs, rules, memory, or cleanup items likely to matter before handoff/end-session.
```

Default to `## Parallel Batch` whenever tasks are genuinely independent and have
disjoint ownership. Use normal phases only when work cannot be split safely,
and note why in the plan.

## Workflow

1. Understand the user's goal or the task passed by `mpi-brainstorm`.
2. **Load project knowledge if present.** Read
   `.agents/mpi-kanban/project-profile.md` and
   `.agents/mpi-kanban/project-knowledge-index.md` when they exist. Follow
   the context-budget rules in
   `<mpi-lib-root>/project-knowledge/indexing.md`. Brief each
   investigation sub-agent with the profile mode and the relevant topic
   block(s), not the whole project.
3. Identify 2-4 investigation areas. Default to spawning one read-only sub-agent
   per independent area, in parallel. Sub-agents write findings to
   `/tmp/investigation/<area>.md` and never edit project files. Use a single
   agent only when the areas are not independent or the work is trivial.
4. Synthesize findings into an adaptive plan with `Current State`,
   `Remaining Work`, `Plan Drift`, `Verification`, and `Preservation Notes`.
   Include project mode in `## Current State` when the profile exists.
5. Self-audit:
   - Each task has `**Verify:**`.
   - Independent implementation work is in `## Parallel Batch` sections by
     default; if splittable work was left as sequential phases, the plan says
     why.
   - Parallel batch tasks declare `Ownership:` and do not overlap.
   - No task assumes later work has already happened.
   - The plan says when `mpi-execute-parallel` is appropriate, if at all.
6. Resolve or create the JSON board task. See "Task-board update" below.
7. Write the plan file to `.agents/mpi-kanban/tasks/<id>/plan.md`.
8. Update the task card's `maturity`, `status`, and `links.plan`.

## Task-board update

Lib pointers, read only when needed:

- `<mpi-lib-root>/task-board-ops/_schema.md` - JSON board and task-card shape.
- `<mpi-lib-root>/task-board-ops/read.md` - `findBoard`, `ensureBoard`,
  `loadTask`, `findTask`.
- `<mpi-lib-root>/task-board-ops/mutate.md` - `createTask`, `writeTask`,
  `ensureLinkedFiles`, `attachPlan`.
- `<mpi-lib-root>/interop-ops/modes.md` - source-of-truth mode gate.

Before mutating `board.json`, read `.agents/mpi-kanban/state/interop.json`
when it exists. If `source_of_truth` is `nimbalyst`, do not move or create MPI
board tasks. Report:

```text
Interop mode is nimbalyst, so Nimbalyst trackers/sessions are canonical. I drafted the plan content, but I will not update .agents/mpi-kanban/board.json or task files. Update the Nimbalyst tracker/session, or run mpi-nimbalyst-sync for an explicit snapshot boundary.
```

If the file is missing or `source_of_truth` is `file`, continue with the
normal JSON task-board update below.

If `mpi-brainstorm` passed a task ID, call `loadTask(<id>)`. If it passed only
a title, call `findTask` by exact title and handle duplicates by asking the
user to choose the visible `MPI-*` ID. Otherwise ask:

```text
Does this work already have a task on the board? If yes, give the MPI ID or exact title. Reply "no" for a fresh To do task.
```

If an existing task matches:

1. If the task is in `done`, ask before reopening it into `todo`. On approval,
   call `moveTask(id, "todo", actor, "Reopened for a new large plan.")`.
2. If the task is in `todo` or `doing`, leave it in its current column unless
   the user explicitly asks to move it.
3. Call `ensureLinkedFiles(id, { "research": "research/" })` if preserving
   investigation notes.
4. Call `attachPlan(id, planMarkdown, actor)`.
5. Store investigation notes under `.agents/mpi-kanban/tasks/<id>/research/`
   when they are worth preserving.
6. If research was preserved, call `writeTask` to keep `links.research` set to
   `research/`.

If no task matches:

1. Call `createTask` with title, a short description, `column: "todo"`,
   `maturity: "planned"`, `status: "active"`, and the current actor.
2. Call `attachPlan(id, planMarkdown, actor)`.
3. Call `ensureLinkedFiles(id, { "research": "research/" })` only if preserving
   investigation notes.

Keep long-form plans, research, and batch details in task workspace files. Do
not embed them in `task.json`.

Confirm:

```text
Task: <id> "<title>" -> <To do | Doing>, planned. Plan: .agents/mpi-kanban/tasks/<id>/plan.md
Next: say "continue this plan" to start, or "create a handoff" if you want a fresh session first.
```

## Hard rules

- Do not execute implementation work.
- Do not add implementation checklist steps yet; `mpi-continue` derives
  lifecycle/phase checklists when implementation starts.
- Do not create parallel batches without explicit ownership for every task.
- New planning work uses `.agents/mpi-kanban/board.json` plus
  `.agents/mpi-kanban/tasks/<id>/plan.md`. Legacy `kanban.md` may be read only
  for explicit migration or compatibility and must not be updated as the live
  board once `board.json` exists.
- Keep plan and research content in task workspace files, not in `task.json`.

## Related invocations

- Related skills: `mpi-create-plan`, `mpi-continue`, `mpi-execute-parallel`.
