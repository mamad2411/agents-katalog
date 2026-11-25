---
name: canarying-releases
description: >-
  Design and evaluate canaries: metrics, blast radius, abort criteria, and automation from the SRE Workbook. Use before risky prod changes and when building progressive delivery.
---

# Canarying Releases

**Domain:** `delivery`  
**Sources:** Workbook Ch16, SRE Book 2e Ch14/17

## When to use

- Shipping risky changes
- Building progressive delivery
- Post-incident 'we should have canaried'

## Principles

- Canaries need success metrics tied to SLIs, not only 'process up'.
- Start small; raise traffic only on evidence.
- Automated abort beats hopeful watching.
- Canary the config and data changes too — not only code.

## Workflow

1. Define blast radius steps (1% → 10% → 50% → 100% or equivalent).
2. Pick canary SLIs/signals and abort thresholds.
3. Ensure enough traffic for statistical usefulness.
4. Include bake time; watch burn rate and key business metrics.
5. Document who can force-promote and when.

## Decision guide

- If traffic too low for stats → longer bake or synthetic + careful promotion.

## Output template

```markdown
# Canary plan
- Change:
- Stages:
- Metrics / abort:
- Owner during bake:
- Rollback command:
```

## Anti-patterns

- Canary without metrics.
- 10-second bake on critical path.

## Related skills

`release-engineering`, `alerting-on-slos`, `testing-for-reliability`

## Canonical references

- [Canarying Releases](https://sre.google/workbook/canarying-releases/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
