---
name: control-frameworks
description: "Covers NIST SP 800-53, CIS Controls v8.1 and COBIT 2019: what each is for, when to pick which, and how they map to ISO 27001 and NIST CSF. Use when the user asks about 800-53 control families or baselines, CIS Implementation Groups, COBIT IT governance, or choosing a control catalog."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Control frameworks: 800-53 vs CIS Controls vs COBIT

Three different jobs. Don't pick by brand, pick by what you need: an **exhaustive control catalog**, a **prioritized do-this-first baseline**, or an **IT-governance operating model**.

## NIST SP 800-53: the control _catalog_

- **Current: Release 5.2.0, published 27 Aug 2025** (a patch release on Rev 5; verify: https://csrc.nist.gov/projects/cprt/catalog#/cprt/framework/version/SP_800_53_5_2_0/home and the 5.2.0 news at https://csrc.nist.gov/News/2025/nist-releases-revision-to-sp-800-53-controls). 5.2.0 adds **no new families**; it strengthens existing controls around **secure software development, update management, software integrity/validation** (driven by EO 14306). Still **20 control families**, ~1000+ controls+enhancements, security **and** privacy.
- **For**: U.S. federal systems and **FISMA/FedRAMP** (mandatory there), or anyone wanting the most comprehensive control library to draw from. Baselines (Low/Moderate/High) come from **SP 800-53B**; the selection _process_ is the **RMF (SP 800-37)**, and **SP 800-53A** gives the assessment procedures.
- **Not for**: a small org wanting a quick start; it's a reference catalog, **not prioritized**. You tailor down, you don't implement all of it.

## CIS Controls v8.1: the prioritized _baseline_

- **Current: v8.1** (released 2024; minor update to v8, adds governance emphasis and aligns asset classes to NIST CSF 2.0). **18 Controls**, **153 Safeguards**. Verify: https://www.cisecurity.org/controls
- **Implementation Groups** scope effort by org maturity: **IG1** = "essential cyber hygiene" (56 safeguards, the floor for every org), **IG2** (adds for orgs managing more sensitive data/multiple departments), **IG3** (all 153, for orgs facing sophisticated/targeted threats).
- **For**: SMBs and anyone who wants an **ordered, actionable "start here"** list, plus free tooling (CIS-RAM risk method, CIS Benchmarks for hardening, CIS Controls Navigator for mappings). Pairs naturally with **CIS Benchmarks** (config hardening).
- **Not for**: a formal compliance attestation by itself; it's a hygiene baseline, not a certifiable standard. Use it to _prioritize_ implementation, then map up to a framework you must attest against.

## COBIT 2019: the IT _governance_ model

- **Current: COBIT 2019** (ISACA; succeeds COBIT 5). Its successor **COBIT 7** was announced by ISACA for **27 Oct 2026**; re-verify the structure below against COBIT 7. **40 governance & management objectives** across 5 domains: **EDM** (Evaluate/Direct/Monitor, 5 governance), **APO** (Align/Plan/Organise, 14), **BAI** (Build/Acquire/Implement, 11), **DSS** (Deliver/Service/Support, 6), **MEA** (Monitor/Evaluate/Assess, 4). Adds **design factors** + **focus areas** to tailor a governance system.
- **For**: **enterprise governance of IT (EGIT)**, board/management accountability, aligning IT to business goals, audit (ISACA's home turf). It governs the _system that runs_ security, not the technical controls themselves.
- **Not for**: hands-on technical control selection; it sits **above** 800-53/CIS, not beside them. Security teams rarely implement COBIT directly; auditors and IT-governance functions do.

## Decision table

| Need                                 | Pick                                     | Why                                            |
| ------------------------------------ | ---------------------------------------- | ---------------------------------------------- |
| FedRAMP / FISMA / U.S. federal       | **800-53** (+ 800-53B baselines, RMF)    | Mandated; exhaustive catalog                   |
| "Where do we start?" / SMB hygiene   | **CIS Controls v8.1 (IG1)**              | Prioritized, free, actionable                  |
| Harden specific systems              | **CIS Benchmarks**                       | Config-level guidance                          |
| Board-level IT governance / IT audit | **COBIT 2019**                           | Governance objectives, business-IT alignment   |
| Certifiable ISMS (intl.)             | **ISO 27001** → `load_skill iso27001`    | Certificate, Annex A controls                  |
| Common language / program structure  | **NIST CSF 2.0** → `load_skill nist-csf` | Govern/Identify/Protect/Detect/Respond/Recover |

## How they map together

- **NIST CSF 2.0** is the umbrella _outcomes_ framework; its Informative References map each subcategory **down to 800-53 controls and CIS Safeguards**; use CSF as the index, 800-53/CIS as the implementation detail.
- **CIS v8.1 ⇄ 800-53 Rev 5**: CIS publishes an official mapping (CIS Controls Navigator / white papers). CIS = the IG1 subset; 800-53 = the full superset. Implement CIS first, then prove 800-53/ISO coverage from it.
- **ISO 27001 Annex A ⇄ 800-53 / CIS**: many-to-many; NIST publishes an official 800-53 Rev 5 ⇄ ISO/IEC 27001:2022 crosswalk (OLIR, SP 800-53 supplemental material). Reuse evidence once, claim against several; see `load_skill control-mapping`.
- **COBIT** maps to ISO 27001 and NIST CSF at the _governance_ layer (it doesn't compete at the control layer).

## Pitfalls

- **Treating CIS or 800-53 as "compliance"**: they're control sets; the certifiable/attestable wrappers are ISO 27001, SOC 2, FedRAMP. Pick the _obligation_ first (`load_skill choosing-a-framework`).
- **Implementing all of 800-53**: always tailor via a baseline; the full catalog is a menu.
- **Confusing COBIT with a control framework**: it governs the program; it won't tell you to enable MFA.
- **Version drift**: cite **800-53 5.2.0 (Aug 2025)**, **CIS v8.1**, **COBIT 2019** (COBIT 7 announced by ISACA for 27 Oct 2026), **CSF 2.0**; re-verify before quoting control counts.

## Pairs with

- `load_skill control-mapping`, `load_skill gap-analysis`, `load_skill risk-assessment`, `load_skill iso27001`, `load_skill nist-csf`, `load_skill choosing-a-framework`.
