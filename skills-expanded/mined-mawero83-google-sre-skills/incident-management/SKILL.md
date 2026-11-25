---
name: incident-management
description: >-
  Run Google-style incident management: roles (IC, comms, ops), severity, lifecycle detection→triage→investigate→mitigate→resolve→learn, and state documents. Use for live incidents and process design.
---

# Incident Management

**Domain:** `operations`  
**Sources:** SRE Book 1e Ch14 + App C, Workbook Ch9, SRE Book 2e Ch10

## When to use

- Live incident
- Designing incident process
- Training ICs

## Principles

- Declare early; clarity beats ego.
- Separate roles: Incident Commander, Communications, Operations/Scribe.
- Mitigation before root cause when users are hurting.
- Single source of truth state doc; periodic stakeholder updates.
- AI may assist triage/hypotheses — humans retain authority for risky mitigations (2e).

## Workflow

1. Detect & declare; assign severity and IC.
2. Spin roles; open state doc from template.
3. Triage: impact, CUJ, customer scope.
4. Investigate with troubleshooting skill; mitigate ASAP.
5. Communicate on cadence (internal + external as needed).
6. Resolve; schedule postmortem if budget/severity thresholds met.

## Decision guide

- If IC also deep in debug → hand IC role off.
- If security angle → engage security-incident-response.

## Output template

```markdown
# Incident state
- Severity / IC / roles:
- Impact statement:
- Timeline (UTC):
- Hypotheses:
- Mitigations applied:
- Next update at:
```

## Anti-patterns

- Silent heroic debugging.
- Root-cause rabbit holes while users burn.

## Related skills

`emergency-response`, `crisis-management`, `learning-from-incidents`, `effective-troubleshooting`

## Canonical references

- [Managing Incidents](https://sre.google/sre-book/managing-incidents/)
- [Workbook Incident Response](https://sre.google/workbook/incident-response/)
- [Example Incident State Doc](https://sre.google/sre-book/example-state-message/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
