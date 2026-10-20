---
name: sprint-loop-controller
description: State machine for /sprint:loop. Decides next action (pull task, run gate, wait, exit) based on .sprints/active/_state.json + tool-history.log + safety knobs. Used by sprint-loop command.
---

# sprint-loop-controller

## State diagram

```
[start]
   │
   ▼
[idle] ──pull next task──▶ [executing]
   │                            │
   │                            ├──gate fired (test-first/checkin)──▶ [gate_blocked]
   │                            │                                          │
   │                            │◀──── auto-resolve OR user fix ────────────┘
   │                            │
   │                            └──task complete──▶ [task_done] ──▶ [idle]
   │
   └──no more tasks──▶ [cycle_done] ──▶ [exit]

[any state] ──max-tasks/max-duration/error──▶ [exit]
```

## Decision rules

| State | Condition | Action |
|-------|-----------|--------|
| idle | tasks remain in plan | start next task |
| idle | no tasks | transition cycle_done |
| executing | tool-history shows progress in last 5 min | wait |
| executing | inactivity > grace | trigger checkin |
| gate_blocked | strictness=lenient AND gate=test-first | invoke codex-rescue with auto-write test prompt |
| gate_blocked | strictness=strict | wait for human |
| cycle_done | retro present | exit |

## Integration

Loop tick = single skill invocation. Skill reads state, returns:
```json
{
  "next_action": "pull_task|wait|invoke|complete|exit",
  "wait_seconds": <int>,
  "reason": "..."
}
```

Used by `/sprint:loop` driver to know whether to ScheduleWakeup or exit.
