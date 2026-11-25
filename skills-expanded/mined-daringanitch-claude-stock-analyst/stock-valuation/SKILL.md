---
name: stock-valuation
description: Valuation framework for a stock. Use when the user asks about valuation, fair value, price target, DCF, or whether a stock is cheap or expensive.
---

Build a valuation summary across four methods:

**1. RELATIVE VALUATION**
- Current EV/EBITDA, P/E, P/S vs 3-year average and sector peers
- Premium or discount: justified or not?

**2. DCF (base case)**
- Revenue CAGR assumption (years 1–5, years 6–10)
- FCF margin at maturity
- Discount rate used and why
- Implied share price

**3. REVERSE DCF**
- What growth rate is the current stock price implying?
- Is that achievable given historical growth and market size?

**4. PRIVATE MARKET VALUE**
- What would a strategic acquirer pay? Cite recent comparable M&A multiples.

Output a table showing implied price per share under bear / base / bull for each method. Flag where assumptions diverge most from consensus.
