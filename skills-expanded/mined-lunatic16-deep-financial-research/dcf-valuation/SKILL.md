---
name: dcf-valuation
description: Performs discounted cash flow (DCF) valuation to estimate intrinsic value per share. Uses Financial Datasets MCP for fundamentals. Triggers when user asks for fair value, intrinsic value, DCF, valuation, "what is X worth", undervalued/overvalued, or price target analysis.
license: Complete terms in LICENSE.txt
---

# DCF Valuation Subskill

Performs discounted cash flow (DCF) valuation analysis to estimate intrinsic value per share. This subskill integrates with the **deep-financial-research** skill and uses the **Financial Datasets MCP** server for data.

> 🔗 Parent skill: [`../../SKILL.md`](../../SKILL.md)

## When to Trigger

### Activate For:
- "What is [ticker] worth?"
- "DCF valuation for [company]"
- "Intrinsic value of [stock]"
- "Fair value estimate"
- "Is [stock] undervalued/overvalued?"
- "Price target based on fundamentals"
- "Run a DCF on [ticker]"

### Don't Trigger For:
- Simple price queries
- Technical analysis requests
- Comparable company analysis (use deep-financial-research instead)

## Step 1: Gather Financial Data (via Financial Datasets MCP)

Request the following data using Financial Datasets MCP tools:

### 1.1 Cash Flow History
**Request:** Annual free cash flow for the last 5 years
**Extract:** `free_cash_flow` for each year
**Fallback:** Calculate as `operating_cash_flow - capital_expenditure`

### 1.2 Financial Metrics
**Request:** Current fundamentals snapshot
**Extract:** 
- `market_cap`
- `enterprise_value`
- `pe_ratio`
- `debt_to_equity`
- `return_on_equity` or `return_on_invested_capital`
- `shares_outstanding`

### 1.3 Balance Sheet
**Request:** Latest balance sheet
**Extract:**
- `total_debt` (short-term + long-term)
- `cash_and_equivalents`
- `total_assets`

### 1.4 Current Price
**Request:** Real-time stock price
**Extract:** `price` with timestamp

### 1.5 Company Facts
**Request:** Company profile
**Extract:** `sector`, `industry`

## Step 2: Calculate FCF Growth Rate

### Calculate 5-Year FCF CAGR
```
CAGR = (Ending FCF / Beginning FCF)^(1/n) - 1
```

### Growth Rate Selection Logic
| FCF Pattern | Approach |
|-------------|----------|
| Stable positive growth | Use CAGR with 10-20% haircut |
| Volatile/negative FCF | Use analyst estimates or industry avg |
| High growth (>20%) | Cap at 15% (sustained high growth is rare) |

### Cross-Validation
Compare with:
- Historical revenue growth
- Analyst EPS growth estimates
- Industry average growth rates

## Step 3: Estimate Discount Rate (WACC)

### Default Assumptions
| Component | Base Value |
|-----------|------------|
| Risk-free rate | 4.0% (10Y Treasury) |
| Equity risk premium | 5.5% |
| Cost of debt (pre-tax) | 5.5% |
| Tax rate | 25% |

### WACC Formula
```
WACC = (E/V × Re) + (D/V × Rd × (1-T))

Where:
- E = Market value of equity
- D = Market value of debt
- V = E + D (total value)
- Re = Cost of equity (Rf + β × ERP)
- Rd = Cost of debt
- T = Tax rate
```

### Sector Adjustments
| Sector | WACC Adjustment |
|--------|-----------------|
| Technology | +0.5% to +1.0% (higher risk) |
| Utilities | -0.5% to -1.0% (stable cash flows) |
| Healthcare | +0.0% to +0.5% |
| Financials | Use cost of equity only |
| Consumer Staples | -0.5% (defensive) |
| Energy | +1.0% to +1.5% (cyclical) |
| Industrials | +0.0% to +0.5% |

### Reasonableness Check
- WACC should be 2-4% below ROIC for value-creating companies
- Typical range: 7-12% for mature companies

## Step 4: Project Future Cash Flows

### Years 1-5 Projections
Apply growth rate with annual decay:
```
Year 1: FCF₀ × (1 + g)
Year 2: FCF₁ × (1 + g × 0.95)
Year 3: FCF₂ × (1 + g × 0.90)
Year 4: FCF₃ × (1 + g × 0.85)
Year 5: FCF₄ × (1 + g × 0.80)
```

### Terminal Value (Gordon Growth Model)
```
Terminal Value = FCF₅ × (1 + g_terminal) / (WACC - g_terminal)

Where g_terminal = 2.5% (GDP growth proxy)
```

## Step 5: Calculate Present Value

### Discount Projected FCFs
```
PV(FCF) = FCF / (1 + WACC)^n
```

### Calculate Enterprise Value
```
Enterprise Value = Σ PV(FCF Years 1-5) + PV(Terminal Value)
```

### Calculate Equity Value
```
Equity Value = Enterprise Value - Net Debt
Net Debt = Total Debt - Cash
```

### Calculate Fair Value Per Share
```
Fair Value Per Share = Equity Value / Shares Outstanding
```

## Step 6: Sensitivity Analysis

Create 3×3 matrix varying:
- **WACC:** Base ±1%
- **Terminal Growth:** 2.0%, 2.5%, 3.0%

Example output:
```
                Terminal Growth
WACC        |   2.0%   |   2.5%   |   3.0%   |
------------|----------|----------|----------|
Base - 1%   |   $XXX   |   $XXX   |   $XXX   |
Base        |   $XXX   |   $XXX   |   $XXX   |
Base + 1%   |   $XXX   |   $XXX   |   $XXX   |
```

## Step 7: Validate Results

### Sanity Checks

1. **EV Comparison**
   - Calculated EV should be within 30% of reported enterprise_value
   - If off by >30%, revisit WACC or growth assumptions

2. **Terminal Value Ratio**
   - Terminal Value / Total EV should be 50-80% for mature companies
   - If >90%: growth rate may be too high
   - If <40%: near-term projections may be aggressive

3. **P/FCF Cross-Check**
   - Fair value should approximate FCF/share × 15-25 for mature companies

## Step 8: Output Format

```markdown
### DCF Valuation: [Company] ([TICKER])

#### Valuation Summary
| Metric | Value |
|--------|-------|
| **Current Price** | $XX.XX |
| **Fair Value** | $XX.XX |
| **Upside/(Downside)** | +XX.X% |
| **Verdict** | Undervalued / Fairly Valued / Overvalued |

#### Key Assumptions
| Input | Value | Source/Notes |
|-------|-------|--------------|
| Current FCF | $X.XXB | Financial Datasets (TTM) |
| FCF Growth Rate (5Y) | X.X% | Based on [CAGR/analyst estimates] |
| Terminal Growth | 2.5% | GDP growth proxy |
| WACC | X.X% | [Sector] adjustment applied |
| Shares Outstanding | X.XXB | Financial Datasets |
| Net Debt | $X.XXB | Debt - Cash |

#### Projected Free Cash Flows
| Year | FCF ($B) | Growth | PV ($B) |
|------|----------|--------|---------|
| Year 1 | $X.X | X.X% | $X.X |
| Year 2 | $X.X | X.X% | $X.X |
| Year 3 | $X.X | X.X% | $X.X |
| Year 4 | $X.X | X.X% | $X.X |
| Year 5 | $X.X | X.X% | $X.X |
| Terminal | $XX.X | 2.5% | $XX.X |

#### Sensitivity Analysis
| WACC \ Terminal | 2.0% | 2.5% | 3.0% |
|-----------------|------|------|------|
| [WACC-1%] | $XXX | $XXX | $XXX |
| [Base WACC] | $XXX | $XXX | $XXX |
| [WACC+1%] | $XXX | $XXX | $XXX |

#### Validation Checks
- ✅ Calculated EV within 30% of reported EV
- ✅ Terminal Value = XX% of Total EV (reasonable range)
- ✅ Implied P/FCF of XX.x (within 15-25 range)

#### Caveats
- DCF models are sensitive to input assumptions
- Growth rates may not be sustainable
- WACC estimates involve judgment
- Terminal value represents XX% of total value
- Does not account for [company-specific risks]

**Conclusion:** At $XX.XX, [TICKER] appears [undervalued/fairly valued/overvalued] relative to our DCF-derived fair value of $XX.XX. Key value drivers include [top 2-3 factors].
```

## Integration with Deep Financial Research

This subskill can be called as part of the deep-financial-research workflow:

1. **After** gathering fundamentals and market data
2. **Before** presenting final investment thesis
3. **Use DCF output** to support valuation conclusion

### Example Integration
```
After completing the company deep dive:
- "Now running DCF valuation to estimate intrinsic value..."
- [Execute DCF workflow]
- "Our DCF suggests [X%] upside/downside, supporting our [bullish/neutral/bearish] stance"
```

## Example Interactions

**User:** "What's NVDA worth based on DCF?"
→ Execute full DCF workflow with Financial Datasets MCP

**User:** "Is Apple undervalued?"
→ Run DCF, compare fair value to current price

**User:** "Run a DCF on Microsoft as part of your analysis"
→ Execute DCF subskill within deep-financial-research workflow

**User:** "Show me the sensitivity analysis for Tesla's valuation"
→ Emphasize Step 6 (Sensitivity Analysis) in output

## Caveats

- DCF is only as good as its assumptions
- High-growth companies are harder to value with DCF
- Cyclical companies require normalized FCF
- Financial companies need different approach (DDM or residual income)
- Always present DCF as one input among many, not definitive answer
