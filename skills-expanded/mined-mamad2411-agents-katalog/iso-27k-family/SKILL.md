---
name: iso-27k-family
description: The ISO/IEC 27000 family as it applies to this product — 27001:2022 ISMS requirements, 27002:2022 controls, the new standalone 27701:2025 privacy management standard, and 27017/27018 for cloud. Use for ISMS gap analysis, certification readiness, or when mapping controls across frameworks.
---

# ISO/IEC 27000 family

Registry: `ISO-27001`, `ISO-27002`, `ISO-27701`, `ISO-27017`, `ISO-27018`.

All are paid standards; `iso.org` blocks automated fetch. Buy them and file the PDFs in
`compliance/sources/pdfs/standards/`. Do not audit against a blog's summary of a control.

## Current state — August 2026

| Standard | Version | Note |
|---|---|---|
| ISO/IEC 27001 | **2022** + Amd 1:2024 (climate action) | 2013→2022 transition closed **31 Oct 2025**; every live certificate is 2022 |
| ISO/IEC 27002 | **2022** | 93 controls in 4 themes — this is the control text to cite |
| ISO/IEC 27701 | **2025**, published 14 Oct 2025 | **Now a standalone standard** — no longer requires 27001/27002 first. Three-year transition to **Oct 2028** |
| ISO/IEC 27017 | current | Cloud security controls, provider/customer split |
| ISO/IEC 27018 | current | PII in public clouds acting as processor |

The 27701:2025 change is the one to internalise. The old model was "get 27001, then bolt on 27701".
The second edition stands alone, which makes a **privacy-first** certification path viable — worth
considering given that PDPL, not security certification, is this product's sharpest exposure.

## What certification actually requires

ISO 27001 is a **management system** standard. The Annex A controls are the visible part; the
audit is mostly about the system around them:

| ID | Requirement | Where it lives |
|---|---|---|
| ISMS-01 | Defined scope of the ISMS | Documentation |
| ISMS-02 | Leadership commitment, policy, assigned roles | Organisational |
| ISMS-03 | Risk assessment methodology, applied and repeated | Documentation |
| ISMS-04 | Risk treatment plan and Statement of Applicability covering all 93 controls | Documentation |
| ISMS-05 | Objectives, competence, awareness, communication | Organisational |
| ISMS-06 | Documented information under control | Documentation |
| ISMS-07 | Operational planning and control | All surfaces |
| ISMS-08 | Monitoring, measurement, internal audit | Organisational |
| ISMS-09 | Management review | Organisational |
| ISMS-10 | Nonconformity, corrective action, continual improvement | Organisational |

**Most of these are not code.** A grid built only from the repo will show gaps that are documentation
gaps. Mark them clearly as `organisational` so engineering effort is not misdirected — but do not
omit them, because they are what fails an audit.

## Technical controls worth grading against the repo

From 27002:2022, the ones that bind directly to this system: access control and privileged access,
authentication, cryptography and key management, secure development lifecycle, change management,
separation of environments, logging and monitoring, backup, information deletion, data masking,
data leakage prevention, supplier relationships, and web filtering/secure coding.

## Cloud split — 27017/27018

We are a **cloud customer** (Azure) and simultaneously a **cloud service provider** to hotel
tenants. Both roles carry controls, and confusing them is a common finding:

- As Azure's customer: shared-responsibility understanding, configuration hardening, key control.
- As our tenants' provider: tenant isolation, data return and deletion at end of service,
  transparency about sub-processors and data location.

27018 maps closely onto PDPL processor duties and onto `SA-NCA-CCC` — cross-walk once, cite
separately.

## Cross-framework mapping

27002 controls map cleanly onto `SOC2-TSC` CC-criteria and onto `SA-NCA-ECC`. Build the control set
once, evidence it once, and cite three ids. That is the efficiency argument for doing ISO first —
but keep the grid citations distinct, because auditors ask for evidence in their own vocabulary.
