---
name: healthcare-core
description: "Shared reference for the healthcare cluster: the three-layer data-protection contract (classify → access-control → audit), the patient-safety bias (alerts block, never silently pass), the alert-severity matrix, and the CRITICAL-vs-HIGH deploy-gate thresholds. USE WHEN handling PHI, designing clinical access control, wiring a CDSS alert, or configuring a safety gate — the interlocking rules every healthcare spoke shares."
cluster: healthcare
version: 1.0.0
---

# Healthcare Core

Shared model for the `healthcare` cluster. The privacy, EMR, CDSS, and eval spokes all depend on
these interlocking concepts — keep them consistent here so no spoke contradicts another.

## 1. The data-protection contract (this cluster's defining model)

Every healthcare app turns on one three-layer contract. Treat data as protected by default:

```
Classify (what is sensitive) ──> Access-control (who may see it) ──> Audit (who did see it)
```

- **Classify** — *PHI* is anything that identifies a patient **and** relates to health
  (name, DOB, address, national ID, MRN, diagnosis, meds, labs, imaging, claims, admissions).
  *PII* is non-patient sensitive data (staff details, doctor payouts, salaries, vendor payments).
  Tag PHI/PII columns at the schema level. → `healthcare-phi-compliance`
- **Access-control** — Row-Level Security scoped to facility/role; the **anon/publishable** key
  on the client, never `service_role`; minimum-necessary slice only. → `healthcare-phi-compliance`
- **Audit** — every PHI create/read/update/delete/print/export is logged to an **insert-only,
  tamper-proof** trail (no update, no delete). → `healthcare-phi-compliance`

**Rule:** grant the **narrowest** access that works; prefer opaque UUIDs over names/MRNs/IDs;
treat any new data path (vendor, LLM, analytics, export) as a privacy change worth stating.

## 2. The patient-safety bias (defaults fail safe)

Clinical software is patient-safety critical, so the safe default is **block, not pass**:

- A **critical** drug interaction **blocks** prescribing; the clinician must document an override
  reason (stored in the audit trail). → `healthcare-cdss-patterns`, `healthcare-emr-patterns`
- A mg/kg dose with **missing weight** returns invalid — it never silently passes.
- Critical alerts are **non-dismissable modals**, never toasts; abnormal values are always flagged.
- Signed encounters are **locked** — corrections are addenda (linked records), never edits.

## 3. Alert-severity matrix (shared by CDSS and EMR)

| Severity | UI behavior | Clinician action |
|---|---|---|
| Critical | Block action. Non-dismissable modal. Red. | Must document override reason to proceed |
| Major | Inline warning banner. Orange. | Must acknowledge before proceeding |
| Minor | Inline info note. Yellow. | Awareness only |

CDSS produces these; the EMR renders them; the eval harness asserts they never regress.

## 4. The deploy-gate thresholds (shared by eval + CI)

Five eval categories, two tiers. A single CRITICAL failure blocks the deploy.

| Category | Tier | Threshold | On failure |
|---|---|---|---|
| CDSS Accuracy | CRITICAL | 100% | **Block deploy** |
| PHI Exposure | CRITICAL | 100% | **Block deploy** |
| Data Integrity | CRITICAL | 100% | **Block deploy** |
| Clinical Workflow | HIGH | 95%+ | Warn, allow with review |
| Integration (HL7/FHIR) | HIGH | 95%+ | Warn, allow with review |

CRITICAL suites run with `--bail`; never lower a CRITICAL threshold to get green.
→ `healthcare-eval-harness`

## 5. Jurisdiction / standards matrix

| Concern | Standard(s) | Notes |
|---|---|---|
| Privacy regime | HIPAA (US), DISHA (India), GDPR (EU) | `healthcare-phi-compliance` covers all three; US adds BAAs / covered-entity gates |
| Diagnosis coding | ICD-10, SNOMED CT | Diagnosis search in the encounter flow → `healthcare-emr-patterns` |
| Clinical scoring | NEWS2 (RCP spec), qSOFA, APACHE, GCS | Tables must match the published spec exactly → `healthcare-cdss-patterns` |
| Interop | HL7 v2.x, FHIR | Integration-compliance eval gate → `healthcare-eval-harness` |
| Accessibility | WCAG AA (4.5:1), 44×44px targets | No color-only indicators; keyboard-first → `healthcare-emr-patterns` |

## 6. Conventions

- CDSS is a **pure, side-effect-free function library** — input clinical data, output alerts;
  fully testable, no `any` types, errors surface loudly (never silently caught).
- Interaction pairs are **bidirectional** (A↔B) and live in a maintainable data structure,
  not hardcoded inline.
- Test runner is illustrative (examples use Jest); thresholds and categories are
  framework-agnostic (Vitest, pytest, PHPUnit all fine).

## 7. Shared guardrails

- **Protect-by-default**: classify → restrict → audit; minimum-necessary; opaque UUIDs.
- **No PHI** in logs, error strings, URLs, browser storage, screenshots, or LLM prompts.
- **Fail safe**: critical alert blocks; missing weight blocks; signed encounter locks.
- Critical clinical alerts are non-dismissable — never toasts; override reasons are audited.
- Third-party SaaS / LLM / observability vendors are blocked-by-default until the data boundary
  (and a BAA, under HIPAA) is established.
- A single CRITICAL eval failure blocks the deploy; don't weaken the gate.
