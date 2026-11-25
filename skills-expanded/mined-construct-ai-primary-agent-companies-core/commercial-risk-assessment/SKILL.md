---
title: Commercial Risk Assessment
description: Identify, classify, and score commercial risks with mitigation strategy generation and risk register integration
version: 1.0
frequency_percent: 60.0
success_rate_percent: 88.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/00250-commercial/commercial-risk-assessment
gigabrain_tags: disciplines, 00250-commercial, commercial-risk-assessment, risk-management
openstinger_context: risk-identification, risk-mitigation
last_updated: 2026-04-01
related_docs:
  - docs_construct_ai/disciplines/00250-commercial/agent-data/domain-knowledge/00250_DOMAIN-KNOWLEDGE.MD
related_skills:
  - commercial-risk-register-management
  - commercial-counterparty-risk-assessment
---

# Commercial Risk Assessment

## Overview

Identify, classify, and score commercial risks (pricing, counterparty, contractual, market), generate mitigation strategies, and integrate with the risk register system.

**Announce at start:** "I'm using the commercial-risk-assessment skill to assess commercial risks."

## When to Use This Skill

**Trigger Conditions:**
- New contract or project phase requiring risk assessment
- Major commercial change (price changes, supplier failure)
- Periodic risk review required
- Project milestone requiring risk update

**Prerequisites:**
- Project scope and context available
- Contract terms understood
- Budget and schedule baseline available

## Step-by-Step Procedure

### Step 1: Risk Identification

Identify risks across categories:

| Risk Category | Examples |
|---------------|----------|
| Pricing Risk | Inaccurate estimates, market volatility, currency fluctuation |
| Counterparty Risk | Client insolvency, subcontractor default, supplier underperformance |
| Contractual Risk | Onerous terms, unclear scope, ambiguous specifications |
| Market Risk | Commodity price changes, supply shortage, regulatory changes |
| Performance Risk | Failure to meet specifications, delays, quality defects |
| Force Majeure | Natural disasters, war, pandemic, government action |

### Step 2: Risk Scoring

For each identified risk:
1. **Likelihood:** Rate 1-5 (Rare to Almost Certain)
2. **Impact:** Rate 1-5 (Insignificant to Catastrophic)
3. **Risk Score:** Likelihood × Impact
4. **Risk Rating:** Low (1-6), Medium (8-12), High (15-19), Critical (20-25)

### Step 3: Mitigation Strategy

For each risk:
1. Identify mitigation options (avoid, reduce, transfer, accept)
2. Select preferred mitigation(s)
3. Assign mitigation owner
4. Set mitigation target date
5. Calculate residual risk after mitigation

### Step 4: Risk Register Update

Update risk register with:
- Risk ID, description, category
- Likelihood, impact, score, rating
- Mitigation strategy and owner
- Target date
- Residual risk assessment

### Step 5: Risk Report

Generate risk summary report:
- Top 10 risks by score
- Risk heatmap summary
- Mitigation status overview
- Emerging risk alerts
- Trend analysis

## Success Criteria

- [ ] All risk categories assessed
- [ ] Each risk scored (likelihood × impact)
- [ ] Mitigation strategy defined for high and critical risks
- [ ] Risk owner assigned
- [ ] Risk register updated
- [ ] Summary report generated

## Common Pitfalls

1. **Generic Risks** — Avoid "weather delays" or "unforeseen conditions". Be specific to the contract and project.
2. **No Mitigation Owner** — Without an owner, mitigation doesn't happen. Always assign ownership.
3. **Underestimating Likelihood** — Don't be optimistic for comfort. Use historical data to assess likelihood.

## Cross-References

### Related Skills
- `commercial-risk-register-management` — Risk register maintenance
- `commercial-counterparty-risk-assessment` — Counterparty risk analysis

### Related Agents
- `COM-011` Commercial Risk Register Agent — Primary agent
- `COM-001` Commercial Coordinator Agent — Supporting agent