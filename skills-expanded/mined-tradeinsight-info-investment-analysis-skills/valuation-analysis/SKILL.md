---
name: valuation-analysis
description: >
  This skill should be used when the user asks about overvalued, undervalued,
  fairly valued, P/E ratio, forward P/E, PEG ratio, EV/EBITDA, EV/EBIT, price
  to earnings, price to sales, price to book, P/FCF, price to free cash flow,
  DCF, discounted cash flow, intrinsic value, enterprise value, earnings yield,
  margin of safety, or valuation for a specific company.
---

# Valuation Analysis

## Purpose

Assess whether a company's current market price adequately reflects its financial fundamentals by computing and interpreting a comprehensive set of valuation multiples. Compare the company's multiples against its own historical range, sector peers, and the broader market. Incorporate forward estimates and, where available, discounted cash flow context to arrive at a reasoned assessment of relative valuation. Present the analysis as informational context, not as a buy or sell recommendation.

## Data Fetching Process

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/data-sources.md` for full source details and fallback behavior.

1. **Resolve the ticker.** Fetch `https://www.sec.gov/files/company_tickers.json` using the `sec-fetch` skill (see `data-sources.md`), locate the company's CIK, and pad it to 10 digits. Cache the CIK and official company name.

2. **Fetch structured financial data (primary).** Request the SEC EDGAR XBRL company facts endpoint:
   ```
   https://data.sec.gov/api/xbrl/companyfacts/CIK{10-digit-CIK}.json
   ```
   Extract the following XBRL concepts for the most recent fiscal year and trailing twelve months where available:
   - `Revenues` — for P/S and EV/Revenue
   - `NetIncomeLoss` — for P/E and earnings yield
   - `EarningsPerShareDiluted` — for P/E computation verification
   - `OperatingIncomeLoss` — for EV/EBIT
   - `DepreciationDepletionAndAmortization` — for EBITDA derivation
   - `NetCashProvidedByUsedInOperatingActivities` — for P/FCF and EV/FCF
   - `PaymentsToAcquirePropertyPlantAndEquipment` — CapEx for FCF
   - `StockholdersEquity` — for P/B
   - `Goodwill`, `IntangibleAssetsNetExcludingGoodwill` — for P/Tangible Book
   - `LongTermDebt`, `ShortTermBorrowings`, `CashAndCashEquivalentsAtCarryingValue`, `ShortTermInvestments` — for enterprise value
   - `CommonStockSharesOutstanding` — for per-share computations

3. **Fetch pre-computed ratios and market data (secondary).** Fetch:
   - `https://stockanalysis.com/stocks/{ticker}/financials/ratios/` — pre-computed P/E, P/B, P/S, EV/EBITDA, and historical multiples
   - `https://stockanalysis.com/stocks/{ticker}/` — current price, market cap, shares outstanding

4. **Fetch analyst estimates (critical for forward multiples).** Fetch:
   - `https://stockanalysis.com/stocks/{ticker}/forecast/` — consensus EPS estimates, revenue estimates, price targets, analyst recommendations

5. **Fetch DCF and intrinsic value data (supplementary).** Fetch:
   - `https://www.gurufocus.com/term/iv_dcf/{ticker}` — Gurufocus DCF intrinsic value estimate
   - `https://www.gurufocus.com/term/pettm/{ticker}` — historical P/E context

## Analysis Steps

### Enterprise Value Computation

Before computing EV-based multiples, derive enterprise value:

```
Enterprise Value = Market Cap + Total Debt + Minority Interest + Preferred Equity − Cash − Short-Term Investments
```

For simplicity when minority interest and preferred equity are not material:

```
EV = Market Cap + Total Debt − Cash and Equivalents
```

Present the EV components in a table so the user understands the bridge from market cap to EV.

### Earnings-Based Multiples

| Multiple | Formula | Interpretation |
|----------|---------|----------------|
| P/E (TTM) | Price / Trailing 12-Month EPS | What investors pay per dollar of current earnings |
| Forward P/E | Price / Consensus Next-Year EPS | Valuation based on expected future earnings |
| PEG Ratio | Forward P/E / Expected EPS Growth Rate (%) | Growth-adjusted P/E; PEG below 1.0 is often considered attractive |
| Earnings Yield | Diluted EPS / Price (inverse of P/E) | Comparable to bond yields; compare against the 10-year Treasury rate |

For earnings yield vs risk-free rate: if the earnings yield is below the current risk-free rate, the market is pricing in significant future growth or the stock may be overvalued on a yield basis. Fetch the current 10-year Treasury yield via WebSearch if not already known.

### Cash Flow-Based Multiples

| Multiple | Formula | Interpretation |
|----------|---------|----------------|
| P/FCF | Market Cap / Free Cash Flow | What investors pay per dollar of free cash flow |
| EV/EBITDA | Enterprise Value / EBITDA | Capital-structure-neutral profitability multiple; widely used in M&A |
| EV/EBIT | Enterprise Value / EBIT | Similar to EV/EBITDA but accounts for depreciation; better for capital-intensive businesses |
| EV/FCF | Enterprise Value / Free Cash Flow | Enterprise-level cash flow multiple |
| EV/Revenue | Enterprise Value / Revenue | Used for high-growth, pre-profit companies |

### Book Value-Based Multiples

| Multiple | Formula | Interpretation |
|----------|---------|----------------|
| P/B | Price / Book Value per Share | Relationship between market price and accounting equity |
| P/Tangible Book | Price / Tangible Book Value per Share | Excludes goodwill and intangibles; more conservative |

P/B below 1.0 means the market values the company below its liquidation value of equity — this may indicate deep value or fundamental problems. P/B is most relevant for asset-heavy industries (banking, insurance, industrials).

### Revenue-Based Multiples

| Multiple | Formula | Interpretation |
|----------|---------|----------------|
| P/S (TTM) | Market Cap / Trailing Revenue | Price paid per dollar of revenue |
| EV/Revenue | Enterprise Value / Revenue | Capital-structure-neutral revenue multiple |

Revenue multiples are most useful for high-growth companies with negative or volatile earnings. For mature companies, earnings and cash flow multiples are more informative.

### Income-Based Multiples

| Multiple | Formula | Interpretation |
|----------|---------|----------------|
| Dividend Yield | Annual Dividends per Share / Price | Current income return |
| Earnings Yield | EPS / Price | Inverse of P/E; directly comparable to interest rates |

### Valuation Context

For each computed multiple, provide context along three dimensions:

1. **Historical comparison.** Compare the current multiple to the company's own five-year average, five-year high, and five-year low. Note whether the stock is trading above or below its historical average.

2. **Peer / sector comparison.** When available from Stock Analysis or Gurufocus, compare the current multiple to the sector median. Note whether the premium or discount is justified by superior growth, margins, or returns.

3. **Market comparison.** Compare to broad market averages (e.g., S&P 500 average P/E of approximately 20-22x) for context.

### Forward Estimates and Analyst Consensus

Present analyst consensus data from Stock Analysis forecast:
- Current-year and next-year EPS estimates
- Current-year and next-year revenue estimates
- Consensus price target (mean, high, low)
- Analyst recommendation distribution (buy, hold, sell)
- Implied upside/downside from the consensus price target

### DCF / Intrinsic Value Context

If Gurufocus DCF data is available, present:
- The Gurufocus DCF intrinsic value estimate
- The current price relative to the DCF estimate (premium or discount percentage)
- The implied margin of safety (if trading below DCF estimate)

Note that a full DCF model requires assumptions about growth rates, discount rates, and terminal values. If the user requests a full DCF, outline the required inputs (revenue growth rate, operating margin trajectory, CapEx assumptions, WACC, terminal growth rate) and note that the Gurufocus estimate provides a reference point.

### Valuation Summary

Synthesize the findings into a brief assessment:
- Is the stock trading at a premium or discount to its historical multiples?
- Is the stock trading at a premium or discount to its peers?
- Do forward estimates suggest improving or deteriorating fundamentals?
- What is the implied return based on the analyst consensus price target?

Avoid definitive "buy" or "sell" language. Use terms like "trading at a premium to historical averages" or "appears attractively valued relative to peers on a PEG basis."

## Depth Handling

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md` for standard formatting rules.

- **Summary depth (default).** Present current P/E (TTM and forward), EV/EBITDA, P/FCF, P/B, and P/S in a single table alongside five-year averages and sector medians. Include the consensus price target and implied upside/downside. Add three to four sentences interpreting relative valuation.

- **Detailed depth.** Expand to include all multiples listed above, the full EV bridge, earnings yield vs risk-free rate comparison, a historical multiple range table, the DCF / intrinsic value context, complete analyst consensus data, and an extended valuation narrative discussing what growth assumptions are embedded in the current price.

## Sector-Specific Adjustments

- **REITs.** Standard P/E is not meaningful due to depreciation distortions. Use:
  - **P/FFO** = Price / FFO per Share (primary REIT valuation metric)
  - **P/AFFO** = Price / AFFO per Share
  - **P/NAV** = Price / Net Asset Value per Share (estimates market premium or discount to property value)

- **Banking / Financial Services.** P/B and P/Tangible Book are primary valuation metrics. Use **P/PTPP** (Price to Pre-Tax Pre-Provision Earnings) as an additional metric that strips out credit cycle volatility.

- **High-Growth / Pre-Profit Technology.** EV/Revenue and P/S are the primary multiples. PEG ratio is particularly important. Revenue growth rate should be presented alongside the multiple to contextualize high valuations.

- **Cyclical Industries (Energy, Materials, Industrials).** P/E may be misleading at cycle peaks (low P/E when earnings are cyclically high). Use normalized earnings or mid-cycle P/E. EV/EBITDA is generally more reliable for cyclicals.

- **Utilities.** Dividend yield and P/E are primary metrics. Compare yield to the 10-year Treasury rate and to the utility sector average.

## Output

Follow the output structure defined in `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md`. Begin with the standard header, present data in markdown tables with right-aligned numbers and units, include source links after each data section, and close with the standard disclaimer.
