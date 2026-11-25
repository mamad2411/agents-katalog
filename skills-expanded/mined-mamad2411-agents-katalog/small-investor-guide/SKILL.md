---
name: small-investor-guide
description: Nancy Dunnan incremental investing framework — budget-tiered guidance
  ($50→$50k+) using openbb-finance MCP tools for real market data
version: 1.0.0
author: Hermes Agent (Skillmate)
license: MIT
metadata:
  hermes:
    tags:
    - finance
    - investing
    - personal-finance
    - dunnan
    - small-investor
    - budget-tiers
    - MCP
    related_skills: []
    triggers:
    - investing guide
    - small investor
    - nancy dunnan
    - budget investing
    - incremental investing
    - personal finance guide
---

# Small-Investor Guide

Nancy Dunnan's incremental investing framework — guide users through progressive budget tiers, using real market data via OpenBB finance MCP tools. Each tier sets a *when-to-move-up* trigger so the agent tailors advice to the user's stated investable amount without flooding them with all tiers at once.

## Domain Concept

Dunnan's ladder is about **progressing through financial vehicles as available capital grows**, not about picking specific stocks at every tier. The core sequence:

1. **Safety first** — emergency fund (3-6 months expenses) before any investing
2. **Tax-advantaged first** — IRAs, 401(k)s, SEPs, HSAs before taxable accounts
3. **Compound early** — even $50 in a high-yield savings or money market starts the habit
4. **Diversify gradually** — bonds at $1k, stock funds at $2k, REITs/corporate bonds at $5k+
5. **Stay scam-aware** — no promissory notes, no "guaranteed returns," no crypto-lending at any tier

## Tiers

| Tier | Threshold | Vehicles | Trigger to Next |
|------|-----------|----------|-----------------|
| 1 | $50–$500 | HYSA, money market, savings bonds | Consistently saving $50/mo without dipping |
| 2 | $500–$1,000 | CDs, Treasury bills (I/EE bonds), high-yield savings | User mentions "retirement" or $1k sustained |
| 3 | $1,000–$2,000 | Roth IRA, traditional IRA, 401(k), SEP IRA, utility stocks (if tax-advantaged maxed) | Tax-advantaged account opened and funded |
| 4 | $2,000–$5,000 | Broad-market stock index funds (VTI, VOO), Treasury bonds (T-bills, T-notes), REIT ETFs | Portfolio diversified across 3+ asset types |
| 5 | $5,000+ | Corporate bonds, REITs, sector ETFs, dividend-growth stocks, covered calls | User expresses interest in income generation |

## Steps

### 1. Assess User's Upfront Investable Amount
Ask or infer the amount the user has available to invest *right now* (not monthly income).

- If amount < $50: guide toward savings-first mindset. No investing until emergency cushion exists.
- If $50–$500: Tier 1 — HYSA, money market, I-bonds
- If $500–$1,000: Tier 2 — CDs, Treasury bills
- If $1,000–$2,000: Tier 3 — open retirement account, fund with broad-market utility
- If $2,000–$5,000: Tier 4 — broad-market stock index fund + Treasury bond + REIT ETF
- If $5,000+: Tier 5 — corporate bonds, dividend-growth stocks, sector ETFs

### 2. Check Emergency Fund Status
Before any investing recommendation, confirm the user has 3–6 months of expenses in liquid savings. If not, advise building that first.

### 3. Pull Real Market Data (via MCP)
Use `openbb-finance` and `trading-signals` MCP tools to show current rates/prices for the recommended vehicles:

```yaml
- stock_quote: current price for any ticker recommended
- company_profile: verify any recommended stock's fundamentals
- analyst_ratings: check consensus on sector picks
- market_indices: show S&P 500 / Dow / NASDAQ context
- sector_performance: identify trending sectors for Tier 4+
- treasury_rates: current T-bill/T-note yields (Tier 2, 4)
- market_scan: find candidates meeting user's risk profile
- technical_signals: timing check before entry
```

### 4. Present Tiered Recommendation
Show **only** the tier matching the user's amount plus one tier above as aspirational. Never dump all tiers at once.

### 5. Include Compounding Example
Show a simple projection for the recommended tier:
- $100/mo at 5% APY → $6,800 after 5 years
- $200/mo at 7% avg return → $14,400 after 5 years
- $500/mo at 8% avg return → $36,800 after 5 years

### 6. Scam Red Flags
Include in every recommendation:
- ❌ "Guaranteed returns" above market rates
- ❌ Promissory notes from unknown issuers
- ❌ Crypto lending/"staking" with double-digit yields
- ❌ Unsolicited investment opportunities
- ❌ Upfront fees to "unlock" an investment

## Pitfalls
- Do NOT recommend stocks over emergency fund — savings first, always
- Do NOT recommend taxable brokerage before maxing IRA/401(k) match
- Do NOT recommend specific tickers as "buys" — present as examples for education
- Do NOT ignore the user's stated risk tolerance — a $5k user who says "scared of stocks" should get bonds/CDs, not VOO
- Do NOT flood with all tiers — present **only** the matching tier + one aspirational step

## Verification
- [ ] Skill prompts for investable amount before recommending
- [ ] Emergency fund check runs before any investment recommendation
- [ ] MCP tools called only for the recommended tier's vehicles
- [ ] Scam red flags included in output
- [ ] Compounding example matches the user's tier
- [ ] Only 1–2 tiers shown to the user (current + aspirational)
