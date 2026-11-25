---
description: Evaluate US stocks with comprehensive fundamental and valuation analysis
---

# US Stock Evaluation

## ⚠️ Data Verification — Do This Before Any Analysis

Before running any analysis, always retrieve the latest market data for the ticker:

1. **Fetch current price** — use web search or ask the user for the live price, 52-week range, and market cap. Never assume a price from training data.
2. **Confirm key figures** — the latest reported quarter and fiscal year (revenue, EPS, margins, FCF), current multiples (P/E, EV/EBITDA, P/FCF) computed from the confirmed price, net debt, and consensus estimates with their date.
3. **State your data source** — fill in the `Data & Sources` header (next section) so the origin, as-of date, retrieval path, and confidence of every figure are explicit at the top of the output.
4. **Flag stale data explicitly** — if live data is unavailable, display this warning before proceeding:

> ⚠️ **Live data unavailable.** The following analysis uses training-data estimates which may be significantly out of date. Verify all prices and metrics before making any decisions.

Never silently substitute training-data estimates for current prices. When in doubt, ask the user to paste the latest quote.

---

## 📋 Data & Sources Header — Open Every Output With It

The first thing in the output is this provenance block, filled in — never left as placeholders. It is the standard documented on the [Data & Accuracy](https://yennanliu.github.io/InvestSkill/data-and-accuracy.html) page and the first thing `result-validator` looks for:

```
Data & Sources
  As of:      <date the figures represent, e.g. 2026-06-30>
  Source:     <primary docs — SEC EDGAR 10-K/10-Q, company IR, FRED, exchange data …>
  Retrieval:  <pasted by user | web/tool retrieval | model memory>
  Confidence: <HIGH | MEDIUM | LOW>
```

- `Retrieval: model memory` must be paired with `Confidence: LOW` — memory is a placeholder until confirmed against a primary source.
- Mixed sources: list each with its own as-of date rather than blending them.
- Sources disagree on the same figure (a closing price, a deal term): prefer the primary source (SEC filing, company release, exchange data) over an aggregator, then the most recent dated one. Show both values with their sources and dates, say which you used and why, and never average them.
- Data the user pasted is reported as `pasted by user`; do not upgrade its confidence beyond what the user's own source supports.

---

## 🌐 Output Language — `--lang zh-TW`

English is the default. With `--lang zh-TW` — or when the user writes in Traditional Chinese and asks for a Chinese answer — write the whole analysis in Traditional Chinese (繁體中文, Taiwan usage), keeping it machine-checkable:

- **Translate** every heading, narrative paragraph, table header and bullet. Give each metric's English name in brackets the first time it appears — 自由現金流（Free Cash Flow, FCF） — so the reader can match it to the glossary and to English analyses.
- **Keep in English** tickers, figures and units, SEC form and item names (10-K Item 7, Form 4), the four `Data & Sources` field labels (`As of`, `Source`, `Retrieval`, `Confidence` — the Retrieval value may be written in Chinese, e.g. 使用者提供), and the Investment Signal box and JSON footer exactly as specified — field names and the BULLISH / NEUTRAL / BEARISH, HIGH / MEDIUM / LOW, BUY / HOLD / SELL, STRONG / MODERATE / WEAK values. Tools parse them.
- Title the invalidation section **論點失效條件（Thesis Invalidation）**, and close with the disclaimer in Chinese: **免責聲明：** 僅供教育用途，非投資建議。
- Use Taiwan financial terms: 殖利率、本益比、營業利益率、自由現金流、聯準會、選擇權、買權／賣權、除息日、預扣稅.

---

Perform comprehensive stock evaluation combining fundamental analysis, valuation modeling, quality scoring, and risk assessment to produce investment-grade conclusions.

## Analysis Components

### 1. Company Overview

- Business model and competitive advantages (moat assessment)
- Market position, addressable market size, and industry trends
- Revenue mix by segment and geographic exposure
- Key products, services, and customer concentration
- Competitive dynamics and threat of disruption

### 2. Financial Health

- Revenue and earnings growth trends (3-year and 5-year CAGR)
- Profit margins: gross margin, operating margin, net margin
- Margin trends: expanding, stable, or compressing
- Balance sheet strength: cash, total debt, net debt, book value
- Liquidity: current ratio, quick ratio, cash conversion cycle
- Cash flow analysis: operating cash flow, free cash flow, FCF yield
- Capital expenditure requirements (maintenance vs. growth capex)
- Working capital management efficiency

### 3. Valuation Metrics

| Metric          | Current | 1-Year Ago | 5-Year Avg | Sector Avg |
|-----------------|---------|------------|------------|------------|
| P/E (TTM)       |         |            |            |            |
| P/E (Forward)   |         |            |            |            |
| PEG Ratio       |         |            |            |            |
| Price/Book      |         |            |            |            |
| Price/Sales     |         |            |            |            |
| EV/EBITDA       |         |            |            |            |
| EV/FCF          |         |            |            |            |
| Dividend Yield  |         |            |            |            |
| Payout Ratio    |         |            |            |            |

### 4. Key Ratios

| Ratio                  | Current | Industry Avg | Assessment |
|------------------------|---------|--------------|------------|
| Return on Equity (ROE) |         |              |            |
| Return on Assets (ROA) |         |              |            |
| Return on Inv. Capital |         |              |            |
| Gross Margin           |         |              |            |
| Operating Margin       |         |              |            |
| Net Margin             |         |              |            |
| Current Ratio          |         |              |            |
| Quick Ratio            |         |              |            |
| Debt-to-Equity         |         |              |            |
| Interest Coverage      |         |              |            |
| Asset Turnover         |         |              |            |

### 5. Peer Comparison

- Direct peer comparison within industry on key valuation multiples
- Historical valuation trends vs. own 5-year history
- Sector performance context and relative positioning
- Market share trends vs. competitors

---

## Deep Financial Statement Analysis

This section provides line-item rigor absorbed from dedicated fundamental analysis workflows. Use when a deeper statement-level breakdown is required.

### Income Statement Line-Item Framework

**Revenue Analysis**
- Break revenue into organic growth vs. acquisition-driven growth vs. FX tailwind/headwind
- Identify top revenue segments by size and growth rate; flag any segment growing faster or slower than the consolidated total
- Assess revenue quality: recurring subscription/contract revenue vs. transactional/one-time revenue
- Operating leverage test: does revenue growth outpace operating expense growth? Calculate incremental operating margin = ΔOperating Income / ΔRevenue

**Cost Structure Decomposition**
- COGS breakdown: raw materials, labor, overhead — track each as % of revenue over 5 years
- SG&A as % of revenue: stable or creeping? Rising SG&A without revenue acceleration signals inefficiency
- R&D intensity: absolute spend and % of revenue — context-dependent (biotech vs. consumer goods)
- Non-recurring items to strip from normalized earnings: restructuring charges, asset write-downs, gain/loss on asset sales, one-time tax benefits, litigation settlements

**Operating Leverage Analysis**
- Fixed vs. variable cost split (estimate from historical margin behavior at different revenue levels)
- Degree of Operating Leverage (DOL) = % Change in Operating Income / % Change in Revenue
- High DOL (>3x) amplifies both upside and downside from revenue swings

| Year | Revenue ($M) | Revenue Growth % | EBIT ($M) | EBIT Growth % | DOL |
|------|-------------|-----------------|-----------|--------------|-----|
| Y-4  |             |                 |           |              |     |
| Y-3  |             |                 |           |              |     |
| Y-2  |             |                 |           |              |     |
| Y-1  |             |                 |           |              |     |
| TTM  |             |                 |           |              |     |

### Working Capital Cycle Analysis

Working capital efficiency directly affects how much cash a business consumes or generates as it grows.

**Key Working Capital Metrics**

| Metric | Formula | Current | Y-1 | Y-2 | Trend |
|--------|---------|---------|-----|-----|-------|
| Days Sales Outstanding (DSO) | Accounts Receivable / (Revenue / 365) | | | | |
| Days Inventory Outstanding (DIO) | Inventory / (COGS / 365) | | | | |
| Days Payable Outstanding (DPO) | Accounts Payable / (COGS / 365) | | | | |
| Cash Conversion Cycle (CCC) | DSO + DIO − DPO | | | | |
| Net Working Capital ($M) | Current Assets − Current Liabilities | | | | |
| NWC as % of Revenue | NWC / Revenue | | | | |

**Cash Conversion Cycle Interpretation**
- **CCC declining**: Company is collecting faster, holding less inventory, and/or extending payables — favorable working capital dynamics, cash generation improves as revenue grows
- **CCC rising**: Working capital is consuming more cash as the business scales — a hidden drag on FCF growth
- **Negative CCC** (e.g., large retailers, subscription businesses): Customers pay before the company pays suppliers — a structural cash flow advantage

**Working Capital as a Growth Funding Check**
- Incremental NWC per $1 of new revenue = ΔNWC / ΔRevenue
- If this ratio exceeds ~15%, rapid revenue growth can strain liquidity even in a profitable business

### DuPont Decomposition

DuPont analysis decomposes ROE into its constituent drivers to identify whether profitability, efficiency, or leverage is the primary return engine — and whether returns are sustainable.

**3-Factor DuPont**

ROE = Net Profit Margin × Asset Turnover × Equity Multiplier

| Component | Formula | Current | Y-1 | Y-2 |
|-----------|---------|---------|-----|-----|
| Net Profit Margin | Net Income / Revenue | | | |
| Asset Turnover | Revenue / Average Total Assets | | | |
| Equity Multiplier | Average Total Assets / Average Shareholders' Equity | | | |
| **ROE** | Margin × Turnover × Multiplier | | | |

**5-Factor DuPont (Extended)**

ROE = Tax Burden × Interest Burden × EBIT Margin × Asset Turnover × Equity Multiplier

| Component | Formula | Current | Y-1 | Y-2 |
|-----------|---------|---------|-----|-----|
| Tax Burden | Net Income / Pre-Tax Income | | | |
| Interest Burden | Pre-Tax Income / EBIT | | | |
| EBIT Margin | EBIT / Revenue | | | |
| Asset Turnover | Revenue / Average Total Assets | | | |
| Equity Multiplier | Average Total Assets / Average Equity | | | |
| **ROE** | Product of all five | | | |

**DuPont Interpretation**
- ROE driven by high **margin** (e.g., luxury brands, software): High-quality, sustainable — least risky driver
- ROE driven by high **asset turnover** (e.g., retailers, distributors): Efficient but thin — watch for margin erosion
- ROE driven by high **leverage** (equity multiplier > 3x): Amplified returns but magnified downside — assess debt sustainability carefully
- Declining ROE: diagnose which factor is deteriorating before drawing conclusions

### Competitive Analysis — Porter's Five Forces

| Force | Intensity (H/M/L) | Key Evidence |
|-------|------------------|--------------|
| Threat of New Entrants | | Capital requirements, brand moats, regulatory barriers |
| Bargaining Power of Suppliers | | Supplier concentration, switching costs, input criticality |
| Bargaining Power of Buyers | | Customer concentration, price sensitivity, alternatives |
| Threat of Substitutes | | Technology disruption, cross-industry competition |
| Competitive Rivalry | | Number of peers, market growth rate, differentiation |

**Overall Moat Assessment**: Wide / Narrow / None
- **Wide moat**: Durable competitive advantage expected to persist 20+ years
- **Narrow moat**: Competitive advantage present but may erode within 10 years
- **No moat**: Competing primarily on price or operational efficiency

### Visualization Data Tables

When a visual or report output is needed, populate these tables for chart generation (compatible with `/us-stock-analysis:report-generator`):

**Revenue & Earnings Growth**
```
Year    Revenue ($M)    Revenue Growth %    Net Income ($M)    EPS ($)
FY-4    [value]         [%]                 [value]            [value]
FY-3    [value]         [%]                 [value]            [value]
FY-2    [value]         [%]                 [value]            [value]
FY-1    [value]         [%]                 [value]            [value]
FY0     [value]         [%]                 [value]            [value]    ← latest reported fiscal year (label with the actual years)
```

**Profit Margin Trends**
```
Year    Gross Margin %    Operating Margin %    Net Margin %    Industry Avg %
2020    [%]              [%]                   [%]             [%]
2021    [%]              [%]                   [%]             [%]
2022    [%]              [%]                   [%]             [%]
2023    [%]              [%]                   [%]             [%]
2024    [%]              [%]                   [%]             [%]
```

**Balance Sheet Composition**
```
Year    Current Assets ($M)    Fixed Assets ($M)    Intangibles ($M)    Total Assets ($M)
2020    [value]               [value]              [value]             [value]
2021    [value]               [value]              [value]             [value]
2022    [value]               [value]              [value]             [value]
2023    [value]               [value]              [value]             [value]
2024    [value]               [value]              [value]             [value]

Year    Current Liab ($M)    Long-term Debt ($M)    Equity ($M)    Total L+E ($M)
2020    [value]             [value]                [value]        [value]
2021    [value]             [value]                [value]        [value]
2022    [value]             [value]                [value]        [value]
2023    [value]             [value]                [value]        [value]
2024    [value]             [value]                [value]        [value]
```

**Cash Flow Waterfall**
```
Component                   Amount ($M)    Notes
Operating Cash Flow         [value]        Core business generation
Capital Expenditures        [value]        Investments in assets
Free Cash Flow             [value]        Available for distribution
Dividends                  [value]        Shareholder distribution
Share Buybacks             [value]        Share repurchases
M&A Activity               [value]        Acquisitions
Debt Repayment             [value]        Debt reduction
Net Cash Change            [value]        Bottom line impact
```

**Valuation Multiples Comparison**
```
Metric              Company    Industry Avg    5-Year Avg    Assessment
P/E Ratio           [value]    [value]         [value]       [Over/Under/Fair]
P/B Ratio           [value]    [value]         [value]       [Over/Under/Fair]
P/S Ratio           [value]    [value]         [value]       [Over/Under/Fair]
EV/EBITDA          [value]    [value]         [value]       [Over/Under/Fair]
PEG Ratio          [value]    [value]         [value]       [Over/Under/Fair]
```

---

## Quality Scoring Framework

### Piotroski F-Score (0–9)

The Piotroski F-Score measures financial strength and operating improvement across 9 binary criteria. Each criterion scores 1 (pass) or 0 (fail). Score of 8–9 is strong; 0–2 is weak.

**Profitability Signals (4 criteria):**

| # | Criterion | Formula | Pass Condition | Score |
|---|-----------|---------|----------------|-------|
| 1 | ROA > 0 | Net Income / Total Assets | Positive ROA in current year | 0 or 1 |
| 2 | Operating Cash Flow > 0 | CFO from cash flow statement | Positive CFO | 0 or 1 |
| 3 | Change in ROA | ROA(t) − ROA(t-1) | ROA improved year-over-year | 0 or 1 |
| 4 | Accruals (quality) | CFO / Total Assets > ROA | Cash earnings exceed reported earnings | 0 or 1 |

**Leverage, Liquidity & Source of Funds (3 criteria):**

| # | Criterion | Formula | Pass Condition | Score |
|---|-----------|---------|----------------|-------|
| 5 | Change in Leverage | Long-term Debt / Avg Assets | Leverage decreased YoY | 0 or 1 |
| 6 | Change in Liquidity | Current Ratio(t) vs (t-1) | Current ratio improved YoY | 0 or 1 |
| 7 | No New Shares Issued | Diluted shares outstanding | No new equity issuance in past year | 0 or 1 |

**Operating Efficiency (2 criteria):**

| # | Criterion | Formula | Pass Condition | Score |
|---|-----------|---------|----------------|-------|
| 8 | Change in Gross Margin | Gross Margin(t) vs (t-1) | Gross margin expanded YoY | 0 or 1 |
| 9 | Change in Asset Turnover | Revenue / Total Assets | Asset turnover improved YoY | 0 or 1 |

**F-Score Interpretation:**
- **8–9**: Strong financial position — high-quality candidate
- **5–7**: Average quality — neutral
- **0–2**: Weak financial position — high risk of deterioration

### Earnings Quality Score

- **Accruals Ratio**: (Net Income − CFO) / Average Total Assets. Low or negative accruals indicate high earnings quality (cash-backed profits).
- **Cash Conversion Rate**: CFO / Net Income. Ratio consistently above 1.0x is positive. Below 0.7x signals potential earnings inflation.
- **Non-Recurring Items**: Identify and strip out restructuring charges, asset write-downs, gains on asset sales, and one-time tax benefits from normalized earnings.
- **Revenue Recognition Risk**: Assess channel stuffing, bill-and-hold arrangements, and aggressive deferred revenue recognition.

---

## ROIC / WACC Analysis

### ROIC Calculation

**ROIC = NOPAT / Invested Capital**

- **NOPAT** (Net Operating Profit After Tax) = EBIT × (1 − effective tax rate)
- **Invested Capital** = Total Equity + Total Debt − Cash and Cash Equivalents
- Alternatively: Invested Capital = Net PP&E + Net Working Capital + Goodwill + Other Long-term Operating Assets

| Component                | Value |
|--------------------------|-------|
| EBIT                     |       |
| Effective Tax Rate       |       |
| NOPAT                    |       |
| Total Equity             |       |
| Total Debt               |       |
| Less: Cash               |       |
| Invested Capital         |       |
| **ROIC**                 |       |

### WACC Calculation

**WACC = (E/V) × Re + (D/V) × Rd × (1 − T)**

- **Cost of Equity (Re)** via CAPM: Re = Rf + β × (Rm − Rf)
  - Rf: Risk-free rate (current 10-year Treasury yield)
  - β: Stock beta (5-year monthly vs. S&P 500)
  - (Rm − Rf): Equity risk premium (historical ~5–6%)
- **Cost of Debt (Rd)**: Weighted average interest rate on outstanding debt
- **Capital Structure Weights**: E/V = market cap / (market cap + total debt), D/V = total debt / (market cap + total debt)
- **Tax Shield**: Multiply Rd by (1 − marginal tax rate) to reflect interest deductibility

| Component              | Value |
|------------------------|-------|
| Risk-Free Rate (Rf)    |       |
| Beta (β)               |       |
| Equity Risk Premium    |       |
| Cost of Equity (Re)    |       |
| Pre-Tax Cost of Debt   |       |
| Tax Rate               |       |
| After-Tax Cost of Debt |       |
| Equity Weight (E/V)    |       |
| Debt Weight (D/V)      |       |
| **WACC**               |       |

### Economic Value Added (EVA)

**EVA = (ROIC − WACC) × Invested Capital**

- **ROIC > WACC**: Company is creating economic value — every dollar invested earns more than its cost. Strong positive signal.
- **ROIC = WACC**: Company is breaking even economically — no value creation or destruction.
- **ROIC < WACC**: Company is destroying shareholder value — capital is deployed below its opportunity cost. Significant warning sign.

ROIC vs. WACC spread trend (expanding = improving value creation, compressing = deteriorating):

| Year    | ROIC | WACC | Spread | EVA |
|---------|------|------|--------|-----|
| Current |      |      |        |     |
| -1 Year |      |      |        |     |
| -2 Year |      |      |        |     |
| -3 Year |      |      |        |     |

---

## DCF Framework

> **A quick DCF, not the valuation of record.** This section gives a fast intrinsic-value range to place the stock in context. For the full model — WACC decomposition, three scenarios, sensitivity tables and comparables — run `stock-valuation`, and when the two disagree, use its number. Both use the same Gordon-growth terminal value; this quick version cross-checks with an EV/EBITDA exit multiple, `stock-valuation` with EV/FCF, so expect small differences.

### Step-by-Step DCF Methodology

**Step 1 — Project Free Cash Flow (Years 1–10)**
- Start with current year base FCF = Operating Cash Flow − Maintenance Capex
- Apply revenue growth rate assumptions (differentiate Phase 1: high growth, Phase 2: fade to stable)
- Apply operating margin assumptions (expanding/stable/compressing)
- Deduct taxes and changes in net working capital
- FCF = NOPAT + D&A − Change in Working Capital − Capex

**Step 2 — Terminal Value Calculation**
- Gordon Growth Model: TV = FCF(Year 10) × (1 + g) / (WACC − g)
- Exit Multiple Method: TV = EBITDA(Year 10) × Terminal EV/EBITDA multiple
- Terminal growth rate (g): typically 2–3% (in line with long-run nominal GDP growth)
- Cross-check both methods for reasonableness

**Step 3 — Discount to Present Value**
- Discount each year's FCF: PV(FCFt) = FCFt / (1 + WACC)^t
- Discount terminal value: PV(TV) = TV / (1 + WACC)^10
- Enterprise Value = Sum of all discounted FCFs + PV(Terminal Value)
- Equity Value = Enterprise Value − Net Debt
- Intrinsic Value Per Share = Equity Value / Diluted Shares Outstanding

### Key Assumptions

| Assumption             | Base Case | Bull Case | Bear Case |
|------------------------|-----------|-----------|-----------|
| Revenue Growth Yr 1–5  |           |           |           |
| Revenue Growth Yr 6–10 |           |           |           |
| Operating Margin       |           |           |           |
| Tax Rate               |           |           |           |
| Capex (% Revenue)      |           |           |           |
| WACC                   |           |           |           |
| Terminal Growth Rate   |           |           |           |
| Terminal EV/EBITDA     |           |           |           |

### Sensitivity Table

Intrinsic value per share at various WACC and terminal growth rate combinations:

| WACC \ Terminal Growth | 1.5%  | 2.0%  | 2.5%  | 3.0%  | 3.5%  |
|------------------------|-------|-------|-------|-------|-------|
| 7%                     |       |       |       |       |       |
| 8%                     |       |       |       |       |       |
| 9%                     |       |       |       |       |       |
| 10%                    |       |       |       |       |       |
| 11%                    |       |       |       |       |       |

### Margin of Safety Assessment

- **Intrinsic Value (Base Case)**:
- **Current Market Price**:
- **Premium / (Discount) to Intrinsic Value**:
- **Margin of Safety**: (Intrinsic Value − Market Price) / Intrinsic Value × 100%
  - > 30% discount: Significant margin of safety — compelling value
  - 10–30% discount: Moderate margin of safety — attractive
  - 0–10% discount: Limited margin of safety — fairly valued
  - Trading at premium: No margin of safety — risk of capital loss if assumptions miss

---

## Management Quality Assessment

### Capital Allocation Track Record

- **ROIC Trend**: Is management generating returns above cost of capital consistently? Review 5-year ROIC history.
- **Acquisition History**: Evaluate past M&A for value creation. Did acquired assets earn above WACC? Were goodwill impairments taken post-acquisition?
- **Buyback Timing**: Did management repurchase shares below intrinsic value? Assess buyback price vs. subsequent performance.
- **Dividend Policy**: Sustainable payout ratio? Dividend growth track record. Balance between dividends, buybacks, and reinvestment.
- **Capex Discipline**: Differentiate growth capex vs. maintenance capex. Asset-light vs. capital-intensive business assessment.

### Guidance Accuracy History (Last 8 Quarters)

| Quarter  | EPS Guidance | EPS Actual | Beat/Miss | Revenue Guidance | Revenue Actual | Beat/Miss |
|----------|-------------|------------|-----------|------------------|----------------|-----------|
| Q1       |             |            |           |                  |                |           |
| Q2       |             |            |           |                  |                |           |
| Q3       |             |            |           |                  |                |           |
| Q4       |             |            |           |                  |                |           |
| Q5       |             |            |           |                  |                |           |
| Q6       |             |            |           |                  |                |           |
| Q7       |             |            |           |                  |                |           |
| Q8       |             |            |           |                  |                |           |
| **Rate** |             |            | X/8       |                  |                | X/8       |

- Beat rate above 75% (6+/8) is strong. Below 50% suggests overpromising or deteriorating visibility.
- Assess guidance conservatism (sandbagging tendency) vs. optimism bias.

### Insider Ownership Alignment

- **CEO ownership** (% of shares outstanding): > 3% meaningful, > 10% highly aligned
- **Board ownership**: Independent directors with meaningful personal stakes indicate alignment
- **Recent insider transactions**: Open-market buys are strongly positive; sells can be routine diversification
- **Insider buy/sell ratio** over past 12 months
- **10b5-1 plan activity**: Scheduled plan sales are less informative than discretionary transactions

### Compensation Structure

- **Pay-for-performance alignment**: Are bonuses and equity vesting tied to ROIC, FCF, and total shareholder return (TSR)?
- **Long-term equity grants**: Stock option or RSU vesting periods (3+ years preferred)
- **CEO pay ratio**: Context for compensation relative to company size and peers
- **Say-on-pay vote**: Shareholder approval percentage in most recent proxy vote
- **Excessive compensation red flags**: Guaranteed bonuses, repriced options, change-of-control severance packages

---

## Analyst Consensus Tracking

### Current Consensus Summary

| Metric               | Value |
|----------------------|-------|
| Buy Ratings          | X (X%) |
| Hold Ratings         | X (X%) |
| Sell Ratings         | X (X%) |
| Mean Price Target    |       |
| High Price Target    |       |
| Low Price Target     |       |
| Current Price        |       |
| Upside to Mean Target|       |
| # of Analysts        |       |

**Consensus interpretation:**
- >70% Buy with >20% upside to mean target: Strong consensus support
- Mixed ratings with tight price target range: Consensus uncertainty
- >30% Sell ratings or mean target below current price: Consensus cautious

### Estimate Revision Trend

Track the direction of earnings estimate changes over time:

| Period       | EPS Estimate (Current FY) | Change vs. 30 Days Ago | Change vs. 90 Days Ago |
|--------------|--------------------------|------------------------|------------------------|
| Current FY   |                          |                        |                        |
| Next FY      |                          |                        |                        |
| Revenue (FY) |                          |                        |                        |

- **Estimates rising**: Positive revision momentum — analysts upgrading expectations
- **Estimates falling**: Negative revision momentum — earnings risk, watch for guidance cuts
- **Stable estimates**: Predictable business with low estimate volatility

### Earnings Estimate Revision Momentum (ERM Signal)

- ERM = (Number of upward revisions − Number of downward revisions) / Total revisions over 30 days
- **ERM > +0.3**: Strong positive momentum — bullish signal
- **ERM −0.3 to +0.3**: Neutral
- **ERM < −0.3**: Negative momentum — bearish signal
- Most reliable when combined with price momentum confirmation

---

## Risk Assessment Matrix

### Business Risk

| Risk Factor        | Level (L/M/H) | Notes |
|--------------------|---------------|-------|
| Industry cyclicality |             |       |
| Competitive intensity |            |       |
| Disruption threat  |               |       |
| Customer concentration |           |       |
| Supplier concentration |           |       |
| Regulatory exposure |              |       |
| ESG / litigation   |               |       |

### Financial Risk

| Risk Factor        | Level (L/M/H) | Notes |
|--------------------|---------------|-------|
| Leverage (Net Debt/EBITDA) |       |       |
| Liquidity (Current Ratio) |        |       |
| Refinancing risk (near-term maturities) |  | |
| Covenant compliance |              |       |
| Pension obligations |              |       |
| Off-balance-sheet items |          |       |

**Leverage thresholds (Net Debt/EBITDA):**
- < 1.0x: Conservative, strong balance sheet
- 1.0–2.5x: Moderate, manageable
- 2.5–4.0x: Elevated, monitor closely
- > 4.0x: High financial risk, limited flexibility

### Valuation Risk

| Scenario                  | Implied Multiple | Notes |
|---------------------------|-----------------|-------|
| Bull case intrinsic value  |                |       |
| Base case intrinsic value  |                |       |
| Bear case intrinsic value  |                |       |
| Current market price       |                |       |
| Premium to bear case       |                |       |

- **Multiple compression scenario**: If sector re-rates to lower multiples (e.g., in rising rate environment), what is the downside?
- **Earnings miss scenario**: What happens to price if EPS misses by 10%? By 20%?
- **Sentiment shift risk**: High-multiple, high-expectation stocks carry disproportionate downside on minor guidance cuts.

### Macro Risk

| Factor              | Impact Level | Current Exposure |
|---------------------|-------------|-----------------|
| Interest rate sensitivity |       |                 |
| USD/FX exposure     |             |                 |
| Commodity cost exposure |         |                 |
| Tariff / trade risk |             |                 |
| Geopolitical exposure |           |                 |
| Regulatory / antitrust |          |                 |

---

## Sector KPI Packs (`--sector`)

Generic operating-company metrics mislead in five sectors. When the user passes `--sector <bank|insurer|reit|biotech|saas>` — or the company is clearly in one of them (SIC code, business description) — **swap the generic metrics for the sector pack, say which pack was applied, and drop the metrics in its "Ignore" line** (or show them only with a note that they are not meaningful here). Pull the KPIs from the 10-K / 10-Q and, where they are not GAAP line items (CET1, occupancy, NRR), from the company's supplemental disclosures, regulatory filings or earnings release — never from memory.

```
/stock-eval ZEPH --sector saas
/financial-report-analyst ZEPH 10-K --sector reit
```

**bank**
- *Swap in:* CET1 ratio vs. its regulatory minimum + buffers · net interest margin (NIM) · efficiency ratio (non-interest expense / revenue) · NPL ratio and net charge-off (NCO) ratio · allowance / loans · loan-to-deposit ratio · deposit beta (Δ deposit cost / Δ policy rate) and uninsured-deposit share · AOCI and held-to-maturity unrealised losses vs. tangible equity · ROTCE · P/TBV
- *Ignore:* P/E as the primary multiple, EV/EBITDA, Altman Z, Beneish, current ratio, DSO/DIO, debt/equity and FCF (deposits and loans are the business, not its financing)
- *Read:* efficiency < 60% is good; NCO ratio against the bank's own cycle history; HTM losses above ~25% of tangible equity are a warning; justify P/TBV with ROTCE (fair P/TBV ≈ ROTCE / cost of equity)

**insurer**
- *Swap in:* combined ratio = loss ratio + expense ratio (P&C) · prior-year reserve development (favourable / adverse, % of opening reserves) · net investment yield and portfolio credit mix · book value per share growth (with and ex-AOCI) · ROE · P/B · solvency: RBC ratio (US) or Solvency II ratio
- *Ignore:* EV/EBITDA, Altman Z, Beneish, FCF, working-capital days, and premium growth as a quality signal (fast growth can mean under-pricing)
- *Read:* combined ratio < 100% = underwriting profit; repeated adverse development is a major flag; BVPS growth plus dividends is the compounding measure; justify P/B with sustainable ROE

**reit**
- *Swap in:* FFO and AFFO per share (NAREIT FFO; AFFO deducts recurring capex, straight-line rent and leasing costs) · P/FFO and P/AFFO · occupancy · same-store NOI growth · weighted average lease expiry (WALE) and the lease-expiry ladder · net debt / EBITDA and fixed-charge coverage · AFFO payout ratio · NAV and implied cap rate
- *Ignore:* EPS and P/E (real-estate depreciation distorts GAAP earnings), Altman X2 (REITs must distribute income), FCF before AFFO adjustments
- *Read:* AFFO payout < ~85% leaves room to grow the dividend, > 100% is unfunded; sector net debt / EBITDA typically runs 5–7×; falling occupancy or negative same-store NOI is the operating warning

**biotech**
- *Swap in:* cash runway in quarters = (cash + investments) / quarterly operating burn · pipeline table (asset, indication, phase, next readout, partner, economics) · probability of success to approval by phase · catalysts (readouts, PDUFA dates, advisory committees) · partnerships (upfronts, milestones, royalties, who holds which rights) · dilution history (shares outstanding over 3–5 years, ATM use, offerings and their discounts)
- *Ignore:* P/E, EV/EBITDA, margins, ROIC, Piotroski F-Score (pre-revenue companies fail it by construction), and DCFs built on management's peak-sales claims
- *Read:* runway < 6 quarters means a raise is near. Rough base rates to approval from industry clinical-success studies (BIO / Informa, all indications): Phase 1 ≈ 8–10%, Phase 2 ≈ 15%, Phase 3 ≈ 50–60%, filed (NDA/BLA) ≈ 90%; oncology runs lower. Risk-adjust every pipeline value by them and hand the dates to `catalyst-calendar`

**saas**
- *Swap in:* ARR and ARR growth · net revenue retention (NRR) and gross revenue retention (GRR) · Rule of 40 (revenue growth % + FCF margin %) · CAC payback (months) = S&M / (net-new ARR × gross margin) × 12 · subscription gross margin · SBC-adjusted FCF margin · RPO and current RPO (cRPO) growth vs. revenue growth
- *Ignore:* GAAP P/E for early-stage names, EV/EBITDA that adds back SBC, headline FCF margin without deducting SBC, current ratio (deferred revenue inflates current liabilities)
- *Read:* NRR > 110% strong, < 100% means the base is shrinking; GRR > 90%; Rule of 40 ≥ 40 on the SBC-adjusted margin; CAC payback < 24 months; cRPO growing slower than revenue is a leading deceleration signal

**How the pack changes the rest of the analysis.** Valuation switches to the sector multiple (P/TBV, P/B, P/AFFO, risk-adjusted pipeline value, EV/ARR or EV/revenue vs. growth); quality uses the sector KPIs in place of the generic margin and ratio checks; risk adds the sector's failure mode (deposit flight and rate marks for banks, reserve inadequacy for insurers, refinancing and occupancy for REITs, trial failure and dilution for biotech, retention decay for SaaS). Everything else — data verification, thesis invalidation and the signal block — is unchanged. State in the output which generic metrics were dropped and why.

---

## Output Format

Provide clear, actionable insights structured as follows:

1. **Investment Thesis Summary** (2–3 sentences capturing the core bull or bear case)
2. **Valuation Assessment**: Undervalued / Fairly Valued / Overvalued, with DCF and multiple-based support
3. **Quality Score**: Piotroski F-Score, Earnings Quality, ROIC vs. WACC verdict
4. **Management Assessment**: Capital allocator quality, guidance credibility, ownership alignment
5. **Analyst Consensus**: Current ratings, price target vs. market, estimate revision direction
6. **Key Risks**: Top 3 risks that could invalidate the thesis
7. **Price Targets**: Bull / Base / Bear case with probability weighting
8. **Recommended Entry Zone**: Based on margin of safety and technical support levels

## Thesis Invalidation

After delivering the analysis signal, specify what would reverse it:

**If signal is BULLISH — thesis breaks if:**
- Piotroski F-Score drops below 3 OR ROIC falls below WACC for 2 quarters
- [One or two more triggers drawn from this analysis's own drivers, each with a threshold]

**If signal is BEARISH — thesis breaks if:**
- F-Score improves to 7+ AND ROIC/WACC spread widens >300bps
- [One or two more triggers drawn from this analysis's own drivers, each with a threshold]

**Re-run this analysis when:**
- [ ] Next earnings release
- [ ] Price moves ±15% from current level
- [ ] 60 days have elapsed
- [ ] Material news event (acquisition, leadership change, regulatory decision)

## Standard Signal Output

All analysis concludes with this standardized block:

In the output, the box below is followed immediately by this machine-readable footer — the same values as the box, filled in (no placeholders, no comments), so tools can read the result without parsing the box:

```json
{"investskill": "1", "skill": "stock-eval", "ticker": "<TICKER, or null for a portfolio / market-wide view>", "as_of": "<YYYY-MM-DD from Data & Sources>", "signal": "<BULLISH | NEUTRAL | BEARISH>", "confidence": "<HIGH | MEDIUM | LOW>", "horizon": "<SHORT-TERM | MEDIUM-TERM | LONG-TERM>", "score": 0.0, "action": "<BUY | HOLD | SELL>", "conviction": "<STRONG | MODERATE | WEAK>", "retrieval": "<pasted by user | web/tool retrieval | model memory>", "sources": ["<each primary source, dated>"]}
```

```
╔══════════════════════════════════════════════╗
║              INVESTMENT SIGNAL               ║
╠══════════════════════════════════════════════╣
║ Signal:      BULLISH / NEUTRAL / BEARISH     ║
║ Confidence:  HIGH / MEDIUM / LOW             ║
║ Horizon:     SHORT / MEDIUM / LONG-TERM      ║
║ Score:       X.X / 10                        ║
╠══════════════════════════════════════════════╣
║ Action:      BUY / HOLD / SELL               ║
║ Conviction:  STRONG / MODERATE / WEAK        ║
╚══════════════════════════════════════════════╝
```

Score Guide: 8.0–10.0 Strongly Bullish | 6.0–7.9 Moderately Bullish | 4.0–5.9 Neutral | 2.0–3.9 Moderately Bearish | 0.0–1.9 Strongly Bearish
Confidence: HIGH (strong data, clear signals) | MEDIUM (mixed signals) | LOW (limited data, conflicting signals)
Horizon: SHORT-TERM (1 week–3 months) | MEDIUM-TERM (3 months–1 year) | LONG-TERM (1+ years)

**Disclaimer:** Educational analysis only. Not financial advice.
