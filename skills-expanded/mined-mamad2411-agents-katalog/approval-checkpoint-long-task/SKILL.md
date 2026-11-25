---
name: approval-checkpoint-long-task
description: Canonical long-task pack for daemon-managed work with deliberate approval checkpoints, status summaries, rollback notes, and mobile-safe governance-aware updates.
tags: [approval, long task, checkpoint, rollback, pause and resume, governed execution]
keywords:
  - approval
  - long task
  - checkpoint
  - rollback
  - pause and resume
  - governed execution
triggers:
  - long running task
  - approval checkpoint
  - pause for approval
  - resume after approval
context_tags:
  - workflow
  - governance
canonical_pack: true
delivery_modes:
  - manual
  - task
  - goal
  - chat-approval
prerequisite_hints:
  - "Daemon task/goal execution must be available."
  - "Remote/mobile approvals work best with configured chat gateways."
  - "Risky side effects require fresh approval at each checkpoint boundary."
source_links:
  - skills/zorai-mcp/operating/tasks.md
  - skills/zorai-mcp/operating/goals.md
  - skills/zorai-mcp/operating/safety.md
mobile_safe: true
approval_behavior: "This pack exists to require explicit checkpoints; risky transitions must pause and request fresh approval before resuming."
---

# Approval-Checkpoint Long Task

## User story

I want long-running work to pause at explicit checkpoints with clear status, next step, and rollback notes, so I can approve or deny risky transitions from in-app or mobile chat without losing context.

## Pack contract

### Prerequisites and readiness

- Reuses daemon task or goal primitives only
- Chat/mobile approval surfaces are optional but preferred for remote control
- If remote approval channels are unavailable, checkpoints must still work in-app

### Inputs and configuration fields

- `task_kind`: task or goal
- `checkpoint_titles`: ordered checkpoint labels
- `rollback_notes`: per-checkpoint rollback instructions
- `summary_cadence`: when to emit status summaries

### Outputs and delivery targets

- current checkpoint
- completed checkpoints
- next action
- rollback state / notes
- approval state and recovery guidance

## Manual run recipe

1. Start daemon task/goal with explicit checkpoint plan in the description.
2. Before each risky transition, summarize state and rollback notes.
3. Pause for approval.
4. Resume only after valid approval resolution.

## Example routine wiring

This pack is usually manual or task/goal-backed rather than purely cron-driven; if scheduled, it should only materialize the governed task template, not auto-bypass approvals.

## Example prompt

`Use the Approval-Checkpoint Long Task pack for this migration. Define checkpoints for backup, schema update, validation, and cutover, with rollback notes and mobile-safe approval summaries.`

## Failure and recovery behavior

- Stale approval -> reject and request a fresh checkpoint approval.
- Missing remote chat surface -> continue with in-app checkpoint approval.
- Failed checkpoint step -> report rollback notes before any retry.

## Verification checklist

- [ ] Manual proof pauses and resumes cleanly.
- [ ] Checkpoint summaries show current step, next step, and rollback notes.
- [ ] Stale approval is rejected cleanly.
- [ ] Mobile-safe status output is preserved.
- [ ] Pack reuses daemon task/goal runtime, not a side runtime.
