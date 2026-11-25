---
name: middle-east-regs
description: "Covers Middle East cyber and data-protection law for security and GRC teams responsible for an entity in the region, at group HQ or locally: Saudi Arabia (NCA ECC-2, OTCC-1, SDAIA PDPL), UAE (federal PDPL, Dubai DESC, DIFC, ADGM), Qatar (PDPPL, QFC), Bahrain, Oman, Kuwait, Israel and Turkey (Law 7545, KVKK), with scope triage, one clocks table, localisation and remote-SOC limits, OT/ICS angles and pending changes. Use when the user has entities, sites or offices in the Gulf, Israel or Turkey, or asks about NCA ECC or OTCC, SDAIA PDPL, DIFC, ADGM, PDPPL, KVKK, Law 7545, or whether a SOC outside the Kingdom may monitor an in-scope Saudi entity."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Middle East cyber & privacy regulation (practitioner orientation, NOT legal advice)

Written for security and GRC teams responsible for an entity in the region, whether at group HQ or the local entity itself, asking four questions: does it reach this entity, which clock runs, what can leave the country, can a SOC outside the country monitor it. Where a law's official text is in Arabic, Hebrew or Turkish, check the original: English versions and summaries are aids. DIFC, ADGM and QFC publish their law in English. Status tags used below: **V** read in official text, **S** secondary or snippet-level source, **U** unverified. Anything tagged U is a lead to confirm with local counsel, not a fact. Dates checked 17 Nov 2026; this region moves fast.

## Does it reach this entity? (triage)

1. **Saudi NCA controls bind by status.** ECC-2:2024 covers government entities and their affiliates (inside and outside the Kingdom) plus private entities owning, operating or hosting critical national infrastructure (CNI) (V). Other entities are only "strongly encouraged". A private entity outside CNI is not automatically in scope; it is reached through CNI status or customer flow-down (e.g. Aramco, government contracts). Get written applicability from the customer or NCA.
2. **UAE is three layers.** Onshore federal law, Dubai (DESC), and the financial free zones DIFC and ADGM, each with its own data law. Locate each entity: an operating entity onshore, an office in DIFC and a treasury entity in ADGM sit under different regimes.
3. **Dubai cyber rules bind government and designated critical entities.** Law 15/2024 gives DESC oversight of government entities and "critical non-government entities" (S). A private Dubai entity is reached by designation or contract.
4. **Turkey designates by sector.** The Cybersecurity Board named 15 critical sectors on 5 May 2026, including **Manufacturing Industry** and **Energy** (V). Secondary regulations are still in preparation, so duties for those sectors are not yet defined.
5. **Data-protection laws bind everyone processing personal data** in the country (HR, CRM, visitor, CCTV, badge data), whatever the sector.

## Clocks table

| Jurisdiction    | Regime                                   | Clock                                                     | Recipient                    | Status                    |
| --------------- | ---------------------------------------- | --------------------------------------------------------- | ---------------------------- | ------------------------- |
| Saudi           | NCA ECC-2 incident controls              | No hour clock in ECC-2; 2026 draft says "immediately"     | NCA (HASEEN)                 | V (ECC-2); draft is S     |
| Saudi           | PDPL Art. 20 + Implementing Regulation   | Statute: on knowing; **72h** sits in the Regulation       | SDAIA, individuals           | V statute; 72h text **U** |
| UAE federal     | PDPL Art. 9                              | "Immediately"; Executive Regulations not confirmed        | Not stated in sources        | S                         |
| UAE (DIFC)      | DP Law 5/2020 Art. 41(1)                 | **As soon as practicable** (not 72h)                      | DIFC Commissioner            | V                         |
| UAE (ADGM)      | DPR 2021 s.32                            | Without undue delay, where feasible **72h**               | ADGM Office of DP            | V (ADGM page)             |
| UAE federal     | Cyber Incident Response Framework v2.0   | Applicability, clock, recipient unknown                   | UAE Cyber Security Council   | **U**                     |
| Qatar (non-QFC) | PDPPL Art. 14 + NCSA guideline           | Statute silent; guideline "without delay, within **72h**" | NCSA (NCGAA), individual     | V (guideline)             |
| Qatar (QFC)     | QFC DP Regulations 2021                  | **72h**; USD 150,000 penalty issued 2 Sep 2024            | QFC DPO                      | V                         |
| Bahrain         | PDPL 30/2018, Order 43/2022              | **72h**                                                   | PDPA                         | S (weak source)           |
| Oman            | PDPL Art. 19 + Exec. Reg. MD 34/2024     | Statute defers; **72h** in Regulation                     | Ministry, data subject       | V statute; 72h S          |
| Kuwait          | CITRA Decision 2024/26                   | 24h vs 72h conflict; scope also unclear                   | CITRA                        | **U**                     |
| Israel          | Data Security Regulations 2017           | "Immediately" for a severe incident                       | Privacy Protection Authority | S (weak source)           |
| Turkey          | Law 7545 Art. 7(1)                       | "Without delay", no number                                | Cybersecurity Presidency     | V                         |
| Turkey          | KVKK Art. 12(5) + Board decision 2019/10 | **72h**                                                   | KVKK Board                   | V                         |

Do not cite 72h as UAE federal law, and do not cite 72h for DIFC. Qatar's NCSA advisory suggesting 2h for national-level cyber incidents is U.

## Country notes

- **Saudi Arabia.** ECC-2 has 4 domains, 28 subdomains, 108 main controls (V). Control 1-2-2 requires cyber positions to be filled by full-time qualified Saudi professionals (V). ECC-2 removed its ICS domain (now OTCC) and the in-Kingdom hosting sub-control (moved to NDMO/SDAIA standards). CCC-2:2024 covers cloud for providers and tenants. PDPL (M/19, 2021, amended 2023): fines up to SAR 5m, doubling for repeats; up to 2 years and SAR 3m for intentional disclosure of sensitive data (V). The in-force date and grace period, registration and DPO rules are U.
- **UAE.** Federal PDPL (Decree-Law 45/2021) has no confirmed Executive Regulations, so build to a GDPR-like baseline without calling it a 72h regime. Federal cybercrime is Decree-Law 34/2021 (U at primary level). The Information Assurance Regulation's binding scope is U. DIFC: since the 2025 amendment, controllers and processors acting under "stable arrangements" are in scope with no "occasional" carve-out (Art. 6(3)(b)), data subjects can sue in the DIFC Courts (Art. 64A), and Schedule 2 fines run USD 25,000 to 50,000 plus an uncapped general fine (V). ADGM's USD 28m cap is S only; ADGM transfer rules were not researched.
- **Qatar.** Two breach regimes (see table). Reported PDPPL fines of QAR 1m (failure to report) and QAR 5m (inadequate precautions) rest on unread article text (S). The NIA Policy has no verified binding scope, OT provisions or IEC 62443 mapping.
- **Bahrain.** Weak sources. PDPL in force 1 Aug 2019; the 72h and the transfer whitelist (Order 42/2022) are snippet-level. No cyber or CII statute found; NCSC's legal basis and the 2025 cybercrime decree are U.
- **Oman.** PDPL (RD 6/2022): breach-notification failures OMR 15,000 to 20,000 (Art. 28) and unlawful transfers **OMR 100,000 to 500,000** (Art. 29) (V, via a private republisher). New Cybercrime Law RD 61/2026 effective 8 Jun 2026; corporate liability under it is U. No CNI rules found.
- **Kuwait.** CITRA Decision 2024/26 replaced Resolution 42/2021; its scope may be wider than telecoms (U). NCSC Decision 2/2026 reportedly makes national baseline controls mandatory for government and critical private organisations with 18 months to comply, from vendor and press summaries only (U).
- **Israel.** No primary text was readable. Amendment 13 to the Privacy Protection Law is reported effective 14 Aug 2025 (S). Do not quote penalty or DPO details.
- **Turkey.** Law 7545 (OG 19 Mar 2025): Art. 7(1) reaches anyone who provides services or processes data using information systems. Fines TRY 1m to 10m for Art. 7(1)(a) to (c), and up to **5% of gross sales** for commercial companies (Art. 16(11), tied to audit cooperation under Art. 8(4)); criminal terms from 1 to 15 years. **Art. 18 (approval of ownership transactions) covers cyber-product companies only**, not manufacturers. Pre-7545 baseline: the 2019 Presidential Circular and Information and Communication Security Guide for public bodies and critical operators. KVKK transfers were reformed by Law 7499 (adequacy, BCRs, Board standard contract notified within 5 business days of signature); its entry-into-force date is U.

## Transfers, localisation and remote SOC

The rules below state what must stay in country or what safeguards a transfer needs; the practical consequence falls on any SOC, SIEM or central hosting outside it.

- **Saudi, the sharpest constraint.** ECC-2 control 4-1-3-2: managed cyber monitoring or operations centres that use remote access must be **fully located in the Kingdom** for in-scope entities (V). A group SOC outside the Kingdom (for example in the EU or US) cannot be assumed to monitor an in-scope Saudi site; ask for a written exemption or stand up an in-Kingdom managed service.
- **Saudi PDPL transfers** (Transfer Regulation v2.0, Aug 2024, V): SDAIA adequacy list reviewed every 4 years; safeguards are SCCs, BCRs or an accreditation certificate; intra-group "necessary central operations" are an exemption route (BCRs, SCCs or certified recipient); a transfer risk assessment is mandatory (Art. 7).
- **Oman:** transfers allowed under the regulation's controls, "without prejudice to Cyber Defence Centre competences" (Art. 23), with the OMR 100,000 to 500,000 penalty ceiling. Treat every cross-border data flow, including group reporting, as in scope.
- **UAE sector rules (S):** health data may not leave the UAE; payments data stays onshore.
- **Turkey:** Law 7499 routes (adequacy, BCRs, Board standard contract).
- Kuwait NCSC approval for offshore storage is headline-only (U). Qatar PDPPL Art. 15 transfers are U.

## OT / ICS

- **Saudi OTCC-1:2022** is the OT extension of ECC: 4 domains, 23 subdomains, 47 main controls, 122 subcontrols (V). It applies to ICS in facilities "deemed critical" owned or operated by government or CNI organisations, **whether in the Kingdom or abroad**. Criticality (high/moderate/low) is set per facility in a separate Methodology and Mapping Annex (not read), so ask the customer which level your site was assigned. An OT site in scope needs OTCC on top of ECC-2.
- **OTCC has no confirmed IEC 62443 mapping.** The text read never mentions 62443; an Annex crosswalk is U. An IEC 62443 programme gives partial coverage at best.
- **Dubai:** the DESC ICS Standard targets government and semi-government critical-infrastructure operators (S). ISR applies to Dubai Government Entities; "ISR v3" has no official source.
- **Turkey:** manufacturing and energy are designated critical sectors; wait for the secondary regulations, and meanwhile expect OT questions from customers.
- Qatar NIA: no OT provisions verified. Israel: the draft bill's standards route is not law.

## Framework mapping (inference, not published crosswalks)

National frameworks stand on their own terms: ECC-2 is the baseline for in-scope Saudi entities and OTCC extends it. Entities already on ISO 27001 or NIST CSF can reuse that work, and mappings work in both directions (national control sets can feed an ISO or CSF programme). The notes call these mappings inference, so treat them as planning aids. No crosswalk from ECC-2 to ISO 27001 or NIST CSF is confirmed in the sources, so any existing ISMS or CSF programme is a starting point, not evidence of compliance. OTCC extends ECC, so an IEC 62443 programme may cover part of it (no confirmed crosswalk). The Israeli bill may accept listed standards such as NIST SP 800-53 (a bill, not law). Qatar NIA is described as ISO 27001-aligned by a low-authority vendor summary (U). Kuwait's baseline is described as CIS or NIST CSF aligned by one vendor (U).

## Pending changes (as of 17 Nov 2026)

| Item                                                 | Status                                                                                                                                                                                                                                     |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Saudi PDPL Implementing Regulation amendment (draft) | Consultation 6 Oct to 5 Nov 2026 (law-firm sources): store-in-Kingdom duty for controllers, wider registration, breach-reporting harm threshold reportedly removed. Adoption not found. Biggest risk for HR/CRM hosted outside the Kingdom |
| Saudi NCNICC-1:2024 (non-CNI private organisations)  | Draft; only title and status confirmed (scope unread). Watch it if the entity is private and outside CNI                                                                                                                                   |
| UAE federal PDPL Executive Regulations               | Not confirmed issued. New AI and Data authority announced June 2026 (S)                                                                                                                                                                    |
| Israel National Cyber Defense Bill 5786-2026         | Passed first reading 8 Jun 2026 (S); survival across the Knesset election U                                                                                                                                                                |
| Turkey Law 7545 sector regulations                   | Manufacturing and Energy rules in preparation (Presidency FAQ, Jul 2026)                                                                                                                                                                   |
| Kuwait NCSC Decision 2/2026                          | Reported; 18-month compliance window; unconfirmed against the Gazette                                                                                                                                                                      |

## Working rules

- Get **written applicability** per site (customer letter, designation, regulator reply) before building to ECC-2, OTCC or a Turkish sector rule.
- Keep a per-site map: legal entity, zone (onshore, DIFC, ADGM, QFC), data categories, whether any customer flow-down applies.
- Build the incident path to the **shortest confirmed clock** per site, and treat table rows tagged U as "ask counsel", not as the clock.
- Before any SOC, MDR or SIEM outside the Kingdom onboards a Saudi site, check control 4-1-3-2.
- Do not cite Israel or Bahrain figures to a regulator or in a contract; the sources are weak.
- Re-verify against primary text after each pending item above lands.

## Pairs with

`load_skill breach-notification-matrix` (all clocks side by side), `load_skill ot-compliance`, `load_skill choosing-a-framework`, `load_skill third-party-risk` (customer and MSSP flow-down), `load_skill privacy-eu` (the GDPR baseline and transfer comparisons).
