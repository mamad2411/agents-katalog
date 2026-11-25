---
name: growth-analysis
description: This skill should be used when the user asks about revenue growth, earnings growth, EPS growth, growth rate, CAGR, forward estimates, growth analysis, organic growth, same-store sales growth, comps, TAM, total addressable market, or growth trajectory for a publicly traded company.
---

# Growth Analysis

## Purpose

Analyze historical and forward-looking growth metrics for a publicly traded company to assess the sustainability, quality, and trajectory of its growth. This skill computes compound annual growth rates (CAGRs) across multiple time horizons for key financial line items, decomposes growth into organic versus acquisition-driven components, and incorporates consensus forward estimates to project future growth. The output enables investors to evaluate whether a company's growth is accelerating, decelerating, or stabilizing, and whether it is driven by durable competitive advantages or transient factors.

## Data Fetching Process

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/data-sources.md` for full data-fetching instructions, ticker resolution, and fallback behavior.

### Primary Data — SEC EDGAR XBRL API

Fetch the company facts endpoint to retrieve historical financial data:

```
https://data.sec.gov/api/xbrl/companyfacts/CIK{10-digit-CIK}.json
```

Extract the following XBRL concepts for annual (FY) and quarterly (Q1-Q4) periods, sorted chronologically by `end` date:

- **Revenue:** `Revenues` or `RevenueFromContractWithCustomerExcludingAssessedTax`
- **Gross Profit:** `GrossProfit`
- **Operating Income:** `OperatingIncomeLoss`
- **Net Income:** `NetIncomeLoss`
- **Diluted EPS:** `EarningsPerShareDiluted`
- **Free Cash Flow:** Derive from `NetCashProvidedByOperatingActivities` minus `PaymentsToAcquirePropertyPlantAndEquipment`
- **Dividends Per Share:** `CommonStockDividendsPerShareDeclared`

Ensure at least 10 years of annual data are collected when available, as CAGR calculations require data across multiple time horizons.

### Secondary Data — Stock Analysis

Fetch the income statement page for pre-computed annual and quarterly figures:

```
https://stockanalysis.com/stocks/{ticker}/financials/
```

Fetch the cash flow statement for FCF components:

```
https://stockanalysis.com/stocks/{ticker}/financials/cash-flow-statement/
```

### Forward Estimates — Stock Analysis Forecast

Fetch consensus analyst estimates for forward growth projections:

```
https://stockanalysis.com/stocks/{ticker}/forecast/
```

Extract consensus revenue and EPS estimates for current quarter, next quarter, current fiscal year, next fiscal year, and any available long-term growth rate projections.

### Supplementary Context — WebSearch

Search for recent earnings call transcripts, management guidance, and investor presentations that discuss organic growth initiatives, acquisition contributions, geographic expansion plans, and total addressable market (TAM) sizing. Use queries such as:

- `"{ticker} earnings call growth guidance {current year}"`
- `"{ticker} total addressable market TAM"`
- `"{ticker} organic growth vs acquisition"`

## Analysis Steps

### Step 1 — Compute Historical CAGRs

Calculate compound annual growth rates using the formula: CAGR = (End Value / Start Value)^(1/n) - 1, where n is the number of years. Use the most recent fiscal year as the end point and count back the appropriate number of years for each horizon.

Compute CAGRs for 1-year, 3-year, 5-year, and 10-year horizons (where data permits) for each of the following metrics:

| Metric | 1yr | 3yr | 5yr | 10yr |
|--------|-----|-----|-----|------|
| Revenue | | | | |
| Gross Profit | | | | |
| Operating Income | | | | |
| Net Income | | | | |
| Diluted EPS | | | | |
| Free Cash Flow | | | | |
| Dividends/Share | | | | |

Note any negative-to-positive or positive-to-negative transitions where CAGR is mathematically undefined, and report percentage change instead with a clear annotation. When EPS growth significantly outpaces revenue growth, note whether this divergence is driven by margin expansion, share buybacks, or both — this distinction is critical for assessing the sustainability of EPS growth.

### Step 2 — Assess Growth Quality

Evaluate the composition and sustainability of growth by examining:

- **Organic vs. Acquisition-Driven:** Compare revenue growth with the timing and magnitude of acquisitions disclosed in filings or press releases. If acquisitions contributed meaningfully, estimate what organic growth would have been by subtracting acquired revenue in the first year of consolidation. Organic growth is generally valued more highly by the market because it reflects underlying business momentum rather than capital deployment. Search 10-K filings and earnings calls for management disclosures on organic versus inorganic contribution.
- **Volume vs. Price/Mix:** Where data permits (particularly for retail, consumer goods, and industrial companies), decompose revenue growth into volume growth and pricing/mix changes. Earnings calls often disclose this breakdown explicitly. Volume-driven growth is typically more sustainable, while price-driven growth may face consumer pushback or competitive pressure over time.
- **Geographic Decomposition:** Identify revenue by geographic segment if disclosed in the 10-K. Determine whether growth is concentrated in one region or diversified across markets. Highlight exposure to high-growth international markets versus mature domestic markets. Note any foreign exchange headwinds or tailwinds that distort reported growth versus constant-currency growth.
- **Segment-Level Growth:** Break down revenue and operating income growth by business segment. Identify which segments are growing fastest and which are declining. Determine whether the fastest-growing segments are also the highest-margin segments, as this combination drives outsized earnings growth. Flag any segments where growth is masking deterioration in others.

### Step 3 — Evaluate Growth Trajectory

Assess whether growth is accelerating, stable, or decelerating:

- Compare recent-period CAGRs (1yr, 3yr) against longer-term CAGRs (5yr, 10yr). If the 1yr and 3yr CAGRs are above the 5yr and 10yr CAGRs, growth is accelerating. If below, growth is decelerating.
- Examine quarterly year-over-year growth rates for the most recent 4-8 quarters to identify inflection points. Present these in a mini-table showing QoQ progression of YoY growth rates to make the trajectory visually clear.
- Flag significant deviations from the historical trend, such as pandemic-era distortions, one-time large contract wins, or divestitures that make year-over-year comparisons misleading. Normalize for these effects when possible by providing adjusted growth rates.
- Compute the sequential quarter-over-quarter growth rate for the most recent 2-3 quarters as an additional signal of near-term momentum, particularly for high-growth companies where annual comparisons may lag.

### Step 4 — Incorporate Forward Estimates

Present consensus forward estimates alongside historical actuals in a unified table that bridges the gap between reported results and projected figures:

- Current-year and next-year revenue and EPS estimates (mean, high, low) with the number of contributing analysts.
- Implied growth rates from current period to estimated periods, calculated as the percentage change from the most recent actual to the estimated figure.
- Long-term EPS growth rate estimate (typically a 3-5 year forward CAGR) if available from the Stock Analysis forecast page.
- Compare forward growth rates against historical CAGRs to determine whether the market expects acceleration or deceleration. If consensus implies materially higher growth than the historical trend, note the potential for disappointment. If consensus implies materially lower growth, note potential for upside surprise.
- Report the estimate revision direction over the last 30 and 90 days — are estimates trending up, down, or stable? Upward revisions combined with acceleration in historical growth form a strong positive signal.

### Step 5 — Contextualize with Management Guidance

Incorporate any management-provided guidance or targets:

- Short-term guidance (current quarter or fiscal year).
- Medium-term targets (e.g., "We aim to grow revenue 15-20% annually over the next 3 years").
- Total addressable market (TAM) estimates and the company's current penetration level.
- Identify discrepancies between management guidance and analyst consensus.

### Step 6 — Synthesize Growth Assessment

Provide an overall growth characterization:

- Classify the company's growth profile using the following framework: **High-Growth** (revenue CAGR above 15%), **Moderate-Growth** (5-15%), **Low-Growth** (0-5%), or **Declining** (negative). Adjust thresholds based on the company's size and sector — a 10% revenue CAGR for a mega-cap is exceptional, while the same rate for a small-cap SaaS company may be below average.
- Identify the primary growth drivers and key risks to continued growth. Be specific — name the product lines, geographies, or secular trends fueling growth, and name the competitive threats, regulatory risks, or market saturation concerns that could impede it.
- Assess whether the current valuation implies growth expectations that are reasonable, optimistic, or pessimistic relative to historical and forward trends. Use the PEG ratio (P/E divided by expected EPS growth rate) as a quick sanity check: a PEG above 2.0 implies the market is pricing in exceptional growth, while below 1.0 suggests growth may be undervalued.
- Provide a concise one-sentence growth thesis summarizing the investment case from a growth perspective.

## Depth Handling

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md` for depth and formatting guidelines.

**Summary depth (default):** Present the CAGR table with 1yr, 3yr, and 5yr columns for the core metrics (revenue, EPS, FCF). Include a 2-3 sentence narrative on growth quality and trajectory, plus the consensus forward growth rate.

**Detailed depth:** Expand to the full CAGR table including 10yr horizons and all seven metrics. Add quarterly YoY growth trends, segment-level decomposition, organic vs. acquisition-driven breakdown, geographic analysis, management guidance comparison, and TAM context. Provide extended narrative commentary explaining growth drivers and sustainability.

## Sector-Specific Adjustments

Apply the following sector-specific metrics when the company operates in a relevant industry:

- **Retail / Restaurants:** Report same-store sales growth (comps) alongside total revenue growth. Distinguish between new store contribution and comparable-store performance. Report unit growth (new store openings net of closures).
- **SaaS / Software:** Report Annual Recurring Revenue (ARR) or Monthly Recurring Revenue (MRR) growth. Include Net Revenue Retention (NRR) and Gross Revenue Retention (GRR) if available. NRR above 120% indicates strong expansion within existing customers.
- **Energy / Natural Resources:** Report production volume growth (barrels of oil equivalent per day, MMcf/d for gas). Include reserve replacement ratio (reserves added / reserves produced) as an indicator of long-term production sustainability.
- **Financial Services / Banking:** Report loan growth, deposit growth, and net interest income growth separately from fee-based revenue growth.
- **Biotech / Pharma:** Focus on pipeline-driven revenue growth. Report revenue by drug/product and identify patent cliff exposure dates.

Only include sector-specific metrics when the company's industry warrants them. Do not force these metrics for unrelated sectors.

## Output Format

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md` for the standard response structure including header, source links, and disclaimer.
