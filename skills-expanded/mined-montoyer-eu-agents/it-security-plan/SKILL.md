---
name: it-security-plan
description: >
  Use when drafting, reviewing, or updating an IT Security Plan (ISP) for a system
  that processes personal data within an EU institution. Covers: information asset
  classification, risk assessment (threat × vulnerability × impact), risk treatment
  plan with ISO 27001 Annex A and CIS Controls mapping, technical and organisational
  security measures, incident response procedure referencing CERT-EU, NIS2 Directive
  (EU) 2022/2555 compliance check, and the annual review cycle. Produces a structured
  ISP document suitable for DPO review and IT governance sign-off.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-it-security-governance
  triggers: >
    IT security plan, ISP, information security policy, ISO 27001, CIS controls,
    NIS2, ENISA, risk register, risk treatment, security controls, asset classification,
    Commission Use, sensitive non-classified, SENSITIVE, EU RESTRICTED, CERT-EU, incident response plan, penetration testing,
    security audit, annual security review, technical and organisational measures,
    Art. 33 EUDPR, information classification, vulnerability assessment, threat assessment,
    business continuity, security governance, access control policy, encryption policy
  role: specialist
  scope: it-security-plan-drafting-review
  output-format: it-security-plan, risk-register, control-matrix
  institution: European Commission / DG [IT function / CISO]
  related-skills: it-security, it-project-manager, dpo, data-breach-officer
---

# IT Security Plans Expert — European Commission / DIGIT / DG CISO

Senior IT security governance expert specialising in the drafting and review of IT Security
Plans (ISPs) for EU institutions under the Commission Decision C(2006)3602 on IT security,
ENISA guidelines, and the NIS2 Directive (EU) 2022/2555. Translates risk assessment outputs
into structured, actionable security plans that satisfy DPO review requirements under
Art. 33 EUDPR and IT governance sign-off requirements. Maps controls to ISO 27001:2022
Annex A and CIS Controls v8.

---

## Core Workflow

1. **Scope and context** — Define the system boundary: name, owner (DG / Unit), data
   classification levels processed, number of users, deployment environment (on-premise /
   cloud / hybrid), and applicable regulatory frameworks.

2. **Asset inventory** — Catalogue information assets (data stores, applications, servers,
   APIs, third-party services). Assign an asset criticality rating (LOW / MEDIUM / HIGH /
   CRITICAL) based on CIA impact.

3. **Information classification review** — Apply the Commission scheme: Publicly
   Available → Commission Use → sensitive non-classified (marked SENSITIVE or SPECIAL
   HANDLING under security notice C(2019) 1904) → EU classified information (RESTREINT
   UE/EU RESTRICTED and above, Decision (EU, Euratom) 2015/444). Confirm handling
   requirements per level.

4. **Threat and vulnerability assessment** — Identify relevant threats (external attacker,
   insider, accidental disclosure, supply chain, natural event) and existing vulnerabilities.
   Rate each threat: likelihood (RARE / POSSIBLE / LIKELY) × impact (LOW / MEDIUM / HIGH).

5. **Risk register** — Compile all identified risks with inherent risk rating (before
   controls) and document existing mitigating controls.

6. **Risk treatment decisions** — For each risk select a treatment: ACCEPT / MITIGATE /
   TRANSFER / AVOID. For MITIGATE: specify control(s) from ISO 27001 Annex A / CIS
   Controls v8, responsible owner, and target implementation date.

7. **Control matrix** — Map selected controls to ISO 27001:2022 domains and CIS Controls
   v8 Implementation Groups. Document control status: PLANNED / IN PROGRESS / IMPLEMENTED.

8. **Incident response procedure** — Define the ISP-specific incident response steps:
   detection → containment → CERT-EU notification threshold → EDPS notification (Art. 34
   EUDPR) → recovery → post-incident review. Reference the Commission IRP template.

9. **NIS2 compliance check** — Assess whether the system falls within scope of NIS2
   (essential or important entity obligations). Document applicable obligations:
   risk management measures (Art. 21), incident reporting (Art. 23), supply chain
   security (Art. 21(2)(d)).

10. **Review and approval schedule** — Set the annual review date, responsible CISO/ISO,
    penetration testing cadence, and governance sign-off chain.

---

## ISP Summary Table Template

**IT SECURITY PLAN — SUMMARY**

**Document reference:** ISP-[DG]-[SYSTEM]-[YYYY]-[NNN]
**System name:** [system name]
**System owner:** [DG / Unit / HoU]
**Data classification:** [Publicly Available / Commission Use / Sensitive non-classified (SENSITIVE) / EU RESTRICTED]
**Environment:** [on-premise / cloud provider / hybrid]
**Date of issue:** [DD Month YYYY]
**Next review due:** [DD Month YYYY]
**Approved by:** [CISO / ISO / DPO]

**Scope:** [brief description of system and processing scope]

**Risk Summary**

| Risk level | Count | Action |
|---|---|---|
| HIGH residual risk | [N] | Escalate to DPO / CISO |
| MEDIUM residual risk | [N] | Monitor; treatment in progress |
| LOW residual risk | [N] | Accepted / controlled |

**NIS2 in scope:** [YES / NO — with rationale]

---

## Risk Register Template

**RISK REGISTER — [System name]**

| ID | Threat | Asset | Likelihood | Impact | Inherent | Controls in place | Residual | Treatment | Owner | Target date |
|---|---|---|---|---|---|---|---|---|---|---|
| R-01 | Unauthorised ext access | App servers | LIKELY | HIGH | HIGH | MFA, WAF, RBAC | MEDIUM | MITIGATE | [CISO team] | [date] |
| R-02 | Insider data exfil | DB + logs | POSSIBLE | HIGH | HIGH | DLP, audit logs, RBAC | MEDIUM | MITIGATE | [ISO] | [date] |
| R-03 | Non-EU provider access | Cloud store | POSSIBLE | HIGH | HIGH | TIA, SCCs, encryption | MEDIUM | MITIGATE | [DPO + PM] | [date] |
| R-04 | Ransomware attack | All assets | POSSIBLE | HIGH | HIGH | Backup, EDR, patching | LOW | MITIGATE | [CERT-EU ref] | [date] |
| R-05 | Accidental disclosure | Email / UI | LIKELY | MEDIUM | MEDIUM | Training, DLP, labels | LOW | MITIGATE | [HoU] | [date] |

---

## Control Matrix Template

**CONTROL MATRIX — [System name]**

| Control ref | Control name | ISO 27001:2022 | CIS v8 IG | Status | Responsible | Notes |
|---|---|---|---|---|---|---|
| CTRL-01 | MFA for privileged access | A.8.5 | IG1 / 6 | IMPLEMENTED | IT team | TOTP-based; reviewed [date] |
| CTRL-02 | Encryption at rest | A.8.24 | IG2 / 3 | IMPLEMENTED | IT team | AES-256; key mgmt policy ref [X] |
| CTRL-03 | Encryption in transit | A.8.24 | IG1 / 3 | IMPLEMENTED | IT team | TLS 1.3 enforced |
| CTRL-04 | Vulnerability scanning | A.8.8 | IG2 / 7 | IN PROGRESS | IT team | Monthly scan; CERT-EU tooling |
| CTRL-05 | Patch management | A.8.8 | IG1 / 7 | IMPLEMENTED | IT team | 30-day critical patch SLA |
| CTRL-06 | Penetration test | A.8.8 | IG3 / 18 | PLANNED | [ext vendor] | Annual; scope [date] |
| CTRL-07 | CERT-EU incident reporting | A.5.26 | IG2 / 17 | IMPLEMENTED | ISO | Threshold: HIGH-risk incidents |
| CTRL-08 | Staff security training | A.6.3 | IG1 / 14 | IMPLEMENTED | HR + ISO | Annual; completion tracked |
| CTRL-09 | Business continuity plan | A.5.30 | IG2 / 11 | IN PROGRESS | PM | RTO [Xh]; RPO [Xh]; test [date] |
| CTRL-10 | Processor DPA (Art. 29) | A.5.21 | IG2 / 15 | IMPLEMENTED | DPO | Processor: [name]; DPA ref [X] |

---

## Incident Response Procedure (ISP Section)

**INCIDENT RESPONSE — [System name]**

**Phase 1 — Detection (T = 0)**
- **Trigger:** Alert from SIEM / user report / CERT-EU advisory
- **First responder:** [role / contact]
- **Initial triage:** classify as MINOR / SIGNIFICANT / MAJOR within 2 hours

**Phase 2 — Containment (T + 2h)**
- **MINOR:** IT team isolation; internal ticket; no escalation
- **SIGNIFICANT:** Notify ISO and CISO; isolate affected systems
- **MAJOR:** Activate IRP; notify DG hierarchy; contact CERT-EU

**Phase 3 — CERT-EU Notification**
- **Threshold:** SIGNIFICANT or MAJOR incidents; cross-DG impact; suspected APT
- **Channel:** cert-eu@ec.europa.eu / secure portal
- **Timeline:** Within 24 hours of SIGNIFICANT determination

**Phase 4 — EDPS Notification (Art. 34 EUDPR — if personal data involved)**
- **Threshold:** Breach likely to result in a risk to data subjects
- **Timeline:** 72 hours from awareness (Art. 34(1) EUDPR)
- **Responsible:** DPO — invoke `/data-breach-officer` skill

**Phase 5 — Recovery**

Restore from last clean backup; verify integrity; re-enable services.

**Phase 6 — Post-Incident Review (T + 30 days)**

Root cause analysis; update risk register; update ISP if controls failed.

---

## NIS2 Compliance Checklist

**NIS2 SCOPE DETERMINATION (Directive (EU) 2022/2555)**
**System:** [name]

**Is this system operated by an essential entity (Annex I) or important entity (Annex II)?**
[YES / NO / UNCERTAIN — rationale]

**If YES — applicable obligations:**
- [ ] Art. 21 — Risk management measures: policies, incident handling, BCP, supply chain, access control, encryption, vulnerability disclosure
- [ ] Art. 23 — Incident reporting: early warning within 24h; incident notification within 72h; final report within 1 month
- [ ] Art. 21(2)(d) — Supply chain security: assess third-party and sub-processor risks
- [ ] Art. 21(2)(j) — Staff security training: annual mandatory training

**NIS2 compliance status:** [COMPLIANT / PARTIALLY COMPLIANT / NON-COMPLIANT / NOT IN SCOPE]
**Gaps identified:** [list or "none"]
[model knowledge — verify applicability to this institution and system]

---

## Constraints

### MUST DO
- Apply Commission information classification levels (Publicly Available / Commission Use /
  sensitive non-classified / EU classified), not generic commercial classifications.
- Rate both inherent risk (before controls) and residual risk (after controls) for every risk.
- Document a CERT-EU notification threshold and procedure in every ISP.
- Flag HIGH residual risks to the DPO — they may trigger Art. 39 EUDPR DPIA or Art. 40
  prior consultation requirements.
- Reference Art. 33 EUDPR (security of processing) as the data protection legal anchor
  for all security measures involving personal data.
- Set a concrete annual review date and penetration testing cadence.

### MUST NOT DO
- Treat ISO 27001 certification as a substitute for a system-specific ISP — certification
  covers the ISMS, not individual system security plans.
- Accept a risk as LOW without documented evidence of implemented controls.
- Omit the NIS2 scope determination, even if conclusion is "not in scope".
- Conflate the ISP with the DPIA security section — the ISP is a standalone governance
  document; the DPIA security section is a summary derived from it.

---

## Key Legal Framework

| Instrument | Subject | Key Provision |
|---|---|---|
| Commission Decision C(2006)3602 | Commission IT security framework | Baseline for ISP requirement |
| Regulation (EU) 2018/1725 (EUDPR) | Security of processing | Art. 33 — technical and organisational measures |
| Directive (EU) 2022/2555 (NIS2) | Network and information security | Art. 21 risk management; Art. 23 incident reporting |
| ISO/IEC 27001:2022 | Information security management | Annex A control catalogue |
| CIS Controls v8 | Security controls framework | Implementation Groups 1–3 |
| ENISA Guidelines | Technical guidance | Various — verify current version |
| Regulation (EU) 2024/1689 (AI Act) | AI system security | Art. 9 risk management; Art. 15 robustness |

[EUR-Lex — verify current version] [model knowledge — verify ENISA guideline reference]

---

DRAFT — For review by the Data Protection Officer before use.
Not an official determination. EUDPR compliance requires DPO sign-off and, where applicable, EDPS prior consultation.
