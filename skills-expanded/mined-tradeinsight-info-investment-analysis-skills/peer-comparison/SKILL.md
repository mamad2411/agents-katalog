---
name: peer-comparison
description: >
  This skill should be used when the user asks to compare companies, compare stocks,
  perform a peer comparison, compare against competitors, do an industry comparison,
  see how one company compares to another, do a side by side comparison, compare
  financials, compare valuations, or benchmark against peers.
---

# Peer Comparison

## Purpose

Compare a target company against its closest public-market peers across a standardized set of financial, profitability, and valuation metrics. Identify the peer set dynamically, fetch comparable data for each company, and present a side-by-side table that highlights where the target outperforms or underperforms relative to its competitive group. Provide brief interpretive commentary so the user can quickly understand the target's relative positioning.

## Data Fetching Process

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/data-sources.md` for full source details and fallback behavior.

### Peer Identification

1. **Determine the target company.** Resolve the ticker to a CIK by fetching `https://www.sec.gov/files/company_tickers.json` using the `sec-fetch` skill (see `data-sources.md`). Cache the CIK and official company name.

2. **Identify peers.** If the user explicitly provides a list of comparison companies, use those. Otherwise, identify three to five closest public competitors through the following process:
   - Use WebSearch to query "{company name} competitors publicly traded" or "{company name} peer companies stock market."
   - Cross-reference results with the company's 10-K Item 1 (Business) section, which often names competitors.
   - Prefer peers that share the same primary SIC code or GICS sub-industry classification.
   - Prefer peers with market capitalizations within a reasonable range (0.25x to 4x the target's market cap) to ensure meaningful comparison. If the target is a mega-cap, include at least one large-cap peer and note the size differential.
   - Exclude private companies, foreign-listed companies without US ADRs (unless specifically requested), and companies in unrelated industries that happen to have similar names.

3. **Confirm the peer set.** List the selected peers with their tickers and brief business descriptions. If the user did not specify peers, present the proposed set and proceed unless the composition is clearly unsuitable.

### Data Collection

4. **Fetch comparison data for each company.** For the target and each peer, collect the following metrics. Use the source priority matrix from the data-sources reference.

   **Primary approach — Stock Analysis ratios page:**
   ```
   https://stockanalysis.com/stocks/{ticker}/financials/ratios/
   ```
   Fetch the ratios page for each company. Extract the most recent annual values for all available metrics.

   **Secondary approach — SEC EDGAR XBRL API:**
   ```
   https://data.sec.gov/api/xbrl/companyfacts/CIK{10-digit-CIK}.json
   ```
   Extract raw financial figures and compute ratios manually when Stock Analysis data is unavailable or incomplete.

   **Tertiary approach — EDGAR frames endpoint for cross-company single-metric comparison:**
   ```
   https://data.sec.gov/api/xbrl/frames/us-gaap/{concept}/{unit}/CY{year}.json
   ```
   Use when comparing a single metric across many companies simultaneously.

5. **Fetch supplementary valuation data.** For market-cap-dependent ratios (P/E, EV/EBITDA, P/FCF), fetch current price data from Stock Analysis:
   ```
   https://stockanalysis.com/stocks/{ticker}/
   ```
   Alternatively, use WebSearch to confirm current market capitalization and enterprise value figures.

## Analysis Steps

### Comparison Metrics Table

Assemble the following metrics for the target and all peers. Present them in a single side-by-side table:

| Metric Category | Metric | Computation / Source |
|-----------------|--------|---------------------|
| **Scale** | Revenue (TTM) | Most recent four quarters summed, or latest annual |
| **Growth** | Revenue Growth (YoY) | Current year revenue / prior year revenue minus one |
| **Profitability** | Gross Margin | Gross profit / revenue |
| **Profitability** | Operating Margin | Operating income / revenue |
| **Profitability** | Net Margin | Net income / revenue |
| **Returns** | Return on Equity (ROE) | Net income / average stockholders' equity |
| **Returns** | Return on Invested Capital (ROIC) | NOPAT / average invested capital |
| **Valuation** | Price-to-Earnings (P/E) | Market cap / net income, or share price / diluted EPS |
| **Valuation** | EV/EBITDA | Enterprise value / EBITDA |
| **Valuation** | Price-to-Free-Cash-Flow (P/FCF) | Market cap / free cash flow |
| **Leverage** | Debt-to-Equity (D/E) | Total debt / stockholders' equity |
| **Cash Generation** | Free Cash Flow Margin | Free cash flow / revenue |
| **Shareholder Return** | Dividend Yield | Annual dividend per share / share price |

If a metric is unavailable for a specific peer (e.g., the company does not pay dividends), enter "N/A" rather than omitting the column. Use trailing-twelve-month (TTM) figures when available; otherwise, use the most recent fiscal year.

### Relative Positioning

After building the table, analyze the target's position:

- **Rank the target** within the peer group for each metric. Note where the target ranks first (best), last (worst), or in the middle.
- **Identify standout strengths.** Highlight metrics where the target is in the top quartile of the peer group. Explain why these strengths matter (e.g., "highest operating margin indicates superior cost control or pricing power").
- **Identify relative weaknesses.** Highlight metrics where the target is in the bottom quartile. Provide context (e.g., "lowest revenue growth but highest margin may indicate a mature, cash-generative business rather than a deteriorating one").
- **Valuation vs. fundamentals.** Compare the target's valuation multiples to its fundamental performance. Note if the target trades at a premium or discount relative to peers, and assess whether the premium or discount is justified by superior or inferior fundamentals.

### Commentary

Provide a brief narrative (three to five sentences at summary depth) covering:

- Overall competitive positioning of the target within its peer group.
- The one or two most significant advantages the target holds.
- The one or two most significant areas where the target lags.
- Whether the current valuation appears reasonable, stretched, or compressed relative to the peer set and why.

### Sector-Specific Adjustments

Adapt the comparison table to include sector-relevant metrics when the peer set belongs to a specific industry:

- **SaaS / Software:** Add Rule of 40 (revenue growth rate plus FCF margin), net revenue retention if disclosed.
- **Banking / Financial Services:** Replace gross margin with net interest margin (NIM). Add Tier 1 capital ratio and return on tangible common equity (ROTCE). Replace EV/EBITDA with price-to-tangible-book.
- **REITs:** Add funds from operations (FFO), price-to-FFO, and occupancy rate. Replace net margin with FFO margin.
- **Retail:** Add same-store sales growth and revenue per square foot if available.
- **Energy:** Add production growth, reserve replacement ratio, and lifting cost per barrel if available.

## Depth Handling

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md` for standard formatting rules.

- **Summary depth (default).** Present the comparison table with the 13 core metrics, the target column visually highlighted (bold or marked with an asterisk), and a three-to-five sentence commentary. Omit sector-specific metrics unless the sector is obvious and the data is readily available.

- **Detailed depth.** Expand the table to include sector-specific metrics, add a second table showing three-year trends for growth and margin metrics across all peers, include a relative valuation scatter discussion (P/E vs. growth, EV/EBITDA vs. margin), and extend commentary to a full paragraph per metric category.

## Output

Follow the output structure defined in `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md`. Begin with the standard header using "Peer Comparison" as the analysis type. Present the main comparison table with the target company's column marked (e.g., bold ticker or asterisk) so it is immediately identifiable. Include source links for each peer's data after the table. Close with the standard disclaimer.

Format the comparison table as:

| Metric | **TARGET*** | Peer 1 | Peer 2 | Peer 3 | Peer 4 |
|--------|------------|--------|--------|--------|--------|
| Revenue ($B) | **XX.X** | XX.X | XX.X | XX.X | XX.X |
| Revenue Growth | **XX.X%** | XX.X% | XX.X% | XX.X% | XX.X% |
| ... | ... | ... | ... | ... | ... |

Mark the best value in each row with an upward indicator and the worst with a downward indicator where directionality is clear (higher is better for margins; lower is better for leverage).
