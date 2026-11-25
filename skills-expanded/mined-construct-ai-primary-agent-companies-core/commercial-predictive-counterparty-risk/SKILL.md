---
title: Commercial Predictive Counterparty Risk
description: Predict counterparty risk from historical payment patterns, market indicators, and performance data using predictive analytics
version: 1.0
frequency_percent: 20.0
success_rate_percent: 80.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/00250-commercial/commercial-predictive-counterparty-risk
gigabrain_tags: disciplines, 00250-commercial, commercial-predictive-counterparty-risk, predictive-analytics, risk-forecasting
openstinger_context: risk-prediction, counterparty-early-warning
last_updated: 2026-04-01
related_docs:
  - docs_construct_ai/disciplines/00250-commercial/agent-data/domain-knowledge/00250_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/00250-commercial/agent-data/prompts/00250_AI-NATIVE-COMMERCIAL-PROMPT.md
related_skills:
  - commercial-counterparty-risk-assessment
  - commercial-market-intelligence
---

# Commercial Predictive Counterparty Risk

## Overview
Predict counterparty failure risk by analyzing historical payment patterns, market indicators, performance data, and financial trends using predictive analytics and machine learning models.
**Announce at start:** "I'm using the commercial-predictive-counterparty-risk skill to predict counterparty risk."

## When to Use This Skill
**Trigger Conditions:** Periodic risk forecast update, early warning triggered, new counterparty onboarded, market disruption detected
**Prerequisites:** Historical counterparty data available, market indicators accessible

## Step-by-Step Procedure
### Step 1: Gather Historical Data
1. Extract historical payment records (on-time, late, disputed, unpaid)
2. Gather market indicator data (credit spreads, CDS prices, stock performance)
3. Compile performance history (quality, delays, disputes)
4. Collect financial filing data

### Step 2: Analyze Payment Patterns
1. Calculate payment timeliness trends (improving/worsening)
2. Identify payment pattern anomalies (sudden delays, partial payments)
3. Calculate payment velocity trend

### Step 3: Assess Market Indicators
1. Analyze credit rating changes (upgrades/downgrades)
2. Monitor CDS spread widening
3. Check for negative news events
4. Analyze sector-wide stress indicators

### Step 4: Apply Predictive Model
1. Feed inputs into predictive risk model
2. Calculate failure probability score
3. Generate risk forecast horizon
4. Calculate confidence level

### Step 5: Generate Risk Forecast Report
1. Risk score and trend
2. Early warning alerts
3. Confidence intervals
4. Recommend early intervention

## Success Criteria
- [ ] Historical data gathered from all sources
- [ ] Payment patterns analyzed for trends
- [ ] Market indicators assessed
- [ ] Predictive model applied with confidence level
- [ ] Risk forecast report generated with recommendations

## Common Pitfalls
1. **Small Dataset** — Insufficient historical data reduces prediction accuracy. Flag low confidence when data is sparse.
2. **Black Swan Events** — Unpredictable events (pandemic, war) may not be captured in historical patterns. Note model limitations.

## Cross-References
### Related Skills
- `commercial-counterparty-risk-assessment` — Fundamental counterparty risk assessment
- `commercial-market-intelligence` — Market indicator input
### Related Agents
- `COM-004` Commercial Market Intelligence Agent — Primary agent
- `COM-011` Commercial Risk Register Agent — Supporting agent