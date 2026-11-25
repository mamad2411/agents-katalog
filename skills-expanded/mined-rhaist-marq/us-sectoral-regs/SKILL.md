---
name: us-sectoral-regs
description: Covers the US security regimes teams meet (SEC cyber disclosure 8-K, HIPAA Security Rule, GLBA Safeguards, NYDFS 23 NYCRR 500, CMMC/FedRAMP/FISMA/NIST 800-171), with a who-must-comply-with-what decision table. Practitioner orientation, not legal advice. Use when the user asks which US regulation applies, SEC material incident disclosure, HIPAA or CMMC requirements, or selling to the US government.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# US sectoral cyber regulations (practitioner orientation, NOT legal advice)

There is no general US cyber law; obligations attach by **what you do** (public company, handle health/financial data, sell to NY-regulated finance, contract with DoD/federal). Each has its **own regulator and clock**. Dates shift; web-fetch the source. Engage counsel for filings.

## Who must comply with what (decision table)

| If you are…                                | Regime                                 | Regulator          | Headline obligation / clock                                                           |
| ------------------------------------------ | -------------------------------------- | ------------------ | ------------------------------------------------------------------------------------- |
| US public company (SEC registrant)         | SEC cyber disclosure rules             | SEC                | **8-K Item 1.05 within 4 business days** of materiality call; annual **10-K Item 1C** |
| Health provider/plan/clearinghouse + BAs   | HIPAA Security + Breach Rules          | HHS OCR            | Safeguards; breach notice **≤60 days** (≥500 indiv.)                                  |
| Nonbank financial institution              | GLBA **Safeguards Rule**               | FTC                | Written infosec program; **notify FTC ≤30 days** (≥500 consumers)                     |
| Bank / depository institution              | GLBA via banking agencies              | OCC/FDIC/FRB/NCUA  | **36-hour** computer-security incident notice to regulator                            |
| NY-licensed financial/insurance entity     | **23 NYCRR Part 500** (NYDFS)          | NY DFS             | **72-hour** incident notice; **24-hour** extortion-payment notice                     |
| DoD contractor handling **CUI**            | **CMMC 2.0** (+ DFARS 252.204-7012)    | DoD / C3PAO        | Level 1 to 3 assessment; **72-hour** incident report to DC3                           |
| Cloud service sold **to federal agencies** | **FedRAMP**                            | GSA / FedRAMP      | FedRAMP Certification (Class A to D, 2026 rules) before federal use                   |
| Federal agency / its IT contractors        | **FISMA / NIST 800-53**                | OMB / CISA / NIST  | Agency ATO program                                                                    |
| Any federal contractor handling CUI        | **NIST SP 800-171**                    | Contracting agency | 110 controls; SPRS score                                                              |
| Critical-infrastructure owner/operator     | **CIRCIA** (when final) + sector rules | CISA + sector      | Covered-incident reporting (rule pending; see below)                                  |

## SEC cybersecurity disclosure (public companies)

- In force since **Dec 2023** (large filers; smaller reporting companies phased in ~June 2024). Two pieces:
  - **Form 8-K Item 1.05**: disclose a **material** cybersecurity incident **within 4 business days** of the **materiality determination** (NOT discovery: the clock starts when you decide it's material, and you must make that call "without unreasonable delay"). Describe nature, scope, timing, and material impact.
  - **Form 10-K Item 1C**: **annual** disclosure of cyber **risk-management processes, strategy, and board/management governance.**
- **National-security/public-safety delay**: only if the **US Attorney General** notifies the SEC; initial delay up to 30 days (extendable). https://www.sec.gov/rules/final/2023/33-11216.pdf
- **Status:** industry petitioned in 2025 to rescind/narrow Item 1.05 (joint petition filed May 2025) and the Commission majority shifted, but **the rule remains in effect as of Nov 2026**; no rescission or amendment has been adopted. **Verify current status** before advising: https://www.sec.gov/rules-regulations/2025/05/joint-petition-rulemaking-amend-sec-cybersecurity-risk-management-strategy-governance-incident
- Pitfall: a **ransom payment or extortion** is not automatically a 1.05 trigger; the test is **materiality**, and many filers over-disclosed early. Document the materiality analysis.
- **Filer practice:** voluntary **Item 8.01** disclosure now outnumbers Item 1.05 (roughly 50 vs 29 filings two years in). Filing under 8.01 avoids asserting materiality, but it is not a way to dodge 1.05 once you have determined the incident _is_ material.

## HIPAA Security Rule (health)

- Applies to **covered entities + business associates**. Requires **administrative, physical, technical safeguards** for ePHI (risk analysis is the central control).
- **Breach Notification Rule**: notify affected individuals **and HHS without unreasonable delay, ≤60 days**; **≥500 individuals** = notify HHS and **prominent media** promptly (≤60 days); **<500** = annual log to HHS. https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html
- **2025 Security Rule NPRM** proposes to **modernize/strengthen** safeguards (mandatory MFA, encryption, asset inventory, faster restoration objectives). Comment period closed Mar 2025 (~4,700 comments). **Not finalized and not withdrawn as of Jul 2026**; the rule has been demoted to the Unified Agenda's **"long-term actions"** with final action targeted **2027**, after 100+ industry organisations demanded withdrawal in Dec 2025. Treat it as **not a 2026 compliance driver**, but don't tell a client it's dead. **Verify status/effective date:** https://www.hhs.gov/hipaa/for-professionals/security/hipaa-security-rule-nprm/index.html

## GLBA Safeguards Rule (nonbank financial: FTC)

- FTC-enforced version applies to **nonbanking financial institutions** (mortgage brokers, auto dealers/financing, payday lenders, tax preparers, etc.; broader than people expect).
- Requires a written infosec program with **named qualified individual, risk assessment, MFA, encryption, access controls, vendor oversight**.
- **Breach notification (effective May 13 2024):** notify the **FTC as soon as possible, no later than 30 days** after discovering an event involving **unencrypted info of ≥500 consumers**. https://www.ftc.gov/news-events/news/press-releases/2023/10/ftc-amends-safeguards-rule-require-non-banking-financial-institutions-report-data-security-breaches
- **Banks** follow GLBA via their prudential regulators, with the separate **36-hour** incident-notification rule: different clock, different regulator.

## NYDFS 23 NYCRR Part 500 (NY financial/insurance)

- Applies to entities with a **NY DFS license** (banks, insurers, mortgage lenders, etc.). Second Amendment (Nov 2023) **fully effective Nov 1 2025**.
- **72-hour** notice to the Superintendent for a reportable cybersecurity incident; **24-hour** notice of any **extortion/ransom payment** + written justification within 30 days. CISO + annual certification, MFA, asset inventory. https://www.dfs.ny.gov/industry_guidance/cybersecurity

## CMMC 2.0 / FedRAMP / FISMA / 800-171 (federal & defense)

- **CMMC 2.0**: DoD contractors handling **FCI/CUI**. Final **48 CFR** acquisition rule **effective Nov 10 2025**, triggering a **4-phase rollout** (verify, dates have moved before):
  - **Phase 1: Nov 10 2025** (the current phase): L1/L2 **self-assessment** required in new contracts.
  - **Phase 2: was Nov 10 2026**: L2 **third-party (C3PAO) certification**. ⚠️ **SUSPENDED 13 Jul 2026** by DoD/DoW pending a 60-day CMMC reform-task-force review (report delivered internally ~11 Sep 2026, **not published; Phase 2 still suspended with no new date as of early Nov 2026**). Announced as policy, then written into DFARS Part 240 by **class deviation 2026-O0025 Rev 3 (3 Sep 2026)**, which has contracting officers remove L2 C3PAO / L3 requirements from active solicitations and contracts (https://www.acq.osd.mil/dpap/dars/dfars_far_overhaul_class_deviations.html). It is **not a Federal Register action**: 32 CFR 170 and DFARS 252.204-7021 still stand, so **do not stand down**: Phase 1 self-assessment, SPRS posting, annual affirmation by an Affirming Official and subcontractor flowdown all remain in force. Re-verify before advising anyone.
  - **Phase 3: Nov 10 2027**: L3. **Phase 4: Nov 10 2028**: full implementation. Both are **also suspended**; the 13 Jul suspension covers all "pending and future" CMMC milestones.
  - https://www.federalregister.gov / https://dodcio.defense.gov/cmmc/ and **verify current phase.** Contract clause is **DFARS 252.204-7021**; DFARS 252.204-7012 still requires **72-hour** incident reporting to DC3 + DIBNet.
- **FedRAMP**: standardized **certification** for **cloud services sold to federal agencies**. The **Consolidated Rules for 2026** (launched 24 Jun 2026, mandatory for all stakeholders **1 Jan 2027**, with area-specific dates over the following year) certify by **Class A to D** (minimal → significant assurance) and replace "authorization" with "certification". FIPS-199 **Low/Moderate/High** remain the security categories, and **NIST 800-53** still underpins the Rev5 path; **20x** is the automated path, and **new Rev5 certifications end 11 Jun 2027**. verify: https://www.fedramp.gov/2026/timeline/ and https://www.fedramp.gov/2026/definitions/
- **FISMA**: governs **federal agencies** (and their contractors operating systems on their behalf); implemented via **NIST 800-53** controls and agency ATOs.
- FedRAMP read against other cloud attestations (STAR, C5, 27017/27018): `load_skill cloud-assurance`.
- **NIST SP 800-171**: the **110-control** CUI baseline for non-federal systems; contractors self-score into **SPRS**. This is the shared substrate under CMMC L2. **Mind the revision:** **Rev 3** is final (May 2024), but **CMMC L2 assessments still run against Rev 2**; don't score a defense contractor against Rev 3 because it's newer. Separately, the proposed **FAR CUI rule** (recast in 2026 under the FAR Overhaul, moving CUI to a new FAR Part 40) would raise the civilian-agency baseline to **Rev 3** and relax incident reporting from 8 to 72 hours; **still a proposal, not final**.
  Assessor-level scoring, 170.19 scoping and 170.21 POA&M rules: `load_skill cmmc-800-171`.

## Critical infrastructure / utilities (high level)

- **CIRCIA** (Cyber Incident Reporting for Critical Infrastructure Act): will require **covered entities** to report covered incidents to **CISA within 72 hours** and ransom payments within 24 hours, **once the final rule is in effect; still NOT enforceable as of mid-2026**: CISA missed the statutory Oct 2025 deadline, targeted May 2026 and missed that too; town halls ran Jun 2026 (after the DHS appropriations lapse) on narrowing scope/burden; it then missed its Sep 2026 Unified Agenda target and **sent the final rule to OMB for review ~1 Oct 2026** (text not public; publication expected late 2026/early 2027, effective date later still). Until it lands **no entity owes a CIRCIA report**; the obligation attaches only at the final rule's effective date. **Verify status:** https://www.cisa.gov/topics/cyber-threats-and-advisories/information-sharing/cyber-incident-reporting-critical-infrastructure-act-2022-circia
- **Cybersecurity Information Sharing Act of 2015**: the liability/antitrust protection for sharing indicators with the government. It **lapsed for ~6 weeks (1 Oct to 12 Nov 2025)**, was restored retroactively-uncertain, and was extended by the FY2027 stopgap (**P.L. 119-103**, signed 2 Sep 2026). It **currently expires again 11 Dec 2026**. If your threat-sharing programme leans on those protections, diary the date and check before assuming cover.
- Sector-specific: **NERC CIP** (bulk electric system), **TSA Security Directives** (pipelines, rail, aviation), **EPA/AWIA** (water), **NRC** (nuclear). Plus state PUC/utility-commission rules. Treat these as additional, not substitutes.

## US vs EU framing

- The US equivalent of NIS2/DORA is **not one law**: it is this **sectoral spread** (SEC ≈ disclosure governance, NYDFS/GLBA ≈ DORA-ish for finance, CMMC/FISMA ≈ federal supply chain, CIRCIA ≈ NIS2-ish but narrower and pending). See `load_skill privacy-eu` for the EU side.

## Pairs with

- US privacy patchwork + breach notification: `load_skill privacy-us`.
- Mapping these regimes onto one control set (don't build N programs): `load_skill control-mapping`, `load_skill choosing-a-framework`.
- Vendor/contract flow-downs (DFARS, BAAs, FedRAMP): `load_skill third-party-risk`, `load_skill legal-contractual`.
