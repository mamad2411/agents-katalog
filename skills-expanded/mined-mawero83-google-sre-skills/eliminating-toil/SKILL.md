---
name: eliminating-toil
description: >-
  Identify, measure, and eliminate toil using Google SRE definitions and automation strategy. Use when on-call is drowning in repetitive work, planning automation, or defending engineering time.
---

# Eliminating Toil

**Domain:** `foundations`  
**Sources:** SRE Book 1e Ch5/7, Workbook Ch6, SRE Book 2e Ch13

## When to use

- Measuring toil %
- Prioritizing automation backlog
- Justifying eng time vs tickets

## Principles

- Toil: manual, repetitive, automatable, tactical, no enduring value, scales with service growth.
- Aspirational: keep toil well under ~50% of time so engineering can happen.
- Automate incrementally; avoid big-bang automation snowballs without ROI.
- Sometimes temporary toil is correct (rare events, unclear requirements).

## Workflow

1. Inventory recurring tasks for 2–4 weeks (or sample on-call diary).
2. Classify toil vs engineering; estimate hours.
3. Score automation candidates: frequency × pain × safety × ROI.
4. Ship smallest safe automation; measure hours returned.
5. Feed chronic toil into error-budget / planning conversations.

## Decision guide

- If task is rare and dangerous to automate wrong → checklist/runbook first.
- If toil grows linearly with customers → prioritize before hiring.

## Output template

```markdown
# Toil reduction plan
- Current toil % estimate:
- Top toil items (hours/month):
- Automation candidates ranked:
- Next 2 shipped automations:
- Success metric:
```

## Anti-patterns

- Automating a broken process.
- Counting all ops work as toil.

## Related skills

`automation-tooling`, `operational-overload`, `software-engineering-in-sre`

## Canonical references

- [Eliminating Toil](https://sre.google/sre-book/eliminating-toil/)
- [Workbook Eliminating Toil](https://sre.google/workbook/eliminating-toil/)
- [Evolution of Automation](https://sre.google/sre-book/automation-at-google/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
