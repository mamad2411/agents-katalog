---
name: software-engineering-in-sre
description: >-
  Balance software engineering and operations in SRE: project selection, production excellence software, and avoiding pure ticket hell — from Google SRE. Use when planning SRE roadmaps and engineering allocation.
---

# Software Engineering In SRE

**Domain:** `delivery`  
**Sources:** SRE Book 1e Ch18, SRE Book 2e Ch13

## When to use

- SRE roadmap / OKRs
- Defending eng time vs interrupt load
- Choosing platform bets

## Principles

- SRE is software engineering applied to ops problems.
- Track interrupt load; protect project time deliberately.
- Prefer internal platforms that remove whole classes of toil.
- Measure outcomes (toil↓, burn↓, MTTR↓), not LOC.

## Workflow

1. Measure time split: interrupts / toil / eng projects.
2. Pick 1–3 projects that cut the largest toil or risk classes.
3. Define success metrics and stakeholders.
4. Ship iteratively; reassess quarterly with error-budget themes.

## Decision guide

- If interrupts > ~50% sustained → overload recovery before new projects.

## Output template

```markdown
# SRE engineering plan
- Time split:
- Candidate projects:
- Chosen bets + metrics:
- Capacity reserved:
```

## Anti-patterns

- SRE as ticket dump.
- Endless rewrites with no ops payoff.

## Related skills

`eliminating-toil`, `automation-tooling`, `operational-overload`

## Canonical references

- [Software Engineering in SRE](https://sre.google/sre-book/software-engineering-in-sre/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
