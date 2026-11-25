---
name: fortax-gst-annual-return
description: Build GSTR-9 and GSTR-9C for a GSTIN and FY - applicability and relaxations for the year, books vs GSTR-1 vs 3B vs 2B reconciliation, the tables that break (4, 5, 6, 8, 10-14, 17-18), ITC split, DRC-03 for short payment, the 9C turnover and ITC walk with reasons, and the certification handover. Typical asks - "GSTR-9 bana do", "annual return FY 2025-26", "9C reconciliation", "Table 6 ITC split", "8A vs 3B difference kyun hai".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# GST annual return (GSTR-9 and GSTR-9C)

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

## Do the work, then stop at the last click

A year of reconciliation ending in one signature. Build it, fill every table, explain every difference, stop
at the DSC or EVC. **Refusing the job because the CA signs it is a failure.** Say where you stop, then start.

## Step 1 — fix the year and the perimeter

Fix the FY first and print it in every header and file name. Then establish, before a number is touched:

- Whether GSTR-9 must be filed for that FY, and whether GSTR-9C applies. Both turn on turnover thresholds
  notified per year. Look them up with `python3 scripts/fortax.py kb "GSTR-9 applicability FY 2025-26" --topics gst`,
  with the due date and late fee.
- Which tables are optional or relaxed for that FY. Relaxations are notified year by year and are the
  commonest source of a wrong annual return; never carry last year's forward.
- Whether the FY needs a certificate from a practising CA or CMA, or self-certification of GSTR-9C.
- Every GSTIN: GSTR-9 is per GSTIN, GSTR-9C reconciles to PAN-level financials, so document the split.

## Step 2 — collect the year, then rebuild it

From the portal (the CA logs in; you download with your browser tool — Claude in Chrome, a Playwright/browser
MCP, or the Codex browser — or give the CA the list and click path): every GSTR-1 and GSTR-3B for the FY, the
system-computed GSTR-9 draft, GSTR-2B for each month, the next FY's returns up to the cut-off (amendments and
ITC declared there feed Tables 10 to 13), the three electronic ledgers (cash, credit, liability), any DRC-03
paid. Plus the books: sales and purchase registers, trial balance, audited financials.

The monthly GSTR-2B vs books work is `fortax-gstr2b-reconciliation` (engine run per month); the monthly
GSTR-1 and 3B figures come from `fortax-gstr1-and-3b`. Bring those in rather than rematching.

Build `<Client>/<FY>/GST/Annual/<date>_GSTR9_<GSTIN>_<FY>_reconciliation.xlsx` with live formulas and one
assumptions block on top. Three columns run through every sheet: books, returns filed, difference —
explained, never squeezed.

## Step 3 — the tables that most often break

| Table | What it holds | Where it breaks |
|---|---|---|
| 4 | Outward supplies on which tax is payable | Advances, RCM inward supplies, credit and debit notes shown net instead of separately |
| 5 | Outward on which tax is not payable | Exports, SEZ, exempt, nil-rated and non-GST mixed up with each other |
| 6 | ITC availed as per GSTR-3B | The split into inputs, capital goods and input services, which 3B never asked for |
| 7 | ITC reversed | Rule 42 and 43 reversals in the books but never in 3B, and 17(5) blocked credit |
| 8 | ITC reconciliation with the portal's figure | 8A is auto-filled and not editable; 8D is a difference, not a claim |
| 10 to 13 | This FY's supplies and ITC declared or reversed in the next FY | Double counting: the same entry in Table 4 and Table 10 |
| 14 | Differential tax paid on Tables 10 and 11 | Left blank when the amendment was actually made |
| 17 to 18 | HSN summary, outward and inward | Digit level and inward applicability differ by year and turnover — look it up |

Table 6 is where the work pays off. GSTR-3B carried one ITC figure; GSTR-9 wants it split. Rebuild the split
from the purchase register by asset and expense head and tie the total to 3B Table 4A. A gap there is a
difference to explain, not a rounding. Tables 15 and 16 (demands, refunds, composition and deemed supply
details) tend to be ignored until a notice asks — fill them from the records.

## Step 4 — carry the year's 3B, 1 and 2B differences into the return

This is where the year's unreconciled positions land. A difference with no cause is a blocker for the CA,
not a footnote.

- **GSTR-1 vs GSTR-3B** on outward supply: turnover and tax declared in one and not the other. Say which is
  right, from the books, and whether the correction was made.
- **GSTR-2B vs books** on ITC: credit claimed but never in 2B, credit in 2B never claimed, this FY's credit
  claimed in the next FY — the last belongs in Tables 8C and 13.

## Step 5 — what was missed during the year

Be explicit about what the annual return can and cannot fix.

- Output tax short-paid **is** reported here, but the liability is paid through DRC-03 in cash, not through
  GSTR-9 and not from the credit ledger where the rule bars it. Confirm before advising.
- ITC missed during the year **cannot** be claimed through GSTR-9. If the section 16(4) window for claiming
  it in a return has closed, it is lost. Say so plainly, with the rule looked up, and imply no workaround.
- Reversals never made are still required: compute them in the workbook, and show the interest with the
  rate looked up.
- GSTR-9 once filed cannot be revised. That single fact decides how much review happens before signing.

## Step 6 — GSTR-9C, the reconciliation statement

GSTR-9C runs from the audited financials to what GSTR-9 says. Where one PAN has several GSTINs, document how
the financials were split, and make the splits add back exactly (formula check, not by eye).

- **Table 5**: turnover per the audited financials, adjusted line by line — unbilled revenue both ends,
  unadjusted advances, deemed supplies, credit notes after year-end, exchange differences — down to the
  turnover in the annual return, unreconciled balance stated, every line sourced.
- **Table 7**: the same walk for taxable turnover. **Table 9**: rate-wise liability against tax paid.
- **Tables 6, 8, 10 and 13**: reasons for every unreconciled amount, in words a reviewer can follow. An empty
  reasons table against a non-zero difference will not survive review.
- **Table 12**: ITC per the audited books against ITC claimed in the annual return. **Table 14**: ITC by
  expense head, from the trial balance, with blocked-credit heads marked.
- **Tables 11 and 16**: additional liability from the reconciliation, again payable through DRC-03.

## Step 7 — the certification handover

Certifying professional or self-certification, the package is the same: the workbook with formulas intact,
the differences schedule with a cause per line, the management representation points the CA will want in
writing, the DRC-03s to pay before filing, and the UDIN placeholder. You do not certify or sign.

## Rules used

Every threshold, relaxation, due date, late fee, interest rate and HSN rule goes in a **Rules used** block:
the rule, the section / rule / notification and FY it is for, and the `kb` source URL with captured date or
"confirm on the portal / notification". A `kb` match of `weak` or `none` is not a source.

## What the CA gets

Dated files in `<Client>/<FY>/GST/Annual/`: the GSTR-9 workbook, the GSTR-9C walk with its reasons, the
differences schedule, the DRC-03 list, and a filing note sourcing every figure. Raw client files are never
renamed or deleted. End with **Rules used** and:

**Check before filing**
- Applicability, optional tables, due date and late fee, all looked up for that FY, in **Rules used**.
- Table 4 plus Table 5 tied to GSTR-1 and to the books; Table 6 tied to GSTR-3B Table 4A; Table 8D understood
  and explained, not treated as a claim.
- Tables 10 to 13 reconciled against the next FY's returns, with nothing double counted.
- Every unreconciled figure in GSTR-9C carrying a reason, and the DRC-03s prepared (the CA pays).
- That GSTR-9 cannot be revised, stated to the CA before signing. The DSC or EVC is the CA's click.
