---
name: ceo-kpi-framework
description: The CEO KPI Framework - 4 perspectives (financial lagging; customers, employees and skills and innovation leading) with 33 KPIs, each with its formula as printed, plus corrections where the printed formula is wrong or loose. Use when the user wants a CEO or board scorecard, needs a KPI formula, or wants to balance lagging and leading indicators. Source Oana Labes (MBA, CPA) infographic "The CEO KPI Framework" (Batch 103). Extends `c-suite-30-kpis` and `kpi-reference-handbook`.
---

# The CEO KPI Framework: track all 4 perspectives

Lagging (results) = Financial. Leading (drivers) = Customers, Employees, Skills and Innovation. Run `/kpi-scorecard` to build a scorecard from your own numbers.

## Lagging: Financial perspective (18)
| KPI | Formula as printed | Note |
|---|---|---|
| Revenue Growth Rate | Revenue current period / revenue previous period - 1 | Correct |
| Gross Margin | (Total revenue - COGS) / total revenue | Correct |
| Operating Profit Margin | Operating profit / total revenue | Correct |
| Net Profit Margin | Net profit / total revenue | Correct |
| Current Ratio | Current assets / current liabilities | Correct |
| Cash Conversion Cycle | Days inventory outstanding + days sales outstanding - days payable outstanding | Correct |
| Debt Coverage Ratio | EBITDA / (principal + interest) | Loose: usual debt service coverage uses net operating income or cash flow available for debt service; state your definition |
| EBITDA | Earnings before interest, taxes, depreciation and amortization | A measure, not a ratio |
| Cash Flow Coverage Ratio | Operating cash flow / total debt | Correct |
| Cash Conversion Ratio | Cash flow from operations / net income | Correct |
| Return on Assets (ROA) | Net income / total assets | Correct |
| Return on Equity (ROE) | Net income / shareholder's equity | Correct |
| Debt-to-Equity Ratio | Total debt / total equity | Correct |
| Market Capitalization | Total outstanding shares x current share price | Correct (listed companies) |
| Turnover Ratio | Net revenue / total assets | This is asset turnover; name it so |
| Dividend Payout Ratio | Dividends / net income | Correct |
| Earnings per Share (EPS) | Net income / number of outstanding shares | Preferred dividends are normally deducted first |
| Price Earnings (P/E) Ratio | Market value per share / EPS | Correct |

## Leading: Customers perspective (5)
| KPI | Formula as printed | Note |
|---|---|---|
| Customer Churn Rate | (Customers at end - customers at start) / customers at start x 100 | Wrong sign and scope: that is net customer growth. Churn = customers lost in the period / customers at start x 100 |
| Net Promoter Score (NPS) | % promoters - % detractors | Correct |
| Market Share | Company's sales / total industry sales x 100 | Correct |
| Customer Lifetime Value (CLV) | Average revenue per customer x gross margin % x customer lifespan | Correct as a simple form; no discounting |
| Customer Retention Rate | (Customers at end - new customers acquired) / customers at start x 100 | Correct |

## Leading: Employees perspective (5)
| KPI | Formula as printed |
|---|---|
| Total Cost of Workforce | Sum of all costs related to employees (salary, benefits, training, recruitment, etc.) |
| Time to Hire | Days between the job being posted and the offer being accepted |
| Employee Net Promoter Score (eNPS) | (% promoters - % detractors) x 100 |
| Average Employee Tenure | Total years of service of all employees / number of employees |
| % High-Performing Employees Retained | High performers retained / total high performers at start of period x 100 |

Note: NPS above is expressed in points (promoters minus detractors); eNPS is printed with "x 100"; use one convention for both.

## Leading: Skills and innovation perspective (5)
| KPI | Formula as printed |
|---|---|
| Training Participation Rate | Employees in training / total employees x 100 |
| Leadership Development Participation Rate | Employees in leadership programs / eligible employees x 100 |
| Innovation Adoption Rate | New initiatives successfully implemented / total new initiatives proposed x 100 |
| Technology Utilization Rate | Usage rate of key digital tools / total potential usage x 100 |
| Internal Mobility Rate | Employees promoted or moved internally / total employees x 100 |

## Using it
1. Pick 3 to 5 KPIs per perspective, not all 33. A CEO scorecard that tracks everything tracks nothing.
2. Write the formula and data source next to each KPI before the first review; most disputes are about definitions.
3. Pair each lagging KPI with the leading KPI you believe drives it (for example Net Profit Margin with Customer Retention Rate and Time to Hire) and test that belief against 4 quarters of data.
4. Related: `c-suite-30-kpis`, `kpi-reference-handbook`, `kpi-dashboard-design`, `/kpi-dashboard-framework`, `saas-growth-efficiency-metrics`.
