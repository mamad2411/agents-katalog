---
name: kpi-reference-handbook
description: Reference library of ~44 standard financial KPIs across 8 categories (Profitability, Efficiency, Liquidity, Financial Structure, Cash, Investor/Valuation) with name, what it measures, and formula, plus an 8-step process for turning any KPI into an action plan (set goals → gather data → understand the ratio → calculate → interpret → compare to prior period/budget → compare to industry → risk assessment and action plan). Use when someone needs a specific financial ratio/formula, is building a KPI dashboard or financial report, needs to explain what a metric like EBITDA margin or the cash conversion cycle means, or wants a structured process for turning raw financial data into a decision.
---

# KPI Reference Handbook

Source: reviewed from an uploaded infographic — "KPIs Handbook" (Bojan
Radojicic, promotional material for a paid handbook sold at
robojan.gumroad.com). The infographic itself is an ad for that product;
the KPIs and formulas it lists are standard, well-known financial metrics
(not proprietary to that book), so they're reproduced here as a reference
library the way `business-decision-frameworks` reproduces MoSCoW/RICE/OKRs
— say so if asked, and point anyone who wants the fuller handbook to the
original product rather than presenting this skill as a substitute for it.

No prompts or repos here — this is a formula reference, used the way
`business-decision-frameworks` is: look up the KPI that matches the
question, don't run all of it top to bottom.

## The 8-step process

Before treating any single KPI as an answer, run it through this
sequence — most KPI misuse comes from stopping at step 4:

1. **Set KPI goals and objectives** — decide what decision this KPI is
   meant to inform before calculating it.
2. **Gather the data** — the inputs the formula needs, at the right time
   period and consistently defined.
3. **Understand the meaning of the ratio** — what it actually measures,
   not just its name.
4. **Apply the formula for calculation.**
5. **Result interpretation** — what the number means in context, not in
   isolation.
6. **Compare with last period and budget** — a KPI without a trend or a
   target is just a number.
7. **Industry comparison** — the same number can be strong in one
   industry and weak in another.
8. **Risk assessment and action plan** — the point of the whole exercise:
   what changes because of what this KPI showed.

## Profitability KPIs

| KPI | Measures | Formula |
|---|---|---|
| EBITDA Margin | Ability to generate profit from operations, excluding financing decisions, tax, and non-cash expenses | EBITDA / Revenues |
| Gross Profit Margin | Profitability of core operations after direct costs of producing/delivering goods or services | Gross profit / Revenues |
| Net Profit Margin | Overall profitability after all expenses (COGS, indirect costs, opex, taxes) | Net profit / Revenues |
| Return on Equity (ROE) | Return earned by shareholders on their equity investment | Net profit / Equity |
| Return on Capital Employed (ROCE) | Profitability from both equity and debt capital combined | Net profit / (Equity + Long-term debt) |
| Return on Assets (ROA) | How effectively total assets are used to generate profit | Net profit / Total assets |
| Revenue per Employee | Workforce efficiency — higher generally means more effective use of headcount | Revenues / Employee number |
| EBITDA per Employee | How effectively employees contribute to operating profit before financing/tax/non-cash items | EBITDA / Employee number |
| Net Profit per Employee | Overall workforce productivity in generating profit | Net profit / Employee number |

## Efficiency KPIs

| KPI | Measures | Formula |
|---|---|---|
| Days Sales Outstanding (DSO) | How long it takes to collect receivables from credit sales | Average accounts receivable / Revenues × 365 |
| Days Inventory Outstanding (DIO) | How long it takes to sell the entire inventory (a.k.a. Days Sales of Inventory) | Average inventories / COGS × 365 |
| Days Payable Outstanding (DPO) | How long the company takes to pay its own suppliers/vendors | Average accounts payable / COGS × 365 |
| Cash Conversion Cycle (CCC) Days | Time to convert investments into cash inflow from sales — working-capital efficiency | DSO + DIO − DPO |
| Assets Turnover | Efficiency of generating revenue relative to total assets | Revenues / Average assets |
| Fixed Assets Turnover | Same as assets turnover, scoped to fixed assets only | Revenues / Average fixed assets |
| EBITDA to Interest Coverage | Ability to cover interest expense with EBITDA — a solvency signal for creditors | EBITDA / Interest expenses |
| Total Cost per Employee | Average all-in cost per employee over a period | Total costs / Employee number |
| Overhead Costs per Employee | Average overhead (not directly attributable to a specific product) per employee | Overhead costs / Employee number |

## Liquidity KPIs

| KPI | Measures | Formula |
|---|---|---|
| Net Working Capital | Capital available to fund day-to-day operations; positive means short-term obligations are covered | Accounts receivable + Inventories − Accounts payable |
| Current Assets − Current Liabilities | Absolute liquid surplus available for upcoming liabilities — a persistently high figure can signal an overly conservative investment policy | Current assets − Current liabilities |
| Current Ratio | Ability to cover short-term liabilities with short-term assets (benchmark: 1–3) | Current assets / Current liabilities |
| Quick Ratio (acid-test) | Ability to meet short-term obligations with the most liquid assets only (benchmark: ≥1) | (Current assets − Inventories) / Current liabilities |
| Cash Ratio | How much of current liabilities pure cash covers, without converting receivables/inventory first | Cash / Current liabilities |
| Working Capital Turnover | Relationship between net working capital and total assets | (Current assets − Current liabilities) / Total assets |

## Financial Structure KPIs

| KPI | Measures | Formula |
|---|---|---|
| Equity Ratio | Proportion of total assets funded by equity — financial leverage and stability | Equity / (Total Equity and Liabilities) |
| Debt Ratio | Proportion of total assets funded by debt — financial risk and dependency on debt financing | Debt / (Total Equity and Liabilities) |
| Interest Expense in Loans | Cost of borrowing — interest paid on the principal over a period | Interest expense / Loan amount |
| Total COGS in Revenue | Gross-profit structure — a higher share means lower gross profit | COGS / Revenue |
| Variable COGS in Revenue | Gross-profit structure — a higher variable-COGS share means lower gross profit but a lower breakeven point | Variable COGS / Revenue × 100 |
| Fixed COGS in Revenue | Gross-profit structure — a higher fixed-COGS share means a higher breakeven point | Fixed COGS / Revenue × 100 |

## Cash KPIs

| KPI | Measures | Formula |
|---|---|---|
| Operating Cash Flow | Cash generated/spent in core business activity, excluding financing and investing | Net Income + D&A − NWC increase |
| Free Cash Flow (FCF) | Cash available for new investment, dividends, or debt repayment after operating and investing costs | Operating Cash Flow + Cash Flow from Investing |
| Cash Conversion Cycle | Average days between paying liabilities and collecting cash (same metric as the Efficiency section's CCC Days) | DSO + DIO − DPO |
| Free Cash Flow Rate | Share of sales left as free cash flow after operating and investing costs | FCF / Sales |
| Free Cash Flow Realization | How well profit converts into actual cash | FCF / Net Income |
| Cash Ratio (liabilities view) | How many dollars of cash cover each dollar of *total* liabilities — a broader denominator than the Liquidity section's Cash Ratio, which uses only *current* liabilities | Cash / Total liabilities |

## Investor / Valuation KPIs

| KPI | Measures | Formula |
|---|---|---|
| Price-to-Earnings (P/E) | Relationship between stock price and earnings per share | Market price per share / Earnings per share |
| Price-to-Sales (P/S) | Relationship between company value and revenue | Market capitalization (or valuation) / Total revenue |
| Price-to-Book (P/B) | Relationship between stock price and book value per share | Market capitalization / Book value |
| Enterprise Value-to-EBITDA (EV/EBITDA) | Relationship between total enterprise value and EBITDA | Enterprise value / EBITDA |
| Price-to-Cash-Flow (P/CF) | How much investors pay per dollar of operating cash flow | Market capitalization / Cash flow from operations |
| Dividend Yield | Share of stock price returned annually as dividends | Annual dividend per share / Stock price |

Note: the source lists "Cash Ratio" twice, once under Liquidity (against
*current* liabilities — the standard definition) and once under Cash
(against *total* liabilities — a broader variant). Both are kept above,
labeled distinctly, rather than silently merged, since they answer
different questions.

## Related skills in this repo

- **business-intelligence-report**, **ceo-reporting-skill**: pull specific
  KPIs from here rather than re-deriving formulas when building a report;
  this skill is the formula reference, those are the reporting/narrative
  layer on top of it.
- **business-decision-frameworks**: the same reference-library pattern,
  for prioritization/roadmap/storytelling frameworks instead of financial
  ratios — the two are companions.
- **quarterly-okr-architect**: KPIs from here can become the measurable
  targets a goal cascade tracks against.
- **data-cleanup-brief-service**: the "clean file, then AI narrative"
  discipline in that skill applies directly here — calculate these ratios
  from a verified clean data source before any AI-drafted commentary
  references them.
