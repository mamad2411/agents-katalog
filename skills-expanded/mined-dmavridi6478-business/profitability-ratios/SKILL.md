---
name: profitability-ratios
description: Calculate, explain, and benchmark the 12 key profitability ratios for any business. Use when the user asks about profit margins, ROA, ROE, ROI, ROCE, EPS, P/E ratio, dividend yield/payout, or asks to analyze business profitability. Runs /profitability-ratios or answers questions like "what is my EBIT margin?" Source: Financiario.il / Oana Labes MBA CPA.
---

# 12 Profitability Ratios — Calculator & Interpreter

Given financial data (or a description of a business), calculate, interpret, and benchmark all 12 profitability ratios. Flag which ratios signal strength, weakness, or require investigation.

## The 12 Ratios

### Margin Ratios (Top-Line to Bottom-Line)

| # | Ratio | Formula | What It Measures |
|---|---|---|---|
| 1 | **Gross Profit Margin** | (Gross Profit / Sales) × 100 | % of sales remaining after cost of goods sold |
| 2 | **Contribution Margin** | (Sales - Variable Costs) / Sales × 100 | % of sales remaining after all variable costs |
| 3 | **Operating Profit (EBIT) Margin** | (Operating Profit / Sales) × 100 | % of sales after COGS + operating expenses |
| 4 | **Net Profit (Net Income) Margin** | (Net Profit / Sales) × 100 | % of sales after COGS, operating expenses, interest + taxes |

### Return Ratios

| # | Ratio | Formula | What It Measures |
|---|---|---|---|
| 5 | **Return on Assets (ROA)** | (Net Profit / Total Assets) × 100 | How effectively assets generate profit |
| 6 | **Return on Equity (ROE)** | (Net Profit / Shareholders' Equity) × 100 | Profit per dollar of shareholder equity |
| 7 | **Return on Investment (ROI)** | (Net Investment Profit / Total Investment) × 100 | Efficiency and profitability of a capital investment |
| 8 | **Return on Capital Employed (ROCE)** | EBIT / (Long Term Debt + Equity) × 100 | Return on all long-term capital (equity + debt) |

### Per-Share & Market Ratios

| # | Ratio | Formula | What It Measures |
|---|---|---|---|
| 9 | **Earnings per Share (EPS)** | (Net Profit - Preferred Dividends) / Avg # Shares Outstanding | Profit attributable to each outstanding share |
| 10 | **Price-to-Earnings (P/E) Ratio** | Market Price per Share / Earnings per Share | Stock price relative to earnings — relative valuation |
| 11 | **Dividend Yield Ratio** | Annual Dividend per Share / Market Price per Share | Dividend payout relative to stock price |
| 12 | **Dividend Payout Ratio** | Annual Dividend per Share / Earnings per Share | % of earnings paid out as dividends |

## Process

When given financial data:
1. Calculate all applicable ratios (skip any where data is missing, state why)
2. For each ratio, state: **Value → Industry benchmark → Signal (Strong / Acceptable / Weak / Flag)**
3. Flag any ratios that contradict each other (e.g. high gross margin + low net margin = overhead problem)
4. Summarize in 3 bullets: biggest strength, biggest risk, one action to improve

## Benchmarks (general, adjust by industry)

- Gross Margin: >40% = strong, 20–40% = acceptable, <20% = commodity/low-value
- Net Margin: >10% = strong, 5–10% = acceptable, <5% = thin/at risk
- ROA: >10% = excellent, 5–10% = good, <5% = weak asset utilization
- ROE: >15% = strong, 10–15% = acceptable, <10% = weak
- ROI: >20% = strong, 10–20% = acceptable, <10% = question the investment
- ROCE: should exceed WACC (cost of capital) — if ROCE < WACC, destroying value
- P/E: compare to sector median — significantly above = premium/growth, below = value/distress
- Dividend Payout: >80% = unsustainable, 40–60% = balanced, <30% = reinvesting for growth

## Usage modes

- `/profitability-ratios [company name]` — ask for financials, then calculate all 12
- `/profitability-ratios [paste P&L + Balance Sheet data]` — calculate immediately
- `/profitability-ratios explain [ratio name]` — explain one ratio in depth with example
