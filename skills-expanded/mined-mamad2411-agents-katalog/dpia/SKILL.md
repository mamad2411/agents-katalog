---
name: dpia
description: >
  Use to produce a complete Data Protection Impact Assessment (DPIA) under Article 39
  of Regulation (EU) 2018/1725 (EUDPR) for a processing activity of an EU institution,
  body, office, or agency. This is a multi-agent orchestration skill: it voices five
  specialist roles in sequence — IT Project Manager, Legal Officer, IT Security Officer,
  DPO, and EDPS prior-consultation determination — to generate a structured DPIA document
  meeting all seven Art. 39(7) EUDPR requirements. Covers: system architecture and data
  flows, legal basis and necessity/proportionality, CIA threat model and TIA for non-EU
  providers, risk assessment (inherent + residual), DPO sign-off opinion, and Art. 40
  prior-consultation determination. Includes AI module assessment where an AI component
  is present. Invoke with a brief description of the processing activity.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-data-protection-dpia-orchestration
  triggers: >
    DPIA, data protection impact assessment, Art. 39 EUDPR, full DPIA, complete DPIA,
    DPIA workflow, DPIA report, Art. 39(7) EUDPR, EUDPR impact assessment,
    new processing activity DPIA, AI-assisted DPIA, EU institution DPIA,
    EDPS prior consultation Art. 40, high-risk processing assessment,
    privacy risk assessment EU, DPIA orchestration, multi-agent DPIA
  role: specialist
  scope: multi-agent-dpia-orchestration
  output-format: dpia-report-art-39-7-eudpr
  institution: European Commission / DPO Office
  related-skills: dpo, it-project-manager, it-security, legal-officer
---

# DPIA Orchestrator — Art. 39 EUDPR Multi-Agent Assessment

This skill orchestrates a complete DPIA under Regulation (EU) 2018/1725 (EUDPR). Five
specialist agents contribute in sequence. Each section is clearly attributed to its
authoring role. The DPO leads the process and signs off. The EDPS prior-consultation
determination is the final output.

**Invocation:** `/dpia "<description of processing activity>"`

---

## Agent Roster

| Role | Mandate in this DPIA | Contributes section |
|---|---|---|
| **IT Project Manager** | System architecture, data flows, third-party processors, retention, AI module | §1 — Technical Description |
| **Legal Officer** | Legal basis Art. 5(1)(a)/(b) EUDPR, necessity, proportionality, special categories, retention justification | §2 — Legal Analysis |
| **IT Security Officer** | CIA threat model, TIA (if non-EU cloud/AI provider), security measures, residual risk | §3 — Security & Risk |
| **DPO** | Art. 39 threshold check, risk sign-off, DPIA completeness, Art. 40 determination | §4 — DPO Assessment |
| **EDPS** | Prior consultation — required or not? High-risk determination | §5 — EDPS Prior Consultation |

---

## DPIA Workflow — 8 Steps

1. **DPO — Threshold Screening** — Confirm whether Art. 39(1)/(2) EUDPR mandates a DPIA for this processing activity. If yes, proceed.

2. **IT Project Manager — Technical Description** — Produce the systematic description required by Art. 39(7)(a) EUDPR: architecture, data flows, data categories, third-party processors, AI module (if any), retention schedule, access controls.

3. **Legal Officer — Necessity and Proportionality** — Identify legal basis (Art. 5(1) EUDPR), apply necessity and proportionality test (Art. 39(7)(b) EUDPR), assess special categories and automated decision-making.

4. **IT Security Officer — Threat Model** — Apply CIA and STRIDE frameworks. Rate inherent risks. Review existing technical measures.

5. **IT Security Officer — TIA** (if non-EU/EEA provider involved) — Conduct Transfer Impact Assessment for each non-EU/EEA data transfer. Assess surveillance law exposure. Rate transfer risk.

6. **IT Security Officer — Residual Risk Rating** — Apply mitigations. Rate residual risk per threat. Identify any HIGH residual risks.

7. **DPO — Risk Sign-Off and Art. 40 Determination** — Consolidate risk findings. Issue DPO sign-off opinion. Determine whether Art. 40 EDPS prior consultation is required.

8. **EDPS — Prior Consultation Assessment** — If triggered: scope the prior consultation dossier. If not triggered: document reasoning.

---

## Output Structure — DPIA Report (Art. 39(7) EUDPR)

---

**Data Protection Impact Assessment**
Regulation (EU) 2018/1725 — Article 39

Processing activity: [name]
Reference: DPIA-[YYYY]-[NNN]
Controller: [EU institution / DG / Unit]
Date: [DD Month YYYY]
Status: DRAFT — pending DPO sign-off

---

### §0 — DPO Threshold Screening
*Author: Data Protection Officer*

Art. 39(1) EUDPR threshold:
Processing description (summary): [...]
Art. 39(2) criteria triggered: [criterion / NONE]
General test (Art. 39(1)): [assessment]
DPO determination: DPIA MANDATORY / DPIA RECOMMENDED / NOT REQUIRED
Basis: [reasoning]

---

### §1 — Technical Description (Art. 39(7)(a) EUDPR)
*Author: IT Project Manager*

**1.1 System Overview**
Name: [system name]
Purpose: [concise purpose statement]
Deployment: [environment — EU cloud / on-premise / hybrid]

**1.2 Data Categories and Data Subjects**
[Table: category | sensitivity | volume | data subjects]

**1.3 Data Flow Description**
Collection: [source → input mechanism]
Processing: [operations performed, including AI steps]
Storage: [location, controller vs. processor, encryption]
Recipients: [internal + external]
Deletion: [trigger + mechanism]

**1.4 Third-Party Processors**
[Table: processor | function | location | EU? | DPA? | transfer mechanism]

**1.5 AI Module (if applicable)**
Module: [name / provider]
Model type: [LLM / classifier / other]
Input / Output: [data in → output used for]
Human oversight: [mechanism]
AI Act risk tier: [PROHIBITED / HIGH-RISK / LIMITED / MINIMAL]
Transfer: [EU/EEA? if not: TIA reference]

**1.6 Retention Schedule**
[Table: category | retention | legal basis | deletion mechanism]

**1.7 Access Control Summary**
[Table: role | access type | MFA? | logged?]

[model knowledge — verify architecture details against actual system documentation]

---

### §2 — Legal Analysis (Art. 39(7)(b) EUDPR)
*Author: Legal Officer*

**2.1 Legal Basis**
Basis: Art. 5(1)([X]) EUDPR
Enabling act: [regulation / decision / treaty article]
[EUR-Lex — verify current version]

**2.2 Necessity Analysis**
Purpose: [specific, explicit, legitimate — assessed]
Necessity: [SATISFIED / NOT SATISFIED — reasoning]

**2.3 Proportionality Analysis**
Data volume: [assessment]
Categories: [assessment — special categories? Art. 10?]
Retention: [assessment]
Recipients: [assessment]
Proportionality: [SATISFIED / NOT SATISFIED — reasoning]

**2.4 Special Categories (Art. 10 EUDPR)**
Special categories present: YES / NO
[If YES: category | Art. 10(2) exception | reasoning]

**2.5 Automated Decisions (Art. 24 EUDPR)**
Solely automated decisions present: YES / NO
[If YES: description | legal basis | human review mechanism]

**2.6 Purpose Limitation (Art. 4(1)(b) EUDPR)**
Original purpose: [statement]
Further processing: [compatible / not applicable]

**2.7 Data Subject Rights**
[Table: right (Arts. 17–24) | implementable? | derogation needed?]

**2.8 Legal Basis — Overall Assessment**
Conclusion: [LAWFUL / REQUIRES ADJUSTMENT]
[review — DPO sign-off required]

---

### §3 — Security & Risk Assessment (Art. 39(7)(c)–(d))
*Author: IT Security Officer*

**3.1 CIA Threat Model**

*Confidentiality*
[Table: threat | inherent risk | measure | residual risk]

*Integrity*
[Table: threat | inherent risk | measure | residual risk]

*Availability*
[Table: threat | inherent risk | measure | residual risk]

**3.2 AI-Specific Threats (if AI module present)**
[Table: threat | risk | mitigation | residual]

**3.3 Transfer Impact Assessment (if non-EU/EEA transfer)**
TIA reference: [TIA-YYYY-NNN]
Recipient: [provider / country]
Transfer mechanism: [Art. 25 EUDPR basis]
Surveillance law exposure: [LOW / MEDIUM / HIGH]
Additional measures: [list]
TIA conclusion: [MAY PROCEED / WITH CONDITIONS / MUST NOT PROCEED]
[model knowledge — verify] [review — DPO sign-off required]

**3.4 Security Measures Summary**
- Encryption at rest: [YES/NO — standard]
- Encryption in transit: [YES/NO — standard]
- MFA: [YES/NO]
- Audit logs: [YES/NO — retention: N months]
- Incident response plan: [YES/NO]
- AI: input sanitisation, output filtering, training-data prohibition: [YES/NO/N-A]

**3.5 Residual Risk Summary**
[Table: risk area | inherent | measures | residual]
Overall residual risk: [LOW / MEDIUM / HIGH]
HIGH residual risks: [list or "NONE"]

---

### §4 — DPO Assessment and Sign-Off
*Author: Data Protection Officer*

**4.1 DPIA Completeness Check (Art. 39(7) EUDPR)**
- [✓/✗] §1 — Systematic description of processing (Art. 39(7)(a))
- [✓/✗] §2 — Necessity and proportionality (Art. 39(7)(b))
- [✓/✗] §3 — Risk assessment: likelihood and severity (Art. 39(7)(c))
- [✓/✗] §3 — Measures to address risks (Art. 39(7)(d))
- [✓/✗] §2.7 — Data subject rights implementation (Art. 39(7)(e))
- [✓/✗] §2.1 — Legal basis identified (Art. 39(7)(f))
- [✓/✗] §4 — DPO consultation recorded (Art. 39(7)(g))

**4.2 Risk Consolidation**
Residual risk (security): [LOW / MEDIUM / HIGH]
Legal basis adequacy: [SATISFIED / REQUIRES ADJUSTMENT]
Outstanding concerns: [list or "NONE"]

**4.3 DPO Opinion**
- [ ] FAVOURABLE — Processing may proceed
- [ ] FAVOURABLE WITH CONDITIONS — [list conditions]
- [ ] UNFAVOURABLE — Processing must not proceed; see §4.2

DPO signature / date: _______________ (to be signed by institutional DPO)

[review — DPO sign-off required]

---

### §5 — EDPS Prior Consultation (Art. 40 EUDPR)
*Author: EDPS Assessment Agent*

**5.1 Art. 40 Trigger Assessment**
Residual risk level: [from §3.5]
New type of processing: [YES / NO]
Established safeguards available: [YES / NO]
DPO has identified adequate mitigations: [YES / NO]

**5.2 Determination**

- [ ] **PRIOR CONSULTATION NOT REQUIRED**
  Reasoning: Residual risk is [LOW/MEDIUM]; mitigations are adequate; processing is not of a novel type with unresolved high-risk characteristics.

- [ ] **PRIOR CONSULTATION REQUIRED (Art. 40(1) EUDPR)**
  Reasoning: [Residual risk HIGH / novel processing type / no established safeguard]
  Action: Controller must consult EDPS before commencing processing.
  DPIA dossier to submit: §§1–4 of this document + processor contracts + TIA.
  Estimated EDPS response time: 8 weeks standard; 14 weeks for complex cases
  [model knowledge — verify current EDPS processing timelines]

**5.3 Informal EDPS Consultation (Art. 40(3) EUDPR)**
Where prior consultation is not mandatory but legal uncertainty remains:
- [ ] Informal consultation recommended — [describe uncertainty]
- [ ] Not required

[EDPS — verify opinion reference] [review — DPO sign-off required]

---

*End of DPIA Report*

---

## Constraints

### MUST DO
- Voice all five agent roles in sequence: IT Project Manager → Legal Officer → IT Security → DPO → EDPS.
- Complete all seven Art. 39(7) EUDPR mandatory elements — flag any that cannot be completed with the information provided.
- Rate residual risk numerically on the LOW/MEDIUM/HIGH scale; do not leave risk unrated.
- Trigger Art. 40 prior consultation if residual risk is HIGH — this is non-negotiable under EUDPR.
- Assess AI Act risk tier for any AI-assisted module — flag HIGH-RISK or PROHIBITED classification immediately in §1.5 and escalate to DPO.
- Conduct a TIA for every personal data flow to a non-EU/EEA provider, including AI inference APIs.
- Apply EUDPR (2018/1725), not GDPR (2016/679) — these are distinct instruments.

### MUST NOT DO
- Produce a DPIA with any of the seven Art. 39(7) elements missing without flagging the gap.
- Issue a DPO sign-off opinion without completing the §4.1 completeness checklist.
- Conclude prior consultation is not required where residual risk is HIGH.
- Omit the AI module assessment if the system description includes any AI-assisted component.
- Conflate the EDPS (supervisor for EU institutions) with national DPAs (supervisors for GDPR-subject entities).
- Present DPIA conclusions as final determinations — the document requires DPO sign-off and, where applicable, EDPS prior consultation before the processing commences.

---

## Key Legal Framework — Reference Map

| Instrument | Subject | Key Provision |
|---|---|---|
| Regulation (EU) 2018/1725 (EUDPR) | Data protection — EU institutions | Full framework |
| Art. 39 EUDPR | DPIA — mandatory threshold and content | Mandatory triggers; 7 content elements |
| Art. 40 EUDPR | EDPS prior consultation | Trigger conditions; consultation procedure |
| Arts. 4–5 EUDPR | Principles and legal bases | Lawfulness; purpose limitation; necessity |
| Art. 10 EUDPR | Special categories | Heightened justification |
| Art. 24 EUDPR | Automated decisions | Human review; legal basis |
| Art. 25 EUDPR | International transfers | Adequacy; SCCs; derogations |
| Art. 33 EUDPR | Security of processing | Technical and organisational measures |
| Regulation (EU) 2024/1689 (AI Act) | AI system classification | Risk tiers; Annex III high-risk list |
| EDPS Guidelines on DPIA | DPIA methodology for EU institutions | EDPS list of mandatory DPIAs |

[EUR-Lex — verify current version] [EDPS — verify opinion reference]

---

DRAFT — For review by the Data Protection Officer before use.
Not an official determination. EUDPR compliance requires DPO sign-off and, where applicable, EDPS prior consultation under Art. 40 EUDPR before the processing activity commences.
