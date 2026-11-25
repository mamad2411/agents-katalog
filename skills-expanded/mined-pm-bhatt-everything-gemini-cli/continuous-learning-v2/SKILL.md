---
name: continuous-learning-v2
description: Instinct-based learning system that observes sessions, creates atomic instincts with confidence scoring, and evolves them into skills/commands.
---

# Continuous Learning v2

An advanced learning system based on atomic "instincts" with confidence scoring that evolve into skills and commands over time.

## Philosophy

v2 improves on the original continuous learning with:
- **Atomic instincts** instead of full skills
- **Confidence scoring** (0.3-0.9 weighted)
- **Observation hooks** for reliable pattern detection
- **Evolution path** from instincts to skills/commands

## Key Concepts

### Instincts
Small, atomic learned behaviors with confidence scores:

```json
{
  "id": "inst_abc123",
  "trigger": "typescript type error with 'any'",
  "behavior": "Suggest explicit typing instead of 'any' type",
  "confidence": 0.7,
  "domain": "code-style",
  "occurrences": 15,
  "last_used": "2025-01-15"
}
```

### Confidence Scoring

- **0.3-0.4**: New instinct, few observations
- **0.5-0.6**: Moderate confidence, useful pattern
- **0.7-0.8**: High confidence, consistently helpful
- **0.9**: Ready for promotion to skill/command

Confidence increases with:
- Successful application
- User positive feedback
- Repeated occurrence

Confidence decreases with:
- User corrections
- Contradicting observations
- Disuse over time (decay)

### Domain Tags

Instincts are tagged by domain:
- `code-style` - Formatting, naming, structure
- `testing` - Test patterns, coverage
- `git` - Version control workflows
- `debugging` - Error resolution
- `performance` - Optimization patterns
- `security` - Security practices

### Evolution Path

```
Observation → Instinct → Cluster → Skill/Command

1. Observe: Hook captures pattern
2. Create: New instinct with low confidence
3. Reinforce: Confidence increases with use
4. Cluster: Related instincts group together
5. Promote: High-confidence clusters become skills/commands
```

## Workflow

### Creating Instincts

When a useful pattern is observed:
1. Check if similar instinct exists
2. If yes: increase confidence and update
3. If no: create new instinct with 0.4 confidence

### Using Instincts

When working on a task:
1. Match active instincts to current context
2. Apply high-confidence instincts (>0.6)
3. Track success/failure of application

### Promoting to Skills

When instinct cluster reaches threshold:
1. Group related instincts
2. Generate skill definition
3. Request user approval
4. Save as skill file

## Best Practices

1. **Start conservative** - Low initial confidence prevents false positives
2. **Let confidence build** - Don't force promotion
3. **Review periodically** - Prune low-confidence instincts
4. **Domain separation** - Keep instincts focused
5. **Export/share** - High-confidence instincts benefit teams
