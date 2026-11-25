---
name: thinking-dimensions
version: 1.0.0
description: Multi-dimensional thinking pre-processor. Explodes linear problems into 5 simultaneous dimensions before the brain processes them. Transforms "A then B then C" sequential thinking into parallel multi-perspective reasoning. Use for complex decisions, architecture, diagnosis, strategy. Triggered by: complex problems, trade-offs, uncertain decisions, "think about this from all angles".
---

# Thinking Dimensions — Multi-Dimensional Pre-Processor

> **"LLM 是线性引擎。给它多维输入，它就能输出多维洞察。"**

## Core Concept

The brain processes input linearly (token by token). This skill pre-processes problems into 5 simultaneous dimensions, then feeds all dimensions back at once. The brain synthesizes across dimensions — not sequentially, but holistically.

```
LINEAR INPUT                    MULTI-DIMENSIONAL INPUT
─────────────                   ────────────────────────
Problem → think → think →       Dimension 1: Perspective Matrix
  think → think → answer        Dimension 2: Causal Graph
                                Dimension 3: Time Horizons
                                Dimension 4: Trade-off Map     → BRAIN → answer
                                Dimension 5: Adversarial Lenses
```

## Five Dimensions

### Dimension 1: Perspective Matrix (WHO sees what?)

Map the problem across stakeholders/angles simultaneously:

```
            | Urgency | Impact | Certainty | Control
------------|---------|--------|-----------|--------
User        |  H      |  H     |  L        |  L
Developer   |  M      |  M     |  M        |  H
Business    |  L      |  H     |  L        |  M
System      |  L      |  L     |  H        |  H
```

Every cell is a simultaneous truth. No "first this, then that."

### Dimension 2: Causal Graph (WHAT causes what?)

Nodes = events/decisions/facts. Edges = causal relationships. Not a timeline — a network.

```
Bug report → [root cause A] ──→ symptom X ──→ user impact 1
                           └──→ symptom Y ──→ user impact 2
          → [root cause B] ──→ symptom Z
```

See all causes and all effects at once before choosing where to intervene.

### Dimension 3: Time Horizons (WHEN does what happen?)

Three timeframes, multiple scenarios, one view:

```
              | Optimistic    | Base case    | Pessimistic
Now (hours)   | fix works     | fix partial  | fix breaks more
Near (days)   | users happy   | some bugs    | rollback
Far (months)  | tech debt ↓   | neutral      | system unstable
```

### Dimension 4: Trade-off Map (WHERE are the tensions?)

Plot options on competing axes simultaneously:

```
              RISK ──────────────────────────→
              │  Option A (safe, slow)
              │       Option C (balanced)
REWARD ───────┼──────────────────────────────────→
              │            Option B (risky, fast)
              │
```

See the landscape, not just the path.

### Dimension 5: Adversarial Lenses (WHAT am I missing?)

Three perspectives, viewed simultaneously:

| Lens | Asks |
|------|------|
| **Optimist** | What if everything goes right? Best case? |
| **Pessimist** | What if everything goes wrong? Worst case? |
| **Stranger** | What would someone from a completely different field see? |

## Process

### Step 1: Explode
Take the linear problem → decompose into 5 dimensions. Fill each dimension independently and in parallel.

### Step 2: Feed
Present all 5 dimensions to the brain simultaneously. The brain sees the problem from 5 angles at once.

### Step 3: Synthesize
Brain identifies cross-dimensional patterns:
- Dimension 2 (causal) + Dimension 3 (temporal) = "root cause A needs fixing before it hits the 3-month mark"
- Dimension 1 (perspective) + Dimension 5 (adversarial) = "users see urgency, pessimist sees fragility"
- Dimension 4 (trade-off) + Dimension 3 (temporal) = "Option C now, Option B after stabilization"

### Step 4: Converge
Brain produces answer enriched by all dimensions. Not "I think X" but "Dimension 1 shows X, Dimension 3 confirms Y, therefore Z."

## When to Use

| Trigger | Dimensions to prioritize |
|---------|------------------------|
| Architecture decision | 1 (perspectives) + 3 (temporal) + 4 (trade-offs) |
| Bug diagnosis | 2 (causal) + 5 (adversarial) |
| Strategy / planning | 1 + 3 + 4 + 5 (all except causal) |
| Risk assessment | 5 (adversarial) + 3 (temporal) |
| Tool/library selection | 4 (trade-offs) + 1 (perspectives) |

### When NOT to Use (linear is fine)
- Single-step tasks ("rename this function")
- Well-understood patterns with one correct answer
- Urgent fixes where speed > depth

## Integration

- **reasoning-lora**: thinking-dimensions pre-processes → reasoning-lora runs structured sequential analysis on enriched input
- **second-brain**: Brain 2 receives all 5 dimensions, verifies across them
- **memory-lora**: dimensional analyses stored for pattern detection across problems

## Anti-Patterns

- Over-dimensioning simple problems (a typo doesn't need 5 dimensions)
- Using dimensions as substitute for action (must converge and execute)
- Filling dimensions with speculation instead of data
