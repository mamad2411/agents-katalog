---
name: etf-portfolio
description: Portfolio analysis for a mix of ETFs. Use when the user has multiple ETFs and wants to understand overlap, hidden concentration, factor exposure, or overall risk across the combined portfolio.
---

Analyze the ETF portfolio provided. The key insight ETF investors miss: owning multiple ETFs does not mean you're diversified — you may be tripling down on the same stocks without knowing it.

**1. UNPACK THE HOLDINGS**
For each ETF, identify:
- Top 10 holdings and weights
- Sector breakdown
- Factor tilt

**2. HIDDEN CONCENTRATION**
- Which single stocks appear across multiple ETFs? List them with combined effective weight
- Flag any stock where combined exposure across all ETFs exceeds 5% of the total portfolio
- Example: owning QQQ + VGT + SOXX = NVDA appears in all three; effective weight may be 15%+ of portfolio

**3. OVERLAP MATRIX**
Build a simple overlap table showing % holdings shared between each ETF pair:

| | ETF A | ETF B | ETF C |
|-|-------|-------|-------|
| ETF A | — | X% | X% |
| ETF B | X% | — | X% |
| ETF C | X% | X% | — |

If any pair >60% overlap: flag as redundant — investor is paying two expense ratios for one position.

**4. FACTOR EXPOSURE**
What is the net factor tilt of the combined portfolio?
- Growth / Value / Momentum / Quality / Size / Yield
- Is this intentional or accidental?

**5. SECTOR CONCENTRATION**
Combined sector weights across all ETFs. What sectors are over/underweight vs a simple S&P 500 benchmark?

**6. MACRO SENSITIVITY**
How does the combined portfolio behave in:
- Rates +100bps
- Recession
- Dollar +10%
- Tech selloff (>20% drawdown in mega-cap tech)

**7. COST DRAG**
Weighted average expense ratio across the portfolio. If >0.20%, identify where the cost is coming from and whether a cheaper equivalent exists.

**8. CONSOLIDATION RECOMMENDATIONS**
Which ETFs are redundant and can be eliminated?
Which single ETF could replace two or more positions?
What's missing entirely?

Output a risk heat map and 2–3 specific rebalancing recommendations with reasoning.
