---
name: income-statement-analysis
description: >
  This skill should be used when the user asks about revenue, earnings, EPS,
  income statement, margins, gross profit, operating income, net income, EBITDA,
  cost of goods sold, COGS, operating expenses, share count, top line, bottom
  line, or earnings per share for a specific company.
---

# Income Statement Analysis

## Purpose

Analyze a company's income statement to evaluate revenue generation, cost management, and profitability across reporting periods. Extract and interpret key line items from the top line (revenue) through the bottom line (net income), computing derived metrics such as margin ratios, growth rates, and per-share figures. Present findings in a structured format that surfaces trends, anomalies, and the quality of reported earnings.

## Data Fetching Process

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/data-sources.md` for full source details and fallback behavior.

1. **Resolve the ticker.** Fetch `https://www.sec.gov/files/company_tickers.json` using the `sec-fetch` skill (see `data-sources.md`), locate the company's CIK, and pad it to 10 digits. Cache the CIK and official company name for subsequent requests.

2. **Fetch structured financial data (primary).** Request the SEC EDGAR XBRL company facts endpoint:
   ```
   https://data.sec.gov/api/xbrl/companyfacts/CIK{10-digit-CIK}.json
   ```
   Extract the following XBRL concepts under `facts > us-gaap > ... > units > USD` (or `USD/shares` for per-share items):
   - `Revenues` or `RevenueFromContractWithCustomerExcludingAssessedTax` — total revenue
   - `CostOfGoodsAndServicesSold` or `CostOfRevenue` — COGS
   - `GrossProfit` — gross profit (compute if absent: revenue minus COGS)
   - `OperatingExpenses` — total operating expenses
   - `OperatingIncomeLoss` — EBIT / operating income
   - `NetIncomeLoss` — net income
   - `EarningsPerShareBasic` — basic EPS
   - `EarningsPerShareDiluted` — diluted EPS
   - `CommonStockSharesOutstanding` or `WeightedAverageNumberOfShareOutstandingBasicAndDiluted` — share count
   - `DepreciationDepletionAndAmortization` — D&A (needed to derive EBITDA)

   Filter each concept for `fp == "FY"` entries to obtain annual figures. Sort by `end` date descending to get the most recent periods first. Collect at least the last five fiscal years when available.

3. **Fetch pre-computed tables (secondary).** If EDGAR data is incomplete or unavailable, fetch:
   - `https://stockanalysis.com/stocks/{ticker}/financials/` — annual income statement
   - `https://stockanalysis.com/stocks/{ticker}/financials/?p=quarterly` — quarterly income statement (when quarterly detail is requested)

4. **Fetch analyst estimates (supplementary).** When forward-looking context is needed, fetch:
   - `https://stockanalysis.com/stocks/{ticker}/forecast/` — consensus revenue and EPS estimates for upcoming periods

## Analysis Steps

### Core Line Items

Extract and tabulate the following for each available fiscal year:

| Line Item | XBRL Concept | Notes |
|-----------|-------------|-------|
| Revenue | `Revenues` | Top-line sales |
| COGS | `CostOfGoodsAndServicesSold` | Direct production costs |
| Gross Profit | `GrossProfit` | Revenue minus COGS |
| Operating Expenses | `OperatingExpenses` | SG&A, R&D, other OpEx |
| Operating Income (EBIT) | `OperatingIncomeLoss` | Gross profit minus OpEx |
| EBITDA | Derived | EBIT plus D&A |
| Net Income | `NetIncomeLoss` | After interest, taxes, non-recurring items |
| Basic EPS | `EarningsPerShareBasic` | Net income per basic share |
| Diluted EPS | `EarningsPerShareDiluted` | Net income per diluted share |
| Shares Outstanding | `CommonStockSharesOutstanding` | Basic share count |

### Margin Hierarchy

Compute each margin as a percentage of revenue for every period:

- **Gross Margin** = Gross Profit / Revenue
- **Operating Margin (EBIT Margin)** = Operating Income / Revenue
- **EBITDA Margin** = EBITDA / Revenue
- **Net Margin** = Net Income / Revenue

Present margins in a multi-year table. Highlight expanding or contracting margins and note the magnitude of change in percentage points year over year. A widening gap between gross margin and operating margin may indicate rising SG&A or R&D spend. A widening gap between operating margin and net margin may signal increasing interest expense or tax burden.

### Growth Rates

Compute year-over-year (YoY) growth for:

- Revenue growth rate
- Gross profit growth rate
- Operating income growth rate
- Net income growth rate
- Diluted EPS growth rate

Flag any period where net income growth significantly outpaces or lags revenue growth, as this indicates margin expansion/compression or non-operating items distorting earnings.

### Share Count Trends

Track basic and diluted shares outstanding across periods. Compute the change in share count YoY. A declining share count indicates buyback activity, which boosts EPS even when net income is flat. A rising share count may indicate dilution from stock-based compensation (SBC) or equity raises.

### Revenue Quality

Assess revenue composition when data permits:

- **Recurring vs. one-time revenue.** Subscription or service revenue is generally higher quality than one-time license or product sales. Look for segment breakdowns in EDGAR filings or Stock Analysis.
- **Geographic diversification.** Note any concentration risk if a single geography dominates.
- **Customer concentration.** Flag if 10-K disclosures mention significant customer concentration.

### Operating Leverage

Evaluate whether revenue growth translates into faster operating income growth. Compute the operating leverage ratio:

- **Operating Leverage** = % Change in Operating Income / % Change in Revenue

A ratio greater than 1.0 indicates positive operating leverage — the company's cost structure allows incremental revenue to flow through to profit at an accelerating rate. A ratio less than 1.0 suggests the opposite.

## Depth Handling

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md` for standard formatting rules.

- **Summary depth (default).** Present the most recent three fiscal years of core line items in a single table, followed by a margin table. Include two to three sentences of narrative interpreting the trend. Show diluted EPS and share count. Omit quarterly data unless the user specifically asks.

- **Detailed depth.** Expand to five fiscal years and include quarterly data for the trailing four to eight quarters. Add a dedicated growth rate table, a share count trend section, a revenue quality discussion, and an operating leverage calculation. Provide extended commentary comparing current margins to historical averages and noting inflection points.

## Sector-Specific Adjustments

- **SaaS / Software companies.** In addition to GAAP revenue, look for Annual Recurring Revenue (ARR) disclosures. Margins may be depressed by heavy SBC — note SBC as a percentage of revenue alongside GAAP margins. Growth rate analysis is often more important than absolute margin levels for early-stage SaaS.

- **Financial services / Banking.** Revenue is often reported as net interest income plus non-interest income rather than a single "Revenues" line. Adapt XBRL concept lookups to `InterestIncomeExpenseNet` and `NoninterestIncome`.

- **Retail / Consumer.** Same-store sales growth may be a more relevant top-line metric than total revenue growth. Note if revenue growth is driven primarily by new store openings versus organic growth.

- **Energy / Commodities.** Revenue is heavily influenced by commodity prices. Note the price environment and distinguish volume growth from price-driven growth when segment data is available.

## Output

Follow the output structure defined in `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md`. Begin with the standard header, present data in markdown tables with right-aligned numbers and units, include source links after each data section, and close with the standard disclaimer.
