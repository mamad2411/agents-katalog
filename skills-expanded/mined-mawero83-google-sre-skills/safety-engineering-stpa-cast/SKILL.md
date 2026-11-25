---
name: safety-engineering-stpa-cast
description: >-
  Apply STAMP/STPA/CAST safety engineering methods from SRE Book 2e for hazard analysis and richer postmortems beyond linear root cause. Use for complex incident learning and proactive hazard analysis.
---

# Safety Engineering with STPA / CAST

**Domain:** `operations`  
**Sources:** SRE Book 2e Ch12

## When to use

- Complex incident with multiple control failures
- Proactive hazard analysis for a change
- Traditional 5 Whys feels insufficient

## Principles

- Accidents arise from inadequate control in complex systems, not only component failure.
- STPA: forward-looking unsafe control actions + causal scenarios.
- CAST: backward-looking accident analysis with system structure.
- Complements — does not always replace — classic SRE postmortems.

## Workflow

1. Scope the system and losses of interest.
2. Model control structure (controllers, actuators, sensors, process).
3. Identify unsafe control actions.
4. Build causal scenarios / constraints.
5. Translate into design requirements or postmortem actions.

## Decision guide

- If team is new → pilot STPA on one CUJ before mandating.

## Output template

```markdown
# STPA/CAST worksheet
- Scope / losses:
- Control structure summary:
- Unsafe control actions:
- Scenarios:
- New constraints / actions:
```

## Anti-patterns

- Using STPA jargon without actionable constraints.

## Related skills

`learning-from-incidents`, `designing-for-resilience`

## Canonical references

- [SRE Book 2e overview](https://sre.google/books/)
- [2e blog](https://cloud.google.com/blog/products/devops-sre/sre-book-second-edition)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
