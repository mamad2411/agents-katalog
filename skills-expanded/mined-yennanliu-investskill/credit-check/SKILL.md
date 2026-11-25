---
description: Balance-sheet solvency and refinancing risk — debt maturity wall, interest coverage trend, leverage vs. covenants, liquidity runway, ratings and spreads, the cost of refinancing at today's rates, and an equity-holder verdict, scored as a Credit Health Score 0–10
---

# Credit Check — Can the Equity Survive the Debt?

## ⚠️ Data Verification — Do This Before Any Analysis

Before running any analysis, always retrieve the latest market data for the ticker:

1. **Fetch current price** — use web search or ask the user for the live price, 52-week range, and market cap. Never assume a price from training data.
2. **Pull the debt disclosures from the filings, not a data feed** — aggregator "total debt" figures routinely omit leases, mix in or leave out current maturities, and lag refinancings. Retrieve:
   - **10-K / latest 10-Q debt footnote** — every instrument: principal, coupon (fixed or floating and its reference rate), maturity, security/seniority, and the **scheduled maturities table** (next five years and thereafter).
   - **MD&A "Liquidity and Capital Resources"** — cash, undrawn revolver capacity and its expiry, commercial paper, planned refinancing, management's stated liquidity needs; and the **contractual obligations** discussion.
   - **Credit agreement / indenture** (8-K Item 1.01 exhibits, 10-K Exhibit 10.x / 4.x) — financial covenants (maximum leverage, minimum coverage, springing tests) and their definitions of EBITDA; the 10-Q covenant-compliance statement.
   - **Lease note** (ASC 842 operating and finance lease liabilities), **pension and OPEB note** (funded status), **commitments and contingencies** (guarantees, purchase obligations), and any **supplier-finance / receivables-factoring** disclosure.
   - **Convertible notes and preferred stock** terms (conversion price, capped calls, put dates).
   - **Credit ratings and outlooks** (S&P, Moody's, Fitch press releases or the company's IR page) and, if available, bond prices / yields (FINRA TRACE) or CDS spreads; benchmark yields by rating from FRED (ICE BofA indices, e.g. `BAMLC0A4CBBB` OAS and `BAMLC0A4CBBBEY` effective yield for BBB; `BAMLH0A1HYBB`, `BAMLH0A2HYB`, `BAMLH0A3HYC` for BB / B / CCC & lower).
   Any 8-K after the latest 10-Q (new notes, tender offers, revolver amendments) supersedes the footnote — check for them.
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

## Overview

Equity sits last in the capital structure. Lenders get paid first, set covenants, and — when a company cannot refinance — take the business. Most equity frameworks in this catalog treat debt as a line in the balance-sheet section or a number in the WACC; none asks the creditor's question from the shareholder's seat: **when does the debt come due, what will it cost to roll at today's rates, can the company pay it without diluting or wiping out the equity, and what does the credit market already think?**

**This skill reads the balance sheet the way a credit analyst does, then translates it back to the equity.** It builds the maturity wall against cash and free cash flow, prices the refinancing shock at current yields for the company's rating, tracks coverage and leverage against approximate rating bands and the company's own covenants, finds the debt that is not called debt (leases, pensions, guarantees, supplier finance), and ends with an **equity-holder verdict**: is the stock the residual claim on a healthy business, or an option on survival? The headline number is a **Credit Health Score (0–10, higher = healthier)**.

**Where it sits.** `financial-report-analyst` and `stock-eval` touch leverage in passing; `bear-case` argues a refinancing thesis without the schedule; `risk-stress-test` shocks prices, not balance sheets. Run this skill when leverage is the swing factor, then hand the refinancing scenario to `bear-case`, the liquidity runway to `risk-stress-test`, and the dividend-coverage question to `dividend-analysis`. If the Altman Z reading in `forensic-accounting` is grey or distressed, this is the next skill to run.

---

## 1. Inputs

| Input | Required | Default if unstated |
|-------|----------|---------------------|
| Ticker | ✅ | — |
| Filings pasted by the user (debt footnote, MD&A liquidity, credit agreement) | optional | retrieve from SEC EDGAR; list accession numbers |
| Base rates for the refinancing shock (Treasury curve, rating-band yields) | optional | fetch from FRED; state the date |
| Rating to use when the company is unrated | optional | infer an implied band from the table in Phase 6 and label it "implied" |
| Stress case for EBITDA | optional | −20% EBITDA (−40% for cyclicals), stated |
| Holding horizon | optional | 1–3 years (covers most maturity walls) |

**Pre-profit mode.** If EBITDA is negative or the company burns cash, coverage and leverage ratios are meaningless — the analysis switches to **liquidity runway** (Phase 4) and dilution history, and the score weights change (Phase 8).

---

## 2. Framework

### Phase 1 — Debt schedule and maturity wall

Build one table from the debt footnote, one row per instrument:

| Instrument | Principal ($M) | Coupon | Fixed / Floating (reference rate + spread) | Maturity | Secured / Unsecured | Callable / Putable | Notes |
|-----------|----------------|--------|------------------------------------------|----------|--------------------|-------------------|-------|

Then the **maturity wall** — cumulative maturities against the resources available to meet them:

| Window | Maturing debt (cumulative) | Cash & ST investments | Undrawn committed revolver (expiring after the window) | Cumulative FCF (base case) | Coverage ratio |
|--------|---------------------------|----------------------|------------------------------------------------------|---------------------------|---------------|
| Next 12 months | | | | | |
| Next 2 years | | | | | |
| Next 3 years | | | | | |
| Next 5 years | | | | | |

```
Coverage ratio (window) = (Cash + Undrawn revolver + Cumulative FCF) / Cumulative maturities
```

| Coverage ratio | Reading |
|----------------|---------|
| > 2.0× | Self-funded — maturities can be repaid without the capital markets |
| 1.0× – 2.0× | Manageable — refinancing preferred but not required |
| 0.5× – 1.0× | **Refinancing-dependent** — the company needs open markets in that window |
| < 0.5× | **Wall** — a closed market or a downgrade in that window is an equity event |

A revolver that expires *before* the maturity it is meant to backstop does not count. Note springing maturities (a term loan that accelerates if a later bond is not refinanced) — they move the wall forward.

**Fixed vs. floating mix.** Report % floating (after disclosed swaps). Each 100 bp move in the reference rate changes interest expense by floating principal × 1% — show it in $ and as % of EBIT.

### Phase 2 — Cost of debt and the refinancing shock

```
Weighted average coupon (WAC) = Σ (principal_i × coupon_i) / Σ principal_i
Market yield                  = today's yield for the company's rating and a similar tenor
                                (the company's own bonds via TRACE if traded; otherwise the ICE BofA rating-band effective yield from FRED)
```

For each tranche maturing in the next three years:

```
ΔInterest_i       = Principal_i × (Market yield − Coupon_i)
Refinancing shock = Σ ΔInterest_i               ($ per year, once all are rolled)
Shock % of EBIT   = Refinancing shock / EBIT (LTM)
EPS impact        = Refinancing shock × (1 − tax rate) / Diluted shares
```

| Shock % of EBIT | Reading |
|-----------------|---------|
| < 5% | Immaterial |
| 5% – 15% | A visible earnings headwind — check whether consensus includes it |
| > 15% | Material — the refinancing alone changes the investment case |

Debt issued during the 2020–2021 low-rate window often carries coupons far below today's yields; name the cheapest tranches and when they roll. A negative shock (rates below coupons) is a tailwind — say so.

### Phase 3 — Coverage, leverage and cash-flow ratios (5-year trend)

| Metric | Formula | Trend (5 yrs) | Stress case |
|--------|---------|---------------|-------------|
| EBIT / interest | EBIT / Interest expense | | |
| EBITDA / interest | EBITDA / Interest expense | | |
| Debt / EBITDA | Total debt / EBITDA | | |
| Net debt / EBITDA | (Total debt − Cash & ST investments) / EBITDA | | |
| Adjusted debt / EBITDAR | (Debt + Lease liabilities + After-tax pension deficit) / (EBITDA + Rent) | | |
| FFO / debt | (Net income + D&A + Deferred taxes + other non-cash items) / Total debt — or (EBITDA − Cash interest − Cash taxes) / Debt, S&P-style | | |
| FCF / debt | (OCF − Capex) / Total debt | | |
| Debt / capital | Total debt / (Total debt + Book equity) | | |

**Rules.** Use **GAAP EBITDA** as the base and show management's "Adjusted EBITDA" alongside — adjustments (synergies, add-backs, SBC) can flatter leverage by a turn or more. Use interest *expense* plus capitalised interest. The **stress case** applies the stated EBITDA haircut with debt held constant. Direction matters as much as level: coverage falling for three years while leverage rises is the pattern that precedes downgrades.

### Phase 4 — Liquidity runway (pre-profit and cash-burning companies)

```
Liquidity       = Cash & ST investments + Undrawn committed revolver (net of covenant-restricted capacity)
Quarterly burn  = −(OCF − Capex), average of the last 4 quarters (use the latest quarter if burn is accelerating)
Runway (quarters) = Liquidity / Quarterly burn
```

| Runway | Reading |
|--------|---------|
| > 12 quarters | Funded through most plans |
| 6 – 12 quarters | Expect a raise within the horizon — price in dilution |
| 4 – 6 quarters | **Raise imminent** — the timing is the company's weakest negotiating moment |
| < 4 quarters | **Survival question** — going-concern language likely |

Report **dilution history** (shares outstanding over 3–5 years, ATM programmes, recent offerings and their discount to market) — the equity holder pays for runway in shares.

### Phase 5 — Covenants, off-balance-sheet and hybrid instruments

**Covenant headroom** (only if the credit agreement discloses the tests):

```
Headroom (%) = (Covenant limit − Actual) / Covenant limit        for a maximum-leverage test
EBITDA cushion = 1 − (Debt / Covenant max leverage) / EBITDA     → how far EBITDA can fall before a breach
```

Use the **covenant's own EBITDA definition** (usually more generous than GAAP). Flag headroom < 15%, any amendment or waiver in the last 2 years, and "springing" covenants that test only when the revolver is drawn. If covenants are not disclosed, say "covenants not disclosed — headroom not assessed" (most investment-grade bonds have none).

**Debt that is not called debt:**

| Item | Where | Treatment |
|------|-------|-----------|
| Operating leases | Lease note (ASC 842) | Add the lease liability to adjusted debt (as S&P and Moody's do) |
| Pension / OPEB deficit | Pension note | Add the after-tax underfunded amount (PBO − plan assets) |
| Guarantees, letters of credit | Commitments note | Disclose; add if a call on the guarantee is plausible |
| Purchase / take-or-pay obligations | Contractual obligations | Fixed claims on future cash — report next 3 years |
| Supplier finance / receivables factoring | Supplier-finance note (ASU 2022-04), MD&A | Economically debt; flatters OCF and payables — add to adjusted debt and say so |
| Unconsolidated JV / VIE debt | Equity-method investment note | Disclose; add the share the company supports |

**Convertibles and hybrids.** For each convertible: conversion price vs. current price, dilution if converted (shares and % of current count), capped call coverage, and put/maturity date. A convert deep **out of the money** is plain debt with a near-term maturity; one **in the money** is equity dilution. Preferred stock and hybrid securities rank ahead of common — include them in the claims ahead of the equity.

### Phase 6 — Ratings, spreads and the implied rating

Report the S&P / Moody's / Fitch rating, outlook (positive / stable / negative / watch) and the date of the last action. Report the company's bond spread or CDS if available, and compare it with the median spread for its rating band — **a bond trading wide of its rating is the market saying a downgrade is coming.**

**Rating-band mapping — a rough guide only.** The ranges below are approximate, assume an average business-risk profile, and are adapted from the concept of the ratio tables in S&P Global Ratings' corporate methodology and Moody's industry rating methodologies. Actual ratings weight business risk, industry, scale and policy heavily; a strong-business company can carry more leverage at the same rating. Use the table to produce an **implied band**, never to second-guess an agency to the notch.

| Band | Debt / EBITDA | EBITDA / interest | FFO / debt | FCF / debt | Typical reading for the equity |
|------|---------------|-------------------|-----------|-----------|-------------------------------|
| AAA / AA | < 1.0× | > 15× | > 60% | > 40% | Debt is irrelevant to the equity case |
| A | 1.0 – 2.0× | 10 – 15× | 45 – 60% | 25 – 40% | Comfortable |
| BBB | 2.0 – 3.0× | 6 – 10× | 30 – 45% | 15 – 25% | Investment grade; watch the BBB− edge (a downgrade to high yield forces selling) |
| BB | 3.0 – 4.0× | 3 – 6× | 20 – 30% | 8 – 15% | Leverage is part of the thesis |
| B | 4.0 – 6.0× | 1.5 – 3× | 12 – 20% | 3 – 8% | Refinancing access drives the equity |
| CCC and below | > 6.0× | < 1.5× | < 12% | < 3% | Equity is an option on survival |

When the agency rating and the implied band differ by more than one band, say which way and why (adjusted EBITDA, parent support, a pending deleveraging plan).

### Phase 7 — Equity-holder verdict

Translate the credit picture into one of four verdicts:

| Verdict | Conditions | What it means for the stock |
|---------|-----------|-----------------------------|
| **Residual of a healthy firm** | Implied band BBB or better, wall coverage > 2× over 3 years, shock < 5% of EBIT | Debt does not drive the equity case — value the business |
| **Levered but serviceable** | BB-ish, coverage > 3×, no wall in 2 years | Leverage magnifies returns both ways — deleveraging is a catalyst, a recession is the risk |
| **Option on refinancing** | Wall coverage < 1× in 2–3 years or shock > 15% of EBIT, but markets are open to the credit | The stock's outcome depends on terms it does not control — price in higher interest and possible dilution |
| **Option on survival** | CCC-ish metrics, runway < 6 quarters, covenant breach risk, or bonds trading at distressed levels (spread > 1,000 bp or price < 70) | The equity is an out-of-the-money call on the enterprise; in a restructuring it is usually wiped out or heavily diluted. Size it as an option, not an investment |

Also note any **creditor–equity conflict**: liability-management exercises (uptiers, drop-downs of collateral), debt-for-equity exchanges, or a dividend/buyback programme the debt cannot support.

### Phase 8 — Credit Health Score (0–10, higher = healthier)

Score each component 0–10 on the anchors, then weight:

| Component | Weight | 10 looks like | 0 looks like |
|-----------|--------|---------------|--------------|
| Leverage (net debt / EBITDA, adjusted debt) | 20% | Net cash, or < 1.0× | > 6.0×, or EBITDA negative |
| Coverage (EBIT and EBITDA / interest, trend) | 20% | EBIT / interest > 15× and stable | EBIT / interest < 1.5× or falling three years running |
| Maturity wall & liquidity | 25% | 3-year wall coverage > 2×, long-dated revolver | 12-month wall coverage < 0.5× with no committed refinancing |
| Refinancing cost shock | 15% | Shock < 5% of EBIT (or negative) | Shock > 25% of EBIT |
| Structure & hidden obligations (floating mix, covenants, off-balance-sheet, converts) | 10% | Mostly fixed, unsecured, no tight covenants, small leases/pension | Tight covenants (< 15% headroom), large supplier finance or pension deficit, secured debt priming the unsecured |
| Market signal (rating, outlook, spreads) | 10% | A-range or better, stable, trading tight | CCC-range, negative watch, or distressed bond prices |

**Pre-profit weights:** Liquidity runway & dilution 50% · Maturity wall 25% · Structure 15% · Market signal 10% (leverage, coverage and refinancing shock dropped — state it).

**Hard caps** (state any that fired):
- Going-concern paragraph, a covenant breach, or a missed payment → Score ≤ **2.0**
- 12-month maturities exceed cash + undrawn revolver + FCF with no committed refinancing, or runway < 4 quarters → Score ≤ **3.0**
- Covenant waiver or amendment to loosen a test in the last 12 months → Score ≤ **5.0**

**Missing data.** Drop any component that cannot be computed, renormalise the remaining weights to 100%, list what was dropped, and cap Confidence at MEDIUM. Never score an unassessed component as 10 or as 0.

---

## 3. Output Format

1. **Data & Sources** header (above), listing the filings, credit agreement, rating releases and FRED series used, each with its date
2. **Executive Summary** — three sentences: the Credit Health Score and verdict, the single biggest credit risk, what would change it
3. **Debt schedule** — one row per instrument; fixed vs. floating mix and the +100 bp sensitivity
4. **Maturity wall** — 1 / 2 / 3 / 5-year table with coverage ratios
5. **Refinancing shock** — tranche-by-tranche ΔInterest, total $, % of EBIT, EPS impact
6. **Ratios** — coverage, leverage, FFO / debt, FCF / debt: 5-year trend plus stress case; implied rating band vs. agency rating
7. **Liquidity runway & dilution** (pre-profit) or **covenant headroom** (where disclosed)
8. **Hidden obligations & hybrids** — leases, pension, guarantees, supplier finance, converts (dilution if converted)
9. **Ratings & spreads** — rating, outlook, last action, spread vs. band median
10. **Equity-holder verdict** — one of the four, with the conditions that put it there
11. **Credit Health Score** — component table, any cap fired, score
12. **Thesis Invalidation** — what would reverse the call (below)
13. **Investment Signal Block** — the standard box (below)

---

## Example

```
User: Credit check on ZEPH (fictional ticker; 10-K debt note and MD&A pasted)

The assistant fills the Data & Sources header (10-K FY2025 pasted by user; BB
effective yield from FRED as of the run date; HIGH for the filing, MEDIUM for the
market yield), then builds the schedule. Hypothetical figures: $1,500M of debt —
a $500M 2.5% note due in 18 months, a $600M 3.75% note due in 4 years, and a $400M
SOFR + 2.25% term loan due in 5 years (27% floating). Cash is $250M, the $300M
revolver expires in 3 years, and base-case FCF is $120M a year.

The 2-year wall coverage is (250 + 300 + 240) / 500 = 1.6× — manageable. Rolling
the 2.5% note at an assumed 7.0% BB yield adds $500M × 4.5% = $22.5M a year of
interest, 9% of EBIT of $250M (≈ $0.13 per share after a 21% tax rate on 140M
shares). EBITDA of $350M gives net debt / EBITDA of 3.6×; interest of about
$61M (term loan at an assumed 6.55% all-in) gives EBITDA / interest of 5.7×:
an implied BB band, matching the agency rating. There are no maintenance
covenants on the notes; the term loan's 4.5× leverage test has 20% headroom.
Operating leases add $180M to adjusted debt.

Components: leverage 5, coverage 6, wall 7, shock 6, structure 6, market 6
→ Credit Health Score 6.1, verdict "levered but serviceable" — BULLISH at the
low end of Moderately Bullish, WEAK-to-MODERATE conviction. Next steps:
`bear-case` with a −30% EBITDA scenario, `dividend-analysis` on whether
the buyback should give way to debt paydown.
```

---

## Notes

- **Equity view, not a bond recommendation.** This skill does not say whether to buy the bonds; it says what the debt means for the stock. A company can be a fine credit and a poor equity (low growth, fully valued) and vice versa.
- **Never invent debt terms.** Coupons, maturities and covenant levels come from the filing or the indenture. If the footnote was not retrieved or pasted, mark the field "not verified" — a wrong maturity date changes the whole verdict.
- **Always date the market yields.** The refinancing shock is only as current as the yield used; state the series and date, and show the result at ±100 bp.
- **Adjusted EBITDA is the borrower's number.** Show it, but score on GAAP-based EBITDA unless the covenant test is the question.
- **Not for banks, insurers or broker-dealers.** Their debt is raw material, not financing, and leverage ratios built for operating companies are meaningless. Point to the regulatory capital metrics instead — banks: CET1, Tier 1 leverage, LCR, NSFR, deposit mix, unrealised securities losses; insurers: RBC ratio / Solvency II ratio, reserve adequacy, investment-portfolio credit quality — and use `stock-eval --sector bank` or `--sector insurer`. REITs and utilities can be assessed here, but compare with sector norms (utilities carry structurally higher leverage at investment-grade ratings; REITs are judged on net debt / EBITDA and fixed-charge coverage).
- **Cyclicals:** use mid-cycle or trough EBITDA in the stress case — peak-cycle leverage always looks fine.
- Pairs with: `financial-report-analyst` (the full filing read), `stock-eval` (whether the business is worth owning), `bear-case` (the refinancing or recession short thesis), `risk-stress-test` (the price shock to go with the balance-sheet shock), `forensic-accounting` (whether the EBITDA itself is reliable), `dividend-analysis` (whether payouts are crowding out deleveraging).

## Thesis Invalidation

After delivering the analysis signal, specify what would reverse it:

**If signal is BULLISH (healthy credit) — thesis breaks if:**
- EBITDA falls enough that net debt / EBITDA rises a full turn or EBIT / interest drops below 4× in the next two quarters
- A debt-funded acquisition, special dividend or buyback raises leverage into the next rating band, or a rating agency moves the outlook to negative
- The company's bond spread widens by more than 150 bp relative to its rating-band index
- A maturity within 12 months is not refinanced by six months before it falls due, or the revolver is drawn heavily

**If signal is BEARISH (weak credit) — thesis breaks if:**
- The company refinances the near-term wall on terms close to its existing coupons, or extends maturities beyond the horizon
- An equity raise, asset sale or FCF beat cuts net debt / EBITDA by a full turn
- Covenant headroom is restored without a waiver, or a rating outlook moves to positive
- The bond price recovers above 90 / the spread tightens back inside its rating-band median

**Re-run this analysis when:**
- [ ] Next 10-Q or 10-K (updated maturities, liquidity and covenant compliance)
- [ ] Any 8-K on new debt, a tender/exchange offer, or a credit-agreement amendment
- [ ] A rating action or outlook change by S&P, Moody's or Fitch
- [ ] Price moves ±15% from current level, or rating-band yields move ±100 bp
- [ ] Material news event (acquisition, leadership change, regulatory decision)

## Standard Signal Output

This skill measures **balance-sheet health from the equity holder's seat, not valuation**, so state the mapping: `Signal: BULLISH` means the debt does not threaten the equity over the horizon; `NEUTRAL` means leverage is serviceable but a refinancing, rate or EBITDA shock would matter; `BEARISH` means the equity's outcome depends on creditors or capital markets. `Action: SELL` here means "the balance sheet does not support holding this equity at an investment-sized position" — read whether the stock is cheap from `stock-valuation`, not from this block.

All analysis concludes with this standardized block:

In the output, the box below is followed immediately by this machine-readable footer — the same values as the box, filled in (no placeholders, no comments), so tools can read the result without parsing the box:

```json
{"investskill": "1", "skill": "credit-check", "ticker": "<TICKER, or null for a portfolio / market-wide view>", "as_of": "<YYYY-MM-DD from Data & Sources>", "signal": "<BULLISH | NEUTRAL | BEARISH>", "confidence": "<HIGH | MEDIUM | LOW>", "horizon": "<SHORT-TERM | MEDIUM-TERM | LONG-TERM>", "score": 0.0, "action": "<BUY | HOLD | SELL>", "conviction": "<STRONG | MODERATE | WEAK>", "retrieval": "<pasted by user | web/tool retrieval | model memory>", "sources": ["<each primary source, dated>"]}
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

**Note:** The box Score is the Credit Health Score itself (higher = healthier balance sheet), so it maps onto the Score Guide directly. Confidence is at most MEDIUM when the debt footnote or market yields were not retrieved or any component was dropped, and LOW when debt terms came from model memory.

**Disclaimer:** Educational analysis only. Not financial advice.
