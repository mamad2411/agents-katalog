---
name: uk-cyber-regs
description: "Covers the UK cyber/privacy regime post-Brexit: NIS Regulations 2018 and the Cyber Security and Resilience Bill, UK GDPR as changed by the Data (Use and Access) Act 2025, NCSC CAF v4.0, Cyber Essentials v3.3, the PSTI product-security regime, finance op-res rules, and where the UK now diverges from EU NIS2/GDPR/CRA/DORA. Use when the user operates in or sells into the UK, or asks about UK NIS, UK GDPR, CAF, Cyber Essentials or PSTI."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# UK cyber & privacy regulation (practitioner orientation, NOT legal advice)

The UK left the EU before NIS2, DORA, the CRA and the AI Act, so **none of them apply in GB as law**: the UK runs its own, mostly narrower and more regulator-led, versions. A UK firm selling into the EU still meets the EU regimes (`load_skill nis2-dora`, `load_skill eu-cra`, `load_skill privacy-eu`). Dates below were checked Nov 2026; Parliament and commencement orders move them; re-verify.

## Map: who hits what

| If you are…                                                                     | Regime                                             | Regulator                     | Headline clock / obligation                                   |
| ------------------------------------------------------------------------------- | -------------------------------------------------- | ----------------------------- | ------------------------------------------------------------- |
| Operator of essential service (energy, transport, health, water, digital infra) | **NIS Regulations 2018** (SI 2018/506)             | Sector competent authority    | NIS incident to CA **without undue delay, ≤72h**              |
| Online marketplace / search engine / cloud provider (RDSP)                      | NIS Regs 2018                                      | **ICO**                       | ≤72h; lighter-touch, reactive supervision                     |
| MSP, data centre, designated critical supplier                                  | **Cyber Security and Resilience Bill** (pending)   | ICO / sector CAs              | **24h initial + 72h full** report (once commenced)            |
| Anyone processing personal data                                                 | **UK GDPR + DPA 2018** (as amended by DUAA 2025)   | ICO (Information Commission)  | Breach to ICO **≤72h** of awareness; individuals if high risk |
| Maker/importer/distributor of consumer connectable products                     | **PSTI Act 2022** + 2023 Regulations               | OPSS                          | 3 security requirements + statement of compliance             |
| Public telecoms provider                                                        | Telecommunications (Security) Act 2021 + 2022 Regs | Ofcom                         | Security measures + code of practice tiers (verify deadlines) |
| PRA/FCA-regulated firm                                                          | Op-resilience rules + PS26/2 / PS7/26              | PRA / FCA / BoE               | Impact tolerances; new incident + third-party reporting 2027  |
| Central-government supplier                                                     | Cyber Essentials (procurement policy)              | Cabinet Office / NCSC / IASME | CE (or CE Plus) as a contract condition                       |

## NIS Regulations 2018 and the Cyber Security and Resilience Bill

- **NIS Regs today:** OES + RDSPs, regulated sector-by-sector (Ofgem/DESNZ, DfT/CAA, DWI, Ofcom, DHSC/health bodies, ICO for RDSPs). Duty of appropriate and proportionate measures; incident notification ≤72h; max penalty **£17m**. The CAF (below) is the assessment instrument most CAs use. verify: https://www.legislation.gov.uk/uksi/2018/506
- **Cyber Security and Resilience (Network and Information Systems) Bill**: amends the NIS Regs rather than replacing them. Status (verified 6 Nov 2026): Commons stages done (report/third reading ~16 Jun 2026), carried over into the 2026 to 27 session (HL Bill 32); **Lords 2R 14 Jul, committee 1 to 7 Sep, report 26 Oct, third reading 2 Nov 2026**; now back in the **Commons for consideration of Lords amendments** (ping-pong). **Not law yet**, and even after Royal Assent most duties start only when **commencement regulations + secondary legislation/codes** land. verify: https://bills.parliament.uk/bills/4035
- What it adds: **relevant managed service providers (RMSPs)** in scope; **data centres** as essential services (thresholds by rated IT load: sources cite ~1MW for third-party/colocation and ~10MW for enterprise sites; verify); power to designate **critical suppliers**; incident reporting widened to incidents _capable_ of significant impact, **initial notice ≤24h, full report ≤72h**, to the regulator **and NCSC**; data centres/RDSPs/RMSPs must **notify likely-affected customers**; Secretary-of-State direction powers for national security; regulator cost recovery. Penalties two-tier: **£10m / 2%** and **£17m / 4%** of worldwide turnover (verify final text).
- Lords amendments now in ping-pong: a **statutory review of the NIS scheme within 12 months** and a **register of hostile state actors**; a frontier-AI incident-reporting amendment was defeated. Watch whether the Commons accepts them.
- Before commencement: if you're an MSP or data-centre operator, build the 24h/72h reporting path and customer-notification template ahead of commencement; it's the same muscle as NIS2 Art. 23.

## UK GDPR after the Data (Use and Access) Act 2025

- **DUAA**: Royal Assent **19 Jun 2025**, commenced in stages. The bulk of the Part 5 data-protection changes came into force **5 Feb 2026** (SI 2026/82): **recognised legitimate interests** (Annex 1 list, with no balancing test, e.g. crime prevention, safeguarding, security of systems), relaxed **automated decision-making** (Art. 22A to D: permitted with safeguards unless special-category data), a new **"not materially lower"** data-protection test for international transfers, and research/cookie changes (some analytics cookies consent-exempt; PECR fines raised toward UK GDPR levels; verify which date each commenced). **Complaints procedure duty from 19 Jun 2026** (s.103: you must run a data-protection complaints process). verify: https://www.gov.uk/guidance/data-use-and-access-act-2025-plans-for-commencement
- **ICO became the Information Commission on 30 Sep 2026**: a board-led body; it still trades as "ICO" and the chair keeps the "Information Commissioner" title. Update policies/DPAs that name the regulator only if you care about legal precision. verify: https://ico.org.uk/about-the-ico/what-we-do/legislation-we-cover/data-use-and-access-act-2025/
- **Unchanged for a security team:** breach to the ICO **≤72h** of awareness (Art. 33), individuals without undue delay if high risk (Art. 34); fines up to **£17.5m or 4%**; Art. 32 security of processing; DPIAs.
- **EU adequacy renewed 19 Dec 2025, valid to 27 Dec 2031**: EEA→UK flows need no SCCs. The EU will keep watching DUAA divergence; a material weakening (e.g. via the transfer test or ADM) is the adequacy risk to diary. verify: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/receiving-personal-information-from-the-eea/
- UK→US: the **UK Extension to the EU-US DPF** ("data bridge"), same CJEU-appeal risk as the EU DPF (`load_skill privacy-eu`); keep the IDTA/Addendum as fallback.

## NCSC Cyber Assessment Framework (CAF)

- **Current: CAF v4.0 (4 Aug 2025)**; no v4.1 as of Nov 2026. 4 objectives (A Managing risk, B Protecting, C Detecting, D Minimising impact), 14 principles, contributing outcomes judged Achieved / Partially / Not achieved against **IGPs** (indicators of good practice). New in v4.0: **A2.b Understanding threat**, **A4.b Secure software development and support** (provenance, attestable integrity), reworked **C1 monitoring/threat hunting** (triage, playbooks, automated response), AI risk throughout. verify: https://www.ncsc.gov.uk/collection/cyber-assessment-framework
- **Profiles** are set by regulators, not NCSC: the **CAF Core Profile** (built on v4.0, aimed at moderately capable adversaries: ransomware, supply chain) is the transition baseline. Ask your CA which profile and version it expects in the next self-assessment.
- NCSC is building a CAF-based **Cyber Resilience Audit scheme** for assured independent assessment alongside the Bill (verify status). Pitfall: CAF is outcome-based: screenshots of a policy don't evidence "Achieved"; show the outcome operating.

## Cyber Essentials (CE / CE Plus)

- **Requirements for IT Infrastructure v3.3 (question set "Danzell"), effective 27 Apr 2026.** Five controls: firewalls, secure configuration, security update management (critical/high patches ≤14 days), user access control, malware protection. CE = verified self-assessment; **CE Plus** = same requirements + hands-on technical audit. verify: https://www.ncsc.gov.uk/cyberessentials/resources
- v3.3 changes that fail people: **MFA on every cloud service that supports it is an automatic fail if missing** (free or paid tier, users and admins); cloud services **cannot be scoped out** (social media accounts count); FIDO2/passkeys count as MFA; backup is recommended, not required. Accounts opened before the switch had 6 months on the old version.
- It's a **floor**, not a framework: useful for supply-chain gating (`load_skill third-party-risk`), not evidence of NIS/CAF maturity.

## PSTI: consumer connectable product security

- In force **29 Apr 2024**: **no universal/default passwords**, a published **vulnerability disclosure policy** (contact + acknowledgement/status updates), and a stated **minimum security-update period** at point of sale; manufacturers ship a **statement of compliance**. Duties also bite importers/distributors. Exclusions include laptops/desktops, smart meters, medical devices, vehicles (separate regimes).
- Enforcer **OPSS**: compliance/stop/recall notices, penalties up to **£10m or 4%** of worldwide revenue + **£20k/day**. 2025/26 was education-first (100+ product assessments, 200+ VDPs checked); no amendment regs found. verify: https://www.gov.uk/government/publications/the-uk-product-security-and-telecommunications-infrastructure-product-security-regime
- Versus the EU CRA: PSTI is **three requirements on consumer products**; the CRA is a full essential-requirements + conformity-assessment + 24h vuln-reporting regime for nearly all products with digital elements. Selling in both = build to the CRA.

## Finance (the UK's answer to DORA)

- **PRA/FCA operational resilience** (SS1/21, PS21/3): important business services, impact tolerances, mapping + scenario testing; fully in force since 31 Mar 2025. **Critical third parties** regime (FSMA 2023; rules from 1 Jan 2025): HM Treasury designates; no designation list confirmed as of Nov 2026 (verify).
- **FCA PS26/2 + PRA PS7/26 (18 Mar 2026), applying 18 Mar 2027:** a single operational-incident reporting regime (PRA collapsed initial/interim/final into one report) plus notification of **material third-party arrangements** and an annual register. verify: https://www.fca.org.uk/publications/policy-statements/ps26-2-operational-incident-third-party-reporting
- Intelligence-led testing is **CBEST**, not TIBER-EU/TLPT.

## Where the UK diverges from the EU (the comparison clients ask for)

| Topic                | EU                                                | UK                                                                                                                             |
| -------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Scope of cyber law   | NIS2: 18 sectors, essential + important, size-cap | NIS Regs: 5 sectors + RDSPs; Bill adds MSPs, data centres, critical suppliers; **no manufacturing/food/postal/chemicals tier** |
| Incident clock       | 24h early warning / 72h / 1 month                 | Today ≤72h; Bill: 24h initial / 72h full                                                                                       |
| Management liability | Explicit NIS2 board accountability + training     | No NIS2-style board-liability clause in the Bill (verify); governance via CAF A1                                               |
| Privacy              | GDPR; Digital Omnibus pending                     | UK GDPR + DUAA: recognised LIs, looser ADM, own transfer test, complaints duty                                                 |
| Products             | CRA (full lifecycle, CE marking)                  | PSTI (3 requirements, consumer IoT only)                                                                                       |
| Finance              | DORA (Regulation, CTPP oversight live)            | PRA/FCA op-res + CTP regime + PS26/2 (2027)                                                                                    |
| AI                   | AI Act                                            | No AI statute; regulator-led principles                                                                                        |

Northern Ireland follows some EU product rules under the Windsor Framework; check whether the CRA reaches NI-placed products before assuming PSTI alone (verify).

## Common pitfalls

- Assuming "we're NIS2-ready" covers the UK (different regulators, scope and forms), or the reverse.
- Treating the Bill as in force: until commencement regs, an MSP has no statutory UK reporting duty (contracts may still impose one).
- Citing CAF v3.2 or CE v3.2 in a 2026 assessment; both were superseded.
- Ransomware-payment ban/reporting for public sector and CNI was announced as policy (2025), but legislation in force is unconfirmed; check before advising on payment decisions (`load_skill incident-response-leadership`).

## Pairs with

`load_skill nis2-dora` (EU side), `load_skill privacy-eu`, `load_skill eu-cra`, `load_skill choosing-a-framework`, `load_skill control-mapping` (CAF↔ISO 27001↔CSF), `load_skill cloud-assurance` (what to ask a cloud/MSP supplier), `load_skill third-party-risk`.
