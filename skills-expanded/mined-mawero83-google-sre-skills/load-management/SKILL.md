---
name: load-management
description: >-
  Apply load balancing and load management practices from Google SRE: frontend and datacenter LB concepts, healthy traffic shaping, and Workbook load guidance. Use when designing traffic systems or fixing imbalanced load.
---

# Load Management

**Domain:** `resilience`  
**Sources:** SRE Book 1e Ch19–20, Workbook Ch11

## When to use

- Designing LB / traffic policy
- Hotspotting / imbalance
- Planning regional failover traffic

## Principles

- Load systems should prefer healthy backends and contain blast radius.
- Global and local load decisions have different information and failure modes.
- Connection management, retries, and timeouts are part of load design.
- Observe from client and server to catch silent drop issues.

## Workflow

1. Map traffic path: DNS/GSLB → edge → service mesh/LB → instances.
2. Identify health signals used at each hop.
3. Check retry budgets and timeout budgets end-to-end.
4. Simulate backend loss; verify shedding and failover.
5. Document expected user impact during partial failure.

## Decision guide

- If retries amplify load → add budgeted retries + jitter.
- If health checks lie → fix health semantics before more capacity.

## Output template

```markdown
# Load management review
- Path diagram:
- Health signals:
- Retry/timeout budget:
- Failover behavior:
- Risks:
```

## Anti-patterns

- Infinite retries.
- LB on CPU only.

## Related skills

`handling-overload`, `cascading-failures`, `capacity-planning`

## Canonical references

- [Load Balancing Frontend](https://sre.google/sre-book/load-balancing-frontend/)
- [Load Balancing Datacenter](https://sre.google/sre-book/load-balancing-datacenter/)
- [Managing Load](https://sre.google/workbook/managing-load/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
