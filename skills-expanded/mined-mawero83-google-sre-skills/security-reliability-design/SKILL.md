---
name: security-reliability-design
description: >-
  Design systems that are both secure and reliable using Building Secure & Reliable Systems: tradeoffs, least privilege, resilience to attack, and lifecycle integration. Use when security and reliability requirements collide.
---

# Security Reliability Design

**Domain:** `security`  
**Sources:** Building Secure & Reliable Systems

## When to use

- Security vs availability tradeoff debates
- Threat-aware design reviews
- Hardening critical systems

## Principles

- A system is not truly reliable if insecure, nor secure if unreliable.
- Integrate security+reliability across design, code, and operations.
- Understand adversaries; design for compromise containment.
- Prefer safe proxies, least privilege, and recoverable controls.

## Workflow

1. Identify assets, adversaries, and reliability CUJs.
2. Map tradeoffs (e.g. lockout vs availability).
3. Design controls that fail safely for both properties.
4. Require detection + recovery paths, not only prevention.
5. Review with both SRE and security owners.

## Decision guide

- If break-glass exists → time-bound, audited, dual-control when needed.

## Output template

```markdown
# Secure+reliable design review
- Assets / CUJs:
- Threats:
- Tradeoffs decided:
- Controls + recovery:
- Gaps:
```

## Anti-patterns

- Security bolted on after GA.
- Reliability that ignores abuse cases.

## Related skills

`security-incident-response`, `designing-for-resilience`, `disaster-planning`

## Canonical references

- [Building Secure & Reliable Systems](https://google.github.io/building-secure-and-reliable-systems/)
- [SRE books hub](https://sre.google/books/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
