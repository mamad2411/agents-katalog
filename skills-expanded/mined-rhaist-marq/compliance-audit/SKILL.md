---
name: compliance-audit
description: Guides running a compliance audit or assessment as a process, covering audit types, control-testing methods, evidence collection, the Statement of Applicability, audit readiness, internal vs external/certification audits, and managing findings via corrective action plans. Use when the user is preparing for an ISO 27001, SOC 2 or other audit, conducting an internal audit, building an SoA, or handling nonconformities.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Compliance audit (the process)

Framework-agnostic mechanics of running or surviving an audit. For the frameworks
themselves load the standard: `load_skill iso27001`, `load_skill pci-dss`, `load_skill nist-csf`.
Audit-method standards: ISO 19011:2026 (any management-system audit; the 2026 edition
superseded 2018; a technical revision folding in remote/hybrid audits, digital-evidence
reliability, and supply-chain scope), ISO/IEC 27007 (ISMS-specific audit guidance layered
on 19011), ISO/IEC 27006-1 (accreditation rules for certification bodies). SOC 2 = AICPA
attestation, not certification.

## Audit types: know which you're in

| Type                                     | Who runs it         | Output                | Use it for                            |
| ---------------------------------------- | ------------------- | --------------------- | ------------------------------------- |
| **Internal (1st-party)**                 | Your own staff/team | Internal report, CAPs | Readiness, continual improvement      |
| **2nd-party**                            | A customer/partner  | Their risk decision   | Vendor due diligence (you're audited) |
| **External / certification (3rd-party)** | Accredited body     | Certificate / opinion | ISO 27001 cert, SOC 2 report          |

ISO 27001 cert runs in two stages: **Stage 1** (documentation/readiness review) then
**Stage 2** (implementation effectiveness), with **annual surveillance** and recert at
year 3. SOC 2 **Type I** = design at a point in time; **Type II** = operating effectiveness
over a period (3 to 12 months). Type II is what customers actually want.

## Control testing methods (auditors use all four; inquiry alone is never enough)

| Method            | Auditor does                          | Evidence strength | Proves                   |
| ----------------- | ------------------------------------- | ----------------- | ------------------------ |
| **Inquiry**       | Asks staff how the control works      | Weakest           | The "how" (claim)        |
| **Observation**   | Watches the control performed         | Moderate          | The "is" (point-in-time) |
| **Inspection**    | Examines records/config/tickets       | Strong            | The "what" (artifact)    |
| **Reperformance** | Re-executes the control independently | Strongest         | The "works"              |

AICPA guidance: inquiry must be corroborated: pair it with inspection or reperformance.
For operating-effectiveness (Type II / surveillance), auditors **sample** over the period;
keep evidence dated and complete across the whole window, not just audit week.

## Evidence collection

- Map every control to its **evidence artifact** up front: policy doc, config screenshot,
  ticket, log export, approval record, training record. One control → named artifact(s).
- Evidence must be **attributable, dated, complete, and within the audit period**. A
  screenshot with no timestamp/system context is weak. Prefer system-generated exports.
- Keep a single **evidence index** (control ID → artifact path → date → owner). Store under
  `/work`; `write_file /work/evidence-index.md` and reference paths so re-audits diff cleanly.
- Don't fabricate or back-date. A gap honestly logged with a CAP beats a faked artifact:
  the latter voids the engagement and is fraud.

## Statement of Applicability (SoA): ISO 27001's spine

The SoA lists **every** Annex A control with: applicable yes/no, justification, implementation
status, and reference to the control's evidence. It's the auditor's index and the first
thing Stage 1 checks. An exclusion needs a real justification (not "too hard"). Other
frameworks have analogues (PCI ROC scope, SOC 2 control matrix); same idea: declared scope

- control-to-evidence mapping. To avoid mapping the same evidence across frameworks,
  `load_skill control-mapping`.

## Audit readiness checklist

- Scope agreed and documented (systems, locations, period); nothing in-scope undocumented.
- SoA / control matrix current; every control has an owner and named evidence.
- Run an **internal audit first**: find your own nonconformities before the assessor does.
- Prior-audit findings/CAPs closed with evidence (open prior findings are the fastest fail).
- Evidence index complete for the **full period**, not a snapshot.
- Staff briefed: answer the question asked, don't volunteer scope, don't guess; "I'll get
  the evidence" beats improvising. (`load_skill gap-analysis` to triage gaps pre-audit.)

## Findings & corrective action plans (CAPs)

Finding severity (terminology varies by scheme; confirm the assessor's):

| Grade                   | Meaning                                | Effect                                   |
| ----------------------- | -------------------------------------- | ---------------------------------------- |
| **Major nonconformity** | Control absent or systemically failing | Blocks certification until closed        |
| **Minor nonconformity** | Isolated lapse; control mostly works   | CAP required; usually doesn't block cert |
| **Observation / OFI**   | Opportunity for improvement            | Advisory; track but not mandatory        |

Each CAP carries: finding ref, **root cause** (not just the symptom: 5-whys), correction
(fix the instance), **corrective action** (fix the cause so it can't recur), owner, due date,
and verification evidence. Majors need a containment/correction date fast; the assessor
re-verifies before issuing the cert. Track CAPs in one register and review at the security
steering committee (`load_skill security-governance`).

## Tie into marq

- `read_file /work/findings.md` is audit evidence of control _effectiveness_
  (recorded OSINT exposures, or pentest/vuln results staged in `/work`): confirmed findings often map directly to nonconformities.
- Push audit findings/CAPs through `report_finding` so compliance and technical findings land
  in one `render_report` deliverable instead of two parallel trackers.

## Pairs with

- Pre-audit gap triage: `load_skill gap-analysis`.
- Cross-framework evidence reuse: `load_skill control-mapping`.
- The frameworks being audited: `load_skill iso27001`, `load_skill pci-dss`, `load_skill nist-csf`.
