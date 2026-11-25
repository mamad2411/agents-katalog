---
name: emergency-response
description: >-
  Execute emergency response playbooks: what to do when paged, prioritization under stress, and safe emergency changes. Use for Sev-level events and emergency rollouts.
---

# Emergency Response

**Domain:** `operations`  
**Sources:** SRE Book 1e Ch13, SRE Book 2e Ch14 (emergency rollouts)

## When to use

- Pager for user-visible outage
- Need emergency rollback/config
- Drilling emergency response

## Principles

- Stop the bleeding first; aesthetics later.
- Prefer tested rollbacks/feature flags over novel hotfixes when possible.
- Keep an audit trail of emergency actions.
- Practice — emergencies are poor times to invent process.

## Workflow

1. Ack page; open runbook + dashboards.
2. Assess severity; escalate/declare incident if needed.
3. Apply known-good mitigation (rollback, flag, capacity, shed load).
4. Verify user-facing SLI recovery.
5. Log actions; transition to incident-management if ongoing.

## Decision guide

- If fix is untested and blast radius high → mitigate with disable/rollback first.

## Output template

```markdown
# Emergency actions log
- Page / symptom:
- Severity:
- Actions (time, who, what):
- SLI verification:
- Follow-up incident/postmortem?:
```

## Anti-patterns

- Unreviewed prod edits without notes.
- Skipping verification.

## Related skills

`incident-management`, `canarying-releases`, `handling-overload`

## Canonical references

- [Emergency Response](https://sre.google/sre-book/emergency-response/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
