---
name: session
version: 1.0.0
description: Session lifecycle — checkpoint, restore, handoff, sleep/wake
uses:
  - core/memory
  - core/bus
requires:
  tools: []
  env: []
security:
  risk_level: write
  capabilities:
    - session:read
    - session:write
    - session:checkpoint
    - session:restore
  requires_approval: false
---

# Session

Manage the agent session lifecycle — starting, checkpointing, restoring, handing off work, and shutting down cleanly. Sessions are the boundary of an agent's active work period.

## Execution Model

This is a **builtin skill** (`handler: type: builtin`). When `session_status` is invoked, the executor returns current session state from the session directory (`.os/sessions/{agent}/{session-id}/`). The tool schema in tool.yaml defines the external contract; the executor handles session state management directly.

## When to Use

- Starting a new work session (boot sequence)
- Checking current session state and duration
- Creating checkpoints to preserve progress
- Restoring from a checkpoint after crash or context loss
- Handing off work to another agent
- Gracefully ending a session

## Methodology

### 1. Session Boot

On session start, execute in order:
1. Load identity from `identity.yaml`
2. Load core skills (bus, memory, session)
3. Check for existing checkpoint — restore if found
4. Register with coordinator (if configured)
5. Publish `session_start` to the `system` channel

### 2. Checkpointing

Checkpoints save session state for recovery. They happen:
- **Automatically**: After each bus message processed, every 5 minutes, before context compaction, on graceful shutdown
- **Manually**: When you want to ensure a critical state is preserved

Checkpoint content:
- Current task context (what you're working on)
- Bus position (last processed message ID)
- Working state (completed and pending items)
- Memory pointers (what to read on restore)

### 3. Restoring

On restore, load the checkpoint and resume:
1. Read last checkpoint from `.os/sessions/{agent}/{session-id}/checkpoint.json`
2. Restore task context
3. Restore bus position (don't reprocess old messages)
4. Restore working state
5. Continue from where you left off

### 4. Handoff

When passing work to another agent:
1. Create a checkpoint with full context
2. Publish a `handoff` message to the `work` channel with:
   - Who it's from and who it's for
   - Why the handoff is happening
   - Checkpoint path for context
   - Key information the receiver needs

### 5. Shutdown

On graceful shutdown:
1. Save final checkpoint
2. Update memory with session summary
3. Publish `session_end` to the `system` channel
4. Deregister from coordinator

## Output Format

```
## Session Status

- Session ID: [ID]
- Agent: [agent name]
- Status: [active/sleeping/shutting-down]
- Duration: [time since start]
- Messages processed: [count]
- Last checkpoint: [timestamp]
- Current task: [description or none]
```

## Quality Criteria

- Boot sequence completes in order (identity, skills, checkpoint, register, announce)
- Checkpoints are saved regularly (not just at session end)
- Checkpoint content is sufficient for full restore
- Handoff messages include enough context for the receiver
- Shutdown is graceful (checkpoint, memory, bus, deregister)
- Crash recovery restores to last checkpoint without data loss

## Recovery (Auto-Restart)

Sessions automatically restart when context is exhausted (up to `max_restarts` times). The recovery system:

- **Detects context exhaustion** from CLI stream events (`stop_reason=max_tokens`) or process exit without a result event
- **Restarts the CLI** with `--resume <session-id>` to restore full conversation history
- **Sends a continuation prompt** from `.os/skills/core/session/prompts/restart.md` telling the agent to read its memory and continue
- **Preserves heartbeat and bus loops** — only I/O tasks are restarted

Agents can influence recovery:
- **Commit early and often** — small commits prevent lost work across restarts
- **Save memory** — write to `.os/agents/{name}/memory/` so context survives
- **Signal completion** — model choosing `end_turn` prevents unnecessary restart

Configuration: `wrapper.max_restarts` (default 3), `wrapper.restart_cooldown` (default 5s), `wrapper.restart_backoff` (default 2x for error exits).

## Common Mistakes

- **Skipping checkpoint before risky operations**: If something might crash the session, checkpoint first. Recovery without a checkpoint means starting from scratch.
- **Not restoring bus position**: After restore, if you don't set the bus position to the last processed message, you'll reprocess old messages.
- **Incomplete handoff context**: Sending a handoff with just "please continue" gives the receiver no context. Include the task, progress, key files, and what's next.
- **Forgetting session_end on shutdown**: If you don't publish session_end, other agents and the coordinator think you're still active.
- **Not updating memory before shutdown**: Session knowledge that isn't saved to memory is lost permanently.
- **Ignoring checkpoint on boot**: If a checkpoint exists and you skip it, you lose all progress from the previous session.

## Completion

Session management is complete when:
- Boot: All steps completed (identity, skills, checkpoint, register, announce)
- Checkpoint: State is saved and can be restored
- Handoff: Receiver has enough context to continue
- Shutdown: Checkpoint saved, memory updated, session_end published, deregistered
