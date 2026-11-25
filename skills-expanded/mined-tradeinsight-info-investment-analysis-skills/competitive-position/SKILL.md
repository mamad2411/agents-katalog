---
name: competitive-position
description: >
  This skill should be used when the user asks about competitive advantages, market position,
  Porter's Five Forces, competitive landscape, market share, industry competition, barriers to entry,
  threat of substitutes, competitive analysis, or industry structure for a publicly traded company.
---

# Competitive Position Analysis

## Purpose

Assess a company's current competitive position within its industry using Porter's Five Forces framework and market share analysis. Map the industry structure, evaluate competitive dynamics, and determine how the company is positioned relative to peers. This skill focuses on the present-day competitive landscape and industry dynamics, distinguishing it from moat analysis which evaluates the durability of advantages over time.

## Data Fetching Process

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/data-sources.md` for full data-fetching instructions, ticker resolution, and fallback behavior.

### Step 1 — Resolve Ticker and Identify Industry Context

1. Resolve the company ticker to a CIK via the SEC company tickers JSON endpoint.
2. Fetch the XBRL companyfacts JSON for the resolved CIK to obtain the SIC code and basic financials.
3. Identify the company's primary industry, sub-sector, and GICS classification using WebSearch if necessary.
4. Note the company's revenue scale and geographic footprint for context.

### Step 2 — Gather Industry and Competitor Data

1. Fetch the company's financial summary from Stock Analysis (`/financials/` and `/financials/ratios/`) to establish baseline metrics including revenue, gross margin, operating margin, and revenue growth over the past 3-5 years.
2. Use WebSearch to identify the top 3-5 direct competitors by revenue in the same industry segment. Search for "{industry} market share" and "{industry} top companies by revenue" to find reliable rankings.
3. For each major competitor, fetch key financial metrics from Stock Analysis for peer comparison: revenue, operating margin, market capitalization, revenue growth, R&D spending as a percentage of revenue, and capital expenditure intensity.
4. Use WebSearch to gather recent industry reports, market size estimates, growth projections, and competitive dynamics commentary. Prioritize reports from industry associations, consulting firms, and financial research providers.
5. Search for industry concentration data (e.g., Herfindahl-Hirschman Index estimates, top-4 or top-10 market share). If formal HHI data is unavailable, estimate concentration from the revenue shares of the top players.

### Step 3 — Gather Regulatory and Disruption Context

1. Use WebSearch to identify current and pending regulatory changes affecting the industry.
2. Search for recent entrants, disruptive technologies, or business model innovations in the space.
3. Search for recent M&A activity that may signal consolidation or competitive shifts.
4. Identify any pending litigation, antitrust actions, or trade policy changes relevant to the competitive landscape.

## Analysis Steps

### Step 1 — Map the Industry Structure

Provide a concise industry overview covering:

- **Industry definition and scope:** What products or services define this industry, and how is it segmented.
- **Market size and growth:** Total addressable market, historical growth rate, projected growth.
- **Industry lifecycle stage:** Emerging, growth, mature, or declining.
- **Concentration level:** Fragmented, moderately concentrated, or oligopolistic. List the top competitors and approximate market shares.
- **Capital intensity:** Level of capital investment required to compete effectively.
- **Regulatory environment:** Key regulations, licensing requirements, and compliance costs.

### Step 2 — Apply Porter's Five Forces

Evaluate each of the five forces on a scale of Low / Medium / High intensity, with specific evidence:

**Threat of New Entrants**
- Assess capital requirements for entry: initial investment, minimum efficient scale, and time to breakeven for a new entrant.
- Evaluate regulatory and licensing barriers: permits, certifications, compliance costs, and the time required to obtain approvals.
- Examine brand loyalty and customer switching behavior among incumbents. Consider whether customers exhibit inertia or actively evaluate alternatives.
- Identify technology or know-how barriers: proprietary technology, patents, learning curve, and the availability of skilled talent in the market.
- Consider access to distribution channels and supplier relationships. Evaluate whether incumbents have exclusive arrangements that lock out new entrants.
- Assess the track record of recent entry attempts: have new entrants succeeded or failed in the past 5 years, and what factors determined the outcome.
- Rate the overall threat level and explain the reasoning.

**Bargaining Power of Suppliers**
- Identify key input categories and the concentration of suppliers in each.
- Assess the availability of substitute inputs and the cost of switching suppliers.
- Evaluate whether suppliers pose a credible forward-integration threat.
- Determine how critical specific inputs are to the final product or service quality.
- Rate the overall supplier power and explain the reasoning.

**Bargaining Power of Buyers**
- Assess buyer concentration: how many customers account for what share of revenue.
- Evaluate price sensitivity: is the product a commodity or differentiated offering.
- Determine switching costs from the buyer's perspective.
- Assess the availability of substitute products or services.
- Evaluate whether buyers pose a credible backward-integration threat.
- Rate the overall buyer power and explain the reasoning.

**Threat of Substitutes**
- Identify potential substitutes from adjacent industries or emerging technologies.
- Evaluate the price-performance trade-off of substitutes versus the industry's offering.
- Assess the propensity of buyers to switch to substitutes.
- Consider whether substitutes are improving in quality or declining in cost over time.
- Rate the overall substitute threat and explain the reasoning.

**Competitive Rivalry**
- Assess the number and relative size of competitors. A few equally sized players often creates more intense rivalry than one dominant leader with smaller followers.
- Evaluate industry growth rate relative to capacity: slow growth increases rivalry as firms compete for a fixed pie.
- Determine the level of product differentiation or commoditization. Highly commoditized products lead to price-based competition.
- Examine exit barriers: specialized assets, strategic importance, emotional attachment, labor agreements, and government restrictions on closure.
- Review recent pricing behavior: price wars, discounting trends, margin compression across the industry over the past 3-5 years.
- Assess the role of innovation cycles: industries with rapid product cycles may see rivalry intensify during technology transitions.
- Rate the overall rivalry intensity and explain the reasoning.

Present the Five Forces summary in a table:

| Force | Intensity | Key Drivers |
|-------|-----------|-------------|
| Threat of New Entrants | Low/Medium/High | [Top 2-3 factors] |
| Supplier Power | Low/Medium/High | [Top 2-3 factors] |
| Buyer Power | Low/Medium/High | [Top 2-3 factors] |
| Threat of Substitutes | Low/Medium/High | [Top 2-3 factors] |
| Competitive Rivalry | Low/Medium/High | [Top 2-3 factors] |

### Step 3 — Assess the Company's Competitive Position

Evaluate how the target company is positioned within this industry structure:

- **Market share and trend:** Current estimated market share and whether it is growing, stable, or declining over the past 3-5 years.
- **Competitive strategy:** Cost leadership, differentiation, or focus/niche. Provide evidence from pricing, margins, and product positioning.
- **Revenue growth vs industry:** Compare the company's revenue growth rate against the overall industry growth rate to assess share gain or loss.
- **Margin comparison:** Compare gross and operating margins against the top 3-5 peers to gauge relative efficiency and pricing power.
- **Competitive response capability:** Assess the company's ability to respond to competitive threats based on balance sheet strength (cash reserves, debt capacity), R&D investment intensity, marketing spend, and management track record in responding to past competitive challenges.
- **Value chain position:** Identify where the company sits in the industry value chain and whether it captures a disproportionate share of industry profits. Some positions (e.g., platform operators, standards setters) capture more value than others (e.g., commodity component suppliers).
- **Innovation posture:** Evaluate whether the company is an innovation leader or fast follower. Compare R&D spending as a percentage of revenue against peers and assess the track record of translating R&D into commercially successful products or services.

Present a peer comparison table:

| Company | Revenue ($B) | Market Share (est.) | Gross Margin | Op. Margin | Rev. Growth (3Y CAGR) |
|---------|-------------|---------------------|--------------|------------|----------------------|
| [Target] | ... | ... | ... | ... | ... |
| [Peer 1] | ... | ... | ... | ... | ... |
| [Peer 2] | ... | ... | ... | ... | ... |

### Step 4 — Identify Competitive Risks and Opportunities

- **Disruption risk:** Emerging technologies, business model innovations, or new entrants that could reshape the industry within 3-5 years. Assess whether the target company is positioned to benefit from or be harmed by these disruptions.
- **Consolidation potential:** Whether M&A activity is likely to change the competitive landscape. Identify potential acquirers and targets, and assess whether consolidation would strengthen or weaken the target company's position.
- **Regulatory shifts:** Upcoming regulations that could advantage or disadvantage specific competitors. Consider antitrust scrutiny, environmental regulations, data privacy rules, and sector-specific policy changes.
- **Geographic expansion:** Opportunities or threats from international competitors entering the company's markets, or the company's ability to expand into new geographic regions.
- **Technology platform shifts:** Assess whether shifts in underlying technology platforms (cloud computing, AI, mobile, electrification) could alter competitive dynamics and whether the company is investing appropriately in these transitions.
- **Talent competition:** In knowledge-intensive industries, evaluate whether the company can attract and retain top talent relative to competitors, as this can be a leading indicator of future competitive position.

Summarize with an overall competitive position assessment: Strong, Moderate, or Weak, with a brief justification that ties back to the Five Forces analysis and peer comparison.

## Depth Handling

- **Summary depth (default):** Five Forces summary table, a compact peer comparison table (3-4 peers), and a one-paragraph competitive position assessment.
- **Detailed depth:** Full industry structure overview, detailed Five Forces analysis with evidence for each factor, comprehensive peer comparison with multi-year data, and a thorough risk/opportunity assessment.
- **Specific question:** If the user asks about a single force or aspect (e.g., "What are the barriers to entry in AAPL's industry?"), focus the analysis on that specific element with supporting data.

## Output Formatting

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md` for standard output structure, table formatting, source citations, and the required disclaimer.

Lead with the Five Forces summary table for quick orientation, followed by the peer comparison. Use narrative sections for qualitative assessments of each force. Always cite the source for market share estimates, industry data, and financial comparisons.
