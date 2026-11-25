---
name: task-spec-execution
description: Use when a docs-driven repository has a selected or selectable concrete docs/tasks task and needs task-local spec or implementation governance before code changes.
---

# Task Spec Execution

## Composition

- Entry: normally reached from `doc-driven-spec-workflow` or `milestone-planning` after a concrete task exists or is selected.
- Owns: task-local `spec.md`, optional task-local `plan.md`, readiness checks, implementation governance, verification, docs/status updates, and branch closing.
- Does not own: minimum docs scaffold bootstrap, milestone boundary decisions, module grouping, roadmap-layer task creation, or planning-stage templates.
- Handoff: return to `doc-driven-spec-workflow` after one concrete task checkpoint and branch closing are resolved.

## Mandatory Rules

These are requirements, not suggestions. If any rule below is not satisfied, the work is blocked until it is satisfied.

- MUST NOT edit implementation code for a concrete `docs/tasks/*` task until spec approval, plan approval when required, branch/worktree isolation, and the readiness checkpoint are complete.
- MUST keep pure docs governance in docs mode. Architecture edits, task/module reshaping, milestone updates, and index maintenance do not create implementation permission and do not require a new spec by default.
- MUST defer repository docs scaffold initialization to `docs-workflow-bootstrap` when the main question is creating the minimum docs layout.
- MUST defer roadmap decomposition to `milestone-planning` when the main question is how many milestones should exist, whether modules are needed, or how work should be split into tasks before selecting the current concrete task.
- MUST treat routine cleanup and concept clarification as inline maintenance, not standalone tasks. Create a pure cleanup/governance/clarification task only when it is complex, cross-cutting, independently reviewable, or needs project-level execution tracking.
- MUST use `docs/tasks/` as the only source of truth for concrete next work; if no suitable open task exists, stop and use `milestone-planning` before writing a spec.
- MUST treat a task inside an unconfirmed milestone as not yet suitable open work for spec execution, even if the task directory or breakdown already exists.
- MUST respect task sizing from the roadmap. If the selected task is too small, too broad, or only an implementation sub-step, stop and use `milestone-planning` to reshape it before writing a spec.
- MUST respect the module layer chosen by the roadmap. Do not create, remove, or regroup modules here.
- MUST treat completed milestones as frozen history. NEVER reopen them or add modules/tasks to them; use `milestone-planning` for follow-up work.
- MUST resolve the previous task checkpoint before starting another concrete task. Default action is commit; uncommitted checkpoints require explicit user approval.
- MUST NOT start a concrete task in a later milestone while the previous milestone is still operationally unresolved. If the earlier milestone's last task is done but milestone closure or milestone transition is still pending, stop and use docs governance first.
- MUST require explicit milestone-entry confirmation before starting a task in a milestone whose status still shows `Roadmap confirmed: no` or equivalent provisional wording.
- MUST treat tasks in a milestone whose status still shows `Roadmap confirmed: no` as candidate tasks only. They are not formal execution tasks until milestone entry is explicitly confirmed.
- MUST NOT treat checkpoint rules as permission to auto-commit newly made docs-only/governance changes. Report the diff/result first; commit only when the user explicitly asked for commit upfront or confirms after review.
- MUST report milestone-entry governance changes before drafting the first task spec in that milestone.
- MUST resolve branch closing after completing a concrete task: verification, docs/status updates, commit or approved uncommitted checkpoint, and branch closing decision.

Spec creation requirements:

- MUST NOT create a new spec for pure docs governance work: architecture docs, task/module reshaping, milestone changes, or index maintenance.
- MUST default to `1 task -> 1 spec` for concrete implementation tracking.
- MUST place concrete task specs and plans inside the task directory by default: `docs/tasks/<milestone>/<module>/<task>/task.md`, `spec.md`, and optional `plan.md`.
- MUST use global `docs/specs/` or `docs/plans/` only for standalone or cross-task documents that do not belong to one concrete task.
- MUST revise the existing spec for that task instead of creating a second spec for corrections or clarifications.
- MUST stop and use `milestone-planning` to split the task first if multiple specs seem necessary. NEVER silently create multiple specs for one task.

Violations that require stopping immediately:

- Coding before branch/worktree isolation.
- Skipping the checkpoint because a change seems small.
- Inferring a task directly from architecture instead of using `milestone-planning` to add or select it in `docs/tasks/`.
- Creating standalone tasks for routine cleanup, concept clarification, link fixes, renames, formatting, index maintenance, or small docs reorganization that should be handled in the current work round.
- Splitting implementation or delivery verification into separate tasks, such as "code review", "write unit tests", "add repository file", "update handler", or "write migration" when they belong to one coherent implementation round.
- Creating tiny modules as buckets for one-off tasks, or one catch-all module when tasks should live directly under the milestone.
- Adding cross-milestone task-level `Depends on` links when the milestone order already expresses the dependency.
- Creating a task-local spec or plan in global `docs/specs/` or `docs/plans/` by default.
- Creating multiple specs for one task instead of revising the existing spec or splitting the task first.
- Adding work to a completed milestone.
- Auto-committing docs-only/governance changes before reporting the result or before user commit confirmation.
- Starting another task before resolving branch closing for the current task.
- Starting a task in milestone `M(n+1)` while `M(n)` still appears open and unclosed, or while the target milestone is still explicitly unconfirmed.
- Assuming the workspace is clean or staying on the current branch without explicit user choice.

## When To Use

Use this skill when the repository uses `docs/architecture`, `docs/tasks`, `docs/context`, and task-local or standalone specs/plans, and the current concrete task has been chosen or is ready to be chosen from the existing roadmap. Use `milestone-planning` first when the user is still deciding milestone/module/task structure. Do not use it for repositories without this layout.

## Docs Roles

- `docs/architecture/`: stable behavior and long-lived constraints
- `docs/tasks/`: milestone roadmap, optional module grouping, task order/dependencies/status, and task directories for complete implementation rounds; tasks under unconfirmed milestones remain provisional candidates until entry is confirmed
- `docs/context/`: supporting research only
- task-local `spec.md`: one current-task design per concrete task by default
- task-local `plan.md`: optional implementation plan for genuinely complex concrete tasks
- `docs/specs/`: standalone or cross-task design docs only
- `docs/plans/`: standalone or cross-task execution plans only

Task ownership: `docs/tasks/index.md` lists only open/completed milestones; milestone indexes list modules/progress when modules exist; module or milestone indexes list open/completed task directories, order, and dependencies; task-local `task.md` tracks source, status, dependencies, and acceptance points.

This skill assumes the minimum docs scaffold and roadmap-layer docs shape already exist or are being updated separately. Its references define the compact docs shape used by current-task execution and task-local specs/plans. Bootstrap belongs to `docs-workflow-bootstrap`; roadmap decomposition, milestone/module indexes, and planning-stage task metadata belong to `milestone-planning`.

## Templates And Workflow

Load only the relevant reference:

- `docs/architecture/`: `references/architecture-template.md`
- `docs/context/`: `references/context-template.md`
- non-roadmap docs indexes: `references/index-template.md`
- selected task directory or `task.md`: `references/task-execution-template.md`
- task-local `spec.md`: `references/spec-template.md`
- task-local `plan.md`: `references/plan-template.md`

Do not load every template by default.
Do not use these references as the default planning-stage output for milestone decomposition.

## Bootstrap Handoff

When the user asks to initialize, bootstrap, create, or scaffold the minimum docs workflow for a repository, use `docs-workflow-bootstrap` instead of this skill.

This skill may read or maintain bootstrap-created docs after they exist, but it is not the primary owner of repository scaffold initialization.

Follow this order unless the user explicitly asks for something different:

1. If the user's feature, behavior, or task intent is ambiguous, use `brainstorming` when available, or an equivalent clarification workflow, before selecting or creating a concrete task.
2. If the main uncertainty is roadmap shape rather than current-task design, use `milestone-planning` before continuing here.
3. Read `docs/index.md` and the relevant docs index files.
4. Read the relevant `docs/architecture/` documents for behavior boundaries.
5. Read the relevant `docs/tasks/` milestone/module index plus task directory or `task.md` for order, status, and dependencies.
6. Use `docs/context/` only for supporting research or unstable reference material.
7. If there is no suitable open task because the roadmap shape itself is missing or unclear, stop and use `milestone-planning`.
8. If the next candidate task is in a new milestone, first verify that the previous milestone checkpoint is closed and the target milestone is explicitly confirmed for entry. If not, stop and resolve milestone governance first.
9. If implementing one concrete task, create or update its task directory and write one focused `spec.md` inside it.
10. Stop after writing the spec; do not code until the user explicitly confirms it in the current thread.
11. Create `plan.md` inside the task directory only for genuinely complex or multi-step work; if created, stop again for user confirmation before coding.
12. After spec approval, and after plan approval when a plan exists, resolve a docs checkpoint for the approved task-local docs before implementation isolation.
13. Before implementation edits, announce and run the readiness checkpoint.
14. Implement from the approved spec or plan, then verify, update docs/status, and resolve branch closing.
15. Stop after one concrete task. Continue only when the user explicitly asks in the current thread.
16. Add an `index.md` for every new major documentation section.

## Execution Rules

- Default flow: `spec -> user confirms -> docs checkpoint -> code`
- Complex flow: `spec -> user confirms -> plan -> user confirms -> docs checkpoint -> code`
- Ambiguous flow: `brainstorming or equivalent clarification -> milestone-planning if needed -> spec -> user confirms -> docs checkpoint -> code`
- Do not default to TDD, plan-driven execution, or heavyweight shared workflows unless the user explicitly asks.
- Write task-local specs/plans directly in this repository's compact local format.
- Treat tests and verification as delivery checks, not as a mandatory test-first workflow.
- A concrete task is a hard pause point: report verification/docs updates, resolve commit or approved uncommitted checkpoint, resolve branch closing, then stop.
- Milestone completion is a hard boundary: once moved to `Completed Milestones`, it is frozen; follow-up work belongs in a new open milestone.
- Crossing from one milestone to another is also a hard pause point: first resolve milestone closure for the old milestone and explicit roadmap confirmation for the new one, then select the next concrete task.
- For docs-only/governance work, stop after reporting changed files and key diffs. Do not commit unless the user already asked for commit/sync in the same request or confirms after seeing the result.

## Branch Closing Rules

- After completing a concrete `docs/tasks/*` task, do not start another task until branch closing is resolved.
- When implementation is complete, verification passes, and Git integration or cleanup remains, use `finishing-a-development-branch` when available to present merge, PR, keep, or discard options.
- If work happened in a worktree, use `using-git-worktrees` cleanup rules when available; otherwise follow an equivalent safe worktree cleanup process.
- Removing a worktree does not remove its task branch. Branch closing is unresolved until the merged task branch is deleted with confirmation or explicitly kept for review/history.
- If the user chooses merge and cleanup, confirm whether cleanup includes deleting the fully merged task branch before deleting it.
- Never delete a branch or worktree without confirming the closing decision.
- If the user asks to continue, treat that as a prompt to resolve branch closing first, not permission to skip it.
- If the user asks to continue after the last open task in a milestone is complete, treat that as a prompt to resolve milestone closure and next-milestone confirmation first, not permission to jump directly into a later milestone task.

## Spec, Plan, And Readiness

- Spec defines behavior, scope, exclusions, and tradeoffs.
- Plan defines implementation slices, file map, and verification only when complexity justifies it.
- Do not collapse them into one document.
- Use local compact templates; if shared plan-writing guidance conflicts, prefer the local template.
- For concrete tasks, default paths are task-local `spec.md` and optional `plan.md`; use global `docs/specs/` or `docs/plans/` only for standalone or cross-task docs.

Run this checkpoint after spec confirmation, and after plan confirmation when a plan exists:

- Resolve previous task checkpoint first: commit by default, or keep uncommitted only with explicit user approval.
- Resolve a docs checkpoint for the approved task-local `spec.md`, and `plan.md` when it exists, before implementation isolation. Default action is to commit these approved docs on the current shared branch; keep them uncommitted before implementation only with explicit user approval.
- Confirm permission to code: current-thread spec approval, and plan approval when a plan exists.
- If this is a concrete `docs/tasks/*` implementation round, branch isolation is mandatory before code edits.

| Situation | Required action |
| --- | --- |
| Workspace is dirty, shared, already risky, or likely to conflict | Use `using-git-worktrees` when available, or an equivalent safe worktree workflow |
| Workspace is clean and isolation risk is low | Create a dedicated task branch in place |
| User explicitly asks to stay on the current branch | You may stay, but only because the user explicitly chose that |

- Never start implementation for a concrete task on the current branch by default.
- Do not carry approved-but-uncommitted task-local `spec.md` or `plan.md` into an implementation worktree or task branch by default.
- If a worktree is needed, prefer `using-git-worktrees`; if it is unavailable, use the environment's equivalent git worktree workflow and preserve the same safety checks.
- Before the first implementation edit, tell the user: `Spec/plan is approved and checkpointed. I am handling branch isolation now before coding.`

## Task And Status Rules

- Use `docs/tasks/` to decide the next task, not `docs/context/`.
- Do not infer a new concrete implementation task from `docs/architecture/` alone.
- If architecture implies follow-up work but `docs/tasks/` has no corresponding open task, use `milestone-planning` or an equivalent roadmap update flow before creating a spec.
- Modules are optional durable capability areas owned by roadmap planning. Respect the selected task's existing milestone/module placement; if placement seems wrong, stop and use `milestone-planning`.
- Tasks should fit one focused branch while including implementation, tests, docs/status updates, code review, and verification. If the selected task does not fit that shape, stop and use `milestone-planning` before writing a spec.
- Keep implementation steps inside `spec.md`, optional `plan.md`, or checklist items; do not promote them into tasks.
- Task-level `Depends on` should normally stay within the same milestone. Put cross-milestone sequencing in milestone-level `Notes`, `Exit Criteria`, or roadmap text; if future task details depend on an earlier milestone, keep them as roadmap text or milestone-level `planned`.
- Respect task dependencies exactly as written.
- Keep task status mutually exclusive: `planned`, `in_progress`, `blocked`, `completed`.
- `docs/tasks/index.md` lists only `Open Milestones` and `Completed Milestones`, with no modules or task counts.
- Move milestones from open to completed only when the whole milestone is done; do not use milestone `[completed/total]`.
- Do not begin a task from a later milestone until the previous milestone is either still intentionally active by explicit user choice or has been reviewed for closure and the target milestone is explicitly confirmed.
- Milestone indexes list modules/progress when modules exist; module or milestone indexes keep `Open Tasks` and `Completed Tasks` accurate.
- Each concrete task should be a directory containing `task.md`, task-local `spec.md`, and optional `plan.md`.
- `task.md` tracks status, dependencies, and acceptance points; it should not become a detailed step-by-step implementation plan.
- When all current open tasks are complete, report whether the current milestone appears complete. Use `milestone-planning` before moving milestone state or adding missing module/task work.
- Pure cleanup, concept clarification, or docs governance belongs in the current work round by default. Create a task directory only for complex/cross-cutting governance or clarification with independent acceptance or project-level execution state; even then, do not create a spec unless it drives concrete implementation.

If you need the selected task directory or `task.md` execution shape, read `references/task-execution-template.md`. If you need milestone/module index shape or roadmap-layer task creation, use `milestone-planning` and its `references/roadmap-template.md`.

## Source Of Truth Rules

- Treat code as the source of truth when code and docs diverge.
- When writing docs, follow the user's current language instruction first; otherwise follow repository-level instruction files such as `AGENTS.md`, `CLAUDE.md`, or `.claude/CLAUDE.md`.
- If implementation changes behavior, API shape, task status, architecture assumptions, or other documented constraints, update the relevant docs in the same round.
- If a conclusion in `docs/context/` becomes a stable system rule, move or restate it in `docs/architecture/`.
