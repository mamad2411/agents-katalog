---
name: moat-analysis
description: >
  This skill should be used when the user asks about economic moats, competitive moats, moat durability,
  switching costs, network effects, cost advantages, intangible assets, brand moats, pricing power,
  ROIC vs WACC, sustainable competitive advantages, or efficient scale for a publicly traded company.
---

# Economic Moat Analysis

## Purpose

Evaluate the durability and strength of a company's competitive advantages using the Morningstar economic moat framework. Identify which moat sources apply, quantify their strength through financial signals such as sustained ROIC above WACC and margin stability, and assess whether the moat is widening, stable, or narrowing. Deliver a structured moat rating (Wide, Narrow, or None) supported by both qualitative and quantitative evidence.

## Data Fetching Process

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/data-sources.md` for full data-fetching instructions, ticker resolution, and fallback behavior.

### Step 1 — Resolve Ticker and Retrieve Financial History

1. Resolve the company ticker to a CIK via the SEC company tickers JSON endpoint.
2. Fetch the XBRL companyfacts JSON for the resolved CIK.
3. Extract the following metrics for the most recent 10 fiscal years (or as many as available):
   - Return on Invested Capital (ROIC): compute from `OperatingIncomeLoss`, `IncomeTaxExpenseBenefit`, `Assets`, `CashAndCashEquivalentsAtCarryingValue`, and current liabilities, or use the pre-computed ratio from Stock Analysis `/ratios/` as a fallback.
   - Gross margin: `GrossProfit` divided by `Revenues`.
   - Operating margin: `OperatingIncomeLoss` divided by `Revenues`.
   - Revenue growth rate year over year.
   - Market share proxy: revenue relative to industry peers (use the XBRL frames endpoint for the same NAICS/SIC sector if available).

### Step 2 — Estimate Weighted Average Cost of Capital (WACC)

1. Fetch the company's long-term debt (`LongTermDebt`) and stockholders' equity (`StockholdersEquity`) from EDGAR.
2. Fetch the current risk-free rate and equity risk premium via WebSearch (search for "current US 10-year Treasury yield" and "Damodaran equity risk premium").
3. Estimate beta from Stock Analysis or Gurufocus. If beta is unavailable, use the sector median beta as a proxy and note the assumption.
4. Estimate the pre-tax cost of debt from interest expense divided by average total debt, or from the company's credit rating spread over Treasuries if available.
5. Compute WACC using the standard formula: WACC = (E/V) * Re + (D/V) * Rd * (1 - Tax Rate), where Re = Rf + Beta * ERP. Use market values for equity (market cap) and book values for debt unless market debt data is readily available.
6. If precise inputs are unavailable, use a reasonable sector-average WACC estimate and note the assumption. Common sector WACC ranges: technology 8-12%, consumer staples 6-9%, utilities 5-7%, financials 8-11%.

### Step 3 — Gather Qualitative Moat Evidence

1. Use WebSearch to find recent moat analyses, brand strength rankings, patent portfolios, and regulatory licenses for the company.
2. Search for switching cost evidence: customer retention rates, contract lengths, integration depth, proprietary ecosystems.
3. Search for network effect indicators: user growth metrics, platform dynamics, marketplace liquidity.
4. Search for cost advantage evidence: scale economics, proprietary processes, location advantages, resource access.
5. Search for efficient scale indicators: natural monopoly characteristics, limited market size relative to incumbents.

## Analysis Steps

### Step 1 — Identify Applicable Moat Sources

Evaluate each of the five Morningstar moat sources and determine which ones apply to the company. For each source, provide specific evidence:

**Intangible Assets**
- Assess brand strength: pricing premium over competitors, brand recognition surveys, brand value rankings (e.g., Interbrand, Brand Finance). Quantify the premium by comparing average selling prices to commodity alternatives in the same category.
- Review patent portfolio: number of active patents, patent citation rates, remaining patent life for key products. Determine whether patents protect core revenue streams or are peripheral.
- Identify regulatory licenses or approvals: FDA approvals, banking charters, spectrum licenses, government contracts with high barriers to recompete. Evaluate how long these licenses take to obtain and whether they are exclusive or limited in number.
- Assess the combined strength of intangible assets: a brand alone may not constitute a moat unless it translates to measurable pricing power; patents must be enforceable and difficult to design around; licenses must create meaningful barriers.

**Switching Costs**
- Identify integration depth: how deeply the product embeds into customer workflows, data, or infrastructure. Enterprise software, ERP systems, and data platforms typically have the highest switching costs.
- Evaluate contract structures: long-term agreements, auto-renewal terms, early termination penalties. Note the average contract length and renewal rate if disclosed.
- Assess retraining costs: time and expense required for customers to switch to a competing product. Consider certification programs, proprietary skill requirements, and ecosystem lock-in.
- Look for evidence in customer retention rates and net revenue retention (especially for SaaS companies). NRR above 120% strongly indicates switching cost moat combined with expansion revenue.
- Evaluate data lock-in: whether customers accumulate proprietary data, history, or configurations within the product that would be costly or impossible to migrate.

**Network Effects**
- Classify the type: direct (user-to-user value, e.g., social networks, messaging), indirect (platform/marketplace, e.g., app stores, payment networks), or data network effects (more users improve the product via data, e.g., search engines, recommendation systems).
- Evaluate strength: user base size relative to competitors, engagement metrics, cross-side adoption rates. Determine whether the network effect has reached critical mass or is still building.
- Assess vulnerability: potential for multi-homing (users active on multiple competing platforms), winner-take-all dynamics versus coexistence, local versus global network effects. Local network effects (e.g., ride-sharing in a city) are more vulnerable than global ones.
- Consider whether the network effect creates a virtuous cycle: more users attract more supply, which attracts more users, creating compounding advantage.

**Cost Advantages**
- Process-driven: proprietary manufacturing, technology, or distribution that lowers unit cost.
- Scale-driven: fixed cost leverage, purchasing power, distribution network density.
- Resource-driven: preferential access to raw materials, talent pools, or geographic locations.
- Compare gross margins and operating margins against the peer group over multiple years.

**Efficient Scale**
- Evaluate whether the addressable market is limited enough that it naturally supports only a few profitable competitors. Calculate the ratio of minimum efficient scale to total market demand.
- Look for examples: utilities, railroads, pipelines, defense primes, niche industrial markets, specialized testing and certification services.
- Assess whether new entry would destroy returns for all participants, making entry economically irrational even absent any other barrier.
- Distinguish efficient scale from other moat sources: the moat arises from the market's limited size, not from the incumbent's cost advantages or brand strength.

### Step 2 — Quantify Moat Strength with Financial Signals

Present a multi-year table of quantitative moat signals:

| Signal | What It Indicates | Threshold for Moat Evidence |
|--------|-------------------|-----------------------------|
| ROIC minus WACC spread | Excess returns sustainability | Positive spread for 5+ consecutive years |
| Gross margin trend | Pricing power and cost control | Stable or expanding over 5+ years |
| Operating margin trend | Operational moat leverage | Stable or expanding over 5+ years |
| Revenue growth consistency | Demand durability | Positive in most years, low volatility |
| Market share trend | Competitive position trajectory | Stable or growing |
| Customer retention / NRR | Switching cost strength | Above 90% retention or 100%+ NRR |

For each signal, present the actual data in a table covering the most recent 5-10 years, then note whether it supports or contradicts moat existence.

### Step 3 — Assess Moat Trajectory

Determine whether the moat is widening, stable, or narrowing:

- **Widening:** ROIC-WACC spread increasing, margins expanding, market share growing, new moat sources emerging.
- **Stable:** Consistent excess returns, steady margins, maintained market share.
- **Narrowing:** ROIC-WACC spread compressing, margin erosion, market share loss, competitive disruption emerging.

Identify specific threats to the moat: technological disruption, regulatory changes, new entrants with different business models, customer preference shifts, commoditization of previously differentiated features, and erosion of switching costs through interoperability standards or open-source alternatives.

Consider the historical persistence of each moat source. Some moat types are inherently more durable than others: switching costs in mission-critical enterprise software tend to persist for decades, while brand moats in consumer goods can erode within a few years if quality or relevance slips. Network effects can flip rapidly if a superior platform achieves critical mass.

### Step 4 — Assign Moat Rating

Assign one of three ratings with a confidence level:

- **Wide Moat:** Multiple strong moat sources, ROIC well above WACC for 10+ years, high confidence moat will persist for 20+ years.
- **Narrow Moat:** One or two moat sources, ROIC above WACC for 5+ years, confidence moat will persist for 10+ years.
- **No Moat:** No durable competitive advantages, ROIC near or below WACC, competitive position eroding.

Provide the rating, a confidence level (High / Medium / Low), and a 2-3 sentence justification.

When assigning confidence, consider data availability and analytical certainty. High confidence requires strong quantitative support (long ROIC track record, clear margin trends) combined with identifiable qualitative moat sources. Medium confidence reflects either limited data history or mixed signals across moat indicators. Low confidence indicates that the assessment is based primarily on qualitative judgment due to insufficient quantitative data or a company in rapid transition.

### Step 5 — Peer Moat Comparison

When detailed depth is requested, compare the target company's moat characteristics against its 2-3 closest peers:

- Present a side-by-side table of ROIC, ROIC-WACC spread, gross margin, and operating margin for the target and each peer over the most recent 5 years.
- Note which peers have wider, narrower, or equivalent moats and identify the primary differentiating factor.
- Assess whether the industry structure supports multiple wide-moat companies (e.g., Visa and Mastercard in payments) or only one dominant moat holder.

## Depth Handling

- **Summary depth (default):** List applicable moat sources with one sentence each, show a compact ROIC vs WACC table (3-5 years), state the moat rating and trajectory in one paragraph.
- **Detailed depth:** Full analysis of all five moat sources with evidence, 10-year quantitative signal tables, moat trajectory analysis with threat assessment, peer comparison of excess returns, and complete rating justification.
- **Specific question:** If the user asks about a single moat source (e.g., "Does AAPL have switching costs?"), focus the analysis on that source with supporting data.

## Output Formatting

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md` for standard output structure, table formatting, source citations, and the required disclaimer.

Present the moat rating prominently near the top of the response after the header. Use tables for quantitative signals and concise narrative for qualitative evidence. Always cite the source for each data point (EDGAR filing, Stock Analysis page, or search result).
