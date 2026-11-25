---
name: india-income-tax
description: Calculate Indian income tax and compare the new and old regimes for Tax Year 2026-27. Use when the user asks "how much tax will I pay", "new vs old regime", "is 12 lakh tax free", "in-hand salary", "80C", or shares a CTC or salary in rupees.
---

# Indian income tax (Tax Year 2026-27)

From 1 April 2026 the Income-tax Act, 2025 replaced the 1961 Act. "Financial year / assessment year" became one "tax year". Rates did not change. Old section numbers still appear everywhere, so mention both when useful (87A → 156, 111A → 196, 112A → 198).

## Run the script, don't do slab math by hand

```
python scripts/tax_calc.py --income 1500000 --salaried --deductions 200000
```

It prints tax under both regimes (with 4% cess, 87A rebate and marginal relief) and which is lower.

## Rules it uses

New regime (default): nil to 4L, 5% to 8L, 10% to 12L, 15% to 16L, 20% to 20L, 25% to 24L, 30% above. Standard deduction Rs 75,000. No tax up to Rs 12L taxable (Rs 12.75L gross for salaried).

Old regime (must opt out of new): nil to 2.5L, 5% to 5L, 20% to 10L, 30% above. Standard deduction Rs 50,000. Rebate up to Rs 5L taxable. Allows 80C (Rs 1.5L), 80D, HRA, home loan interest (Rs 2L), NPS 80CCD(1B) (Rs 50,000).

## Before running, ask for
- Gross annual income (not CTC: remove employer PF and gratuity).
- Salaried or not.
- Old-regime deductions, if they want a comparison. Apply each section's cap before passing `--deductions`: 80C (incl. EPF, PPF, ELSS, life insurance, home loan principal) max Rs 1.5L, 80CCD(1B) NPS extra Rs 50,000, home loan interest Rs 2L. If the user says "2 lakh in 80C", count only Rs 1.5L and say why.

## Not handled (say so)
- Surcharge above Rs 50L income.
- Capital gains: taxed separately at special rates, and the 87A rebate does not apply to them. Use the india-capital-gains skill.

End with: rough estimate, confirm with Form 16 / a CA.

## Calculator code
If `scripts/tax_calc.py` isn't in this skill's folder (some apps keep only SKILL.md), save this code as `tax_calc.py` and run it the same way. Don't do the arithmetic by hand.

<!-- embed: scripts/tax_calc.py -->
```python
"""Indian income tax, new vs old regime, Tax Year 2026-27 (FY 2026-27).
Usage: python tax_calc.py --income 1500000 [--salaried] [--deductions 200000]
--deductions = old-regime deductions (80C, 80D, HRA, home loan interest...). Ignored for the new regime.
"""
import argparse

NEW = [(400000, 0), (800000, .05), (1200000, .10), (1600000, .15), (2000000, .20), (2400000, .25), (float("inf"), .30)]
OLD = [(250000, 0), (500000, .05), (1000000, .20), (float("inf"), .30)]


def slab_tax(income, slabs):
    tax, low = 0, 0
    for high, rate in slabs:
        if income > low:
            tax += (min(income, high) - low) * rate
        low = high
    return tax


def regime_tax(gross, salaried, deductions, new):
    taxable = max(gross - (75000 if new else 50000) * salaried - (0 if new else deductions), 0)
    tax = slab_tax(taxable, NEW if new else OLD)
    limit = 1200000 if new else 500000
    if taxable <= limit:  # section 87A rebate (s.156 of the 2025 Act)
        tax = 0
    elif new:  # marginal relief just above 12 lakh
        tax = min(tax, taxable - limit)
    # ponytail: no surcharge (income above 50 lakh) and no special-rate income (capital gains)
    return taxable, round(tax * 1.04)  # 4% health and education cess


if __name__ == "__main__":
    assert regime_tax(1275000, True, 0, True)[1] == 0
    assert regime_tax(1210000, False, 0, True)[1] == round(10000 * 1.04)  # marginal relief
    assert regime_tax(2000000, False, 0, True)[1] == round(200000 * 1.04)
    assert regime_tax(1000000, False, 0, False)[1] == round(112500 * 1.04)
    p = argparse.ArgumentParser()
    p.add_argument("--income", type=float, required=True, help="gross annual income in rupees")
    p.add_argument("--salaried", action="store_true", help="apply standard deduction")
    p.add_argument("--deductions", type=float, default=0, help="old-regime deductions")
    a = p.parse_args()
    if a.income > 5000000:
        print("Note: income above 50 lakh attracts surcharge, not included here.")
    res = {name: regime_tax(a.income, a.salaried, a.deductions, new) for name, new in (("New regime", True), ("Old regime", False))}
    for name, (taxable, tax) in res.items():
        print(f"{name}: taxable Rs {taxable:,.0f}, tax incl. cess Rs {tax:,.0f}")
    best = min(res, key=lambda k: res[k][1])
    print(f"Lower tax: {best} (saves Rs {abs(res['New regime'][1] - res['Old regime'][1]):,.0f})")
```
