---
name: sre-communication
description: >-
  Improve SRE communication and collaboration: production meetings, stakeholder updates, and cross-team clarity from Google SRE. Use for meeting design and stakeholder management.
---

# SRE Communication

**Domain:** `organization`  
**Sources:** SRE Book 1e Ch31 + App F, Workbook processes chapters

## When to use

- Production meeting redesign
- Stakeholder trust issues
- Cross-team incident friction

## Principles

- Regular production meetings with data beat status theater.
- Write for the audience; executives need impact and decisions.
- Shared vocabulary (SLO, budget, severity) reduces conflict.

## Workflow

1. Define meeting purpose, attendees, and artifacts.
2. Standard agenda: SLO/budget, incidents, risks, decisions.
3. Publish notes with owners/dates.
4. Kill meetings that produce no decisions.

## Decision guide

- If meeting >30–45m without decisions → redesign.

## Output template

```markdown
# Comms / meeting design
- Purpose:
- Agenda:
- Artifacts:
- Decision log method:
```

## Anti-patterns

- Meetings as blame sessions.
- No written decisions.

## Related skills

`production-meetings`, `incident-management`, `sre-engagement-model`

## Canonical references

- [Communication and Collaboration](https://sre.google/sre-book/communication-and-collaboration-in-sre/)
- [Example Production Meeting](https://sre.google/sre-book/production-meeting/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
