---
name: crisis-management
description: >-
  Manage organizational crises spanning reliability and security: prestaging, crisis comms, cross-functional command, and aftermath — from Building Secure & Reliable Systems. Use for wide-impact disasters and security crises.
---

# Crisis Management

**Domain:** `operations`  
**Sources:** Building Secure & Reliable Systems Ch16–18

## When to use

- Company-wide or multi-system crisis
- Security + reliability joint incident
- Disaster plan activation

## Principles

- Prestage people, systems, and decision rights before the bad day.
- Crisis management ≠ routine incident response — scale of coordination differs.
- Communications strategy is part of mitigation.
- Aftermath: eject/mitigate/learn with deliberate sequencing (esp. attackers).

## Workflow

1. Activate crisis team; clarify authority and legal/comms partners.
2. Establish facts cadence; separate rumormill from state doc.
3. Prioritize life-safety / customer trust / data protection as applicable.
4. Execute technical mitigations with incident-management discipline.
5. Plan recovery & disclosure; schedule deep retrospective.

## Decision guide

- If active adversary → do not tip off prematurely; coordinate with security.

## Output template

```markdown
# Crisis brief
- Authority / command:
- Known facts vs unknowns:
- Customer/trust impact:
- Comms plan:
- Technical priorities:
- Aftermath owners:
```

## Anti-patterns

- Ad-hoc exec pile-on without IC.
- Destroying forensic evidence early.

## Related skills

`incident-management`, `security-incident-response`, `disaster-planning`

## Canonical references

- [Building Secure & Reliable Systems](https://google.github.io/building-secure-and-reliable-systems/)
- [SRE books hub](https://sre.google/books/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
