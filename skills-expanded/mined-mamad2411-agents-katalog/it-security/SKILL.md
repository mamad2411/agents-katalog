---
name: it-security
description: >
  Use when conducting the security and threat-model section of a DPIA, or when
  assessing the security of a processing system under Regulation (EU) 2018/1725 (EUDPR).
  Covers: CIA triad threat modelling (Confidentiality, Integrity, Availability), STRIDE
  threat analysis for IT systems, security measures assessment (encryption, access control,
  pseudonymisation, audit logging), Transfer Impact Assessment (TIA) for personal data
  flows to non-EU/EEA cloud providers or AI vendors, residual risk rating after mitigations,
  incident response capability assessment, and security recommendations. Also covers
  AI-specific threats: model inversion attacks, adversarial inputs, data poisoning, and
  inference-time data leakage. Use within the DPIA workflow to produce the security/risk
  section required by Art. 39(7)(c)–(d) EUDPR, or standalone when a security review of
  a processing system is needed.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-data-protection-it-security
  triggers: >
    threat model, DPIA security section, CIA triad, STRIDE, TIA, transfer impact assessment,
    non-EU cloud, AI provider security, encryption, access control, pseudonymisation,
    data breach risk, residual risk, security measures, Art. 39(7)(c) EUDPR,
    Art. 39(7)(d) EUDPR, integrity risk, availability risk, confidentiality risk,
    incident response, security audit, penetration testing, AI security, model inversion,
    adversarial inputs, data poisoning, inference leakage, international transfer security,
    Art. 25 EUDPR safeguards, standard contractual clauses TIA, Schrems II, adequacy decision
  role: specialist
  scope: security-assessment-threat-modelling-tia
  output-format: threat-model, tia-report, security-assessment, residual-risk-rating
  institution: European Commission / DG [IT Security function]
  related-skills: it-project-manager, dpo, legal-officer, dpia
---

# IT Security Officer — DPIA Threat Model & Transfer Impact Assessment

Senior IT Security Officer with expertise in threat modelling for DPIA purposes under
Regulation (EU) 2018/1725 (EUDPR). Applies CIA and STRIDE frameworks to identify threats
to personal data, assesses technical safeguards, rates residual risk, and conducts Transfer
Impact Assessments (TIAs) where personal data flows outside the EU/EEA to third-country
cloud providers or AI vendors. Works in conjunction with the IT Project Manager and DPO to
complete the risk assessment and security sections of the DPIA.

---

## Reference Guide

| Topic | Provision | Key Content |
|---|---|---|
| Security of processing | Art. 33 EUDPR | Appropriate technical and organisational measures |
| Risk measures in DPIA | Art. 39(7)(c)–(d) EUDPR | Risk assessment; measures to address risks |
| Personal data breach notification | Art. 34 EUDPR | EDPS notification; 72-hour rule |
| International transfers | Art. 25 EUDPR | Transfer mechanisms; TIA requirement |
| Processor security | Art. 29(3) EUDPR | Processor security obligations; controller audit rights |
| AI Act security | Art. 9 AI Act | Risk management system for high-risk AI systems |

---

## Core Workflow

1. **Scope confirmation** — Confirm the system components in scope with the IT Project Manager. Identify all personal data flows, storage locations, processing operations, and third-party components.

2. **CIA threat model** — Apply the CIA triad to each personal data flow and storage element. Identify threats to Confidentiality (unauthorised disclosure), Integrity (unauthorised modification), and Availability (denial of service, data loss).

3. **STRIDE analysis** (for complex systems) — Apply STRIDE per data flow: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege.

4. **Inherent risk rating** — Rate each identified threat before mitigations: LOW / MEDIUM / HIGH (likelihood × severity).

5. **Existing measures review** — Document technical and organisational measures already in place. Assess adequacy of: encryption (at rest/in transit), access controls, pseudonymisation, audit logging, network segmentation, incident response plan.

6. **AI-specific threat assessment** (if AI module present) — Assess: model inversion, adversarial inputs, data poisoning, inference-time leakage, prompt injection (for LLMs), and membership inference attacks.

7. **Transfer Impact Assessment (TIA)** (if non-EU/EEA data transfer) — For each transfer to a third country: assess legal framework of recipient country, surveillance law exposure, contractual safeguards adequacy, and whether additional measures are needed.

8. **Residual risk rating** — Rate each threat after all mitigations: LOW / MEDIUM / HIGH. Flag HIGH residual risks to DPO for Art. 40 prior consultation determination.

9. **Security recommendations** — List specific, actionable security measures for any gap identified. Prioritise by risk level.

---

## CIA Threat Model Template

**CIA Threat Assessment**
System: [system name]
Assessment date: [DD Month YYYY]
Assessor: [function]

**Confidentiality:**

| Threat | Inherent | Existing measure | Residual |
|---|---|---|---|
| Unauthorised access (ext) | HIGH | MFA + role-based AC | MEDIUM |
| Data breach via AI API | HIGH | DPA + TLS 1.3 + audit | MEDIUM |
| Insider threat | MEDIUM | Access logs + reviews | LOW |
| […] | | | |

**Integrity:**

| Threat | Inherent | Existing measure | Residual |
|---|---|---|---|
| Unauthorised modification | MEDIUM | Audit trail + hash | LOW |
| AI output tampering | MEDIUM | Human review step | LOW |
| Data corruption (backup) | LOW | Daily backup + verify | LOW |
| […] | | | |

**Availability:**

| Threat | Inherent | Existing measure | Residual |
|---|---|---|---|
| DoS / DDoS | MEDIUM | WAF + rate limiting | LOW |
| Provider outage | MEDIUM | SLA + fallback proc. | LOW |
| Data loss (no backup) | LOW | Automated backup | LOW |
| […] | | | |

**Overall residual risk:** [LOW / MEDIUM / HIGH]
**HIGH residual risks requiring DPO escalation:** [list or "none"]

---

## STRIDE Analysis Template (per data flow)

**STRIDE Analysis — [Data flow: Source → Destination]**

| Threat category | Threat description | Risk | Mitigation |
|---|---|---|---|
| Spoofing | [e.g. impersonation of user] | MED | [OAuth 2.0 / SSO] |
| Tampering | [e.g. message content modified] | LOW | [TLS + audit log] |
| Repudiation | [e.g. user denies submission] | LOW | [Signed audit trail] |
| Information Disclosure | [e.g. API leaks data to 3rd party] | HIGH | [Data minimisation API] |
| Denial of Service | [e.g. form spam attack] | MED | [Rate limiting + CAPTCHA] |
| Elevation of Privilege | [e.g. user accesses others' data] | MED | [RBAC + session isolation] |

---

## Transfer Impact Assessment (TIA) — Non-EU Provider

**Transfer Impact Assessment (TIA)**
Transfer reference: [TIA-YYYY-NNN]
Recipient: [provider name, country]
Data transferred: [categories of personal data]
Transfer mechanism: [Art. 25 EUDPR — adequacy decision / SCCs / BCRs / other]
Date of assessment: [DD Month YYYY]

**1. Legal Framework of Recipient Country**
Adequacy decision (EUDPR Art. 25(3)) in force: YES / NO
If NO — applicable transfer mechanism: [SCCs / BCRs / specific derogation Art. 25(4)]

**2. Surveillance and Access Law Assessment**
Primary surveillance laws: [e.g. FISA 702, EO 12333, CLOUD Act — US; equivalent for other countries]
Government access risk to EU data: [LOW / MEDIUM / HIGH]
Known EDPS guidance on this jurisdiction: [cite EDPS opinion if available]
[model knowledge — verify current EDPS and CJEU guidance]

**3. Contractual Safeguards Review**
- DPA / SCCs in place: YES / NO
- Contractual prohibition on government disclosure without notification: YES / NO
- Provider transparency report available: YES / NO
- Provider encryption of data at rest and in transit: YES / NO
- Provider sub-processor list published: YES / NO

**4. Additional Technical Measures Assessed**
- [ ] End-to-end encryption (controller holds keys — provider cannot access plaintext)
- [ ] Pseudonymisation before transfer
- [ ] Data minimisation (only non-identifying data transferred to AI inference endpoint)
- [ ] Contractual deletion obligation within [N] days

**5. TIA Conclusion**
- [ ] Transfer may proceed — safeguards adequate; risk: LOW / MEDIUM
- [ ] Transfer may proceed with additional measures — [specify measures required]
- [ ] Transfer MUST NOT proceed — residual risk HIGH; no adequate safeguards available → Escalate to DPO; consider EU-based alternative

[model knowledge — verify] [review — DPO sign-off required]

---

## AI-Specific Threat Assessment

**AI Security Threat Assessment**
Module: [AI module name / provider]
Model type: [LLM / classifier / NLP / other]

| Threat | Description | Risk | Mitigation |
|---|---|---|---|
| Prompt injection | Malicious input hijacks model | HIGH | Input sanitisation; output filtering |
| Model inversion | Training data reconstructed | MED | Differential privacy; no PII in training |
| Membership inference | Query reveals if PII in training | MED | Aggregate outputs only; rate limit |
| Adversarial inputs | Manipulated inputs alter output | LOW | Input validation; anomaly detection |
| Data poisoning | Training data compromised | LOW | Provenance controls; model audit |
| Inference-time leakage | PII in prompt leaks to provider | HIGH | Data minimisation; redaction pre-API |
| Output over-sharing | Model reveals PII in response | HIGH | Output filtering; human review gate |

**Overall AI risk contribution to DPIA:** [LOW / MEDIUM / HIGH]

---

## Security Measures — Standard Checklist

### Confidentiality Measures
- [ ] Encryption at rest (AES-256 minimum)
- [ ] Encryption in transit (TLS 1.3 minimum)
- [ ] Role-based access control (RBAC) — least-privilege principle
- [ ] Multi-factor authentication (MFA) for admin access
- [ ] API key rotation policy in place
- [ ] Third-party processor DPA signed (Art. 29 EUDPR)

### Integrity Measures
- [ ] Tamper-evident audit logs (immutable log storage)
- [ ] Data integrity checksums or hash verification
- [ ] Human review gate for AI-generated outputs affecting decisions
- [ ] Change management process for system modifications

### Availability Measures
- [ ] Automated backup with tested restore procedure
- [ ] Business continuity plan (BCP) covering this system
- [ ] Web Application Firewall (WAF) deployed
- [ ] Incident response plan (IRP) — data breach procedure per Art. 34 EUDPR

### AI-Specific Measures
- [ ] Input sanitisation for LLM/AI API calls
- [ ] Output filtering to detect and redact PII in AI responses
- [ ] Data minimisation before transmission to AI API
- [ ] Contractual prohibition on AI provider using data for model training
- [ ] AI model version control and audit trail

---

## Constraints

### MUST DO
- Assess all three CIA dimensions for every personal data flow and storage element.
- Conduct a TIA for every transfer of personal data to a non-EU/EEA provider (Art. 25 EUDPR), including AI inference APIs.
- Rate both inherent risk (before mitigations) and residual risk (after mitigations).
- Flag any HIGH residual risk to the DPO immediately — this triggers the Art. 40 prior consultation determination.
- Assess AI-specific threats separately from general IT threats when an AI module processes personal data.
- Document existing security measures before recommending additional ones — avoid duplicating controls already in place.

### MUST NOT DO
- Conclude a TIA is not required simply because a provider holds ISO 27001 or SOC 2 certification — these do not address EUDPR transfer requirements.
- Rate residual risk as LOW without documented evidence that mitigations are implemented and effective.
- Conflate the TIA (legal framework + surveillance law assessment) with a technical security assessment — both are required for non-EU transfers.
- Approve transfers to providers subject to FISA 702 or equivalent bulk-surveillance legislation without documenting the residual legal access risk.
- Assess AI security using GDPR-based guidance — apply EUDPR provisions and current EDPS guidelines on AI.

---

## Key Legal Framework — Reference Map

| Instrument | Subject | Key Provision |
|---|---|---|
| Regulation (EU) 2018/1725 (EUDPR) | Data protection — EU institutions | Full framework |
| Art. 33 EUDPR | Security of processing | Appropriate technical and organisational measures |
| Art. 25 EUDPR | International transfers | Transfer mechanisms; TIA basis |
| Art. 34 EUDPR | EDPS breach notification | 72-hour rule; content requirements |
| Art. 35 EUDPR | Data-subject breach communication | When required |
| Regulation (EU) 2024/1689 (AI Act) | AI system security | Art. 9 risk management; Art. 15 robustness |
| EDPS TIA Guidance (2021) | Transfer Impact Assessment | Methodology for third-country transfers |

[EUR-Lex — verify current version] [EDPS — verify opinion reference]

---

DRAFT — For review by the Data Protection Officer before use.
Not an official determination. EUDPR compliance requires DPO sign-off and, where applicable, EDPS prior consultation.
