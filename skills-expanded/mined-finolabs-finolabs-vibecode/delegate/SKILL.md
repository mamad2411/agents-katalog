---
name: delegate
description: Route and run work across coding agents (Claude Code, Codex, Antigravity, ZCode). Use when choosing the agent and model per task, handing a task to an agent, running tasks in parallel, when quota runs out, a watched run stalls or times out, or running a spec with a session per task. One brief or handover is handoff.
---

# Delegate

Read [references/entry.md](references/entry.md) before dispatch: canonical host config, dependencies and references; project rules win.

## Delegation mode

Read [references/delegation-mode.md](references/delegation-mode.md) for this step.

Offer neutral Yes and No choices with none preselected or marked recommended; a default, a timeout or an auto-selected option never counts as the yes.

## The loop

Read [references/loop.md](references/loop.md): grade, route, brief, dispatch, watch, accept, record; name runs as `tidy` "Titles" says.
Accept starts with `log_scan.py scan <log>` and `log_scan.py show <log>`; finish uses `ledger.py finish --log-path <log>`.
Report a leak by name, never chase it; the reference owns redaction and the environment-only residual-risk report.

## Grade
Read [references/grade.md](references/grade.md) for this step.

## Route
Read [references/route.md](references/route.md) for this step.

For reviews, route reviews with `review_route.py`; the reference retains reachability and quota checks.

### Keep or hand off

Follow the accounting rule in [references/route.md](references/route.md).

## Capabilities and budget

Read [references/capabilities-and-budget.md](references/capabilities-and-budget.md) for this step.

## Parallel dispatch

Read [references/parallel-dispatch.md](references/parallel-dispatch.md) for family pools and advisory slots.

## Budget and liveness

Read [references/budget-and-liveness.md](references/budget-and-liveness.md) for this step.

## Heavy jobs

Read [references/heavy-jobs.md](references/heavy-jobs.md) for this step.

## Accept

Use `checks` "Accepting someone else's work"; read [references/accept.md](references/accept.md) for the receipt gate, which of `checks.py run --dispatch <id>` (an approved check list) or `verify_claim.py` (the brief's tests) writes the receipt, and the explicit exception for work with nothing to check. The coordinator retains the verdict.

## Handover after an interrupted run

Read [references/handover-after-an-interrupted-run.md](references/handover-after-an-interrupted-run.md) for this step.

## Where files go

Read [references/where-files-go.md](references/where-files-go.md) for this step.

## Ledger

Record every dispatch with `scripts/ledger.py` in this skill's base directory, at the moment it happens: a `start` line at dispatch, a `finish` line when the run is accepted, rejected or stopped. Commands, the agent values and what `summary` reports are in [references/ledger.md](references/ledger.md). The ledger holds short task labels only: no task data, secrets or personal data.

## Related skills

- `handoff`: write the brief and dispatch one task.
- `advisor`: one second opinion or two contrasting families for root cause or planning when stuck, all read-only.
- `status`: the usage dashboard (router coverage, skill use, load cost, delegation, review gate) and the runs still open.
