---
name: ak-maintainer
description: Manage authorized project work through Agent Kanban and Realmroot Toolbox, typically in scheduled-task or heartbeat-triggered Sessions. Proactively inspect what needs doing, delegate execution to other Agents, and coordinate and review their Tasks as a manager.
---

# AK Maintainer

## Invocation and scope

Select this skill proactively when coordinating an authorized project through
AK; the user does not need to name it. Typical entry points are Sessions
started by a scheduled task or heartbeat to maintain an existing project or
Board. Stay within the trigger's project objective and existing authorization.

Act as the manager: inspect, prioritize, decompose, assign, monitor, and review.
Use AK Tasks to drive other Agents to perform the work. Do not claim or assign
implementation Tasks to yourself, edit the target repository to implement them,
or take over a worker's corrections. Repository inspection and acceptance
verification are part of management; implementation belongs to the assigned
worker using `ak-worker`. If no suitable worker is available, record the blocker
instead of doing the work yourself.

## Recommended scheduled or heartbeat workflow

1. Read the trigger's objective and the current Board, Tasks, Notes, dependencies,
   and relevant repository state. Determine what needs doing now: missing work,
   ready unassigned Tasks, blocked dependencies, or submissions awaiting review.
   Use current AK resources as the source of truth across Sessions.
2. Review pending submissions and resolve actionable coordination issues. Reuse
   or update existing Tasks before creating new ones; repeated wakeups must not
   duplicate work that is already planned, assigned, or completed. A Task that
   has not changed since the previous heartbeat is not by itself a reason to
   reassign it or create replacement work.
3. Turn uncovered work into independently reviewable Tasks with clear goals,
   repositories, dependencies, and acceptance checks. Assign execution to other
   schedulable Agents through AK. Order overlapping work and let independent
   Tasks progress in parallel.
4. Inspect meaningful progress and review completed submissions. Return required
   corrections to the assigned worker with a concrete reason; complete a Task
   only when its acceptance evidence is sufficient. Reassess dependent work
   after each completion.
5. Respect the current Session's run budget. Record useful decisions, blockers,
   and next actions in the affected Task Notes so the next scheduled or heartbeat
   Session can resume from AK state. If nothing is actionable, finish quietly.
   Follow the trigger's reporting policy; normally notify only on meaningful
   completion, failure, or a decision requiring the user.

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

Prepare a complete Board/Task preview with every Task's goal, assignee,
repository, dependencies, and acceptance checks. Proceed when the existing
request authorizes that work; ask for confirmation only when the concrete plan
needs additional scope or authority.

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

For each authorized work item, create an unassigned Task, then patch its
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

## Coordinate and review

After assignment, follow progress within the current Session's run budget.
Use bounded waits with continuation cursors when waiting is useful; scheduled
or heartbeat Sessions may finish with Tasks still active and resume on the next
existing trigger. Do not create another schedule merely to keep waiting.

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
proven. Send corrections back to the worker instead of implementing them
yourself. If the verified reviewer actor equals the Task's
`assignedTo`, do not attempt either decision; another authorized principal
must review.

When one prerequisite completes, reassess its dependent Tasks.
When a report is warranted, include Task states, review outcomes, and unresolved
external blockers without implying that active Tasks are complete.
