---
name: financial-report
description: >
  Generate comprehensive financial reports including P&L statements, balance sheet summaries,
  cash flow statements, KPI dashboards, and executive commentary.
  TRIGGER when: user says /financial-report, "generate financial report", "P&L report", "income statement", "financial statements", "board report", "monthly close report".
argument-hint: "[report type] [entity] [period]"
user-invocable: true
---

# Financial Report

Generate clear, accurate financial reports suitable for leadership, board, or investor audiences. This skill covers income statements, balance sheets, cash flow statements, KPI dashboards, and the narrative commentary that ties the numbers together.

---

## Step 1 — Define Report Requirements

Clarify what the audience needs before building the report.

| Parameter            | Description                                        | Example                          |
|----------------------|----------------------------------------------------|----------------------------------|
| Report Type          | P&L, balance sheet, cash flow, full package, KPI   | Full monthly close package       |
| Entity               | Legal entity, business unit, or consolidated        | Consolidated — all entities      |
| Period               | Reporting period                                    | March 2026                       |
| Comparison Basis     | Budget, prior period, prior year, forecast          | Budget + Prior Year              |
| Audience             | Board, executive team, investors, department heads  | Board of Directors               |
| Level of Detail      | Summary, detailed, or drill-down                    | Summary with appendix detail     |
| GAAP / IFRS          | Accounting standard                                 | US GAAP                          |
| Deadline             | When the report is due                              | 10th business day of month       |

### Checklist
- [ ] Month-end close is complete and books are locked
- [ ] All accruals, deferrals, and adjustments posted
- [ ] Intercompany eliminations processed (if consolidated)
- [ ] Revenue recognition reviewed and approved
- [ ] Bank reconciliations completed
- [ ] Trial balance ties to sub-ledgers

---

## Step 2 — Income Statement (P&L)

Build the profit and loss statement with variance analysis.

### P&L Template

| Line Item                    | Current Period | Budget    | Var ($)  | Var (%) | Prior Year | YoY (%)  |
|------------------------------|----------------|-----------|----------|---------|------------|----------|
| **Revenue**                  |                |           |          |         |            |          |
|   Product Revenue            |                |           |          |         |            |          |
|   Services Revenue           |                |           |          |         |            |          |
|   Other Revenue              |                |           |          |         |            |          |
| **Total Revenue**            |                |           |          |         |            |          |
| **Cost of Revenue**          |                |           |          |         |            |          |
|   Direct Costs               |                |           |          |         |            |          |
|   Hosting / Infrastructure   |                |           |          |         |            |          |
|   Customer Support           |                |           |          |         |            |          |
| **Gross Profit**             |                |           |          |         |            |          |
| **Gross Margin %**           |                |           |          |         |            |          |
| **Operating Expenses**       |                |           |          |         |            |          |
|   R&D                        |                |           |          |         |            |          |
|   Sales & Marketing          |                |           |          |         |            |          |
|   General & Administrative   |                |           |          |         |            |          |
| **Total OpEx**               |                |           |          |         |            |          |
| **Operating Income (EBIT)**  |                |           |          |         |            |          |
| **Operating Margin %**       |                |           |          |         |            |          |
|   Interest Expense           |                |           |          |         |            |          |
|   Other Income / (Expense)   |                |           |          |         |            |          |
| **Pre-Tax Income**           |                |           |          |         |            |          |
|   Income Tax                 |                |           |          |         |            |          |
| **Net Income**               |                |           |          |         |            |          |
| **Net Margin %**             |                |           |          |         |            |          |

### Variance Commentary Rules
- Explain any line item with variance > 5% or > $25K (whichever is smaller).
- Lead with the business reason, not the accounting entry.
- Note if the variance is timing (will reverse) or permanent.

---

## Step 3 — Balance Sheet Summary

Present the financial position at period end.

### Balance Sheet Template

| Line Item                       | Current Period | Prior Period | Change ($) | Change (%) |
|---------------------------------|----------------|--------------|------------|------------|
| **Assets**                      |                |              |            |            |
|   Cash & Equivalents            |                |              |            |            |
|   Accounts Receivable (net)     |                |              |            |            |
|   Prepaid Expenses              |                |              |            |            |
|   Other Current Assets          |                |              |            |            |
| **Total Current Assets**        |                |              |            |            |
|   Property & Equipment (net)    |                |              |            |            |
|   Intangible Assets             |                |              |            |            |
|   Goodwill                      |                |              |            |            |
|   Other Non-Current Assets      |                |              |            |            |
| **Total Assets**                |                |              |            |            |
| **Liabilities**                 |                |              |            |            |
|   Accounts Payable              |                |              |            |            |
|   Accrued Liabilities           |                |              |            |            |
|   Deferred Revenue              |                |              |            |            |
|   Current Portion of Debt       |                |              |            |            |
| **Total Current Liabilities**   |                |              |            |            |
|   Long-Term Debt                |                |              |            |            |
|   Other Non-Current Liabilities |                |              |            |            |
| **Total Liabilities**           |                |              |            |            |
| **Equity**                      |                |              |            |            |
|   Common Stock                  |                |              |            |            |
|   Retained Earnings             |                |              |            |            |
|   Other Equity                  |                |              |            |            |
| **Total Equity**                |                |              |            |            |
| **Total Liabilities + Equity**  |                |              |            |            |

### Key Balance Sheet Ratios

| Ratio                    | Formula                                    | Current | Target / Benchmark |
|--------------------------|--------------------------------------------|---------|--------------------|
| Current Ratio            | Current Assets / Current Liabilities       |         | > 1.5              |
| Quick Ratio              | (Cash + AR) / Current Liabilities          |         | > 1.0              |
| Debt-to-Equity           | Total Debt / Total Equity                  |         | < 1.0              |
| Days Sales Outstanding   | (AR / Revenue) x Days in Period            |         | < 45 days          |
| Days Payable Outstanding | (AP / COGS) x Days in Period               |         | 30–60 days         |

---

## Step 4 — Cash Flow Statement

Show how cash moved during the period.

### Cash Flow Statement Template

| Line Item                            | Current Period | Prior Period | Budget    |
|--------------------------------------|----------------|--------------|-----------|
| **Operating Activities**             |                |              |           |
|   Net Income                         |                |              |           |
|   + Depreciation & Amortization      |                |              |           |
|   + Stock-Based Compensation         |                |              |           |
|   +/- Changes in Working Capital     |                |              |           |
|     Change in Accounts Receivable    |                |              |           |
|     Change in Prepaid Expenses       |                |              |           |
|     Change in Accounts Payable       |                |              |           |
|     Change in Deferred Revenue       |                |              |           |
|     Change in Accrued Liabilities    |                |              |           |
| **Net Cash from Operations**         |                |              |           |
| **Investing Activities**             |                |              |           |
|   Capital Expenditures               |                |              |           |
|   Acquisitions                       |                |              |           |
| **Net Cash from Investing**          |                |              |           |
| **Financing Activities**             |                |              |           |
|   Debt Proceeds / (Repayments)       |                |              |           |
|   Equity Issuance / (Buybacks)       |                |              |           |
| **Net Cash from Financing**          |                |              |           |
| **Net Change in Cash**               |                |              |           |
| Beginning Cash Balance               |                |              |           |
| **Ending Cash Balance**              |                |              |           |

---

## Step 5 — KPI Dashboard

Present the metrics that matter most to the audience.

### SaaS / Subscription KPIs

| KPI                          | Current Period | Prior Period | Trend    | Target   |
|------------------------------|----------------|--------------|----------|----------|
| ARR (Annual Recurring Rev.)  |                |              |          |          |
| MRR (Monthly Recurring Rev.) |                |              |          |          |
| Net New ARR                  |                |              |          |          |
| Gross Revenue Retention      |                |              |          |          |
| Net Dollar Retention         |                |              |          |          |
| CAC (Customer Acq. Cost)     |                |              |          |          |
| LTV (Lifetime Value)         |                |              |          |          |
| LTV:CAC Ratio                |                |              |          | > 3:1    |
| CAC Payback (months)         |                |              |          | < 18     |
| Rule of 40 Score             |                |              |          | > 40     |
| Burn Multiple                |                |              |          | < 2.0    |

### General Business KPIs

| KPI                          | Current Period | Prior Period | Trend    | Target   |
|------------------------------|----------------|--------------|----------|----------|
| Revenue Growth (YoY)         |                |              |          |          |
| Gross Margin %               |                |              |          |          |
| EBITDA Margin %              |                |              |          |          |
| Free Cash Flow               |                |              |          |          |
| Headcount                    |                |              |          |          |
| Revenue per Employee         |                |              |          |          |
| OpEx as % of Revenue         |                |              |          |          |

---

## Step 6 — Executive Commentary

Write the narrative that accompanies the numbers.

### Commentary Structure

1. **Performance Headline**: One sentence summarizing the period (e.g., "Revenue exceeded plan by 8% driven by strong enterprise pipeline conversion").
2. **Revenue Commentary**: What drove revenue performance; notable deals; pipeline outlook.
3. **Margin Commentary**: Gross margin trends; OpEx efficiency; any one-time impacts.
4. **Cash Position**: Cash balance, runway, notable cash events (collections, payments).
5. **Key Wins**: Major accomplishments, deals closed, milestones hit.
6. **Key Risks / Concerns**: Items requiring attention; potential headwinds.
7. **Outlook**: Forward-looking guidance or forecast adjustments.

### Commentary Best Practices
- Lead with "so what" — the insight, not the data point.
- Quantify everything ("improved by $50K" not "improved significantly").
- Separate one-time events from ongoing trends.
- Connect financial performance to operational drivers.
- Keep the total commentary to 1–2 pages maximum.

---

## Output Format

```
## Financial Report — [Entity] — [Period]

### 1. Executive Summary & Commentary
[1-page narrative with key highlights, risks, and outlook]

### 2. Income Statement
[P&L with budget and prior year variance]

### 3. Balance Sheet
[Condensed balance sheet with key ratio callouts]

### 4. Cash Flow Statement
[Three-section cash flow with ending balance]

### 5. KPI Dashboard
[Relevant KPI table based on business model]

### 6. Variance Analysis
[Detailed explanation of material variances]

### 7. Appendix
- Departmental P&L detail
- Revenue bridge (prior period to current)
- Headcount summary
- Glossary of terms (for board/investor audience)
```

---

## Quality Checklist

- [ ] Income statement foots correctly (revenue - costs = net income)
- [ ] Balance sheet balances (assets = liabilities + equity)
- [ ] Cash flow reconciles to balance sheet cash change
- [ ] All material variances (> 5% or > $25K) are explained
- [ ] KPIs are consistent with the financial statements
- [ ] Commentary is factual, forward-looking, and concise
- [ ] Report has been reviewed by a second set of eyes
- [ ] Formatting is consistent and professional
- [ ] Prior period figures match the previously published report

---

## Edge Cases

| Scenario                                 | Handling Approach                                                             |
|------------------------------------------|-------------------------------------------------------------------------------|
| Restatement of prior period              | Clearly mark restated figures; explain reason; show before/after comparison   |
| Partial period (stub period)             | Annualize cautiously; label metrics as "annualized" vs. "actual"             |
| Multi-entity consolidation               | Show eliminations line; provide segment-level detail in appendix             |
| Board requesting non-GAAP metrics        | Present GAAP first; reconcile to non-GAAP (e.g., adjusted EBITDA)           |
| Late-breaking adjustment after report    | Issue an addendum; do not silently revise the published report               |
| First report for a new entity            | No prior period comparison available; benchmark against plan or industry      |
