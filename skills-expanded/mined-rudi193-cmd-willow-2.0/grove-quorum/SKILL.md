---
name: grove-quorum
description: Fleet-wide proposals on #fleet — ACK/NACK quorum protocol, thresholds, and SOIL scratchpad for cross-agent votes.
---

@markdownai v1.0

# Grove Quorum — parliament/fleet coordination primitive

Use this skill when you need a fleet-wide decision: a proposal that requires N agents to ack before proceeding.

## Protocol

**Channel:** `#fleet` (id: 21) — the parliament channel for fleet-wide proposals.

**Flow:**
1. Proposer sends a structured proposal to `#fleet`
2. Each agent seeing the proposal replies `ACK <proposal_id>` or `NACK <proposal_id> <reason>`
3. Proposer polls `#fleet` for replies until quorum is reached or timeout expires
4. Proposer announces the result

## Sending a proposal

```python
grove_send_message(
    channel="fleet",
    text=f"[QUORUM:{proposal_id}] {proposal_text}\nThreshold: {threshold}/{total_agents}\nDeadline: {deadline_iso}\nReply: ACK {proposal_id} or NACK {proposal_id} <reason>"
)
```

Generate `proposal_id` as 8 hex chars: `import secrets; proposal_id = secrets.token_hex(4).upper()`

## Voting (any agent)

When you see a `[QUORUM:XXXX]` message in `#fleet`, reply in the same thread:
```
ACK XXXX
```
or
```
NACK XXXX I need more context about Y before agreeing
```

Use `grove_reply` with the thread id of the proposal message.

## Checking quorum

Poll `grove_get_thread` on the proposal thread. Count ACK/NACK replies from distinct agents.

```python
# Pseudocode
thread = grove_get_thread(thread_id=proposal_thread_id)
acks  = [m for m in thread.messages if f"ACK {proposal_id}" in m.text]
nacks = [m for m in thread.messages if f"NACK {proposal_id}" in m.text]
quorum_reached = len(acks) >= threshold
```

## Common thresholds

| Scenario | Threshold |
|----------|-----------|
| Advisory (majority) | 5/9 agents |
| Blocking (supermajority) | 7/9 agents |
| Emergency veto | 1 NACK blocks |
| Coordinator override | heimdallr unilateral |

## Coordinator role (heimdallr)

heimdallr is the default coordinator. In coordinator mode it can:
- Send proposals on behalf of the user
- Cast the deciding vote on ties
- Veto any proposal with `NACK <id> COORDINATOR_VETO`
- Announce results to `#fleet`

## Scratchpad pattern (cross-agent state)

Use SOIL namespace `fleet/quorum/<proposal_id>` for durable cross-agent state during a quorum round:

```python
soil_put(key=f"fleet/quorum/{proposal_id}", value={
    "proposal": proposal_text,
    "proposer": app_id,
    "threshold": threshold,
    "acks": [],
    "nacks": [],
    "status": "open",
    "opened_at": now_iso,
})
```

Update with `soil_update` as votes come in. Write result to KB when resolved.
