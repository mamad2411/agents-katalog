---
name: ksa-pdpl
description: Saudi Personal Data Protection Law (PDPL), its Implementing Regulations and the Transfer Regulations — the primary privacy regime for this product. Use for any question about guest personal data in a Saudi deployment: lawful basis, consent, minimisation, retention, data-subject rights, breach notification, DPO, records of processing, or moving data outside the Kingdom.
---

# Saudi PDPL

Registry: `SA-PDPL-LAW`, `SA-PDPL-IR`, `SA-PDPL-TRANSFER`, `SA-PDPL-TRA-GUIDE`.
Regulator: **SDAIA**. Status: in force; the enforcement grace period ended **14 September 2024** and
SDAIA is enforcing (48 cumulative enforcement decisions reported by early 2026).

Verify before citing procedural detail: SDAIA ran a third public consultation on amendments to the
Implementing Regulations (Apr–May 2025) and the amended text had not been published as of mid-2026.
`sdaia.gov.sa` is unreachable from automated tooling here — use the PDF in
`compliance/sources/pdfs/ksa/`.

This is the **default privacy regime** for the product, not GDPR. Do not audit a Saudi deployment
against GDPR and assume PDPL is covered — the obligations overlap but the transfer regime,
registration expectations and consent mechanics differ.

## Control checklist

| ID | Requirement | Surfaces |
|---|---|---|
| PDPL-01 | A lawful basis exists and is recorded for every processing purpose — consent, contract performance, legal obligation, legitimate interests (narrower than GDPR's) | backend |
| PDPL-02 | Consent is specific, informed, freely given and withdrawable; withdrawal is as easy as giving it | frontend, backend |
| PDPL-03 | Privacy notice discloses purpose, categories, recipients, transfers, retention and rights — in the languages served, Arabic included | frontend |
| PDPL-04 | Data minimisation: each field collected is necessary for a stated purpose. Challenge every identity-document field | backend |
| PDPL-05 | Purpose limitation: guest data collected for a stay is not reused for marketing or AI training without a basis | backend |
| PDPL-06 | Records of processing activities maintained and current | backend (documentation) |
| PDPL-07 | Data-subject rights implemented: access, correction, deletion, and the right to obtain a copy in a readable format | frontend, backend |
| PDPL-08 | Retention limited to purpose; destruction, anonymisation or pseudonymisation applied when the purpose ends — reconciled against tax retention minimums | backend |
| PDPL-09 | Personal-data breach handling: detection, assessment, notification to SDAIA and to affected individuals where required, with a documented timeline | backend, cicd |
| PDPL-10 | Processor contracts in place with every third party receiving personal data (payment gateways, SMS/WhatsApp, email, cloud, AI) | backend |
| PDPL-11 | Security appropriate to the sensitivity — identity documents and their scans are the top tier here | backend, cicd |
| PDPL-12 | Data protection officer appointed where required, and contactable | organisational |
| PDPL-13 | Transfers outside the Kingdom rely on a permitted route, with a transfer risk assessment where required and SDAIA-approved SCCs or Binding Common Rules | backend, cicd |
| PDPL-14 | Disclosures required by law (Shomoos, NTMP) are recorded as legal-obligation processing, not as consent | backend |
| PDPL-15 | Privacy by design in new modules; assess before launch, not after | all |

## Transfer analysis — the part this architecture keeps hitting

`SA-PDPL-TRANSFER` plus `SA-PDPL-TRA-GUIDE` (Feb 2025). Every egress of personal data out of Saudi
Arabia needs a route and, for continuous or large-scale transfers of sensitive data, a documented
risk assessment. SDAIA can halt transfers touching national security or vital interests.

Enumerate concretely for this codebase, then grade each:

- Azure Container Apps region and the databases behind it
- S3 bucket region (`S3_REGION`)
- OpenAI API calls (`Services/Integrations/AI/OpenAi/`) — US processing of whatever is in the prompt
- Firebase / FCM push
- SMS and WhatsApp providers
- Email (`nodemailer` / SMTP host)
- `geoip-lite` (local, no egress — worth noting as the counter-example)
- Payment gateways
- Backups, log aggregation, error tracking, analytics

A Saudi Azure region was announced for 2026; confirm availability before telling a tenant the data
stays in-Kingdom. See also `SA-CST-CCRF` in `ksa-nca-controls` for the cloud classification angle.

## Interaction with other regimes

- **Shomoos / NTMP** (`ksa-hospitality-reporting`) — legal obligation, and the lawful basis for
  transmitting guest identity data to the Ministry of Interior. It does not license using that data
  for anything else.
- **ZATCA / VAT** — tax retention sets a floor that overrides deletion requests for invoice data.
  Resolve field by field, not by refusing the request wholesale.
- **GDPR** — applies additionally where EU guests are served; it does not replace PDPL.

## Output

Findings cite `SA-PDPL-*` ids and the control id above, per surface, with file evidence.
