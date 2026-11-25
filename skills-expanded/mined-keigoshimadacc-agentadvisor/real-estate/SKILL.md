# Skill: Residential real estate and housing finance

Domain guidance for buy/rent/sell and property-financing decisions.

## What a serious answer must contain

- **Full cost of ownership, not the mortgage payment.** Include property tax, insurance,
  maintenance reserve, HOA or management fees, transaction costs on entry and exit, and
  the opportunity cost of the down payment. Comparisons that omit these are wrong by a
  large margin, not a small one.
- **A rent-versus-buy calculation with a stated holding period.** The answer flips with
  horizon. State the break-even year.
- **Leverage treated as a risk multiplier, not free money.** Show the equity outcome
  under a price decline, not only under appreciation.
- **Liquidity and mobility cost.** Transaction costs and time-to-sell constrain the
  user's optionality. Quantify what the decision forecloses.

## Standard alternatives to consider

Continue renting and invest the difference; buy a smaller or different-location property;
delay purchase conditional on a stated rate or price trigger; and, where relevant, buy
with a different financing structure.

## Source hierarchy for this domain

1. Public records: registry transfers, tax assessments, permits, flood and zoning maps.
2. Government and central-bank statistics: price indices, rent indices, rate series.
3. Multiple-listing and brokerage transaction data with an as-of date.
4. Local market reports from named institutions.
5. Listing sites and agent commentary. Asking prices are not transaction prices; never
   treat a listing price as evidence of value.

## Domain-specific traps

- **Asking price mistaken for market price.** Use closed transactions.
- **Ignoring the imputed rent side.** Owning saves rent; that saving belongs in the model.
- **Assuming appreciation.** Long-run real house-price growth is close to zero in many
  markets. If the model needs appreciation, that is an assumption with a materiality
  rating, not a fact.
- **Sample-of-one comps.** A single neighbouring sale is anecdote.
- **Rate path extrapolation.** Do not assume refinancing at a better rate; model the
  decision at the rate actually available.

## Quantitative expectations

Produce a break-even analysis over the holding period, with sensitivity on the rate,
appreciation rate, rent growth and maintenance cost. Report the range. Code under
`analysis/`.
