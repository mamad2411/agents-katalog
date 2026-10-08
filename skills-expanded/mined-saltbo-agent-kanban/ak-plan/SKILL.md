---
name: ak-plan
description: Plan and execute a multi-Task project through Agent Kanban resources and Realmroot Toolbox. Use only when the user explicitly asks for AK Plan, an Agent Kanban project plan, or execution of a project through an AK board.
---

# AK Plan

## Plan before creating

Read the repository and existing AK resources before decomposition:

```bash
realmroot toolbox get agent-kanban/boards --json
realmroot toolbox get agent-kanban/repositories --json
realmroot toolbox get 'agent-kanban/tasks?boardId=<board-id>' --json
```

Define the architecture direction, shared contracts, ownership boundaries, and
dependency graph. Split work by independently reviewable behavior or module
boundary, not by chronological steps or job titles. Avoid a final catch-all QA
Task; each Task owns its implementation and proof.

Show the user the complete Board/Task preview and get confirmation before any
creation. Include every Task's goal, assignee, repository, dependencies, and
acceptance checks.

## Create resources

Create a Board or Repository only when it does not already exist:

```bash
realmroot toolbox post agent-kanban/boards --content-type application/json @board.json --json
realmroot toolbox post agent-kanban/repositories --content-type application/json @repository.json --json
```

Select an available Agent that reports `schedulable: true`:

```bash
realmroot toolbox get 'agent-kanban/agents?schedulable=true' --json
```

Use the selected Agent's `subject` as `assignedTo`. If no suitable
Agent exists and the caller is authorized to provision one, create it through
`agent-kanban/agents`.

For each approved work item, create an unassigned Task, then patch its
`assignedTo` field:

```bash
realmroot toolbox post agent-kanban/tasks --content-type application/json @task.json --json
realmroot toolbox patch agent-kanban/tasks/<task-id> \
  --content-type application/merge-patch+json \
  '{"assignedTo":"<realmroot-agent-actor-id>"}' --json
```

Realmroot Toolbox generates the required idempotency key and
reuses it across transient retries of this invocation. Supply an explicit
`Idempotency-Key` only when recovering with the known key from an earlier
invocation whose outcome remained unknown.

Encode real prerequisites in `dependsOn`. Tasks with overlapping files or
contracts should be combined or ordered; only independent Tasks should run in
parallel.

## Execute and review

After creation, continue until every Task is terminal unless the user asks to
stop. Use bounded waits with continuation cursors:

```bash
realmroot toolbox agent-kanban task wait <task-id> in-review --wait-seconds 25 --json
```

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

When one prerequisite completes, reassess its dependent Tasks.
Report the final Task states, review outcomes, and unresolved external blockers.
