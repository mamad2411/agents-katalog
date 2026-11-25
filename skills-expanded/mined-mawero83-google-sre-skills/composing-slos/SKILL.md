---
name: composing-slos
description: >-
  Compose multi-service reliability mathematically: serial vs parallel dependencies, hedging, and dependency budgets. Use when deriving platform or path SLOs from dependencies.
---

# Composing SLOS

**Domain:** `foundations`  
**Sources:** SRE Book 2e Appendix E, Workbook Ch2 (advanced)

## When to use

- Service depends on many backends and needs a path SLO
- Debating whether dependency SLOs multiply correctly
- Designing hedging / parallel fanout reliability

## Principles

- Serial dependencies multiply availability (roughly); many 99.9% deps destroy path reliability.
- Parallel with hedging can improve latency/availability — model carefully.
- Budget dependencies intentionally; do not assume independent failures.
- Prefer fewer critical deps and soft dependencies with graceful degradation.

## Workflow

1. Draw the CUJ dependency graph (critical vs soft).
2. Classify edges: serial, parallel, hedged.
3. Compute approximate path availability from component SLOs.
4. Identify weakest links and redesign (cache, degrade, shed).
5. Document assumptions (independence, correlated failure domains).

## Decision guide

- If product of deps < target → reduce critical path or raise dep SLOs / add fallbacks.
- If failures correlate (same zone/region) → treat as shared failure domain, not independent.

## Output template

```markdown
# Composed SLO analysis
- CUJ path:
- Critical deps + their SLOs:
- Serial/parallel/hedged model:
- Estimated path reliability:
- Gaps vs target + mitigations:
```

## Anti-patterns

- Multiplying SLOs blindly without correlation analysis.

## Related skills

`sli-slo-design`, `designing-for-resilience`, `cascading-failures`

## Canonical references

- [Implementing SLOs](https://sre.google/workbook/implementing-slos/)
- [SRE Book 2e overview](https://sre.google/books/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
