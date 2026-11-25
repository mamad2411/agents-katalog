---
name: risk-assessment
description: >
  This skill should be used when the user asks about risks, red flags, accounting quality, risk factors,
  customer concentration, geographic concentration, product concentration, litigation risk, accounting red flags,
  GAAP vs non-GAAP discrepancies, risk assessment, key person risk, or regulatory risk for a publicly
  traded company.
---

# Risk Assessment

## Purpose

Identify, categorize, and evaluate the key business, financial, macroeconomic, and accounting quality risks facing a publicly traded company. Surface red flags that may not be immediately apparent from headline financial metrics, including concentration risks, off-balance-sheet exposures, aggressive accounting practices, and pending litigation. Deliver a prioritized risk inventory that highlights the most material threats to the investment thesis.

## Data Fetching Process

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/data-sources.md` for full data-fetching instructions, ticker resolution, and fallback behavior.

### Step 1 — Resolve Ticker and Retrieve Risk Factor Disclosures

1. Resolve the company ticker to a CIK via the SEC company tickers JSON endpoint.
2. Search for the most recent 10-K filing using the EFTS endpoint: query the company name or ticker with `forms=10-K`.
3. Fetch the 10-K filing and locate the "Risk Factors" section (Item 1A). Extract the key risk categories and specific risks disclosed by management.
4. If the full 10-K is too long to parse, use WebSearch for "{ticker} 10-K risk factors" or "{ticker} annual report risk factors" to find summaries or analyses of the risk disclosures.
5. Note any new risk factors added in the most recent filing compared to prior years, as newly disclosed risks often signal emerging concerns.

### Step 2 — Retrieve Financial Data for Quantitative Risk Signals

1. Fetch the XBRL companyfacts JSON for the resolved CIK.
2. Extract the following metrics for the most recent 5 fiscal years:
   - Revenue by segment or geography (if available in XBRL data; otherwise use WebSearch or 10-K segment disclosures).
   - Total debt (`LongTermDebt`, `ShortTermBorrowings`, or `DebtCurrent`).
   - Interest expense (`InterestExpense`).
   - Operating cash flow vs net income comparison.
   - Accounts receivable (`AccountsReceivableNetCurrent`) growth vs revenue growth.
   - Inventory (`InventoryNet`) growth vs revenue growth.
   - Goodwill (`Goodwill`) and intangible assets (`IntangibleAssetsNetExcludingGoodwill`) as a percentage of total assets.
   - Deferred revenue trends.
3. Fetch pre-computed ratios from Stock Analysis (`/financials/ratios/`) for debt-to-equity, interest coverage, current ratio, and quick ratio.

### Step 3 — Gather Qualitative Risk Intelligence

1. Use WebSearch to find recent news about the company related to:
   - Pending or recent litigation, regulatory investigations, or enforcement actions.
   - Product recalls, safety issues, or quality concerns.
   - Management departures, key person changes, or organizational disruption.
   - Customer losses, contract cancellations, or competitive displacement.
   - Regulatory changes affecting the industry.
2. Search for "{ticker} short seller report" or "{ticker} accounting concerns" to identify any published critiques of the company's accounting or business practices.
3. Search for "{ticker} auditor change" or "{ticker} audit opinion" to check for auditor changes or qualified opinions.

## Analysis Steps

### Step 1 — Assess Business Risks

Evaluate each category of business risk with specific evidence:

**Concentration Risks**
- Customer concentration: identify the percentage of revenue from the top 1, 5, and 10 customers. Flag if any single customer exceeds 10% of revenue (disclosed in 10-K).
- Product concentration: assess revenue diversification across products or services. Flag if a single product line accounts for more than 50% of revenue.
- Geographic concentration: evaluate revenue split by region. Flag heavy dependence on a single country or region.
- Supplier concentration: identify reliance on single-source suppliers for critical inputs.

**Operational Risks**
- Key person risk: assess dependence on a founder, CEO, or small number of key individuals. Consider succession planning quality.
- Technology obsolescence: evaluate whether the company's products or technology face disruption risk from newer alternatives.
- Intellectual property risk: assess the strength and breadth of patent protection, trade secret vulnerability, and IP litigation exposure.
- Supply chain risk: evaluate geographic concentration of manufacturing, sole-source dependencies, and recent supply chain disruptions.

**Litigation and Regulatory Risks**
- List material pending litigation with estimated potential liability where disclosed.
- Identify regulatory investigations or enforcement actions.
- Assess the regulatory environment trajectory: increasing or decreasing regulatory burden.
- Note any recent or pending legislation that could materially affect the business.

Present business risks in a summary table:

| Risk Category | Severity | Evidence | Trend |
|--------------|----------|----------|-------|
| Customer Concentration | Low/Medium/High | [Key fact] | Improving/Stable/Worsening |
| Product Concentration | Low/Medium/High | [Key fact] | Improving/Stable/Worsening |
| ... | ... | ... | ... |

### Step 2 — Assess Financial Risks

**Leverage and Liquidity**
- Calculate net debt to EBITDA ratio and compare to industry norms.
- Assess the debt maturity schedule: identify any large maturities within the next 2-3 years that create refinancing risk.
- Evaluate interest coverage ratio (EBIT / Interest Expense): below 3x is concerning, below 1.5x is critical.
- Assess current ratio and quick ratio for near-term liquidity adequacy.
- Note the availability and size of revolving credit facilities.

**Off-Balance-Sheet Exposures**
- Identify operating lease obligations (now on-balance-sheet under ASC 842, but assess magnitude).
- Look for unconsolidated entities, variable interest entities (VIEs), or joint ventures with contingent liabilities.
- Check for pension or post-retirement benefit obligations that may be underfunded.
- Identify guarantees, indemnifications, or contingent consideration from acquisitions.

**Cash Flow Quality**
- Compare operating cash flow to net income over 5 years. Persistent net income exceeding operating cash flow is a warning sign.
- Calculate free cash flow margin (FCF / Revenue) and assess its stability.
- Evaluate capital expenditure requirements: high maintenance capex reduces true free cash flow.
- Assess working capital trends: rapidly growing receivables or inventory relative to revenue may signal demand softness or channel stuffing.

### Step 3 — Assess Macroeconomic Risks

Evaluate the company's sensitivity to macro factors:

- **Interest rate sensitivity:** Impact of rising/falling rates on borrowing costs, demand for products, and valuation of financial assets.
- **Currency exposure:** Revenue and cost mix by currency. Quantify the FX impact disclosed in filings if available.
- **Commodity exposure:** Dependence on specific commodity prices for input costs or revenue.
- **Trade and tariff risk:** Exposure to international trade policy changes, tariffs, or sanctions.
- **Inflation sensitivity:** Ability to pass through input cost increases to customers (relates to pricing power).
- **Recession sensitivity:** Historical revenue decline during past recessions as a gauge of cyclicality.

### Step 4 — Evaluate Accounting Quality

**Revenue Recognition**
- Identify the revenue recognition policy from the 10-K notes. Flag any aggressive practices such as bill-and-hold, channel stuffing indicators, or long-term contract front-loading.
- Compare revenue growth to cash collected from customers (operating cash flow adjustments).

**GAAP vs Non-GAAP Gap**
- Identify the key adjustments between GAAP and non-GAAP earnings.
- Calculate the GAAP-to-non-GAAP earnings gap as a percentage. A persistent gap exceeding 20-30% warrants scrutiny.
- Assess whether stock-based compensation (the most common adjustment) is growing faster than revenue, which indicates it is a real and increasing cost.
- Flag any unusual or inconsistent non-GAAP adjustments.

**Accrual Quality Signals**
- Calculate the accruals ratio: (Net Income - Operating Cash Flow) / Average Total Assets. High positive accruals suggest earnings may not be sustainable.
- Evaluate accounts receivable days sales outstanding (DSO) trend: increasing DSO may signal aggressive revenue recognition or collection issues.
- Assess inventory days trend: increasing days may signal obsolescence risk or demand weakness.
- Check for changes in accounting estimates (depreciation lives, warranty reserves, bad debt allowances) that could be used to manage earnings.

**Auditor and Disclosure Quality**
- Identify the auditing firm and note any recent auditor changes. A change from a Big Four firm to a smaller firm is a red flag.
- Check for any qualified audit opinions, material weaknesses in internal controls, or restatements.
- Assess the clarity and completeness of footnote disclosures.

Present accounting quality flags in a summary:

| Signal | Finding | Concern Level |
|--------|---------|---------------|
| GAAP vs Non-GAAP Gap | X% gap, driven by [items] | Low/Medium/High |
| Accruals Ratio | X.XX | Low/Medium/High |
| DSO Trend | Increasing/Stable/Decreasing | Low/Medium/High |
| Auditor Changes | None / Changed in [year] | Low/Medium/High |

### Step 5 — Prioritize and Summarize

Rank all identified risks by materiality and likelihood:

1. Assign each risk a severity rating: Low, Medium, or High.
2. Assign each risk a likelihood: Low, Medium, or High.
3. Create a prioritized risk matrix with the top 5-10 risks.
4. Highlight any risks that are both high-severity and high-likelihood as critical risks requiring immediate attention.

Provide an overall risk profile assessment: Low Risk, Moderate Risk, Elevated Risk, or High Risk, with a 2-3 sentence justification.

## Depth Handling

- **Summary depth (default):** Prioritized top 5 risks table with severity and evidence, accounting quality summary (3-4 key signals), and an overall risk profile rating in one paragraph.
- **Detailed depth:** Full analysis of all four risk categories with supporting tables, comprehensive accounting quality review with multi-year trends, macro sensitivity assessment, and detailed risk matrix with mitigation factors.
- **Specific question:** If the user asks about a single risk type (e.g., "What are the accounting red flags for AAPL?"), focus the analysis on that category with full supporting data.

## Output Formatting

Consult `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/output-format.md` for standard output structure, table formatting, source citations, and the required disclaimer.

Lead with the prioritized risk summary table for immediate orientation. Use narrative sections for detailed analysis of each risk category. Always cite the specific SEC filing section, data source, or news article supporting each risk finding.
