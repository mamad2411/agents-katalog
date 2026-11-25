---
name: ksa-hospitality-reporting
description: Saudi hospitality-sector obligations that no generic compliance framework covers — Shomoos guest registration with the Ministry of Interior and NTMP occupancy/reservation reporting to the Ministry of Tourism. Use for check-in, guest identity capture, occupancy and property-licensing questions in a Saudi deployment.
---

# Saudi hospitality reporting — Shomoos and NTMP

Registry: `SA-MOI-SHOMOOS`, `SA-MT-NTMP`. Backend surface.

These two are the obligations that separate a PMS that can be sold in Saudi Arabia from one that
cannot. They are also the reason the product holds passport data at all — which makes them central
to the PDPL analysis, not a side quest.

## Shomoos — Ministry of Interior

Established by Royal Decree in 2014. Accommodation facilities must transmit guest information to
the **National Information Center** at the Ministry of Interior, automatically and in real time at
check-in, through the Shomoos system on the National Information Network.

| ID | Requirement | Notes |
|---|---|---|
| SHM-01 | Guest identity captured at check-in in the form Shomoos requires (national ID / Iqama / passport, per guest type) | Drives the `passport_*` and identity fields in the schema |
| SHM-02 | Registration transmitted at check-in, in real time — not batched overnight | |
| SHM-03 | Check-out / departure recorded where the system requires it | |
| SHM-04 | Accompanying guests and children handled per the rules, not just the booker | |
| SHM-05 | Failed transmissions detected, queued, retried and alerted — a silent failure is a licensing risk for the property | |
| SHM-06 | Credentials per property, stored as secrets, never shared across tenants | Cross-ref `backend-compliance` B-14 |
| SHM-07 | The transmission is logged as a disclosure in the processing records | Cross-ref `ksa-pdpl` PDPL-14 |

**The integration specification is not published openly.** It is issued to licensed operators
through MOI/NIC onboarding. Obtain it via the hotel's onboarding and file the PDF in
`compliance/sources/pdfs/ksa/`. Do not implement against a third-party blog's description of the
API, and do not let a vendor summary become the citation.

## NTMP — Ministry of Tourism

The National Tourism Monitoring Platform, launched 2019 (then SCTH). Accommodation facilities must
share **financial, occupancy and reservation information**; the platform monitors accommodation
performance and tourism movement.

| ID | Requirement | Notes |
|---|---|---|
| NTMP-01 | Reservation, occupancy and financial data reported per the platform's schema and cadence | |
| NTMP-02 | Per-property API credentials — API key plus username and password issued by the Ministry — held as secrets | |
| NTMP-03 | Reporting failures surfaced and reconciled | |
| NTMP-04 | Data minimised to what the platform requires | Cross-ref `ksa-pdpl` PDPL-04 |
| NTMP-05 | Reporting recorded as a disclosure in the processing records | |

Official e-service: `SA-MT-NTMP` registry entry.

## Privacy framing — get this right

Both are **legal obligations** under PDPL, which is the lawful basis for the disclosure. Two
consequences people get wrong:

1. You do **not** need guest consent to transmit to Shomoos — and asking for it implies a choice
   that does not exist. Disclose it in the privacy notice instead.
2. The legal obligation covers *that* transmission only. It is not a licence to retain passport
   scans indefinitely, to use identity data for marketing, or to expose it to every staff role.
   Retention and access control still apply in full.

## Grid guidance

These are backend rows. Frontend gets one related row — capture UX and the privacy notice text
that discloses the disclosure. CI/CD gets `n/a`.

A property operating in Saudi Arabia without working Shomoos and NTMP integration has a licensing
problem, not a compliance-nice-to-have. Rank these rows at the top of the backend grid alongside
identity-document protection.
