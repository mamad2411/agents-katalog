---
title: Commercial Cash Flow Prediction
description: Contract milestone scheduling analysis, payment term evaluation, and cash flow forecasting with shortfall identification
version: 1.0
frequency_percent: 20.0
success_rate_percent: 85.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/00250-commercial/commercial-cash-flow-prediction
gigabrain_tags: disciplines, 00250-commercial, commercial-cash-flow-prediction, cash-flow-management, predictive-analytics
openstinger_context: cash-flow-forecasting, payment-timing
last_updated: 2026-04-01
related_docs:
  - docs_construct_ai/disciplines/00250-commercial/agent-data/domain-knowledge/00250_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/00250-commercial/agent-data/prompts/00250_AI-NATIVE-COMMERCIAL-PROMPT.md
related_skills:
  - commercial-cost-escalation-forecasting
  - commercial-milestone-billing
---

# Commercial Cash Flow Prediction

## Overview
Analyze contract milestone schedules, payment terms, and billing cycles to forecast cash inflows and outflows, identify potential shortfalls, and recommend timing adjustments.
**Announce at start:** "I'm using the commercial-cash-flow-prediction skill to forecast cash flow."

## When to Use This Skill
**Trigger Conditions:** Monthly cash flow review required, major contract milestone approaching, payment cycle optimization needed, potential shortfall identified
**Prerequisites:** Milestone schedule available, payment terms defined, billing application process understood

## Step-by-Step Procedure
### Step 1: Gather Milestone Schedule
1. Extract project milestone schedule from contract
2. Identify expected completion dates for each milestone
3. Identify payment terms and periods for each milestone

### Step 2: Analyze Payment Terms
1. Calculate payment cycle time (application to payment)
2. Identify payment delays (dispute, incomplete documentation, processing)
3. Apply historical payment performance data
4. Calculate expected payment timeline for each milestone

### Step 3: Model Cash Inflows and Outflows
1. Model scheduled milestone payments as cash inflows
2. Model costs as cash outflows
3. Calculate net cash flow per period
4. Apply payment delay factors to realistic inflow timing

### Step 4: Generate Cash Flow Forecast
1. Generate monthly cash flow forecast for project duration
2. Identify potential shortfalls and surpluses
3. Calculate cash flow timing risk
4. Apply sensitivity analysis for schedule delays and payment delays

### Step 5: Recommend Timing Adjustments
1. Identify milestone acceleration opportunities
2. Recommend billing application optimization
3. Suggest payment term negotiations
4. Identify cash flow timing risk mitigation strategies

### Step 6: Produce Cash Flow Report
1. Forecast with monthly detail
2. Shortfall identification and timing
3. Sensitivity analysis results
4. Recommendations for optimization

## Success Criteria
- [ ] Milestone schedule analyzed with payment terms
- [ ] Cash inflows and outflows modeled
- [ ] Cash flow forecast generated for project duration
- [ ] Potential shortfalls identified with timing
- [ ] Timing adjustment recommendations provided

## Common Pitfalls
1. **Over-Optimistic Milestone Timing** — Don't assume best-case milestone completion. Apply realistic delay factors.
2. **Ignoring Payment Delay History** — If the paying party has a history of late payments, factor this into the forecast.

## Cross-References
### Related Skills
- `commercial-cost-escalation-forecasting` — Cost escalation impact on cash flow
- `commercial-milestone-billing` — Milestone billing process
### Related Agents
- `COM-014` Commercial Cash Flow & Forecasting Agent — Primary agent