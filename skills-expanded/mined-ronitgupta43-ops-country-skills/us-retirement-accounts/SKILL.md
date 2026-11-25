---
name: us-retirement-accounts
description: 2026 limits and rules for 401(k), traditional IRA, Roth IRA and HSA, Roth income phase-out, and which account to fund first. Use when the user asks "how much can I put in my 401k", "Roth or traditional", "Roth IRA income limit", "backdoor Roth", or "where should I save".
---

# US retirement accounts (2026)

## Limits (IRS Notice 2025-67)
- 401(k)/403(b)/457 employee deferral: $24,500. Catch-up from age 50; a larger "super catch-up" ($11,250) at ages 60 to 63. From 2026, catch-ups for people who earned over $150,000 (FICA wages) the prior year must go in as Roth.
- IRA (traditional + Roth combined): $7,500, plus $1,100 catch-up at 50+.
- Roth IRA phase-out (MAGI): $153,000 to $168,000 single / head of household; $242,000 to $252,000 married filing jointly.
- Traditional IRA deduction phase-out if covered by a workplace plan: $81,000 to $91,000 single; $129,000 to $149,000 MFJ. If neither spouse has a workplace plan, it's fully deductible.

## Roth limit at a given income: run the script
The calculator lives in the us-income-tax skill (`scripts/us_tax.py`); if that skill isn't installed, the code is at the end of us-income-tax's SKILL.md in this repo.
```
python us_tax.py --wages 160000 --magi 160500
```

## Usual order (general information, not advice)
1. 401(k) up to the full employer match.
2. HSA if on a high-deductible health plan (triple tax advantage).
3. Roth IRA if eligible (or backdoor Roth: non-deductible traditional IRA contribution, then convert; watch the pro-rata rule if they hold other pre-tax IRA money).
4. Back to the 401(k) up to the limit.
5. Taxable brokerage.

Roth vs traditional: Roth if they expect a higher tax rate later (early career, low bracket now); traditional if their bracket is high now.

## Leaving the US
401(k)s can usually stay put. Early withdrawals (before 59½) cost 10% penalty plus tax. Non-residents face 30% withholding unless a tax treaty lowers it, and the new country may not honor Roth tax-free status. Plan with a cross-border advisor.

End with: check limits on irs.gov and with the plan administrator.
