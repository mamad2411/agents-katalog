---
name: sre-hiring-training
description: >-
  Hire and train SREs using Google-inspired attributes, antipatterns, and career paths from SRE Book 2e and classic onboarding chapters. Use for hiring loops, ramp plans, and career frameworks.
---

# SRE Hiring Training

**Domain:** `organization`  
**Sources:** SRE Book 2e Ch5, SRE Book 1e Ch28

## When to use

- Building SRE hiring loop
- New hire ramp to on-call
- Career ladder design

## Principles

- Successful SREs combine systems thinking, coding, troubleshooting, and collaboration.
- Hiring antipatterns: pure ops clones, pure SWE with no prod curiosity, hero-only filters.
- Training is organized exposure to production with safety nets.
- IC career paths must reward reliability impact, not only features.

## Workflow

1. Define role attributes and interview signals.
2. Build ramp: architecture → shadow on-call → primary with backup.
3. Set milestones to on-call readiness.
4. Pair learning plan with real project ownership.

## Decision guide

- If candidate strong SWE but weak prod debug → train deliberately or hire elsewhere.

## Output template

```markdown
# Hiring/training plan
- Role attributes:
- Loop / signals:
- 30/60/90 ramp:
- On-call readiness gate:
```

## Anti-patterns

- Throwing new hires primary on-call week one.
- No engineering interview for 'SRE'.

## Related skills

`on-call-excellence`, `learning-path-sre`, `sre-foundations`

## Canonical references

- [Accelerating SREs to On-Call](https://sre.google/sre-book/accelerating-sre-on-call/)
- [SRE Book 2e](https://sre.google/books/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
