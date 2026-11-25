---
name: india-business-ops-router
description: >-
  Start here for running a company in India when a task spans several compliance areas, or when it
  is not clear which area applies. Gives a grouped who-does-what map (Tax & GST, People & Payroll,
  Entity & Filings, Books & Data), a first-time-setup vs ongoing-compliance overview, and routes
  the request to the right dedicated skill (gst-compliance, invoicing-einvoice-eway,
  tds-compliance, payroll-statutory, company-roc-compliance, business-registrations-licenses,
  tally-operations). Use for broad asks like "what compliance does my Indian startup need",
  "which of these applies to us", or an end-to-end setup checklist. For a clearly single-area task
  (one GST return, one TDS deduction, one payroll run), use that specific skill directly instead.
---

# India business ops — router

Use this when the task is broad or you're unsure which skill fits. Pick the dedicated skill below
and follow it; this file only decides *where to go*. If the task is already clearly one area, skip
this and open that skill directly.

## The seven skills, grouped

**Tax & GST**
- `gst-compliance` — GST returns (GSTR-1/3B/9), rates, HSN/SAC, input tax credit, GSTIN validation.
- `invoicing-einvoice-eway` — the sale *document*: tax invoice fields, e-invoice (IRN/QR), e-way bill.

**People & Payroll**
- `payroll-statutory` — salary structure, EPF, ESI, Professional Tax, gratuity, payslips, salary TDS (192).
- `tds-compliance` — TDS/TCS on *vendor / non-salary* payments (194-series, 195), deposits, quarterly returns, Form 16/16A.

**Entity & Filings**
- `business-registrations-licenses` — starting up: entity choice, PAN/TAN, GSTIN, Udyam, Shops & Est., IEC, FSSAI.
- `company-roc-compliance` — after incorporation: recurring MCA/ROC filings (AOC-4, MGT-7), DIR-3 KYC, registers.

**Books & Data**
- `tally-operations` — moving data in/out of Tally and reconciling the books to GST/TDS filings.

## Route by what the user is actually asking

| If the task is about… | Go to |
|---|---|
| A GST return, a GST rate, input tax credit, checking a GSTIN | `gst-compliance` |
| Making an invoice, e-invoice (IRN/QR), e-way bill | `invoicing-einvoice-eway` |
| Deducting tax on a vendor/contractor/professional/landlord payment, TDS returns, Form 16A | `tds-compliance` |
| Salaries, payslips, PF/ESI/PT, gratuity, Form 16 for staff | `payroll-statutory` |
| Starting/registering a business, picking Pvt Ltd vs LLP, a licence | `business-registrations-licenses` |
| Annual company/LLP filings, director KYC, registers (already incorporated) | `company-roc-compliance` |
| Importing/exporting Tally data, reconciling books to returns | `tally-operations` |

## The two common distinctions people get wrong

- **Setting up vs staying compliant.** "How do I register / which licence" → `business-registrations-licenses`.
  "What do we file every year now that we exist" → `company-roc-compliance`.
- **Salary tax vs vendor tax.** TDS on an employee's salary and the PF/ESI/PT around it →
  `payroll-statutory`. TDS on a payment to a contractor, professional, landlord or non-resident,
  and the quarterly TDS returns → `tds-compliance`.

## First-time setup, in order (end-to-end asks)

1. Choose entity + register → `business-registrations-licenses` (PAN/TAN, GSTIN, Udyam, Shops & Est.).
2. Start invoicing correctly → `invoicing-einvoice-eway`, with `gst-compliance` for the GST on each sale.
3. Hire people → `payroll-statutory` (EPF/ESI/PT), and `tds-compliance` once you pay vendors.
4. Keep the books → `tally-operations`.
5. File on the cycle → `gst-compliance` (monthly/quarterly), `tds-compliance` (quarterly),
   `company-roc-compliance` (annual).

Whichever you route to, the same rule holds across the pack: **the model decides what to do, the
bundled code does the exact numbers, and current rates/thresholds/dates are confirmed on the
official portal — never guessed.** See the repo's ARCHITECTURE.md.
