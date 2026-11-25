---
name: nalsd-system-design
description: >-
  Practice Non-Abstract Large System Design (NALSD): quantitative design with back-of-envelope capacity, bottlenecks, and iterative refinement from the SRE Workbook. Use for design interviews, RFCs, and capacity-aware design.
---

# NALSD — Non-Abstract Large System Design

**Domain:** `resilience`  
**Sources:** Workbook Ch12

## When to use

- Writing an RFC / design doc
- SRE design interview prep
- Estimating if a design can work at scale

## Principles

- Design with numbers: QPS, payload, fanout, storage growth, failure rates.
- Iterate: compute → find bottleneck → redesign → recompute.
- Include failure and operational concerns in the design, not as appendix fluff.
- Prefer simple designs that meet numbers over elegant ones that do not.

## Workflow

1. State requirements: traffic, latency, durability, cost envelope.
2. Draw one-page component diagram.
3. Compute resource needs and bottlenecks.
4. Add failure modes and ops plan (SLIs, deploy, overload).
5. Iterate until numbers and complexity are acceptable.

## Decision guide

- If bottleneck is a single writer → shard, batch, or change consistency needs.

## Output template

```markdown
# NALSD worksheet
- Requirements:
- Diagram:
- Key calculations:
- Bottlenecks:
- Redesign iterations:
- Ops/SLO plan:
```

## Anti-patterns

- Abstract boxes with no math.
- Ignoring ops until production.

## Related skills

`capacity-planning`, `simplicity`, `designing-for-resilience`

## Canonical references

- [NALSD](https://sre.google/workbook/non-abstract-design/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
