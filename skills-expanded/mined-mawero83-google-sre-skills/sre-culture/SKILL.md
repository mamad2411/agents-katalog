---
name: sre-culture
description: >-
  Build generative reliability culture: psychological safety, learning, Westrum typology, and DORA-aligned practices from SRE Book 2e. Use when culture blocks SRE adoption or blameless learning.
---

# SRE Culture

**Domain:** `organization`  
**Sources:** SRE Book 2e Ch4, Workbook Ch10/21

## When to use

- Blame culture after outages
- SRE transformation stalled
- Leadership asks how to 'install SRE culture'

## Principles

- Culture enables or kills SRE practices.
- Generative cultures learn from failure; pathological cultures hide it.
- Error budgets and blameless postmortems are cultural mechanisms, not paperwork.
- Training and confidence benchmarks sustain culture.

## Workflow

1. Assess current culture signals (postmortem honesty, freeze politics, hero worship).
2. Install one ritual well (blameless PM or error budget meeting).
3. Align incentives: do not punish reported near-misses.
4. Show leaders trend data linking learning → fewer repeats.

## Decision guide

- If execs demand names for blame → escalate as transformation risk.

## Output template

```markdown
# Culture intervention
- Current signals:
- Ritual to install:
- Incentive changes:
- Success measure:
```

## Anti-patterns

- Postmortems as prosecution.
- Hero culture as staffing plan.

## Related skills

`learning-from-incidents`, `organizational-change`, `error-budget-policy`

## Canonical references

- [SRE Book 2e](https://sre.google/books/)
- [Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
