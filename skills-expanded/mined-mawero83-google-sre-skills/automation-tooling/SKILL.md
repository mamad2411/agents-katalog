---
name: automation-tooling
description: >-
  Decide what to automate and how: levels of automation, incremental approach, pitfalls, and human factors from Google SRE. Use when building ops automation, Autopilot-style systems, or AI ops agents.
---

# Automation Tooling

**Domain:** `delivery`  
**Sources:** SRE Book 1e Ch7, SRE Book 2e Ch13/21

## When to use

- Automation design reviews
- Autopilot / auto-remediation proposals
- AI agent autonomy debates

## Principles

- Automate to reduce toil and variance — not to remove understanding.
- Incremental automation with observability beats opaque mega-bots.
- Levels of autonomy require matching safety controls.
- UI, speed, and failure visibility are part of automation design.

## Workflow

1. State the toil/risk problem and success metric.
2. Choose automation level (suggest → act with confirm → act within guardrails).
3. Define guardrails, audit logs, and kill switch.
4. Ship shadow mode; compare to human actions.
5. Graduate autonomy only with evidence.

## Decision guide

- If blast radius high and confidence low → suggestion mode only.
- If AI-driven → require human authority for irreversible actions (see ai-supports-sre).

## Output template

```markdown
# Automation design
- Problem / metric:
- Autonomy level:
- Guardrails:
- Shadow results:
- Rollout plan:
```

## Anti-patterns

- Fully autonomous prod changes without audit.
- Automating rare unclear tasks first.

## Related skills

`eliminating-toil`, `ai-supports-sre`, `software-engineering-in-sre`

## Canonical references

- [Evolution of Automation](https://sre.google/sre-book/automation-at-google/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
