---
name: doc-driven-spec-workflow
description: Routes docs-driven repository work to the correct workflow stage and preserves handoff context. Use when the next step is unclear between bootstrap, clarification, roadmap planning, task preparation, or execution.
---

# Doc-Driven Spec Workflow

## Purpose

Choose exactly one next stage skill. Do not do stage work here.

## Use when

- the repository follows this docs-driven workflow
- the user wants to continue work but the current stage is not explicit
- a fresh conversation must recover workflow state from docs and the prompt

## Read first

1. `docs/tasks/index.md`
2. `docs/tasks/planning-inbox.md`
3. `docs/tasks/backlog.md`
4. relevant milestone, module, and task docs under `docs/tasks/`
5. `docs/architecture/`
6. `docs/context/`
7. the current user prompt

Missing docs are routing signals, not proof that goals are unclear.

## Owns

- identify the current workflow stage
- choose the next stage skill
- ask the smallest routing question when evidence is insufficient
- hand off `Decided`, `Undecided`, `Next skill`, and `Stop point`

## Must not own

- scaffold creation details
- roadmap decomposition details
- task-local `spec.md` or `plan.md` authoring
- execution isolation, implementation, verification, or branch closing
- local decisions that belong to the selected stage skill

## Routing table

| Situation | Next skill |
| --- | --- |
| Minimum docs scaffold is missing | `docs-workflow-bootstrap` |
| Docs or prompt show unresolved goals, constraints, success criteria, or now-vs-later boundaries | `planning-clarification` |
| Milestone shape, module grouping, task breakdown, or delivery order is unclear | `milestone-planning` |
| A concrete task is selected or clearly selectable from confirmed roadmap state | `task-preparation` |

## Entry checks

- Route to `docs-workflow-bootstrap` when any minimum scaffold file is missing:
  - `docs/index.md`
  - `docs/architecture/index.md`
  - `docs/tasks/index.md`
  - `docs/tasks/planning-inbox.md`
  - `docs/tasks/backlog.md`
  - `docs/context/index.md`
- Route to `planning-clarification` only for positive ambiguity evidence. Missing or stale docs alone are not enough.
- Route to `task-preparation` only when all are true:
  - the milestone has `Roadmap confirmed: yes`
  - previous milestone closure is resolved when crossing milestones
  - task status is `planned` or `in_progress`
  - dependencies are satisfied or explicitly waived
  - no unresolved hard gate blocks progress
  - the user selected the task, or docs clearly identify it as next

## Default flow

1. Read docs in evidence order and identify the strongest routing signal.
2. Choose exactly one next stage skill.
3. If evidence is insufficient, ask one minimal routing question instead of guessing.
4. Hand off only stage context, not stage-specific decisions.

## Stop point

- handoff to one stage skill
- or one minimal routing question

## If blocked

- ask one routing question when evidence does not identify the next stage
- do not answer the routing question on the user's behalf
- do not bypass uncertainty by drafting specs or inventing roadmap structure

## Handoff

- `Current stage`
- `Why`
- `Decided`
- `Undecided`
- `Next skill`
- `Stop point`
