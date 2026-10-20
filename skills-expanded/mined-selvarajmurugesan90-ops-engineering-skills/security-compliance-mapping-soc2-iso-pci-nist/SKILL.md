---
name: security-compliance-mapping-soc2-iso-pci-nist
description: >
  Guides mapping technical controls an engineering team has already
  implemented — secrets management, IAM/least-privilege, logging and audit
  trails, encryption at rest/in transit, SAST/DAST/SCA scanning, backup and
  DR — to SOC 2 Trust Services Criteria, ISO/IEC 27001 Annex A controls,
  PCI-DSS requirements, and NIST Cybersecurity Framework (CSF) functions,
  and identifying the evidence needed to make each mapping audit-ready. Use
  when a user asks to "map our controls to SOC 2", "prepare evidence for an
  ISO 27001 audit", "which PCI-DSS requirement does our secrets rotation
  satisfy", "align our security posture to NIST CSF", "get audit-ready", or
  "build a controls matrix for our compliance team." This is a technical
  control-mapping and audit-readiness guide, not a certification process,
  legal opinion, or substitute for a qualified auditor/QSA/assessor —
  frameworks are certified or attested by accredited third parties, not by
  running this skill.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: standards-and-compliance-frameworks
  maturity: stable
---

# Security Compliance Mapping: SOC 2 / ISO 27001 / PCI-DSS / NIST CSF

## Purpose

Engineering teams frequently already operate most of the technical controls
that SOC 2, ISO/IEC 27001, PCI-DSS, and the NIST Cybersecurity Framework
(CSF) ask for — secrets management, least-privilege IAM, centralized
logging, encryption, vulnerability scanning, backup/DR — but cannot answer
"which framework requirement does this satisfy, and can we prove it operates
continuously?" when a compliance team, sales prospect's security
questionnaire, or upcoming audit asks. This skill guides mapping controls
that already exist in the engineering environment to the corresponding
criteria/controls/requirements/functions in each framework, and — more
importantly — identifying what **evidence** would demonstrate to an
independent assessor that the control operates as described, continuously,
not just that it was configured correctly once.

**This is explicitly not a certification or audit process.** SOC 2 reports
are issued by licensed CPA firms following AICPA attestation standards; ISO
27001 certification is issued by an accredited certification body following
a stage 1/stage 2 audit; PCI-DSS compliance validation (SAQ or a Report on
Compliance) is completed by the merchant/service provider or a Qualified
Security Assessor (QSA) depending on level; NIST CSF is a voluntary
risk-management framework with no certification body at all — organizations
assess and report their own maturity against it, often for a regulator,
customer, or internal governance purpose. Mapping your technical controls to
these frameworks using this skill gets an engineering organization
audit-ready and gives a compliance/legal team accurate, evidence-backed
input to work with — it does not itself produce a certification, an
attestation, legal compliance, or a guarantee of passing an audit. Always
involve qualified compliance, legal, and (where required) accredited
audit professionals for the actual certification or attestation process,
and treat control ID numbers here as commonly-cited, illustrative
references — always verify the exact current numbering against the
specific framework version your auditor is using.

## When to use

- A user asks "which SOC 2 criteria does our Vault-based secrets rotation
  satisfy" or similar for ISO 27001, PCI-DSS, or NIST CSF.
- Preparing a controls matrix or evidence package ahead of a SOC 2 Type
  II audit, an ISO 27001 certification/surveillance audit, a PCI-DSS
  assessment, or a NIST CSF maturity self-assessment.
- Responding to a customer security questionnaire that asks for framework
  alignment (e.g. "are you SOC 2 compliant," "do you meet PCI-DSS
  requirement 8," "what is your NIST CSF maturity for the Protect
  function").
- A compliance or GRC team has a framework requirement list and needs
  engineering to identify which existing technical control (and which
  specific configuration/policy/log) satisfies it.
- Identifying **gaps** — framework requirements with no corresponding
  technical control yet — so they can be prioritized as engineering work
  before an audit, not discovered during one.
- Building a repeatable, evidence-generating process (e.g. continuous
  control monitoring) rather than a one-time spreadsheet exercise that
  goes stale.

## Prerequisites & environment

- Know the exact framework, and version/scope, actually in play — e.g.
  "SOC 2 Type II, Security + Availability Trust Services Criteria,
  covering [PRODUCT] for the trailing 6 months" or "PCI-DSS v4.0, SAQ D
  for service providers" — mappings and required evidence differ
  significantly by scope and version.
- Access to the actual technical control implementations to cite as
  evidence sources: secrets manager audit logs, IAM policy/role
  definitions and access review records, centralized log
  aggregation/SIEM retention config, encryption configuration
  (KMS/TLS), SAST/DAST/SCA scan history and remediation SLAs, backup and
  DR test records.
- A named internal or external compliance owner — this skill supports
  that person/team with accurate technical mapping; it does not replace
  them. For SOC 2, the CPA firm performing the audit; for ISO 27001, the
  accredited certification body; for PCI-DSS above a certain
  transaction/merchant level, a QSA — identify who that is before
  starting, since they set the actual evidence bar.
- A controls-tracking artifact (spreadsheet, GRC tool such as Vanta,
  Drata, or a custom controls matrix) to record: framework requirement ID,
  mapped technical control, evidence source/location, evidence-collection
  frequency, and control owner.
- Familiarity with the underlying technical controls this skill maps
  from — most come from other skills in this repo (see
  Cross-references) rather than being re-explained here.

## Step-by-step guidance

1. **Confirm framework, scope, and version** with the compliance owner —
   e.g. "SOC 2 Type II / Security criteria only," "ISO 27001:2022 Annex A,"
   "PCI-DSS v4.0.1," "NIST CSF 2.0." Do not guess; requirement numbering
   and even category names have changed between versions (e.g. ISO 27001
   Annex A was substantially restructured between the 2013 and 2022
   editions; PCI-DSS v4.0 renumbered and added requirements versus v3.2.1;
   NIST CSF 2.0 added the "Govern" function versus CSF 1.1).
2. **Inventory the technical controls already implemented**, grounded in
   what actually exists (config, code, running services), not what the
   team intends to build. Pull from:
   [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md),
   [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md),
   [sast-integration](../../../devsecops/skills/sast-integration/SKILL.md),
   [dast-integration](../../../devsecops/skills/dast-integration/SKILL.md),
   [supply-chain-security-slsa-sbom](../../../devsecops/skills/supply-chain-security-slsa-sbom/SKILL.md),
   [policy-as-code-guardrails](../../../devsecops/skills/policy-as-code-guardrails/SKILL.md),
   [disaster-recovery-and-backup-strategy](../../../cloud/skills/disaster-recovery-and-backup-strategy/SKILL.md),
   [cis-benchmarks-hardening](../cis-benchmarks-hardening/SKILL.md), and
   the org's logging/monitoring stack.
3. **Map each technical control to one or more framework requirements**,
   citing the specific criteria/control/requirement ID at whatever
   precision you're confident in (see the illustrative table below) —
   flag any ID you're not fully certain of as "verify exact numbering
   against current framework text with the compliance owner/auditor"
   rather than asserting it confidently.
4. **For each mapping, identify the evidence an assessor would need**:
   not "we have a secrets manager" but "Vault audit log showing automatic
   90-day rotation executed on schedule for the last two quarters,"
   "quarterly access review sign-off records," "SAST scan results with
   remediation timestamps meeting the documented SLA." A control that
   cannot produce continuous evidence is a gap even if it's technically
   implemented.
5. **Explicitly flag gaps** — framework requirements with no mapped
   control, or a control that exists but has no evidence trail (e.g.
   access reviews happen informally over Slack with no record) — as
   engineering backlog items, prioritized with the compliance owner by
   audit timeline.
6. **Build the controls matrix** as a living artifact: framework
   requirement ID → control description → technical implementation →
   evidence source/location → collection frequency → owner → last
   verified date.
7. **Set up continuous evidence collection** where possible (automated
   log export, scheduled access-review reminders, scan result retention)
   rather than manually gathering evidence once a year right before an
   audit — auditors for SOC 2 Type II and PCI-DSS specifically test
   whether a control operated effectively **over a period of time**, not
   whether it was correctly configured on the day of the audit.
8. **Hand the matrix to the compliance owner / auditor**, framed
   explicitly as engineering's input to their process — not as a
   self-certification. Be ready to walk an assessor through how any
   given control actually works technically.
9. **Re-validate the matrix on a cadence** (e.g. before each audit cycle,
   and whenever a mapped control changes — e.g. secrets manager migration,
   new cloud account) since drift between "what the matrix says" and "what
   is actually running" is one of the most common audit findings.

## Best practices

- Cite control IDs at the precision you can verify, and explicitly note
  "verify exact numbering with current framework text/auditor" for
  anything you're not fully certain of — frameworks revise their
  numbering (PCI-DSS v3.2.1 → v4.0, ISO 27001:2013 → 2022, NIST CSF 1.1 →
  2.0) and an outdated citation undermines the whole matrix.
- Map to **evidence that proves continuous operation**, not a one-time
  screenshot — "secret rotation is configured" is not the same claim as
  "secret rotation executed successfully every 90 days for the last four
  quarters, with logged confirmations." SOC 2 Type II and PCI-DSS
  specifically test operating effectiveness over a period.
- Keep the matrix in version control or a GRC tool with change history —
  a static spreadsheet from eighteen months ago is itself an audit
  finding waiting to happen ("this control mapping doesn't reflect our
  current architecture").
- Loop in the actual compliance owner (and, for PCI-DSS at higher levels,
  the QSA) early — they determine the real evidence bar and scope; a
  technically accurate but scope-mismatched mapping wastes engineering
  effort.
- Reuse one control across multiple frameworks rather than treating each
  framework as a separate project — a single Vault rotation policy can
  simultaneously map to SOC 2 CC6.1, ISO 27001 Annex A control on
  cryptographic keys/access management, PCI-DSS requirement 8 (or
  requirement 3 aspects), and NIST CSF `PR.AA`/`PR.DS` — build the matrix
  so that overlap is visible and evidence is collected once, referenced
  many times.
- Be explicit with stakeholders, every time, that this mapping is
  audit-**preparation**, not an audit outcome — say so in the deliverable
  itself, not just verbally.

## Common pitfalls

- **Symptom:** The controls matrix lists "Secrets rotation — implemented"
  against SOC 2 CC6.1 with no evidence link, and the auditor asks for
  proof and the team scrambles.
  **Fix:** Every mapped control needs a named evidence source (log
  export, ticket system, dashboard) and a collection frequency recorded
  *before* the audit — a mapping without evidence is a claim, not a
  control.
- **Symptom:** A control is mapped once when it was first implemented,
  but the underlying system has since changed (e.g. migrated from one
  secrets manager to another, or IAM roles were restructured), and the
  matrix still describes the old system.
  **Fix:** Re-validate the matrix against the actual current
  implementation on a fixed cadence and whenever a mapped system changes
  — treat matrix drift as a tracked risk, not a paperwork afterthought.
- **Symptom:** The team declares "we are SOC 2 compliant" or "we are PCI
  compliant" internally or to a customer based on having completed this
  mapping exercise themselves.
  **Fix:** State clearly, every time, that only an accredited certification
  body (ISO 27001), a licensed CPA firm (SOC 2), or the appropriate PCI-DSS
  validation process (SAQ self-assessment or QSA-led Report on Compliance,
  depending on level) can produce that determination — this skill
  produces audit-ready technical mapping and evidence, not the attestation
  itself.
- **Symptom:** Engineering maps a control to a framework requirement using
  a control ID they are not actually sure is current, and the auditor
  flags the citation as incorrect, casting doubt on the whole matrix.
  **Fix:** Mark uncertain citations explicitly ("commonly cited as X;
  verify against current framework text") rather than asserting false
  precision — a matrix with a few honestly-flagged uncertainties is more
  credible than one with confident wrong numbers.
- **Symptom:** All effort goes into mapping controls that already exist
  and look good (e.g. encryption, SAST), while gaps (e.g. no formal
  incident response plan, no quarterly access reviews) are left off the
  matrix entirely because there's no existing control to map.
  **Fix:** Build the matrix from the framework's requirement list
  outward, not from the existing-controls list inward — every framework
  requirement should appear as a row, even if the "mapped control" column
  says "gap — no control yet, backlog item opened."

## Worked example

Illustrative controls-mapping matrix excerpt (control IDs shown are
commonly-cited examples for illustration — always verify exact current
numbering against the specific framework version and your auditor):

| Technical control (existing implementation) | SOC 2 Trust Services Criteria | ISO/IEC 27001 Annex A (illustrative) | PCI-DSS (illustrative, v4.0-era) | NIST CSF 2.0 function/category | Evidence source | Frequency |
|---|---|---|---|---|---|---|
| Vault-managed secret rotation, 90-day automatic rotation (see [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md)) | CC6.1 (logical access controls) | A.8.24 (use of cryptography) / A.5.17 (authentication information) | Req. 8 (identify users, authenticate access) | `PR.AA` (Identity Mgmt, Authentication & Access Control) | Vault audit log export showing rotation events; quarterly rotation report | Quarterly |
| Least-privilege IAM roles + quarterly access review (see [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md)) | CC6.2, CC6.3 (access provisioning/removal) | A.5.15 (access control), A.5.18 (access rights) | Req. 7 (restrict access by need to know) | `PR.AA` | Access review sign-off tickets; IAM policy diff history | Quarterly |
| Centralized log aggregation with 1-year retention | CC7.2 (monitoring for security events) | A.8.15 (logging) | Req. 10 (log and monitor access) | `DE.AE` (Adverse Event Analysis), `DE.CM` (Continuous Monitoring) | SIEM retention config; sample log query results | Continuous, reviewed monthly |
| TLS 1.2+ enforced in transit; KMS-managed encryption at rest | CC6.7 (data transmission/encryption) | A.8.24 (cryptography) | Req. 3 (protect stored account data), Req. 4 (protect data in transit) | `PR.DS` (Data Security) | TLS config scan results; KMS key policy export | Per release / quarterly |
| SAST + DAST in CI/CD with tracked remediation SLA (see [sast-integration](../../../devsecops/skills/sast-integration/SKILL.md), [dast-integration](../../../devsecops/skills/dast-integration/SKILL.md)) | CC7.1 (vulnerability detection) | A.8.29 (security testing in development) | Req. 6 (develop/maintain secure systems) | `ID.RA` (Risk Assessment), `PR.PS` (Platform Security) | CI pipeline scan history; remediation ticket closure times | Continuous, reviewed monthly |
| Tested cross-region backup + documented RTO/RPO (see [disaster-recovery-and-backup-strategy](../../../cloud/skills/disaster-recovery-and-backup-strategy/SKILL.md)) | A1.2 (Availability — recovery) | A.5.29/A.5.30 (ICT readiness for business continuity — numbering varies by edition) | Req. 12 (support info security with policies; DR referenced under org policy) | `RC.RP` (Incident Recovery Plan Execution) | DR test report with timestamps and measured RTO/RPO vs target | Semi-annual test |
| **Gap (illustrative):** no formal quarterly access-recertification process, only ad hoc | CC6.2 | A.5.18 | Req. 7 | `PR.AA` | None yet | — |

Illustrative summary handed to the compliance owner: "5 of 6 core control
areas mapped with continuous evidence sources identified; 1 gap opened as
engineering backlog item `<TICKET_PLACEHOLDER>` (formal quarterly access
recertification) targeted before the next audit window. This matrix
reflects engineering's technical control mapping as input to your audit
preparation — final scope, sampling, and attestation determination remain
with `<AUDIT_FIRM_OR_QSA_PLACEHOLDER>`."

## Cross-references

- [cis-benchmarks-hardening](../cis-benchmarks-hardening/SKILL.md) — infrastructure/OS hardening scan evidence that commonly supports security-criteria mappings above.
- [cloud-well-architected-framework-review](../cloud-well-architected-framework-review/SKILL.md) — broader architecture/risk review; its security-pillar findings often become gaps or controls in this matrix.
- [owasp-top-10-secure-coding-standards](../owasp-top-10-secure-coding-standards/SKILL.md) — application security practices and tooling that support PCI-DSS Requirement 6 and NIST CSF `PR.PS` mappings.
- [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md) — the control implementation behind most access-control/authentication mappings.
- [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md) — least-privilege and access-review controls mapped above.
- [sast-integration](../../../devsecops/skills/sast-integration/SKILL.md) and [dast-integration](../../../devsecops/skills/dast-integration/SKILL.md) — secure-development-lifecycle evidence for PCI-DSS Req. 6 / NIST CSF `ID.RA`, `PR.PS`.
- [supply-chain-security-slsa-sbom](../../../devsecops/skills/supply-chain-security-slsa-sbom/SKILL.md) — SBOM/provenance evidence increasingly requested in vendor security questionnaires and NIST supply-chain guidance.
- [policy-as-code-guardrails](../../../devsecops/skills/policy-as-code-guardrails/SKILL.md) — automated enforcement that strengthens the "operates continuously" evidence story for many mapped controls.
- [disaster-recovery-and-backup-strategy](../../../cloud/skills/disaster-recovery-and-backup-strategy/SKILL.md) — availability/recovery control evidence for SOC 2 Availability criteria and PCI-DSS/ISO business-continuity references.
