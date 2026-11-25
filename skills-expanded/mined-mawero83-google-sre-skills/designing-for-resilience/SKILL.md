---
name: designing-for-resilience
description: >-
  Design resilient products using Google SRE 2e principles: progressive rollout, defense in depth, failure domains, overload controls, data resilience, and emergency modes. Use for architecture reviews and reliability design decisions.
---

# Designing For Resilience

**Domain:** `resilience`  
**Sources:** SRE Book 2e Ch17, SRE Book 1e Ch21–22

## When to use

- Architecture / design review for reliability
- Planning failure domains or degrade modes
- Adding emergency mode / feature kill switches

## Principles

- Reliability emerges from change management, dependencies, overload control, and data resilience — not only redundancy.
- Progressive rollout + change supervision beat big-bang.
- Align failure domains; recover domains deliberately.
- Critical data needs independent fallbacks and tested restores.
- Practice incident modes for developers, responders, and leadership.

## Workflow

1. List CUJs and their hard dependencies.
2. For each dep: failure mode, detect, degrade, recover.
3. Define failure domains (zone/region/cell) and blast radius caps.
4. Specify overload shedding and client-side controls.
5. Require progressive delivery + abort criteria.
6. Document emergency mode behavior and drill it.

## Decision guide

- If no degrade path → treat as launch blocker for critical CUJs.
- If shared fate with a weak dep → add bulkhead or cache.

## Output template

```markdown
# Resilience design review
- CUJs:
- Failure domains:
- Dep failure matrix:
- Overload controls:
- Rollout / abort:
- Emergency mode:
- Gaps / blockers:
```

## Anti-patterns

- Hope-based HA.
- Single global control plane without break-glass.

## Related skills

`cascading-failures`, `handling-overload`, `canarying-releases`, `nalsd-system-design`

## Canonical references

- [SRE Book 2e](https://sre.google/books/)
- [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
