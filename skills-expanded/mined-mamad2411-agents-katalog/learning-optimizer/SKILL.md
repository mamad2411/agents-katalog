---
name: learning-optimizer
description: >-
  Guides continuous learning concepts for EPCI workflows.
  Auto-invoke when discussing estimation accuracy, calibration, suggestion scoring,
  or learning preferences. Do NOT load for basic EPCI usage without learning context.
---

# EPCI Learning Optimizer Skill

## Overview

This skill provides guidance on EPCI's continuous learning system (F08), which:
- Calibrates time estimations using Exponential Moving Average (EMA)
- Tracks suggestion acceptance/rejection for scoring
- Detects recurring patterns for proactive suggestions

## Core Concepts

### Learning Loop

```
Measure → Analyze → Adapt → Improve
   │         │         │         │
   │         │         │         └── Next estimation more accurate
   │         │         └── Adjust calibration factors
   │         └── Identify patterns, calculate scores
   └── Collect actual vs estimated times
```

### Calibration

Calibration adjusts time estimates based on historical accuracy.

**Formula (EMA):**
```
new_factor = alpha * (actual/estimated) + (1 - alpha) * old_factor
```

Where:
- `alpha = 0.3` (default) — weight of new data
- `actual/estimated` — ratio from latest feature
- `old_factor` — previous calibration factor

**Interpretation:**
| Factor | Meaning |
|--------|---------|
| 1.0 | Estimates are accurate |
| > 1.0 | Under-estimating (actual > estimated) |
| < 1.0 | Over-estimating (actual < estimated) |

**Confidence:**
Increases logarithmically with sample count. Full confidence (1.0) at 5+ samples.

### Suggestion Scoring

Suggestions are scored to prioritize the most relevant ones.

**Formula:**
```
score = acceptance_rate * recency_factor * relevance_factor
```

**Factors:**
- `acceptance_rate`: Historical accept/reject ratio (0-1)
- `recency_factor`: Exponential decay based on days since last seen
- `relevance_factor`: Context match (domain, file types, preferences)

**Thresholds:**
| Score | Action |
|-------|--------|
| >= 0.3 | Show suggestion |
| < 0.3 | Hide suggestion |
| disabled | Never show |

### Pattern Detection

Patterns are detected from corrections during code review.

**Auto-suggest threshold:** 3+ occurrences

**Categories:**
- `security`: Input validation, injection, auth
- `performance`: N+1 queries, caching, indexing
- `quality`: Code duplication, complexity, naming
- `test`: Coverage gaps, missing assertions

## Data Storage

All learning data is stored in `.project-memory/learning/`:

| File | Content |
|------|---------|
| `calibration.json` | Factors by complexity, history, global stats |
| `preferences.json` | Suggestion feedback, disabled/preferred patterns |
| `corrections.json` | Correction history, recurring patterns |

## Commands

| Command | Purpose |
|---------|---------|
| `/epci-learn status` | View learning state |
| `/epci-learn reset` | Clear learning data |
| `/epci-learn export` | Export for analysis |
| `/epci-learn calibrate` | Force recalibration |

## Integration Points

### Phase 3 Finalization

After feature completion, EPCI automatically:
1. Saves feature history with times
2. Triggers calibration update
3. Updates velocity metrics

### Breakpoints

Calibrated estimates are shown in breakpoint metrics:
- Original estimate
- Calibrated estimate (with factor)
- Confidence level

### Suggestions

Suggestion scores affect display order and filtering:
- Higher scores appear first
- Below threshold scores are hidden
- Disabled patterns never appear

## Best Practices

### For Accurate Calibration

1. **Record times consistently** — Always set estimated/actual times
2. **Use appropriate complexity** — TINY/SMALL/STANDARD/LARGE
3. **Collect enough samples** — 5+ per complexity for confidence
4. **Review periodically** — Check `/epci-learn status`

### For Better Suggestions

1. **Provide feedback** — Accept/reject suggestions
2. **Disable noise** — Use "never suggest" for irrelevant patterns
3. **Mark preferences** — Boost patterns you find valuable
4. **Review corrections** — Ensure pattern_id is consistent

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Inaccurate estimates | Collect more samples, check time format |
| Irrelevant suggestions | Disable pattern, adjust threshold |
| Missing suggestions | Check if disabled, lower threshold |
| Corrupted data | Use `/epci-learn reset` |

## Privacy

Learning collects only:
- Time metrics (not code)
- Pattern identifiers (not content)
- User actions (accept/reject)

All data is local and exportable.
