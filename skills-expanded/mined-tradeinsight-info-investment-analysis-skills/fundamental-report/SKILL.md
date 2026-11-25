---
name: fundamental-report
description: >
  This skill should be used when the user invokes "/fundamental-report" followed by a
  stock ticker. Generates a comprehensive fundamental analysis research note at
  summary depth covering all 14 analysis areas with key metrics, signal rating,
  cross-validation, and investment thesis arguments.
user-invocable: true
disable-model-invocation: true
---

# Fundamental Report — Summary Depth

Generate a comprehensive fundamental analysis research note for a publicly traded company. Orchestrate all analysis skills in parallel, aggregate results, and compile into a structured report.

## Orchestration Process

### Step 0: Ticker Resolution

Before dispatching parallel tasks, resolve the ticker:

1. Fetch the company ticker-to-CIK mapping from `https://www.sec.gov/files/company_tickers.json` using the `sec-fetch` skill (it handles SEC credentials and User-Agent automatically — see `data-sources.md`)
2. Find the CIK for the given ticker and pad to 10 digits
3. Fetch company overview from `https://stockanalysis.com/stocks/{ticker}/` via WebFetch to get current price, market cap, sector, and exchange
4. Store resolved metadata: CIK, company name, sector, exchange, current price, market cap

If the ticker is not found in EDGAR (international company), note this and proceed with Stock Analysis and WebSearch only.

**Important:** For ALL SEC EDGAR fetches (`data.sec.gov`, `efts.sec.gov`, `www.sec.gov`), use the `sec-fetch` skill — never WebFetch.

### Step 1: Parallel Dispatch

Launch the following as parallel subagents using the Agent tool. Pass the resolved ticker and company metadata to each:

**Analysis Skills (14):**
- income-statement-analysis
- balance-sheet-analysis
- cash-flow-analysis
- profitability-analysis
- valuation-analysis
- financial-health
- growth-analysis
- efficiency-analysis
- dividend-analysis
- analyst-estimates
- moat-analysis
- competitive-position
- insider-activity
- risk-assessment

**Utility Skills (2):**
- peer-comparison
- sec-filing-reader (request 10-K summary for the most recent fiscal year)

**Agent (1):**
- signal-rater agent (fetches Buy/Hold/Sell ratings independently)

Total: 17 parallel tasks.

Instruct each skill to provide **summary depth** output: key metrics in tables with 1-2 sentence interpretation per metric group.

### Step 2: Sequential Cross-Validation

After all 17 parallel results are collected:

1. Invoke the cross-validation skill with the collected data
2. Cross-validate key metrics (revenue, net income, EPS, total assets, total debt, market cap, P/E, EV/EBITDA) across sources
3. Flag any discrepancies where values differ by more than 5%

### Step 3: Report Assembly

Do not announce or enumerate data sources, tools, or fetching details to the user at this stage. Simply compile the results.

Compile all results into the following structure:

#### Section 1: Key Metrics Summary

Present a quick-reference table at the top of the report:

```markdown
| Metric | Value |
|--------|-------|
| Price | $XXX.XX |
| Market Cap | $X.XXT |
| P/E (TTM) | XX.X |
| Forward P/E | XX.X |
| EV/EBITDA | XX.X |
| P/FCF | XX.X |
| Revenue Growth (YoY) | XX% |
| EPS Growth (YoY) | XX% |
| ROE | XX% |
| ROIC | XX% |
| Gross Margin | XX% |
| Net Margin | XX% |
| Debt/Equity | X.XX |
| Current Ratio | X.XX |
| FCF Yield | XX% |
| Dividend Yield | XX% |
| TipRanks SmartScore | X/10 |
| Overall Signal | Buy/Hold/Sell |
```

#### Section 2: Signal Rating

Present the aggregated rating from the signal-rater agent:
- Per-source breakdown table (TipRanks, analyst consensus, Gurufocus, insider signal)
- Overall signal with confidence level
- Weighted average score

#### Section 3: Detailed Analysis

Organize all skill results by tier at summary depth:

**Tier 1 — Core Financial:**
- Income Statement highlights
- Balance Sheet highlights
- Cash Flow highlights
- Profitability metrics
- Valuation assessment
- Financial Health assessment

**Tier 2 — Growth & Returns:**
- Growth trajectory
- Efficiency metrics
- Dividend profile
- Analyst consensus

**Tier 3 — Qualitative:**
- Moat assessment
- Competitive position
- Management & governance
- Risk factors

Include peer comparison table and 10-K summary highlights where relevant.

#### Section 4: Cross-Validation

Present cross-validation results:
- Table of validated metrics with Confirmed/Discrepancy status
- Both source values and URLs for any discrepancies
- Note any metrics with single-source coverage

#### Section 5: Reasons to Consider

Derive 3-5 bull case arguments from the analysis. Focus on:
- Strong or improving fundamentals (margins, returns, growth)
- Attractive valuation relative to peers or historical range
- Durable competitive advantages (moat strength)
- Positive catalysts (insider buying, estimate upgrades, new products)

#### Section 6: Reasons to Avoid

Derive 3-5 bear case arguments from the analysis. Focus on:
- Deteriorating fundamentals (declining margins, rising debt)
- Overvaluation signals
- Competitive threats or moat erosion
- Accounting red flags or governance concerns
- Macro or regulatory headwinds

#### Section 7: Summary

Synthesize the entire analysis into a concise summary. This is what gets displayed in the terminal — the full report is written to file.

```markdown
## Summary

**[Company Name] ([TICKER])** — **[Overall Signal: Strong Buy / Buy / Hold / Sell / Strong Sell]** (Confidence: [High/Medium/Low])

**Weighted Score:** X.X / 5.0 | **Price:** $XXX.XX | **Market Cap:** $X.XXT

**Thesis:** [2-3 sentence investment thesis synthesizing the key finding from the analysis — what matters most about this company right now and why the signal lands where it does.]

**Key Strengths:**
- [Top bull case point with supporting metric]
- [Second bull case point]
- [Third bull case point]

**Key Risks:**
- [Top bear case point with supporting metric]
- [Second bear case point]
- [Third bear case point]

**Report:** [Full report saved to `reports/YYYY-MM-DD-HH-MM-SS-TICKER.md`]
```

#### Section 8: Source Links

Compile all URLs referenced throughout the report, grouped by source:
- SEC EDGAR links
- Stock Analysis links
- Gurufocus links
- TipRanks references
- Other WebSearch sources

#### Section 9: Disclaimer

```
For informational purposes only. Not financial advice. Data sourced from public
filings and third-party websites. Verify critical data points independently
before making investment decisions.
```

## Report File Output

After assembling the full report (Sections 1-9), write it to a markdown file:

1. Generate the filename using the current timestamp and ticker: `reports/YYYY-MM-DD-HH-MM-SS-{TICKER}.md` (e.g., `reports/2026-03-13-14-30-45-AAPL.md`)
2. Create the `reports/` directory in the current working directory if it doesn't exist
3. Write the complete report (all 9 sections) to the file using the Write tool
4. In the terminal, display **only the Summary section** (Section 7) — do not print the full report to the terminal
5. Include the file path in the summary so the user knows where to find the full report

## Additional Resources

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/data-sources.md` for data fetching instructions and source priority matrix.

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md` for detailed output formatting guidance.
