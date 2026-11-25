---
title: Commercial Counterparty Risk Assessment
description: Assess counterparty risk from financial health, market position, performance history, and credit ratings
version: 1.0
frequency_percent: 50.0
success_rate_percent: 85.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/00250-commercial/commercial-counterparty-risk-assessment
gigabrain_tags: disciplines, 00250-commercial, commercial-counterparty-risk-assessment, financial-analysis
openstinger_context: counterparty-analysis, financial-risk
last_updated: 2026-04-01
related_docs:
  - docs_construct_ai/disciplines/00250-commercial/agent-data/domain-knowledge/00250_DOMAIN-KNOWLEDGE.MD
related_skills:
  - commercial-risk-assessment
  - commercial-supplier-evaluation
---

# Commercial Counterparty Risk Assessment

## Overview

Assess counterparty risk by analyzing financial health, market position, performance history, and credit ratings to determine the likelihood of counterparty failure.

**Announce at start:** "I'm using the commercial-counterparty-risk-assessment skill to assess counterparty risk."

## When to Use This Skill

**Trigger Conditions:**
- New counterparty being considered for contract
- Annual counterparty review required
- Counterparty showing signs of distress
- Major contract value requiring updated assessment

**Prerequisites:**
- Counterparty identity confirmed
- Financial statements available
- Performance history available

## Step-by-Step Procedure

### Step 1: Gather Counterparty Data

1. Financial statements (balance sheet, income statement, cash flow)
2. Credit rating from rating agencies
3. Market position and competitive analysis
4. Performance history on previous contracts
5. Outstanding litigation or claims

### Step 2: Financial Analysis

1. Calculate key ratios (liquidity, leverage, profitability)
2. Compare ratios to industry benchmarks
3. Analyze cash flow trends (positive/negative, stability)
4. Check for signs of financial distress (negative equity, declining revenue, cash burn)
5. Rate financial health (strong/moderate/weak)

### Step 3: Market Position Analysis

1. Assess market position (leader/challenger/niche/declining)
2. Analyze market conditions affecting counterparty
3. Review regulatory or competitive threats
4. Rate market position stability

### Step 4: Performance History Review

1. Review past contract performance (on-time, quality, disputes)
2. Check for any insolvency or restructuring events
3. Rate performance reliability

### Step 5: Calculate Risk Score

Combine financial, market, and performance ratings into composite risk score:
- Strong financial + stable market + reliable performance = Low Risk
- Moderate across all = Medium Risk
- Weak financial + declining market = High Risk
- Signs of distress = Critical Risk

### Step 6: Recommend Mitigation

For medium or higher risk:
- Require performance bond or guarantee
- Reduce contract value or duration
- Increase monitoring frequency
- Identify backup counterparty

## Success Criteria

- [ ] Financial statements analyzed
- [ ] Key ratios calculated and compared to benchmarks
- [ ] Market position assessed
- [ ] Performance history reviewed
- [ ] Composite risk score calculated
- [ ] Risk mitigation recommended for medium+ risks

## Common Pitfalls

1. **Outdated Financials** — Financial data older than 12 months may not reflect current status. Request most recent.
2. **Ignoring Market Signals** — Financials may lag market conditions. Check for recent negative market events.

## Cross-References
### Related Skills
- `commercial-risk-assessment` — Risk scoring and register entry
- `commercial-supplier-evaluation` — Supplier qualification
### Related Agents
- `COM-011` Commercial Risk Register Agent — Primary agent
- `COM-003` Commercial Procurement Specialist Agent — Supporting agent
