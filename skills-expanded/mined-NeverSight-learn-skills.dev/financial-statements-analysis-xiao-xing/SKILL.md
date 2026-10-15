---
name: financial-statements-analysis-xiao-xing
description: "Analyze company financials using Xiao Xing's three-statement framework. Trigger on: \"read this balance sheet\", \"is this company profitable\", \"analyze financials\", \"ROIC vs WACC\", \"cash flow health\"."
license: "Skill distillation for personal/educational use. Do not reproduce source passages verbatim."
---

# Financial Statement Analysis (肖星·一本书读懂财报)

## Overview

This skill applies Xiao Xing's (Tsinghua University) integrated three-statement framework to analyze company financials for investors, managers, and MBA students. It covers balance sheet structure, income statement logic, cash flow patterns, ratio analysis, and the ROIC-vs-WACC test for identifying genuinely good companies.

## When to Use This Skill

- User shares or describes a company's financial statements
- Questions about profitability, liquidity, solvency, or cash flow
- "Is this a good company?" / "Is this company worth investing in?"
- Requests to interpret specific accounting items (receivables, depreciation, R&D, goodwill)
- M&A due diligence questions about hidden liabilities
- Comparing companies across industries using common-size analysis

## Core Principle

Financial statements are a language. The balance sheet is a **snapshot** (照相机) of what a company owns and owes at a point in time; the income statement is a **video** (摄像机) of how it performed over a period; the cash flow statement is the **truth-teller** that shows whether profits are real. All three must be read together — and the ultimate test of a good company is whether ROIC exceeds WACC.

---

## DIMENSION 1: Balance Sheet Structure

**The Rule:** A balance sheet reveals both where money went (assets) and where it came from (liabilities + equity) — and shareholders are the last to be paid, bearing all residual risk and reward.

### Key questions to ask:
- What % of assets are receivables? (High % → weak pricing power or aggressive revenue recognition)
- What is the liquidity ratio? (Current assets / Current liabilities — below 1 is a warning)
- How much of financing comes from interest-bearing debt vs. operating payables?
- Are there significant intangible assets or goodwill that could be written down?
- What is the equity ratio (equity / total assets)?

### Decision criteria / Checklist:
- [ ] Current ratio ≥ 1.5 (comfortable liquidity buffer)
- [ ] Receivables / Total assets < 20% (unless industry norm is higher)
- [ ] Debt-to-asset ratio < 60% for manufacturing; < 80% only acceptable for asset-heavy utilities
- [ ] Assets recorded at historical cost — check for revaluation or fair-value exceptions
- [ ] No large off-balance-sheet obligations flagged in notes

### Warning signals:
- Receivables growing faster than revenue → collection problems or inflated sales
- Goodwill spike after acquisitions → potential future impairment
- Short-term debt used to finance long-term assets → maturity mismatch risk
- Equity turning negative → insolvency territory

### Agent instruction:
When asked to analyze a balance sheet, apply the accounting equation (Assets = Liabilities + Equity), decompose assets into current/non-current, flag any items with high receivables or debt concentration, and summarize the company's financial structure in plain language.

---

## DIMENSION 2: Income Statement Logic

**The Rule:** Revenue recognition follows the accrual principle (not cash receipt), so the income statement shows economic performance — but not necessarily cash reality.

### Key questions to ask:
- What is the gross margin trend? (Compression = pricing pressure or rising costs)
- Are operating expenses (sales, admin, finance) growing faster than revenue?
- Is non-operating income (gains on asset sales, subsidies) inflating net profit?
- What is the effective tax rate — is it sustainable?

### Five-step income waterfall:
1. Revenue − COGS = **Gross Profit**
2. − Operating expenses = **Operating Profit**
3. ± Non-operating items = **Pre-tax Profit**
4. − Income tax = **Net Profit**
5. ÷ Shares outstanding = **EPS**

### Decision criteria / Checklist:
- [ ] Gross margin stable or expanding over 3 years
- [ ] Net margin > industry average
- [ ] Non-operating income < 20% of net profit (core business earns the profit)
- [ ] No large one-off items distorting the trend

### Warning signals:
- Revenue growing but gross margin shrinking → cost pressures or pricing concessions
- Net profit rising but operating profit flat → non-recurring gains propping up the number
- R&D capitalized rather than expensed → inflated short-term profit, hidden future write-offs

### Agent instruction:
When analyzing profitability, walk through all five steps of the income waterfall. Highlight the source of profit (core operations vs. non-operating), flag margin trends, and note any accounting choices (R&D treatment, revenue recognition policies) that affect comparability.

---

## DIMENSION 3: Cash Flow Pattern Diagnosis

**The Rule:** Cash flow is harder to manipulate than accrual income. The pattern of operating / investing / financing cash flows reveals a company's true life-cycle stage and financial health.

### Four archetype patterns:
| Pattern | Operating CF | Investing CF | Financing CF | Interpretation |
|---------|-------------|-------------|-------------|----------------|
| Healthy growth | + | − | ± | Earns cash, reinvests it — classic growth |
| Mature harvest | + | + | − | Earns cash, selling assets, paying down debt |
| Startup/turnaround | − | − | + | Burning cash, expanding, needs external funding |
| Red flag | + | + | + | All inflows — possible asset stripping or manipulation |

### Key questions to ask:
- Is operating cash flow consistently greater than net income? (Depreciation adds back; working capital changes matter)
- Is the company funding capex from operations or from debt?
- Does free cash flow (Operating CF − Capex) trend positive?

### Decision criteria / Checklist:
- [ ] Operating CF > Net income over a 3-year average (high quality earnings)
- [ ] Free cash flow positive for mature businesses
- [ ] Investing CF negative = investment-mode (acceptable if operations are healthy)
- [ ] Financing CF positive for startups; negative (debt repayment, dividends) for mature firms

### Warning signals:
- Operating CF negative while net profit positive → earnings may be fictional
- Financing CF rising every year → increasingly dependent on external capital
- Operating + Investing + Financing all positive → potential asset disposal or manipulation

### Agent instruction:
When asked about cash flow health, classify the company into one of the four archetypes, compute free cash flow if data is available, and compare operating CF to net income. State clearly whether earnings quality is high or suspect.

---

## DIMENSION 4: Ratio Analysis Toolkit

**The Rule:** No single ratio tells the full story. Use profitability, efficiency, liquidity, and solvency ratios together, always benchmarked against industry norms and the company's own history.

### Profitability ratios:
- **Gross margin** = Gross profit / Revenue
- **Net margin** = Net profit / Revenue
- **ROE** = Net profit / Equity (DuPont: Net margin × Asset turnover × Leverage)
- **ROIC** = Tax-after operating profit / Invested capital (Equity + interest-bearing debt)

### Efficiency ratios:
- **Receivables turnover** = Revenue / Average receivables (higher = faster collection)
- **Inventory turnover** = COGS / Average inventory (higher = less capital tied up)
- **Asset turnover** = Revenue / Total assets (higher = more efficient asset use)

### Liquidity ratios:
- **Current ratio** = Current assets / Current liabilities (> 1.5 comfortable)
- **Quick ratio** = (Cash + Receivables) / Current liabilities (> 1.0 safe)

### Solvency ratios:
- **Debt-to-asset ratio** = Total liabilities / Total assets
- **Interest coverage** = Operating profit / Interest expense (> 3x healthy)

### Agent instruction:
When computing ratios, always state the industry context (e.g., "retail companies typically run 20–30% gross margins"). Present ratios in a table with a one-line interpretation for each. Flag any ratio that deviates significantly from industry norms.

---

## DIMENSION 5: Three-Statement Integration

**The Rule:** Balance sheet, income statement, and cash flow are one interconnected system — net income flows into retained earnings; depreciation in the income statement reconciles to investing cash flow; working capital changes link the balance sheet to operating cash flow.

### Linkage map:
- Net income → Retained earnings (Balance Sheet equity)
- Depreciation charge → Added back in Operating CF; reduces PPE on Balance Sheet
- Increase in receivables → Reduces operating CF (cash not yet collected)
- Increase in payables → Increases operating CF (cash not yet paid out)
- Capex → Investing CF outflow; increases PPE on Balance Sheet

### Common-size analysis (同型分析):
- Income statement: Express all items as % of revenue → reveals cost structure
- Balance sheet: Express all items as % of total assets → reveals capital allocation

### Agent instruction:
When asked to do a comprehensive analysis, always cross-check the three statements for consistency: verify that net income reconciles with cash flow from operations (after adjustments), that capex matches asset changes on the balance sheet, and that equity changes tie to net income minus dividends.

---

## DIMENSION 6: Good Company Test (ROIC vs. WACC)

**The Rule:** A company truly "makes money" only when its Return on Invested Capital (ROIC) exceeds its Weighted Average Cost of Capital (WACC). Revenue and profit growth alone are insufficient — a company can grow and simultaneously destroy shareholder value.

### ROIC calculation:
- **Invested Capital** = Equity + Interest-bearing debt (exclude non-interest payables like accounts payable, wages payable, taxes payable)
- **Tax-after operating profit** ≈ Net profit + After-tax interest expense
- **ROIC** = Tax-after operating profit / Invested Capital

### WACC components:
- **Cost of equity** (CAPM): Risk-free rate + Beta × Equity risk premium
- **Cost of debt** (after-tax): Interest rate × (1 − Tax rate)
- **WACC** = Weighted average of both

### Verdict thresholds:
| Outcome | Meaning |
|---------|---------|
| ROIC > WACC | Value-creating company — worthy of investment premium |
| ROIC ≈ WACC | Neutral — earns exactly its cost of capital |
| ROIC < WACC | Value-destroying — growth makes things worse, not better |

### Warning signals:
- High revenue growth + ROIC < WACC = value destruction at scale
- High net margin but low asset turnover → may still fail the ROIC test
- Apple benchmark: High ROIC driven by brand premium + asset-light supply chain model

### Agent instruction:
When asked whether a company is "good" or "worth investing in," always calculate or estimate ROIC and compare to an appropriate WACC. Explain why profit growth alone is not sufficient evidence of value creation.

---

## DIMENSION 7: Industry Context & Strategic Positioning

**The Rule:** The same ratio means different things in different industries. Financial data reflects industry structure (capital intensity, cycle, competition) and strategic choices (cost leadership vs. differentiation).

### Three-layer analysis:
1. **Industry environment**: Is it capital-intensive? Cyclical? Highly competitive?
2. **Strategic positioning**: Cost leadership (thin margins, high turnover) vs. differentiation (fat margins, lower turnover)?
3. **Execution capability**: Is the strategy working? Are the numbers moving in the right direction?

### Industry fingerprints:
| Industry type | Typical characteristics |
|--------------|------------------------|
| Capital-intensive (paper, steel) | Low margins, high asset turnover, cyclical, high depreciation |
| Consumer electronics | Low margins, fast inventory turns, intense competition, R&D heavy |
| Software/platform | High gross margins, low capex, high ROE, scalable |
| Banking | High leverage, interest spread as "margin", capital adequacy ratios matter |

### Agent instruction:
Always establish industry context before interpreting ratios. State the industry norm explicitly, then compare the company's metrics against it. Identify the company's strategic positioning and assess whether the financial data is consistent with that strategy.

---

## Query Response Framework

### Query Type 1: "Analyze this company's financial statements"
1. **Identify industry** — state context and norms
2. **Balance sheet snapshot** — structure, liquidity, leverage (Dimension 1)
3. **Income waterfall** — margins, profit quality (Dimension 2)
4. **Cash flow archetype** — classify health stage (Dimension 3)
5. **Key ratios table** — profitability, efficiency, liquidity, solvency (Dimension 4)
6. **Three-statement cross-check** — consistency verification (Dimension 5)
7. **ROIC vs. WACC verdict** (Dimension 6)
8. **Summary verdict**: Healthy / Concerns / Red flags

### Query Type 2: "Is this a good company / worth investing in?"
1. Confirm ROIC data is available or estimable
2. Compute or estimate ROIC vs. WACC (Dimension 6)
3. Check cash flow quality (Dimension 3)
4. Assess strategic positioning vs. industry (Dimension 7)
5. State verdict with supporting evidence

### Query Type 3: "Explain this accounting item" (receivables, goodwill, deferred revenue, etc.)
1. Define the item in plain language
2. Explain where it appears across the three statements
3. State what it reveals about the business
4. Flag any warning signals associated with it (Dimension 1 or 2)

### Query Type 4: "Compare these two companies"
1. Common-size both income statements and balance sheets (Dimension 5)
2. Build a side-by-side ratio table (Dimension 4)
3. Identify industry positioning differences (Dimension 7)
4. Compare ROIC vs. WACC for each (Dimension 6)
5. State which company shows stronger fundamentals and why

---

## Output Format

For comprehensive analyses, use this structure:

```
## [Company Name] — Financial Analysis

### Industry Context
[1–2 sentences on industry norms]

### Balance Sheet (Snapshot)
[3–5 bullet points on key structural observations]

### Income Statement (Performance)
[3–5 bullet points: margins, profit sources, trends]

### Cash Flow (Health)
**Pattern:** [Archetype name]
[2–3 bullet points]

### Key Ratios
| Category | Ratio | Value | vs. Industry | Signal |
|----------|-------|-------|-------------|--------|
| Profitability | Gross Margin | X% | Above/Below | ✅/⚠️/🚨 |
| ...

### ROIC vs. WACC
ROIC: X% | WACC: ~X% | **Verdict: Value-creating / Neutral / Value-destroying**

### Overall Verdict
[2–3 sentences: is this a healthy, investable, or risky company?]
```

---

## Critical Reminders

1. **Accrual ≠ Cash.** Profit on the income statement does not mean cash in the bank. Always cross-check with operating cash flow.
2. **ROIC > WACC is the only real profitability test.** Net profit growth without ROIC > WACC destroys shareholder value.
3. **Liabilities are more dangerous than assets in due diligence.** Hidden contingent and off-balance-sheet liabilities are harder to detect than overvalued assets.
4. **Context is everything.** A 5% net margin is excellent in retail; it is mediocre in software. Always state the industry benchmark.
5. **Historical cost is not market value.** Balance sheet assets reflect purchase price, not current worth — especially relevant for real estate, investments, and intangibles.
6. **Cash flow archetypes reveal lifecycle stage.** A startup burning cash is not the same as a mature company doing so — context determines whether the pattern is a warning or a feature.
7. **DuPont decomposition reveals the source of ROE.** High ROE from high leverage is very different from high ROE from high margins — decompose before concluding.
