---
name: sre-foundations
description: >-
  Teach and apply core Google SRE foundations: reliability as a feature, software engineering applied to operations, sociotechnical systems, and when SRE is the right model. Use when onboarding SREs, explaining what SRE is, framing reliability work, or starting a learning path.
---

# SRE Foundations

**Domain:** `foundations`  
**Sources:** SRE Book 1e Ch1–2, SRE Book 2e Ch1–3, Workbook Ch1

## When to use

- Someone asks what SRE is or how it differs from DevOps/ops
- Building an SRE team charter or mission
- Onboarding a new SRE or reliability partner
- Choosing whether to adopt SRE practices

## Principles

- SRE is a dedicated voice for reliability using a software-engineering approach to operations.
- 100% is the wrong reliability target — cost and velocity trade off against perfection.
- Reliability is a feature with customer, CFO, engineering, and cultural value (Book 2e).
- Treat production as a sociotechnical system: people, process, and software together.
- Hierarchy of production health (Book 2e): situational awareness → continuous preparedness → infrastructure design → resilient products → emergent reliability.

## Workflow

1. Clarify the audience: aspiring SRE, practitioner, or leader.
2. Define the reliability problem in user-journey terms (not infra symptoms).
3. Map current maturity: absent → reactive → proactive → strategic → visionary.
4. Pick one foundational practice to install first (usually SLOs + error budgets).
5. Write a one-page charter: mission, scope, services, success metrics, values.
6. Point learners to the Learning Path skill and the Source Map.

## Decision guide

- If the org has no shared reliability language → start with SLIs/SLOs, not tooling.
- If ops is pure ticket toil → prioritize toil measurement + automation before hiring more humans.
- If leadership wants 'SRE' as a rename of ops → push back; require engineering time (≥50% aspirational).

## Output template

```markdown
# SRE foundations brief
- Audience:
- Reliability problem (user journey):
- Maturity today → target:
- First practice to install:
- Charter draft link / text:
- Canonical docs to read next:
```

## Anti-patterns

- Equating SRE with 'people who carry pagers'.
- Buying observability tools before defining user-facing SLIs.
- Copying Google org charts without Google's error-budget culture.

## Related skills

`value-of-reliability`, `sli-slo-design`, `learning-path-sre`, `sre-culture`

## Canonical references

- [SRE Book TOC](https://sre.google/sre-book/table-of-contents/)
- [Workbook TOC](https://sre.google/workbook/table-of-contents/)
- [SRE books hub](https://sre.google/books/)
- [SRE ↔ DevOps](https://sre.google/workbook/how-sre-relates/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
