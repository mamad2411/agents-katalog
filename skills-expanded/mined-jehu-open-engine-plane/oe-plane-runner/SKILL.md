---
name: oe-plane-runner
description: Run exactly one Open Engine queue check in Plane for a production runtime using the deterministic runner/helper. Use for Plane-based agent handoffs, runtime status ledger updates, status transitions, and AGENT receipt comments.
triggers:
  - "run open engine queue"
  - "plane queue runner"
  - "open engine smoke test"
  - "agent handoff in plane"
---

# Open Engine Plane Runner

Use this skill when you are acting as an Open Engine runtime that processes work items in the Plane project `Open Engine`.

Open Engine coordination is stigmergic: the runtime reads visible Plane traces, performs one scoped local action, and leaves improved traces for humans or later agents. The runner pattern is:

```text
observe queue trace → claim one eligible task → do scoped work → leave terminal receipt
```

## Runtime identity

- Determine your runtime agent code before processing work.
- The invoking runtime must provide its agent code explicitly, for example via prompt, scheduler configuration, environment wrapper, or command argument.
- Valid production routes are defined in Plane routing map work item `#2`.
- Only process work items whose title matches `[agent instructions][<agent-code>][task] ...`.
- Queue eligibility is determined by visible route traces: state `Agent Todo`, label `agent-instructions`, and title route `[agent instructions][<agent-code>][task] ...`.
- The Plane issue assignee remains the human/operator owner. The central Open Engine Bot may be the API actor, but it is not the default eligibility filter.
- `OPEN_ENGINE_OPERATOR_UUID` is optional scoping only. When unset, the helper does not fall back to `/api/v1/users/me/`; human assignees are read from the selected issue for review/input/hold/failure mentions.

## Normal queue check

Process **at most one task work item per run**.

1. Run the deterministic entrypoint with either an explicit argument or `OPEN_ENGINE_AGENT_CODE`:
   `scripts/run_one_queue_check.sh <agent-code>`
   or `OPEN_ENGINE_AGENT_CODE=<agent-code> scripts/run_one_queue_check.sh`
2. Follow exactly one returned action:
   - `recover_working_task`: inspect detail/comments and continue without a second claim.
   - `resume_paused_task`: run the returned `resume_command`, then continue scoped work.
   - `inspect_paused_task`: do not claim new work; stop unless a safe private answer is already available.
   - `process_new_task`: inspect detail, run the returned `claim_command`, do scoped work, then finish.
   - `no_work`: stop.
3. Finish with one terminal helper command: `done`, `block`, `hold`, or `fail`.
4. Stop after that one item.

Use lower-level helper commands only for state transitions, receipts, detail lookup, or debugging:

`scripts/plane_queue_helper.sh status|routes|validate-route|next|working|paused|detail|comments|ledger|claim|done|block|hold|resume|resume-hold|fail ...`

Read `references/plane-api-contract.md` only when debugging/extending Plane API behavior beyond the runner/helper.

## Additional helper commands

- `review <agent> <seq> [message]`: complete work requiring human review (`AGENT DONE` + `Agent Review`).
- `preflight <agent>`: standing-context version/hash snapshot before task work.
- `delegate <source> <target> <parent-seq> <title>`: create a delegated task for target agent and post `AGENT DELEGATED` on parent.
- `follow-up <agent>`: check delegated tasks for terminal/review status changes and post `AGENT FOLLOW-UP` where needed.
- `delegated <agent>`: list delegated tasks created by this agent.
- `assignee-check`: print the optional `OPEN_ENGINE_OPERATOR_UUID` queue scope, or empty when no operator scope is set.

## Required processing order

The runner enforces this order; preserve it if working manually:

1. Validate production route.
2. Update this runtime's `AGENT STATUS` ledger entry to `checking`.
3. Check own `Agent Working` items for crash/retry recovery.
4. Check own paused `Agent Needs Input` items.
5. Check oldest eligible `Agent Todo` item.
6. If no work exists, update ledger to `none` and stop.

## Trace-first execution rule

The Plane issue is the shared coordination medium. During execution:

- Treat the issue title, body, labels, state, comments, and artifacts as the source of local truth.
- Do not rely on hidden chat context for essential task requirements.
- If work changes files, creates artifacts, delegates, blocks, fails, or needs review, make that visible through the helper state transition and receipt.
- A terminal receipt should identify the runtime agent code, summarize changes, name verification performed, reference artifacts, and state the next expected action when one exists.
- Keep comments concise and actionable so the shared medium remains readable.

## Correctness rules

- Never process unknown agent routes in production.
- Never claim success for a status change unless the helper verifies the final state.
- Never write a second `AGENT CLAIMED` for an already claimed item.
- Leave exactly one terminal receipt per run: `AGENT DONE`, `AGENT BLOCKED`, `AGENT HUMAN HOLD`, or `AGENT FAILED`.
- `AGENT HUMAN HOLD` is only for private operator-thread requirements: local runtime permission, install approval, account authority, private context, credentials, or external/destructive approval.
- Do not use `AGENT HUMAN HOLD` just because the issue contains an `If blocked` section.
- If no actual information, permission, or authority is missing, complete the scoped task.

## Intake rule

New or unclear work belongs in Plane Triage/Intake/Backlog. A work item may enter `Agent Todo` only after it is agent-ready: requester, desired outcome, sources, acceptance criteria, boundaries, target runtime/agent code, output handoff, and blocker rule are present or explicitly not needed.

## Receipt vocabulary

Receipts are persistent system memory and handoff signals. Use exact receipt tokens in Plane comments:

- `AGENT CLAIMED`: after verified move to `Agent Working`.
- `AGENT DONE`: scoped work complete. Pair with `Agent Done` when no review is needed, or `Agent Review` when human review/QA/approval is required.
- `AGENT BLOCKED`: missing answer belongs on the Plane work item.
- `AGENT HUMAN HOLD`: missing answer belongs in the human's private agent thread/app.
- `AGENT UNBLOCKED` then `AGENT RESUMED`: Plane blocker answered.
- `AGENT HUMAN ANSWERED` then `AGENT RESUMED`: private human hold answered.
- `AGENT FAILED`: unrecoverable failure or unverifiable state change.
- `AGENT DELEGATED`: posted on parent issue when work is delegated to another agent.
- `AGENT FOLLOW-UP`: posted on delegated issue when source agent observes a terminal/review status change.
- `AGENT STATUS`: status ledger heartbeat/result.

## Boundaries

Never publish, email, Slack-post, deploy, delete, change billing, change credentials, or make outward-facing changes unless explicitly approved in the work item.

## Plane description formatting

When creating or updating Plane work item descriptions through the API, set compact one-line `description_html`. Do not set `description_stripped`; Plane generates it from `description_html`.
