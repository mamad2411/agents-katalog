---
name: statemaster-promptforge-state-management
description: >
  Use when managing conversation state, context preservation across sessions,
  memory synchronization, and state recovery for multi-agent workflows. This skill
  ensures no context is lost between agent interactions or across session boundaries.
---

# StateMaster - State Management & Context Preservation

## Overview
StateMaster manages state and context preservation for PromptForge AI. In multi-agent workflows, state includes conversation history, decisions made, partial results, and workflow progress. Losing state means losing work and forcing agents to redo effort.

## When to Use
- When preserving context across agent handoffs or session boundaries
- When implementing state recovery after agent failures or restarts
- When synchronizing state between parallel agents working on the same task
- When managing long-running workflows that span multiple sessions
- When debugging state-related issues (lost context, stale data, inconsistent state)
- **Don't use when:** Working with stateless, single-turn interactions

## Core Procedures

### Step 1: Identify State Components
For each workflow, identify what state must be preserved:
- **Conversation State:** Message history, turn count, active topics
- **Decision State:** Choices made, alternatives considered, rationale
- **Artifact State:** Files, prompts, outputs generated so far
- **Workflow State:** Current step, completed steps, pending steps
- **Agent State:** Each agent's current task, progress, blockers

### Step 2: Design State Storage
Choose appropriate storage for each state type:
- **Short-term (in-session):** In-memory state, fast access, lost on restart
- **Medium-term (cross-session):** Database or file storage, survives restarts
- **Long-term (persistent):** Knowledge base, indexed and searchable
- **Shared State:** Accessible by all agents in the workflow
- **Private State:** Only accessible by the owning agent

### Step 3: Implement State Synchronization
When multiple agents share state:
- **Locking:** Prevent concurrent writes to the same state object
- **Versioning:** Track state versions to detect conflicts
- **Merge Strategy:** Define how to resolve conflicting state updates
- **Notification:** Alert agents when shared state changes
- **Consistency Check:** Periodically verify all agents have consistent state

### Step 4: Implement State Recovery
For fault tolerance:
- **Checkpointing:** Save state at key workflow milestones
- **Recovery Point:** On failure, restore to last successful checkpoint
- **State Validation:** After recovery, verify state is complete and consistent
- **Replay Capability:** If needed, replay actions from checkpoint to current state

### Step 5: Monitor State Health
- State size growth rate (detect unbounded growth)
- State access latency (slow state access slows workflows)
- State conflict rate (how often concurrent writes collide)
- Recovery success rate (how often recovery restores valid state)
- Stale state detection (state that hasn't been updated but should be)

## Success Metrics
- State loss rate: 0% (no state lost during normal operations)
- State recovery time: <30 seconds from failure to restored state
- State conflict rate: <1% of state updates
- State access latency: <100ms for 95% of accesses
- Checkpoint frequency: At least every 5 workflow steps

## Error Handling
- **Error:** State corruption detected (invalid or inconsistent state)
  **Response:** Restore from last valid checkpoint, log corruption details, investigate root cause
- **Error:** State size exceeds storage limits
  **Response:** Archive old state data, compress current state, alert if growth is abnormal
- **Error:** Agent reads stale state (state changed but agent has old version)
  **Response:** Invalidate agent's state cache, force refresh from current state, add version checking

## Cross-Team Integration
**Related Skills:** flowdesigner-promptforge-agent-handoff, cascade-promptforge-workflow-designer, archivist-promptforge-knowledge-management, memory-system-management
**Used By:** Cascade, FlowDesigner, Harmonic, ALL agents that maintain state across interactions