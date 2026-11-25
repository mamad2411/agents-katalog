---
name: invoicing-einvoice-eway
description: >-
  Producing GST-compliant SALE DOCUMENTS in India: a tax invoice with all mandatory fields, a
  bill of supply, credit/debit notes, e-invoicing (generating the IRN and QR code via the
  IRP), and the e-way bill for moving goods. Use when the task is making an invoice or invoice
  template, invoice numbering, a credit/debit note, or deciding whether e-invoice (IRN/QR) or
  an e-way bill applies. For GST returns, rates, classification and input tax credit use
  gst-compliance instead.
---

# Invoicing, e-invoice and e-way bill (India)

Under GST a sale isn't just a bill — the document must carry specific fields, and above certain
thresholds it must be registered electronically (e-invoice) and accompanied by an e-way bill when
goods move. This skill helps produce correct documents and work out what applies.

> [!IMPORTANT]
> E-invoice and e-way-bill applicability thresholds, and some field requirements, change by
> notification. Never assert a current threshold from memory — confirm on the GST portal
> (https://www.gst.gov.in), the e-invoice portal (https://einvoice.gst.gov.in) and the e-way-bill
> portal (https://ewaybillgst.gov.in). The reference holds dated snapshots.

## The tax invoice — get the fields right

A GST tax invoice must carry a defined set of fields. Read
[`references/invoice-fields-and-einvoice.md`](references/invoice-fields-and-einvoice.md) for the
full list; the essentials:

- Supplier name, address and **GSTIN**; a consecutive, unique **invoice number** (within a series)
  and date.
- Recipient name, address and GSTIN (for B2B); **place of supply** for inter-state.
- Description, **HSN/SAC**, quantity, value, discount, taxable value.
- **Tax split** — CGST + SGST for intra-state, IGST for inter-state — with rate and amount.
- Whether tax is on **reverse charge**.
- Signature / digital signature.

Pick the right **document type**:

- **Tax invoice** — taxable supply by a regular registered supplier.
- **Bill of supply** — exempt supplies, or a composition dealer (who can't charge GST the normal
  way). No tax shown.
- **Receipt / refund voucher** — for advances.
- **Credit note / debit note** — to reduce/increase a previously invoiced value (and reported in
  GSTR-1).

Invoice **numbering** must be consecutive and unique per series per financial year — gaps and
duplicates cause return and audit problems.

## E-invoicing (IRN + QR)

Above a turnover threshold, B2B invoices (and exports/credit-debit notes) must be reported to the
**Invoice Registration Portal (IRP)**, which returns a signed **IRN** (Invoice Reference Number)
and a **QR code** that must be printed on the invoice. Key points:

- It applies **per the supplier's aggregate turnover** crossing the notified limit (the limit has
  been lowered in stages — verify the current figure and whether the business is covered).
- It is **not** a different invoice — it's your invoice, registered. Generate it at or before issue.
- A covered supplier's invoice **without a valid IRN/QR is not a valid tax invoice**, and the buyer
  can face ITC trouble.
- There can be a reporting **time limit** for older invoices for large taxpayers — check.

## E-way bill

When **goods** move and the consignment value crosses the threshold, an **e-way bill** is required
(with some exemptions by distance, goods type, and intra-state rules that vary by state). It has
Part A (invoice/consignment details) and Part B (transport/vehicle). Confirm the current threshold
and state rules before concluding one isn't needed.

## How to help, concretely

- **Build an invoice template** — produce a clean format with every mandatory field, the correct
  tax-split layout for intra- vs inter-state, and a space for IRN/QR if the business is e-invoice
  covered.
- **"Does e-invoice / e-way bill apply to us?"** — ask turnover (e-invoice) and the movement/value
  (e-way), then confirm the live threshold on the portal and answer with the check shown.
- **Credit/debit note** — produce the correct document linked to the original invoice and note that
  it must be reported in GSTR-1.
- **A numbering or format query** — explain the consecutive-series rule and fix the scheme.

## Guardrails

- The CGST+SGST vs IGST choice follows **place of supply**, not billing address — get it right on
  the template.
- Mark every threshold "verify on the portal"; they have moved repeatedly.
- A composition dealer issues a **bill of supply**, not a tax invoice — don't put GST on it.
