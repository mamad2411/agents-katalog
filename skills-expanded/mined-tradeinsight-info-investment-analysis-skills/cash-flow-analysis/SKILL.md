---
name: cash-flow-analysis
description: >
  This skill should be used when the user asks about cash flow, free cash flow,
  FCF, operating cash flow, OCF, capital expenditures, CapEx, quality of
  earnings, cash flow statement, FCF margin, cash conversion, levered free cash
  flow, FFO, or funds from operations for a specific company.
---

# Cash Flow Analysis

## Purpose

Analyze a company's cash flow statement to evaluate the quality and sustainability of its cash generation. Distinguish between cash earned from operations, cash deployed in investing activities, and cash raised or returned through financing activities. Compute derived metrics including free cash flow, FCF margin, and cash conversion ratios to assess whether reported earnings translate into actual cash. Surface trends that reveal capital allocation priorities and long-term financial sustainability.

## Data Fetching Process

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/data-sources.md` for full source details and fallback behavior.

1. **Resolve the ticker.** Fetch `https://www.sec.gov/files/company_tickers.json` using the `sec-fetch` skill (see `data-sources.md`), locate the company's CIK, and pad it to 10 digits. Cache the CIK and official company name.

2. **Fetch structured financial data (primary).** Request the SEC EDGAR XBRL company facts endpoint:
   ```
   https://data.sec.gov/api/xbrl/companyfacts/CIK{10-digit-CIK}.json
   ```
   Extract the following XBRL concepts under `facts > us-gaap > ... > units > USD`:
   - **Operating Activities:** `NetCashProvidedByUsedInOperatingActivities`, `DepreciationDepletionAndAmortization`, `ShareBasedCompensation`, `IncreaseDecreaseInAccountsReceivable`, `IncreaseDecreaseInInventories`, `IncreaseDecreaseInAccountsPayable`
   - **Investing Activities:** `PaymentsToAcquirePropertyPlantAndEquipment` (CapEx), `PaymentsToAcquireBusinessesNetOfCashAcquired`, `NetCashProvidedByUsedInInvestingActivities`
   - **Financing Activities:** `RepaymentsOfDebt`, `ProceedsFromIssuanceOfDebt`, `PaymentsForRepurchaseOfCommonStock`, `PaymentsOfDividends`, `NetCashProvidedByUsedInFinancingActivities`
   - **Supplemental:** `NetIncomeLoss` (for quality-of-earnings ratio), `CommonStockSharesOutstanding` (for per-share calculations)

   Filter for `fp == "FY"` entries. Sort by `end` date descending. Collect at least the last five fiscal years when available.

3. **Fetch pre-computed tables (secondary).** If EDGAR data is incomplete or unavailable, fetch:
   - `https://stockanalysis.com/stocks/{ticker}/financials/cash-flow-statement/` — annual cash flow statement

4. **Fetch ratio data (supplementary).** For pre-computed cash flow ratios:
   - `https://stockanalysis.com/stocks/{ticker}/financials/ratios/`

## Analysis Steps

### Operating Cash Flow (OCF)

Extract and analyze the operating activities section:

- **Net cash from operations (OCF).** The headline figure. Compare to net income to assess earnings quality.
- **Depreciation and Amortization (D&A).** A non-cash add-back. Large D&A relative to CapEx suggests aging assets or an asset-light transition.
- **Stock-Based Compensation (SBC).** A non-cash add-back that inflates OCF relative to true cash economics. Compute SBC as a percentage of OCF — a high ratio (above 20 percent) indicates that OCF overstates cash available to shareholders.
- **Working Capital Changes.** Analyze changes in receivables, inventory, payables, and deferred revenue. Growing receivables faster than revenue suggests collection issues. Growing deferred revenue is a positive signal for subscription businesses.

Compute derived operating metrics:

- **OCF Margin** = OCF / Revenue
- **OCF-to-Net-Income Ratio** = OCF / Net Income (quality of earnings indicator; a ratio consistently above 1.0 indicates high-quality earnings backed by cash)

### Investing Activities

Analyze capital deployment:

- **Capital Expenditures (CapEx).** Cash spent on property, plant, and equipment. Distinguish between maintenance CapEx (sustaining existing operations) and growth CapEx (expanding capacity) when disclosures permit.
- **Acquisitions.** Cash spent on business combinations. Large or frequent acquisitions may distort organic growth metrics.
- **CapEx Intensity** = CapEx / Revenue. A high ratio indicates a capital-intensive business. Track the trend — rising CapEx intensity may indicate a growth investment phase or deteriorating capital efficiency.
- **CapEx vs D&A.** When CapEx consistently exceeds D&A, the company is investing in growth. When CapEx falls below D&A, the company may be underinvesting in its asset base.

### Financing Activities

Analyze how the company funds itself and returns capital:

- **Debt Activity.** Net debt issuance minus repayments. Persistent net issuance increases leverage. Aggressive repayment may signal deleveraging.
- **Share Buybacks.** Cash spent repurchasing common stock. Compare to SBC to assess whether buybacks are net accretive or merely offsetting dilution.
- **Dividends.** Cash dividends paid. Compute the dividend payout ratio relative to both net income and FCF.
- **Net Shareholder Return** = Buybacks + Dividends. Compare to FCF to assess sustainability of capital returns.

### Free Cash Flow Metrics

Compute and present the following derived metrics for each period:

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| Free Cash Flow (FCF) | OCF − CapEx | Cash available after maintaining/growing the asset base |
| FCF Margin | FCF / Revenue | Efficiency of converting revenue to free cash |
| FCF per Share | FCF / Diluted Shares Outstanding | Per-share cash generation |
| FCF Growth | (FCF current − FCF prior) / abs(FCF prior) | Year-over-year FCF trajectory |
| Levered FCF | OCF − CapEx (after interest payments already in OCF) | Cash flow to equity holders |
| Unlevered FCF | EBIT × (1 − tax rate) + D&A − CapEx − Change in Working Capital | Cash flow to all capital providers; useful for EV-based valuation |
| FCF-to-Net-Income | FCF / Net Income | Earnings quality adjusted for CapEx |

Present FCF metrics in a multi-year table. Persistent positive FCF indicates the company generates more cash than it consumes. Declining FCF despite rising net income is a red flag — it may indicate aggressive accounting, rising CapEx needs, or working capital deterioration.

### Cash Flow Reconciliation

Walk from net income to OCF to FCF in a waterfall-style table:

```
Net Income → + D&A → + SBC → +/- Working Capital Changes → = OCF → - CapEx → = FCF
```

This reconciliation highlights which non-cash adjustments and working capital movements are most material.

## Depth Handling

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md` for standard formatting rules.

- **Summary depth (default).** Present three years of OCF, CapEx, FCF, FCF margin, and FCF per share in a single table. Include the OCF-to-net-income ratio. Add two to three sentences interpreting trends and quality of earnings.

- **Detailed depth.** Expand to five years. Include the full cash flow reconciliation waterfall, a working capital changes breakdown, a financing activities summary showing buybacks vs dividends vs debt activity, and an unlevered FCF calculation. Provide extended commentary on capital allocation strategy, SBC impact, and sustainability of shareholder returns relative to FCF.

## Sector-Specific Adjustments

- **REITs (Real Estate Investment Trusts).** Standard FCF is not the appropriate measure. Compute:
  - **Funds From Operations (FFO)** = Net Income + D&A on real estate assets − Gains on property sales
  - **Adjusted FFO (AFFO)** = FFO − Maintenance CapEx (recurring capital expenditures)
  - AFFO is the REIT equivalent of FCF and is the basis for REIT valuation and dividend sustainability analysis.

- **Capital-intensive industries (Utilities, Energy, Industrials).** CapEx intensity is structurally high. Focus on the trend in CapEx relative to D&A and the maintenance vs growth CapEx split. Regulatory CapEx (mandated by regulators) should be distinguished from discretionary growth CapEx.

- **Technology / SaaS.** SBC is often a significant component of OCF. Always compute FCF both including and excluding SBC. Capitalized software development costs may reduce reported CapEx — check for `PaymentsForSoftware` or similar concepts.

- **Financial services.** Traditional OCF analysis may not apply cleanly due to the nature of banking cash flows. Focus on net interest income, provision for loan losses, and cash returns to shareholders rather than the standard OCF-CapEx framework.

## Output

Follow the output structure defined in `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md`. Begin with the standard header, present data in markdown tables with right-aligned numbers and units, include source links after each data section, and close with the standard disclaimer.
