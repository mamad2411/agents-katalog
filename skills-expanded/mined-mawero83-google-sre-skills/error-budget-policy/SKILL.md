---
name: error-budget-policy
description: >-
  Draft and enforce Google-style error budget policies that balance feature velocity with reliability: freezes, postmortem triggers, and planning inputs. Use when defining what happens when an SLO is missed.
---

# Error Budget Policy

**Domain:** `foundations`  
**Sources:** Workbook App B, Workbook Ch2, SRE Book 1e Ch3–4

## When to use

- SLO exists but no consequences when burned
- Product wants to ship during reliability debt
- Writing governance for releases vs reliability

## Principles

- Error budget = 1 − SLO; it is the agreed risk spend for change.
- Policy must be binary enough to act: e.g. halt non-P0/security changes when budget exhausted over the window.
- Large single-incident burns (e.g. >20% of 4-week budget) mandate postmortem + P0 action.
- Recurring class of outages → quarterly P0 reliability work.

## Workflow

1. Confirm SLOs and windows are documented and measured.
2. Draft policy: green path (releases proceed) vs red path (freeze + reliability focus).
3. Define exceptions (P0, security) narrowly.
4. Define postmortem triggers and planning hooks.
5. Get eng + product + SRE sign-off; publish next to SLO doc.
6. Review after first freeze — refine fairness and clarity.

## Decision guide

- If political freeze is impossible → start with mandatory reliability allocation % instead of hard freeze, then tighten.
- If multiple SLOs → enact policy when ANY objective exhausts its budget.

## Output template

```markdown
# Error budget policy
- Service + SLO window:
- Green behavior:
- Red behavior (freeze / focus):
- Exceptions:
- Postmortem triggers:
- Quarterly planning hooks:
- Owners / escalation:
```

## Anti-patterns

- Policy without measurement.
- Endless exceptions that empty the policy.

## Related skills

`sli-slo-design`, `learning-from-incidents`, `release-engineering`

## Canonical references

- [Example Error Budget Policy](https://sre.google/workbook/error-budget-policy/)
- [Implementing SLOs](https://sre.google/workbook/implementing-slos/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
