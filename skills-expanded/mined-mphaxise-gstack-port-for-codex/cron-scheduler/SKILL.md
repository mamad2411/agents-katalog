---
name: cron-scheduler
description: Codex automation scheduling for recurring work, thread heartbeats, reminders, workspace checks, local/worktree automation choices, and safe cadence planning.
---

# Cron Scheduler

Use this skill when the user wants recurring agent work, reminders, a recurring follow-up, or help deciding how a Codex automation should run.

This port is adapted from `garrytan/gbrain` at commit `0b47afbf402a4e27a648bb9d131ce584461461ea`.

## Important Adaptation

Upstream GBrain assumes raw cron jobs, host schedulers, and held notification queues. In Codex, the closest native primitives are:

- thread heartbeats for same-thread wakeups and sub-hour follow-ups
- standalone/project automations for independent recurring work against one or more workspaces
- local-project or worktree execution for Git repositories, chosen by whether the run may safely touch the active checkout
- sandbox and approval settings inherited by unattended automation runs

Before scheduling anything, read:

- `references/automation-patterns.md`
- `references/quiet-hours.md`

## Workflow

1. Decide whether the task should stay in the current thread or run as a standalone recurring job.
2. Decide whether project automation should run in the local checkout or a worktree:
   - use a worktree when changes should be isolated from active local work
   - use local mode only when direct access to the main checkout is required and the user accepts that it can modify active files
3. Write a thin automation prompt:
   - describe only the durable task
   - keep schedule and workspace details out of the prompt body
   - add gating rules such as "only if new commits landed" or "skip if the report already exists"
   - include when to stop, no-op, or ask the user for input
4. Choose the cadence in the user's local time:
   - prefer waking hours unless the user explicitly wants overnight activity
   - offset multiple recurring jobs by 5-15 minutes when they would otherwise bunch up
   - prefer a morning digest or follow-up over noisy overnight wakeups
5. Check whether the current sandbox/approval settings are sufficient for unattended work.
6. Create or update the automation with `automation_update`.
7. Confirm the schedule, workspace/local-vs-worktree choice, and sandbox assumption in plain language.
8. If a similar automation already exists, update or replace it instead of creating a duplicate.

## Decision Rules

- Prefer a thread heartbeat when:
  - the work depends on current thread context
  - the user asked for follow-up in this conversation
  - the cadence is below one hour
- Prefer a cron automation when:
  - the work should run independently of this thread
  - the task is workspace-oriented
  - the cadence is hourly or weekly and does not need conversational context
- Prefer a worktree-backed project automation when:
  - the automation may edit files
  - the user has active local work in the checkout
  - the run should produce a reviewable branch or isolated artifact

For recurring brain work, prefer one multi-source sync surface over competing per-source jobs. Every recurring task must be idempotent or document its deduplication key, state file, and retry behavior.

## Guardrails

- Do not stuff giant prompts into an automation when a short task description will do.
- Do not create duplicate automations when an update is cleaner.
- Avoid schedules that create overnight inbox churn unless the user explicitly asks for that tradeoff.
- Keep recurring tasks idempotent so repeated runs do not duplicate work.
- Use `ACTIVE` by default; only start paused if the user asks.
- Do not schedule unattended work that requires approvals unless the prompt can safely no-op or report the blocker.
