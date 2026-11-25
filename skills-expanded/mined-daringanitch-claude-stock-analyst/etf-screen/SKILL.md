---
name: etf-screen
description: ETF overview and analysis. Use when the user asks about an ETF ticker, wants to understand what an ETF holds, or wants a first look at an exchange-traded fund.
---

Run a structured 1-page ETF screen covering:

**1. WHAT IT IS**
- Full name, index tracked, index provider, fund issuer
- Strategy in 1 sentence: what does owning this ETF mean you're betting on?
- Inception date, AUM, average daily volume, expense ratio

**2. WHAT YOU ACTUALLY OWN**
- Top 10 holdings with % weight
- Sector breakdown (% of portfolio)
- Geographic breakdown if relevant
- Number of holdings total — how concentrated vs diversified is it really?

**3. CONCENTRATION RISK**
- Top 5 holdings as % of total portfolio
- If top 10 > 50%: flag as concentrated, not diversified
- Any single-stock dominance (>10% in one name) — name it explicitly

**4. FACTOR TILT**
- What factors does this ETF load on? (growth, value, momentum, quality, size, yield)
- What kind of market environment does it outperform / underperform?
- Beta vs S&P 500 (high/low/negative)

**5. COST & EFFICIENCY**
- Expense ratio vs cheapest alternative covering same exposure
- Tracking error vs benchmark (if available)
- Tax efficiency: does it distribute capital gains? (relevant for taxable accounts)

**6. THE HONEST 1-LINE VERDICT**
One sentence: what is this ETF actually good for, and who should own it?

Flag any data older than 2 quarters. Note if the ETF is thinly traded (avg daily volume <$10M) — liquidity matters at exit.
