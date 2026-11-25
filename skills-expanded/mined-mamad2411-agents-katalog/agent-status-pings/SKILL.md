---
name: agent-status-pings
description: "Emit standardized progress pings during long-running work so the coordinator and the user know whether you are alive, stuck, or done — never go dark."
---

# Agent status pings

Long-running agent work (research, refactors, multi-step planning) MUST surface a heartbeat. Silence is the worst possible signal in a multi-agent system because the coordinator cannot tell silence from a stalled process.

## When to use

- Any task you estimate will take more than 60 seconds of agent time.
- Any task spawned by a coordinator under `parallel-agent-coordination`, `swarm-coordination`, or `crew-manager-pattern`.
- Any plan executed under `crew-planner-executor` once you cross the first executor step.

## The ping format

Use a short, structured message (Slack thread, planning task comment, or assistant message) with three fields:

```
status: <starting|working|blocked|waiting-for-human|done|failed>
progress: <one short sentence — what you finished, what you're doing next>
next_eta: <ISO timestamp or "<N> minutes">
```

Examples:

```
status: working
progress: parsed 3 of 7 repos; next is monorepo X
next_eta: 4 minutes
```

```
status: blocked
progress: terraform plan errors on missing IAM role poly-deploy
next_eta: human input needed; paused pending Slack reply
```

## Cadence

- First ping within 30 seconds of starting (`status: starting`).
- Recurring `status: working` ping every 3–5 minutes, OR after every meaningful sub-step.
- Final ping is `status: done` (with a brief result summary) or `status: failed` (with the failure reason and what you tried).
- A `blocked` ping must include WHAT would unblock you — not just that you are stuck.

## Where to send pings

- For agents wired into planning: append a comment on the parent task via `planning_list_tasks` → comment write.
- For Slack-enabled initiatives: post in the agent's thread channel.
- Always also append to your assistant reply so the human user sees it inline.

## Anti-patterns

- Going silent for >5 minutes mid-task.
- Pinging only on success.
- A `blocked` ping that does not say what unblocks it.
