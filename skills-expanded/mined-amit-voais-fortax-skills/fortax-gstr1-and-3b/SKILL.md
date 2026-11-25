---
name: fortax-gstr1-and-3b
description: Build a client's monthly or quarterly GSTR-1 portal JSON from their sales register (Tally, Busy, Zoho, Excel or any export) and a GSTR-3B working paper with output tax, ITC from 2B, set-off, interest and late fee. Checks credit notes, minus lines, place of supply vs IGST/CGST, header discounts and the HSN rule. Typical asks - "GSTR-1 bana do", "Aug ka GSTR-1 JSON", "3B working ready karo", "sales register se GSTR-1", "kitna tax cash me bharna hai".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# GSTR-1 and GSTR-3B

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

Two outputs for one period: the GSTR-1 JSON the CA uploads on the portal, and the GSTR-3B working paper
the CA files from. The engine builds GSTR-1 and computes the figures. You read its summary out, judge
what code cannot (HSN/SAC for an item), check the register for the traps below, and assemble 3B.
The CA uploads, files, pays and signs.

## Inputs (look in `<Client>/<FY>/GST/<YYYY-MM>/` or wherever the CA dropped files)

- **Sales register** for the period — any accounting software export (Tally, Busy, Zoho Books, Marg,
  an ERP, a hand-kept Excel), .xlsx or .csv, one row per invoice or per invoice line. Needs invoice no,
  date, buyer GSTIN, buyer name, place of supply, taxable value, rate, IGST/CGST/SGST, cess, HSN/SAC,
  B2B/B2C, credit/debit notes, exports, SEZ, nil/exempt.
- **Purchase register** with supplier GSTIN, invoice no and date, ITC amount, eligible/ineligible tag.
- **GSTR-2B** for the period (portal JSON, zip or Excel) — see `fortax-gstr2b-reconciliation`.
- **Previous period's 3B** — carry-forward ITC, negative liability, RCM paid.
- **RCM register** — GTA, legal fees, import of services, security services, others notified.

If a file is missing, list it under "Data needed" and continue with what exists.

## Step 1 — lock the period

- Month or quarter, and filer type (monthly or QRMP). Ask the CA if it is not in the folder or their notes.
- GSTIN: 15 characters, state code (first two digits) matches the client's state, PAN inside it matches.
- Due dates for GSTR-1 and 3B: `python3 scripts/fortax.py kb "GSTR-1 due date QRMP" --topics gst`
  and `kb "GSTR-3B due date"`. Quote source and captured date. `weak` or `none` -> say "confirm on the
  portal" rather than answering from memory.

## Step 2 — GSTR-1 from the sales register (the engine)

```bash
python3 scripts/fortax.py gstr1 --sales "<register.xlsx>" --gstin 09ABCDE1234F1Z5 --fp 082026 \
  --company "Sharma Traders" [--sheet "Sales Register"] [--out <folder>]
```

- Headers it recognises: invoice no, invoice date, buyer GSTIN, buyer name, place of supply, invoice
  value, HSN/SAC, description, UQC, quantity, GST rate, taxable value, IGST, CGST, SGST/UTGST, cess,
  reverse charge, invoice type, e-commerce GSTIN. A clean minimal layout that works:
  `Invoice No, Invoice Date, Party GSTIN, Party Name, Place Of Supply, Rate, Taxable Value, Invoice Value`
  — one row per invoice per rate.
- **Column not recognised** -> the summary names it. Rerun with a map from field key to the register's
  header: `--map '{"inum":"Bill No","txval":"Basic Amt"}'`. Keys: `inum idt ctin cname pos val hsn desc
  uqc qty rt txval iamt camt samt csamt rchrg ityp etin`.
- **Several registers in one workbook** -> `--sheet`.
- Output next to the register: `GSTR1_<GSTIN>_<MMYYYY>.json` (portal upload) and `_summary.txt`.
  **Errors block the JSON**; the summary lists them by invoice number.

Read the summary out as it is — totals, B2B/B2C, errors, file paths. **Do not recompute, re-add,
re-list or re-verify any engine figure.** If the JSON was not made, tell the CA which invoices to fix in
their accounting software, re-export, and rerun — except HSN.

### HSN/SAC missing — you classify, you do not ask the CA

When the reply ends with a NEXT STEP about lines without HSN/SAC:

1. Classify each listed item yourself. Services by the scheme of classification of services
   (Notification 11/2017-Central Tax (Rate), Annexure); goods by the Customs Tariff. Examples: a land or
   tour package is 998555 tour operator services; ticket or hotel booking 998551 / 998552; visa
   assistance 998559; a cancellation charge takes the SAC of the service cancelled.
2. Write `{"item description exactly as listed": "code"}` to a JSON file next to the register
   (e.g. `hsn_map_082026.json`).
3. Rerun the same command with `--hsn-map hsn_map_082026.json`.
4. Name every code you chose in the reply and ask the CA to confirm them and set them in the item
   master of their software, so next month's export carries them.

### HSN summary rule

HSN digits in the GSTR-1 HSN table depend on aggregate turnover of the preceding FY (the rule in force
since 1 April 2021 is 4 digits up to ₹5 crore, 6 digits above; B2C lines may be relaxed). Confirm the rule
for the period with `kb "HSN digits GSTR-1 Table 12"` before telling the CA the HSN table is fine.

## Step 3 — check the register for what a total cannot show

The engine's figures follow the rows it was given. These traps sit in the export itself. Check each with a
short script or spreadsheet filter over the register (not by eye), and say every one to the CA, even
when nothing was found:

- **Not final documents.** Drafts, proformas, quotations, cancelled or void invoices left in the export
  are not supplies. Remove them from the register before the run, or list them if they went in.
- **Tax type differs from place of supply.** IGST charged where the place of supply is in the client's
  own state (CGST+SGST was due), or CGST+SGST where it is another state. Compare place of supply (or the
  buyer GSTIN's state code) with the tax columns. The return follows place of supply; the CA decides what
  to do about the invoices already issued (credit note and re-issue). Place of supply for services can
  follow special rules — accommodation and immovable property, passenger transport, events, admission,
  tour operator services — where one applies, ask the CA rather than applying the default.
- **Party state unknown.** A B2C row with no place of supply or state is usually taken as the home state
  by software. List those rows; an inter-state B2C sale taken as intra-state shifts tax between heads.
- **Minus lines inside invoices.** A refund, discount or cancellation typed as a negative line inside an
  invoice. If it carries tax, the books' tax is lower than the invoice the customer received. Compare with
  the issued invoice and ask the CA: it belongs on a credit note (CDNR / CDNUR), not as a minus line.
- **Header discount, shipping or bill-level tax.** Amounts charged or given at invoice level and not
  spread across lines (a "Discount" or "Freight" or "Round off with tax" row in the footer). Line-wise
  exports miss them. **Stop and ask** the CA how to spread them before filing.
- **Invoice-level vs line-level totals.** Some exports put "total before tax" that already includes
  line tax on the invoice row and only a bill-level tax in "tax amount" — the invoice row can show tax nil
  while the lines carry lakhs. Build GST figures from the line-level register, never from invoice
  summary rows.
- **Tax without a rate** and **rate without tax** — rows where the tax columns and the rate disagree.
- **Lines without HSN/SAC** — handled in Step 2; if the software suggested codes when items were
  created, still ask the CA to confirm them.
- **Credit notes in the period not included.** Many exports keep sales returns / credit notes in a
  separate register. Ask for it if the period has none. Credit notes cannot exceed the original
  invoice's tax, and cannot be issued after 30 November following the end of the FY of the supply
  (or the annual return date, if earlier — section 34(2); confirm with `kb`).
- **Blank or invalid buyer GSTIN** on a B2B row (15 characters, valid state code, checksum), and
  negative values anywhere.

## Step 4 — GSTR-1 table view for the CA

From the engine summary (not recomputed), set out: B2B (per GSTIN), B2CL (inter-state B2C invoices above
the threshold — ₹2.5 lakh historically, ₹1 lakh from 1 August 2024 by Notification 12/2024-CT; confirm
with `kb`), B2CS (rate-wise, state-wise), CDNR / CDNUR, exports (with and without payment), SEZ,
nil-rated / exempt / non-GST, HSN summary, and document series issued (from–to, cancelled count) from the
register.

## Step 5 — GSTR-3B working paper

1. **Table 3.1 output tax.** From the GSTR-1 summary: taxable value and tax rate-wise, split
   IGST / CGST / SGST / cess; zero-rated, nil/exempt and non-GST separately. Inward supplies liable to
   reverse charge go in 3.1(d) from the RCM register.
2. **Table 4 ITC — start from GSTR-2B, not books.** Run `fortax-gstr2b-reconciliation`; use its Table 4
   figures as they are, do not match by hand. Buckets it gives: matched, in 2B not in books (ask before
   claiming), in books not in 2B (do not claim; park), mismatch. Then remove:
   - ineligible under section 17(5): motor vehicles, food and beverages, club membership, personal
     consumption, works contract / construction of immovable property, CSR expenses, others listed;
   - reversals under Rule 42 / 43 (common credit, exempt supply ratio), Rule 37 (supplier not paid within
     180 days), and Table 4(B)(2) temporary reversals.
3. **Net liability and set-off.** IGST credit first against IGST, then against CGST and SGST in any order;
   CGST credit cannot be set off against SGST, nor SGST against CGST. Show cash payable per head.
4. **Interest and late fee** if filed late: interest at 18% p.a. on the net cash liability from the due
   date to the payment date (section 50); late fee per day under section 47 with the caps notified for the
   period. Get the current amounts from `kb`, cite them. Do the arithmetic in the spreadsheet with formulas.
5. **Write the workpaper**: `<Client>/<FY>/GST/<YYYY-MM>/GSTR3B_<GSTIN>_<MMYYYY>_working.xlsx` (formulas
   live, one sheet per section above, a source column for every figure) and a short `.md` note with the
   figures and the check list. Engine numbers are pasted as values with "Source: Fortax engine summary".

## Check before filing (always include)

- Turnover tie-out: GSTR-1 total vs 3B Table 3.1(a) vs books.
- ITC claimed not more than 2B eligible; parked ITC listed with supplier names.
- RCM liability paid in cash and claimed as ITC in the same period.
- Credit notes not exceeding the original invoice's tax; time limit respected.
- Amendments to earlier periods flagged (they go in the amendment tables, not the current ones).
- No negative values, no blank or invalid GSTINs, place of supply consistent with the tax type.
- Every check in Step 3 said, with what the CA decided.
- Due date, late fee and HSN rule shown with their `kb` source or marked "confirm on the portal".

## The CA keeps

Portal login, OTP, the upload of the JSON, Generate Summary, payment of the challan, EVC/DSC filing.
Stop at the review screen with the checklist above.

## Never

- Recompute, re-add or re-list an engine figure.
- Claim ITC not in 2B "to be safe".
- Ask the CA for HSN/SAC codes you can classify.
- Edit the client's original register — work on a copy if rows must be removed or renamed.
- File, submit or pay anything on the portal.
