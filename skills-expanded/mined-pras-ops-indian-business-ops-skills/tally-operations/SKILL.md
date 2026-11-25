---
name: tally-operations
description: >-
  Moving accounting data in and out of Tally (Tally Prime / Tally.ERP 9) and reconciling the
  books to filings: generating Tally-importable XML (vouchers, ledgers, stock items), parsing
  Tally exports (day book, ledger, trial balance in XML/Excel/CSV), mapping to GST returns,
  and reconciling Tally data against GSTR-1 / GSTR-2B / Form 26AS. Use for Tally
  import/export, Tally XML, vouchers/ledgers/day book/trial balance, or syncing the books with
  GST/TDS. For the GST rules themselves use gst-compliance; for TDS rules use tds-compliance.
---

# Tally operations (India)

Tally (Tally Prime, and the older Tally.ERP 9) is the most common bookkeeping software in Indian
businesses. This skill helps **exchange data with Tally** and keep the books consistent with the
GST and TDS filings those books feed — it works with files you export/import; it does not control a
running Tally licence.

> [!IMPORTANT]
> Tally's XML schema and some behaviours differ between **Tally Prime** and **Tally.ERP 9** and
> across releases. Confirm tag names against the version in use before trusting an import, and
> always import into a **test company first**. Treat tax rates/fields per the `gst-compliance` and
> `tds-compliance` skills — don't bake rates into mappings.

## Reading live Tally data (the action layer)

This skill works with files you export and import. To let an agent read a *running* Tally
company directly (outstanding receivables, live P&L, this month's GST liability), the clean route
is a **Tally MCP server** — a separate action-layer component that exposes Tally over the Model
Context Protocol, which these skills can then drive. Keep that integration as its own component
with its own access control; this skill stays the "understand and map the data" layer, not the
"log in and change the books" layer.

<!-- Add a verified link here: an open-source Tally MCP server you have checked (name, repo,
     licence). Left blank on purpose rather than citing an unverified one. -->

## How Tally exchanges data

Read [`references/tally-xml-and-import.md`](references/tally-xml-and-import.md) for the concrete
formats and a voucher XML skeleton. The three routes:

1. **XML (native).** Tally imports and exports a specific XML dialect (`<ENVELOPE>` → `TALLYMESSAGE`
   with `VOUCHER`, `LEDGER`, `STOCKITEM` elements). This is the reliable route for bulk/automated
   import of vouchers and masters.
2. **Excel / CSV.** Tally exports day book, ledgers, trial balance and GST reports to Excel; for
   import, data is usually converted to XML first (directly importing arbitrary Excel is limited).
3. **ODBC / HTTP-XML (advanced).** A running Tally instance can serve/accept XML over a local port
   for live integration — version- and setup-dependent; mention it but don't assume it's available.

## The golden rule of masters

Tally matches on **exact names**. A voucher that references a ledger or stock item imports cleanly
**only if that master already exists with the identical name** (spacing, case, punctuation). So:

- **Import or confirm masters first** (ledgers, stock items, GST details), **then** vouchers.
- A single name mismatch ("ABC Traders" vs "ABC Traders ") creates a duplicate ledger or fails the
  row. Normalise names before generating XML.

## Common jobs and how to approach them

- **Bulk-import sales/purchases:** map the source columns to voucher fields (date, voucher type,
  party ledger, sales/purchase ledger, GST ledgers, item, qty, rate, amount), confirm every
  referenced ledger/item exists, generate voucher XML, import into a **test company**, verify
  totals, then import to live.
- **Parse a Tally export:** read the exported XML/Excel (day book, ledger, trial balance), extract
  the rows, and produce the summary or sheet the user needs.
- **Map to a GST return:** turn Tally sales data into the structure GSTR-1 expects (B2B invoice-wise,
  B2C summary, HSN summary, credit/debit notes), flagging anything missing a GSTIN or HSN.
- **Reconcile:** compare Tally against the external truth —
  - Sales in Tally ↔ **GSTR-1** filed.
  - Purchase/ITC in Tally ↔ **GSTR-2B**.
  - TDS entries in Tally ↔ **Form 26AS / AIS**.
  List mismatches with the likely cause (missing entry, wrong GSTIN, rate difference, period
  mismatch).

## How to help, concretely

- When generating import XML, produce a small, **validated sample first** (one or two vouchers),
  have the user import it into a test company and confirm it lands correctly, then scale up. This
  catches schema/version mismatches cheaply.
- When parsing, don't assume column positions — read the header row and map by name.
- Keep a clear audit trail: show the mapping you used (source field → Tally field) so the user can
  check it.

## Guardrails

- **Always a test company first** for imports; Tally imports are hard to cleanly undo in a live
  company.
- Confirm **Tally Prime vs ERP 9** and the release — tag names and GST fields differ.
- Numbers and classifications follow the GST/TDS skills; this skill moves and maps data, it doesn't
  decide tax rates.
