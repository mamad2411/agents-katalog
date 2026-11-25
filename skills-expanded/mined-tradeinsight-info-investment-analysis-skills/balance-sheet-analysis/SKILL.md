---
name: balance-sheet-analysis
description: >
  This skill should be used when the user asks about balance sheet, assets,
  liabilities, equity, book value, tangible book value, net cash, working
  capital, shareholders equity, goodwill, intangible assets, debt, accounts
  receivable, inventory, or total assets for a specific company.
---

# Balance Sheet Analysis

## Purpose

Analyze a company's balance sheet to evaluate its financial position at a point in time, covering the composition and quality of assets, the structure of liabilities, and the residual claim of shareholders. Compute derived metrics such as book value per share, tangible book value per share, net cash position, working capital, and key leverage ratios. Surface trends across multiple periods that reveal shifts in asset quality, capital structure, or financial risk.

## Data Fetching Process

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/data-sources.md` for full source details and fallback behavior.

1. **Resolve the ticker.** Fetch `https://www.sec.gov/files/company_tickers.json` using the `sec-fetch` skill (see `data-sources.md`), locate the company's CIK, and pad it to 10 digits. Cache the CIK and official company name.

2. **Fetch structured financial data (primary).** Request the SEC EDGAR XBRL company facts endpoint:
   ```
   https://data.sec.gov/api/xbrl/companyfacts/CIK{10-digit-CIK}.json
   ```
   Extract the following XBRL concepts under `facts > us-gaap > ... > units > USD`:
   - **Current Assets:** `CashAndCashEquivalentsAtCarryingValue`, `ShortTermInvestments`, `AccountsReceivableNetCurrent`, `InventoryNet`, `OtherAssetsCurrent`, `AssetsCurrent`
   - **Non-Current Assets:** `PropertyPlantAndEquipmentNet`, `Goodwill`, `IntangibleAssetsNetExcludingGoodwill`, `OtherAssetsNoncurrent`, `Assets`
   - **Current Liabilities:** `AccountsPayableCurrent`, `ShortTermBorrowings` or `DebtCurrent`, `DeferredRevenueCurrent`, `LiabilitiesCurrent`
   - **Non-Current Liabilities:** `LongTermDebt` or `LongTermDebtNoncurrent`, `DeferredRevenueNoncurrent`, `LiabilitiesNoncurrent`, `Liabilities`
   - **Shareholders' Equity:** `CommonStockValue`, `RetainedEarningsAccumulatedDeficit`, `AccumulatedOtherComprehensiveIncomeLossNetOfTax`, `TreasuryStockValue`, `StockholdersEquity`
   - **Shares:** `CommonStockSharesOutstanding`

   Filter for `fp == "FY"` entries. Sort by `end` date descending. Collect at least the last five fiscal years when available.

3. **Fetch pre-computed tables (secondary).** If EDGAR data is incomplete or unavailable, fetch:
   - `https://stockanalysis.com/stocks/{ticker}/financials/balance-sheet/` — annual balance sheet

4. **Fetch ratio data (supplementary).** For pre-computed leverage and efficiency ratios:
   - `https://stockanalysis.com/stocks/{ticker}/financials/ratios/`

## Analysis Steps

### Asset Composition

Break down total assets into major categories and present as a table:

| Category | Components | What to Watch |
|----------|-----------|---------------|
| Cash & Equivalents | Cash, short-term investments, marketable securities | Absolute level and trend; war chest for M&A or buybacks |
| Receivables | Accounts receivable net | Growth rate vs revenue growth; rising AR/revenue ratio signals collection risk |
| Inventory | Raw materials, WIP, finished goods | Days inventory outstanding; write-down risk for obsolescence |
| PP&E | Property, plant, equipment net of depreciation | Capital intensity; age of assets (accumulated depreciation / gross PP&E) |
| Goodwill | Acquisition premium | Percentage of total assets; impairment risk if acquisitions underperform |
| Other Intangibles | Patents, customer relationships, trademarks | Amortization trajectory; finite vs indefinite-lived |

Compute the percentage of total assets each category represents. Flag goodwill-heavy balance sheets (goodwill exceeding 30 percent of total assets) as carrying elevated impairment risk.

### Liability Structure

Break down total liabilities into current and non-current:

- **Current liabilities:** Accounts payable, accrued expenses, short-term debt, current portion of long-term debt, deferred revenue (current). Compute the ratio of current liabilities to total liabilities.
- **Non-current liabilities:** Long-term debt, deferred revenue (non-current), pension obligations, operating lease liabilities, other long-term obligations.
- **Total debt:** Sum of short-term borrowings, current portion of long-term debt, and long-term debt. Distinguish between gross debt and net debt (gross debt minus cash and short-term investments).

### Shareholders' Equity

Decompose equity into its components:

- **Common stock and APIC** — par value plus additional paid-in capital
- **Retained earnings** — cumulative net income minus cumulative dividends; a negative balance indicates accumulated losses
- **AOCI (Accumulated Other Comprehensive Income/Loss)** — unrealized gains/losses on securities, foreign currency translation, pension adjustments
- **Treasury stock** — shares repurchased; presented as a negative; growing treasury stock indicates active buyback programs

### Derived Metrics

Compute the following for each period:

- **Book Value per Share** = Total Stockholders' Equity / Shares Outstanding
- **Tangible Book Value per Share** = (Equity − Goodwill − Intangible Assets) / Shares Outstanding
- **Net Cash** = Cash + Short-Term Investments − Total Debt
- **Net Cash per Share** = Net Cash / Shares Outstanding
- **Working Capital** = Current Assets − Current Liabilities
- **Debt-to-Equity (D/E)** = Total Debt / Stockholders' Equity
- **Debt-to-Assets (D/A)** = Total Debt / Total Assets
- **Equity Multiplier** = Total Assets / Stockholders' Equity

Present derived metrics in a multi-year table. Highlight trends — a rising D/E ratio combined with declining equity signals increasing financial risk. Negative tangible book value is common for companies with large goodwill balances from acquisitions but should be flagged.

### Balance Sheet Trends

Compare the most recent balance sheet to prior periods:

- Is total asset growth driven by productive assets (PP&E, inventory) or non-productive assets (goodwill, intangibles)?
- Is the debt level growing faster than equity? This increases leverage.
- Is working capital positive and stable? Negative working capital may be acceptable for companies with strong cash conversion (e.g., subscription businesses) but is a warning sign for capital-intensive firms.
- Is retained earnings growing? Declining retained earnings may indicate persistent losses or aggressive dividend/buyback policies beyond earnings capacity.

## Depth Handling

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md` for standard formatting rules.

- **Summary depth (default).** Present three years of key balance sheet items in a condensed table: total assets, total liabilities, stockholders' equity, cash, total debt, net cash, goodwill. Include a derived metrics table with book value/share, tangible book value/share, net cash/share, working capital, D/E, and D/A. Add two to three sentences of narrative.

- **Detailed depth.** Expand to five years. Break out individual asset and liability line items. Include a full equity decomposition table. Add a balance sheet composition chart description (percentage of assets by category). Provide extended commentary on asset quality, leverage trajectory, and working capital dynamics.

## Sector-Specific Adjustments

- **Banking / Financial services.** The balance sheet is the core operating statement. Focus on loan portfolio composition, allowance for loan losses, deposit base, and regulatory capital ratios. Traditional working capital analysis does not apply. Look for `LoansAndLeasesReceivableNetReportedAmount`, `Deposits`, `AllowanceForLoanAndLeaseLossesRealEstate`.

- **REITs / Real estate.** PP&E (investment properties) dominates the asset side. Book value may understate market value of properties. Focus on net asset value (NAV) rather than book value. Look for `RealEstateInvestmentPropertyNet`.

- **Technology / Asset-light companies.** Intangible assets and goodwill may dominate. Cash and investments often represent a large share of total assets. Working capital analysis should focus on deferred revenue trends as an indicator of future revenue visibility.

- **Insurance.** Investment portfolio composition and reserve adequacy are critical. Look for `InvestmentsInDebtAndEquitySecurities` and `LiabilityForFuturePolicyBenefits`.

## Output

Follow the output structure defined in `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md`. Begin with the standard header, present data in markdown tables with right-aligned numbers and units, include source links after each data section, and close with the standard disclaimer.
