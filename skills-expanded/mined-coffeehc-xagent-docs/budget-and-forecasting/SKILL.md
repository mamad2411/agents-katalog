---
name: budget-and-forecasting
description: Use when creating, reviewing, explaining, or improving budgets, forecasts, variance analysis, expense plans, headcount plans, department budgets, cash planning assumptions, scenario plans, or finance operating summaries. Prefer this Skill when the task needs assumptions, drivers, variance explanation, scenario logic, or management narrative. Do not use for accounting advice, tax advice, audit assurance, or bank actions.
meta:
  version: 1
  display_name: 预算与预测
---

# Budget And Forecasting

## Purpose

Turn financial operating information into clear budget, forecast, variance, and scenario narratives with explicit assumptions and drivers.

## Use When

Use for:

- budget drafts
- forecast narratives
- variance analysis
- expense planning
- headcount planning
- cash planning assumptions
- scenario planning
- management finance summaries

## Material Gate

Identify:

- period, currency, unit, department, owner, and source data
- baseline, actuals, forecast, budget, and variance definitions
- revenue, cost, hiring, usage, price, churn, or timing drivers
- audience and decision need

If numbers are missing or unverified, state assumptions and avoid false precision.

## Workflow

1. Clarify the planning question and time period.
2. Separate actuals, budget, forecast, assumptions, and scenario inputs.
3. Identify the drivers behind major movements.
4. Explain variance by price, volume, mix, timing, one-time items, or operational change.
5. Build scenarios when uncertainty is material.
6. Translate finance detail into management narrative.
7. Use `data-visual-report-builder` or `html-report-builder` for budget reports when needed.

## Checks

- Units, currency, period, and source are visible.
- Variance has driver explanation, not only numbers.
- Assumptions are explicit.
- Scenario outputs are not treated as predictions.
- Accounting, tax, or audit conclusions are not overclaimed.

## Outputs

- budget narrative
- forecast summary
- variance analysis
- scenario plan
- expense review
- headcount plan summary
- cash planning note

## Boundary

This Skill owns budget reasoning, forecast narrative, variance framing, and scenario structure. It does not own accounting policy, tax advice, audit assurance, banking actions, ERP writes, payroll, or finance approval.

It must not run shell, Python, Node, npm, curl, MCP, ERP, accounting system, banking, payroll, spreadsheet, package install, or external API commands by itself; those actions belong to XAgent tools visible in the current session.
