---
name: canada-capital-gains
description: Adjusted cost base (average cost), realized capital gains/losses per year and superficial loss warnings for a Canadian non-registered account. Use when the user asks "what's my ACB", "how much tax if I sell", "capital gains", "superficial loss", or uploads a trades CSV.
---

# Capital gains (non-registered account)

## Input

A CSV with columns `date,action,symbol,qty,price,fees` (action = buy or sell, date = YYYY-MM-DD, prices in CAD). If the user's broker export looks different (Wealthsimple, Questrade, Coinbase), rename the columns to match first. Convert USD trades to CAD at the Bank of Canada rate for the trade date.

## Run

```
python scripts/acb.py trades.csv
```

It prints ACB per share for each holding, realized gain/loss per year, and flags any loss that may be superficial.

## Rules the script uses

- ACB is average cost: (total cost incl. fees) / shares. Selling doesn't change ACB per share.
- Gain = proceeds - fees - ACB of shares sold.
- 50% of a net capital gain is taxable (inclusion rate).
- Superficial loss: a loss is denied if the same security was bought within 30 days before or after the sale (by the user or a spouse) and is still held 30 days after. The denied loss is added to the ACB of the new shares.

## After running

- For flagged losses, explain the rule and that the loss gets added to the ACB of the repurchased shares, not lost forever.
- Gains in TFSA/RRSP/FHSA are not taxed; this is only for non-registered accounts.
- Say this is an estimate; the user should check against their T5008 slips.

## Calculator code
If `scripts/acb.py` isn't in this skill's folder (some apps keep only SKILL.md), save this code as `acb.py` and run it the same way. Don't do the arithmetic by hand.

<!-- embed: scripts/acb.py -->
```python
"""ACB (average cost), realized gains by year, superficial loss flags. Usage: python acb.py trades.csv"""
import csv
import sys
from collections import defaultdict
from datetime import date


def run(rows):
    rows = sorted(rows, key=lambda r: r["date"])
    shares, cost = defaultdict(float), defaultdict(float)
    gains, flags = defaultdict(float), []
    for r in rows:
        s, q, px, fee = r["symbol"].upper(), float(r["qty"]), float(r["price"]), float(r.get("fees") or 0)
        d = date.fromisoformat(r["date"])
        if r["action"].lower() == "buy":
            shares[s] += q
            cost[s] += q * px + fee
            continue
        if q > shares[s] + 1e-9:
            raise ValueError(f"{r['date']}: selling {q} {s} but only {shares[s]} held")
        acb = cost[s] / shares[s] * q
        gain = q * px - fee - acb
        shares[s] -= q
        cost[s] -= acb
        if gain < 0:
            # ponytail: flags any buy within +/-30 days; doesn't compute the exact denied portion.
            if any(b["symbol"].upper() == s and b["action"].lower() == "buy"
                   and abs((date.fromisoformat(b["date"]) - d).days) <= 30 for b in rows):
                flags.append(f"{r['date']} {s}: loss ${-gain:,.2f} may be a superficial loss")
        gains[d.year] += gain
    return shares, cost, gains, flags


if __name__ == "__main__":
    t = [{"date": "2026-01-02", "action": "buy", "symbol": "RY", "qty": "10", "price": "100", "fees": "0"},
         {"date": "2026-02-01", "action": "buy", "symbol": "RY", "qty": "10", "price": "120", "fees": "0"},
         {"date": "2026-03-01", "action": "sell", "symbol": "RY", "qty": "5", "price": "100", "fees": "0"}]
    sh, co, ga, fl = run(t)
    assert sh["RY"] == 15 and co["RY"] == 1650 and ga[2026] == -50 and fl  # bought 28 days before the loss

    with open(sys.argv[1], newline="") as f:
        shares, cost, gains, flags = run(list(csv.DictReader(f)))
    print("Holdings:")
    for s in shares:
        if shares[s] > 1e-9:
            print(f"  {s}: {shares[s]:g} shares, ACB ${cost[s]:,.2f} (${cost[s] / shares[s]:,.4f}/share)")
    print("Realized gain/loss by year:")
    for y, g in sorted(gains.items()):
        print(f"  {y}: ${g:,.2f}  (taxable at 50%: ${max(g, 0) / 2:,.2f})")
    for line in flags:
        print("WARNING:", line)
```
