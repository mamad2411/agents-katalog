---
name: apac-cyber-regs
description: "Covers APAC cyber law (not privacy) for security and GRC teams responsible for an entity, at group HQ or locally, in China, Japan, South Korea, Taiwan, Hong Kong, Australia, Singapore, India, Malaysia, Indonesia, Vietnam, Thailand and the Philippines: whether an entity or site is in scope, which incident clock runs, what telemetry can leave the country, and OT/ICS rules. Use when the user asks about MLPS, China CSL or CAC incident reporting, CERT-In, SOCI or the Cyber Security Act 2024, Singapore CII code, Japan Cyber Response Capability Act, Taiwan/Hong Kong/Malaysia/Vietnam cyber law, or whether an APAC entity or site must comply."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# APAC cyber law for security and GRC teams (practitioner orientation, NOT legal advice)

Written for security and GRC teams responsible for an entity in the region, whether at group HQ or the local entity itself. Where a law's official text is not in English (Chinese, Japanese, Korean, Malay, Vietnamese, Thai, Indonesian), check the original: English versions and summaries are aids, and some are outdated (Korea's official English Network Act text, for one).

There is no APAC NIS2. Each country has its own statute, regulator and clock, and most of them attach to a **designated** population, not to every business. Only China and India bind an ordinary entity directly with an incident clock, and Australia does for ransomware payments. This skill covers cyber law only; privacy and breach law for personal data is in `load_skill privacy-apac`. Status tags: **V** read from official text, **S** secondary source only, **U** unconfirmed (treat as a question for local counsel, not a fact). Checked Nov 2026; re-verify before advising.

## Does it reach this entity? Triage

1. **Applies to every operator or body corporate:** China (network operators: every site) and India (CERT-In Directions: body corporates). Assume in scope.
2. **Applies to every business above a threshold, for one event:** Australia ransomware-payment report (prior-year turnover above AUD 3m, pro-rated for part years).
3. **Applies only if designated:** Japan, Korea, Taiwan, Hong Kong, Singapore, Malaysia, Thailand, Australia SOCI. Designation lists are often not public, and sector wording is broad (Malaysia lists "Trade, industry and economy" among 11 NCII sectors; Singapore and SOCI have no manufacturing class; Thailand's draft adds an "industrial sector"). Ask each local entity for **written confirmation of designation or non-designation** per site, plus whether it is a supplier to a designated operator.
4. **Reached by contract:** designated customers push logging, forensics and supplier-extension demands down (Japan, Korea, Taiwan, Hong Kong; Hogan Lovells for Japan, S). China adds a statutory flow-down: operators must contractually require their security/ops service providers to report incidents to them (CAC Measures Art. 5, V), which hits the entity's local MSSP and integrator contracts.

Output per site: statute, trigger, designating body, evidence of designation, flow-down chain.

## Clocks (the table to keep)

| Jurisdiction           | Who                                                  | Clock                                                                                        | Recipient                                       | Status                                  |
| ---------------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------------------- | ----------------------------------------------- | --------------------------------------- |
| China                  | All network operators; CIIOs; state organs           | Others **4h**; CIIO **1h**; state organs 2h; only "relatively major" and above               | Provincial CAC (CIIO: protection dept + police) | V (CAC Measures, from 1 Nov 2025)       |
| India                  | Body corporates, intermediaries, data centres        | **6h** of noticing                                                                           | CERT-In                                         | V (Directions, in force 27 Jun 2022)    |
| Australia              | Business above AUD 3m turnover                       | Ransomware payment: **72h** of paying or learning of payment                                 | ASD                                             | V (Cyber Security Act s27)              |
| Australia              | SOCI asset operators                                 | **12h** significant impact; **72h** relevant impact (oral, then written record in 84h / 48h) | Commonwealth                                    | V (SOCI s30BC, s30BD)                   |
| Singapore              | CII owners                                           | **2h**; follow-ups 72h and 30 days; other incidents quarterly                                | CSA                                             | S (CSA release; S 678 via search)       |
| Malaysia               | NCII entities                                        | Immediate notice; particulars **6h**; supplement 14 days after the immediate notice          | NACSA                                           | V (P.U.(A) 220, Malay text)             |
| Taiwan                 | Public agencies and specific non-government agencies | **1h** notify; report **72h** (levels 1 to 2) or **36h** (major)                             | MODA / competent authority                      | V via mirror (regulation of 5 Jan 2026) |
| Hong Kong              | Designated CI operators                              | **12h** serious (core function); **48h** other; written follow-up 14 days                    | regulating authority                            | V as the Bill; enacted text U           |
| Japan                  | 258 designated operators, 15 sectors                 | Flash: DDoS asap; other attacks "3 to 5 days" of awareness; detailed **30 days**             | Cabinet Office / NCO                            | V (per-type split U)                    |
| Korea                  | ICT service providers; designated CII                | "Immediately" in the readable (2017) English text; a numeric 24h is **not supported**        | MSIT / KISA                                     | U (law.go.kr text not read)             |
| Vietnam                | System managers                                      | "Immediately" if an incident exceeds own capacity; no hour clock found                       | Competent forces                                | S (Decree 333/2026, partial text)       |
| Thailand               | Designated CII                                       | 24h initial (trigger wording ambiguous)                                                      | Regulator                                       | U                                       |
| Indonesia, Philippines | n/a                                                  | No applicable clock found                                                                    | n/a                                             | S                                       |

Run the shortest clock first: a China incident has a 4h external clock, often before any group function outside China has finished triage.

## Per country

- **China.** Amended CSL in force **1 Jan 2026** (V). Penalties are tiered (Art. 61): operators RMB 10k to 50k, rising to RMB 50k to 500k if they refuse to correct or harm results; RMB 500k to 2m for large data leakage; the **RMB 10m** top tier needs a CII losing its main function. The new AI article's number is U. Reporting thresholds: 1m / 10m / 100m individuals' PI or RMB 5m / 20m / 100m direct loss; CII outage of 10 min (whole) or 30 min (main function) at the lowest tier. Ransomware demand details are reportable; 30-day summary after closure. **MLPS 2.0** (GB/T 22239-2019): level 2 and above filed with local public security within 30 days of grading; level 3 evaluated at least yearly by a PRC-based agency (V, from 2007 MPS Measures; whether a pending regulation supersedes them is U). Product vendors report vulnerabilities to MIIT within 2 days (V, 2021 Provisions).
- **India.** CERT-In Directions bind body corporates; also NTP sync (a global time source is allowed if it does not deviate from NIC/NPL). CEA power-sector rules: see OT below. NCIIPC sector list U. MSME deferral year U.
- **Australia.** SOCI s9 has **no manufacturing class** (nearest: food and grocery, defence industry; V for the Act, but rules-prescribed assets under s9(1)(f) were not checked). The ransomware duty is the one that reaches an ordinary business above the threshold. Smart-device standard (consumer-connectable products manufactured from 4 Mar 2026) matters for manufacturers **exporting** such products to Australia, not for their own OT; whether industrial products are exempt is U. Essential Eight is mandatory only for non-corporate Commonwealth entities. Any "education first" grace on ransomware reporting is not in the legislation (U).
- **Singapore.** Cybersecurity (Amendment) Act 2024 partly in force 31 Oct 2025 (provider-owned CII including overseas-located systems, wider reporting; V). Manufacturing is not a CII sector. The Code for CII (2026), effective 29 Jul 2026, replaced "CCoP 2.0"; CII owners must hold Cyber Trust Mark Advocate (Tier 5) within 24 months of designation (V). Later Act parts (ESCI, major FDI) not found commenced (U).
- **Japan.** Cyber Response Capability Enhancement Act core duties from **1 Oct 2026**: asset notification (existing operators have six months), incident reporting, consultative council. Penalties U. An entity that is not itself designated is reached mainly as a supplier.
- **Korea.** Law No. 21500 (Network Act amendment) in force 1 Oct 2026, level evaluation from 1 Apr 2027 (S). Reported CISO, committee and 3% revenue fines for repeat incidents are U. An ordinary entity is in scope only if designated under the ICI Protection Act or if it is an ICT service provider.
- **Taiwan.** Cyber Security Management Act amendments reportedly effective 1 Dec 2025 (S); fine maximum and which manufacturers are designated are U.
- **Hong Kong.** Cap. 653 in force 1 Jan 2026 (S, L.N. 144 of 2025). Sectors: energy, IT, banking, air/land/maritime transport, healthcare, telecoms and broadcasting, plus "other infrastructure". Audit at least every 24 months, risk assessment at least every 12; fines to HK$5m (all as the Bill). No designations found.
- **Malaysia.** Act 854 in force 26 Aug 2024. Failure to notify: up to RM 500,000 or 10 years. Audit cadence U.
- **Vietnam.** Law 116/2025/QH15 in force 1 Jul 2026 (S); Decree 333/2026 (19 Aug 2026) exists; Decree 53/2022's repeal status U; Law text U.
- **Thailand.** Cybersecurity Act binds designated CII only; current 24h clock and THB 200,000 fine U; no primary Thai text was read.
- **Indonesia / Philippines.** No dedicated cyber statute binds a private entity (Indonesia's PP 71/2019 duties for private electronic system operators aside): Indonesia's RUU KKS is in committee, the Philippines' HB 9605 is at the Senate.

## What can leave the country (SOC, SIEM, MES, historian feeds)

Each rule below states what must stay in country; the practical consequence falls on any cross-border SOC or SIEM.

- **China.** CAC Provisions Art. 3 (22 Mar 2024, V) exempts data generated in international trade, cross-border transport, academic cooperation or **transnational manufacturing and marketing** from assessment, standard contract and certification, if it contains **no personal information or important data**. Production telemetry usually fits; a SIEM feed that carries user accounts or other PI does not (inference, apply the privacy routes in `load_skill privacy-apac`). "Important data" means data notified by the authorities or publicly released as important (Art. 2); the identification standard GB/T 43697-2024 is S. MIIT industrial-sector data rules (Wang An [2022] No. 166) are partly verified; their domestic-storage wording was not read, so do not assume a rule either way.
- **India.** CERT-In requires ICT logs kept for a rolling **180 days within Indian jurisdiction**. SCADA, historian and firewall logs can fall under "ICT systems" wording (a reading, not a CERT-In statement), so a SIEM hosted outside India (for example a group-central one) must keep the India copy.
- **Vietnam.** Decree 333 localisation targets user and user-created data of service providers (24-month minimum storage), not factory OT. Foreign enterprises in listed sectors are required to localise or set up an office only after triggers such as repeated non-compliance.
- **Indonesia.** PP 71/2019: private-scope operators may store abroad if supervisory and law-enforcement access is ensured; public-scope data stays onshore (S; Perpres 82/2022 and BSSN rules U).
- Other countries: no cyber-law localisation rule was found in the sources; that is absence of evidence, so confirm with counsel.

## OT/ICS specifics

- **China:** MIIT Industrial Internet Security Classification and Grading Measures are **final** (Wang An [2024] No. 68, 11 Apr 2024). They cover raw materials, equipment, consumer goods and electronics manufacturing: self-grading, registration on a national platform, local checks within 30 working days (S, mirror of the MIIT notice). MIIT's Jan 2024 ICS guidelines and any MLPS ICS extension set are U.
- **Singapore:** CII Code (2026) section 10 covers OT CII: limits on connection to enterprise networks, monitoring of data flows into them, separate authentication and credentials, Safety Instrumented System connection limits, firmware and program-code integrity (V). Existing owners get a per-section transition date (not extracted).
- **India:** CEA (Cyber Security in Power Sector) Regulations 2026, dated 31 Jul 2026, are **final** (not a draft): generators, captive plants and storage at **50 MW or more**, CSIRT-Power as nodal body, drills at least every six months (S from search excerpts; the Gazette was not read). Effective 1 Apr 2027, a 6h CSIRT-Power report and a CISO duty are U. Any plant with large captive generation should check this.
- **Japan:** METI Cyber/Physical Security Guidelines for Factory Systems (main text v1.0, 16 Nov 2022; supplements Apr 2024 and Apr 2025) are voluntary but the de facto OT audit benchmark; a "Ver1.1" is U.
- **Hong Kong, Taiwan, Korea:** designated-CI regimes; OT content was not verified.

## Mapping to ISO 27001 / IEC 62443 / NIST CSF

Each national act stands on its own terms, and mappings to frameworks are reuse aids that work in both directions. No jurisdiction found mandates ISO 27001, IEC 62443 or NIST CSF as such for a private entity, and none accepts a certificate in place of the national act. China's MLPS filing and testing are separate legal acts. Singapore's Code mentions no IEC 62443 (keyword search, not exhaustive) and requires Cyber Trust Mark for CII owners. Japan's METI guidelines' NIST CSF and IEC 62443 basis is U.

Inference, not sourced: MLPS level 3 controls roughly correspond to ISO 27001 Annex A plus IEC 62443 zone and conduit ideas, so evidence can be reused in both directions (an entity built on MLPS can feed an ISO 27001 programme, and a group control set can feed MLPS), but treat each national act as its own audit. Use `load_skill choosing-a-framework` for the internal baseline and `load_skill control-mapping` for crosswalks.

## Watch list (dated)

- Japan: asset notification for existing operators by about 1 Apr 2027 (arithmetic from the 1 Oct 2026 start); communications-information use from autumn 2027.
- Korea: information-security-level evaluation 1 Apr 2027.
- India: CEA power-sector mandatory provisions (1 Apr 2027 per PwC, U).
- Thailand: draft amendment adding an "industrial sector" CII category (consultation closed 15 Jul 2026; the item most likely to pull manufacturers in).
- Australia: SOCI Tranche 2 (consultation closed 31 Jul 2026); Enhanced CIRMP Rules (reported as F2026L00701, 10 Jun 2026) are U: no primary source reached.
- Indonesia RUU KKS enactment; Philippines HB 9605 in the Senate; Vietnam remaining decrees; Hong Kong first designations and Code of Practice; Taiwan designations of manufacturers.

## Working rules

- Scope per site in writing before any group policy cascade: designation status, local MSSP contract flow-down, log location.
- Do not cite a U item to a board or auditor as law; carry the flag into the register.
- Local-language text governs; use local counsel for filings and keep templates ready for the 1h to 6h clocks (`load_skill incident-response-leadership`).
- A cross-border or central SIEM design needs three checks per country: cyber clock, log or data location, and personal-data transfer route.

## Pairs with

`load_skill privacy-apac`, `load_skill breach-notification-matrix`, `load_skill ot-compliance`, `load_skill choosing-a-framework`, `load_skill third-party-risk`, `load_skill ot-ics`, `load_skill data-security`.
