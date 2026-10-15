---
name: grayscale-crypto-sectors
description: "Use when evaluating crypto through a Grayscale-style Crypto Sectors lens: sector taxonomy, FTSE/Grayscale index eligibility, fee/usage fundamentals, sector-share valuation, ETP/trust wrappers, and Zcash-style privacy-as-money theses."
invest: ./invest.md
---

# Grayscale Crypto Sectors

Use this skill to apply Grayscale Research's public judgment system: classify first, then ask whether the token is index-eligible, whether usage/fees support the use case, and whether valuation vs its Crypto Sector still prices the theme as a rounding error.

## When To Use

Use this skill when the user asks for:

- Grayscale, Crypto Sectors, FTSE/Grayscale indexes, or a Grayscale Top 20
- Zcash / ZEC / ZCSH / privacy-coin institutionalization
- Whether a token belongs in Currencies, Smart Contract Platforms, Financials, Consumer & Culture, Utilities & Services, or AI
- Sector-share valuation vs replacing Bitcoin
- Crypto ETP, trust, NAV premium/discount, or ETF-conversion structure
- Institutional access: custody, listing, legal classification, creation/redemption

Trigger phrases include `Grayscale`, `Crypto Sectors`, `ZCSH`, `Zcash`, `ZEC`, `privacy as money`, `sector share`, `FTSE Grayscale`, `crypto ETP`, and `trust premium/discount`.

## Do Not Use When

- The request is a memecoin attention trade with no sector use case. Use `ansem-crypto`.
- The user wants protocol-mechanism or MEV design review. Use `paradigm-crypto-research`.
- The user wants funding/leverage cycle timing. Use `arthur-hayes-liquidity`.
- Critical market-cap, sector, fee, or product-wrapper data is missing and a live verdict is requested.
- The user wants guaranteed returns or unbounded leverage.

## Inputs Needed

- Token, theme, or Grayscale product ticker
- Crypto Sector assignment and nearest sector peers
- Circulating market cap, sector market cap, and implied sector share
- Users / active addresses, transactions, and fees
- Token supply inflation and unlocks
- Upcoming catalysts: upgrades, legislation, ETP/ETF filings
- For listed products: NAV, market price, premium/discount, creation/redemption status
- Time horizon and whether this is a core monetary sleeve or a satellite theme

If live data matters and is missing, say what is missing and give a provisional sector memo rather than a false-precision target.

## Process

1. Assign one primary Crypto Sector. Do not score a currency like an app token.
2. Check index eligibility: use case fit, listings, market-cap floor, ADTV, custody/access, legal viability.
3. Measure fundamentals. Treat fees as the hardest-to-fake "revenue" proxy; pair with users and transactions.
4. Value against sector share, not against "replacing Bitcoin." Ask what modest share capture would imply.
5. Separate usage evidence from narrative mindshare. Both can move price; only usage supports a multi-year sector-share thesis.
6. Layer the product wrapper last: trust vs ETF, NAV gap, authorized-participant arbitrage, sponsor/affiliate flows.
7. Size as a satellite or theme overlay. Do not treat a 0.3% sector name as a Bitcoin substitute.

## Output Format

```md
# Grayscale Crypto Sectors View: [Asset / Theme]

## Verdict
Overweight Sector / Single-Name Research / Watch / Wrapper Trade / Pass / Too Hard

## Sector Classification

## Index Eligibility

## Fundamentals
| Metric | Reading | vs peers | Weight |
|--------|---------|----------|--------|

## Sector-Share Valuation

## Catalysts And Wrapper

## Tail Risks

## Sizing

## Invalidation

## Missing Data
```

## Guardrails

- Do not confuse a backward-looking Top 20 (volatility-adjusted winners) with a forward-looking research pick.
- Do not treat an ETF filing as the thesis. It is an access/catalyst layer.
- Do not value ZEC as a Bitcoin-replacement bet. Grayscale's published case is that private digital money is under-recognized inside Currencies.
- Do not ignore NAV premium/discount when the vehicle is a closed trust.
- Not financial advice. Separate facts, assumptions, and judgment.

## Questflow Use

Use as a Questflow-style sector and institutional-access module: taxonomy, eligibility, fees, sector-share math, and product wrapper. Load this skill first, then attach 1-3 Grayscale primary sources.
