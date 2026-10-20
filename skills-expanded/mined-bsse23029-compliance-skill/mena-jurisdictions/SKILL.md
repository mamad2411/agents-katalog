---
name: mena-jurisdictions
description: Per-country routing for the wider MENA/GCC region — UAE (federal, DIFC, ADGM), Oman, Qatar, Bahrain, Kuwait, Egypt, Jordan — covering privacy law and e-invoicing status for each. Use when a deployment sits outside Saudi Arabia but inside the region, or when assessing regional expansion.
---

# MENA jurisdictions

**"MENA compliance" does not exist.** It is a market grouping, not a regulator. Every country here
has its own authority, its own law, its own timetable. This skill routes to the right one; it never
applies a regional average.

Saudi Arabia is handled by the dedicated `ksa-*` skills and is not repeated here.

## Routing questions

Ask before answering anything: where is the property, where is the operating entity incorporated
(especially **DIFC/ADGM vs onshore UAE** — different laws entirely), where is the data hosted, and
who is the invoicing counterparty.

## United Arab Emirates

**Privacy — `AE-PDPL`.** Federal Decree-Law No. 45 of 2021. Confidence in the registry is
deliberately **low**: reporting conflicts on whether the Article 28 Executive Regulations have been
issued. One line of 2026 commentary says a Cabinet decision issued them with compliance required
from **1 January 2027**; another says they could not be located on official UAE sources. **Do not
assert their content.** Verify with the UAE Data Office before making a requirement claim.

**Free zones — `AE-DIFC-DP`.** A DIFC-incorporated entity follows DIFC Data Protection Law No. 5 of
2020, not the federal PDPL. ADGM has its own Data Protection Regulations 2021. This is a common and
expensive mistake: check incorporation, not just the emirate.

**E-invoicing — `AE-EINV`.** Live and dated:

| Milestone | Date |
|---|---|
| MoF pilot with Accredited Service Providers | 1 July 2026 (running now) |
| Large businesses must appoint an ASP | 30 October 2026 |
| Large business mandatory go-live | 1 January 2027 |
| SMEs | 1 July 2027 |
| Government transactions | 1 October 2027 |

Model: decentralised clearance and exchange (DCTCE) on the **Peppol 5-corner** framework; invoices
as structured XML to the **PINT AE** schema, exchanged only through a ministry-accredited ASP.
Architecturally this is *not* ZATCA — Saudi is direct clearance to the tax authority; UAE routes
through an accredited provider network. Do not reuse the ZATCA integration design and assume it fits.

**Also**: UAE VAT invoice content rules.

## Oman — `OM-PDPL`
Personal Data Protection Law with Executive Regulations reaching **full implementation on
5 February 2026**. Treat as live and enforced.

## Qatar — `QA-PDPPL`
Law No. 13 of 2016 on Personal Data Privacy Protection, in force. The first GCC general privacy law.

## Bahrain — `BH-PDPL`
Law No. 30 of 2018, in force, with a dedicated Personal Data Protection Authority.

## Kuwait — `KW-CITRA-DPPR`
**No general personal data protection statute.** CITRA's Data Privacy Protection Regulation is
sector-scoped (telecom service providers). A general law is anticipated — re-check before advising.
Do not claim a Kuwaiti hotel is subject to a general privacy law.

## Egypt — `EG-PDPL`
Law No. 151 of 2020, in force. Confirm whether the executive regulations have been issued before
relying on procedural detail such as registration and licensing mechanics.

## Jordan — `JO-PDPL`
Personal Data Protection Law No. 24 of 2023.

## Cross-cutting guidance

- **Localisation and transfer rules differ per country.** A single regional Azure region does not
  satisfy every jurisdiction at once. Do the transfer analysis per tenant.
- **E-invoicing is diverging, not converging.** Saudi (ZATCA clearance), UAE (Peppol/ASP), Pakistan
  (licensed integrator) are three different architectures. Build the invoicing layer with a
  pluggable fiscalisation adapter or accept three forks.
- **Confidence is low on several entries here.** Every registry entry in this region except the UAE
  e-invoicing timeline carries `confidence: low` or `medium`. Re-verify before a client-facing
  statement, and update the registry when you do.
