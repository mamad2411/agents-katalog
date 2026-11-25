---
name: canada-first-home
description: Plan a first home purchase in Canada - minimum down payment, CMHC insurance, monthly payment, the mortgage stress test, Ontario and Toronto land transfer tax with first-time rebates, and how to use the FHSA and RRSP Home Buyers' Plan. Use when the user asks "can I afford this house", "how much down payment", "will I pass the stress test", "land transfer tax", "closing costs", "FHSA or HBP", or is buying a first home or condo in Canada.
---

# First home in Canada

## Rules (2026, update every January)

| | |
|---|---|
| Minimum down payment | 5% of the first $500,000 + 10% of the part from $500,000 to $1.5M |
| Price $1.5M or more | 20% down, no mortgage insurance |
| Mortgage insurance (CMHC, Sagen, Canada Guaranty) | under 20% down: 4.00% (5-9.99% down), 3.10% (10-14.99%), 2.80% (15-19.99%) of the loan, added to the mortgage |
| 30-year amortization | insured mortgages only for first-time buyers or new builds; adds 0.20% to the premium |
| Stress test | qualify at the higher of 5.25% or your rate + 2% |
| Debt limits (insured) | housing costs (GDS) up to 39% of gross income, all debts (TDS) up to 44% |
| Ontario land transfer tax | 0.5% to $55k, 1% to $250k, 1.5% to $400k, 2% to $2M, 2.5% above; first-time rebate up to $4,000 |
| Toronto adds its own land transfer tax | same rates up to $2M; first-time rebate up to $4,475 |
| FHSA | $8,000 a year, $40,000 lifetime, deductible going in, tax-free out for a first home |
| RRSP Home Buyers' Plan | withdraw up to $60,000 tax-free, repay over 15 years |

## Run the numbers

Don't do mortgage maths by hand (Canadian fixed rates compound semi-annually). Run:

```
python scripts/home.py --price 700000 --down 50000 --rate 4.5 --years 30 --first-time --toronto --income 130000 --debts 400 --property-tax 4800
```

- `--rate` is the rate the user was quoted. If they don't have one, ask; don't invent today's rates.
- `--income` is gross household income on the mortgage. `--debts` is monthly car, student loan and card minimums.
- Add `--condo-fee` for condos (half counts toward GDS). `--heat` defaults to $100/month.
- Outside Ontario, ignore the land transfer lines and tell the user to check their province's rules (BC, Manitoba, Quebec and Nova Scotia have their own).

## How to answer

1. Show the script's lines: minimum down, insurance, monthly payment, stress-test payment, land transfer tax, cash at closing, and whether GDS/TDS pass.
2. If it fails the stress test, say what would make it pass: a bigger down payment, a lower price, paying off a debt, or a co-borrower. Re-run the script with the change instead of estimating.
3. Remind them closing costs beyond the script: legal fees ($1,500 to $2,500), title insurance, home inspection, moving, property tax and utility adjustments. Keep 1.5% to 4% of the price aside.
4. Down payment sources, in order: FHSA first (deductible and tax-free), then RRSP HBP (must be repaid), then TFSA. They can combine FHSA and HBP for the same home.
5. "First-time" means different things: the FHSA and HBP count you as first-time if you didn't live in a home you or your spouse owned this year or in the previous four years, but the Ontario and Toronto land transfer rebates need you to have never owned a home anywhere in the world. Flag this when someone owned a home abroad.

Always end with: lenders decide the final approval; get a pre-approval from a lender or broker. This is information, not financial advice.

## Calculator code
If `scripts/home.py` isn't in this skill's folder (some apps keep only SKILL.md), save this code as `home.py` and run it the same way. Don't do the arithmetic by hand.

<!-- embed: scripts/home.py -->
```python
"""First home in Canada: minimum down payment, CMHC premium, monthly payment, stress test, Ontario/Toronto land transfer tax.
Usage: python home.py --price 700000 --down 50000 --rate 4.5 [--years 25] [--first-time] [--toronto]
                      [--income 120000 --debts 400 --property-tax 4800 --heat 100 --condo-fee 0]
Rules as of 2026; update each January.
"""
import argparse

INSURED_CAP = 1_500_000
CMHC = [(0.15, 0.028), (0.10, 0.031), (0.05, 0.040)]  # down-payment share at least X -> premium on the loan
CMHC_30Y_SURCHARGE = 0.002
ON_LTT = [(55_000, 0.005), (250_000, 0.01), (400_000, 0.015), (2_000_000, 0.02), (float("inf"), 0.025)]
TORONTO_LTT = [(55_000, 0.005), (250_000, 0.01), (400_000, 0.015), (2_000_000, 0.02), (3_000_000, 0.025)]
ON_REBATE, TORONTO_REBATE = 4_000, 4_475
GDS_MAX, TDS_MAX = 0.39, 0.44


def slab(x, slabs):
    tax, lo = 0.0, 0
    for hi, r in slabs:
        if x > lo:
            tax += (min(x, hi) - lo) * r
        lo = hi
    return tax


def min_down(price):
    if price >= INSURED_CAP:
        return price * 0.20
    return min(price, 500_000) * 0.05 + max(price - 500_000, 0) * 0.10


def cmhc_rate(price, down, years):
    share = down / price
    if share >= 0.20:
        return 0.0
    rate = next(r for s, r in CMHC if share >= s - 1e-9)
    return rate + (CMHC_30Y_SURCHARGE if years > 25 else 0)


def payment(principal, annual_rate, years):
    """Canadian fixed-rate mortgages compound semi-annually."""
    m = (1 + annual_rate / 2) ** (1 / 6) - 1
    n = years * 12
    return principal / n if m == 0 else principal * m / (1 - (1 + m) ** -n)


def land_transfer(price, first_time, toronto):
    on = slab(price, ON_LTT)
    on_net = on - (min(on, ON_REBATE) if first_time else 0)
    if not toronto:
        return on, on_net, 0.0, 0.0
    if price > 3_000_000:
        raise ValueError("Toronto has luxury MLTT bands above $3M: check toronto.ca")
    to = slab(price, TORONTO_LTT)
    return on, on_net, to, to - (min(to, TORONTO_REBATE) if first_time else 0)


def plan(price, down, rate, years=25, first_time=False, toronto=False):
    need = min_down(price)
    if down < need - 0.5:
        raise ValueError(f"Down payment too small: minimum is ${need:,.0f}")
    if years > 25 and down / price < 0.20 and not first_time:
        raise ValueError("Insured mortgages over 25 years need a first-time buyer or a new build")
    prem_rate = cmhc_rate(price, down, years)
    premium = (price - down) * prem_rate
    loan = price - down + premium
    on, on_net, to, to_net = land_transfer(price, first_time, toronto)
    q_rate = max(rate + 0.02, 0.0525)
    return {"min_down": need, "premium_rate": prem_rate, "premium": premium, "pst_on_premium": premium * 0.08,
            "loan": loan, "monthly": payment(loan, rate, years), "qualifying_rate": q_rate,
            "qualifying_monthly": payment(loan, q_rate, years), "ontario_ltt": on, "ontario_ltt_net": on_net,
            "toronto_ltt": to, "toronto_ltt_net": to_net}


def ratios(qualifying_monthly, income, debts, property_tax, heat, condo_fee):
    housing = qualifying_monthly + property_tax / 12 + heat + condo_fee * 0.5
    gross = income / 12
    return housing / gross, (housing + debts) / gross


if __name__ == "__main__":
    # hand-checked: $700k, 10% down -> premium 3.10% of $630k = $19,530
    t = plan(700_000, 70_000, 0.045)
    assert round(t["premium"]) == 19_530 and round(t["ontario_ltt"]) == 10_475
    assert min_down(900_000) == 65_000 and min_down(1_500_000) == 300_000
    assert round(plan(700_000, 50_000, 0.045, 30, True, True)["toronto_ltt_net"]) == 6_000

    p = argparse.ArgumentParser()
    p.add_argument("--price", type=float, required=True)
    p.add_argument("--down", type=float, required=True)
    p.add_argument("--rate", type=float, required=True, help="contract rate in percent, e.g. 4.5")
    p.add_argument("--years", type=int, default=25)
    p.add_argument("--first-time", action="store_true")
    p.add_argument("--toronto", action="store_true")
    p.add_argument("--income", type=float)
    p.add_argument("--debts", type=float, default=0, help="other monthly debt payments")
    p.add_argument("--property-tax", type=float, default=0, help="yearly")
    p.add_argument("--heat", type=float, default=100, help="monthly")
    p.add_argument("--condo-fee", type=float, default=0, help="monthly")
    a = p.parse_args()
    r = plan(a.price, a.down, a.rate / 100, a.years, a.first_time, a.toronto)
    print(f"Minimum down payment: ${r['min_down']:,.0f} (you have ${a.down:,.0f}, {a.down / a.price:.1%})")
    if r["premium"]:
        print(f"Mortgage insurance: {r['premium_rate']:.2%} = ${r['premium']:,.0f}, added to the loan"
              f" (in Ontario, 8% PST on it is due in cash at closing: ${r['pst_on_premium']:,.0f})")
    print(f"Mortgage: ${r['loan']:,.0f} over {a.years} years at {a.rate:g}% -> ${r['monthly']:,.2f}/month")
    print(f"Stress test at {r['qualifying_rate']:.2%}: ${r['qualifying_monthly']:,.2f}/month")
    lt = f"Ontario land transfer tax: ${r['ontario_ltt']:,.0f}"
    if a.first_time:
        lt += f", ${r['ontario_ltt_net']:,.0f} after the first-time rebate"
    print(lt)
    if a.toronto:
        print(f"Toronto land transfer tax: ${r['toronto_ltt']:,.0f}" + (f", ${r['toronto_ltt_net']:,.0f} after the rebate" if a.first_time else ""))
    cash = a.down + r["ontario_ltt_net"] + r["toronto_ltt_net"] + (r["pst_on_premium"] if r["premium"] else 0)
    print(f"Cash needed at closing (down + LTT + PST), before legal fees and inspection: ${cash:,.0f}")
    if a.income:
        gds, tds = ratios(r["qualifying_monthly"], a.income, a.debts, a.property_tax, a.heat, a.condo_fee)
        ok = gds <= GDS_MAX and tds <= TDS_MAX
        print(f"GDS {gds:.1%} (max 39%), TDS {tds:.1%} (max 44%): {'passes' if ok else 'does NOT pass'} the stress test")
```
