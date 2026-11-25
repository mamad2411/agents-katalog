---
name: pager-hygiene
description: >-
  Establish pager hygiene standards: what deserves a page, runbook links, ownership, severity, and handoff quality. Use as a lightweight companion to alert-noise-reduction and on-call-excellence.
---

# Pager Hygiene

**Domain:** `operations`  
**Sources:** SRE Book 1e Ch10–11, Workbook Ch5/8

## When to use

- Creating a new alert
- Alert review councils
- On-call quality regressions

## Principles

- Page only for urgent, user-impacting, actionable problems.
- Every page has a runbook and an owner team.
- Severity vocabulary is shared org-wide.
- Silent pages (no runbook) are bugs.

## Workflow

1. For each new page: assert user impact, urgency, action.
2. Attach runbook with diagnose → mitigate → escalate.
3. Set urgency and routing; avoid dual primary pages.
4. Review pages quarterly; delete/demote ruthlessly.

## Decision guide

- If 'FYI' → never page; ticket/Slack.

## Output template

```markdown
# Alert quality checklist
- User impact?:
- Action?:
- Runbook URL:
- Owner:
- Page vs ticket:
```

## Anti-patterns

- Informational pages.
- Orphan alerts.

## Related skills

`alert-noise-reduction`, `alerting-on-slos`, `on-call-excellence`

## Canonical references

- [Practical Alerting](https://sre.google/sre-book/practical-alerting/)
- [Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
