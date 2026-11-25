---
name: cmmc-800-171
description: Covers assessor-level NIST SP 800-171 and CMMC, including Rev 2 vs Rev 3 and which one CMMC L2 assesses, SP 800-171A objectives, the DoD scoring methodology and SPRS, CMMC POA&M rules and the 180-day closeout, affirmations, L1/L2/L3 scope, CUI asset categories and enclaves, and the current (suspended) CMMC phase state. Use when the user handles CUI, supplies the US DoD, or asks about CMMC levels, SPRS scores, POA&Ms or 800-171 assessment scope.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# NIST SP 800-171 & CMMC: the assessor's view (practitioner orientation, NOT legal advice)

**800-171** is the requirement set for CUI on non-federal systems; **DFARS 252.204-7012** makes it a DoD contract obligation; **CMMC** (32 CFR 170 + DFARS 252.204-7021) is the **verification** layer on top. The regime map, the CMMC phase timeline and the July 2026 suspension live in `load_skill us-sectoral-regs`; this skill does not restate them differently. Re-verify phase state before every engagement.

## Which revision you assess against

| Document                                    | Shape                                                    | Status for DoD work                                                                                                                                              |
| ------------------------------------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SP 800-171 Rev 2** (2020)                 | **110 requirements, 14 families**                        | **What 7012 and CMMC L2 require**: locked by class deviation 2024-O0013 (Rev 1, 22 May 2024) "until rescinded"; 32 CFR 170 incorporates Rev 2 by reference       |
| **SP 800-171A** (Jun 2018)                  | **320 assessment objectives** (determination statements) | The CMMC L2 assessment procedure                                                                                                                                 |
| SP 800-171 Rev 3 (May 2024)                 | 97 requirements, 17 families (adds PL, SA, SR), **ODPs** | Final at NIST; DoD will adopt **only by future rulemaking**; none found as of Nov 2026. DoD published its own ODP values (Apr 2025) for voluntary early adopters |
| SP 800-171A Rev 3 (May 2024)                | Rev 3 assessment procedures                              | Not used for CMMC                                                                                                                                                |
| SP 800-172 (Feb 2021)                       | Enhanced requirements                                    | **CMMC L3 = 24 selected requirements** with DoD parameters                                                                                                       |
| SP 800-172 Rev 3 / 172A Rev 3 (13 May 2026) | Enhanced requirements, new edition                       | NIST withdrew the 2021 text, but CMMC L3 references the 2021 version until DoD amends the rule (verify)                                                          |

verify: https://csrc.nist.gov/projects/protecting-controlled-unclassified-information and https://dodcio.defense.gov/cmmc/

- **Never score a DoD contractor against Rev 3.** If a client built to Rev 3, map back: Rev 3 merged or withdrew some Rev 2 requirements, so evidence often misses Rev 2 objectives. Civilian agencies are different: the proposed FAR CUI rule would use Rev 3 (`load_skill us-sectoral-regs`).
- A requirement is **MET only if every one of its 800-171A objectives is MET**. Assessors test with **examine / interview / test**; one method rarely suffices for a technical requirement.

## Levels and scope

| Level                                  | Requirements                     | Who assesses                                 | Cadence                                | POA&M?          |
| -------------------------------------- | -------------------------------- | -------------------------------------------- | -------------------------------------- | --------------- |
| **L1** (FCI)                           | 15 requirements = FAR 52.204-21  | Self                                         | Annual self-assessment + affirmation   | **No**: all MET |
| **L2** (CUI)                           | 110 requirements (800-171 Rev 2) | Self **or** C3PAO, per the contract          | Every 3 years + **annual affirmation** | Limited (below) |
| **L3** (CUI, high-priority programmes) | L2 + 24 from 800-172             | DCMA **DIBCAC** (needs L2 C3PAO Final first) | Every 3 years + annual affirmation     | Limited         |

**CUI asset categories (32 CFR 170.19)**. The scoping decision drives cost more than any control:

- **CUI assets**: process, store or transmit CUI. Fully assessed.
- **Security Protection Assets (SPA)**: provide security to the CUI environment (IdP, SIEM, EDR console, jump hosts, the MSP/MSSP's tools). In scope and assessed against relevant requirements, **even if they never touch CUI**.
- **Contractor Risk Managed Assets (CRMA)**: _can_ but aren't intended to handle CUI, controlled by policy. Documented in the SSP; not assessed beyond a check unless documentation is inadequate. **At L3 they become CUI assets.**
- **Specialized assets**: IoT/IIoT, OT, GFE, restricted IS, test equipment. Documented in the SSP (with how they're managed); not assessed against all requirements at L2.
- **Out-of-scope**: physically or logically separated and cannot handle CUI. Prove the separation.
- **External service providers:** a **CSP** that stores/processes/transmits CUI must be **FedRAMP Moderate authorized or meet DoD's FedRAMP Moderate equivalency** (DoD CIO memo, Dec 2023) and accept 7012(c) to (g). A non-CSP ESP (MSP/MSSP) is assessed as part of your SPAs; if it handles CUI itself, check its own CMMC status requirement in 170.19 (verify). Get the provider's **customer responsibility matrix**; its rows become your evidence.

**Enclaves:** a CUI enclave (GCC High tenant, VDI, segmented network) shrinks the CUI-asset count, but SPAs serving it stay in scope and the boundary must hold. Leak paths assessors find: email forwarding and Teams/OneDrive sync out of the enclave, print/scan, backups, admin workstations shared with corporate IT, CUI in ticketing systems. Draw the data flow first (`load_skill network-segmentation`, `load_skill data-security`).

## DoD Assessment Methodology and SPRS

- **DFARS 252.204-7019/-7020** require a current (≤3 years) **NIST SP 800-171 DoD Assessment** score in **SPRS** to be considered for award: **Basic** (self, low confidence), **Medium** (DIBCAC document review), **High** (DIBCAC on-site). verify: https://www.sprs.csd.disa.mil/
- **Scoring:** start at **110**, subtract **5, 3 or 1** per unmet requirement by weight; floor **−203**. Partial credit only for **3.5.3 MFA** (−3 instead of −5 if MFA covers remote and privileged but not all users) and **3.13.11 FIPS crypto** (−3 instead of −5 if encryption is used but not FIPS-validated). The SSP itself (**3.12.4**) has no score because without it there is no assessment.
- SPRS entry fields: score, assessment date, scope (CAGE codes), **SSP name/version/date**, and **POA&M completion date** (when 110 will be reached). A self-score of 110 with open gaps is the classic **False Claims Act** fact pattern (DOJ Civil Cyber-Fraud Initiative).
- **CMMC scoring** (170.24) uses the same weights; **N/A counts as MET**; a documented temporary deficiency under an **operational plan of action** (3.12.2) can be MET. Don't confuse that with a POA&M.

## POA&M rules under CMMC (32 CFR 170.21)

- **L1: no POA&M at all.**
- **L2 Conditional status** needs a score **≥ 88/110 (80%)**, and every POA&M item must be a **1-point requirement**, except **3.13.11** where encryption exists but isn't FIPS-validated. **Never allowed on a POA&M:** 3.1.20 (external connections), 3.1.22 (public content), **3.12.4 (SSP)**, 3.10.3/3.10.4/3.10.5 (escorting, physical-access logs, physical-access devices).
- **L3 Conditional** needs ≥80% of the L3 requirements, with a short list of 800-172 requirements barred from the POA&M (check 170.21(a)(3)).
- **180 days** from Conditional status to close every item and pass a **POA&M closeout assessment** (by the same type of assessor). Miss it and Conditional status **expires**; contract remedies follow. Conditional → **Final** only on closeout.
- Under plain 7012/7020 (no CMMC), any requirement may be "not yet implemented" with a planned date; CMMC is far stricter, which is the most common client misunderstanding.

## Affirmations (32 CFR 170.22)

- A senior **Affirming Official** affirms **continuing compliance** in SPRS: after **each** assessment (self, C3PAO or DIBCAC), **annually** thereafter, and after **POA&M closeout**. Lapse = status lapses. The affirmation is the personal-accountability hook; brief the signer on what they are attesting, with evidence.

## Current phase state (from `load_skill us-sectoral-regs`: verify there)

- **Phase 1 (since 10 Nov 2025)** is in force: L1/L2 **self-assessment**, SPRS posting, annual affirmation, flowdown to subcontractors handling FCI/CUI.
- **Phase 2 (L2 C3PAO, was 10 Nov 2026) is suspended** (13 Jul 2026); **class deviation 2026-O0025 Rev 3 (3 Sep 2026)** has COs remove L2 C3PAO / L3 requirements from active solicitations and contracts. 32 CFR 170 and DFARS 252.204-7021 are unchanged, so **don't stand down**, and expect the C3PAO requirement to return. Phases 3 to 4 suspended too.
- **7012** still requires 800-171 Rev 2, **72h** incident reporting to DC3 via DIBNet (medium-assurance certificate), 90-day image preservation, and malware submission (independent of CMMC).

## Assessment-readiness checklist

1. CUI identified and marked; data-flow diagram; **FCI vs CUI** boundary written down.
2. Asset inventory tagged with the 170.19 categories; SSP describes every boundary, SPA, CRMA and specialized asset.
3. ESP/CSP evidence: FedRAMP package or equivalency body of evidence + CRM.
4. Evidence per **objective**, not per requirement (`load_skill compliance-audit`, `load_skill gap-analysis`).
5. Honest SPRS score; POA&M within the 170.21 limits; affirming official briefed.

## Pairs with

`load_skill us-sectoral-regs` (phase state, FedRAMP, FAR CUI), `load_skill control-frameworks` (800-53 lineage), `load_skill cloud-assurance` (FedRAMP/CSP evidence), `load_skill control-mapping`, `load_skill third-party-risk` (subcontractor flowdown), `load_skill incident-response-leadership` (the 72h DC3 clock).
