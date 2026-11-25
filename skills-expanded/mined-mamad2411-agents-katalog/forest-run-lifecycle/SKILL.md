---
name: forest-run-lifecycle
description: "Integrate FOREST run submission, controls, live output, recovery, budgets, and human intervention receipts. Use for run panels or execution-client changes that must preserve saved intent and current-versus-historical provenance; not for choosing scientific experiments."
---

# FOREST run lifecycle integration

Expose accepted intent and observed execution accurately across enqueue, control,
recovery, and completion. A UI redesign must preserve execution ownership.

## Establish the affected owner

Read [repository-map.md](references/repository-map.md) for the action matrix,
transport shape, source owners, and relevant regressions before changing controls.
The inspected snapshot is HEAD `ff16c3f656f94d053d1bba65c6b3a07a5feaccde`;
recheck the target source before treating its states/actions as current.
Paths in the map are FOREST-root relative. Trace only the touched route through
scheduler/control/readback and affected consumers; avoid an unrelated full audit.

Preserve the four canonical skills under `research/agents/skills/` and runtime
research semantics. Work-round boundaries, cumulative action/run counts, or a
completed node do not create a new scientific stopping rule.

## Model submission and observation separately

- One intended enqueue gets one retained `request_id`; store returned run IDs.
  A network error may leave acceptance unknown. Recover the same submission
  where supported rather than issuing another UUID automatically.
- Node run can return a Run or `{runs,run_ids}`; branch run returns `{runs}`;
  selected run submission returns `{runs,run_ids}`. Handle each real shape.
- Render run, node, controller, tool-decision, and intervention state independently.
  Never make a closed terminal, successful POST, or `queued` receipt imply success.
- Preserve nullable node/branch IDs, timestamps, PID, exit code, error, session,
  resource accounting, and spending values; absence is not zero or completion.
- Preserve unknown task configuration keys and saved historical provenance.
  Node edits affect new runs; retry preserves the selected run's saved context.

## Use the actual state/action contract

At the inspected HEAD, scheduler groups are:

```text
ACTIVE: queued running pausing paused waiting_input waiting budget_exhausted
TERMINAL: completed failed cancelled interrupted skipped
```

Wire status is an extensible string; render an unfamiliar value as unknown with
its raw value. Do not invent `succeeded`, merge blocked work into failure, or
interpret all terminal outcomes as successful. Completion, verification,
Goal applicability, and scientific handoff acceptance remain separate.

Supported `/api/runs/{ident}/{action}` controls are `pause`, `resume`, `cancel`,
`retry`, `skip`, and `priority`. Read the source-checked matrix in
[repository-map.md](references/repository-map.md) when enabling a control.
Server state and receipts decide whether it succeeded; UI enablement is guidance.
`retry` creates a new Run; `resume` continues the same Run and its accumulated usage.
Historical retry does not become a current node result after the node changed.

## Represent intervention effects

Keep request intent/revision, parent receipt, action-specific target identity, effect
status, observations, errors, and retry state inspectable. `accepted` differs
from `applied`; effects may be pending, uncertain, superseded, or partially applied.
For `materialize_workspace`, effect `run_id` contains a Branch ID; resolve it by
action instead of changing the contract or treating every effect as a Run.
`pausing` can represent pending lifecycle reconciliation, including Resume.
Do not optimistically mark processes paused/stopped until readback confirms them.
Poll/refetch intervention and run state after controls, remounts, and reconnects.

Ordinary comments are annotations. Explicit instructions use project/branch/node/
run scope and `next_request` or `next_run` boundary. An in-flight request retains
its context. These choices are not a Cartesian product: run scope requires an
active Agent run and `next_request`; reject/disable `next_run`, non-Agent runs and
stopped runs with the server's reason. Applied delivery means inclusion in a
successful physical model
request, possibly complete recorded pages; it does not prove semantic obedience.

Human action review preserves the exact proposed action and reviewed revision.
Accept/edit/reject is distinct from budget-checked execution. Show `resume_error`
and `can_resume`; Continue uses Resume for an already saved answer, not Answer
again. Cancellation closes unused decisions while preserving the saved rejection.

## Keep recovery and budgets honest

Read [repository-map.md](references/repository-map.md) when changing budget,
checkpoint, process recovery, import, or configuration editing.
Retain the original supervisor/attempt identity and show uncertain reconciliation.
Never launch a replacement solely because a browser lost contact.
`waiting` with `wait_for.type:work_round` is automatic continuation under the same
Run ID; it is not necessarily a human decision or completed research.
Resume checks remaining task/project/provider allowance and preserves prior usage.
Paused live work consumes wall time. Unknown cost/usage stays unknown.
Imported/duplicated control history does not transfer live execution authority.

## Read output and events correctly

Use the returned stdout byte `offset`, even with filtering or multibyte text;
never compute it from JS string length. Prevent duplicate chunk append after a
retried read and read the final chunk before ending terminal-run polling.
SSE is ordered invalidation/replay, not authoritative complete state. Retain its
sequence cursor; on `cursor_reset`, reload REST state and resume from the supplied
cursor. Terminal WebSocket lifecycle is separate from worker run lifecycle.

## Verify only the changed behavior

Choose targeted existing regressions from
[repository-map.md](references/repository-map.md): double submit/lost response,
state-gated controls, per-target reconciliation, stale retries, same-run resume,
usage preservation, multibyte output, and restart/history where touched.
Unit fixtures and local fake provider transports can check isolated logic.
Integrated changes also require an isolated real backend/worker workflow with
actual process effects and artifacts, guided by the browser-testing skill;
fixture-only output does not establish that integration. Do not start the user's
existing tasks or call an unauthorized paid provider. Report observed checks
and unresolved limitations without asserting unexecuted effects.
