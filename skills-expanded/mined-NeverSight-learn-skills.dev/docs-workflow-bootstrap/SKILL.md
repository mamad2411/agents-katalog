---
name: docs-workflow-bootstrap
description: Use when initializing, bootstrapping, creating, or scaffolding the minimum docs-driven workflow layout for a repository before roadmap planning, specs, or implementation tasks exist.
---

# Docs Workflow Bootstrap

Initialize the minimum docs-driven workflow scaffold for a repository.

This skill is only for repository documentation bootstrap. It does not plan milestones, create implementation tasks, write specs, or authorize code changes.

## Composition

- Entry: normally reached from `doc-driven-spec-workflow` when the repository lacks the minimum docs scaffold.
- Owns: minimum docs entry points and compact bootstrap content.
- Does not own: roadmap decomposition, task creation, task-local specs, plans, implementation, or branch closing.
- Handoff: return to `doc-driven-spec-workflow` after reporting created or changed files, unless the user explicitly asks to continue to planning.

## Mandatory Rules

- MUST keep bootstrap work in docs governance mode.
- MUST create only the minimum docs entry points unless the user explicitly asks for more.
- MUST NOT create implementation tasks unless the user provides an actual milestone/task.
- MUST NOT create `docs/specs/` or `docs/plans/` by default.
- MUST NOT write task-local `spec.md` or `plan.md`.
- MUST report created or changed files and stop.

## Bootstrap Layout

Create these files when missing:

- `docs/index.md`
- `docs/architecture/index.md`
- `docs/tasks/index.md`
- `docs/context/index.md`

Use the repository's documentation language instructions when available. Otherwise follow the user's current language request.

## Default Content Shape

Keep generated files compact:

- `docs/index.md`: explain the docs entry point and link to architecture, tasks, and context
- `docs/architecture/index.md`: explain stable design and behavior boundaries
- `docs/tasks/index.md`: explain roadmap/task tracking and include `Open Milestones` and `Completed Milestones`
- `docs/context/index.md`: explain research notes and supporting context

Do not create roadmap details during bootstrap unless the user supplies actual roadmap content.

## Handoff

After bootstrap:

- Return to `doc-driven-spec-workflow` so it can choose the next stage.
- Continue directly to `milestone-planning` only when the user explicitly asks to plan milestones, modules, and tasks.
- Continue directly to `task-spec-execution` only when the user explicitly asks and a concrete task already exists or is selected.

Stop after reporting the bootstrap result unless the user explicitly asks to continue.
