---
name: dashboard-critique
description: Use when reviewing a dashboard, KPI page, or reporting artifact and the AI should assess metric clarity, structure, comparability, and decision usefulness.
source: perlytics-skill
version: 1.0.0
---

# Dashboard Critique

## Purpose

Assess whether a dashboard helps people make better decisions or merely displays numbers.

## When to use

Use this skill when:

- reviewing a KPI dashboard
- improving an existing report
- deciding whether a dashboard is fit for stakeholder use

## When not to use

Do not use this skill when:

- the task is to diagnose a metric change in detail
- there is no reporting artifact to review

## Required thinking discipline

- Judge the dashboard against decisions, not aesthetics alone.
- Check metric definitions, baselines, and comparability.
- Look for ways the dashboard could mislead a stakeholder.
- **Evidence constraint:** Every conclusion must cite specific data — a number, a rate, a segment, or a timeframe. Do not speculate without evidential basis. If data is insufficient, state what is missing rather than asserting an unsupported inference.

## Workflow

1. Identify the audience and decision use case.
2. Review metric labels and definitions.
3. Review baselines, comparisons, and time context.
4. Review segmentation and drill-down usefulness.
5. Identify likely misreads or missing context.
6. Recommend the smallest changes that materially improve decision value.

## Output format

- Intended audience
- What works
- What is unclear or risky
- Missing context
- Recommended changes
- Priority order

## Good example

> The dashboard shows weekly active users but not the baseline, target, or segmentation. A manager can see the count moved, but not whether the movement is meaningful or where it came from.

## Bad example

> The dashboard looks busy and should be cleaner.

Why this is bad:

- it is mostly aesthetic
- it ignores business usefulness
- it does not mention metric clarity

## Practical notes

- A good dashboard usually answers a recurring decision question.
- If a metric can be interpreted multiple ways, the dashboard should not force the audience to guess.

## Optional variants

- Executive dashboards: focus on signal hierarchy and decision framing.
- Analyst dashboards: focus on drill paths, definitions, and segment cuts.
