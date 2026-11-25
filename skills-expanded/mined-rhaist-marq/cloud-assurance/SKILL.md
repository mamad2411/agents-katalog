---
name: cloud-assurance
description: Covers cloud assurance regimes providers attest to and buyers ask for (CSA STAR levels with CCM v4.1/CAIQ and STAR for AI, BSI C5:2020→C5:2026, ISO/IEC 27017/27018, the stalled EUCS scheme, FedRAMP's 20x transition) and how to read a provider's attestation package versus a SOC 2. Use when the user asks about CSA STAR, CCM, CAIQ, C5, EUCS or FedRAMP, or is assessing a cloud provider's assurance evidence.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Cloud assurance: what providers attest to, and how to read it

A cloud buyer cannot audit AWS, Azure or a SaaS vendor directly, so assurance arrives as **third-party reports and certificates** the provider publishes (trust portals, the STAR Registry, the FedRAMP Marketplace). Your job is to check that the report **covers the service, region and period you actually use**, at the **assurance level** your obligation needs, and to pick up the **controls it hands back to you**. Architecture side: `load_skill cloud-security`. SOC 2 mechanics: `load_skill soc2`. Dates checked Nov 2026.

## The regimes at a glance

| Regime                    | Owner                    | What it is                                                                    | Assurance type                                | Who asks for it                                   |
| ------------------------- | ------------------------ | ----------------------------------------------------------------------------- | --------------------------------------------- | ------------------------------------------------- |
| **CSA STAR L1**           | Cloud Security Alliance  | CAIQ self-assessment against CCM                                              | **None** (self-declared; optional AI scoring) | Vendor questionnaires, first-pass TPRM            |
| **CSA STAR L2**           | CSA + accredited auditor | ISO 27001 + CCM (Certification) or SOC 2 + CCM (Attestation); C-STAR in China | Third-party                                   | Enterprise buyers wanting cloud-specific coverage |
| **SOC 2 Type II**         | AICPA / CPA firm         | Attestation on TSC over a period                                              | Reasonable assurance, with exceptions listed  | US/global default                                 |
| **BSI C5**                | BSI (Germany)            | Criteria catalogue, ISAE 3000 attestation                                     | Type 1 (design) / Type 2 (period)             | German public sector, German health, DACH buyers  |
| **ISO/IEC 27017 / 27018** | ISO/IEC                  | Cloud control guidance / PII-processor code                                   | Audited within an ISO 27001 certificate scope | Global procurement, GDPR processor diligence      |
| **FedRAMP**               | GSA FedRAMP PMO          | US federal cloud authorization/certification                                  | 3PAO assessment + continuous monitoring       | US federal agencies; DoD CUI (via equivalency)    |
| **EUCS**                  | ENISA / Commission       | EU certification scheme (Basic/Substantial/High)                              | **Not adopted**: nothing to certify against   | (eventually) EU public sector, NIS2/DORA evidence |
| National schemes          | ANSSI, CCN, ACN…         | SecNumCloud (FR), ENS (ES), ACN qualification (IT)                            | Qualification/certification                   | That country's public sector / sensitive data     |

## CSA STAR, CCM and CAIQ

- **CCM v4.1** released **28 Jan 2026** (succeeding v4.0.13); 17 domains, each control mapped to ISO 27001/27002, NIST 800-53, PCI, etc., and tagged with **shared-security-responsibility (SSRM)** ownership (the most useful column for a buyer). **CAIQ v4.1** is the question set. STAR accepts v4.0 or v4.1 submissions from Mar 2026; **only v4.1 from Dec 2027** (v4.0.x withdrawn). verify: https://cloudsecurityalliance.org/blog/2026/02/19/ccm-v4-1-transition-timeline
- **Level 1** = a CAIQ posted to the Registry. It is a **marketing artefact, not assurance**; treat it as a structured questionnaire answer. CSA's "Valid-AI-ted" scoring grades consistency of answers, not truth.
- **Level 2** = **STAR Certification** (ISO 27001 certification body extends the audit to CCM, with a maturity score) or **STAR Attestation** (CPA firm adds CCM criteria to a SOC 2) or **C-STAR** (China, GB/T 22239-based). Ask which one; they have different opinion formats.
- **STAR for AI**: Level 1 (AI-CAIQ, Oct 2025) and **Level 2 launched 27 Oct 2026** (ISO/IEC 42001 and/or 27001 + the **AI Controls Matrix**, or a SOC 2-based attestation; AICM v1.1 Jun 2026). Relevant when the service is an AI platform; pair with `load_skill ai-security`, `load_skill eu-ai-act`.

## BSI C5

- **C5:2020** (121 criteria, 17 areas) remains the operative catalogue. **C5:2026** (v1.0.1; **168 criteria**, 17 areas; adds container management, supply chain, post-quantum crypto, confidential computing, deeper multi-tenancy and sovereignty) applies to **Type 1 reports dated on/after 1 Jun 2027 and Type 2 periods beginning on/after 1 Jun 2027**; early adoption allowed, **no mixing** versions within one period. verify: https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Empfehlungen-nach-Angriffszielen/Cloud-Computing/Kriterienkatalog-C5/kriterienkatalog-c5_node.html
- Structure: **basic vs additional criteria**, **complementary customer criteria** (C5's CUECs), and the disclosed **"surrounding parameters"**: data location, jurisdiction and government-access powers, certifications held. Those parameters are why sovereignty-sensitive buyers prefer C5 over SOC 2.
- German demand drivers: the BSI minimum standard for federal use of external cloud, and the health-sector requirement (SGB V §393) for C5 attestations when cloud processes health/social data; verify current transition terms.

## ISO/IEC 27017:2026 and 27018:2025

- **27017** = cloud-specific guidance on 27002 controls plus cloud-only controls (shared roles, VM segregation, admin operations, customer monitoring), for **both** CSP and customer. **27018** = code of practice for **public-cloud PII processors** (processor-side GDPR-ish duties: purpose limitation, sub-processor disclosure, return/deletion, breach notice to customer). See `load_skill iso27001`.
- Neither is a standalone management-system certificate: they're **assessed inside a 27001 certificate** and appear in the SoA/certificate scope. Check the **certificate scope statement** names the service you buy: "corporate IT, London office" is not the platform.
- For privacy management use **ISO/IEC 27701:2025** (standalone since 2025).

## EUCS: status

- Drafted by ENISA since 2020; **still not adopted as of Nov 2026**. It stalled on **sovereignty/immunity-from-foreign-law** requirements for the "High" level (France pushed SecNumCloud-style rules, others resisted). The Commission says work will **resume** under the **revised Cybersecurity Act** proposal (20 Jan 2026) with sovereignty gaps to be filled by the planned **Cloud and AI Development Act** (verify whether proposed). verify: https://digital-strategy.ec.europa.eu/en/policies/cloud-computing
- Practical answer when a buyer asks "are you EUCS certified?": nobody is. Offer C5 / SecNumCloud / ISO 27001+27017/27018 / SOC 2 and map them to the NIS2 Art. 21 supply-chain and DORA third-party evidence they need (`load_skill nis2-dora`).

## FedRAMP (summary; detail in `load_skill us-sectoral-regs`)

- Under the **Consolidated Rules for 2026** (mandatory for all stakeholders **1 Jan 2027**, with area-specific dates; existing providers must follow them over the following year to keep certification) FedRAMP certifies by **Class A to D**, from minimal to significant assurance: **20x** applications opened 3 Aug 2026 (Class A) and 31 Aug 2026 (B/C); a temporary Rev5 pipeline for B/C opened 10 Aug 2026; **no new Rev5 certifications after 11 Jun 2027**. verify: https://www.fedramp.gov/2026/timeline/ and https://www.fedramp.gov/2026/definitions/
- 20x leans on **machine-readable, automated validation** (key security indicators, OSCAL) rather than narrative SSPs (`load_skill grc-automation`).
- DoD contractors: a CSP holding CUI must be FedRAMP Moderate (or DoD-defined equivalent) (`load_skill cmmc-800-171`).

## Reading a provider's attestation package vs a SOC 2

Read every report against the same seven questions; a "yes, we have X" answers none of them.

1. **What exactly is in scope?** Service names, regions, data centres, and whether the product/tier you buy is listed. Hyperscalers scope per service; a new service may be absent for a cycle.
2. **What assurance level?** Self-declared (STAR L1, CAIQ) < certification (ISO, STAR Certification: "a management system exists") < attestation with tested controls over a period (SOC 2 Type II, C5 Type 2, FedRAMP).
3. **Point in time or period, and how stale?** Type 1/Type I = design only. Check period end vs today; ask for a **bridge letter** (management assertion, not auditor assurance).
4. **What's the opinion and what are the exceptions?** SOC 2 and C5 list deviations; ISO certificates hide nonconformities (ask for the surveillance summary under NDA if it matters).
5. **What is handed back to you?** CUECs (SOC 2), complementary customer criteria (C5), SSRM "customer-owned" CCM rows, FedRAMP customer responsibility matrix. These are **your** controls: import them into your control set (`load_skill control-mapping`).
6. **Who else is underneath?** Subservice organisations carved out (the SaaS on top of a hyperscaler); you need _their_ report too.
7. **Does it meet your obligation?** DORA register-of-information and NIS2 supply-chain duties need contractual audit/access rights as well as reports; German public sector wants C5; US federal wants FedRAMP; GDPR processor diligence fits 27018 + DPA (`load_skill legal-contractual`).

## Common pitfalls

- Accepting a CAIQ or STAR L1 as evidence of controls.
- ISO certificate scoped to the vendor's HQ, not the service.
- Ignoring CUECs (the most common root of "the vendor's report was clean but we were breached").
- Asking every provider for every scheme; tier vendors and ask for the one report that matches the risk (`load_skill third-party-risk`).
- Citing C5:2026 as required today (it's 1 Jun 2027) or EUCS as existing.

## Pairs with

`load_skill soc2`, `load_skill iso27001`, `load_skill third-party-risk`, `load_skill cloud-security`, `load_skill us-sectoral-regs`, `load_skill nis2-dora`, `load_skill compliance-audit`.
