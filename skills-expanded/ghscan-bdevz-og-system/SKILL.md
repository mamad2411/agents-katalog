# Routing Skill -- Message Router

## Purpose

Route messages between agents (Jay, Z, Rick, Leroy) based on the dependency graph and business rules. All inter-agent communication flows through EM. EM is the message broker that ensures dependencies are respected, safety gates are enforced, and messages don't get lost or arrive out of order.

## Core logic

Every message that arrives at EM gets a routing decision:

1. **Route immediately:** Message prerequisites are met, target agent is healthy, message is safe to deliver.
2. **Hold pending input:** Message prerequisites not yet met (e.g., Z data not ready for Jay submission). Hold and retry when prerequisites available.
3. **Escalate to human:** Message involves safety-critical decision (blocking submission due to duplicate, profile ban) or high-uncertainty situation. Present to human for approval.
4. **Drop silently:** Message is duplicate or superseded (e.g., two status checks from same agent in same minute). Log and discard.

## Routing rules

All routing rules are configured in `routing_rules.json`. EM reads this file and applies rules to every incoming message.

Key rules:

- **URGENT priority:** Inbound leads, critical alerts, agent failures → route immediately
- **Z safety gate:** If Z is DEAD/ERROR, PAUSE all submissions (no data validation possible)
- **Dependency enforcement:** Rick doesn't get submission requests until Jay submitted AND Z approved
- **Deadline tracking:** Messages miss SLA → escalate to human
- **Queue management:** If target agent queue is too deep, batch and hold new messages

## Input/Output

**Input:** Message envelope
```json
{
  "from": "Jay",
  "to": "Z",
  "type": "REQUEST",
  "priority": "NORMAL",
  "timestamp": "2025-02-15T09:00:00Z",
  "reference": "SUBM-C042-001",
  "payload": {
    "consultant_id": "C-042",
    "job_posting_id": "LI-9876",
    "vendor": "TrueBlue",
    "end_client": "Microsoft",
    "confidence_score": 8.2
  },
  "context": "Jay completed research, confidence >6.5, no staleness risk"
}
```

**Output:** Routing decision
```json
{
  "message_id": "MSG-001",
  "original_from": "Jay",
  "original_to": "Z",
  "routing_decision": "ROUTE_IMMEDIATELY",
  "target": "Z",
  "reason": "Z has fresh data (2 hours old), no dependency violations, priority is NORMAL",
  "timestamp": "2025-02-15T09:00:15Z",
  "sla": "Expected Z response within 15 minutes",
  "logged": true,
  "posted_to_channel": "#agent-feed"
}
```

## Usage

```python
from message_router import route_message

# Route a single message
envelope = {
    "from": "Jay",
    "to": "Z",
    "type": "REQUEST",
    "priority": "NORMAL",
    "timestamp": datetime.now().isoformat(),
    "reference": "SUBM-C042-001",
    "payload": {...},
    "context": "..."
}

decision = route_message(envelope, system_state)
# decision = {
#   "routing_decision": "ROUTE_IMMEDIATELY",
#   "target": "Z",
#   "reason": "...",
#   ...
# }
```

## Implementation details

- **Rules engine:** Load `routing_rules.json`, evaluate against every message
- **State checks:** Before routing, check target agent state (ACTIVE/IDLE/BUSY/SLOW/ERROR/DEAD)
- **Dependency graph:** Maintain in-memory graph from `routing_rules.json`, validate prerequisites
- **Logging:** Every routing decision logged to agent-feed (JSON line)
- **Escalation:** If decision is ESCALATE_TO_HUMAN, post to #alerts with full context
- **SLA tracking:** Record expected response time, track if response late

## Error cases

| Error | Decision | Action |
|-------|----------|--------|
| Target agent DEAD | ESCALATE_TO_HUMAN | Alert human, attempt restart from backup |
| Z is DEAD (safety gate violation) | PAUSE_ALL_SUBMISSIONS | Block all submission requests until Z restored |
| Target agent queue >threshold | HOLD_PENDING_CAPACITY | Queue message locally, retry when queue drops |
| Message prerequisite not met | HOLD_PENDING_INPUT | Queue message locally, retry when prerequisite available |
| Message is duplicate | DROP_SILENTLY | Log duplicate, discard (idempotence) |

## Metrics tracked

- Messages routed per hour (should be ~100+)
- Routing decisions by type (IMMEDIATE, HOLD, ESCALATE, DROP)
- Average hold time (should be <30 min for NORMAL priority)
- Escalation count (should be <5/day)
- Message loss (should be zero)
