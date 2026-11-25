---
name: etf-compare
description: Side-by-side ETF comparison. Use when the user wants to compare two or more ETFs, decide between ETFs covering the same space, or understand the difference between similar funds.
---

Run a side-by-side comparison of the ETFs provided. Structure:

**1. WHAT EACH ONE IS**
One sentence per ETF: strategy, index tracked, issuer.

**2. SIDE-BY-SIDE SCORECARD**

| Metric | [ETF 1] | [ETF 2] |
|--------|---------|---------|
| AUM | | |
| Expense ratio | | |
| # of holdings | | |
| Top holding (% weight) | | |
| Top 10 as % of portfolio | | |
| 1yr return | | |
| 3yr annualized | | |
| Beta vs S&P 500 | | |
| Avg daily volume | | |

**3. OVERLAP ANALYSIS**
- What % of holdings do they share?
- If overlap >70%: flag — owning both is redundant
- Where they diverge: what does one own that the other doesn't?

**4. WHAT YOU'RE ACTUALLY CHOOSING BETWEEN**
- Is this a cost decision? (same exposure, different fee)
- Is this a conviction decision? (different index methodology = different bet)
- Is this a liquidity decision? (one trades much more thinly)
- Is this a tax decision? (different distribution behavior)

**5. FACTOR DIFFERENCES**
Which ETF loads more heavily on: growth / value / momentum / quality / size?
Under what market conditions does each outperform the other?

**6. VERDICT: WHICH ONE AND WHY**
Give a clear recommendation. If the answer is genuinely "it depends," explain on what — don't hedge without a reason.

If the user provides more than 2 ETFs, run the comparison as a ranked table and eliminate the weakest option first with a clear explanation.
