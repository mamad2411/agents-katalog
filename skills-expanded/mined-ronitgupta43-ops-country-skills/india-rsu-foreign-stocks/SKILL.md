---
name: india-rsu-foreign-stocks
description: Tax on RSUs, ESPP and US or other foreign shares for Indian residents - perquisite at vest, short vs long-term capital gains on sale, dividends, Schedule FA and FSI, Form 67 foreign tax credit, and the FAST-DS 2026 window for missed disclosures. Use when the user says "my RSUs vested", "I sold my Google/Microsoft/Amazon shares", "tax on US stocks in India", "Schedule FA", "Form 67", "foreign tax credit", or has an E*TRADE, Schwab, Fidelity, Morgan Stanley, Vested or INDmoney statement.
---

# RSUs and foreign stocks (India resident)

## Rules (Tax Year 2026-27, check every year)

| Event | How it is taxed |
|---|---|
| RSU vests | Shares x FMV on the vest date x rupee rate = salary perquisite. Employer deducts TDS; it is in Form 16 |
| ESPP purchase | (FMV - price paid) x shares x rate = perquisite |
| Sale, held 24 months or less | Short-term gain, added to income at your slab rate |
| Sale, held over 24 months | Long-term gain, 12.5% + cess, no indexation, **no Rs 1.25 lakh exemption** (that is only for Indian-listed shares) |
| Cost of RSU shares | The FMV already taxed at vest, in rupees |
| Holding period | Starts on the vest date (or purchase date) |
| Losses | Short-term loss sets off any capital gain; long-term loss only long-term gain; carry forward 8 years if the return is filed on time |

Foreign shares count as unlisted in India, so the 12-month rule and the 20% short-term rate for Indian shares do not apply.

**Exchange rates:** the State Bank of India TT buying rate (TTBR), not the market rate.
- Vest: use the rate your employer used for the perquisite (it is on the payslip). The capital gains cost must match the perquisite in Form 16.
- Sale: TTBR on the last day of the month before the month of sale.
- Never use the TT selling rate.

## Run the numbers

Ask for the broker's vesting and sales history (E*TRADE "Gains & Losses", Schwab "Realized Gain/Loss", Fidelity "Stock Plan Transactions") and the rates. Put them in a CSV and run the calculator instead of doing it by hand:

```
date,type,shares,price,rate
2024-03-15,vest,50,140,82.9
2025-08-20,buy,10,180,87.2
2026-04-10,sell,60,190,85.4
```

```
python scripts/rsu.py events.csv --slab 30
```

- `vest` rows: price = FMV per share on the vest date.
- `buy` rows: shares bought with your own money (LRS, ESPP). For ESPP, add the discount as a separate perquisite note.
- `sell` rows: include **sell-to-cover** shares the broker sold at vest for US tax. They usually show a tiny gain or loss and still must be reported.
- `--slab` is the user's top slab rate, to estimate tax on short-term gains.

It prints, per Indian tax year: the perquisite (compare with Form 16), short- and long-term gains after set-off, the tax on each, and the shares held at each 31 December for Schedule FA.

## Reporting checklist

1. **Use ITR-2 (or ITR-3 with business income).** ITR-1 is not allowed once you hold foreign assets.
2. **Schedule CG:** each sale, with dates, rupee sale value and rupee cost.
3. **Schedule FA, Table A3:** every foreign share held at any time in the **calendar year** (January to December), even if sold. Initial value, peak value, 31 December value, and gross proceeds. Also list the brokerage account in Table A2 if it holds cash.
4. **Dividends:** the US withholds 25% under the India-US tax treaty. Show the gross dividend in Schedule OS and Schedule FSI, taxed at slab rate, and claim credit for the US tax.
5. **Form 67:** file it to claim credit for any foreign tax (dividends, or tax withheld at vest abroad). It is due by the end of the assessment year, 31 March, but file it before the return to be safe.
6. **Penalty:** not reporting a foreign asset can cost Rs 10 lakh per year under the Black Money Act. The penalty does not apply if all foreign assets apart from property total Rs 20 lakh or less, **but you must still report them**.
7. **Missed earlier years?** FAST-DS 2026, a one-time disclosure scheme for small taxpayers, is open until **31 December 2026** on the e-filing portal. Point the user to the CBDT FAQs and a chartered accountant to check eligibility; do not work out its tax yourself.

## Buying foreign shares with your own money

Transfers abroad under the Liberalised Remittance Scheme (up to USD 250,000 a year) attract 20% TCS on the amount above Rs 10 lakh in a financial year. It is not an extra tax: it shows in Form 26AS and is adjusted against the year's tax or refunded.

## How to answer

Show the calculator's lines, then the checklist items that apply. Flag a mismatch between the calculator's perquisite and Form 16. If the user is moving back to India, also use india-nri-return (residential status changes what is taxable).

Always end with: this is information, not tax advice; check with a chartered accountant before filing.

## Calculator code
If `scripts/rsu.py` isn't in this skill's folder (some apps keep only SKILL.md), save this code as `rsu.py` and run it the same way. Don't do the arithmetic by hand.

<!-- embed: scripts/rsu.py -->
```python
"""RSUs and foreign shares for an Indian resident: perquisite at vest, capital gains on sale (FIFO), Schedule FA holdings.
Usage: python rsu.py events.csv [--slab 30]
events.csv columns: date,type,shares,price,rate
  type  vest  price = FMV per share on the vest date (foreign currency); rate = the rupee rate your employer used
        buy   price = price paid per share; rate = SBI TT buying rate used for the purchase
        sell  price = sale price per share; rate = SBI TT buying rate on the last day of the month before the sale month
Rules as of Tax Year 2026-27; update each year.
"""
import argparse
import csv
from datetime import date

LTCG_RATE = 0.125
CESS = 0.04


def inr(x):
    """Indian digit grouping: 12,34,567."""
    n = f"{abs(round(x)):d}"
    head, tail = n[:-3], n[-3:]
    while len(head) > 2:
        tail = head[-2:] + "," + tail
        head = head[:-2]
    return ("-" if x < 0 else "") + "Rs " + (head + "," + tail if head else tail)


def tax_year(d):
    return f"{d.year}-{(d.year + 1) % 100:02d}" if d.month >= 4 else f"{d.year - 1}-{d.year % 100:02d}"


def long_term(bought, sold):
    """More than 24 months."""
    y, m = bought.year + 2, bought.month
    try:
        cutoff = bought.replace(year=y)
    except ValueError:  # 29 Feb
        cutoff = date(y, m, 28)
    return sold > cutoff


def run(events):
    lots, years, holdings = [], {}, {}
    for e in sorted(events, key=lambda e: e["date"]):
        y = years.setdefault(tax_year(e["date"]), {"perquisite": 0.0, "stcg": 0.0, "ltcg": 0.0})
        if e["type"] in ("vest", "buy"):
            inr = e["shares"] * e["price"] * e["rate"]
            if e["type"] == "vest":
                y["perquisite"] += inr
            lots.append({"date": e["date"], "shares": e["shares"], "cost_each": inr / e["shares"]})
        elif e["type"] == "sell":
            left, proceeds_each = e["shares"], e["price"] * e["rate"]
            while left > 1e-9:
                if not lots:
                    raise ValueError(f"{e['date']}: selling more shares than you hold")
                lot = lots[0]
                n = min(left, lot["shares"])
                gain = n * (proceeds_each - lot["cost_each"])
                y["ltcg" if long_term(lot["date"], e["date"]) else "stcg"] += gain
                lot["shares"] -= n
                left -= n
                if lot["shares"] <= 1e-9:
                    lots.pop(0)
        else:
            raise ValueError(f"unknown type {e['type']}")
        held = sum(l["shares"] for l in lots)
        holdings[e["date"].year] = (held, sum(l["shares"] * l["cost_each"] for l in lots))
    return years, holdings


def net(stcg, ltcg):
    """Short-term loss can reduce long-term gain; long-term loss only carries forward."""
    if stcg < 0 and ltcg > 0:
        used = min(-stcg, ltcg)
        return stcg + used, ltcg - used
    return stcg, ltcg


if __name__ == "__main__":
    # hand-checked: 100 vest at $200 x 85 = 17,00,000; sell 40 at $250 x 86 within 24 months -> STCG 40 x (21,500 - 17,000) = 1,80,000
    ys, _ = run([{"date": date(2025, 6, 15), "type": "vest", "shares": 100, "price": 200, "rate": 85},
                 {"date": date(2026, 9, 1), "type": "sell", "shares": 40, "price": 250, "rate": 86}])
    assert round(ys["2025-26"]["perquisite"]) == 1_700_000 and round(ys["2026-27"]["stcg"]) == 180_000
    assert long_term(date(2024, 1, 10), date(2026, 1, 11)) and not long_term(date(2024, 1, 10), date(2026, 1, 10))
    assert net(-50, 200) == (0, 150)
    assert inr(1404050) == "Rs 14,04,050" and inr(-28500) == "-Rs 28,500"

    p = argparse.ArgumentParser()
    p.add_argument("csv")
    p.add_argument("--slab", type=float, help="your top slab rate in percent, to estimate tax on short-term gains")
    a = p.parse_args()
    with open(a.csv, newline="") as f:
        events = [{"date": date.fromisoformat(r["date"]), "type": r["type"].strip().lower(), "shares": float(r["shares"]),
                   "price": float(r["price"]), "rate": float(r["rate"])} for r in csv.DictReader(f)]
    years, holdings = run(events)
    for ty, y in sorted(years.items()):
        st, lt = net(y["stcg"], y["ltcg"])
        if not (y["perquisite"] or y["stcg"] or y["ltcg"]):
            continue
        print(f"\nTax Year {ty}")
        if y["perquisite"]:
            print(f"  Perquisite at vest (salary, check it matches Form 16): {inr(y['perquisite'])}")
        if y["stcg"] or y["ltcg"]:
            print(f"  Short-term gain (held 24 months or less, slab rate): {inr(st)}")
            print(f"  Long-term gain (held over 24 months, 12.5%, no Rs 1.25 lakh exemption): {inr(lt)}")
            if lt > 0:
                print(f"    Tax at 12.5% + 4% cess: {inr(lt * LTCG_RATE * (1 + CESS))}")
            if st > 0 and a.slab:
                print(f"    Tax at {a.slab:g}% + 4% cess: {inr(st * a.slab / 100 * (1 + CESS))}")
            if lt < 0:
                print("    Long-term loss: set off only against long-term gains; carry forward up to 8 years if you file on time")
    print("\nSchedule FA (calendar year, Table A3): shares held at year end and their cost")
    for yr, (n, cost) in sorted(holdings.items()):
        print(f"  {yr}: {n:g} shares, initial value (cost) {inr(cost)}; add the peak and 31 December values from your broker")
```
