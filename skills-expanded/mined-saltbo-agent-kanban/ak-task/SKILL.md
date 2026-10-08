---
name: ak-task
description: Create, assign, monitor, and review one Agent Kanban Task through Realmroot Toolbox. Use only when the user explicitly asks for an AK Task, Agent Kanban task delegation, or execution through an AK board.
---

# AK Task

## Before creation

Use generic Toolbox reads to resolve the Board, Repository, and existing Tasks:

```bash
realmroot toolbox get agent-kanban/boards --json
realmroot toolbox get agent-kanban/repositories --json
realmroot toolbox get 'agent-kanban/tasks?boardId=<board-id>' --json
```

Find available Agents:

```bash
realmroot toolbox get 'agent-kanban/agents?schedulable=true' --json
```

Use the selected Agent's `subject` as `assignedTo`. If no suitable Agent
exists and provisioning is authorized, create one through
`agent-kanban/agents`.

Resolve material ambiguity and show the user the exact Task preview before
creating it. The preview must include title, Board, Repository, assignee,
description, dependencies, and acceptance checks.

## Create and assign

Create an unassigned Task, then patch its `assignedTo` field.

```bash
realmroot toolbox post agent-kanban/tasks \
  --content-type application/json \
  @task.json --json

realmroot toolbox patch agent-kanban/tasks/<task-id> \
  --content-type application/merge-patch+json \
  '{"assignedTo":"<realmroot-agent-actor-id>"}' --json
```

Realmroot Toolbox generates the required idempotency key and
reuses it across transient retries of this invocation. Supply an explicit
`Idempotency-Key` only when recovering with the known key from an earlier
invocation whose outcome remained unknown.

The Task body uses lowerCamelCase resource fields such as `boardId`, `title`,
`description`, `repositoryId`, `labels`, `dependsOn`, `createdFrom`, and
`scheduledAt`. Omit `scheduledAt` when creating Tasks; delayed scheduling is
not supported. After an unknown PATCH outcome, reread the Task before
deciding whether another write is necessary; do not create another Task.

## Monitor

Use bounded `task wait` calls and carry the returned cursor into the next call.
Do not build an unbounded polling loop.

```bash
realmroot toolbox agent-kanban task wait <task-id> in-review --wait-seconds 25 --json
```

Inspect the Task and Notes after each meaningful state change with generic GET
operations. A cancelled Task is terminal.

## Review

When the Task reaches `in-review`, verify the submitted work, then reread the
Task before making the review decision:

```bash
realmroot toolbox get agent-kanban/tasks/<task-id> --include --json

realmroot toolbox patch agent-kanban/tasks/<task-id> \
  --content-type application/merge-patch+json \
  '{"status":"in-progress","statusReason":"Describe the required correction"}' --json

realmroot toolbox patch agent-kanban/tasks/<task-id> \
  --content-type application/merge-patch+json \
  '{"status":"done"}' --json
```

Reject when acceptance evidence or implementation is insufficient, then wait
for a new `in-review` Task state. Complete only after the requested outcome is
proven. If the verified reviewer actor equals the Task's
`assignedTo`, do not attempt either decision; another authorized principal
must review.

Cancel a non-terminal Task through the same Task patch:

```bash
realmroot toolbox patch agent-kanban/tasks/<task-id> \
  --content-type application/merge-patch+json \
  '{"status":"cancelled"}' --json
```
