---
name: ib-merger-model
version: 1.0.0
description: Build an accretion/dilution merger model — pro forma EPS, financing mix, synergies, and purchase price allocation — to test whether an acquisition creates or destroys value for the acquirer's shareholders.
author: matrixx0070
tags: [investment-banking, m&a, merger-model, accretion-dilution, valuation]
capabilities: []
---

## When to use
Use this when an acquirer needs to know whether a proposed deal lifts or dilutes its earnings per share and on what terms. The merger model combines the two companies pro forma, layers in the purchase price, financing (cash/debt/stock), synergies, and the incremental charges from purchase accounting, then compares pro forma EPS to the acquirer's standalone EPS.

**Not for:** normalizing the target's raw financials (use ib-datapack-builder), the buyer-facing story (use ib-cim-builder), or standalone DCF/comps valuation. Use the datapack as the input source; do not re-derive the target's numbers here.

## Method
1. Pull standalone forecasts for acquirer and target from the datapack: revenue, EBIT, net income, and diluted shares.
2. Set deal terms: offer price/premium, equity purchase price, and the financing mix (cash on hand, new debt, new stock) with the interest rate on new debt and the acquirer's share price for stock consideration.
3. Run purchase price allocation (PPA): allocate purchase price over net identifiable assets, step up assets, book intangibles, and record goodwill as the residual; compute incremental D&A from write-ups.
   **Decision point:** deal structure matters — an asset deal (or 338(h)(10) election) can create tax-deductible goodwill/step-up amortization; a stock deal usually does not. Confirm structure before modeling tax effects.
4. Layer synergies: phase in cost synergies (and any revenue synergies, treated more conservatively) net of one-time integration costs.
5. Build the pro forma income statement: combine EBIT, add synergies, subtract incremental D&A from step-ups, subtract incremental interest on new debt, apply the marginal tax rate, and add shares issued for stock consideration.
6. Compute pro forma diluted EPS and compare to acquirer standalone EPS: accretion if higher, dilution if lower; report the percentage and the breakeven synergy level.
7. Sensitize the answer: flex premium, financing mix, synergy realization, and interest rate; show the accretion/dilution grid.

## Example
> All-cash acquisition funded with new debt at 6%. Target adds $40M EBIT; PPA created $200M of intangibles amortized over 10 years (+$20M annual D&A) and goodwill (no amortization). Run-rate cost synergies of $15M phased 50%/100% over two years. Incremental after-tax interest and step-up D&A were subtracted; no new shares. Pro forma EPS rose 4.2% in year 1 (accretive) driven by cheap debt and synergies; breakeven required only $6M of synergies. A stock-funded variant at the same premium was dilutive 2.1% because the acquirer's P/E was below the target's implied acquisition multiple.

## Pitfalls
- Forgetting the incremental charges from purchase accounting — step-up D&A and, in taxable structures, their tax shield — which flatter EPS if omitted.
- Double-counting or over-crediting synergies, especially revenue synergies, and ignoring one-time integration costs.
- Modeling tax-deductible goodwill in a straight stock deal where it is not deductible.
- Using stale share counts or share price for stock consideration, which distorts the shares-issued and accretion math.

## Output format
```
MERGER MODEL — <Acquirer> / <Target> — <date>

DEAL TERMS
Offer price / premium: <>   Equity purchase price: <>
Financing: cash <> | new debt <> @ <rate> | new stock <> @ <acquirer px>

PURCHASE PRICE ALLOCATION
Purchase price                <->
- Net identifiable assets     <->
- Asset step-up / intangibles <->  -> incremental D&A <-> /yr
= Goodwill (residual)         <->   Deductible? [Y/N per structure]

PRO FORMA EPS BUILD (Year 1)
Acquirer EBIT + Target EBIT            <->
+ Synergies (net of integration)      <->
- Incremental step-up D&A             <->
- Incremental interest on new debt    <->
= Pro forma pre-tax income            <->
- Tax @ <rate>                        <->
= Pro forma net income                <->
/ Pro forma diluted shares            <->
= Pro forma EPS                       <->

Standalone acquirer EPS               <->
ACCRETION / (DILUTION)                <+/-%>
Breakeven synergies                   <->

SENSITIVITY: accretion/dilution vs. [premium] x [synergy realization]
```

## Reference
- Accretion/dilution: pro forma EPS > standalone acquirer EPS = accretive; < = dilutive. Rule of thumb — a deal tends to be accretive when the acquirer's P/E exceeds the after-tax cost of the consideration used (cheap debt or a high-P/E acquirer paying a lower-multiple target).
- Sources & uses must balance: uses (equity purchase price, refinanced debt, fees) = sources (cash, new debt, new equity).
- PPA: purchase price is allocated to identifiable assets (with step-ups) and liabilities; the residual is goodwill. Step-ups create incremental D&A; goodwill is not amortized for book but is tested for impairment.
- Consideration trade-offs: cash/debt avoids dilution but adds interest and leverage; stock shares risk/reward but can dilute EPS; the accretion answer is highly sensitive to premium, synergies, and financing rate — always show the sensitivity grid.
