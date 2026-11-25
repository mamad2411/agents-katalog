---
name: cross-validation
description: >
  This skill should be used when the user asks to validate financial data, cross-check
  numbers, verify data, cross-validate, check data accuracy, compare sources, validate
  against another source, or investigate data discrepancies. Also invoked programmatically
  by the fundamental-analyst agent as a sequential post-step after parallel analysis.
---

# Cross-Validation

## Purpose

Verify key financial data points by cross-referencing values across two or more independent data sources. Detect discrepancies that may arise from differences in reporting periods, accounting adjustments, rounding conventions, or outright data errors. Produce a validation report that flags confirmed data, discrepancies above a defined threshold, and metrics with only single-source coverage, so downstream analysis rests on trustworthy inputs.

## Data Fetching Process

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/data-sources.md` for full source details and fallback behavior.

### Source Selection Rules

1. **Determine the primary source of the data being validated.** Identify which source originally provided the data points under review:
   - If the original data came from **SEC EDGAR**, validate against **Stock Analysis** as the cross-check source.
   - If the original data came from **Stock Analysis**, validate against **SEC EDGAR** or **Gurufocus** as the cross-check source.
   - If the original data came from **Gurufocus**, validate against **SEC EDGAR** as the cross-check source.
   - If the original source is unknown or the user simply requests validation, fetch from both SEC EDGAR and Stock Analysis independently and compare.

2. **Resolve the ticker.** Fetch `https://www.sec.gov/files/company_tickers.json` using the `sec-fetch` skill (see `data-sources.md`), locate the company's CIK, and pad it to 10 digits. Cache the CIK and official company name.

### Fetching Source A — SEC EDGAR XBRL API

3. **Fetch structured financial data from EDGAR.** Request:
   ```
   https://data.sec.gov/api/xbrl/companyfacts/CIK{10-digit-CIK}.json
   ```
   Extract the following XBRL concepts for the most recent fiscal year (filter for `fp == "FY"`, sort by `end` date descending):

   | Metric | XBRL Concept(s) | Unit |
   |--------|-----------------|------|
   | Revenue | `Revenues`, `RevenueFromContractWithCustomerExcludingAssessedTax` | USD |
   | Net Income | `NetIncomeLoss` | USD |
   | Diluted EPS | `EarningsPerShareDiluted` | USD/shares |
   | Total Assets | `Assets` | USD |
   | Total Debt | `LongTermDebt`, `LongTermDebtAndCapitalLeaseObligations` | USD |
   | Stockholders' Equity | `StockholdersEquity` | USD |
   | Shares Outstanding | `CommonStockSharesOutstanding` | shares |

   Record the `end` date for each data point to ensure period alignment during comparison.

### Fetching Source B — Stock Analysis

4. **Fetch financial data from Stock Analysis.** Retrieve:
   - `https://stockanalysis.com/stocks/{ticker}/financials/` — revenue, net income, EPS
   - `https://stockanalysis.com/stocks/{ticker}/financials/balance-sheet/` — total assets, total debt, equity
   - `https://stockanalysis.com/stocks/{ticker}/financials/ratios/` — P/E, EV/EBITDA, market cap

   Parse the HTML tables to extract the matching fiscal year's figures. Ensure the fiscal year end date aligns with the EDGAR data. Note any labeling differences (e.g., Stock Analysis may label "Total Debt" differently than EDGAR's `LongTermDebt`).

### Fetching Source C — Gurufocus (When Needed)

5. **Fetch supplementary data from Gurufocus** when a third source is required for tiebreaking or when one of the primary sources is unavailable:
   ```
   https://www.gurufocus.com/term/{metric}/{ticker}
   ```
   Common metric slugs: `revenue`, `net-income`, `eps-diluted`, `total-assets`, `long-term-debt`, `pe-ratio`, `ev-to-ebitda`.

### Market-Derived Metrics

6. **Validate market-derived metrics separately.** Market cap, P/E, and EV/EBITDA change with share price and may differ between sources due to timing:
   - Fetch current market cap from Stock Analysis main page: `https://stockanalysis.com/stocks/{ticker}/`
   - Compute P/E as market cap divided by TTM net income, or share price divided by TTM diluted EPS.
   - Compare computed P/E with the reported P/E from Stock Analysis ratios page and Gurufocus.
   - Accept wider discrepancy thresholds for market-derived metrics (up to 10%) since share price fluctuates intraday.

## Analysis Steps

### Key Metrics to Validate

Validate the following core metrics. These represent the most commonly referenced data points in fundamental analysis and are the highest-priority items for accuracy:

| Priority | Metric | Why It Matters |
|----------|--------|---------------|
| Critical | Revenue | Foundation of all growth and margin calculations |
| Critical | Net Income | Drives EPS, P/E, and profitability metrics |
| Critical | Diluted EPS | Most widely quoted earnings figure |
| High | Total Assets | Denominator for ROA and leverage ratios |
| High | Total Debt | Key input for D/E, interest coverage, solvency |
| High | Market Cap | Basis for all valuation multiples |
| Medium | P/E Ratio | Most common valuation shorthand |
| Medium | EV/EBITDA | Enterprise-level valuation multiple |

### Discrepancy Detection

For each metric, compute the percentage discrepancy between sources:

```
Discrepancy % = |Value_A - Value_B| / ((Value_A + Value_B) / 2) * 100
```

Apply the following thresholds:

| Metric Type | Threshold | Rationale |
|-------------|-----------|-----------|
| Reported financials (revenue, net income, EPS, assets, debt) | 5% | These come from audited filings; differences above 5% likely indicate a data error, period mismatch, or definitional difference |
| Market-derived metrics (market cap, P/E, EV/EBITDA) | 10% | Share price changes cause natural divergence between sources with different data refresh cycles |
| Computed ratios (ROE, ROIC, margins) | 8% | Slight differences in denominators or averaging methods can produce meaningful ratio differences |

### Discrepancy Investigation

When a discrepancy exceeds the threshold:

1. **Check period alignment.** Verify that both sources reference the same fiscal year end date. A common cause of discrepancy is one source reporting calendar-year data while the other reports the company's fiscal year (e.g., Apple's fiscal year ends in September, not December).

2. **Check definitional differences.** Revenue may differ if one source includes or excludes excise taxes. Debt may differ if one source includes capital lease obligations while the other reports only long-term debt. EPS may differ between basic and diluted. Document the specific definitional cause.

3. **Check currency and unit scaling.** Ensure both values use the same currency and scale (millions vs. billions vs. raw numbers). A factor-of-1000 discrepancy almost always indicates a unit mismatch rather than a data error.

4. **Check restatements.** If the company restated financials, one source may reflect the restated figures while the other retains the originally reported values. Note which value is the restated figure.

5. **Tiebreak with a third source.** If the cause of discrepancy cannot be determined, fetch the same metric from Gurufocus or WebSearch for an SEC filing excerpt. Align with whichever two of three sources agree.

### Single-Source Coverage

Note any metrics where only one source provides data. Common situations include:

- Gurufocus-only metrics: quality scores, predictability rank, DCF intrinsic value
- EDGAR-only metrics: specific XBRL concepts not mapped by aggregator sites
- Stock Analysis-only metrics: pre-computed TTM figures, analyst estimate composites

Flag single-source metrics explicitly so the user understands these data points have not been independently verified.

## Depth Handling

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md` for standard formatting rules.

- **Summary depth (default).** Present the validation table with status indicators for the eight core metrics. Include a one-sentence note for any flagged discrepancy explaining the likely cause. Omit detailed investigation steps. Total output should be a single table plus two to three sentences of commentary.

- **Detailed depth.** Expand to include all validated metrics (core plus any additional metrics the user or calling agent requested). Provide a full investigation narrative for each discrepancy, including the raw values from all sources consulted, the computed discrepancy percentage, the identified root cause, and the recommended value to use. Include a separate section listing single-source metrics with an assessment of reliability.

## Output

Follow the output structure defined in `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md`. Begin with the standard header using "Data Cross-Validation" as the analysis type. Present findings in the following validation table format:

| Metric | Source A (EDGAR) | Source B (Stock Analysis) | Discrepancy | Status |
|--------|-----------------|--------------------------|-------------|--------|
| Revenue ($B) | 394.3 | 394.3 | 0.0% | Confirmed |
| Net Income ($B) | 97.0 | 96.8 | 0.2% | Confirmed |
| Diluted EPS | 6.42 | 6.42 | 0.0% | Confirmed |
| Total Debt ($B) | 108.0 | 111.1 | 2.8% | Confirmed |
| P/E Ratio | 32.1 | 33.5 | 4.3% | Confirmed |
| EV/EBITDA | 25.4 | 28.1 | 10.1% | Discrepancy |

Use "Confirmed" when the discrepancy is within threshold and "Discrepancy" when it exceeds the threshold. For discrepancies, add a footnote row or inline note explaining the likely cause and the recommended value.

After the table, include a summary line:
```
Validation result: X of Y metrics confirmed, Z discrepancies flagged.
```

Note any metrics with single-source coverage in a separate row or footnote. Include source URLs for both sources consulted. Close with the standard disclaimer.
