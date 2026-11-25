---
name: clarify-question
description: Use when a user asks an ambiguous business, product, growth, operations, reporting, CSV, spreadsheet, dashboard, or data-analysis question and the AI should clarify goal, metric, dimension, grain, timeframe, baseline, filters, and decision context before answering.
source: perlytics-skill
version: 1.0.0
---

# Clarify Question

## Purpose

Turn a vague business or analytics question into a clear analysis brief before answering.

## When to use

Use this skill when:

- the user asks "why", "what happened", or "how is X doing" without enough detail
- the user asks to analyze a file, CSV, spreadsheet, report, dashboard, or table without specifying the metric or decision
- the user says "analyze this data," "read these numbers," or "find insights" but the analytical frame is still missing
- the metric is implied but not defined
- the comparison period is missing
- the requested answer could change depending on entity, segment, or grain

## When not to use

Do not use this skill when:

- the question is already tightly scoped and fully specified
- the user is asking for a mechanical task rather than analysis framing
- the necessary metric, baseline, and decision context are already explicit

## Required thinking discipline

- Do not answer the business question immediately.
- Separate clarification from explanation.
- Ask only the minimum questions needed to make the request answerable.
- If context remains missing, state assumptions explicitly before continuing.
- **Evidence constraint:** Every conclusion must cite specific data — a number, a rate, a segment, or a timeframe. Do not speculate without evidential basis. If data is insufficient, state what is missing rather than asserting an unsupported inference.

## Workflow

1. Restate the user's question in neutral business terms.
2. Identify missing elements:
   - **Metric**: the quantitative definition being analyzed
   - **Dimension**: the categorical breakdown used to slice the metric
   - **Grain**: the unit of observation (day, order, user, account, etc.)
   - **Timeframe**: the period included in the analysis
   - **Baseline**: the reference point used for comparison
   - **Filter**: the inclusion or exclusion rule that narrows scope
   - **Decision context**: what action or decision this analysis is meant to inform
3. Ask the smallest useful set of clarifying questions.
4. If the user cannot answer, propose default assumptions and mark them clearly.
5. Produce a clarified analysis brief before any interpretation.

## Output format

- Original question
- Clarified objective
- Candidate metric definition
- Proposed dimensions or segments
- Grain and timeframe
- Comparison baseline
- Needed filters
- Open questions
- Working assumptions

## Good example

User:

> Why did revenue drop last month?

Good response:

> Before diagnosing the drop, I need to pin down the frame. Are we looking at gross or net revenue, billed or recognized revenue, which market, and compared with which baseline: prior month, prior 4 weeks, or same month last year?  
> Working brief if unanswered: net recognized revenue, daily grain, all markets, compared with the prior 4-week baseline.

## Bad example

> Revenue likely dropped because of seasonality, lower conversion, and churn.

Why this is bad:

- it assumes the metric
- it assumes the comparison period
- it jumps to drivers before the question is scoped

## Practical notes

- If several missing items exist, ask grouped questions instead of a long checklist.
- Prefer clarifying decision context, not just data context.
- When useful, turn the user's request into a one-paragraph analysis brief.
- Generic asks like "analyze this CSV" or "look at this dashboard" usually need this skill unless the metric and baseline are already obvious.

## Optional variants

- For executives: ask fewer questions and propose stronger defaults.
- For analyst teams: be stricter about grain, filters, and baseline.
- For dashboards: explicitly ask whether the question is diagnostic or monitoring-oriented.
