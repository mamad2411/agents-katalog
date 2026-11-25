---
name: india-gst
description: Indian GST for small businesses and freelancers - GST 2.0 rates, whether to register, CGST/SGST vs IGST on an invoice, GSTIN validation and return due dates. Use when the user asks "do I need GST registration", "how much GST to charge", "check this GSTIN", "GSTR-1/3B due date", or "composition scheme".
---

# GST (India)

## Rates: GST 2.0, from 22 September 2025
The 12% and 28% slabs were removed. Main slabs are 5% (essentials, processed food, many textiles) and 18% (most goods and services, including IT, consulting, design, SaaS), plus 40% for luxury and sin goods. Special rates: 3% gold/silver, 0.25% rough diamonds. Many essentials, healthcare, education and individual health/life insurance are 0% or exempt.
Always confirm the exact rate for the HSN (goods) or SAC (services) code; don't guess a product's slab.

## Calculations: use the script
```
python scripts/gst.py calc 50000 18 --from 07 --to 07           # Delhi to Delhi: CGST + SGST
python scripts/gst.py calc 50000 18 --from 07 --to 29           # Delhi to Karnataka: IGST
python scripts/gst.py calc 59000 18 --from 07 --to 07 --inclusive
python scripts/gst.py check 27AAPFU0939F1ZV
```
- Same state = CGST + SGST (half each). Different state, export or SEZ = IGST.
- Exports of services are zero-rated (file a LUT to invoice without IGST).
- GSTIN check only proves the format and check character are right. Tell the user to confirm it's active on the GST portal (Search Taxpayer).

## Registration
- Mandatory above aggregate turnover of Rs 40 lakh (goods) or Rs 20 lakh (services); Rs 20 lakh / Rs 10 lakh in special category states.
- Mandatory from day one for inter-state supply of goods, selling through e-commerce operators, and reverse-charge liability.
- Freelancers serving foreign clients only: exports count toward turnover; registration plus LUT is common once over the threshold.
- Voluntary registration helps when B2B clients want input tax credit.

## Composition scheme
Turnover up to Rs 1.5 crore (goods; lower for services). Flat low rate (1% traders/manufacturers, 5% restaurants, 6% services), no input tax credit, can't charge GST on the bill, no inter-state sales. Files CMP-08 quarterly and GSTR-4 yearly.

## Returns
- GSTR-1 (sales): 11th of next month; quarterly filers (QRMP, turnover up to Rs 5 crore) by the 13th after the quarter.
- GSTR-3B (summary + payment): 20th of next month (22nd/24th for QRMP depending on state).
- GSTR-9 annual: 31 December.
- Late fee and 18% p.a. interest on unpaid tax. Many 3B fields are now auto-filled from GSTR-1 and locked; fix errors through GSTR-1/1A.

## A valid tax invoice has
Supplier name, address and GSTIN; invoice number (new series each tax year) and date; buyer GSTIN for B2B; HSN/SAC; taxable value; rate and CGST/SGST or IGST amounts; place of supply; signature.

End with: rates and dates change by notification; confirm on gst.gov.in or with a CA.

## Calculator code
If `scripts/gst.py` isn't in this skill's folder (some apps keep only SKILL.md), save this code as `gst.py` and run it the same way. Don't do the arithmetic by hand.

<!-- embed: scripts/gst.py -->
```python
"""India GST helper.
  python gst.py check 27AAPFU0939F1ZV                       # validate a GSTIN
  python gst.py calc 10000 18 --from 27 --to 29             # tax on a price (exclusive)
  python gst.py calc 11800 18 --from 27 --to 27 --inclusive # split a GST-inclusive price
"""
import argparse
import re

A = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
RATES = {0, 0.25, 3, 5, 18, 40}  # GST 2.0, from 22 Sep 2025


def gstin_ok(g):
    g = g.strip().upper()
    if not re.fullmatch(r"\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z]Z[0-9A-Z]", g):
        return False, "wrong format (2-digit state + PAN + entity no. + Z + check char)"
    s = 0
    for i, c in enumerate(g[:14]):
        p = A.index(c) * (2 if i % 2 else 1)
        s += p // 36 + p % 36
    if A[(36 - s % 36) % 36] != g[14]:
        return False, "check character doesn't match (typo or fake GSTIN)"
    return True, f"valid format, state code {g[:2]}, PAN {g[2:12]}"


def calc(amount, rate, same_state, inclusive=False):
    base = amount / (1 + rate / 100) if inclusive else amount
    tax = base * rate / 100
    split = {"CGST": tax / 2, "SGST/UTGST": tax / 2} if same_state else {"IGST": tax}
    return round(base, 2), {k: round(v, 2) for k, v in split.items()}, round(base + tax, 2)


if __name__ == "__main__":
    assert gstin_ok("27AAPFU0939F1ZV")[0] and gstin_ok("29AAGCB7383J1Z4")[0]
    assert not gstin_ok("27AAPFU0939F1ZA")[0]
    assert calc(10000, 18, False) == (10000, {"IGST": 1800}, 11800)
    assert calc(11800, 18, True, inclusive=True) == (10000, {"CGST": 900, "SGST/UTGST": 900}, 11800)

    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check"); c.add_argument("gstin")
    k = sub.add_parser("calc"); k.add_argument("amount", type=float); k.add_argument("rate", type=float)
    k.add_argument("--from", dest="src", required=True, help="supplier state code, e.g. 27"); k.add_argument("--to", required=True, help="place of supply state code")
    k.add_argument("--inclusive", action="store_true")
    a = p.parse_args()
    if a.cmd == "check":
        ok, msg = gstin_ok(a.gstin)
        print(("OK: " if ok else "INVALID: ") + msg)
    else:
        if a.rate not in RATES:
            print(f"Note: {a.rate}% isn't a current GST 2.0 rate ({sorted(RATES)}). Check the HSN/SAC rate.")
        base, split, total = calc(a.amount, a.rate, a.src == a.to, a.inclusive)
        print(f"Taxable value Rs {base:,.2f}")
        for name, v in split.items():
            print(f"{name}: Rs {v:,.2f}")
        print(f"Invoice total Rs {total:,.2f}")
```
