---
name: delivery-planning
description: Turns an approved architecture into an ordered plan of atomic engineering tasks with dependencies, affected modules, validation requirements and tests, grouped into milestones and sequenced so that nothing is built before what it depends on. Run immediately after the validation gate.
license: MIT
metadata:
  category: delivery-skills
  version: 1.0.0
  depends_on: [engineering-core, architecture-proposal, validation-gate]
  outputs: [milestone-plan, task-breakdown, dependency-order, parallelisation-map]
---

# Delivery Planning

Converts an approved architecture into work that can be executed one task at a
time, in an order where nothing waits on something that does not exist yet.

The plan is a working instrument, not a document produced for its own sake. It
is short enough to update and specific enough to execute.

## 1. Milestones

Group tasks into milestones that each end in something demonstrable. A
milestone that produces nothing observable is a phase of the plan, not a
milestone.

Typical order, adapted to the architecture:

```
M0 Foundation      repository, tooling, configuration, CI skeleton
M1 Data            schema, migrations, seed, the data layer
M2 Identity        authentication, then authorization
M3 Core domain     the business rules the product exists for
M4 API             the endpoints over the domain
M5 Frontend base   layout, design system usage, routing, data layer
M6 Features        one milestone per feature group, each end to end
M7 Integrations    external services, each with its failure path
M8 Hardening       security, performance, accessibility passes
M9 Operations      environments, pipeline, deployment, observability
M10 Delivery       documentation, handover, release
```

Feature milestones are vertical, never horizontal. `M6a invitations, end to
end` is a milestone. `M6 all backends, then M7 all frontends` is a plan that
discovers its integration problems at the end, when they are most expensive.

## 2. Atomic tasks

A task is atomic when it can be implemented, reviewed and committed on its
own, and when its completion is observable.

```
ID           stable, referenced by commits and the checklist
Objective    one sentence, what is true afterwards
Requirement  which requirement or architecture section it serves
Depends on   task identifiers, not descriptions
Modules      the files or areas it touches
Implements   what to build, concretely
Validates    what input it must reject, if any
Authorizes   who may do it, if any
Tests        the cases that must exist, named
Done when    the observable condition
```

Sizing: if `Implements` needs more than roughly five lines, the task is two
tasks. If `Depends on` lists more than three tasks, the ordering is probably
wrong.

## 3. Dependency ordering

Order by what a task needs to exist, not by what is interesting.

```
configuration  before  anything that reads it
schema         before  the data layer
data layer     before  the services
identity       before  any authorized endpoint
services       before  the endpoints over them
API contract   before  any frontend consuming it
design system  before  the components using it
a feature      before  its end to end test
observability  before  the first deployment, not after the first incident
```

The last line is the one that gets reordered under time pressure, and it is
the one that costs the most when a deployment misbehaves.

## 4. Parallelisation map

Mark each task with what it may run alongside. The rule from
`delivery-orchestrator` section 6 applies: parallelise across a contract,
never across an unknown.

```
| Task | May run with | Must wait for |
|---|---|---|
| T21 invitation endpoint | T22 invitation UI | T14 contract fixed |
| T22 invitation UI | T21 | T14 |
| T23 invitation e2e | nothing | T21, T22 |
```

The contract task, T14 here, is what makes T21 and T22 safe to parallelise. It
is a real task with a deliverable, not a note.

## 5. Estimation

Estimates are stated as ranges with their driver, or omitted.

```
Good:  T21, half a day to a day. The range is the idempotency handling, which
       depends on whether the provider's key semantics match ours.
Bad:   T21, 4 hours.
```

A precise estimate on unfamiliar work is a guess wearing a number. When the
project has a deadline, the plan states which milestones fit inside it and
which do not, rather than compressing every estimate until the arithmetic
works.

## 6. What the plan is not

- Not a Gantt chart. Dependencies and order, not dates on a grid.
- Not a restatement of the architecture. It references sections, never copies
  them.
- Not a place for design decisions. Those belong in the architecture, and a
  task that needs one has revealed a gap in the proposal.
- Not permanent. It is updated as the work reveals reality, and the update is
  part of the work.

## 7. Replanning

The plan changes. That is expected and is not a failure.

Replan when: a task turns out to depend on something unbuilt, a milestone
grows past its purpose, a discovery invalidates an ordering, or an external
dependency becomes unavailable.

Do not replan for: a task taking longer than estimated, a bug found during
implementation, or an ordinary refactor.

A replan that changes the approved architecture is not a replan. It goes
through `scope-and-change-control`.

## 8. Protocol

1. Take the approved architecture and the requirements mapping.
2. Derive milestones, section 1, each ending in something demonstrable.
3. Break each milestone into atomic tasks, section 2.
4. Order by dependency, section 3.
5. Build the parallelisation map, section 4, and name the contract tasks.
6. Attach tests to every task that changes behaviour.
7. Check coverage: every requirement in the mapping is served by at least one
   task.
8. State the plan in one page plus the task list.
9. Update it as reality arrives, section 7.

## 9. Auto-critique

Score from 0 to 5: milestones demonstrable and vertical, tasks genuinely
atomic, dependencies by identifier, ordering respects section 3, contract
tasks named before parallel work, tests attached, every requirement covered,
plan short enough to maintain.

Threshold: no axis below 3, average at least 4. A requirement with no task, or
parallel tasks with no contract between them, is an automatic failure.

## 10. Interfaces

- Upstream: `validation-gate`, `architecture-proposal`.
- Downstream: `engineering-orchestrator` executes each task,
  `delivery-orchestrator` tracks completion.
- Related: `scope-and-change-control` when a task reveals an architectural
  gap.
