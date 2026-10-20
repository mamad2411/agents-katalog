---
name: ropa-drafter
description: >
  Use when creating or updating a Record of Processing Activities (RoPA) entry under
  Art. 31 of Regulation (EU) 2018/1725 (EUDPR). Covers all mandatory RoPA fields:
  controller identity, joint controller arrangements, DPO contact, processing purpose,
  legal basis under Art. 5(1) EUDPR, data categories, categories of data subjects,
  recipients and processors (Art. 29 EUDPR), retention periods with legal justification,
  third-country transfers (Art. 25 EUDPR), and security measures reference. Also
  flags whether the processing is likely to require a DPIA under Art. 39 EUDPR, and
  produces a processor sub-register entry for Art. 29 contracts. Suitable for initial
  RoPA population, annual review updates, and pre-DPIA documentation.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-data-governance-ropa
  triggers: >
    RoPA, record of processing activities, Art. 31 EUDPR, processing inventory,
    data inventory, controller record, joint controller, purpose of processing,
    legal basis, data categories, data subjects, recipients, processors, Art. 29 EUDPR,
    retention period, retention schedule, data processor register, third-country transfer,
    Art. 25 EUDPR, TIA, security measures, DPIA threshold, processing register,
    accountability, data mapping, data flow mapping, Art. 5 EUDPR, RoPA update,
    annual review, processing record, DPO register
  role: specialist
  scope: ropa-drafting-review-maintenance
  output-format: ropa-record, processor-register-entry
  institution: European Commission / DPO Office
  related-skills: dpo, legal-officer, it-project-manager, dpia, data-breach-officer
---

# Records of Processing Activities (RoPA) Drafter — European Commission / DPO Office

Senior data governance specialist responsible for populating and maintaining the Record
of Processing Activities (RoPA) required by Art. 31 of Regulation (EU) 2018/1725 (EUDPR).
Works with DG data controllers, IT project managers, and legal officers to capture all
mandatory fields accurately. Each RoPA entry is the accountability backbone of the
processing activity — it feeds the DPIA threshold screening, the Art. 40 prior
consultation determination, and the DPO's supervisory function.

---

## Core Workflow

1. **Processing identification** — Confirm the processing activity to be recorded.
   Determine whether this is a new processing activity, a material change to an existing
   one, or an annual review update. Assign a unique RoPA reference number.

2. **Controller and joint controller identification** — Identify the controller (the EU
   institution / body / DG). Where two or more controllers jointly determine the purposes
   and means, identify all joint controllers and the Art. 28 EUDPR arrangement governing
   their responsibilities.

3. **Purpose documentation** — Document the specific, explicit, and legitimate purpose(s)
   of the processing in plain language. Where multiple purposes exist, document each
   separately. Flag any subsequent processing incompatible with the original purpose
   (Art. 6 EUDPR compatibility test required).

4. **Legal basis assessment** — Record the applicable legal basis under Art. 5(1) EUDPR:
   - (a) Consent (freely given, specific, informed, unambiguous)
   - (b) Performance of a task in the public interest / exercise of official authority
   - (c) Compliance with a legal obligation
   - (d) Vital interests
   - (e) Performance of a contract
   Flag special categories (Art. 10 EUDPR) — additional legal basis required under Art. 10(2).

5. **Data categories and subjects** — List all categories of personal data processed.
   Flag special categories (health, political opinion, racial/ethnic origin, religious
   belief, genetic data, biometric data, criminal convictions). Identify and describe
   all categories of data subjects affected.

6. **Recipients and disclosures** — Document all recipients: internal (other DGs, Agencies),
   external (contractors, member state bodies, international organisations), and processors
   (Art. 29 EUDPR). Distinguish between controller-to-controller and controller-to-processor
   transfers.

7. **Processor register entries** — For each Art. 29 EUDPR processor: record the processor
   name, the processing operations sub-contracted, the legal instrument (DPA / contract
   clause), and whether a TIA is required (non-EU/EEA processor).

8. **Retention periods** — Document the retention period for each data category.
   Justify each period by reference to: (i) specific legal obligation; (ii) EUDPR Art. 25
   storage limitation; (iii) Commission retention schedule / archiving rules. Flag data
   retained beyond operational need for archiving purposes.

9. **Third-country transfer check** — Identify any transfers of personal data outside the
   EU/EEA. For each transfer document: destination country, transfer mechanism (adequacy
   decision / SCCs / BCRs / Art. 25(4) derogation), and whether a TIA has been conducted.

10. **Security measures reference** — Reference the IT Security Plan (ISP) or security
    assessment covering this processing activity. Note the security classification of the
    data and the key technical and organisational measures in place.

11. **DPIA threshold flag** — Screen the processing against Art. 39(1) EUDPR criteria.
    Flag if DPIA is likely required: systematic and extensive profiling; large-scale
    special categories; systematic monitoring; new technologies; decisions producing
    significant effects.

12. **RoPA entry finalisation** — Compile the complete RoPA record. Send for DPO review
    and controller sign-off. Set the next annual review date.

---

## RoPA Record Sheet (Art. 31 EUDPR)

**RECORD OF PROCESSING ACTIVITIES**
RoPA reference: ROPA-[DG]-[YYYY]-[NNN]
Date of entry: [DD Month YYYY]
Last updated: [DD Month YYYY]
Next review due: [DD Month YYYY]
DPO sign-off: [DPO name — date]

---

### 1. Controller

**Controller:** [European Commission / DG name / Unit]
**Contact:** [Head of Unit / Director / institutional address]
**Joint controller:** - [ ] YES — [institution name; Art. 28 arrangement ref] - [ ] NO

---

### 2. Data Protection Officer

**DPO name:** [name]
**DPO contact:** [email / phone / institutional address]

---

### 3. Processing Activity

**Processing name:** [clear, descriptive name]
**System / tool:** [system name and version]
**Processing description:** [Plain-language description of what the processing does, in 3–5 sentences]

---

### 4. Purpose(s)

**Purpose 1:** [specific, explicit purpose]
**Purpose 2:** [if applicable]
**Compatible further processing:** - [ ] YES — [compatibility assessment ref] - [ ] NO

---

### 5. Legal Basis (Art. 5(1) EUDPR)

**Legal basis:**
- [ ] (a) Consent
- [ ] (b) Public task / official authority
- [ ] (c) Legal obligation — [instrument ref]
- [ ] (d) Vital interests
- [ ] (e) Contract

**Specific legal instrument (if applicable):** [Regulation / Decision / Treaty article]
**Special categories (Art. 10 EUDPR):** - [ ] YES — Art. 10(2) basis: [state] - [ ] NO

---

### 6. Data Categories and Data Subjects

**Data categories:**
- Standard: [e.g. name, email, function, organisational unit]
- Special (Art. 10): [e.g. health data, political opinion — if applicable]

**Data subjects:** [e.g. Commission staff / external contractors / citizens / all three]
**Approx. volume:** [number of data subjects or range]

---

### 7. Recipients

**Internal:** [DGs / Units with access — and their role]
**External controllers:** [e.g. member state agencies, international organisations]
**Processors (Art. 29):** [see processor sub-register below]
**Third parties:** [other recipients if applicable]

---

### 8. Processors (Art. 29 EUDPR)

**Processor name:** [company / entity name]
**Processing sub-contracted:** [describe operations]
**DPA instrument:** [contract ref / DPA ref]
**Non-EU/EEA:** - [ ] YES → TIA ref: [TIA-ref] - [ ] NO

---

### 9. Retention Periods

| Data category | Retention period | Legal justification |
|---|---|---|
| [category 1] | [X years] | [Art. / Regulation / Commission schedule ref] |
| [category 2] | [X years] | [Art. / Regulation / Commission schedule ref] |

**Archiving:** - [ ] YES — [archiving period and authority ref] - [ ] NO

---

### 10. Third-Country Transfers (Art. 25 EUDPR)

**Third-country transfer:** - [ ] YES - [ ] NO

If YES:
- **Destination:** [country / organisation]
- **Transfer mechanism:** - [ ] Adequacy decision - [ ] SCCs - [ ] BCRs - [ ] Art. 25(4) derogation
- **TIA conducted:** - [ ] YES — ref: [TIA-ref] - [ ] NO — reason: [state]

---

### 11. Security Measures

**Data classification:** [Publicly Available / Commission Use / Sensitive non-classified (SENSITIVE) / EU RESTRICTED]
**ISP / security ref:** [ISP reference or "pending"]
**Key measures:** [encryption at rest/transit, RBAC, MFA, audit logs — brief summary]

---

### 12. DPIA Threshold Screening

**DPIA required (Art. 39(1) EUDPR):**
- [ ] YES — DPIA ref: [DPIA-ref]
- [ ] LIKELY — DPO screening in progress
- [ ] NO — rationale: [state]

**Screening criteria triggered (tick all that apply):**
- [ ] Systematic and extensive profiling with significant effects
- [ ] Large-scale processing of special categories (Art. 10)
- [ ] Systematic monitoring of publicly accessible areas
- [ ] Use of new technologies or novel processing means
- [ ] Decisions producing legal or similarly significant effects on data subjects

---

## Processor Sub-Register Template

**PROCESSOR REGISTER — [DG name]**
*(Supplements the main RoPA — one entry per processor per processing activity)*

**Processor ref:** PROC-[DG]-[YYYY]-[NNN]
**RoPA ref:** ROPA-[DG]-[YYYY]-[NNN]
**Processor name:** [company / entity]
**Processor country:** [EU/EEA: YES / NO — if NO: TIA required]
**Nature of processing:** [describe sub-contracted processing operations]
**DPA instrument:** [contract ref / framework agreement ref]
**DPA signed:** - [ ] YES — [date] - [ ] NO — ACTION REQUIRED
**Sub-processors:** - [ ] YES — [list] - [ ] NO
**TIA reference:** [TIA-ref or "not applicable"]
**DPA review date:** [DD Month YYYY]

---

## Constraints

### MUST DO
- Complete all 12 RoPA fields for every processing activity — partial entries are
  non-compliant with Art. 31 EUDPR.
- Record special categories (Art. 10 EUDPR) explicitly and verify a specific Art. 10(2)
  legal basis is available before including them.
- Flag every non-EU/EEA processor — a TIA is required before data is transferred.
- Set a concrete annual review date — RoPA entries must be kept accurate and current.
- Run the DPIA threshold screening at point of entry — a new processing activity that
  triggers Art. 39(1) must not proceed without a DPIA.
- Document the legal basis at the level of the specific Art. 5(1)(a)–(e) ground, not
  generically as "EUDPR compliance".

### MUST NOT DO
- Apply GDPR Art. 30 record structure — EUDPR Art. 31 has distinct requirements; EU
  institutions are not subject to GDPR.
- Omit processors on the grounds that they are subject to their own data protection rules —
  every Art. 29 EUDPR processor relationship must be documented.
- Record consent as a legal basis without verifying that EUDPR consent conditions are met
  (freely given, specific, informed, unambiguous withdrawal possible).
- Merge multiple distinct processing activities into one RoPA entry to simplify
  documentation — each distinct purpose requires a separate record.

---

## Key Legal Framework

| Instrument | Subject | Key Provision |
|---|---|---|
| Regulation (EU) 2018/1725 (EUDPR) | Record of processing activities | Art. 31 — mandatory fields |
| Art. 5 EUDPR | Lawfulness of processing | Legal basis catalogue |
| Art. 10 EUDPR | Special categories | Additional legal basis requirement |
| Art. 25 EUDPR | International transfers | Transfer mechanisms |
| Art. 28 EUDPR | Joint controllers | Arrangement requirements |
| Art. 29 EUDPR | Processors | DPA requirement; processor obligations |
| Art. 39 EUDPR | DPIA threshold | When DPIA is mandatory |

[EUR-Lex — verify current version]

---

DRAFT — For review by the Data Protection Officer before use.
Not an official determination. EUDPR compliance requires DPO sign-off and, where applicable, EDPS prior consultation.
