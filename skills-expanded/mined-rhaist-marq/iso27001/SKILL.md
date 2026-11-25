---
name: iso27001
description: Covers how ISO/IEC 27001:2022 and its Annex A (93 controls in 4 themes) are structured, plus a certification implementation path; cites by clause rather than reproducing control text. Use when the user asks about ISO 27001 clauses or Annex A controls, ISMS implementation, the 2013-to-2022 transition, or how to get certified.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# ISO/IEC 27001:2022

The standard certifies an **ISMS** (information security management system): a _process_, not a checklist. You certify the management system; Annex A is the control menu it manages.

Canonical source (buy/access for exact text): ISO.org `ISO/IEC 27001:2022`. Control _implementation guidance_ lives in the companion **ISO/IEC 27002:2022** (same control numbering). Cite clauses; web-fetch when exact wording is needed.

## Structure: two halves

**Mandatory management clauses 4 to 10** (these are what an auditor certifies; you cannot exclude them):

- **4 Context**: scope of the ISMS, interested parties.
- **5 Leadership**: top-management commitment, policy, roles.
- **6 Planning**: risk assessment + risk treatment; **Statement of Applicability (SoA)**; security objectives.
- **7 Support**: resources, competence, awareness, documented info.
- **8 Operation**: run the risk assessment/treatment.
- **9 Performance evaluation**: monitoring, internal audit, management review.
- **10 Improvement**: nonconformity + corrective action, continual improvement.

**Annex A**: the reference control set you select _from_ (justify inclusions/exclusions in the SoA).

## Annex A:2022: 93 controls, 4 themes

The 2022 revision restructured the old 2013 layout (114 controls / 14 domains) into **4 themes / 93 controls**, and added **11 new controls**:

- **A.5 Organizational**: 37 controls
- **A.6 People**: 8 controls
- **A.7 Physical**: 14 controls
- **A.8 Technological**: 34 controls

New-in-2022 controls (common gap items): **threat intelligence (5.7), information security for cloud services (5.23), ICT readiness for business continuity (5.30), physical security monitoring (7.4), configuration management (8.9), information deletion (8.10), data masking (8.11), data leakage prevention (8.12), monitoring activities (8.16), web filtering (8.23), secure coding (8.28).** Each control also carries **5 attributes** (control type, infosec properties, cybersecurity concepts, operational capabilities, security domains) for filtering; verify the exact attribute taxonomy in 27002.

## Implementation path

1. **Scope (cl. 4)**: define boundaries; smaller scope = faster first cert.
2. **Risk assessment + treatment (cl. 6)**: identify risks, choose treatment, select Annex A controls → produce the **SoA** (it lists every Annex A control with applicable/not + justification).
3. **Implement** selected controls + the mandatory clause-4 to 10 processes.
4. **Operate** long enough to generate evidence (internal audit + at least one management review).
5. **Certification audit** by an accredited body: **Stage 1** (documentation/readiness) then **Stage 2** (implementation effectiveness).
6. **3-year cycle**: certificate valid 3 years, **annual surveillance audits**, recertification at year 3.

## Notes

- The **2013→2022 transition deadline was 31 Oct 2025**: certs must be on :2022 now (verify if a date matters).
- **Amendment 1:2024 (climate action)** added a sentence to **cl. 4.1** ("the organization shall determine whether climate change is a relevant issue") and a note to **cl. 4.2** (interested parties may have climate-related requirements). No Annex A change, but it's now part of the certifiable clauses: auditors expect to see you've considered and documented it.
- ISO 27001 is **certifiable**; ISO 27002 is **not** (guidance only).
- Annex A is a _reference set you tailor_, not a mandate to implement all 93, but every exclusion must be justified in the SoA.
- Sector add-ons: ISO 27017:2026 (cloud), 27018:2025 (PII in cloud), 27701:2025 (privacy/PIMS for GDPR alignment; **standalone** since the 2025 edition, no longer a 27001 extension).

## Pairs with

- Gap assessment against clauses + Annex A: `load_skill gap-analysis`.
- Mapping Annex A to SOC 2 / CSF / 800-53 to avoid duplicate work: `load_skill control-mapping`.
