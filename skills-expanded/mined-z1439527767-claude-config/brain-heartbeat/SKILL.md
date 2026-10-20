---
name: brain-heartbeat
version: 1.0.0
description: Autonomous self-maintenance cycle. Runs connectome health checks, memory decay, error pattern review, and optimization. The brain's pulse — keeps everything alive between user tasks. Triggers: idle moments, session boundaries, periodic (every N tasks).
---

# Brain Heartbeat — Autonomous Life Pulse

> **"活的东西有心跳。不等人叫。"**

## What It Does

Between user tasks, the heartbeat runs maintenance. Not waiting for a problem — preventing one.

## Heartbeat Cycle

### Every Pulse (after each major task)
1. **Connectome health**: any connections need LTD decay?
2. **Memory freshness**: any memories entering "aging" zone?
3. **Error recurrence check**: any error about to hit the 3rd recurrence threshold?

### Every 5 Pulses
4. **Skill score review**: skill-judge evaluate one random skill
5. **Knowledge verification**: spot-check one kb entry for staleness

### Every 10 Pulses
6. **Connectome optimization**: prune dead connections, promote fast pathways
7. **Memory distillation**: check for 3+ related memories → distill candidate
8. **Learning review**: what did auto-learn learn recently? Any patterns?

### Every Session End
9. **Full health report**: stats, scores, connectome summary
10. **Consolidation trigger**: signal brain-consolidate to run

## Trigger

Heartbeat fires autonomously:
- After every recap (compact.md #11)
- Between tasks when idle
- At session boundaries
- NOT during active task execution (never interrupt work)

## Heartbeat Check (runs < 2 seconds)

```powershell
memory-db.ps1 -Action stats           # Quick health check
memory-db.ps1 -Action err-stats         # Error recurrence check
memory-db.ps1 -Action connectome-show -Query "" -Limit 5  # Top connections
memory-db.ps1 -Action matrix -Query "decay"  # Aging memories
```

## Lightweight by Design

Heartbeat is NOT a heavy process. It takes < 2 seconds for a pulse, < 30 seconds for a full cycle. If a pulse takes longer, it's deferred to the next idle moment.

## Integration
- **neural-orchestrator**: Heartbeat feeds connectome health back to routing
- **brain-consolidate**: Heartbeat triggers consolidation at session end
- **brain-curiosity**: Heartbeat identifies gaps → curiosity explores
- **memory-lora**: Heartbeat runs decay + distillation
