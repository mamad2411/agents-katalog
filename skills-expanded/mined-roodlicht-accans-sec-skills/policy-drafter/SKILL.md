---
name: policy-drafter
description: Policy-drafting workflow for security policies — AUP, Incident Response Plan, Access Control, Data Classification, BCP, Change Management, Vendor Management, Crypto, and Remote Work. Structure with Purpose/Scope/Statement/Roles/Enforcement/Review, ISO 27001 Annex A.5 alignment, NL/EN drafting.
---

# Policy Drafter

> **Disclaimer**: this skill supports technical and operational policy drafting. Legal review (employment-law aspects of an AUP, privacy interfaces, contractual carry-through to customers) belongs with legal/HR/DPO. This skill does not produce a legally binding text.

## When to use

Security policies are the documented rules your ISMS, your compliance audits, and your day-to-day operations are measured against. This skill helps with drafting, structural consistency, review workflows, and clause libraries.

Triggers on:

- A question like "write an AUP", "IRP template", "access control policy", "review our security policies", "what goes in a data classification policy", "how often to review policies".
- A handoff from `iso27001` (Cl 5.2 Information Security Policy, Annex A.5 group), `soc2` (CC1-CC2-CC5 policy requirements), `nis2` (Art 21 first measure), `dora` (Art 6 framework).
- A new organization or new product line where the policy stack is still missing.
- An annual review cycle, or event-driven revision (incident, organizational change, new legislation).

### When NOT (handoff)

- Privacy-specific policies (privacy statement, DPA, cookie policy) → `gdpr-pia` context plus legal. Touches on this skill but requires separate legal expertise.
- Technical implementation of what policies require → security skills (`secure-coding`, `security-review`, `container-hardening`, etc.).
- Contractual policies aimed at vendors → `vendor-questionnaire` + legal.
- Risk-appetite statement as part of risk management → `risk-register`.
- Evidence-policy alignment for audits → `audit-evidence`.
- IR operational runbooks (step-by-step response) → `ir-runbook`. This skill covers the policy layer; the runbook is the execution.

## Approach

Six phases. Phase 2 (structure) + phase 3 (drafting per type) are the core.

### 1. Inventory the policy stack

Not every organization needs every policy, but a coherent stack prevents both gaps and overlap. Typical baseline:

- **Tier 1 (highest, board-approved)**: Information Security Policy (the umbrella). For ISO 27001 this is the Cl 5.2 requirement.
- **Tier 2 (topic policies, CISO-approved)**: Acceptable Use Policy, Access Control Policy, Data Classification Policy, Incident Response Plan, Business Continuity Plan, Vendor Management Policy, Change Management Policy, Cryptography Policy, Risk Management Policy.
- **Tier 3 (procedures and standards, dept-approved)**: password standard, secure-coding standard, backup procedure, onboarding procedure.

Inventory: which policies exist, which are missing against the chosen framework (ISO 27001 Annex A.5, NIST CSF Govern function, SOC 2 CC5, NIS2 Art 21(1-2)). Prioritize gaps on risk impact, not on ease of writing.

### 2. Shared structure (against inconsistency)

Every policy follows the same six-section structure. Keeps review auditable, comparable, maintainable.

1. **Purpose**: why this policy exists. One paragraph.
2. **Scope**: who and what. Explicit: all employees/contractors/vendors; all systems/data/locations; exceptions.
3. **Policy Statement**: the rules themselves. Concrete, imperative, no "should consider". "Users shall..." / "The organization must...".
4. **Roles and Responsibilities**: who does what. RACI-style or a bullet per role.
5. **Compliance and Enforcement**: consequences for non-compliance. HR-disciplinary for employees, contractual for vendors.
6. **Review and Revision**: review cadence (usually annual + event-driven), approver, version control.

Metadata header per policy: title, policy ID, version, issue date, next-review date, approver, owner.

Common miss: the "Policy Statement" becomes vague ("we take security seriously"). That is not a policy, that is marketing. Test: can an auditor use this policy to determine whether someone has violated it? If not, rewrite.

### 3. Per-policy guidance (clause libraries)

Brief per type. Detailed templates via references (SANS, NIST, NCSC-NL) instead of copying them here.

- **Acceptable Use Policy (AUP)**. Covers: permitted use of company assets, password handling, e-mail/internet use, remote work, social media, reporting suspicious activity, employee privacy expectations. NL-specific: AVG aspects of monitoring (Art 88 AVG gives NL room, the UAVG fills it in) — refer to legal. Example clauses: "Employees may not use company assets for [list]. Incidental personal use is permitted insofar as..."
- **Access Control Policy**. Covers: identity lifecycle (joiner/mover/leaver), role-based access, privileged-access management, access-review cadence, MFA requirements, session timeouts. Aligns with ISO 27001 Annex A.5.15-A.5.18, A.8.2-A.8.5.
- **Data Classification Policy**. Covers: classification levels (typically 3-4: Public, Internal, Confidential, Restricted/Secret), handling rules per level (storage, transmission, destruction), labeling rules. Aligns with A.5.12-A.5.14.
- **Incident Response Plan (IRP)**. Covers: definitions (incident vs event), severity levels, escalation paths, roles in the IR team, communication requirements (internal + external + regulator), post-incident review. This is the policy layer; the operational runbook lives in `ir-runbook`.
- **Business Continuity Plan (BCP)**. Covers: business-impact analysis (BIA), RTO/RPO per service, recovery procedures at a high level, testing cadence. Technical execution in DR playbooks; this policy sets the requirements.
- **Vendor Management Policy**. Covers: onboarding due diligence, contract clauses (aligned with `vendor-questionnaire`), ongoing monitoring, offboarding procedure, concentration limits. Aligns with DORA Art 28-30 for financial, NIS2 Art 21(4) for others.
- **Change Management Policy**. Covers: change types (standard/normal/emergency), approval thresholds, testing requirements, rollback planning. Aligns with A.8.32, and relevant for SOC 2 CC8.
- **Cryptography Policy**. Covers: approved algorithms and key lengths (AES-256, RSA-3072+, Ed25519, ECDSA-P256+), key-management lifecycle, crypto agility for the post-quantum transition. Aligns with A.8.24, FIPS 140-3 context.
- **Remote Work Policy**. Covers: approved devices and networks, VPN requirements, physical-security requirements at home, data handling on devices, theft/loss reporting obligation.
- **Clean Desk / Clear Screen Policy**. Covers: physical discipline for sensitive papers, lock-on-leave policy, print rules.

### 4. Drafting discipline

- **Language**: pick one primary language (NL for NL operations, EN for international), be consistent. Bilingual policies double review work and create inconsistency risk when one version is updated but not the other.
- **Readability**: short sentences, active voice, definitions in a glossary section or at the start. Avoid legal jargon where operational is clearer.
- **Concrete over vague**: "Passwords must be at least 14 characters" > "Passwords must be sufficiently complex". Every vague clause is future audit friction.
- **References**: to other policies (not copy-paste), to framework refs (ISO 27001 Annex A codes), to external laws/standards. Make sure references stay current with policy updates.
- **Exception procedure**: every policy has a path for deviations with CISO approval plus a deadline for re-compliance. Without an exception procedure, an informal workaround culture forms.

### 5. Review + approval workflow + publication

- **Review cadence**: annual minimum. Event-driven revision on (a) a significant security incident, (b) organizational change (M&A, scope change), (c) new law/rule (NIS2 entering into force, AVG change), (d) significant technology change.
- **Approval chain**: tier 1 to the board, tier 2 to the CISO, tier 3 to the department head. Each approval documented (meeting minutes or signed approval memo).
- **Publication**: internal policy portal (Confluence, SharePoint, dedicated GRC platform). Searchable, versioned, accessible to all in-scope persons. Mobile-reachable for remote workers.
- **Awareness and training**: every policy update generates a communication moment. Training for high-impact policies (AUP, IRP) annually required with tracking. SOC 2 CC2 evidence.
- **Version history** and **change log**: what changed between versions and why. Critical at audit time when explaining why a particular clause was added.

### 6. Verification-loop

Layer 1: scope (all tier-1 and relevant tier-2 policies present for the chosen frameworks?), assumptions (policy statements concrete enough to audit?), gaps (exception procedure for every policy?), consistency (terminology consistent across policies, every RACI matches). Layer 2: no invented ISO Annex A codes, framework mapping correct (e.g. AUP maps to A.5.1, A.6.2, A.5.10), NL legal references (AVG, UAVG, Arbo) correct, no pretense that a technical standard document is legally binding outside the organization.

## Output

Two modes: policy drafting (produce a new policy) or policy review (assess an existing policy).

**Drafting mode** delivers a draft policy document following the six-section structure, plus a metadata header, plus a reference list for review.

**Review mode**:

```
Policy review — <policy name + version>
Owner: <...> | Last review: <date> | Next review: <date>

Structure check (six sections):
  Purpose:          <present + quality>
  Scope:            <clearly bounded | vague>
  Policy Statement: <concrete | vague>
  Roles & Resp:     <RACI clear | gap>
  Compliance:       <enforcement mechanism clear | gap>
  Review/Revision:  <cadence + approver>

Content findings:
  - Vague statements: <list with quotes>
  - Inconsistencies with other policies: <list>
  - Framework gaps (ISO/SOC2/NIS2/DORA): <codes>
  - Legal review needed: <topics, with handoff>

Update recommendations:
  <concrete changes with rationale>

Verification-loop: ...
```

## References

- **SANS Policy Templates** — [https://www.sans.org/information-security-policy/](https://www.sans.org/information-security-policy/). Freely available templates, good starting point, may be adapted.
- **NIST SP 800-53 Rev. 5** — [https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final). Control catalog policies refer to.
- **NIST SP 800-100** — [https://csrc.nist.gov/pubs/sp/800/100/final](https://csrc.nist.gov/pubs/sp/800/100/final). Information Security Handbook, policy-structure guidance.
- **ISO/IEC 27002:2022** — [https://www.iso.org/standard/75652.html](https://www.iso.org/standard/75652.html). Guidance companion for Annex A controls, useful for policy context.
- **NCSC-NL — Handreikingen** — [https://www.ncsc.nl/](https://www.ncsc.nl/). NL-specific guidance, sometimes template language.
- **BIO (Baseline Informatiebeveiliging Overheid)** — [https://bio-overheid.nl/](https://bio-overheid.nl/). For NL government and chain partners, a practical template basis.
- **ENISA — Information security policies** — [https://www.enisa.europa.eu/](https://www.enisa.europa.eu/). Publications with example policies.

## Categories

- grc
