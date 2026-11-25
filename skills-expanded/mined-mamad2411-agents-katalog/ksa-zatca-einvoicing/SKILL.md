---
name: ksa-zatca-einvoicing
description: Saudi ZATCA e-invoicing (Fatoora) Phase 1 and Phase 2, the XML/security technical specifications, wave scoping and VAT invoice rules. Use for any question about invoices, folios, credit notes, refunds, tax fields or invoice immutability in a Saudi deployment.
---

# ZATCA e-invoicing (Fatoora)

Registry: `SA-ZATCA-EINV-REG`, `SA-ZATCA-SPEC`, `SA-ZATCA-SECURITY`, `SA-VAT`.
Regulator: **ZATCA**. Backend-only surface — the frontend and pipeline rows are `n/a` with reason.

## Where the mandate stands

- **Phase 1 (Generation)** — since 4 Dec 2021. Structured electronic invoices, QR on simplified
  invoices, no more handwritten or free-form PDF invoices.
- **Phase 2 (Integration)** — since 1 Jan 2023, rolled out in waves by VAT-taxable revenue. Requires
  connecting the invoicing system to Fatoora: signed XML, UUID, cryptographic stamp, hash chaining,
  QR, and clearance (standard invoices) or reporting (simplified invoices) via API.
- **Wave 23** — deadline 31 Mar 2026, revenue > SAR 750,000 in 2022/2023/2024.
- **Wave 24** — announced 26 Sep 2025, deadline 30 Jun 2026, revenue > **SAR 375,000** — the lowest
  threshold so far, which sweeps in small properties.

ZATCA gives roughly six months' notice per wave, so **Wave 25+ may already be announced**. Never
tell a tenant they are out of scope without re-checking the current wave list. At the SAR 375,000
threshold, assume in-scope unless proven otherwise.

## What the code must actually do

| ID | Requirement | Notes |
|---|---|---|
| ZATCA-01 | Generate invoices as XML conforming to the Electronic Invoice XML Implementation Standard | `SA-ZATCA-SPEC` |
| ZATCA-02 | Populate every mandatory field per the Electronic Invoice Data Dictionary — seller VAT number, buyer details where required, line items, tax categories, totals | `SA-ZATCA-SPEC` |
| ZATCA-03 | Distinguish **standard** (B2B/B2G, cleared before issuance) from **simplified** (B2C, reported within 24 hours) — a hotel issues both | `SA-ZATCA-EINV-REG` |
| ZATCA-04 | Cryptographic stamp, invoice UUID, previous-invoice hash (chaining), and counter | `SA-ZATCA-SECURITY` |
| ZATCA-05 | QR code with the required TLV fields | `SA-ZATCA-SECURITY` |
| ZATCA-06 | Onboarding/CSID lifecycle: certificate request, renewal, and secure storage of the private key | `SA-ZATCA-SECURITY` |
| ZATCA-07 | Tamper-resistance — no deletion or silent edit of an issued invoice; corrections via credit/debit note only | `SA-ZATCA-EINV-REG` |
| ZATCA-08 | Sequential, gapless numbering with no user-facing reset | `SA-ZATCA-EINV-REG` |
| ZATCA-09 | Archival of invoices for the statutory retention period, in the required form | `SA-VAT` |
| ZATCA-10 | Handle clearance/reporting failures without losing the invoice or blocking checkout — queue, retry, reconcile | operational |
| ZATCA-11 | Arabic language requirements on the invoice | `SA-ZATCA-SPEC` |
| ZATCA-12 | Correct VAT treatment of hospitality specifics: deposits, no-shows, cancellation fees, service charges, municipality fees, package splits, city ledger | `SA-VAT` |

## Design consequences for the PMS

The hard one is **ZATCA-07 vs how folios normally work**. Front-desk staff expect to edit a folio
until checkout. Once an invoice is issued and cleared, it is immutable — corrections are credit or
debit notes. The boundary between "open folio" and "issued invoice" must be explicit in the data
model, not implied by a status flag that some code path can flip back.

Second: **key material**. The CSID private key used for the cryptographic stamp is a production
secret per property. In a multi-tenant deployment that means per-tenant key isolation, not one
shared key — cross-reference `backend-compliance` B-14 and `ksa-nca-controls` NCA-05.

Third: **retention beats deletion**. A PDPL erasure request cannot delete a cleared invoice.
Resolve at field level: what must persist for tax, what can be minimised around it.

## Verification

The ZATCA developer pages do not display document version numbers. When the specification PDFs are
downloaded into `compliance/sources/pdfs/ksa/`, record the version from the cover page in the
registry entry. Re-check the wave list and the developer portal quarterly at minimum.
