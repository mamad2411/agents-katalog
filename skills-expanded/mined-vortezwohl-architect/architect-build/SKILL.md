---
name: architect-build
description: "Manual-only skill. Use only when the user explicitly invokes the architect-build skill to execute one sealed plan in order, preserve its hard functional boundary, adapt cautiously when the code impact scope expands, record execution-time decisions truthfully, and request a user decision only when the functional boundary cannot be preserved. Do not auto-trigger from a generic implementation request."
---

# Architect Build

Use this skill only as the manually selected `architect-build` stage. Its job is to
execute the sealed plan from start to finish, preserve its hard functional
boundary, and keep execution state and logs truthfully aligned with actual
progress. It may make cautious, local, execution-time minimal design decisions
when the recorded code impact scope proves incomplete, but it does not reopen
earlier stages or silently change the approved functionality. It is stage 3 and
the final stage of the one-way flow `architect-design -> architect-propose ->
architect-build`.

## Defined Terms

- `functional boundary`: the approved target functionality, protected related
  functionality, explicit non-goals, compatibility obligations, and hard-stop
  condition. It is a hard execution constraint.
- `code impact scope`: the recorded expected paths, symbols, configuration,
  tests, and callers likely to be affected. It is a coverage-oriented reference,
  not a permission list or a prohibition list.
- `impact-scope adaptation`: a cautious execution-time assessment and minimal
  implementation decision made when required work extends beyond the recorded
  code impact scope but remains inside the functional boundary.
- `functional-boundary exception`: a user-approved runtime decision made only
  after build proves that the target cannot be completed without changing
  protected functionality or a non-goal.

## Manual Invocation Only

- Run this skill only when the user explicitly asks for `architect-build`.
- Do not auto-switch into `architect-design` or `architect-propose`.
- Do not reopen earlier stages from this skill.

## Strict Boundary

- Do not alter the approved target functionality, protected related
  functionality, explicit non-goals, or compatibility obligations without an
  explicit user decision under the recorded functional-boundary escalation.
- Do not edit task or design Markdown files after the plan is sealed.
- Treat the code impact scope as evidence to reassess, not as a hard source
  modification limit. Do not silently expand it.
- When the code impact scope is incomplete but the functional boundary is
  preserved, perform and record a cautious impact-scope adaptation before
  applying the smallest justified change.
- Stop only when no viable minimal implementation can preserve the functional
  boundary. Present the recorded analysis, a recommendation, and scenario-
  specific numbered options to the user. Derive the number, content, and
  tradeoffs of those options from the proven conflict; do not require a fixed
  option count or predefined decision paths. Do not continue until the user
  selects an approving option.
- Do not silently skip a required status update or log update.
- Do not claim progress, completion, or task-declared execution result that did
  not actually happen.
- Do not invoke, reopen, or route execution back to `architect-design` or
  `architect-propose`. The stage order remains irreversible.

## Core Outcome

Execute the stored package as one engineering run, not as a new
`architect-design` pass:

- load the sealed plan, full task sequence, current state, and current log;
- execute all recorded tasks in order until the stored plan is fully run;
- preserve every recorded functional boundary while executing each `T-xxx` task
  and its cited `D-xxx` units;
- proactively restate the core `architect-design` context needed by the current
  tasks when
  the live context has been compressed or diluted;
- adapt the code impact scope cautiously when repository evidence proves that
  the recorded reference surface is incomplete;
- escalate only genuine functional-boundary conflicts to the user, without
  reopening earlier stages;
- update task status as work actually advances;
- update the execution log with actual actions, results, and task-declared
  execution results as they happen;
- keep moving through the stored execution path instead of questioning the
  sealed solution.

## Start Condition

Before any source edit, read the sealed plan, protocol version, current
execution state, current execution log, task catalog, every pending `T-xxx`
task, and every referenced `D-xxx` document needed for the current execution
window. Rebuild the current task's functional boundary and code impact scope
from those artifacts. Use them as the execution source of truth for this run.

When the live conversation no longer contains the active objective, the current
task, the cited design rules, the current execution state, or the latest
factual log evidence, proactively rebuild a compact working context from the
package. That rebuilt context must include exactly those five items. Do not
rely on memory when the package already contains the needed context.

## Execution Loop

Run through the remaining task sequence in recorded order within the same
manual `architect-build` invocation:

1. Announce the next `T-xxx` task, its cited `D-xxx` units, target
   functionality, protected related functionality, explicit non-goals, code
   impact scope, `MUST DO`, `MUST NOT DO` rules, and the functional-boundary
   escalation trigger.
2. Restate the task's required design context before editing. That restated
   context must include the task objective, the cited `D-xxx` rules, the
   functional boundary, code impact scope, current execution state, and the
   latest relevant factual log entry.
3. Perform the declared atomic steps. When a necessary path, symbol, helper,
   wrapper, local state transition, or implementation detail is absent from the
   code impact scope, first assess the actual caller and behavior impact,
   compare the smallest viable alternatives, confirm that the functional
   boundary remains intact, and record the chosen impact-scope adaptation in
   state and log before editing.
4. If the target cannot be completed without changing protected related
   functionality, an explicit non-goal, or a compatibility obligation, stop.
   State why no compliant minimal design exists, show the impact-scope
   evidence considered, recommend the best path, and derive a problem-specific
   numbered set of reliable options with functional, compatibility, risk, and
   verification consequences. Continue only after the user selects an approving
   option;
   record the selected functional-boundary exception in state and log.
5. Immediately update task state when the task meaningfully changes status:
   started, in progress, or completed.
6. Immediately append log entries that record actual actions taken, affected
   scope, actual results, and actual task-declared execution results.
7. Perform only the task-declared execution-result steps already recorded in the sealed
   task, then record the real result in state and log without embellishment.
8. Continue directly to the next recorded task until all remaining tasks in the
   plan have been executed.

## Completion Standard

Finish only after the full recorded task sequence has been executed, every
required task-declared execution result has been recorded truthfully, and the
state and log accurately reflect what actually happened across the entire run.
The final report must distinguish completed evidence, impact-scope
adaptations, user-approved functional-boundary exceptions, and remaining risk,
without reopening `architect-design` judgment during the `architect-build`
stage. Do not report an execution-time decision as if it had been part of the
original sealed plan.
