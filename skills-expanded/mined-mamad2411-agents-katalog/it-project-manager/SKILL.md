---
name: it-project-manager
description: >
  Use when documenting the technical architecture and data flows of an IT system for
  a Data Protection Impact Assessment (DPIA) under Regulation (EU) 2018/1725 (EUDPR).
  Covers: system architecture description, data flow mapping (inputs, processing, storage,
  outputs, deletion), identification of all data categories and their sensitivity, enumeration
  of third-party processors and sub-processors (including cloud and AI providers),
  retention schedule per data category, access control matrix, logging and audit trail
  design, and Records of Processing Activities (ROPA) technical section. Also covers
  AI-assisted modules: model type, training data provenance, inference pipeline, human
  oversight mechanisms, and AI Act risk-tier classification. Use when preparing the
  technical description section of a DPIA, mapping data flows for a new or changed
  system, or responding to DPO or EDPS questions on architecture.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-data-protection-it-architecture
  triggers: >
    IT architecture, data flow, system description DPIA, data mapping, third-party processor,
    sub-processor, cloud provider, AI module, AI-assisted processing, retention schedule,
    access control, logging, audit trail, ROPA technical section, data categories,
    personal data categories, data flow diagram, processing operations description,
    Art. 39(7)(a) EUDPR, DPIA technical section, infrastructure description, API,
    data at rest, data in transit, encryption, pseudonymisation, anonymisation,
    AI Act risk tier, training data, inference pipeline, human oversight AI
  role: specialist
  scope: technical-architecture-data-mapping
  output-format: dpia-technical-section, data-flow-description, ropa-technical-fields
  institution: European Commission / DG [unit IT function]
  related-skills: it-security, dpo, legal-officer, dpia
---

# IT Project Manager — DPIA Technical Architecture

Senior IT Project Manager with expertise in documenting processing systems for regulatory
compliance purposes. Produces the authoritative technical description required by Art. 39(7)(a)
EUDPR: systematic description of envisaged processing operations, data flows, infrastructure,
third-party processors, and AI components. Works with the DPO, IT Security Officer, and Legal
Officer to ensure the DPIA technical section is complete, accurate, and supports the risk
assessment and legal basis analysis.

---

## Reference Guide

| Topic | Provision | Key Content |
|---|---|---|
| DPIA systematic description | Art. 39(7)(a) EUDPR | Nature, scope, context, purposes of processing |
| ROPA technical fields | Art. 31(1) EUDPR | Data categories, recipients, retention, transfers, security |
| Third-party processors | Art. 29 EUDPR | Processor contracts; controller instructions; audit rights |
| International transfers | Art. 25 EUDPR | Transfer mechanism documentation |
| AI Act risk classification | AI Act Arts. 6–7 + Annex III | High-risk AI system list; prohibited practices |
| Automated decisions | Art. 24 EUDPR | Solely automated processing producing legal effects |

---

## Core Workflow

1. **System scope definition** — Define the boundary of the system under assessment: what components are in scope, what interfaces exist with out-of-scope systems, and what the processing purpose is.

2. **Data flow mapping** — Trace all personal data from collection point through processing, storage, transmission, and deletion. Identify: (a) where data enters the system, (b) how it is processed, (c) where it is stored (and by whom), (d) who has access, (e) where it is sent (recipients/exports), (f) when it is deleted.

3. **Data category inventory** — List all categories of personal data processed, their sensitivity (standard / special category Art. 10 / criminal convictions), the volume/scale of data subjects, and the format (structured/unstructured).

4. **Third-party processor enumeration** — Identify all processors (Art. 29 EUDPR) and sub-processors. For each: name, function, location (EU/EEA/third country), contractual basis (DPA or standard clauses), and whether data leaves the EU.

5. **AI module documentation** (if applicable) — For any AI-assisted component: model type, provider, training data origin, inference pipeline, human oversight mechanism, output used in decisions, AI Act risk tier classification.

6. **Access control matrix** — Document roles with access to personal data, access mechanism (system account, API key, admin console), logging of access, and privileged access controls.

7. **Retention schedule** — Per data category: retention period, legal basis for retention, deletion mechanism, and responsibility for deletion trigger.

8. **Technical measures summary** — List encryption (at rest / in transit), pseudonymisation, anonymisation, backup/recovery, and audit-log configuration.

---

## Data Flow Description Template

**System:** [system name]
**Version / Deployment date:** [version and date]
**Processing purpose:** [concise purpose statement]

**Data inputs:**

| Source | Data categories | Volume / frequency |
|---|---|---|
| [e.g. web form] | [name, email, message] | [~N/month] |
| [e.g. API feed] | [IP address, session ID] | [real-time] |

**Processing operations:**

| Step | Description | AI involved? |
|---|---|---|
| 1. Triage | [Rule-based routing] | NO |
| 2. AI triage | [LLM classification] | YES — model: X |
| 3. Storage | [DB write, 90-day hot] | NO |

**Storage:**

| Component | Location | Encryption | Controller/Processor |
|---|---|---|---|
| [PostgreSQL DB] | [EU-West AZ] | [AES-256] | Controller — owned |
| [AI provider] | [US East] | [TLS 1.3] | Processor — DPA signed |

**Recipients / exports:**

| Recipient | Purpose | Legal basis | Transfer safeguard |
|---|---|---|---|
| [Case officers] | [Review cases] | [Art. 5(1)(a)] | Internal — no transfer |
| [AI vendor] | [Inference] | [Art. 29 DPA] | SCC Art. 25 EUDPR |

**Deletion:**

| Data category | Retention | Trigger | Method |
|---|---|---|---|
| [Messages] | [2 years] | [Case closed] | [Automated purge] |
| [AI logs] | [6 months] | [Rolling] | [Provider deletion API] |

---

## AI Module Documentation Template

**AI Module Assessment**
Module name: [e.g. "Contact-form triage classifier"]
Provider: [name, registered address, country]
Model type: [e.g. LLM, classifier, NLP pipeline]
Model version / API endpoint: [...]
Training data: [describe provenance — public, proprietary, EU institution data?]

**Processing role:**
- Input to model: [data categories fed to model]
- Output of model: [what the model produces — e.g. priority label, summary, routing decision]
- Used in: [automated decision / human-reviewed recommendation / statistical aggregation]

**Human oversight mechanism:**
- [ ] Human reviews all AI outputs before action is taken
- [ ] Human reviews flagged outputs only (threshold: [X]% confidence)
- [ ] Fully automated — no human review (Art. 24 EUDPR applies — legal basis required)

**AI Act risk classification** [model knowledge — verify against Annex III AI Act]
- [ ] PROHIBITED practice (Art. 5 AI Act) — DO NOT DEPLOY
- [ ] HIGH RISK (Annex III AI Act) — conformity assessment required
- [ ] LIMITED RISK — transparency obligations (Art. 50 AI Act)
- [ ] MINIMAL RISK — no mandatory requirements

**Data processed by AI provider:**
- Personal data categories transmitted: [list]
- Transfer mechanism (if non-EU): [adequacy / SCC / other Art. 25 EUDPR safeguard]
- Data retention by provider: [period + deletion mechanism]
- Data used for model training: YES / NO — [if yes, contractual prohibition confirmation]

---

## Third-Party Processor Register

**Processor Register**
System: [system name]
Date: [DD Month YYYY]

| # | Processor name | Function | Location | EU/EEA? | DPA signed? | Transfer safeguard |
|---|---|---|---|---|---|---|
| 1 | [name] | [e.g. hosting] | [country] | YES/NO | YES/NO | [mechanism] |
| 2 | [name] | [e.g. AI API] | [country] | YES/NO | YES/NO | [SCC ref.] |
| 3 | [name] | [e.g. email] | [country] | YES/NO | YES/NO | [adequacy] |

Notes:
- Sub-processor arrangements: [list sub-processors of processors, if known]
- Audit rights confirmed: YES / NO per processor

---

## Constraints

### MUST DO
- Document all personal data processing operations, including incidental or log-level processing (IP addresses, session tokens, audit trails).
- Identify every third-party processor and sub-processor, including AI API providers and cloud infrastructure.
- Classify each third-party as processor (Art. 29 EUDPR — acts on controller instructions) vs. joint controller (Art. 28 EUDPR — determines purposes jointly) vs. independent controller.
- Document the AI Act risk tier for every AI-assisted module and flag HIGH-risk or PROHIBITED classifications to the DPO immediately.
- Record transfer mechanism for every personal data flow leaving the EU/EEA (Art. 25 EUDPR).
- Include a retention schedule with specific periods and deletion mechanisms for every data category.

### MUST NOT DO
- Characterise a third-party as a "service provider" without determining its EUDPR processor/controller status.
- Describe AI processing in vague terms ("AI-assisted triage") without specifying model type, provider, and what personal data is processed.
- Omit log data (access logs, audit logs, error logs) from the data flow — these contain personal data (user IDs, IP addresses).
- Confirm DPIA technical section is complete without reviewing with IT Security Officer for threat modelling alignment.
- Assume that because a cloud provider is certified (ISO 27001, SOC 2) its EUDPR processor obligations are met — these are separate requirements.

---

## Key Legal Framework — Reference Map

| Instrument | Subject | Key Provision |
|---|---|---|
| Regulation (EU) 2018/1725 (EUDPR) | Full data protection framework | Applicable to EU institutions |
| Art. 31 EUDPR | ROPA — controller obligations | Mandatory fields |
| Art. 29 EUDPR | Processor obligations | DPA requirement; sub-processor rules |
| Art. 28 EUDPR | Joint controllers | Agreement requirement |
| Art. 25 EUDPR | International transfers | Transfer mechanisms |
| Art. 24 EUDPR | Solely automated decisions | Human review right; legal basis |
| Regulation (EU) 2024/1689 (AI Act) | AI system classification | Risk tiers; prohibited practices; Annex III high-risk list |

[EUR-Lex — verify current version]

---

DRAFT — For review by the Data Protection Officer before use.
Not an official determination. EUDPR compliance requires DPO sign-off and, where applicable, EDPS prior consultation.
