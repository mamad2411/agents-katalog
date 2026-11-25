---
name: canada-registered-accounts
description: Work out TFSA, RRSP and FHSA contribution room and which account to fund first. Use when the user asks "how much TFSA room do I have", "RRSP limit", "FHSA", "TFSA vs RRSP", or is a newcomer to Canada asking where to save.
---

# Registered accounts (TFSA / RRSP / FHSA)

## Limits (update every January)

| | 2026 |
|---|---|
| TFSA yearly limit | $7,000 |
| TFSA total since 2009 (eligible every year) | $109,000 |
| RRSP dollar limit | $33,810 (2027: $35,390) |
| RRSP rule | 18% of last year's earned income, up to the dollar limit |
| FHSA | $8,000/year, $40,000 lifetime |

## TFSA room

Run the script instead of adding by hand:

```
python scripts/tfsa_room.py --start 2022 --contributed 5000 --withdrawn-before-this-year 1000
```

`--start` is the later of: the year the user turned 18, the year they became a Canadian resident, or 2009. Room only builds while they are 18+ and resident.

## RRSP room

Don't estimate it. Tell the user it's on their Notice of Assessment or CRA My Account. Newcomers have no RRSP room until they have filed a return with earned income.
Over-contributing more than $2,000 costs 1% per month on the excess.

## FHSA

- Must be a first-time home buyer, resident, 18+.
- Room starts only when the account is opened; unused room carries forward at most $8,000 (so max $16,000 in one year).
- Contributions are deductible like an RRSP; qualifying withdrawals are tax-free.
- Can be combined with the RRSP Home Buyers' Plan for the same home.

## Which first (general order, not advice)

1. Employer RRSP match, if any.
2. FHSA if they may buy a first home.
3. TFSA if income is low or they may need the money / leave Canada.
4. RRSP if income is in a higher bracket now than expected at withdrawal.

If they plan to leave Canada: TFSA contributions made while non-resident are taxed 1%/month; RRSP withdrawals as a non-resident have 25% withholding.

Always end with: check exact room in CRA My Account; this is information, not financial advice.

## Calculator code
If `scripts/tfsa_room.py` isn't in this skill's folder (some apps keep only SKILL.md), save this code as `tfsa_room.py` and run it the same way. Don't do the arithmetic by hand.

<!-- embed: scripts/tfsa_room.py -->
```python
"""TFSA contribution room. Usage: python tfsa_room.py --start 2022 [--year 2026] [--contributed X] [--withdrawn-before-this-year Y]"""
import argparse

# Update each January. ponytail: hardcoded table, add new year when CRA announces it.
LIMITS = {**{y: 5000 for y in range(2009, 2013)}, 2013: 5500, 2014: 5500, 2015: 10000,
          **{y: 5500 for y in range(2016, 2019)}, **{y: 6000 for y in range(2019, 2023)},
          2023: 6500, 2024: 7000, 2025: 7000, 2026: 7000}


def tfsa_room(start, year, contributed=0, withdrawn_before=0):
    start = max(start, 2009)
    if year not in LIMITS:
        raise ValueError(f"No TFSA limit for {year} yet - update LIMITS")
    return sum(LIMITS[y] for y in range(start, year + 1)) - contributed + withdrawn_before


if __name__ == "__main__":
    assert tfsa_room(2009, 2026) == 109000
    assert tfsa_room(2022, 2026, 5000, 1000) == 6000 + 6500 + 7000 * 3 - 4000
    p = argparse.ArgumentParser()
    p.add_argument("--start", type=int, required=True, help="later of: year turned 18, year became resident, 2009")
    p.add_argument("--year", type=int, default=max(LIMITS))
    p.add_argument("--contributed", type=float, default=0, help="all contributions ever made")
    p.add_argument("--withdrawn-before-this-year", type=float, default=0)
    a = p.parse_args()
    print(f"TFSA room for {a.year}: ${tfsa_room(a.start, a.year, a.contributed, a.withdrawn_before_this_year):,.0f}")
```
