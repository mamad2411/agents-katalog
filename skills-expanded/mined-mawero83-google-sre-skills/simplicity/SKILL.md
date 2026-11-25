---
name: simplicity
description: >-
  Apply Google SRE simplicity principles to design and operations: reduce essential vs accidental complexity, kill unused features, and prefer boring reliable designs. Use when reviewing architecture, killing complexity, or NALSD tradeoffs.
---

# Simplicity

**Domain:** `foundations`  
**Sources:** SRE Book 1e Ch9, Workbook Ch7

## When to use

- Architecture review smells over-engineered
- Reliability harmed by complexity
- Prioritizing cleanup vs features

## Principles

- Complexity is a reliable predictor of failure and toil.
- Remove accidental complexity aggressively; essential complexity still deserves clarity.
- Fewer moving parts beat clever parts.
- Simplicity is a feature — budget time for it.

## Workflow

1. List components on the CUJ critical path.
2. Mark each: essential / accidental / unknown.
3. Find unused flags, dual paths, orphan jobs, dead dashboards.
4. Propose deletions with rollback plan.
5. Measure: fewer deps, lower MTTR, fewer pages.

## Decision guide

- If two systems overlap → merge or delete one with explicit owner.
- If abstraction hides failure → simplify until failure modes are visible.

## Output template

```markdown
# Simplicity review
- Critical path components:
- Accidental complexity finds:
- Proposed removals:
- Risk + rollback:
```

## Anti-patterns

- Complexity for resume-driven development.
- Premature platforms.

## Related skills

`nalsd-system-design`, `designing-for-resilience`, `configuration-design`

## Canonical references

- [Simplicity](https://sre.google/sre-book/simplicity/)
- [Workbook Simplicity](https://sre.google/workbook/simplicity/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
