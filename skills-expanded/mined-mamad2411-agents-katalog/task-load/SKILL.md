---
name: task-load
description: >
  Load the next unblocked TASK as a complete agent brief — context,
  implementation steps, and acceptance criteria. Use when the user says
  load the task, next task, start building, hand this to the agent,
  or runs /ultimate-sdd:load or /ultimate-sdd:next.
license: MIT
metadata:
  author: andrewr303
  version: "2.0"
---

Load a complete brief only after deterministic eligibility checks.

**Read:** `references/execution.md`, `references/handoff.md`, `references/model.md`, and `templates/handoff-template.md`.

## Resolve and gate

Use a named `REQ-n/TASK-k`. A bare TASK-k is valid only when its parent is unambiguous. Otherwise run `plan.py next --root "<root>" --json` in the target repo and follow its graph-derived action; do not pick work from stale chat/INDEX memory. If Next is Specify/Scope or selection is ambiguous, stop with that action.

Before writing the handoff, changing status, or building, run:

```text
python "<plugin>/scripts/sdd.py" config --repo "<repo>" --root "<root>" --json
python "<plugin>/scripts/sdd.py" gate --task REQ-n/TASK-k --phase load --repo "<repo>" --root "<root>" --json
```

Require exit code 0 and `ok: true` from the load gate. Parent readiness >= 4 is necessary, not sufficient: eligible TASK/REQ statuses and both REQ and TASK blockers matter. Missing runtime, malformed result, low readiness, blocked/done/cancelled work, or other gate errors prevent loading. Never mutate configuration or status to bypass a failure.

## Write the brief

Follow the handoff reference/template, preserving section order and the all-green context/steps/AC checklist.

- Copy owned AC **verbatim** from the on-disk REQ's IDs in TASK `ac:`.
- Include only relevant platform/business context and source paths; name allowed and forbidden file scopes.
- Use written TASK steps. Hollow steps or missing AC return to Scope/Specify, not improvised implementation. If the contract is corrected, re-run the load gate before dispatch.
- In Verify, include validated policy, approved exact check argv/cwd, evidence destinations, TDD applicability, and the ordered independent reviews/complete gate. Commands in plan text are not automatically authorized to execute.

Write `<root>/tasks/REQ-n/TASK-k.handoff.md` in the target repo. TASK → `in-progress`; REQ → `in-progress` if it was `ready`. Update INDEX in the same turn with `plan.py board --root "<root>" --write`, then `plan.py validate --root "<root>"`. Do not change contracts after successful review without refreshing the evidence.

## Stop or build

If the user only said **load**, output the brief and stop. Do not implement siblings. For **start building / load and build**, implement this TASK only through `agents/implementer.md` and `plan-tdd`, then `task-verify`.

The full path is load gate → narrow implementation/tests → fresh independent spec review → quality review only after spec passes → complete gate → done. `execution_mode:inline` allows building, not independent self-review; absent subagent capability leaves `PENDING_INDEPENDENT_REVIEW`. Never create fake reviewer identities or automatic git commits/reverts. Multiple authorized TASKs follow the disjoint-files plus independent-graph policy in `references/execution.md`.
