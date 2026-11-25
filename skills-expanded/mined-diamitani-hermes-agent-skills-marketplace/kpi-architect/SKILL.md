---
name: kpi-architect
description: "Use when generating KPIs and activity metrics from business goals. Creates measurable performance indicators tied to strategic objectives."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [kpi, metrics, performance, okrs, business-intelligence, dashboards]
    related_skills: [strategic-business-architect, gtm-architect, sop-architect]
---

# KPI Architect

## Overview

Translates high-level business goals and strategic objectives into concrete, measurable Key Performance Indicators. For each KPI, defines the formula, data source, measurement cadence, target/benchmark, and which team owns the number. Helps teams move from "we should track this" to "here's exactly what we measure every week."

## When to Use

- A leader says "we need KPIs" but hasn't defined what success looks like.
- Building a dashboard or scorecard and need the right metrics (not vanity metrics).
- Aligning team-level activity metrics with company-level strategic objectives.
- Designing compensation or bonus structures tied to measurable outcomes.
- Auditing existing KPIs for relevance, actionability, and data availability.
- Don't use for: financial modeling, valuation, or accounting metrics (those need domain-specific tools).

## How It Works

1. **Goal Discovery** — Extracts strategic objectives from user input (revenue targets, growth goals, efficiency aims, quality targets).
2. **Metric Generation** — Maps each goal to leading and lagging indicators, organized by business function (sales, marketing, product, CS, ops).
3. **KPI Specification** — For each KPI: name, formula, data source, owner, cadence, target, and alert threshold.
4. **Gap Analysis** — Flags objectives with no measurable indicators and warns about vanity metrics.

## Steps

1. **Gather objectives:** Ask: What are the top 3-5 business goals this quarter/year? What teams or functions are involved? What decisions will these KPIs drive?
2. **Generate metric tree:** Produce a structured breakdown:
   - **Lagging indicators** (outcomes): revenue, churn, NPS, gross margin.
   - **Leading indicators** (activities): demos booked, pipeline created, activation rate, support tickets resolved.
3. **Specify each KPI** with: Name | Formula | Data Source | Owner | Cadence | Target | Red/Yellow/Green thresholds.
4. **Reality check:** For each KPI, ask: Can we actually measure this today? If not, flag it as aspirational and suggest a proxy metric until instrumentation is ready.
5. **Dashboard mapping:** Recommend the best dashboard layout: which metrics go top-left (most critical), groupings by team, and comparison periods (WoW, MoM, QoQ, YoY).

## Common Pitfalls

1. **Vanity metrics:** "Page views" and "followers" feel good but rarely drive decisions. Every KPI must pass the "so what?" test — what action changes if this number moves?
2. **Too many KPIs:** If a team has 20+ KPIs, they're tracking everything and acting on nothing. Aim for 3-7 per team.
3. **No owner:** A KPI without an accountable person is a suggestion, not a metric. Every number needs a name.
4. **Unmeasurable KPIs:** "Brand awareness" is real but hard to instrument. Pair it with a measurable proxy (share of voice, branded search volume) until better data exists.
5. **Static targets:** KPIs need quarterly review. A Q1 target may be irrelevant by Q3 — build in a review cadence.

## Verification Checklist

- [ ] Every strategic objective maps to at least one KPI
- [ ] Each KPI has: formula, data source, owner, cadence, target
- [ ] Leading and lagging indicators are balanced
- [ ] Vanity metrics are flagged or removed
- [ ] Aspirational (not-yet-measurable) KPIs have proxy alternatives
- [ ] Dashboard layout recommendation is included

## Source

Originally a custom GPT: [KPI Architect](https://chatgpt.com/g/g-68ae5416b9848191831ef9943306451d-kpi-architect-gpt)
