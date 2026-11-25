---
name: platform-engineering-sre
description: >-
  Apply platform engineering through an SRE lens: paved paths, guardrails, cognitive load, and shift-down — from SRE Book 2e. Use when building internal platforms and developer reliability paths.
---

# Platform Engineering SRE

**Domain:** `delivery`  
**Sources:** SRE Book 2e Ch18

## When to use

- Internal platform strategy
- Too many snowflake services
- Reducing cognitive load on app teams

## Principles

- Platforms are curated gardens with paths and guardrails, not infinite choice.
- Shift down undifferentiated reliability work into the platform.
- Measure adoption and outcomes, not only platform feature count.
- Exceptions exist but must be costly and visible.

## Workflow

1. Identify top repeated reliability burdens across teams.
2. Define golden path (deploy, observe, SLO, on-call basics).
3. Add guardrails (policy, defaults, lint).
4. Migrate 1–2 pilot services; measure time-to-reliable.
5. Publish scorecard of platform outcomes carefully (avoid vanity).

## Decision guide

- If teams bypass platform → fix UX/incentives before mandating.

## Output template

```markdown
# Platform reliability plan
- Burdens to absorb:
- Golden path:
- Guardrails:
- Pilot results:
- Next adoption wave:
```

## Anti-patterns

- Platform as ticket queue.
- Mandates without paved path.

## Related skills

`sre-engagement-model`, `automation-tooling`, `monitoring-observability`

## Canonical references

- [SRE Book 2e](https://sre.google/books/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
