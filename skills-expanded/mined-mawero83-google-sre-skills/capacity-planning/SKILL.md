---
name: capacity-planning
description: >-
  Plan capacity the modern Google SRE way: demand forecasting, uncertainty, failure domains, efficiency, and AI-era accelerator constraints. Use for capacity reviews, launches, and resource risk.
---

# Capacity Planning

**Domain:** `resilience`  
**Sources:** SRE Book 2e Ch15, SRE Book 1e (related load chapters)

## When to use

- Quarterly capacity plan
- Launch sizing
- GPU/TPU or scarce resource planning

## Principles

- Engineer to reduce fragile manual capacity planning where possible — but do not fly blind.
- Quantify uncertainty; plan for demand + failure domain loss.
- Efficiency and reclaiming stranded capacity are reliability work.
- AI fleets: fungibility, utilization/loss frameworks, power, and scheduling primitives matter.

## Workflow

1. Forecast demand with ranges; list drivers and leading indicators.
2. Map capacity to failure domains; reserve for N+1 / region loss as required.
3. Identify bottlenecks and degrade plans when short.
4. Set utilization targets and stranded capacity hunts.
5. For launches: peak model + soak + abort thresholds.

## Decision guide

- If supply constrained → demand shaping + prioritization of CUJs.

## Output template

```markdown
# Capacity plan
- Demand forecast (range):
- Failure domain assumptions:
- Headroom / risks:
- Efficiency actions:
- Launch/peak plan:
```

## Anti-patterns

- Planning to average only.
- Ignoring correlated failures.

## Related skills

`handling-overload`, `sre-supports-ai`, `reliable-launches`

## Canonical references

- [SRE Book 2e](https://sre.google/books/)
- [2e blog (capacity/AI themes)](https://cloud.google.com/blog/products/devops-sre/sre-book-second-edition)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
