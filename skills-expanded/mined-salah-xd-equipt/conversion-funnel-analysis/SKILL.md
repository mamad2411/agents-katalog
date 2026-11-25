---
name: conversion-funnel-analysis
description: "Maps and analyzes conversion funnels with drop-off identification, optimization priorities, and benchmarking. Use when diagnosing where prospects are lost in your sales process."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Conversion Funnel Analysis

## When to Use This Skill

Use this skill when you need to:
- Map your customer journey from awareness to purchase
- Identify where the biggest drop-offs occur in your funnel
- Prioritize optimization efforts for maximum conversion impact
- Benchmark your funnel performance against industry standards

**DO NOT** use this skill for A/B test design, ad campaign optimization, or CRM pipeline management. This is for analyzing and diagnosing funnel performance.

---

## Core Principle

FIX THE BIGGEST LEAK FIRST — A 10% IMPROVEMENT AT THE WORST DROP-OFF POINT BEATS A 50% IMPROVEMENT AT A STEP THAT ALREADY CONVERTS WELL.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Funnel type** | "What funnel? (website, e-commerce checkout, SaaS signup, sales pipeline)" | Website lead funnel |
| **Funnel stages** | "List every step from first visit to final conversion." | Must be provided |
| **Current data** | "Do you have numbers for each stage? (visitors, leads, trials, purchases)" | Must be provided or estimated |
| **Time period** | "What time period does the data cover?" | Last 30 days |
| **Goal** | "What conversion rate are you targeting for the full funnel?" | Industry benchmark |
| **Known issues** | "Any stages you already suspect are underperforming?" | Unknown |

**GATE: Confirm brief and data before proceeding.**

---

## Phase 2: Map

### Funnel Visualization

Build a stage-by-stage funnel with:
- **Volume** at each stage (absolute numbers)
- **Conversion rate** between each stage
- **Drop-off rate** at each stage (inverse of conversion)
- **Cumulative conversion** from top to bottom

### Benchmark Comparison

Provide relevant benchmarks per stage:

| Funnel Type | Stage | Typical Conversion |
|-------------|-------|-------------------|
| Website lead gen | Visit → Lead | 2-5% |
| SaaS | Signup → Trial active | 40-60% |
| SaaS | Trial → Paid | 15-25% |
| E-commerce | Visit → Add to cart | 8-12% |
| E-commerce | Cart → Purchase | 40-65% |

**GATE: Present the funnel map and confirm accuracy before analyzing.**

---

## Phase 3: Analyze

### Deliverables

**1. Funnel Performance Report**
- Stage-by-stage conversion and drop-off rates
- Comparison to benchmarks: above, at, or below industry
- The "biggest leak" — the stage with the highest absolute opportunity

**2. Drop-Off Diagnosis**
For each underperforming stage, diagnose likely causes:
- **Visit → Lead:** Weak CTA, unclear value proposition, slow load time
- **Lead → Qualified:** Poor targeting, mismatched expectations, no nurture
- **Qualified → Close:** Pricing friction, lack of urgency, competitor strength
- Provide 3-5 hypotheses per underperforming stage

**3. Optimization Priority Matrix**
| Stage | Drop-Off Rate | Potential Uplift | Effort | Priority |
|-------|--------------|-----------------|--------|----------|
| Cart → Checkout | 65% | High | Low | 1 |
| Visit → Signup | 97% | Medium | Medium | 2 |

**4. Action Plan**
- Top 3 fixes ranked by impact-to-effort ratio
- Specific recommendations for each fix
- Measurement plan: how to verify the fix worked

---

## Phase 4: Polish

### Monitoring Dashboard Spec

Recommend a simple funnel dashboard with:
- Weekly stage-by-stage conversion rates
- Trend lines to spot degradation early
- Alert thresholds for each stage

### Review Cadence

- Weekly: quick funnel health check
- Monthly: full analysis with segment overlays
- Quarterly: funnel redesign review — are the stages still correct?

---

## Example 1: SaaS Free Trial Funnel

**Stages:** Website Visit → Signup → Trial Active → Feature Activated → Paid
**Key finding:** 70% drop-off between Signup and Trial Active — onboarding is broken
**Top fix:** Reduce signup-to-value time with guided onboarding flow

## Example 2: E-commerce Purchase Funnel

**Stages:** Visit → Product View → Add to Cart → Checkout → Purchase
**Key finding:** 55% cart abandonment — above benchmark of 35%
**Top fix:** Add trust badges, simplify checkout, implement cart abandonment email

---

## Anti-Patterns

- **Optimizing the top when the bottom leaks** — doubling traffic to a broken checkout page doubles frustration, not revenue. Fix the bottom first.
- **Ignoring absolute numbers** — a 50% conversion rate on 10 visitors is 5 customers. Sometimes the problem is volume, not rate.
- **Single-metric obsession** — overall conversion rate masks stage-specific problems. Always break down by stage.
- **Benchmarking without context** — a 1% website conversion rate might be excellent for luxury goods and terrible for a free tool. Use relevant benchmarks.
- **Analyzing without segmenting** — mobile vs. desktop, new vs. returning, and channel-specific funnels often tell very different stories.

---

## Recovery

- **No funnel data available:** Help define the stages and set up basic tracking. Provide a 30-day data collection plan before analysis.
- **Funnel stages unclear:** Map the customer journey from their perspective, not the internal process. Ask "What does the customer DO at each step?"
- **Everything looks bad:** Prioritize ruthlessly. Pick the one stage with the highest absolute impact and start there.
- **User wants to redesign the whole funnel:** Optimize the existing funnel first. Redesign only after quick wins are exhausted.
