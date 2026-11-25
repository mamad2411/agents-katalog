---
name: bank-statement-reconciliation
description: Verify a bank's monthly CSV and PDF exports agree before trusting either for bookkeeping. Use when reconciling bank statements, importing monthly bank exports, or building a local ledger from raw bank data.
---

# Bank Statement Reconciliation

When a bank gives you both a CSV and a PDF for the same statement period, **never trust either in isolation**. Verify they agree on three things before using them downstream.

## When to use

- New monthly bank statement files land in `data/imports/<bank>/`
- About to import bank data into Zoho / Xero / a local ledger
- Diffing annual vs monthly exports for the same bank
- Wio Business specifically — see `references/wio-business.md`

## The 3-point verification

For each (CSV, PDF) pair:

1. **Row count match.** `len(csv_rows) == count(date-prefixed lines in PDF)`. Mismatch ≠ automatic fail (PDF text-extraction can double-count wrapped descriptions), but flag it for manual eyeball.
2. **Closing balance match.** Extract from PDF header (regex: `CLOSING BALANCE.*?([\d,]+\.\d{2})\s*AED`). Must equal the last `Balance` column value in the CSV to the cent.
3. **Chain integrity.** This month's opening balance = previous month's closing balance. Computed: `csv_rows[0].Balance - csv_rows[0].Amount`. Off-by-cent = real gap.

If 2 and 3 pass but 1 doesn't, the data is usable. If 2 or 3 fails, stop and investigate.

## Standard recipe (Python)

```python
import csv, re, subprocess

with open(csv_path) as f:
    rows = list(csv.reader(f))
header, data = rows[0], rows[1:]
amt = header.index("Amount"); bal = header.index("Balance"); dt = header.index("Date")
opening = float(data[0][bal]) - float(data[0][amt])
closing = float(data[-1][bal])
inflow  = sum(float(r[amt]) for r in data if float(r[amt])>0)
outflow = sum(float(r[amt]) for r in data if float(r[amt])<0)

txt = subprocess.check_output(["pdftotext","-layout","-enc","UTF-8",pdf_path,"-"]).decode()
txn_lines = [ln for ln in txt.split("\n") if re.match(r"^\s*\d{2}/\d{2}/\d{4}", ln)]
pdf_close = re.search(r"CLOSING BALANCE.*?([\d,]+\.\d{2})\s*AED", txt, re.S).group(1)

assert pdf_close == f"{closing:,.2f}", f"CLOSING MISMATCH: PDF={pdf_close} CSV={closing:,.2f}"
```

## Pitfalls

- **Annual / lumped exports lie.** Many banks' "full year" CSV silently drops rows that exist in the monthly exports. Always prefer monthly. If you only have a lumped file, treat it as untrusted until proven otherwise.
- **PDF date-regex false positives.** Multi-line transaction descriptions can produce 2nd/3rd lines that start with a date-shaped string. Off-by-1-or-2 row counts are usually this, not real gaps.
- **CSV header names vary.** Wio uses `Balance` for the running balance column; some banks use `Running Balance` or `Closing Balance`. Don't hardcode — use `header.index(...)` with a fallback.
- **File-naming from bank apps is ugly.** Mobile-app exports often land as `statement(Mon DD, YYYY - Mon DD, YYYY.csv` with a typo'd year (Wio's puts "2025" on a 2024 export). Rename to `YYYY-MM.csv` / `YYYY-MM.pdf` immediately, before analysis.

## Bank-specific notes

- **Wio Business** — see `references/wio-business.md` for filename pattern, account filter, and the documented annual-CSV row-drop bug.
