---
name: pakistan-compliance
description: Pakistan-specific obligations — FBR digital invoicing with licensed integrators and the 72-hour invoice amendment window, PECA 2016 as the operative data framework, and the still-unenacted Personal Data Protection Bill. Use for any deployment, entity or invoicing counterparty in Pakistan.
---

# Pakistan

Registry: `PK-FBR-DIGITAL-INVOICING`, `PK-PECA`, `PK-PDPB`. Secondary jurisdiction for this product
after Saudi Arabia and the wider MENA region — but the `cnic` column in the schema says it is real.

## FBR digital invoicing — `PK-FBR-DIGITAL-INVOICING`

This is the binding, immediate obligation. Status: **in force for all sales-tax-registered
persons**; the phased rollout under SRO 1852(I)/2025 brought the final group in on
**31 December 2025**. The framework came in through SRO 1413(I)/2025, clarified by **Sales Tax
General Order No. 01 of 2026**.

| ID | Requirement | Notes |
|---|---|---|
| FBR-01 | Issue digital sales tax invoices from an integrated system | Not a PDF; a reported electronic invoice |
| FBR-02 | Real-time reporting to FBR's computerised system **through an FBR-licensed integrator** | You cannot integrate directly; pick from the licensed list |
| FBR-03 | Multiple licensed integrators are permitted per taxpayer | Per STGO 01/2026 — allows architectural flexibility and failover |
| FBR-04 | Invoice cancel/delete/edit only **inside the FBR system** and only within **72 hours** of issuance | Hard constraint |
| FBR-05 | Changes after 72 hours require prior approval from the Commissioner Inland Revenue | Design a correction workflow, not an edit button |
| FBR-06 | Invoice carries the FBR-assigned identifiers (IRN and QR) as required | Verify current field list against FBR docs |
| FBR-07 | Retention and reconciliation of reported invoices against the FBR record | |

**Design consequence.** The 72-hour rule plus ZATCA's immutability rule point the same way: an
issued invoice is append-only, and corrections are documents in their own right. Build the folio
model so that "issued" is a one-way door with a credit/debit-note path out of it, and the fiscal
integration is a pluggable adapter — Pakistan (licensed integrator), Saudi (direct clearance) and
UAE (Peppol ASP) are three different shapes.

**Verify:** the full SRO chain and the current licensed-integrator list on `fbr.gov.pk`. Only
1413(I)/2025, 1852(I)/2025 and STGO 01/2026 are confirmed in the registry.

## Data protection — `PK-PECA`, `PK-PDPB`

**There is no enacted general data protection law in Pakistan.** As of 2026 no version of the
Personal Data Protection Bill has been passed. The operative framework is **PECA 2016 (amended
January 2025)** plus sector rules — offences around unauthorised access, data interference and
misuse of identity information, rather than a controller/processor regime.

Two rules for how to handle this:

1. **Never present the PDP Bill as binding.** A revised MoITT draft reportedly adds caste and
   ethnicity to sensitive data, mandatory age verification and parental consent for children's
   data, and consent withdrawal as an ongoing right — but it is unpublished and not before
   Parliament. It informs design; it does not produce findings. Registry status: `draft-not-law`.
2. **Do not treat the absence of a law as an absence of obligation.** PECA still applies, sector
   regulators (SBP for payments, PTA for telecom-adjacent) still apply, contractual commitments to
   hotel groups still apply, and the same guest data is often simultaneously subject to Saudi PDPL
   or GDPR because of where the guest or the group is based.

Practical position for this product: **run the Saudi PDPL control set as the baseline everywhere.**
It is the strictest regime we already have to satisfy, it is close enough to GDPR to carry most of
that weight, and it means a future Pakistani law lands on a system that is already compliant rather
than triggering a migration.

## Grid guidance

Backend rows for FBR; `n/a` on frontend and CI/CD except where an invoice is rendered or exported.
Mark PDP Bill rows as `n/a — draft, not law` with the registry id, so the decision is recorded once.
