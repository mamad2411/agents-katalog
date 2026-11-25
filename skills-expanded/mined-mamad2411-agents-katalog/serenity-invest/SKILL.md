---
name: serenity-invest-skill
description: Analyze high-growth industries with supply-chain bottleneck investing. Use to map value chains, score chokepoints, validate listed companies, and build research watchlists.
license: MIT
compatibility: Agent Skills compatible. Designed for Claude Code and OpenAI Codex. Framework use is offline; current market/company facts require web or market-data tools.
metadata:
  version: "1.0.0"
  maintainer: "xiaowei"
  domain: "investment-research"
---

# Serenity Invest Skill

## Purpose

Use this skill to perform **supply-chain bottleneck investment research**. The goal is not to chase the hottest end market, but to work backward from an explosive demand trend and identify the upstream nodes that are hardest to expand, easiest to underprice, and most likely to become chokepoints when the thesis becomes real.

This skill helps the agent produce:

- Industry supply-chain maps.
- Chokepoint rankings.
- Company watchlists mapped to bottleneck nodes.
- Evidence checklists and confidence ratings.
- Risk flags, disconfirmation signals, and follow-up data requests.

The skill must **not** present outputs as guaranteed returns or personalized investment advice. It should frame results as research candidates and explicitly state uncertainty.

## When to Use

Activate this skill when the user asks about any of the following:

- "Serenity" investment style, chokepoint investing, bottleneck investing, hidden supply-chain winners, picks-and-shovels investing, or upstream constraints.
- Which industries or stocks benefit if a demand theme explodes.
- Mapping an industry from downstream demand to upstream materials, equipment, infrastructure, or certification bottlenecks.
- Screening companies under constraints such as market, price, exchange, sector, liquidity, or board listing.
- Comparing a public figure's or fund's disclosed/rumored holdings against a bottleneck-investing framework.
- Building a repeatable research process for AI, robotics, GLP-1, batteries, grid equipment, low-altitude economy, defense, space, synthetic biology, or similar high-growth themes.

Do **not** use this skill for:

- Day-trading signals, technical-analysis-only requests, or price-prediction requests without business fundamentals.
- Personalized portfolio allocation, tax advice, legal advice, or suitability analysis.
- Insider-information requests or attempts to trade on non-public material information.
- Claims that require current facts unless fresh sources are available and cited.

## Core Thesis

Serenity-style research asks seven questions in order:

1. What demand shock could grow faster than consensus expects?
2. What must physically, operationally, or legally scale for that demand to be met?
3. Which supply-chain nodes have the lowest supply elasticity?
4. Which nodes have long expansion cycles, customer qualification, high capex, low yields, or concentrated suppliers?
5. Which listed companies own those nodes?
6. Is the company's exposure large enough to change revenue, margins, or valuation?
7. What evidence would prove the thesis wrong?

Rule of thumb:

> Do not only buy the story. Look for the thing that becomes scarce if the story comes true.

## Workflow

### 1. Define the Demand Shock

Identify the demand driver and its expected time horizon.

Minimum fields:

- End market or technology trend.
- Demand driver: technology breakthrough, policy, cost curve, regulation, demographics, capex cycle, defense cycle, medical adoption, or consumer adoption.
- Time horizon: immediate, 6-18 months, 1-3 years, 3-5 years, or longer.
- Evidence quality: primary filings, official data, industry reports, credible news, or only social/market narrative.

If the request involves current market facts, prices, holdings, filings, policy, earnings, or news, use current sources before making factual claims.

### 2. Build the Supply-Chain DAG

Represent the industry as a directed acyclic graph, not merely a linear table.

Default layers:

1. End demand and applications.
2. System integrators or finished products.
3. Modules and subsystems.
4. Critical components.
5. Materials, process inputs, and test equipment.
6. Infrastructure, energy, land, water, regulatory approvals, and labor.

Keep drilling upstream until at least one of these appears:

- Material with constrained supply.
- Specialized equipment with long lead time.
- Manufacturing process with yield/qualification bottleneck.
- Certification or regulatory bottleneck.
- Infrastructure bottleneck.
- Supplier concentration or single/few-source dependency.

### 3. Score Bottleneck Nodes

Score every important node from 1 to 5 on these dimensions:

| Factor | Meaning |
|---|---|
| Demand acceleration | How fast downstream demand can grow. |
| Supply inelasticity | How hard it is to expand supply quickly. |
| Expansion lag | Time needed to add meaningful capacity. |
| Supplier concentration | Degree to which supply is controlled by few players. |
| Qualification difficulty | Customer certification, regulatory approval, or reliability hurdle. |
| Technical difficulty | Yield, precision, process complexity, or know-how barrier. |
| Pricing power | Ability to raise prices or sustain margins in shortage. |
| Capital intensity | Capex burden and financing difficulty. |

Use this normalized score:

```text
Bottleneck Pressure Score, 0-100 =
100 * (
  0.18*demand_acceleration +
  0.18*supply_inelasticity +
  0.14*expansion_lag +
  0.14*supplier_concentration +
  0.12*qualification_difficulty +
  0.10*technical_difficulty +
  0.08*pricing_power +
  0.06*capital_intensity
) / 5
```

Interpretation:

| Score | Meaning |
|---:|---|
| 85-100 | Severe chokepoint candidate. |
| 70-84 | Strong bottleneck, worth mapping to companies. |
| 55-69 | Moderate bottleneck; thesis needs more proof. |
| 40-54 | Related but likely competitive or elastic. |
| <40 | Not a bottleneck under this framework. |

### 4. Map Bottleneck Nodes to Companies

For each high-scoring node, identify companies at three levels:

| Level | Company type | Serenity relevance |
|---|---|---|
| Level 1 | Obvious leaders and end-market winners | Higher certainty, lower awareness gap. |
| Level 2 | Critical component/module suppliers | Often attractive if exposure is meaningful. |
| Level 3 | Materials, equipment, test, infrastructure, and qualification gatekeepers | Most Serenity-like if under-researched and supply-constrained. |

Do not treat a company as a candidate merely because it mentions the theme. Require a plausible revenue path.

### 5. Verify Company Exposure

For each company, verify:

- Revenue exposure: how much of revenue can plausibly come from the bottleneck node.
- Customer evidence: named customers, design wins, supply agreements, certifications, or management commentary.
- Order evidence: backlog, capacity utilization, capex, shipments, product mix, or contracted volumes.
- Margin evidence: gross margin, ASP, product mix, or operating leverage.
- Competitive evidence: alternatives, substitution risk, and ability of customers to dual-source.
- Financial quality: cash flow, leverage, dilution risk, profitability, and inventory risk.
- Market awareness: analyst coverage, market cap, volume, narrative saturation, and valuation.

Use `references/evidence-checklist.md` for a stricter evidence hierarchy.

### 6. Score Company Opportunity

After node scoring, score each company from 1 to 5:

| Factor | Meaning |
|---|---|
| Node quality | Bottleneck Pressure Score of the node it maps to. |
| Revenue exposure | Related revenue as a share of the business. |
| Evidence quality | Strength of filings, orders, customers, and product data. |
| Awareness gap | How under-recognized the market appears to be. |
| Operating leverage | Ability to convert revenue growth to profit growth. |
| Financial quality | Balance sheet, cash flow, dilution, and execution quality. |
| Liquidity fit | Whether liquidity matches the user's risk preference. |

Suggested formula:

```text
Company Opportunity Score, 0-100 =
100 * (
  0.25*node_quality_scaled_1_to_5 +
  0.20*revenue_exposure +
  0.18*evidence_quality +
  0.14*awareness_gap +
  0.10*operating_leverage +
  0.08*financial_quality +
  0.05*liquidity_fit
) / 5
- risk_penalty
```

Risk penalty is 0-25 points based on overvaluation, hype, customer concentration, weak finances, governance, regulatory risk, and lack of verifiable exposure.

### 7. Produce the Output

A complete answer should include:

1. The demand shock thesis.
2. A supply-chain map or DAG-style table.
3. Bottleneck ranking with scores and reasons.
4. Company mapping by bottleneck node.
5. Candidate segmentation: high-confidence, watchlist, speculative, exclude.
6. Evidence table and source quality.
7. Key risks and disconfirmation signals.
8. Follow-up indicators to monitor.

Use `references/output-templates.md` for tables.

## Required Research Guardrails

- If the user asks for current stocks, prices, holdings, filings, regulation, earnings, or news, verify with current sources.
- Cite primary filings, exchange disclosures, investor presentations, earnings transcripts, regulatory documents, official statistics, and reputable financial media wherever possible.
- Separate facts from inference. Label inference clearly.
- Avoid unsupported claims that a company is a supplier to a specific customer unless sourced.
- Avoid saying a stock is a buy/sell. Say "research candidate", "watchlist candidate", or "does not yet meet the evidence threshold".
- Always include a "what would disconfirm this thesis" section for investment outputs.
- For small-cap or illiquid names, warn about volatility, liquidity, promotional risk, and fragile evidence.
- If a requested screen uses a price threshold, market cap, exchange, or board filter, treat the result as date-sensitive and verify with current market data.

## Common Red Flags

Reject or downgrade candidates with these traits:

- Thematic mention only, with no meaningful revenue exposure.
- Business line too small to affect consolidated earnings.
- No customer, order, product, capacity, or margin evidence.
- A bottleneck node with many interchangeable suppliers.
- Strong theme but already fully priced by valuation and consensus.
- Social-media-driven narrative with no primary-source confirmation.
- Capex plans that create future oversupply.
- Customer concentration that creates cliff risk.
- Poor balance sheet, repeated dilution, or weak cash conversion.

## File References

Use these files only when needed:

- `references/framework.md` — detailed research process and scoring definitions.
- `references/evidence-checklist.md` — evidence hierarchy and company verification checklist.
- `references/output-templates.md` — tables for reports, screens, and watchlists.
- `references/risk-controls.md` — risk filters, disconfirmation signals, and compliance guardrails.
- `examples/ai-infrastructure-example.md` — example output for AI infrastructure.
- `examples/robotics-example.md` — example output for humanoid robotics.
- `scripts/score_bottlenecks.py` — calculate bottleneck scores from CSV.
- `scripts/score_companies.py` — calculate company opportunity scores from CSV.
- `scripts/validate_skill.py` — validate basic Agent Skills frontmatter conventions.
