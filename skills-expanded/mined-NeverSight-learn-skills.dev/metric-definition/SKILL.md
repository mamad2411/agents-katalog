---
name: metric-definition
description: Use when an analysis depends on a KPI, metric, ratio, column label, or business definition that could be interpreted in multiple valid ways across datasets, dashboards, or reports.
source: perlytics-skill
version: 1.0.0
---

# Metric Definition

## Purpose

Force precise metric definitions before interpretation, reporting, or comparison.

## When to use

Use this skill when:

- a metric name could mean several things
- a file, chart, or dashboard contains labels like revenue, usage, activation, churn, or cost that are not yet formally defined
- the user asks for analysis of a dataset but the main KPI could be interpreted in multiple valid ways
- teams are debating a KPI
- an answer depends on denominator choice
- a dashboard label is too vague to trust

## When not to use

Do not use this skill when:

- the metric has an agreed canonical definition already documented and confirmed
- the task is pure arithmetic on an already defined metric

## Required thinking discipline

- Never treat a metric label as a definition.
- Identify numerator and denominator clearly.
- Specify the entity, grain, timeframe, and filters.
- Surface definition risks that could change interpretation.
- **Evidence constraint:** Every conclusion must cite specific data — a number, a rate, a segment, or a timeframe. Do not speculate without evidential basis. If data is insufficient, state what is missing rather than asserting an unsupported inference.

## Workflow

1. Restate the metric name.
2. Define what is counted.
3. Define what is excluded.
4. Define denominator logic if the metric is a rate or ratio.
5. Specify grain, timeframe, and segment rules.
6. Note data source or implementation assumptions.
7. Produce a metric spec before any narrative interpretation.

## Output format

- Metric name
- Business intent
- Formal definition
- Numerator
- Denominator
- Entity and grain
- Timeframe logic
- Filters and exclusions
- Known ambiguities

## Good example

Metric:

> Activation rate

Good response:

> Activation rate = share of new signups who complete project creation within 7 days of signup.  
> Numerator: distinct new users who create at least one project within 7 days.  
> Denominator: distinct new signups in the cohort.  
> Exclude internal accounts and spam-flagged users.

## Bad example

> Activation rate is how many users become activated.

Why this is bad:

- numerator is undefined
- denominator is missing
- time window is missing
- exclusions are unclear

## Practical notes

- If a metric is controversial, show 2 possible valid definitions and explain the consequence.
- For executive readouts, include one plain-English definition plus one formal definition.
- In generic data-analysis asks, use this skill whenever a column name or KPI label could silently change the conclusion.

## Optional variants

- Growth metrics: be strict about attribution windows and exclusion rules.
- Finance metrics: be strict about recognition timing and currency handling.
- Operations metrics: clarify service level thresholds and exception handling.
