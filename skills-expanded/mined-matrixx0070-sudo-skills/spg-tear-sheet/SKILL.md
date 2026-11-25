---
name: spg-tear-sheet
version: 1.0.0
description: Produce a one-page company tear sheet — snapshot, financial highlights, valuation multiples, capital structure, and key ratios — as a consistent, disclosure-grounded reference. Educational analytical workflow, not investment advice.
author: matrixx0070
tags: [spg, equity, tear-sheet, financials, multiples, ratios, snapshot]
capabilities: []
---

# Company Tear Sheet

## When to use
Use this to compile a compact, standardized one-page reference on a company: the identity snapshot, a few years of financial highlights, valuation multiples, capital structure and leverage, profitability and liquidity ratios, and the handful of facts anyone needs before a deeper look. The goal is a consistent, comparable, fact-grounded sheet — not a thesis.

**Not for:** the full valuation and scenario build (lseg-equity-research), the pre-earnings expectations map (spg-earnings-preview-beta), or credit/funding analysis (spg-funding-digest). This is the reference snapshot those build on.

This is educational analysis, not investment advice.

## Method
1. **Identity snapshot.** Name, ticker/exchange, sector/industry, brief business description, market cap, enterprise value, and reporting currency. State the as-of date and fiscal-year convention.
2. **Financial highlights (3 years + latest).** Revenue, gross profit, EBITDA, operating income, net income, EPS (basic/diluted), and free cash flow. Show growth rates. Use reported figures; if you present adjusted numbers, label them and keep the GAAP bridge visible.
3. **Valuation multiples.** P/E (trailing and forward), EV/EBITDA, EV/Sales, P/B, FCF yield, and dividend yield. Note whether trailing or forward and the estimate source.
4. **Capital structure.** Total debt, cash, net debt, net debt/EBITDA, shares outstanding (and dilution), and any preferreds/minorities/leases that affect EV. Bridge market cap → EV explicitly.
5. **Profitability & returns.** Gross/operating/net margins, ROE, ROIC, and asset turnover — trend, not just the latest.
6. **Liquidity & solvency.** Current/quick ratios, interest coverage (EBIT/interest), and the debt maturity profile at a high level.
7. **Assemble consistently.** Same line items, same order, same units every time — the value of a tear sheet is comparability. Footnote any non-standard adjustment. Flag data gaps rather than estimating silently.

## Example
Snapshot: MegaCorp (MEGA, NYSE), industrials, makes automation equipment. Price $84, mkt cap $12.6B, net debt $2.1B → EV $14.7B, reporting USD, FY-Dec, as-of 2026-06-30. Highlights: revenue $6.2B/$6.8B/$7.4B (3y, ~9% CAGR), EBITDA margin 21%→23%, diluted EPS $3.10→$3.95, FCF $780M. Multiples: fwd P/E 21.3×, EV/EBITDA 8.6×, EV/Sales 2.0×, FCF yield 6.2%, div yield 1.4%. Capital: total debt $2.9B, cash $0.8B, net debt/EBITDA 1.2× (comfortable), diluted shares 150M (SBC dilution ~1%/yr). Returns: ROIC 14%, ROE 19%, op margin 18%. Liquidity: current 1.8×, interest coverage 9×. Footnote: EBITDA is company-adjusted; GAAP op income $1.33B. Illustrative — NOT advice.

## Pitfalls
- **Mixing trailing and forward multiples** without labeling — a "cheap" forward P/E vs a peer's trailing is not a comparison.
- **Market cap vs enterprise value confusion.** EV multiples need net debt (and leases/minorities/preferreds) added; always show the bridge.
- **Adjusted numbers presented as GAAP.** Keep the bridge visible; unlabeled "adjusted EBITDA" flatters leverage and margins.
- **Ignoring dilution and leases.** SBC-driven share creep and capitalized operating leases (post-IFRS16/ASC842) change per-share value and net debt materially.
- **Single-year snapshots** hide the trend — always show 3+ years for margins and returns.
- **Silent data gaps.** If a figure is unavailable or non-comparable (currency, restatement, M&A), flag it — don't interpolate into the table.

## Output format
```
COMPANY TEAR SHEET — <name> (<ticker>/<exchange>) | as-of <date> | ccy <..> | FY <..>
Snapshot: sector <..>, business <..>, mkt cap <..>, EV <..>
Financial highlights (FYt-2 / t-1 / t / LTM):
  | line | ... | (revenue, GP, EBITDA, op inc, net inc, EPS d, FCF, growth%)
Valuation: P/E (T/F) <..>, EV/EBITDA <..>, EV/Sales <..>, P/B <..>, FCF yld <..>, div yld <..>
Capital structure: debt <..>, cash <..>, net debt <..>, ND/EBITDA <..>, dil shares <..>
  Bridge: mkt cap → +net debt +minorities +leases −associates → EV <..>
Returns/margins: gross/op/net <..>, ROE <..>, ROIC <..>, asset turnover <..>
Liquidity/solvency: current <..>, quick <..>, interest cov <..>, maturity wall <..>
Footnotes / adjustments / data gaps: <..>
NOT investment advice — educational reference only.
```

## Reference

### Enterprise value bridge
`EV = market cap + total debt + minority interest + preferred equity + underfunded pension + capitalized leases − cash & equivalents − value of associates`. EV is the capital-structure-neutral value of the operating business — the correct denominator for EV/EBITDA and EV/Sales. Always show the bridge so the reader can see what was included.

### Multiples — definitions and when to use
- **P/E (trailing/forward):** price / EPS. Equity-level, capital-structure-sensitive; label the period and estimate source.
- **EV/EBITDA:** capital-structure-neutral; the default cross-company multiple. Watch capex intensity.
- **EV/Sales:** for pre-profit or margin-in-transition names; pair with gross margin.
- **P/B:** for financials and asset-heavy businesses.
- **FCF yield:** FCF / market cap — the cash reality check.
- **Dividend yield + payout:** income and its sustainability (payout ratio, FCF cover).

### Leverage and coverage
- **Net debt / EBITDA:** the headline leverage gauge; <2× generally comfortable for a stable industrial, higher tolerable for stable-cashflow utilities/infrastructure.
- **Interest coverage (EBIT / interest, or EBITDA / interest):** ability to service debt; <3× is a caution flag for cyclicals.
- **Maturity profile:** near-term maturity walls create refinancing risk, especially in a high-rate environment — note the next big maturity.

### Returns
- **ROE** = net income / equity (distorted by leverage — high ROE on high leverage is fragile).
- **ROIC** = NOPAT / invested capital — the cleaner return measure; compare to WACC (ROIC > WACC = value creation).
- **Asset turnover** = revenue / assets — the efficiency leg of the DuPont decomposition (ROE = margin × turnover × leverage).

### Consistency and adjustments
A tear sheet's worth is in being **comparable across companies and over time**: identical line items, order, and units. Standardize the treatment of adjusted vs GAAP, leases (IFRS 16 / ASC 842), and stock-based comp. Footnote every non-standard adjustment and every data gap rather than silently estimating — a flagged gap is honest; an interpolated number is a hidden error.
