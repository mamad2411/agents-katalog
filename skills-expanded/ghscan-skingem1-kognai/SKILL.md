---
name: godman-lax
description: "Use LAX to enforce latency budgets, route agent calls by SLA tier, and probe execution timing. LAX prevents timeout cascades in multi-agent pipelines."
tags: ["latency", "sla", "routing", "performance", "godman-protocols"]
version: "0.2.0"
---

# LAX — Latency-Aware Execution

Use this skill when you need to enforce time budgets on agent calls, route to faster models under pressure, or detect SLA violations before they cascade.

## Key Operations

```typescript
import { createLatencyBudget, allocateSlot, createSLAContract, probeLatency, selectRoute } from '@godman-protocols/lax';

// Create a budget for a pipeline step
const budget = createLatencyBudget({ total_ms: 5000, warning_threshold_ms: 3000 });

// Route by SLA tier
const route = selectRoute(budget, availableAgents); // picks fastest within budget

// Probe and record
const probe = probeLatency(agentId, startMs, endMs);
const sla = createSLAContract({ p95_ms: 2000, p99_ms: 4000 });
```

## When to Use
- Multi-step pipelines where one slow agent blocks all downstream
- Choosing between local model (fast) vs cloud model (smart) based on remaining budget
- Detecting which agent caused a timeout in a swarm run

## Notes
- Integrate with SIGNAL to broadcast SLA violation events
- Combine with DRS to preempt slow resource allocations
