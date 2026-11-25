---
name: fortax-financial-statements
description: Prepare financial statements from a trial balance - Schedule III (Division I for AS, Division II for Ind AS) balance sheet, statement of profit and loss, cash flow statement and notes for companies, and the ICAI format for LLPs, firms and proprietors - with ledger-to-line mapping, a tie-back to the TB, comparatives, ratio disclosures, period-end adjustments and a material-variance list. Also monthly / quarterly MIS P&L against prior period and budget. Typical asks - "balance sheet bana do", "TB se final accounts", "Schedule III me daalo", "notes to accounts ready karo", "monthly MIS P&L", "ratios with reasons".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
  credits: "Income statement workflow, variance method, presentation reference and period-end adjustments adapted from anthropics/knowledge-work-plugins, https://github.com/anthropics/knowledge-work-plugins (Apache-2.0)"
---

# Financial statements

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

Build the statements in a workbook where every figure is a formula back to the trial balance. This
skill prepares drafts; the CA reviews, the board / partners approve, and the auditor signs.

## Inputs

- **Trial balance** for the year (or period) and the previous year — Tally/Busy/Zoho export, .xlsx/.csv,
  with ledger name, group, opening, debit, credit, closing.
- Last year's signed financial statements (comparatives, note structure, accounting policies).
- Fixed asset register, ageing of debtors and creditors (with MSME status of suppliers), stock
  statement, loan statements, share capital register, tax computation, and any known adjustments.
- The entity type, which decides the format:

| Entity | Format |
|---|---|
| Company following Accounting Standards (AS) | Schedule III Division I, Companies Act, 2013 |
| Company following Ind AS (listed, or net worth Rs 250 crore or more, and their group — Companies (Ind AS) Rules, 2015; confirm) | Schedule III Division II |
| NBFC following Ind AS | Schedule III Division III |
| LLP, partnership firm, proprietor, trust | ICAI Guidance Note on Financial Statements of Non-Corporate Entities (2022) formats, or as required by the regulator / bank |

Formats line by line: [references/schedule-iii-formats.md](references/schedule-iii-formats.md).
Thresholds that decide small-company exemptions, Ind AS applicability or rounding change by
notification: check with `python3 scripts/fortax.py kb "small company definition paid up capital turnover" --topics mca`
and quote the source and date, or mark "confirm on MCA".

If no TB is given, ask for it. Paste-in data is fine for an MIS; statutory statements need the TB.

## Step 1 — map every ledger

1. Load the TB into a sheet `TB`. Check it first: total debits = total credits, and opening + debits -
   credits = closing for each ledger (formulas). A TB that does not tie goes to `fortax-reconciliation`.
2. Sheet `Mapping`: every ledger gets a Schedule III line and a note number. Group names in Tally are a
   start, not the answer (e.g. `Sundry Creditors` with debit balances are advances to suppliers;
   `Loans (Liability)` has current maturities of long-term debt).
3. A check cell: sum of mapped closing balances = TB total, and count of unmapped ledgers = 0.
   **Do not build statements while any ledger is unmapped.**
4. Ledgers whose placement is a judgement (a director's account, an advance of unclear nature, a
   debit balance in a creditor) are listed for the CA to confirm.

## Step 2 — period-end adjustments

Before the statements, list and pass (as proposed entries, via `fortax-journal-entry`):

1. **Accruals:** expenses incurred not booked (audit fee, interest, salary, power).
2. **Deferrals:** prepaid expenses, income received in advance.
3. **Depreciation and amortisation** under Schedule II.
4. **Provision for doubtful debts / expected credit loss** from the ageing and history.
5. **Inventory:** valuation at cost or NRV, whichever is lower (AS 2 / Ind AS 2); write-down of
   obsolete or slow-moving stock.
6. **Foreign currency:** restate monetary items at the closing rate (AS 11 / Ind AS 21).
7. **Tax:** current tax from the computation; deferred tax (AS 22 / Ind AS 12).
8. **Fair value:** investments and derivatives measured at fair value (Ind AS 109).
9. **Employee benefits:** gratuity and leave (AS 15 / Ind AS 19).
10. **MSME:** interest payable under s.16 MSMED Act on dues beyond 45 days, and its disallowance.

Reclassifications (no P&L effect): long-term borrowings due within 12 months to current maturities;
netting of allowances and accumulated depreciation; related-party / group eliminations on consolidation;
discontinued operations to a separate line; share of associates (equity method) in consolidated
statements; debit balances in creditors and credit balances in debtors to the other side.

## Step 3 — build the statements (sheets with formulas off `Mapping`)

- **Balance Sheet** and **Statement of Profit and Loss** in the Schedule III order, with the previous
  year alongside (reclassify comparatives to match and say so in a note).
- **Cash Flow Statement** (AS 3 / Ind AS 7), indirect method. Not required for a one person company, a
  small company or a dormant company (s.2(40) Companies Act) — confirm the entity's status.
- **Statement of Changes in Equity** for Ind AS companies.
- **Notes**: accounting policies, then one note per line item, and the Schedule III additional
  disclosures (list in the reference file): promoter shareholding, trade receivable and payable ageing,
  CWIP ageing, title deeds not in the company's name, the ratios with reasons for change over 25%,
  MSME dues, related-party transactions, contingent liabilities, CSR, and the rest.
- Rounding as Schedule III allows for the turnover band (confirm the band).

## Step 4 — tie-back checks (each a formula cell that must show TRUE / 0)

- [ ] Total assets = total equity and liabilities, both years
- [ ] Profit for the year in P&L = movement in surplus in reserves (after dividends and transfers)
- [ ] Closing cash and bank in the cash flow = balance sheet = bank BRS balances
- [ ] Every note total = its line on the face
- [ ] Sum of all mapped ledgers = TB; unmapped ledgers = 0
- [ ] Depreciation in P&L = fixed asset note; additions in the note = investing cash flow (after
      capital creditors)
- [ ] Tax expense = current tax + deferred tax; DTA/DTL movement = deferred tax charge
- [ ] Previous-year figures = last year's signed statements (or the reclassification is noted)
- [ ] Revenue in books vs GST returns (GSTR-1/3B, annual return) — differences explained

## Step 5 — comparison and variances

For a management P&L (monthly, quarterly, annual, year-to-date), present current period, comparison
period, variance in Rs and %, and budget where available:

```
STATEMENT OF PROFIT AND LOSS — Sharma Traders Pvt Ltd
Period: Q2 FY 2026-27                                (Rs in lakh)

                              Current   Prior    Var (Rs)  Var (%)  Budget   Budget var
Revenue from operations
  Sale of products              X         X        X        X%       X         X
  Sale of services              X         X        X        X%       X         X
Other income                    X         X        X        X%
TOTAL INCOME                    X         X        X        X%       X         X

Cost of materials consumed      X         X        X        X%       X         X
Purchases of stock-in-trade     X         X        X        X%
Changes in inventories          X         X        X        X%
GROSS MARGIN                    X         X        X        X%
  Gross margin %                X%        X%       X pp

Employee benefits expense       X         X        X        X%       X         X
Other expenses                  X         X        X        X%       X         X
EBITDA                          X         X        X        X%
Finance costs                   X         X        X        X%
Depreciation and amortisation   X         X        X        X%
PROFIT BEFORE TAX               X         X        X        X%       X         X
Tax expense (current, deferred) X         X        X        X%
PROFIT FOR THE PERIOD           X         X        X        X%       X         X
  Net margin %                  X%        X%       X pp
```

Variance: Rs variance = current - comparison; % variance = (current - comparison) / |comparison|;
margins and ratios as change in percentage points (or basis points, 1 bp = 0.01%). Materiality,
decomposition (volume, price, mix, one-time, timing, exchange), narratives and waterfalls follow
`fortax-variance-analysis`.

Key metrics block:

```
KEY METRICS                   Current   Prior    Change
Revenue growth %                                  X%
Gross margin %                X%        X%        X pp
EBITDA margin %               X%        X%        X pp
Net margin %                  X%        X%        X pp
Employee cost % of revenue    X%        X%        X pp
Effective tax rate %          X%        X%        X pp
```

Material variance list:

| Line item | Var (Rs) | Var (%) | Favourable / Adverse | Preliminary driver | Action |
|---|---|---|---|---|---|

For statutory statements, the Schedule III ratio note needs a reason for every ratio that moved more
than 25% — take the reason from the ledgers, not a guess; unknown reasons are questions for the client.

## Output

Into `<Client>/<FY>/Audit/` (or `Books/`), e.g. `FS_Sharma-Traders_FY2026-27_draft.xlsx` with sheets
`TB`, `Mapping`, `Adjustments`, `BS`, `PL`, `CFS`, `Notes`, `Ratios`, `Checks`, plus a short note:

1. The statements with comparatives.
2. Key metrics and the ratio note.
3. Material variances with investigation flags.
4. Proposed adjustments, ledgers whose mapping needs confirmation, and follow-up questions for the client.
5. Any failed check — a blocker, not a footnote.

For a client reporting to a foreign parent under US GAAP or IFRS, the presentation rules and reference
formats are in [references/us-gaap-ifrs-presentation.md](references/us-gaap-ifrs-presentation.md).

## Credit

Workflow, variance method, presentation reference and adjustments adapted from
anthropics/knowledge-work-plugins (Apache-2.0). Changed by Fortax: rebuilt around Schedule III, Indian
Accounting Standards, TB mapping and tie-back checks; US GAAP material moved to a reference file.
