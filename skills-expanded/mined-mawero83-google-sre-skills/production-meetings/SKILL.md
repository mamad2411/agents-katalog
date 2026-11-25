---
name: production-meetings
description: >-
  Run effective production meetings using Google SRE agendas: SLO health, incidents, risks, and actions. Use for weekly/biweekly prod reviews.
---

# Production Meetings

**Domain:** `organization`  
**Sources:** SRE Book 1e App F, SRE Book 1e Ch31

## When to use

- Starting a prod meeting
- Meeting has become status spam

## Principles

- Data first: budgets, burns, pages, launch risks.
- Decisions and owners required.
- Timebox; escalate blockers.

## Workflow

1. Prepare dashboards beforehand.
2. Review SLO/budget exceptions.
3. Review incidents and overdue actions.
4. Surface upcoming risky changes.
5. Record decisions; follow up next meeting.

## Decision guide

- If same risk repeats 3 meetings → convert to tracked project.

## Output template

```markdown
# Prod meeting notes
- SLO/budget:
- Incidents / actions:
- Risks:
- Decisions:
```

## Anti-patterns

- Reading tickets aloud without decisions.

## Related skills

`sre-communication`, `error-budget-policy`, `outage-tracking`

## Canonical references

- [Example Production Meeting Minutes](https://sre.google/sre-book/production-meeting/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
