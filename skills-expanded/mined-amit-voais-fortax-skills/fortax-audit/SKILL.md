---
name: fortax-audit
description: Audit fieldwork support for statutory, tax and internal audits - build the working paper file (index, lead schedules, analytical review of the trial balance, ratios, ledger scrutiny area by area, voucher sampling, tick marks, review points), pull Form 3CD and CARO data from the ledgers with source references, test internal financial controls (IFC under s.143(3)(i), or SOX 404 for US-linked groups) with sample sizes, evidence standards and deficiency classification, and draft management letter points. Opinions and sign-off stay with the auditor. Typical asks - "audit file ready karo", "ledger scrutiny karo", "vouching ke liye sample nikalo", "3CD ke clauses bharne hain", "CARO points", "IFC testing", "management letter".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
  credits: "Control testing methodology, sample selection, documentation standards, deficiency classification and control types adapted from anthropics/knowledge-work-plugins, https://github.com/anthropics/knowledge-work-plugins (Apache-2.0)"
---

# Audit support and working papers

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

You prepare workings, samples, data pulls and flags with a source on every figure. **Opinions,
materiality decisions, deficiency conclusions and sign-off are the auditor's.** Nothing here is audit or
legal advice; every working paper is reviewed by the engagement partner.

Rules change by year: sections below are cited for the Income-tax Act, 1961 (tax years up to
2025-26). From tax year 2026-27 the Income-tax Act, 2025 and its rules apply, with new section and form
numbers — including the tax audit report. Before using a clause or limit, check it with
`python3 scripts/fortax.py kb "<clause or limit>" --topics itr` and quote the source and captured date,
or mark it "confirm on the portal / notification".

## Inputs

- Trial balance for the current and previous year; ledgers (Tally/Busy/Zoho export, .xlsx/.csv).
- Last year's audited financial statements, audit report, CARO report, tax audit report and
  management letter.
- Fixed asset register, stock records, debtor/creditor ageing, loan statements and sanction letters,
  bank statements and BRS, GST returns (GSTR-1, 3B, 9/9C), 26AS/AIS, TDS returns, PF/ESI challans,
  board minutes, statutory registers.
- The engagement type: statutory audit (Companies Act), tax audit (s.44AB), internal audit, bank or
  stock audit, IFC testing.

Folder: `<Client>/<FY>/Audit/`.

## Step 1 — trial balance and analytical review

1. Load the TB (current and previous year) and map it (`fortax-financial-statements` Step 1).
2. Variance analysis: every line with a movement over 20% **or** over Rs 1 lakh (or the thresholds the
   auditor sets) gets a one-line reason to obtain. Method and narratives: `fortax-variance-analysis`.
3. Ratios, current vs previous year, outliers flagged: gross profit %, net profit %, debtor days,
   creditor days, inventory days, current ratio, debt-equity, interest coverage (and the Schedule III
   ratios for companies, reason required for changes over 25%).
4. Materiality: the auditor sets it (SA 320). Record the benchmark and % used; sampling and "above
   materiality" selections below use that figure.

All figures by formula in the workbook; nothing added by eye.

## Step 2 — ledger scrutiny, area by area

**Sales and purchases**
- Cut-off around 31 March: invoices and goods movement in the last and first week; credit notes issued
  after year end relating to the year.
- Related-party transactions: s.188 Companies Act approvals, AS 18 / Ind AS 24 disclosure.
- GST turnover vs books: GSTR-1 and 3B totals vs sales ledgers, month-wise, differences explained
  (`fortax-reconciliation`); ITC in books vs GSTR-2B (`fortax-gstr2b-reconciliation`).

**Expenses**
- Personal expenses; capital items expensed.
- Cash payments over the s.40A(3) limit (Rs 10,000 per person per day; Rs 35,000 for transporters).
- TDS applicability on each expense head — map heads to sections (194C contractors, 194J professional /
  technical, 194I rent, 194H commission, 194Q purchase of goods, 192 salary ...), deducted or not, rate,
  deposited on time; disallowance under s.40(a)(i)/(ia).
- s.43B items (statutory dues, bonus, leave encashment, interest to banks, MSME payments under 43B(h))
  paid before the due date.
- Prior-period items.

**Fixed assets**
- Additions supported by invoices; put-to-use dates; capital work-in-progress ageing.
- Depreciation under the Companies Act (Schedule II, SLM/WDV, useful life, residual value) vs
  Income-tax (block-wise WDV, half-rate rule for assets used under 180 days).
- Disposals: profit or loss in books; block adjustment and short-term capital gain in tax.
- Title deeds in the company's name (Schedule III and CARO).

**Loans and borrowings**
- Cash loans or deposits taken or repaid in breach of ss.269SS / 269T (Rs 20,000).
- Interest accrual and TDS on interest; covenants in the sanction letter.
- Loans to directors and related parties (ss.185 / 186 Companies Act); deemed dividend s.2(22)(e).
- Balance confirmations for significant parties.

**Statutory dues**
- GST, TDS, PF, ESI, professional tax: month-wise paid vs payable, delays and interest — for 3CD
  (43B and TDS clauses) and CARO clause 3(vii).

**Cash and bank**
- BRS at year end, old unreconciled items (`fortax-bank-statement-to-books`); cash balance physically
  verified; negative cash days; cash receipts of Rs 2 lakh or more (s.269ST).

## Step 3 — sampling for vouching

- **All** vouchers above materiality (or the auditor's key-item threshold), plus a random or systematic
  sample from the rest (methods and sizes in [references/control-testing.md](references/control-testing.md);
  SA 530 for audit sampling).
- Generate the random selection with a script and record the seed, so the sample can be reproduced.
- List each selected voucher with the documents expected: invoice, GRN / delivery challan, PO,
  approval, payment proof, GST invoice validity (GSTIN, HSN, tax), TDS deducted.
- Results column per item: pass / exception, with what was seen.

## Step 4 — tax audit (Form 3CD) data pulls

Where tax audit applies, fill from the ledgers with a source reference (ledger, voucher no, date) on every
line. Clause numbers below are for Form 3CD under the Income-tax Rules, 1962 — map them to the new form
before use for tax year 2026-27:

- Clause 21 — amounts debited to P&L that are inadmissible (personal, penalties, 40(a), 40A(3), 40A(2)(b)).
- Clause 26 — s.43B sums: paid before the due date of return or not paid.
- Clause 31 — loans and deposits taken or repaid, and specified sums received, otherwise than by
  account payee cheque / bank draft / electronic mode (269SS, 269T, 269ST).
- Clause 34 — TDS / TCS compliance: sections, amounts, deducted, deposited, delay, returns filed.
- Clause 44 — break-up of expenditure by GST registered / unregistered / composition suppliers.
- Also commonly pulled: clause 18 (depreciation block-wise), 20(b) (employees' PF/ESI contribution paid
  late), 22 (MSME interest disallowance), 36A (deemed dividend).

## Step 5 — CARO 2020 pulls (companies to which it applies)

Point by point, with evidence: fixed assets and title deeds (3(i)); inventory verification and quarterly
returns to banks vs books (3(ii)); loans, guarantees and investments given (3(iii)); ss.185/186
compliance (3(iv)); deposits (3(v)); cost records (3(vi)); statutory dues undeposited and disputed
(3(vii)); undisclosed income surrendered (3(viii)); defaults in repayment and use of loans (3(ix));
fund raising (3(x)); fraud and whistle-blower complaints (3(xi)); related-party compliance (3(xiii));
internal audit (3(xiv)); non-cash transactions with directors (3(xv)); cash losses (3(xvii)); auditor
resignation (3(xviii)); ability to meet liabilities (3(xix)); CSR unspent (3(xx)). Confirm the order's
current text and applicability exemptions before use.

## Step 6 — internal financial controls testing

For companies where the auditor reports on IFC over financial reporting (s.143(3)(i), ICAI Guidance
Note on Audit of Internal Financial Controls over Financial Reporting), or SOX 404 work for a US-listed
group: scope significant accounts and assertions, document and walk through controls, test design and
operating effectiveness on samples, classify deficiencies (deficiency / significant deficiency /
material weakness), and track remediation. The full method is in
[references/control-testing.md](references/control-testing.md).

## Working paper standards (SA 230)

- **Index:** A (planning, materiality, engagement letter), B (TB, lead schedules, analytical review),
  C onwards one section per area (C sales, D purchases, E expenses, F fixed assets, G loans, H statutory
  dues, J cash and bank, K equity), T (tax audit), R (CARO), X (IFC), Z (review points, management letter).
- **Lead schedule** per area: TB lines, current and previous year, adjustments, final, cross-reference to
  the detail papers.
- **Tick marks**, with a legend on each paper: e.g. `T` traced to TB, `V` vouched to invoice, `B` agreed to
  bank statement, `C` agreed to confirmation, `R` recalculated, `X` exception.
- Each paper: client, period, area, objective, procedure, source, result, conclusion space for the
  auditor, preparer and date, reviewer and date.
- **Review points** sheet: point, paper reference, raised by, response, cleared by, date.

## Output

Into `<Client>/<FY>/Audit/`, with area and date in the name:

- `Audit_<area>_workpaper.xlsx` per area (lead schedule, detail, sample, results, tick-mark legend).
- `Audit_3CD_data.xlsx` and `Audit_CARO_points.xlsx` where applicable, source on every line.
- `Management_letter_points.md`: observation, risk / impact, recommendation, management response
  (blank for the client), each linked to the working paper.
- A short summary for the auditor: verdict first (what needs their attention), open items, exceptions
  found, documents still awaited.

Opinions and sign-off are the auditor's; you provide workings and flags only. Letters to the client are
drafts the CA sends.

## Credit

Control-testing method adapted from anthropics/knowledge-work-plugins (Apache-2.0). Changed by Fortax:
set in Indian audit practice (Standards on Auditing, s.143(3)(i) IFC, CARO 2020, Form 3CD) and merged
with Fortax's working-paper method.
