---
name: pf-big-purchase
version: 1.0.0
description: Decide on a big purchase (rent vs buy, cash vs finance) using a structured cost-and-fit framework.
author: matrixx0070
tags: [big-purchase, rent-vs-buy, financing, affordability, personal-finance]
capabilities: []
---

## When to use

Use this when the owner faces a large decision — home, car, major appliance — and needs a framework to compare rent vs buy, or cash vs financing, without emotion driving the call. Good for pressure-testing affordability before committing.

**Not for:** predicting home/market prices, choosing a specific lender or mortgage product, or approving the purchase. You frame the trade-offs; the owner decides and signs.

This skill provides education and structure, not individualized financial advice. For mortgages, large loans, or anything irreversible, recommend a licensed advisor or mortgage professional.

## Method

1. Define the item, total price, and how long the owner realistically expects to keep/use it.
2. Compute true cost of ownership: purchase price + financing interest + maintenance/insurance/fees + opportunity cost of the down payment. For renting: rent + expected increases over the same period.
3. Decision point — **rent vs buy**: if the horizon is short (<3-5 yr) or the owner values mobility, renting usually wins; longer horizons and stability favor buying. Compare total costs over the *same* period.
4. Affordability gate: does the monthly payment fit the budget without cutting savings below target? If it forces savings to zero, it fails the gate.
5. Decision point — **cash vs finance**: compare the loan APR to what the cash could earn safely. High APR favors paying cash/larger down payment; low APR may favor keeping cash invested — if the owner has the discipline.
6. Reserve check: does the owner keep their emergency fund intact after the down payment? If not, defer.
7. Score fit vs cost and state a clear recommendation with the deciding factor.

## Example

Car, $30,000, keep 8 years. Buy financed at 7% APR: interest ~$5,600 + insurance/maintenance. Cash available but that would drain the emergency fund → finance, but with a larger down payment to cut interest. Monthly payment $520 fits budget without touching savings. Recommendation: buy, finance partially, keep 3-month reserve. Deciding factor: long horizon + reserve preservation.

## Pitfalls

- Comparing monthly rent to a mortgage payment alone — ignores maintenance, taxes, insurance, and opportunity cost.
- Draining the emergency fund for a down payment; one shock then forces high-interest debt.
- Stretching to the maximum a lender approves. Approval is not affordability.
- Anchoring on sticker price and ignoring multi-year total cost of ownership.

## Output format

```
BIG-PURCHASE DECISION — [owner] — [item]
Price: $[x]   Horizon: [x] yrs

RENT/KEEP-CASH vs BUY/FINANCE (same period)
Option A total cost: $[x]
Option B total cost: $[x]

AFFORDABILITY GATE: payment $[x]/mo — [fits | fails] (savings target intact? [y/n])
RESERVE CHECK: emergency fund after purchase — [intact | breached]
CASH vs FINANCE: APR [x]% vs safe yield [x]% -> [pay cash | finance]

RECOMMENDATION: [buy/rent/defer] — deciding factor: [x]
Confirm large loans with a licensed professional before signing.
```

## Reference

Educational frameworks below — general working knowledge, not individualized financial advice. Figures are illustrative anchors that vary by market, rate environment, and time.

### Total cost of ownership (TCO), not sticker price

Compare options over the **same holding period** using full cost, not the headline price:

- **Buying:** purchase price + financing interest + maintenance/repairs + insurance + property tax/registration/fees + transaction costs (closing costs, sales tax) − resale/residual value + **opportunity cost** of the down payment (what that cash could have earned).
- **Renting/leasing:** rent or lease payment + expected increases + renter's insurance + any fees, over the same period.

The comparison is only fair when both cover identical years and include every recurring cost.

### Rent vs buy — the horizon rule

Buying carries large upfront and exit costs (often ~2-5% to buy, ~6-10% to sell a home). You typically need to hold long enough to spread those costs — a commonly taught **breakeven is roughly 3-5+ years** for a home. Shorter horizons or a need for mobility usually favor renting; longer horizons plus stability favor buying. The "price-to-rent ratio" (home price ÷ annual rent for a comparable place) is a rough screen: very high ratios lean toward renting, low ratios toward buying.

### Affordability guidelines

- **Housing:** a common ceiling is total housing cost ≤ ~28% of gross income; total debt payments ≤ ~36% (the "28/36 rule" lenders use). **Approval ≠ affordability** — lenders qualify you at the max, not the comfortable, number.
- **Cars:** one widely taught guideline is **20/4/10** — at least 20% down, finance no longer than 4 years, and keep total transport costs under ~10% of gross income.
- **Universal gate:** the payment must fit *without* cutting savings below target or breaching the emergency fund.

### Cash vs finance

Compare the **loan APR** against what the cash could **safely earn** (and after-tax where relevant):

- APR clearly **above** safe yield → paying cash or a larger down payment usually wins (you "earn" the avoided interest, guaranteed).
- APR **below** safe yield (e.g., a 0% or subsidized promo) → keeping cash invested *can* win — but only with the discipline to not spend it and the reserve to cover the payments.
- **0% promos:** verify it's truly 0% (not deferred interest that back-charges if unpaid) and that you'll clear it before expiry.

Interest cost on a loan rises with both rate and term: a longer term lowers the monthly payment but raises total interest and the time spent "underwater" (owing more than the item is worth), especially on fast-depreciating goods like cars.

### Depreciation and reserves

- New cars commonly lose a large share of value in the first few years; used can cut that depreciation hit.
- **Never** drain the emergency fund for a down payment — one shock afterward forces high-interest borrowing, erasing the savings.
- Budget an ongoing maintenance/repair reserve for anything owned (homes: a rough teaching figure is ~1% of home value per year for upkeep).

### Decision checklist

1. Same-period TCO for each option computed?
2. Horizon long enough to clear transaction costs?
3. Payment fits budget with savings target intact?
4. Emergency fund untouched after the down payment?
5. Cash-vs-finance settled on APR vs safe yield?
6. Recommendation states the single deciding factor.

Large loans and mortgages are irreversible commitments — confirm terms with a licensed professional before signing.
