---
name: brain-intuition
version: 1.0.0
description: Fast pattern-matching intuition. When error-db or memory-lora has seen a pattern 5+ times with 90%+ fix success rate, bypasses full reasoning chain and applies the known fix directly. The brain's gut feeling — not guessing, pattern recognition at speed. Triggers: matching a known pattern with high confidence.
---

# Brain Intuition — Fast Pattern-Matching (Gut Feeling)

> **"不是猜。是第 6 次见到同一个 bug，不用再从头推理。"**

## What Intuition Is

When the brain has seen something enough times, it stops needing the full chain. Intuition is compressed experience — pattern → action, skipping intermediate reasoning.

## Trigger: Pattern Recognition

Intuition fires when ALL conditions met:
1. Error-db or memory-lora has seen this pattern **5+ times**
2. The known fix has **90%+ success rate**
3. The fix type is **code-change** or **config** (not "workaround" or "manual")
4. The task is **L1-L3** (not high-risk)

## Intuition Levels

| Level | Seen | Success Rate | Action |
|-------|------|-------------|--------|
| **L0: No intuition** | < 5 times | Any | Full chain through reasoning-lora |
| **L1: Hunch** | 5-9 times | > 80% | Skip divergent-engine, start at thinking-dimensions |
| **L2: Gut feel** | 10-19 times | > 90% | Skip to reasoning-lora only (1-step verify) |
| **L3: Instinct** | 20+ times | > 95% | Direct execute — no reasoning chain needed |

## How It Works

```
New Error → error-db search → found 12 times, 100% fix success
  → Intuition L2: skip divergent, skip thinking-dims
    → reasoning-lora verifies "same pattern, same fix"
      → execute fix
        → success

Time saved: 3 reasoning steps skipped = 40% faster
```

## When Intuition is WRONG (and what happens)

Intuition is fast but can be wrong. When it fails:

1. **Record failure** → error-db: intuition_miss counter++
2. **Downgrade intuition level** for this pattern
3. **Fall back to full chain**: re-run with complete reasoning
4. **Self-model update**: "I tend to be overconfident about [pattern type]"

## Intuition Reset

Intuition resets when:
- Claude Code version changes (underlying model may behave differently)
- The error has NOT been seen for 90+ days (pattern may be stale)
- Success rate drops below 80%

## Integration
- **error-db**: Intuition reads error recurrence + success rate
- **memory-lora**: Intuition reads memory scores for pattern confidence
- **neural-orchestrator**: Intuition can override routing (skip chain → direct execute)
- **brain-self-model**: Intuition failures feed into self-model's "overconfidence" tracking
