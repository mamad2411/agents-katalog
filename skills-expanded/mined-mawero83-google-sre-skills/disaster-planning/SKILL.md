---
name: disaster-planning
description: >-
  Create pragmatic disaster plans: prestaging, DR tests, roles, and scenario playbooks from Building Secure & Reliable Systems. Use for DR programs and wide-scale outage preparedness.
---

# Disaster Planning

**Domain:** `security`  
**Sources:** Building Secure & Reliable Systems Ch16, SRE Book 1e testing/DR themes

## When to use

- DR program design
- Region failure planning
- Tabletop exercises

## Principles

- You cannot plan every scenario — you can prestage people, access, and systems.
- Test restores and failovers; paper plans rot.
- Include communications and decision rights.
- Relate DR objectives to data RPO/RTO.

## Workflow

1. List plausible disasters by impact (region, identity, supply chain).
2. For top scenarios: roles, dependencies, runbooks, data plan.
3. Prestage access, artifacts, and out-of-band comms.
4. Run tabletop + technical drill; log gaps.
5. Fix gaps; schedule next drill.

## Decision guide

- If never tested failover → do not claim multi-region readiness.

## Output template

```markdown
# Disaster plan summary
- Top scenarios:
- Prestaged assets:
- Last drill results:
- Open gaps:
```

## Anti-patterns

- Binders nobody drills.
- DR only for compliance theater.

## Related skills

`data-integrity`, `crisis-management`, `testing-for-reliability`

## Canonical references

- [Building Secure & Reliable Systems](https://google.github.io/building-secure-and-reliable-systems/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
