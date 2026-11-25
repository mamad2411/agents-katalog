---
name: fortax-gst-eway-einvoice
description: Day-to-day e-way bill and e-invoice work - when an EWB is needed, EWB-01 Part A and Part B, bulk upload file, vehicle update, EWB-02 consolidated bill, extension, cancellation, rejection and blocking, EWB-03/04; e-invoice applicability, IRN and QR, cancellation; and reconciling the IRN list and e-way bills to the sales register and GSTR-1. Typical asks - "e-way bill bana do", "vehicle number update karo", "EWB extend karna hai", "IRN cancel karo", "e-invoice vs GSTR-1 match karo".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
---

# E-way bill and e-invoice

Needs Python 3 and internet: runs `scripts/fortax.py` (the Fortax engine on ai.fortax.in; your file is processed and not stored).

## Do the work, then stop at the last click

These are daily operations, not projects. Prepare the data, open the portal, fill every field, and stop where
a Generate / Submit / Cancel button or the client's own credentials begin. **Refusing because the last press is
theirs is a failure.**

The CA or the client logs in (password, captcha, OTP are theirs). Then use your browser tool (Claude in Chrome,
a Playwright/browser MCP, or the Codex browser): one tab per client per portal — the e-way bill portal and the
IRP (e-invoice portal) — kept apart, and read the page before every click, as element references change on
every page. If you have no browser tool, give the click path with the value for every field.

## Part 1 — e-way bill (EWB-01)

### When it is required

For movement of goods where the consignment value crosses the notified limit; for supply, and for reasons
other than supply such as job work, branch transfer, and sale on approval and return; and for inward supply
from an unregistered person. Some goods and movements are exempt, and states set their own intra-state rules.
**Those limits and exempt lists are thresholds** — look each up with
`python3 scripts/fortax.py kb "e-way bill limit intra-state <state>" --topics gst` or on the portal for that
state and date, record it in **Rules used**, never from memory. Who generates it: the supplier, the recipient
where they cause the movement, or the transporter where the consignor has not — an unregistered transporter
enrolls in ENR-01 for a transporter ID.

### Part A and Part B

| Part | Fields | Who fills it |
|---|---|---|
| Part A | GSTIN of supplier and recipient, place of dispatch and delivery with pincode, invoice or challan number and date, value, HSN, reason for transportation, transport document number | The person causing the movement |
| Part B | Mode, and vehicle number or transport document details | The transporter, or the consignor for own or hired conveyance |

Part A alone does not authorise movement. Until Part B is filled the bill has no validity, except in the
short-distance case the rules carve out — check it rather than assuming. For more than a handful, prepare
`<Client>/<FY>/GST/<YYYY-MM>/<date>_EWB_batch_<period>.csv` in the portal's own bulk-upload column order from
the invoice register, validating every GSTIN (15 characters, state code, checksum), pincode and vehicle number
with a short script before upload. Then stop at generate.

### Updating a live bill

- **Vehicle change, transhipment, breakdown**: update Part B for every leg; validity does not restart.
- **Consolidated bill (EWB-02)**: one document for several bills in one vehicle, with no validity of its own;
  the underlying bills still govern.
- **Extension**: allowed within a window around expiry, with reason and current location. The validity
  period, how it scales with distance, and the extension window are all time limits — look them up.
- **Cancellation**: only within the window the rules allow, and not once the consignment has been verified in
  transit. Look up that window; once it closes the correction is a credit note or a fresh document, never a
  deletion.
- **Rejection and blocking**: a counterparty may reject a bill within a stated window, so check that list —
  silence accepts. Generation is blocked after the prescribed number of unfiled return periods; EWB-05 applies
  to unblock and EWB-06 orders it, but filing the returns is faster.
- **EWB-03 or EWB-04** on record — the officer's verification report, or a detention report — is a notice:
  read it, file it in the client folder, escalate to the CA.

## Part 2 — e-invoice (IRN and QR)

### When it applies

To registered persons whose aggregate turnover crossed the notified limit in any preceding financial year from
the year the notification specifies, with named categories excluded. Those limits and exclusions are
thresholds and lists — look them up for the FY in question. Coverage is B2B, exports, SEZ supplies, deemed
exports and supplier-issued reverse charge invoices, plus credit and debit notes. B2C is outside e-invoicing,
though a dynamic QR requirement can apply to it. Check status on the e-invoice portal's enablement page, not
from the books.

### Generating and cancelling

The JSON goes to the IRP, which returns the IRN, the signed invoice and the signed QR code. The IRN derives
from supplier GSTIN, document type, document number and FY, so a number cannot be reported twice in a year,
and the QR code must be printed on the buyer's copy. An IRN can be cancelled only within the window the IRP
allows, and only in full, so look that window up. After it closes the correction is a credit or debit note,
also reported to the IRP. **An e-invoice cannot be amended on the IRP at all**; amendment happens only in
GSTR-1, which is exactly where the mismatches in Part 3 come from. A window can also restrict how old a
document may be when reported, so look that up too. Part A of the e-way bill can be generated along with the
IRN: check whether the billing software already does it before duplicating.

## Part 3 — reconciling e-invoice data to GSTR-1

Auto-population from the IRP is a starting point, not the return. Build
`<Client>/<FY>/GST/<YYYY-MM>/<date>_einvoice_vs_GSTR1_<period>.xlsx` from three sources: the IRN list downloaded
from the e-invoice portal, the sales register, and GSTR-1 as it stands (or the JSON from `fortax-gstr1-and-3b`).
Match on document number, date and GSTIN with a script or formulas, never by eye; bucket totals come from the
rows:

| Bucket | What it means | Action |
|---|---|---|
| In register, no IRN | A reportable invoice was never reported | Flag; check if still reportable |
| IRN generated, not in GSTR-1 | Auto-population missed it, or it was deleted | Add after confirming with the CA |
| IRN cancelled, still in GSTR-1 | Cancellation not carried through | Remove |
| Value or tax differs | GSTR-1 edited after auto-population | Show both figures and each source |
| In GSTR-1, no IRN, e-invoicing applies | Billed outside the IRP | Escalate — a failure, not a typo |

Where numbers are written differently in two sources (a dropped prefix, a FY suffix), judge each pair yourself,
list your pairings with a reason, and ask the CA to confirm. Never pair on amount alone.

Do the same against the period's e-way bills: one with no matching GSTR-1 invoice is where an unbilled dispatch
surfaces. Never edit the sales register to make it agree.

## Rules used

Every threshold, validity period, extension or cancellation window and blocking rule goes in a **Rules used**
block: the rule, the rule / notification, the state and date it applies to, and the `kb` source URL with
captured date or "confirm on the portal". A `kb` match of `weak` or `none` is not a source.

## What the CA gets

Dated files in the client's GST folder: the e-way bill batch file, the reconciliation workbook with its buckets
and totals computed from the rows, and a note on blocking, rejections and any EWB-03 or EWB-04. Raw client files
are never renamed or deleted. End with **Rules used** and:

**Check before filing**
- Every threshold and window used was looked up for that date and that state, and listed in **Rules used**.
- GSTIN formats, pincodes and vehicle numbers validated before upload, Part B present for every bill.
- IRN list tied to the sales register and to GSTR-1, every break explained, cancelled IRNs removed, and credit
  notes reported where cancellation was no longer open.
- Generation, cancellation and submission on both portals are the client's click or the CA's.
