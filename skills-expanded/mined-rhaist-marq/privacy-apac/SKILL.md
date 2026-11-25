---
name: privacy-apac
description: "Covers APAC privacy and cyber-reporting law for a security team: China (PIPL/DSL/amended CSL, incident-reporting measures, cross-border routes and exemptions), India (DPDP Act + Rules phase-in, CERT-In), Singapore PDPA, Japan APPI and its 2026 amendment, Korea PIPA 2026 amendment, and Australia (Privacy Act reforms, NDB, SOCI, APRA CPS 234/230), with every breach clock in one table. Use when the user operates in or transfers data to APAC, or asks about PIPL, DPDP, CERT-In, PDPA, APPI, PIPA or Australian breach reporting."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# APAC privacy & breach reporting (practitioner orientation, NOT legal advice)

There is no APAC GDPR. Each country has its own law, regulator, transfer rule and (most importantly for incident response) its **own clock**, several of them **far shorter than GDPR's 72h** (China 1 to 4h, India CERT-In 6h, Singapore CII 2h, MAS 1h). A GDPR programme does not cover these; map per country. Cyber-only law (MLPS, CERT-In scope, SOCI, OT rules, data-leaving-the-country, other APAC countries): `load_skill apac-cyber-regs`. Comparison baselines: `load_skill privacy-eu`, `load_skill privacy-us`. Dates checked Nov 2026; re-verify before advising.

## Breach / incident clocks (the table to keep)

| Country   | Trigger                                                           | To whom                                                             | Clock                                                                              |
| --------- | ----------------------------------------------------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| China     | Cyber incident "relatively major" (较大) or worse                 | CII: protection dept + police; others: provincial CAC               | **CIIO 1h; other operators 4h**; state organs 2h (CAC measures, from 1 Nov 2025)   |
| China     | Personal-information leak (PIPL Art. 57)                          | PI regulator + individuals                                          | **Immediately** remediate and notify; no fixed hours                               |
| India     | Cyber incident (CERT-In Directions 2022)                          | CERT-In                                                             | **6 hours** of noticing                                                            |
| India     | Personal-data breach (DPDP Rule 7, from 13 May 2027)              | Data Principals + DP Board                                          | Without delay; **detailed report to Board ≤72h**                                   |
| Singapore | Notifiable breach (significant harm or ≥500 people)               | PDPC (+ individuals)                                                | Assess ≤30 days; **PDPC ≤3 calendar days** after assessing notifiable              |
| Singapore | Prescribed CII incident (Cybersecurity Act)                       | CSA                                                                 | **2 hours**; supplementary 72h, final 30 days (third-party CII regs 2026)          |
| Singapore | MAS-regulated FI relevant incident                                | MAS                                                                 | **1 hour**; root-cause report 14 days                                              |
| Japan     | Leak of sensitive / financial-harm / malicious / >1,000           | PPC + individuals                                                   | Preliminary **"promptly" (~3 to 5 days)**; final **30 days (60 if malicious act)** |
| Korea     | Leak (or, since 11 Sep 2026, _possible_ leak)                     | Data subjects; PIPC/KISA if ≥1,000, sensitive/unique ID, or hacking | **72h** (Enforcement Decree; verify post-2026 decree)                              |
| Australia | Eligible data breach (NDB)                                        | OAIC + individuals                                                  | Assess ≤30 days; notify **as soon as practicable** (draft bill → **72h**)          |
| Australia | Critical-infrastructure cyber incident (SOCI)                     | ASD / ACSC                                                          | **12h** significant impact; **72h** relevant impact                                |
| Australia | Ransomware/extortion **payment** (Cyber Security Act 2024)        | ASD                                                                 | **72h** of paying                                                                  |
| Australia | APRA-regulated material info-sec incident (CPS 234)               | APRA                                                                | **72h**; material control weakness 10 business days                                |
| Australia | CPS 230 material op-risk incident / critical op outside tolerance | APRA                                                                | **72h** / **24h**                                                                  |

## China: PIPL, DSL, CSL

- **PIPL** (1 Nov 2021) personal information; **DSL** (1 Sep 2021) data classification, "important data", core data; **CSL** (2017) network security + MLPS 2.0 grading. **CSL amendment in force 1 Jan 2026**: tiered fines (Art. 61: **RMB 50k to 500k** for aggravated network-operator breaches, up to **RMB 10m** only when a CII loses its main function; individuals up to RMB 1m at that tier), explicit extraterritorial reach over foreign actors harming China's cybersecurity, AI-governance hooks. Plus Network Data Security Management Regulations (1 Jan 2025) and PI compliance-audit measures (2025).
- **Incident reporting**: CAC _National Cybersecurity Incident Reporting Measures_, effective **1 Nov 2025**: CIIOs **1h**, other network operators **4h** to the provincial CAC, for incidents graded "relatively major" and above; late, omitted or concealed reports are aggravating. verify: https://www.cac.gov.cn/2025-09/15/c_1759583017717009.htm
- **Cross-border transfer: pick the route by volume** (Provisions on Promoting and Regulating Cross-Border Data Flows, Mar 2024; counted cumulatively from 1 Jan of the year, non-CIIO):
  - **Exempt:** <100k individuals' non-sensitive PI; transfers necessary for a contract with the individual (e-commerce, payments, travel), cross-border HR under lawful policies, emergencies; data not containing PI/important data; FTZ data outside a published negative list.
  - **Standard Contract filing _or_ certification:** 100k to 1M non-sensitive, or <10k sensitive. **PI-protection certification measures in force 1 Jan 2026** make certification a real alternative to SCC filing.
  - **CAC security assessment:** >1M non-sensitive, ≥10k sensitive, any CIIO export, or any **important data** (data the authorities have notified or publicly released as important; Art. 2). Approval valid 3 years.
  - Every route still needs **separate consent** (where consent is the basis) and a **PI-protection impact assessment**; exemptions waive the filing, not PIPL itself.
- Pitfalls: remote access from abroad _is_ export; a global SIEM/EDR pulling China telemetry is a transfer; local-language filings; police/CAC data requests have no GDPR-style challenge path. Residency design: `load_skill data-security`.

## India: DPDP Act 2023 + DPDP Rules 2025

- Rules notified **13 Nov 2025** (gazetted 14 Nov). Phase-in: Data Protection Board + definitions **immediately**; **Consent Manager registration from 13 Nov 2026**; **substantive duties from 13 May 2027**: notice/consent, **reasonable security safeguards (Rule 6:** encryption/masking, access control, logging retained ≥1 year, backups, processor contracts), breach notice (Rule 7), retention/erasure, children, **Significant Data Fiduciary** DPIA + annual audit, rights, transfers. MeitY floated compressing 18 months to 12 (Jan to Mar 2026); **not gazetted as of Nov 2026**; verify before planning to May 2027: https://www.meity.gov.in/
- Penalties up to **₹250 crore** (security-safeguard failure), **₹200 crore** (breach-notification failure).
- **Transfers:** blocklist model: allowed unless the government restricts a country; SDFs can be told to localise specified data. **Sector rules override** (RBI payment-data localisation, SEBI, IRDAI).
- **CERT-In Directions (Apr 2022)** are already live and are the binding first clock: **6h** incident report, **180 days of logs kept in India**, NTP sync. Don't wait for DPDP.

## Singapore: PDPA

- Mandatory breach notification since Feb 2021 (thresholds above). Fines up to **10% of Singapore turnover** (if >S$10m) or **S$1m**. Protection obligation = reasonable security arrangements; PDPC decisions are a good bar for "reasonable". verify: https://www.pdpc.gov.sg/
- **Cybersecurity (Amendment) Act 2024** key provisions in force **31 Oct 2025**: CII reporting widened (supply-chain and APT incidents, non-interconnected systems), 2h clock; regs for third-party-owned CII (2026). verify: https://www.csa.gov.sg/legislation/cybersecurity-act/
- FIs: **MAS TRM Guidelines + Notice on Technology Risk Management** (1h incident notice, critical-system availability) and Cyber Hygiene Notice.

## Japan: APPI

- Breach reporting mandatory since Apr 2022 (four triggers in the table). Extraterritorial for foreign businesses handling Japanese residents' data; cross-border transfer needs consent with information on the destination regime, an equivalent-system (contract) basis, or an adequacy country (EU/UK).
- **2026 amendment, enacted 10 Jul 2026, promulgated 17 Jul 2026, not yet in force**: introduces an **administrative surcharge (課徴金)** for serious, profit-generating violations (large-scale (>1,000 individuals) and lacking due care), consent exemption for statistics-only uses, rules for under-16s, stiffer penalties for illicit sale of PI databases. Cabinet orders/PPC rules setting the effective date were being drafted (Aug 2026); verify date and whether breach-report relaxations made the final text: https://www.ppc.go.jp/personalinfo/legal/r8kaiseihogohou/

## South Korea: PIPA

- **Amendment passed 12 Feb 2026, promulgated 10 Mar 2026, in force 11 Sep 2026**: punitive fines up to **10% of total revenue** for repeated or serious breaches (repeat intentional/grossly negligent violations within 3 years, ≥10M people affected, or a leak after ignoring a corrective order) vs the 3% general cap; notify on a **possible** leak, not only a confirmed one; forgery/alteration/damage now notifiable; **CEO accountability** explicit; CPO appointment/removal by **board resolution** reported to PIPC; fine mitigation for documented security investment. ISMS-P certification reported as mandatory for major entities from **1 Jul 2027** (verify). A further amendment (promulgated 8 Sep 2026, effective 9 Mar 2027); check content: https://www.law.go.kr/
- Korea is notably strict on **employee monitoring** and **cross-border consent**; see `load_skill insider-threat` before deploying UEBA there.

## Australia

- **Privacy Act 1988 / APPs**; max penalty the greater of **A$50m, 3× benefit, or 30% of adjusted turnover**. **POLA Act 2024** (Royal Assent 10 Dec 2024): statutory tort for serious invasions of privacy (from 10 Jun 2025), tiered civil penalties + OAIC infringement notices, APP 11 now names technical and organisational measures, **automated-decision transparency in privacy policies from 10 Dec 2026**.
- **Tranche 2**: exposure draft _Privacy Amendment (Personal Data Protection) Bill 2026_ released **31 Aug 2026**, consultation closed **18 Sep 2026**; government aims to legislate by Dec 2026; proposes a **72h** OAIC breach notice among much else. **Not introduced/enacted as of Nov 2026**; verify: https://consultations.ag.gov.au/rights-and-protections/privacy-reform/
- **SOCI Act 2018**: CIRMP (annual board-approved report), incident reporting 12h/72h, enhanced obligations for systems of national significance. **Cyber Security Act 2024**: ransomware-payment reporting (from 29/30 May 2025 by source; businesses above AUD 3m turnover; any "education first" grace is not in the legislation, unconfirmed), smart-device security standards, Cyber Incident Review Board. verify: https://www.cyber.gov.au/report-and-recover/report/ransomware-payment-and-cyber-extortion-payment-reporting
- **APRA**: **CPS 234** (info-sec capability, testing, 72h notice) and **CPS 230** (operational risk, critical operations + tolerances, material service providers) in force **1 Jul 2025**; pre-existing service-provider contracts had until the earlier of renewal or **1 Jul 2026**. verify: https://www.apra.gov.au/

## Working rules

- Run **the shortest clock first**: in a multi-country incident, China/India/Singapore-CII deadlines expire before you have finished GDPR scoping. Pre-agree local counsel and local-language templates (`load_skill incident-response-leadership`, `load_skill crisis-management`).
- **Transfer law ≠ breach law ≠ sector localisation**: three separate checks per dataset (`load_skill data-security`, `load_skill third-party-risk`).
- Contracts: push regulator-grade clocks into DPAs with APAC processors (`load_skill legal-contractual`).

## Pairs with

`load_skill privacy-eu`, `load_skill privacy-us`, `load_skill apac-cyber-regs`, `load_skill uk-cyber-regs`, `load_skill choosing-a-framework`, `load_skill cloud-assurance` (C-STAR / regional attestations), `load_skill control-mapping`.
