---
name: healthcare-orchestrator
description: "Route a healthcare-software task to the right skill among four clinical specialists — PHI/PII privacy & access control, EMR/EHR encounter workflows, the CDSS safety engine (drug interactions, dose, NEWS2), and the patient-safety eval harness that gates deploys. USE WHEN building, reviewing, or shipping a clinical/health app but the specific concern (privacy vs. workflow vs. decision-support vs. release gate) hasn't been named."
cluster: healthcare
version: 1.0.0
---

# Healthcare Orchestrator

The single entry skill for healthcare-software work. It locates the task on the **lifecycle ×
concern** map and delegates to one of four specialist spokes. The cross-cutting model every
clinical app shares — the three-layer data-protection contract (classify → control access →
audit), the patient-safety bias (alerts block, never silently pass), and the CRITICAL-vs-HIGH
gate thresholds — lives in `healthcare-core`; read it before designing data access, wiring a
CDSS alert, or configuring a deploy gate.

## Cluster map

- **`healthcare-phi-compliance`** — the data-protection implementation core: PHI/PII
  classification, Row-Level Security, audit trails, encryption, and the common leak vectors
  (logs, URLs, browser storage, service keys). Multi-jurisdiction: HIPAA (US), DISHA (India),
  GDPR (EU).
- **`healthcare-emr-patterns`** — EMR/EHR build patterns: the single-page encounter flow,
  smart clinical templates, the locked-encounter + addendum model, prescription PDFs, and
  accessibility-first medical UI.
- **`healthcare-cdss-patterns`** — the Clinical Decision Support engine as a pure,
  side-effect-free function library: drug-interaction checking (bidirectional), weight/age/renal
  dose validation, clinical scoring (NEWS2, qSOFA), and alert-severity → UI behavior.
- **`healthcare-eval-harness`** — the patient-safety verification gate: five test categories,
  three CRITICAL (100%, block deploy) + two HIGH (95%+, warn), wired into CI/CD.

## Routing rules by intent

**Privacy, access, and data exposure**
- "Is this PHI? can we log/send/store it?" → `healthcare-phi-compliance`
- RLS / multi-facility isolation / audit-trail schema → `healthcare-phi-compliance`
- Vendor / LLM-provider / analytics data path → `healthcare-phi-compliance` *(model in `healthcare-core`)*

**Building the clinical app (EMR/EHR)**
- Encounter workflow, templates, locked notes, prescription UI → `healthcare-emr-patterns`
- Accessible medical data-entry UI → `healthcare-emr-patterns`

**Clinical decision support (patient-safety logic)**
- Drug-interaction / dose-validation / clinical-scoring logic → `healthcare-cdss-patterns`
- Alert severity → block/acknowledge/inform UI behavior → `healthcare-cdss-patterns` *(consumed by `healthcare-emr-patterns`)*

**Shipping safely**
- Pre-deploy safety gate / CI thresholds / eval report → `healthcare-eval-harness`

## Standard flow

1. Locate the task: which lifecycle stage (protect data → build workflow → wire decision-support
   → gate the deploy) and which concern.
2. If it touches **PHI handling, audit, alert-severity behavior, or deploy thresholds**, pull the
   model from `healthcare-core` first — these are interlocking, not independent.
3. Delegate to the spoke(s). Multi-step asks fan out in lifecycle order — e.g. "add AI visit
   summaries to a clinician dashboard" → `healthcare-phi-compliance` (PHI/prompt/vendor boundary)
   → `healthcare-emr-patterns` (where it renders) → `healthcare-cdss-patterns` (if it influences a
   decision) → `healthcare-eval-harness` (gate before ship).
4. Return: chosen spoke(s), the PHI/audit and patient-safety implications, the jurisdiction(s) in
   play, and the next action.

## Guardrails

See `healthcare-core`. In short: **patient safety and minimum-necessary access are
non-negotiable** — a critical CDSS alert blocks the action (never a dismissable toast), a
missing weight blocks a mg/kg dose (never passes), and PHI never lands in logs, URLs, browser
storage, prompts, or client-visible errors. Treat any third-party SaaS / LLM / observability
vendor as blocked-by-default until its data boundary (and BAA, for US) is clear. A single
CRITICAL eval failure blocks the deploy — don't lower the threshold to get green.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
