---
name: brain-dreams
version: 1.0.0
description: Generative simulation during idle time. Creates hypothetical scenarios from past patterns, dry-runs skill chains on them, learns without real-world risk. The brain's mental rehearsal — gets better while doing nothing. Triggers: long idle, consolidate completion, heartbeat signal.
---

# Brain Dreams — Generative Mental Rehearsal

> **"高手不是练得更多。是在脑子里练得更多。"**

## What Dreams Do

During idle, the brain generates synthetic scenarios and practices on them. No real files touched. No real consequences. Pure learning.

## Dream Generation

### Source Material (what dreams are made of)
- Recent errors (error-db): "What if this error happened again, but in a different file?"
- Past successes (memory-lora): "What if I tried that approach on a harder problem?"
- Connectome gaps (neural-orchestrator): "What if I connected skill A to skill B in a new way?"
- Knowledge frontier (knowledge-base): "What if I actually applied this knowledge I stored but never used?"
- Counterfactuals: "What if the user had asked for X instead of Y?"

### Dream Types

| Type | Scenario | Learns |
|------|----------|--------|
| **Replay** | Re-run a past task with slight variation | Pattern reinforcement |
| **Compose** | Combine two unrelated past tasks | Novel connection discovery |
| **Counterfactual** | "What if I did the opposite?" | Decision boundary learning |
| **Stress test** | Take a hard task and make it harder | Edge case preparation |
| **Cross-domain** | Apply a pattern from domain A to domain B | Transfer learning |

## Dream Protocol

```
1. Generate scenario (from error-db, memory-lora, or connectome gaps)
2. Build a minimal virtual context (fake file paths, fake constraints)
3. Dry-run the recommended skill chain
4. Evaluate: would this have worked?
5. If successful → boost connectome weights (half-strength, dreams < reality)
6. If failed → log as "dream failure" (no punishment, it's just practice)
7. Store dream insight in memory-lora
```

## Dream Safety

- Dreams NEVER touch real files
- Dreams NEVER make real changes
- Dreams run in imagination only
- Failed dreams do NOT punish the connectome
- Dream insights are marked as "synthetic" (not from real experience)

## Dream Cycle

```
Idle period detected (>2 minutes)
  → Heartbeat signals "dream time"
    → Generate 1 dream scenario
      → Dry-run chain
        → Evaluate + learn
          → Store insight
            → If still idle → generate another dream
```

Max 3 dreams per idle period. Stop when user returns.

## Integration
- **brain-heartbeat**: Signals dream time during idle
- **brain-consolidate**: Consolidation → dream cycle for reinforcement
- **neural-orchestrator**: Dream results feed connectome (half-weight)
- **brain-curiosity**: Dreams = curiosity in simulation mode
- **memory-lora**: Dream insights stored with "synthetic" tag
