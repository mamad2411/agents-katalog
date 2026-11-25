---
name: sre-in-diverse-environments
description: >-
  Adapt SRE practices for startups, solo SRE, hybrid/legacy, and constrained orgs — from SRE Book 2e Ch22. Use when classic Google-scale patterns do not fit and you need pragmatic reliability.
---

# SRE In Diverse Environments

**Domain:** `ai`  
**Sources:** SRE Book 2e Ch22, Workbook Ch1/19–21

## When to use

- First SRE in a startup
- Legacy/mainframe adjacent systems
- Severe staffing constraints

## Principles

- Principles scale down; org charts may not.
- Start with SLOs on the few CUJs that pay the bills.
- Buy/borrow platform capabilities before building Google clones.
- Document constraints honestly; design around them.

## Workflow

1. List constraints (staff, access, change windows, legacy).
2. Pick minimal viable SRE set: SLO, paging hygiene, postmortem, rollback.
3. Automate the noisiest toil first.
4. Expand engagement as trust grows.

## Decision guide

- If solo → ruthlessly limit scope; escalate org risk visibly.

## Output template

```markdown
# Pragmatic SRE plan
- Constraints:
- MVP practices:
- 90-day roadmap:
- Explicit non-goals:
```

## Anti-patterns

- Boiling the ocean with full Google clone on day one.

## Related skills

`sre-foundations`, `sli-slo-design`, `sre-engagement-model`

## Canonical references

- [SRE Book 2e](https://sre.google/books/)
- [How SRE Relates to DevOps](https://sre.google/workbook/how-sre-relates/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
