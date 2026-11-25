---
name: debt-payoff
description: Build a plan to pay off credit cards, loans and lines of credit - avalanche vs snowball, months to debt-free, total interest, and which debt to attack first. Works in any currency. Use when the user says "help me pay off my debt", "credit card debt", "snowball or avalanche", "which debt first", "how long to be debt free", or lists balances and interest rates.
---

# Debt payoff

## What you need from the user
For each debt: name, balance, yearly interest rate, minimum monthly payment. Plus one number: the total they can pay toward debt each month. If they don't know a rate, ask them to check the statement or app; don't guess.

## Run the plan
Save their debts as a CSV and run the script instead of estimating:

```
name,balance,rate,min_payment
Visa,12500,20.99,375
Car loan,14000,7.49,320
```

```
python scripts/payoff.py debts.csv --budget 1200
```

It compares:
- **Avalanche**: minimums on everything, every extra dollar to the highest rate. Always the least interest.
- **Snowball**: extra to the smallest balance first. Costs more, but quick wins keep some people going.

Show both results, then recommend avalanche unless the difference is small and the user says motivation is the problem.

## Then help with the plan
1. If the budget barely covers minimums, help find money: a budget review, or selling something.
2. Ways to cut the rate, by country:
   - Canada: call the card issuer for a lower rate, a balance transfer card, or a line of credit (usually far below card rates).
   - US: 0% balance transfer cards (check the transfer fee, usually 3% to 5%), or a personal loan from a credit union.
   - India: a personal loan to close credit card debt (cards often charge over 40% a year), and never pay only the "minimum due".
   Re-run the script with the new rate to show the saving.
3. Stop adding new debt: take the card out of phone wallets and autopay the minimums.
4. Keep a small emergency fund (one month of expenses) so a surprise doesn't go back on the card.
5. If debts are more than they can repay, point to free non-profit credit counselling (Canada: Credit Counselling Canada; US: NFCC members). Avoid "debt relief" companies that charge up front.

Always end with: this is information, not financial advice.

## Calculator code
If `scripts/payoff.py` isn't in this skill's folder (some apps keep only SKILL.md), save this code as `payoff.py` and run it the same way. Don't do the arithmetic by hand.

<!-- embed: scripts/payoff.py -->
```python
"""Debt payoff plan: avalanche (highest rate first) vs snowball (smallest balance first).
Usage: python payoff.py debts.csv --budget 1200
debts.csv columns: name,balance,rate,min_payment   (rate = yearly %, e.g. 20.99)
Works in any currency. Interest is charged monthly at rate/12.
"""
import argparse
import csv


def simulate(debts, budget, order):
    debts = [dict(d) for d in debts]
    if budget < sum(d["min_payment"] for d in debts):
        raise ValueError("Budget is below the total minimum payments")
    month, interest, paid_off = 0, 0.0, []
    while any(d["balance"] > 0.005 for d in debts):
        month += 1
        if month > 1200:
            raise ValueError("Not paid off in 100 years: the budget doesn't cover the interest")
        for d in debts:
            if d["balance"] > 0:
                i = d["balance"] * d["rate"] / 100 / 12
                d["balance"] += i
                interest += i
        left = budget
        for d in debts:  # minimums first
            pay = min(d["min_payment"], d["balance"])
            d["balance"] -= pay
            left -= pay
        for d in sorted((d for d in debts if d["balance"] > 0.005), key=order):  # extra goes to the target
            pay = min(left, d["balance"])
            d["balance"] -= pay
            left -= pay
        for d in debts:
            if d["balance"] <= 0.005 and d["name"] not in [n for n, _ in paid_off]:
                paid_off.append((d["name"], month))
    return month, interest, paid_off


AVALANCHE = lambda d: -d["rate"]
SNOWBALL = lambda d: d["balance"]


if __name__ == "__main__":
    # hand-checked: one 12% debt of 1,000 paid 100/month -> 11 months, 58.98 interest
    m, i, _ = simulate([{"name": "a", "balance": 1000, "rate": 12, "min_payment": 100}], 100, AVALANCHE)
    assert m == 11 and abs(i - 58.98) < 0.01

    p = argparse.ArgumentParser()
    p.add_argument("csv")
    p.add_argument("--budget", type=float, required=True, help="total paid toward all debts each month")
    a = p.parse_args()
    with open(a.csv, newline="") as f:
        debts = [{"name": r["name"], "balance": float(r["balance"]), "rate": float(r["rate"]),
                  "min_payment": float(r["min_payment"])} for r in csv.DictReader(f)]
    print(f"Total debt {sum(d['balance'] for d in debts):,.2f}, paying {a.budget:,.2f} a month")
    results = {}
    for label, order in (("Avalanche (highest rate first)", AVALANCHE), ("Snowball (smallest balance first)", SNOWBALL)):
        months, interest, order_done = simulate(debts, a.budget, order)
        results[label] = interest
        print(f"\n{label}: debt-free in {months} months ({months // 12}y {months % 12}m), interest {interest:,.2f}")
        print("  Paid off: " + ", ".join(f"{n} (month {m})" for n, m in order_done))
    (b, bi), (w, wi) = sorted(results.items(), key=lambda kv: kv[1])
    print(f"\n{b.split(' (')[0]} saves {wi - bi:,.2f} in interest.")
```
