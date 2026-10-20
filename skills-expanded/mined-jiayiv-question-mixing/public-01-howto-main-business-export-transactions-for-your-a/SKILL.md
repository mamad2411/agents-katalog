---
name: export-transactions-for-your-accountant
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 10min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Export transaction data for your accountant with the right date range, accounts, and supporting reports.

## Preconditions

- You know the accountant's requested period, format, and scope.
- Bank feeds and obvious uncategorized transactions have been reviewed.
- You can access reports or export tools in the accounting system.

## Steps

1. **Confirm the requested scope.** Identify date range, accounts, report basis, file format, and whether attachments are needed. → *Expect:* export requirements are written down.
2. **Open the export or reports area.** Go to reports, accounting export, transactions, or accountant tools. → *Expect:* export options are visible.
3. **Select date range and accounts.** Choose the requested period and include bank, credit card, sales, purchases, payroll, or journal data as needed. → *Expect:* the export preview matches the requested scope.
4. **Choose format.** [BRANCH: CSV | spreadsheet | PDF | accountant access] select the format your accountant requested or grant accountant-user access if preferred. → *Expect:* the output type is correct.
5. **Run the export.** Generate the file or report package. → *Expect:* the system creates downloadable files or confirms access.
6. **Review for completeness.** Check row counts, date range, headers, and whether sensitive fields are necessary. → *Expect:* the export contains the expected transactions and no obvious extras.
7. **Send securely.** Use the accountant portal, encrypted share, or approved secure email method. → *Expect:* the accountant can access the files through a secure channel.

## Decision points

- Accountant has direct access → send a note with the period instead of exporting sensitive files.
- Payroll or personal data is included → limit export to required fields or use a secure portal.
- Books are not ready → send draft status and list open items.
- Attachments are requested → export receipts separately only if the system supports it securely.

## Failure modes & recovery

- **F1 Wrong period:** detect by file dates outside the requested range → recover by regenerating with correct dates.
- **F2 Missing account:** detect by absent bank, card, or loan account → recover by adding the account to the export.
- **F3 File unreadable:** detect by accountant unable to open or parse file → recover by exporting CSV or another requested format.
- **F4 Sensitive over-share:** detect by payroll, full bank details, or customer data not needed → recover by redacting or narrowing the export and replacing the shared file.

## Verification

The accountant receives the requested files or access covering the correct period, accounts, format, and supporting reports through an approved secure channel.

## Variations

- [BRANCH: QuickBooks | Xero | generic] QuickBooks may offer accountant copies, reports, or invited accountant access; Xero often uses advisor access and export reports; generic tools may export ledgers or transaction CSVs.
- `us`: tax preparers may ask for general ledger, trial balance, P&L, balance sheet, payroll reports, and sales-tax reports.

## Safety & privacy

Medium risk because exports may include bank, payroll, vendor, and customer data. Share only the requested scope through secure channels and remove access when no longer needed.
