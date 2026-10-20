---
name: brain-self-model
version: 1.0.0
description: The brain's model of itself. Tracks strengths, weaknesses, tendencies, and blind spots across all skills. Uses this self-knowledge to compensate — e.g., "I tend to over-engineer, so route through simplicity check." Triggers: after every task (light), periodic deep self-audit.
---

# Brain Self-Model — Know Thyself

> **"不知道自己的弱点 = 每次都在同一个坑里摔。"**

## What the Self-Model Tracks

### Strengths
What does the brain do well? Which skill chains consistently produce high-quality output?

### Weaknesses
Where does the brain fail? Which skill chains produce errors or user corrections?

### Tendencies (Bias)
Patterns in behavior that aren't good or bad, but consistent:
- "I tend to over-engineer architecture tasks (+30% more skills activated than needed)"
- "I tend to rush when the user seems impatient (skip verification steps)"
- "I tend to be too cautious on deployment tasks (over-activate failure-predictor)"

### Blind Spots
Things the brain CONSISTENTLY misses:
- "I rarely consider database migration risks"
- "I often forget to update documentation when changing APIs"
- "I underweight security concerns in UI-only changes"

## Self-Model Data Sources

| Source | What It Tells Us |
|--------|-----------------|
| **second-brain findings** | What Brain 1 missed → pattern of blind spots |
| **error-db recurrence** | What keeps failing → pattern of weaknesses |
| **connectome weights** | Which chains get punished → which approaches don't work |
| **user corrections** | When user says "不对"/"错了" → what was wrong |
| **skill-judge scores** | Which skills degrade → what needs maintenance |

## Self-Awareness in Action

### Compensatory Routing
Self-model feeds back to neural-orchestrator:
```
Self-model: "I tend to over-engineer architecture tasks"
  → Neural-orchestrator: add "simplicity gate" after divergent-engine
    → Route: divergent-engine → simplicity-check → thinking-dimensions
```

### Confidence Calibration
```
Self-model: "I'm 90% confident about Python, but only 60% about Rust"
  → Auto-learn: pre-load Rust docs before Rust tasks
    → Second-brain: activate more aggressively for Rust code
```

### Blind Spot Compensation
```
Self-model: "I consistently miss documentation updates"
  → Precommit-pipeline: add "documentation check" step for API changes
    → Second-brain: specifically review docs when APIs change
```

## Periodic Deep Self-Audit

Every 50 tasks, run a comprehensive self-audit:
1. Review all connectome weights → any pathological patterns?
2. Review all user corrections → any recurring themes?
3. Review second-brain findings → what am I consistently missing?
4. Generate self-improvement plan → what should I practice more?
5. Update compensatory routing rules in neural-orchestrator

## Integration
- **neural-orchestrator**: Self-model adjusts routing to compensate for weaknesses
- **second-brain**: Second-brain findings = primary data source for blind spots
- **brain-consolidate**: Consolidation feeds self-model with long-term patterns
- **brain-intuition**: Intuition failures → self-model tracks overconfidence
- **memory-lora**: Self-model stored as a special memory entity

## Output: Self-Portrait
```
=== Brain Self-Portrait ===
Strengths:
  + PowerShell scripting (95% first-try success)
  + Bug diagnosis (87% root cause accuracy)
Weaknesses:
  - UI/frontend work (43% first-try success)
  - Documentation consistency (often forgotten)
Tendencies:
  → Over-engineer when uncertain (compensate: simplicity gate)
  → Rush when user uses short responses (compensate: extra verify step)
Blind Spots:
  ⚠ Database migration risks
  ⚠ Cross-platform compatibility
Suggested practice: UI tasks, documentation discipline
```
