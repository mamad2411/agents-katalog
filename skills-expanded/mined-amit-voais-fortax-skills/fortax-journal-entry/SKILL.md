---
name: fortax-journal-entry
description: Prepare correct double-entry journal entries with narration, supporting working and a review checklist - month-end and year-end provisions and accruals, depreciation (Companies Act Schedule II), prepaid amortisation, salary and PF/ESI/PT/TDS provisions, revenue deferral, GST and TDS entries, rectification entries from a BRS or reconciliation - in a layout the accountant can post or import. Typical asks - "JV bana do", "provision entry pass karni hai", "depreciation ki entry", "salary payable ki entry", "year end adjustments", "rectification entry do".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
  credits: "Journal entry workflow, entry types and review checklist adapted from anthropics/knowledge-work-plugins, https://github.com/anthropics/knowledge-work-plugins (Apache-2.0)"
---

# Journal entry preparation

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

Prepare journal entries with debits, credits, narration, supporting working and review documentation.
This skill helps prepare entries; the CA or the client's accountant reviews and posts them. Never post
to the accounting software yourself.

## What to ask for

- **Type** of entry (below) and the **period** (e.g. `2026-08`, `Q2 FY 2026-27`, `FY 2026-27`).
- **Data**: the trial balance or ledger balances for the affected accounts (Tally/Busy/Zoho export,
  .xlsx/.csv, or pasted), the supporting schedule (fixed asset register, salary register, prepaid list,
  contracts, bills received after period end), and last period's entries of the same type if any.
- The client's **ledger names** from their ledger list or TB — entries use the client's names, not
  generic ones. A ledger that does not exist is listed for the CA to create.

Look in `<Client>/<FY>/` or wherever the CA dropped files. If something is missing, say what, and
prepare what the evidence supports.

## Step 1 — calculate the entry (in a workbook with formulas or a short script, never mentally)

**Expense accrual / provision for expenses** (goods or services received, bill not yet booked):
- Identify from bills received after period end, POs/GRNs, contracts, or recurring monthly charges.
- Dr the expense (or the asset, if capital) / Cr `Outstanding Expenses` or the party.
- Where TDS applies on credit to the party's account or payment, whichever is earlier, the TDS is due
  on the provision too when the payee is identifiable — flag it. Section and rate:
  `python3 scripts/fortax.py kb "TDS on provision for expenses year end" --topics tds`.

**Depreciation and amortisation:**
- From the fixed asset register: asset class, cost, put-to-use date, useful life, residual value, method.
- Companies Act: Schedule II useful lives, SLM or WDV, pro rata from the put-to-use date.
  Income-tax: block-wise WDV rates, half rate for assets put to use for under 180 days in the year —
  a separate working, not a book entry.
- Dr `Depreciation` (by class or cost centre) / Cr the asset or `Accumulated Depreciation`.

**Prepaid expenses:**
- From the prepaid schedule (insurance, AMC, software subscriptions, rent paid in advance).
- Period amortisation = amount x months elapsed / months covered.
- Dr the expense / Cr `Prepaid Expenses`. At payment: Dr `Prepaid Expenses` / Cr Bank.

**Salary and payroll provisions:**
- Salary for days worked but unpaid; employer PF and ESI contributions; bonus (Payment of Bonus Act,
  where applicable); leave encashment and gratuity (AS 15 / Ind AS 19 — actuarial valuation where
  required); professional tax deducted.
- Dr `Salaries & Wages`, `Contribution to PF & ESI`, `Bonus`, `Gratuity` / Cr `Salary Payable`,
  `PF Payable`, `ESI Payable`, `PT Payable`, `TDS Payable - 192`, `Provision for Bonus/Gratuity`.
- Flag s.43B (Income-tax Act, 1961): employer contributions, bonus and leave encashment are allowed on
  payment; employees' PF/ESI contribution must be deposited by the due date under that law
  (s.36(1)(va)). From tax year 2026-27 the Income-tax Act, 2025 applies — confirm the section via `kb`.
  Detail of the payroll run: `fortax-payroll-monthly-run`.

**Revenue:**
- Review contracts and what has been delivered or performed (AS 9 / Ind AS 115).
- Unbilled revenue: Dr `Unbilled Revenue` / Cr Sales or `Service Income`.
- Advance billed but not earned: Dr Sales / Cr `Income Received in Advance`.
- GST follows the time of supply rules, not the accounting accrual — note the difference for 3B.

**GST entries** (common in rectifications):
- Purchase: Dr Expense/Asset, Dr `Input CGST/SGST/IGST` / Cr party.
- Sale: Dr party / Cr Sales, Cr `Output CGST/SGST/IGST`.
- Reverse charge: Dr Expense, Dr `Input GST (RCM)` / Cr party (net), Cr `Output GST (RCM) Payable`.
- Monthly set-off: Dr `Output GST` / Cr `Input GST`, Cr `Electronic Cash Ledger` or Bank for the cash
  portion. Ineligible credit (s.17(5) CGST Act) goes to the expense or asset, not to input.

**TDS on payments to others:**
- Dr Expense (gross) / Cr party (net), Cr `TDS Payable - <section>`; on deposit Dr `TDS Payable` / Cr Bank.

**Rectification entries** (from a BRS or reconciliation): reverse the wrong posting and pass the right
one, or a single net correcting entry; the narration names the original voucher number and date.

## Step 2 — present the entry

```
Journal Entry: [Type] — [Period]
Company: Sharma Traders Pvt Ltd
Prepared by: [name]          Date: [period end date, e.g. 31-03-2027]

| Line | Ledger                    | Group            | Dr (Rs)  | Cr (Rs)  | Cost centre | Narration |
|------|---------------------------|------------------|----------|----------|-------------|-----------|
| 1    | Audit Fees                | Indirect Expenses| 1,00,000 |          | HO          | Statutory audit FY 2026-27, engagement letter dated ... |
| 2    | TDS Payable - 194J        | Duties & Taxes   |          | 10,000   |             | TDS on audit fee provision |
| 3    | Outstanding Expenses      | Current Liabilities|        | 90,000   |             | Audit fee payable |
|      | Total                     |                  | 1,00,000 | 1,00,000 |             |           |

Supporting working: [basis, assumptions, the schedule or document it comes from]
Reversal: [Yes/No — if yes, the reversal date, e.g. 01-04-2027]
```

Figures in the table come from the working file (formulas), with totals computed, not typed.
Amounts use the Indian grouping (1,00,000). The rate shown in the example is illustrative — take the
actual one from `kb` and quote its source.

## Step 3 — review checklist

- [ ] Debits equal credits (a formula check in the working, not a glance)
- [ ] Correct period and voucher date
- [ ] Ledgers exist in the client's books and sit under the right group
- [ ] Amounts traced to the supporting working; the working traced to documents
- [ ] Narration is specific enough for an auditor: what, which period, which document
- [ ] Cost centre / branch coding is correct
- [ ] Treatment is consistent with last period's entry of the same type
- [ ] Reversal flag set where appropriate (accruals and provisions for bills that will be booked)
- [ ] GST and TDS consequences considered and flagged
- [ ] Within the authority of whoever will approve it
- [ ] Nothing unusual or out of pattern left without a note

## Step 4 — output

Into `<Client>/<FY>/Books/` (or next to the inputs), named with the client and period, e.g.
`JV_year-end-provisions_2027-03.xlsx`:

1. The formatted entry (sheet `Entries`), one row per line, in the columns above.
2. The supporting calculations (sheet `Working`), with live formulas.
3. Comparison with last period's entry of the same type, where available.
4. Items flagged for review or follow-up (TDS not deducted, ledger to be created, missing document).
5. Posting instructions: manual entry in Tally (Gateway of Tally -> Vouchers -> F7 Journal), or the
   import layout the client's software accepts. The CA or accountant posts.

## Credit

Workflow, entry types and checklist adapted from anthropics/knowledge-work-plugins (Apache-2.0).
Changed by Fortax: Indian ledgers and groups, Companies Act/Income-tax depreciation, GST, TDS and
payroll entries, rupee formatting, no connector placeholders.
