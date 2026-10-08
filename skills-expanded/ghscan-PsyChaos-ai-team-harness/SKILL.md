---
name: planning-projects
description: Decomposes a product or engineering goal into executable GitHub phases, features, tasks, subtasks, acceptance criteria, risks, and native issue dependencies. Use when a project or issue is in PLANNING.
---

# Planning Projects

Transform a goal/specification into an executable work graph.

For a new project from natural language, use `.ai-team/bin/bootstrap-project
--brief FILE` (or `--brief -` for stdin). It creates/reuses the Project and publishes
the validated graph. Its dedicated prompt defines bounded JSON output. Planning
has no GitHub write authority; the deterministic publisher creates issues/edges.
Root/phase/feature/grouping issues stay BACKLOG and are never implementation work.
Only task/subtask leaves with acceptance and validation can become READY. All
leaves stay BLOCKED until the complete graph has been verified; the root's final
completion marker is mandatory before any descendant can run.
Do not regenerate a bootstrap plan on retry: recover it from the tracking issue.

Principles:
- plan outcomes, not fake busywork
- prefer one coherent reviewable outcome per task
- use subtasks only when they improve ownership/dependency/review clarity
- every executable task needs acceptance criteria
- dependencies must be native GitHub relationships where practical
- separate product decisions from implementation
- identify critical path and risks

Each phase needs objective, entry criteria, exit criteria, risks, features/tasks.

Each task needs Goal, Context, In/Out of Scope, Acceptance Criteria, Dependencies, Constraints, Validation, Evidence Required and Risk.

Good tasks are usually one PR, independently reviewable, bounded, and completable by one agent session. Avoid both giant multi-outcome tasks and meaningless microtasks.

Mark only genuinely executable dependency-free tasks READY; blocked work remains BLOCKED.
