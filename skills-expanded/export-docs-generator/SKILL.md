---
name: export-docs-generator
description: Generates international export shipping paperwork — commercial invoices, packing lists, and draft certificates of origin — correctly formatted for specific exporting and destination jurisdictions (India, UK, EU, UAE/GCC, US, and Global Generic). Use whenever the user asks to create, draft, or fill an export invoice, packing list, proforma invoice, or certificate of origin, or mentions shipping goods internationally and needs country-accurate identifiers (IEC, GSTIN, EORI, VAT, TRN, HSN/TARIC) and Incoterms 2020 rules.
license: MIT
metadata:
  author: Open Source Community
  version: "1.2.0"
---

# Export Documentation Generator — Ground-Truth Trade Engine

## Purpose & Scope
Generate legally structured, country-accurate export shipping paperwork (commercial invoices, packing lists, and draft certificates of origin) across international jurisdictions without US-centric defaults.

> [!CAUTION]
> **CUSTOMS CLEARANCE WARNING**: False or inaccurate particulars on customs invoices can result in cargo seizure, heavy civil penalties, and blacklisting of exporter identification numbers (IEC/EORI/TRN). All documents generated are drafts and must be reviewed against verified commercial contracts and shipping bills by a licensed Customs Broker (CHA) or Freight Forwarder.

---

## 🛑 ZERO ASSUMPTIONS & GROUND TRUTH PROTOCOL

To eliminate hallucinations and prevent dangerous documentation discrepancies:

1. **NEVER Guess Incoterms® 2020**: Never assume an Incoterm (e.g. FOB vs CIF vs DDP). If unspecified by the user, ask for clarification or explain the cost/risk implications of common options.
2. **NEVER Assume Currency Exchange Rates**: Invoices involving foreign exchange conversions must state that customs valuation relies on the **notified official Customs Exchange Rate** on the date of the export declaration, not commercial bank or market rates.
3. **NEVER Invent or Guarantee HS/HSN/TARIC Codes**: Provide structured guidance for classification chapters, but explicitly flag that the exact 6, 8, or 10-digit code must be confirmed against the origin and destination national tariff schedules.
4. **NEVER Assume Wood Packaging Compliance**: Never mark packaging as ISPM-15 compliant unless verified by the user, as uncertified wood packaging will trigger container quarantine or re-export at destination.
5. **NEVER Assume Destination Import Duty Exemptions**: Preferential trade agreements (FTAs, CEPAs) require a formally stamped Certificate of Origin issued by an authorized governmental body (e.g., Chamber of Commerce / DGFT), not merely an in-chat draft.

---

## Step 1: Gather Shipment Parameters (Confirmed Ground Truth)
Before generating any document, determine:
1. **Origin Country** (Determines exporter tax ID format, origin customs endorsement, and currency).
2. **Destination Country** (Determines consignee details, duty-preferential rules, and Certificate of Origin needs).
3. **Line Items**: Description, Harmonized System (HS / HSN / TARIC) code, Quantity, Unit of Measurement (UOM), Unit Price, Total Currency Value.
4. **Incoterms® 2020 Rule**: (e.g., FOB, CIF, CFR, EXW, DAP, DDP).
5. **Logistics Details**: Port of Loading, Port of Discharge, Mode of Transport (Ocean/Air/Multimodal), Vessel/Flight info, Container/Seal numbers.

---

## Step 2: Dynamic Routing to Regional Reference

Load the specific reference module based on the exporting country:

- **[references/india-export-docs.md](file:///skills/export-docs-generator/references/india-export-docs.md)**: Exporter IEC, GSTIN, State Code, Port Code (6-character), SCOMET checks, ISPM-15, and LUT/IGST statutory endorsements.
- **[references/uk-eu-export-docs.md](file:///skills/export-docs-generator/references/uk-eu-export-docs.md)**: GB/EU EORI numbers, VAT registration, 8/10-digit TARIC commodity codes, and origin declaration statements (EU-UK TCA / GSP).
- **[references/uae-gcc-export-docs.md](file:///skills/export-docs-generator/references/uae-gcc-export-docs.md)**: UAE TRN (Tax Registration Number), Dubai Customs Mirsal 2 / Bayan declaration requirements, bilingual English/Arabic layout guidelines.
- **[references/generic-export-docs.md](file:///skills/export-docs-generator/references/generic-export-docs.md)**: Universal country-agnostic commercial invoice and packing list templates compliant with WCO (World Customs Organization) standards.

---

## Step 3: Required Core Output Specifications

### 1. Commercial Invoice
- **Header**: Exporter & Consignee complete legal names, addresses, tax IDs (IEC/EORI/TRN/EIN).
- **Metadata**: Invoice number, Date, Buyer's PO/Reference, Country of Origin, Final Destination.
- **Delivery & Terms**: Incoterm 2020 + Named Port/Place (e.g., `CIF Rotterdam Port, Incoterms® 2020`), Payment Terms (e.g., `LC at sight`, `Net 30 Days`).
- **Tabular Breakdown**: Item No, Description, HS/HSN Code, Qty, Unit, Unit Price, Total Amount.
- **Cost Summary**: FOB value + Freight + Insurance = Total CIF/CIP Invoice Value.
- **Statutory Endorsements & Signature Block**: Country-specific declarations + Authorized Signatory.

### 2. Packing List
- **Header & Traceability**: Linked to Commercial Invoice No & Date.
- **Package-by-Package Breakdown**: Box/Pallet No, Marks & Numbers, Package Dimensions ($L \times W \times H$ in cm/in), Net Weight (kg), Gross Weight (kg), Volume (CBM).
- **Summary Totals**: Total Packages, Total Net Weight, Total Gross Weight, Total Cubic Volume (CBM).
