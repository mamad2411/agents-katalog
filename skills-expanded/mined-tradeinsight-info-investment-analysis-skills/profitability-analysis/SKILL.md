---
name: profitability-analysis
description: >
  This skill should be used when the user asks about ROE, ROA, ROIC, return on
  equity, return on assets, return on invested capital, ROCE, return on capital
  employed, DuPont decomposition, DuPont analysis, profitability, return
  metrics, or Rule of 40 for a specific company.
---

# Profitability Analysis

## Purpose

Evaluate a company's ability to generate returns on the capital deployed by shareholders, lenders, and the business itself. Analyze the margin hierarchy across reporting periods, compute return metrics (ROE, ROA, ROIC, ROCE), and decompose returns using the DuPont framework to identify whether profitability is driven by margins, asset efficiency, or leverage. Compare returns against the company's cost of capital to determine whether it is creating or destroying value.

## Data Fetching Process

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/data-sources.md` for full source details and fallback behavior.

1. **Resolve the ticker.** Fetch `https://www.sec.gov/files/company_tickers.json` using the `sec-fetch` skill (see `data-sources.md`), locate the company's CIK, and pad it to 10 digits. Cache the CIK and official company name.

2. **Fetch structured financial data (primary).** Request the SEC EDGAR XBRL company facts endpoint:
   ```
   https://data.sec.gov/api/xbrl/companyfacts/CIK{10-digit-CIK}.json
   ```
   Extract the following XBRL concepts:
   - **Income statement:** `Revenues`, `GrossProfit`, `OperatingIncomeLoss`, `NetIncomeLoss`, `DepreciationDepletionAndAmortization`, `InterestExpense`, `IncomeTaxExpenseBenefit`
   - **Balance sheet:** `Assets`, `StockholdersEquity`, `Goodwill`, `IntangibleAssetsNetExcludingGoodwill`, `LongTermDebt`, `ShortTermBorrowings` or `DebtCurrent`, `CashAndCashEquivalentsAtCarryingValue`, `ShortTermInvestments`
   - **Cash flow:** `NetCashProvidedByUsedInOperatingActivities` (for operating return context)

   Filter for `fp == "FY"` entries. Sort by `end` date descending. Collect at least five fiscal years.

3. **Fetch pre-computed ratios (secondary).** Fetch:
   - `https://stockanalysis.com/stocks/{ticker}/financials/ratios/` — pre-computed ROE, ROA, ROIC, margins
   - `https://stockanalysis.com/stocks/{ticker}/financials/` — income statement for margin computation

4. **Fetch WACC and return benchmarks (supplementary).** For ROIC vs WACC comparison:
   - `https://www.gurufocus.com/term/wacc/{ticker}` — weighted average cost of capital
   - `https://www.gurufocus.com/term/roic/{ticker}` — ROIC with Gurufocus methodology

## Analysis Steps

### Margin Hierarchy

Compute and tabulate the full margin stack for each fiscal year:

| Margin | Formula | Significance |
|--------|---------|-------------|
| Gross Margin | Gross Profit / Revenue | Pricing power and direct cost management |
| Operating Margin (EBIT) | Operating Income / Revenue | Core business profitability after all operating costs |
| EBITDA Margin | (Operating Income + D&A) / Revenue | Operating profitability before depreciation; useful for capital-intensive businesses |
| Net Margin | Net Income / Revenue | Bottom-line profitability after all costs, interest, and taxes |

Present margins in a multi-year trend table. Identify whether margins are expanding, stable, or contracting. Compute the spread between gross margin and operating margin (indicating operating cost burden) and between operating margin and net margin (indicating financial and tax burden).

### Return Metrics

Compute the following for each period, using average balance sheet figures (average of beginning and ending period values) for denominator metrics:

| Metric | Formula | What It Measures |
|--------|---------|-----------------|
| ROE | Net Income / Average Stockholders' Equity | Return generated on shareholder capital |
| ROA | Net Income / Average Total Assets | Return generated on all assets regardless of funding |
| ROIC | NOPAT / Average Invested Capital | Return on all operating capital (debt + equity minus excess cash) |
| ROCE | EBIT / Average Capital Employed | Return on long-term capital base |
| ROTE | Net Income / Average Tangible Equity | Return on equity excluding goodwill and intangibles; critical for acquisitive companies |

Where:
- **NOPAT** = Operating Income × (1 − Effective Tax Rate)
- **Invested Capital** = Total Equity + Total Debt − Cash and Short-Term Investments
- **Capital Employed** = Total Assets − Current Liabilities
- **Tangible Equity** = Stockholders' Equity − Goodwill − Intangible Assets

Present return metrics in a multi-year table. Identify trends — rising returns indicate improving capital efficiency; declining returns may signal overinvestment, margin compression, or balance sheet bloat.

### DuPont Decomposition

Decompose ROE into its three component drivers:

```
ROE = Net Margin × Asset Turnover × Equity Multiplier
```

Where:
- **Net Margin** = Net Income / Revenue (profitability lever)
- **Asset Turnover** = Revenue / Average Total Assets (efficiency lever)
- **Equity Multiplier** = Average Total Assets / Average Stockholders' Equity (leverage lever)

Present the decomposition in a multi-year table showing each component alongside the resulting ROE. This reveals the source of ROE changes:
- If ROE rises due to increasing net margin, profitability is improving.
- If ROE rises due to increasing asset turnover, the company is extracting more revenue per dollar of assets.
- If ROE rises primarily due to a higher equity multiplier, the company is using more leverage — which increases financial risk.

Flag cases where a high ROE is driven predominantly by leverage (equity multiplier above 3.0) as this may represent risk rather than quality.

### ROIC vs WACC

When WACC data is available, compare ROIC to WACC:

- **ROIC > WACC** indicates economic value creation — each dollar of invested capital generates returns above its cost.
- **ROIC < WACC** indicates economic value destruction — the company would return more value by distributing capital to shareholders.
- **ROIC ≈ WACC** indicates the company is earning approximately its cost of capital.

Compute the **economic spread** = ROIC − WACC. Present the spread for each available year and note the trend.

### Multi-Year Trend Analysis

For all return metrics, compute:
- Five-year average
- Five-year high and low
- Direction of trend (improving, stable, deteriorating)
- Comparison to sector median when available via peer data

## Depth Handling

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md` for standard formatting rules.

- **Summary depth (default).** Present three years of the margin hierarchy and key return metrics (ROE, ROA, ROIC) in two tables. Include the DuPont decomposition for the most recent year. Add two to three sentences interpreting whether returns are improving and what is driving them.

- **Detailed depth.** Expand to five years. Include all return metrics (ROE, ROA, ROIC, ROCE, ROTE), the full multi-year DuPont decomposition table, the ROIC vs WACC analysis, and five-year averages. Provide extended commentary on the quality and sustainability of returns, the role of leverage in ROE, and how the company compares to its sector.

## Sector-Specific Adjustments

- **SaaS / High-Growth Technology.** Apply the **Rule of 40**: Revenue Growth Rate (%) + Operating Margin (%) should ideally exceed 40. For early-stage SaaS companies with high growth but negative margins, the Rule of 40 is a more relevant profitability benchmark than absolute ROE or ROIC. Report both the GAAP and adjusted (excluding SBC) margin in the Rule of 40 calculation.

- **Banking / Financial Services.** Use **ROTCE (Return on Tangible Common Equity)** as the primary return metric rather than ROE, since banks carry significant goodwill from acquisitions. Also compute **Net Interest Margin (NIM)** = Net Interest Income / Average Earning Assets and **Efficiency Ratio** = Non-Interest Expense / Total Revenue (lower is better).

- **REITs.** Standard ROE and ROA are distorted by depreciation conventions for real property. Focus on FFO-based returns and NAV-based returns rather than net-income-based ratios.

- **Capital-intensive industries (Utilities, Industrials).** ROCE and ROIC are more informative than ROE due to the heavy use of debt financing. Focus on the ROIC vs WACC spread to assess value creation.

- **Insurance.** Use **Combined Ratio** (loss ratio + expense ratio) as the primary profitability metric. A combined ratio below 100 percent indicates underwriting profitability.

## Output

Follow the output structure defined in `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md`. Begin with the standard header, present data in markdown tables with right-aligned numbers and units, include source links after each data section, and close with the standard disclaimer.
