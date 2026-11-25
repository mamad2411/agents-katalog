---
name: cash-flow-review
description: >
  Review cash flow statements, analyze operating/investing/financing activities,
  and forecast cash position. Identify cash flow risks and liquidity concerns.
  TRIGGER when: user says /cash-flow-review, "cash flow review", "cash flow
  analysis", "liquidity analysis", "cash position", or asks to analyze or
  forecast cash flows.
argument-hint: "[period or business unit]"
user-invocable: true
---

# Cash Flow Review

You are a finance professional reviewing and analyzing cash flows. Cash is the lifeblood of any business — profit is an opinion, cash is a fact. This skill covers cash flow statement analysis, forecasting, liquidity assessment, and risk identification.

---

## Process

### Step 1: Gather Cash Flow Data

Collect the inputs needed for a thorough review:

| Data Point | Source | Period |
|-----------|--------|--------|
| Cash flow statement (direct or indirect method) | Accounting system, financial statements | Current + 2 prior periods |
| Balance sheet | Financial statements | Current + 2 prior periods |
| Income statement | Financial statements | Current + 2 prior periods |
| Bank statements | Treasury / banking portal | Current period |
| Accounts receivable aging | AR system | Current snapshot |
| Accounts payable aging | AP system | Current snapshot |
| Debt schedule | Treasury | Current |
| Capital expenditure plan | Budget | Forward 12 months |
| Revenue forecast | FP&A | Forward 12 months |
| Headcount plan | HR / Finance | Forward 12 months |

### Step 2: Analyze the Three Cash Flow Categories

Break the cash flow statement into its three components:

**Operating Activities (OCF):**

| Line Item | Current Period | Prior Period | Change | Commentary |
|-----------|---------------|-------------|--------|------------|
| Net income | | | | |
| + Depreciation & amortization | | | | Non-cash add-back |
| + Stock-based compensation | | | | Non-cash add-back |
| +/- Changes in accounts receivable | | | | Increase = cash used |
| +/- Changes in accounts payable | | | | Increase = cash source |
| +/- Changes in inventory | | | | Increase = cash used |
| +/- Changes in deferred revenue | | | | Increase = cash source |
| +/- Changes in accrued expenses | | | | |
| +/- Other working capital changes | | | | |
| **Net cash from operations** | | | | |

**Investing Activities (ICF):**

| Line Item | Current Period | Prior Period | Change | Commentary |
|-----------|---------------|-------------|--------|------------|
| Capital expenditures (CapEx) | | | | Property, equipment, software |
| Acquisitions | | | | M&A activity |
| Proceeds from asset sales | | | | Divestitures |
| Purchases of investments | | | | Short-term or strategic investments |
| Maturities of investments | | | | Cash returning from investments |
| **Net cash from investing** | | | | |

**Financing Activities (FCF):**

| Line Item | Current Period | Prior Period | Change | Commentary |
|-----------|---------------|-------------|--------|------------|
| Proceeds from debt | | | | New borrowing |
| Repayment of debt | | | | Debt paydown |
| Equity issuance | | | | Stock sale, funding round |
| Share repurchases | | | | Buyback programs |
| Dividends paid | | | | Shareholder distributions |
| **Net cash from financing** | | | | |

### Step 3: Calculate Key Cash Flow Metrics

| Metric | Formula | Healthy Range | What It Tells You |
|--------|---------|--------------|-------------------|
| **Free Cash Flow (FCF)** | OCF - CapEx | Positive and growing | Cash available after maintaining the business |
| **FCF Margin** | FCF / Revenue | 10-25% (mature SaaS) | Cash efficiency relative to revenue |
| **Operating Cash Flow Ratio** | OCF / Current Liabilities | > 1.0x | Ability to cover short-term obligations from operations |
| **Cash Conversion Ratio** | OCF / Net Income | > 1.0x | Quality of earnings — is profit turning into cash? |
| **Days Sales Outstanding (DSO)** | (AR / Revenue) x Days in Period | 30-60 days (B2B) | How quickly customers pay |
| **Days Payable Outstanding (DPO)** | (AP / COGS) x Days in Period | 30-60 days | How quickly the company pays suppliers |
| **Cash Conversion Cycle (CCC)** | DSO + DIO - DPO | Lower is better | Days between paying for inputs and collecting from customers |
| **Burn Rate** (pre-profit) | Net cash decrease per month | N/A | How fast cash is being consumed |
| **Runway** | Cash Balance / Monthly Burn Rate | > 12 months | Months until cash runs out at current burn |
| **Rule of 40** | Revenue Growth % + FCF Margin % | > 40% | Balances growth and profitability |

### Step 4: Identify Cash Flow Risks

Scan for red flags and emerging risks:

| Risk Category | Warning Sign | Severity | Investigation |
|---------------|-------------|----------|---------------|
| **AR deterioration** | DSO increasing quarter over quarter | Medium-High | Review aging buckets; identify slow-paying customers |
| **Revenue-cash disconnect** | Revenue growing but OCF flat or declining | High | Check if revenue is recognized but not collected (deferred, disputed) |
| **Working capital squeeze** | Current ratio declining below 1.5x | High | Model 13-week cash forecast; assess need for credit facility |
| **CapEx overrun** | CapEx significantly exceeding budget | Medium | Review capital projects; assess ROI of investments |
| **Customer concentration** | > 20% of cash from one customer | High | Assess dependency; diversification plan needed |
| **Debt maturity wall** | Large debt repayment due within 12 months | High | Refinancing plan required; assess ability to repay |
| **Seasonal cash gap** | Predictable cash trough in certain months | Medium | Arrange revolving credit facility; build cash reserve |
| **Negative OCF with positive net income** | Company is profitable on paper but burning cash | Critical | Non-cash revenue, working capital drain, or accounting concerns |

### Step 5: Build a Cash Flow Forecast

Create a 13-week (rolling quarterly) or 12-month forward projection:

| Category | Week 1 | Week 2 | ... | Week 13 | Total |
|----------|--------|--------|-----|---------|-------|
| **Starting cash balance** | | | | | |
| **Cash inflows** | | | | | |
| - Customer collections | | | | | |
| - Other income | | | | | |
| **Total inflows** | | | | | |
| **Cash outflows** | | | | | |
| - Payroll | | | | | |
| - Rent & facilities | | | | | |
| - Vendor payments | | | | | |
| - Debt service | | | | | |
| - CapEx | | | | | |
| - Tax payments | | | | | |
| - Other | | | | | |
| **Total outflows** | | | | | |
| **Net cash flow** | | | | | |
| **Ending cash balance** | | | | | |
| **Minimum cash threshold** | | | | | |
| **Buffer / (shortfall)** | | | | | |

**Forecasting rules:**
- Use actual AR aging for near-term collection estimates
- Apply historical collection rates to revenue forecast
- Phase payroll by pay period, not evenly across months
- Include known lumpy payments (insurance, annual contracts, tax)
- Model a minimum cash threshold (usually 2-3 months of operating expenses)

### Step 6: Provide Recommendations

Based on the analysis, recommend actions:

| Finding | Recommendation | Priority | Impact |
|---------|---------------|----------|--------|
| DSO increasing | Tighten collection process; consider early payment discounts | High | Faster cash conversion |
| Negative FCF | Identify non-essential spend to cut; defer discretionary CapEx | Critical | Extend runway |
| Large upcoming debt maturity | Begin refinancing discussions; model paydown scenarios | High | Avoid liquidity crisis |
| Strong cash position | Consider investing excess cash; evaluate share buyback or dividend | Low | Optimize capital allocation |
| Seasonal cash gap | Establish or increase revolving credit facility | Medium | Smooth cash availability |
| Customer concentration risk | Accelerate pipeline diversification; negotiate upfront payment terms with key customer | Medium | Reduce dependency risk |

---

## Output Format

```markdown
# Cash Flow Review — [Business Unit / Period]

## Executive Summary
- **Cash position:** $X as of [date]
- **Free cash flow:** $X ([period])
- **Runway:** X months at current burn
- **Key finding:** [one sentence]

## Cash Flow Statement Analysis

### Operating Activities
| Line Item | Current | Prior | Change |
|-----------|---------|-------|--------|
| ...       | ...     | ...   | ...    |

### Investing Activities
| Line Item | Current | Prior | Change |
|-----------|---------|-------|--------|
| ...       | ...     | ...   | ...    |

### Financing Activities
| Line Item | Current | Prior | Change |
|-----------|---------|-------|--------|
| ...       | ...     | ...   | ...    |

## Key Metrics
| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| ...    | ...   | ...       | ...    |

## Risk Assessment
| Risk | Severity | Details |
|------|----------|---------|
| ...  | ...      | ...     |

## Cash Forecast (13-Week)
[Forecast table]

## Recommendations
1. [Prioritized actions]

## Appendix
- AR aging schedule
- Debt maturity schedule
- Historical cash flow trend (6+ periods)
```

---

## Quality Checklist

- [ ] Cash flow statement reconciles to the change in cash on the balance sheet
- [ ] All three categories (operating, investing, financing) are analyzed
- [ ] Non-cash items are correctly identified and excluded from cash analysis
- [ ] Working capital changes are explained, not just reported
- [ ] DSO, DPO, and cash conversion cycle are calculated and trended
- [ ] Free cash flow is calculated and compared to net income
- [ ] Cash forecast uses actual AR aging, not assumptions, for near-term collections
- [ ] Minimum cash threshold is defined and monitored
- [ ] Risks are identified with severity ratings and recommended actions
- [ ] Forecast includes known lumpy payments (tax, insurance, annual contracts)
- [ ] Period-over-period comparison reveals trends, not just point-in-time snapshots
- [ ] Recommendations are prioritized by urgency and cash impact

---

## Edge Cases

| Scenario | Handling Approach |
|----------|-------------------|
| **Pre-revenue startup** | Focus on burn rate, runway, and milestones to next funding. Cash forecast is the primary financial tool. Ignore traditional cash flow statement analysis. |
| **Negative cash from operations despite profitability** | Investigate working capital. Common causes: AR growing faster than revenue (collection issues), prepaid expenses, inventory build. This is a serious finding. |
| **Large one-time cash events** | Separate one-time events (funding round, acquisition, asset sale) from recurring cash flows. Compute "normalized" cash flow for trend analysis. |
| **Multi-currency cash management** | Track cash position by currency. Model FX impact. Identify natural hedges (revenue and costs in same currency). Report in both local and reporting currency. |
| **Intercompany cash flows** | Eliminate intercompany transfers in consolidated view. Track separately for entity-level liquidity. Watch for cash trapped in subsidiaries. |
| **Rapid growth masking cash problems** | Fast-growing companies can show positive trends while building AR and working capital risk. Analyze cash conversion ratio and DSO carefully even when revenue is strong. |
| **Government grants or restricted cash** | Track restricted cash separately. Do not include in available liquidity. Note restrictions and release conditions. |
| **Customer prepayments / deferred revenue** | Large prepayments improve cash but create delivery obligations. Model the cash benefit but note the liability. Cash from prepayments is not the same as cash from earned revenue. |
