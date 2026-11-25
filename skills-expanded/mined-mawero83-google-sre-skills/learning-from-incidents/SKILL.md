---
name: learning-from-incidents
description: >-
  Run blameless postmortems and learning systems: action items that fix systems not people, CAST/systems thinking awareness, and follow-through. Use after incidents and when improving learning culture.
---

# Learning From Incidents

**Domain:** `operations`  
**Sources:** SRE Book 1e Ch15 + App D, Workbook Ch10, SRE Book 2e Ch11–12

## When to use

- Writing a postmortem/RCA
- Action items never finish
- Culture is blame-heavy

## Principles

- Blameless: improve systems, incentives, and defenses.
- Meeting threshold examples: large budget burn, Sev, novel failure.
- Action items need owners, priority, and due dates — track to close.
- Consider systems-theoretic views (STPA/CAST) for complex socio-technical failures (2e).

## Workflow

1. Collect timeline with evidence (UTC).
2. Impact: users, duration, budget burn, data.
3. Root causes + contributing factors (5 Whys + system factors).
4. What went well / poorly / luckily.
5. Action items: prevent, detect, mitigate faster — prefer P0 structural fixes.
6. Publish; track; review overdue monthly.

## Decision guide

- If only 'be more careful' actions → reject; demand system change.

## Output template

```markdown
# Postmortem skeleton
- Summary:
- Impact:
- Timeline:
- Root causes / factors:
- Lessons:
- Action items (owner, P, due):
```

## Anti-patterns

- Blame language.
- Orphan action items.
- Skipping writing when busy.

## Related skills

`incident-management`, `safety-engineering-stpa-cast`, `error-budget-policy`

## Canonical references

- [Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)
- [Workbook Postmortems](https://sre.google/workbook/postmortem-culture/)
- [Example Postmortem](https://sre.google/sre-book/example-postmortem/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
