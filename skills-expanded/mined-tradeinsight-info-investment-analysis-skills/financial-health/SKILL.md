---
name: financial-health
description: >
  This skill should be used when the user asks about debt levels, liquidity,
  solvency, balance sheet strength, current ratio, quick ratio, debt to equity,
  interest coverage, financial health, credit quality, debt maturity, leverage,
  debt to EBITDA, cash ratio, Tier 1 capital, or capital ratio for a specific
  company.
---

# Financial Health Analysis

## Purpose

Assess a company's financial health by evaluating its ability to meet short-term obligations (liquidity), sustain long-term debt commitments (solvency), and withstand adverse economic conditions. Compute and interpret a comprehensive set of liquidity ratios, leverage metrics, and coverage ratios. Examine debt maturity profiles, covenant risk indicators, and off-balance-sheet obligations to provide a holistic view of financial resilience. Flag potential stress signals that may not be apparent from headline financial statements alone.

## Data Fetching Process

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/data-sources.md` for full source details and fallback behavior.

1. **Resolve the ticker.** Fetch `https://www.sec.gov/files/company_tickers.json` using the `sec-fetch` skill (see `data-sources.md`), locate the company's CIK, and pad it to 10 digits. Cache the CIK and official company name.

2. **Fetch structured financial data (primary).** Request the SEC EDGAR XBRL company facts endpoint:
   ```
   https://data.sec.gov/api/xbrl/companyfacts/CIK{10-digit-CIK}.json
   ```
   Extract the following XBRL concepts:
   - **Current Assets:** `AssetsCurrent`, `CashAndCashEquivalentsAtCarryingValue`, `ShortTermInvestments`, `AccountsReceivableNetCurrent`, `InventoryNet`
   - **Current Liabilities:** `LiabilitiesCurrent`, `AccountsPayableCurrent`, `DebtCurrent` or `ShortTermBorrowings`
   - **Non-Current Liabilities:** `LongTermDebt` or `LongTermDebtNoncurrent`, `Liabilities`
   - **Total Balance Sheet:** `Assets`, `StockholdersEquity`
   - **Income Statement:** `OperatingIncomeLoss`, `DepreciationDepletionAndAmortization`, `InterestExpense`, `Revenues`, `IncomeTaxExpenseBenefit`
   - **Cash Flow:** `NetCashProvidedByUsedInOperatingActivities`

   Filter for `fp == "FY"` entries. Sort by `end` date descending. Collect at least five fiscal years.

3. **Fetch pre-computed ratios (secondary).** Fetch:
   - `https://stockanalysis.com/stocks/{ticker}/financials/ratios/` — pre-computed liquidity and leverage ratios
   - `https://stockanalysis.com/stocks/{ticker}/financials/balance-sheet/` — balance sheet for cross-reference

4. **Fetch credit and debt detail (supplementary).** For deeper credit quality analysis:
   - Use WebSearch to find "{ticker} debt maturity schedule" or "{ticker} credit rating" for rating agency data
   - `https://www.gurufocus.com/term/deb2equity/{ticker}` — Gurufocus debt-to-equity history
   - Search SEC EDGAR for the most recent 10-K filing to review debt footnotes (Note on Long-Term Debt typically includes maturity schedule and interest rates)

## Analysis Steps

### Liquidity Ratios

Compute the following for each period to assess short-term financial health:

| Ratio | Formula | Healthy Range | Interpretation |
|-------|---------|--------------|----------------|
| Current Ratio | Current Assets / Current Liabilities | 1.5 – 3.0 | Ability to cover short-term obligations with short-term assets |
| Quick Ratio | (Cash + Short-Term Investments + Receivables) / Current Liabilities | 1.0 – 2.0 | Liquidity excluding inventory (more conservative) |
| Cash Ratio | (Cash + Short-Term Investments) / Current Liabilities | 0.5 – 1.0 | Most conservative; ability to pay obligations with cash alone |
| OCF Ratio | Operating Cash Flow / Current Liabilities | > 1.0 | Ability to cover short-term obligations from ongoing operations |

Present liquidity ratios in a multi-year table. Flag ratios that fall below the lower bound of the healthy range as potential liquidity concerns. Note that acceptable ranges vary by industry — retail and subscription businesses may operate sustainably with current ratios below 1.0 due to negative working capital models (collecting cash before paying suppliers).

A declining trend in liquidity ratios, even if above the threshold, warrants attention and narrative explanation.

### Solvency and Leverage Ratios

Compute the following to assess long-term financial sustainability:

| Ratio | Formula | Interpretation |
|-------|---------|----------------|
| Debt-to-Equity (D/E) | Total Debt / Stockholders' Equity | Proportion of debt vs equity financing |
| Debt-to-Assets (D/A) | Total Debt / Total Assets | Percentage of assets funded by debt |
| Debt-to-EBITDA | Total Debt / EBITDA | Years of earnings needed to repay debt at current levels |
| Net Debt-to-EBITDA | (Total Debt − Cash) / EBITDA | Leverage adjusted for cash on hand; most widely used by credit analysts |
| Interest Coverage | EBIT / Interest Expense | Ability to service interest payments from operating profit |
| Fixed Charge Coverage | (EBIT + Lease Payments) / (Interest Expense + Lease Payments) | Broader coverage including lease obligations |
| Equity Multiplier | Total Assets / Stockholders' Equity | Degree of asset leverage; higher = more leveraged |

Present solvency ratios in a multi-year table. Key interpretation guidelines:

- **D/E above 2.0** generally indicates high leverage for non-financial companies, though this varies by industry.
- **Net Debt-to-EBITDA above 3.0x** is typically considered elevated; above 4.0x is a potential credit concern.
- **Interest coverage below 3.0x** signals that a relatively small decline in earnings could impair the company's ability to service debt.
- **Negative equity** (total liabilities exceeding total assets) is a severe red flag unless the company is in a specific sector where this is common (e.g., some tobacco or consumer staples companies with large buyback programs).

### Credit Quality Assessment

Go beyond ratios to assess qualitative credit factors:

- **Debt maturity profile.** Review the 10-K debt footnotes for the schedule of upcoming maturities. Flag any "maturity wall" — a concentration of debt maturing in the next one to three years — as a refinancing risk, especially in a rising rate environment.
- **Interest rate composition.** Determine the mix of fixed-rate vs floating-rate debt. A high proportion of floating-rate debt exposes the company to interest rate risk.
- **Credit rating.** When available via WebSearch, note the current credit rating from major agencies (S&P, Moody's, Fitch). Investment grade (BBB- / Baa3 or above) vs high yield (below BBB-) is a critical distinction for access to capital markets.
- **Covenant risk.** Search for covenant information in the 10-K or credit agreements. Companies approaching covenant thresholds may face restricted financial flexibility.
- **Off-balance-sheet obligations.** Check for operating lease obligations (now largely on-balance-sheet under ASC 842), unfunded pension liabilities, and purchase commitments that represent future cash outflows not fully reflected in the debt figures.

### Trend Analysis

For all ratios, analyze the trajectory across the available periods:

- Is leverage increasing or decreasing? A company actively deleveraging (reducing debt-to-EBITDA over time) is improving its financial health.
- Is liquidity deteriorating despite stable or growing revenue? This may indicate working capital problems or excessive capital returns.
- Is interest coverage declining? This could be due to rising debt, falling EBIT, or both.
- Compare the current period's ratios to the five-year average to identify whether the company is at a historical extreme.

### Stress Indicators

Flag the following as potential financial stress signals:

- Current ratio below 1.0 combined with negative OCF
- Interest coverage below 2.0x
- Net debt-to-EBITDA above 5.0x
- Declining cash balance combined with rising short-term debt
- Negative retained earnings (accumulated deficit) combined with negative free cash flow
- Significant upcoming debt maturities (within 12 months) exceeding available cash and undrawn credit facilities

## Depth Handling

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md` for standard formatting rules.

- **Summary depth (default).** Present three years of key ratios in two tables: one for liquidity (current, quick, cash ratios) and one for solvency (D/E, net debt-to-EBITDA, interest coverage). Add a brief narrative (two to three sentences) on overall financial health and any flagged concerns.

- **Detailed depth.** Expand to five years. Include all ratios from both categories, the debt maturity profile (if available from 10-K), credit rating context, fixed-rate vs floating-rate debt breakdown, off-balance-sheet obligations, the full stress indicator checklist, and an extended narrative discussing the company's financial flexibility, refinancing risk, and trajectory relative to its sector.

## Sector-Specific Adjustments

- **Banking / Financial Services.** Traditional liquidity and leverage ratios do not apply to banks. Focus on:
  - **Tier 1 Capital Ratio** = Tier 1 Capital / Risk-Weighted Assets (minimum 6 percent regulatory requirement; well-capitalized above 8 percent)
  - **Common Equity Tier 1 (CET1) Ratio** — the highest quality capital measure
  - **Total Capital Ratio** = Total Capital / Risk-Weighted Assets
  - **Non-Performing Loan (NPL) Ratio** = Non-Performing Loans / Total Loans
  - **Loan-to-Deposit Ratio** = Total Loans / Total Deposits (above 100 percent indicates reliance on wholesale funding)
  - **Provision Coverage Ratio** = Allowance for Loan Losses / Non-Performing Loans
  Look for `RiskWeightedAssets`, `Tier1CapitalToRiskWeightedAssetsRatio` or similar XBRL concepts, or fetch from Stock Analysis ratios page.

- **Utilities.** Higher leverage is structurally acceptable due to regulated, predictable cash flows. D/E ratios of 1.0–1.5 are common. Focus on interest coverage and the regulatory environment's impact on rate recovery.

- **REITs.** High leverage is common. Focus on net debt-to-EBITDA, interest coverage, debt maturity profile, and the percentage of fixed-rate vs floating-rate debt. Also assess the weighted average maturity and weighted average interest rate of the debt portfolio.

- **Technology / Asset-light companies.** Many carry net cash positions (more cash than debt). For these companies, the financial health story is about cash deployment rather than debt risk. Focus on cash burn rate (for unprofitable companies) and cash runway analysis.

- **Cyclical industries (Energy, Materials).** Evaluate leverage at both the current point in the cycle and on a normalized-earnings basis. A company may appear healthy at cycle peak earnings but be dangerously leveraged when earnings normalize. Use mid-cycle EBITDA for debt-to-EBITDA if available.

## Output

Follow the output structure defined in `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md`. Begin with the standard header, present data in markdown tables with right-aligned numbers and units, include source links after each data section, and close with the standard disclaimer.
