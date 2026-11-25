---
name: real-estate-analysis
description: Real estate investment analysis — rental yield (gross/net), cap rate, NOI, cash-on-cash return, mortgage amortization and loan terms, buy vs rent comparison, occupancy and vacancy assumptions, operating expense ratios, sensitivity analysis on rates and rents, property comparison frameworks. Use when evaluating a property purchase, rental investment, or buy-vs-rent decision.
---

# Real Estate Investment Analysis (NOI, cap rate, cash-on-cash, buy vs rent)

## Core metrics — define the basis or the numbers lie

```
Gross yield      = annual gross rent / purchase price
EGI              = gross potential rent × (1 − vacancy rate) + other income
NOI              = EGI − operating expenses            (EXCLUDES debt service, capex reserve
                                                        varies by convention — state yours)
Cap rate         = NOI / purchase price (or market value)   ← unlevered, ignores financing
Net yield        = NOI / total acquisition cost (price + closing + initial repairs)
Cash-on-cash     = pre-tax annual cash flow after debt service / total cash invested
                   (down payment + closing + repairs)
DSCR             = NOI / annual debt service           (lenders commonly want ≥ 1.2)
OER              = operating expenses / EGI            (typical 35–50% long-term rental)
Monthly payment  = P × r(1+r)^n / ((1+r)^n − 1)        r = monthly rate, n = months
```

Two rules that catch most broken analyses:

1. **Never quote a return without its basis.** Gross vs net, price vs total acquisition cost,
   levered vs unlevered — a "7% yield" can be any of six different numbers.
2. **Cap rate compares properties; cash-on-cash compares against your alternatives.** Don't use a
   levered return to compare buildings, or an unlevered one to judge your own equity.

## Operating expenses — itemize, never guess a lump

Property tax, insurance, maintenance/repairs (rule-of-thumb reserve ~1% of property value/yr or
per local cost data), capex reserve (roof, HVAC — sinking fund, not "surprise"), property
management (typically 8–10% of collected rent — include it even if self-managing; your time isn't
free), HOA/service charges, utilities you pay, leasing/turnover costs, and vacancy (one month per
year ≈ 8% is a common baseline — never 0%).

## Buy vs rent — compare total unrecoverable costs

- **Owning, unrecoverable**: mortgage *interest* (not principal), property tax, insurance,
  maintenance, transaction costs amortized over the holding period, and the opportunity cost of
  the down payment invested elsewhere.
- **Renting, unrecoverable**: the rent.
- Principal paydown is forced savings, not a cost; appreciation is an assumption, not a fact —
  show the breakeven appreciation rate rather than asserting one.
- Holding period dominates: transaction costs (often 5–10% round trip) make short holds lose even
  in rising markets. State the assumed hold explicitly.

## Sensitivity analysis — mandatory, not optional

Build a small grid, don't report a single scenario:

- Rent: −10% / base / +10%
- Vacancy: 5% / 8% / 12%
- Interest rate at refinance: ±2 percentage points
- Exit cap rate: entry ± 1 point (exit value = final-year NOI / exit cap)

If the deal only works in the best cell, it doesn't work. Report which variable flips cash flow
negative first — that is the real risk statement.

## Comparing properties

Same-basis table: price, gross rent, vacancy assumption, itemized OpEx, NOI, cap rate, cash
needed, cash-on-cash, DSCR, and the top sensitivity per property. Rank by the metric that matches
the goal (income → cash-on-cash and DSCR; long-term value → cap rate vs market cap + location
fundamentals), never by gross yield.

## Failure modes

- Underwriting at 0% vacancy and $0 maintenance — the classic listing-brochure pro forma.
- Using gross yield to compare properties with different tax/HOA/management burdens.
- Counting principal paydown as "profit" in cash flow, or ignoring capex until the roof fails.
- Comparing a levered cash-on-cash return to an unlevered index return.
- Assuming today's teaser rate persists past the fixed period; no stress test at reset.
- Appreciation assumptions doing all the work — the income case fails and nobody notices.
- Ignoring transaction costs in buy-vs-rent, which flips short-hold decisions.

## Reviewer checklist

- [ ] Every return metric carries its basis (gross/net, levered/unlevered, price vs all-in cost)
- [ ] Vacancy ≥ a stated non-zero assumption; management fee included even if self-managed
- [ ] OpEx itemized; capex reserve separate from maintenance
- [ ] Debt terms explicit: rate, fixed period, amortization length, payment, DSCR
- [ ] Sensitivity grid present; the first variable to flip cash flow negative is named
- [ ] Buy-vs-rent compares unrecoverable costs and states holding period + breakeven appreciation
- [ ] Comparison table uses identical assumptions and basis across properties

## Provenance

Standard residential/small-commercial underwriting practice. Ranges (vacancy, OER, management %,
maintenance reserve) are **derived, unverified** defaults — replace with local market data and the
property's actual history before committing capital.
