---
name: testing-for-reliability
description: >-
  Build a reliability testing strategy: unit→integration→canary→fault injection→DR, plus emergent agentic testing themes from SRE Book 2e. Use when improving test strategy for production confidence.
---

# Testing For Reliability

**Domain:** `delivery`  
**Sources:** SRE Book 1e Ch17, SRE Book 2e Ch14

## When to use

- Strengthening release confidence
- Introducing chaos/fault injection
- Emergency rollout testing gaps

## Principles

- Tests reduce uncertainty; they do not create certainty.
- Production-like environments and progressive delivery catch what labs miss.
- Fault injection finds cascade and degrade bugs traditional tests miss.
- Test the emergency path (rollback, flag off) regularly.

## Workflow

1. Map riskiest failure modes → missing tests.
2. Ensure critical CUJ integration coverage.
3. Add canary metrics as production tests.
4. Pilot fault injection in nonprod then limited prod blast radius.
5. Schedule DR / restore / failover tests.

## Decision guide

- If only unit tests gate prod → raise bar for critical services.

## Output template

```markdown
# Reliability test plan
- Critical risks:
- Current coverage gaps:
- New tests / fault drills:
- Cadence:
```

## Anti-patterns

- Chaos without observability or abort.
- Never testing rollback.

## Related skills

`canarying-releases`, `disaster-planning`, `designing-for-resilience`

## Canonical references

- [Testing for Reliability](https://sre.google/sre-book/testing-for-reliability/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
