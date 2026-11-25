---
name: brain-consolidate
version: 1.0.0
description: Sleep-phase memory consolidation. Reviews recent tasks, strengthens important patterns, weakens noise, integrates learnings across domains. The brain's REM sleep. Triggers: session end, idle periods, brain-heartbeat signal.
---

# Brain Consolidate — Memory Consolidation (REM Sleep)

> **"不整理 = 噪音。整理了 = 智慧。"**

## Consolidation Cycle

### Phase 1: Review
Scan last N tasks: what worked? what failed? which chains used?

### Phase 2: Strengthen
Successful outcomes → boost connectome weights, boost memory scores, promote KB entries Verified

### Phase 3: Weaken
Failed outcomes → slightly weaken weights, reduce misleading memory scores

### Phase 4: Integrate
Cross-domain discovery: error from domain A matching pattern from domain B? Lesson from project X useful in project Y? → promote to global scope

### Phase 5: Clean
Prune dead connections (weight < 0.1, never fired). Archive memories (score < -0.5). Deprecate stale KB entries (unverified 90+ days).

## Output
```
=== Consolidation ===
Reviewed: N tasks | Strengthened: X conns, Y memories | Pruned: Z dead
Discoveries: A cross-domain patterns | Next: [suggested action]
```

## Integration
- **brain-heartbeat**: Triggers consolidation at session end
- **neural-orchestrator**: Adjusts connectome weights
- **memory-lora**: Updates scores, runs distillation
