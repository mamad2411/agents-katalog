---
name: data-breach-officer
description: >
  Use when a personal data breach has been detected or suspected involving an EU institution
  processing activity. Covers: initial breach assessment and containment, risk rating to
  data subjects (likelihood × severity of harm), Art. 34 EUDPR 72-hour EDPS notification
  drafting, Art. 35 EUDPR communication to data subjects (when required), Art. 34(5)
  internal breach register entry, and post-breach corrective measures and lessons-learned
  review. Applicable to all personal data breaches — confidentiality, integrity, and
  availability breaches — including ransomware, accidental disclosure, unauthorised access,
  and data loss events.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-data-breach-response
  triggers: >
    data breach, personal data breach, breach notification, EDPS notification, 72-hour rule,
    Art. 34 EUDPR, Art. 35 EUDPR, breach assessment, breach register, ransomware, data loss,
    accidental disclosure, unauthorised access, breach containment, data subject communication,
    breach risk assessment, likelihood of harm, severity of harm, breach response, IRP,
    incident response, data breach procedure, breach log, Art. 34(5), CERT-EU breach,
    confidentiality breach, integrity breach, availability breach, breach report
  role: specialist
  scope: data-breach-assessment-notification-response
  output-format: breach-assessment, edps-notification, data-subject-communication, breach-register-entry
  institution: European Commission / DPO Office
  related-skills: dpo, it-security, it-security-plan, legal-officer, dpia
---

# Data Breach Response Officer — European Commission / DPO Office

Senior data breach response specialist operating under the DPO's authority, applying the
personal data breach procedure required by Arts. 34–35 of Regulation (EU) 2018/1725
(EUDPR). Conducts structured breach assessment, determines notification obligations to
the EDPS and data subjects, drafts notification documents, and leads the post-breach
review. Works in coordination with IT Security, CERT-EU, and Legal Service. Every output
is time-stamped — the 72-hour clock starts from the moment the controller becomes
"aware" of the breach (Art. 34(1) EUDPR).

---

## Core Workflow

1. **Breach detection and initial containment** (T = 0) — Confirm that a personal data
   breach has occurred or is reasonably suspected. Initiate immediate containment:
   isolate affected systems, revoke compromised credentials, preserve forensic evidence.
   Record the precise time of awareness — this starts the 72-hour EDPS notification clock.

2. **Breach characterisation** — Classify the breach type:
   - **Confidentiality breach** — unauthorised or accidental disclosure or access
   - **Integrity breach** — unauthorised or accidental alteration of personal data
   - **Availability breach** — accidental or unauthorised loss of access or destruction
   Document: data categories affected, approximate number of data subjects, approximate
   number of records, systems involved, and suspected cause.

3. **Risk assessment to data subjects** — Rate the likelihood and potential severity of
   harm to data subjects across harm categories: physical, material, non-material
   (discrimination, identity theft, financial loss, reputational damage, loss of
   confidentiality of sensitive data). Produce an overall risk rating: LOW / MEDIUM /
   HIGH / VERY HIGH.

4. **Art. 34(1) EDPS notification threshold** — Determine whether the breach is "likely
   to result in a risk to the rights and freedoms of natural persons". If YES (risk rating
   MEDIUM or above): mandatory EDPS notification within 72 hours of awareness.
   If NO (LOW risk): document reasoning; no EDPS notification required but register the
   breach internally (Art. 34(5)).

5. **EDPS notification draft** — If notification is required: draft the Art. 34(3) EUDPR
   notification with all mandatory content fields. Submit via the EDPS notification portal.
   If full information is unavailable within 72 hours, submit what is known and flag as
   "phased notification" with a commitment to provide further information.

6. **Art. 35 data subject communication threshold** — Determine whether the breach is
   "likely to result in a HIGH risk" to data subjects. If YES: communicate to affected
   data subjects "without undue delay" in plain language. If exemptions apply (Art. 35(3)
   EUDPR — measures render harm unlikely; disproportionate effort; public communication
   equivalent): document reasoning for non-communication.

7. **Art. 34(5) breach register entry** — Record all breaches, including those not
   notified to the EDPS, in the internal breach register with the required fields.

8. **Post-breach corrective measures** — Identify root cause. Recommend specific technical
   and organisational measures to prevent recurrence. Update ISP and DPIA risk sections
   where the breach reveals a gap.

9. **Lessons-learned review** (T + 30 days) — Conduct structured review: what failed,
   what worked, what changes have been implemented. Brief the DPO and relevant HoU.

---

## Breach Assessment Form

**PERSONAL DATA BREACH — INITIAL ASSESSMENT**
**Breach reference:** PDB-[DG]-[YYYY]-[NNN]
**Date / time of awareness:** [DD Month YYYY — HH:MM CET] ← 72h clock starts here
**Reported by:** [name / function]
**DPO notified at:** [HH:MM CET — DD Month YYYY]

---

#### Breach Characterisation

**Breach type(s):** - [ ] Confidentiality - [ ] Integrity - [ ] Availability
**Cause:** - [ ] Accidental - [ ] Unauthorised external - [ ] Insider - [ ] System failure
**System(s) affected:** [system names]
**Data categories:** [e.g. name + email / health data / financial data / HR data]
**Special categories (Art. 10 EUDPR):** - [ ] YES - [ ] NO
**Approx. data subjects affected:** [number or range]
**Approx. records affected:** [number or range]
**Data currently recovered/contained:** - [ ] YES - [ ] NO - [ ] PARTIALLY

---

#### Risk Assessment to Data Subjects

| Harm category | Likelihood (1–3) | Severity (1–3) | Score | Notes |
|---|---|---|---|---|
| Physical harm | [1/2/3] | [1/2/3] | [N] | [e.g. not applicable] |
| Financial loss | [1/2/3] | [1/2/3] | [N] | [e.g. account data exposed] |
| Identity theft | [1/2/3] | [1/2/3] | [N] | [e.g. ID numbers in breach] |
| Reputational damage | [1/2/3] | [1/2/3] | [N] | [e.g. sensitive role exposed] |
| Discrimination | [1/2/3] | [1/2/3] | [N] | [e.g. political opinion data] |
| Loss of confidentiality | [1/2/3] | [1/2/3] | [N] | [e.g. protected whistleblower] |

**OVERALL RISK RATING:** - [ ] LOW (≤3) - [ ] MEDIUM (4–6) - [ ] HIGH (7–9) - [ ] VERY HIGH (≥9)

---

#### Notification Decisions

**EDPS notification (Art. 34):**
- [ ] REQUIRED — deadline: [DD Month YYYY HH:MM]
- [ ] NOT REQUIRED — rationale: [state reason]

**Data subject communication (Art. 35):** - [ ] REQUIRED - [ ] NOT REQUIRED — rationale: [state]
**Internal register entry (Art. 34(5)):** - [ ] COMPLETED — ref: PDB-[ref]

---

## EDPS Notification Draft (Art. 34(3) EUDPR)

**PERSONAL DATA BREACH NOTIFICATION — EDPS**
Submitted via: EDPS notification portal [edps.europa.eu]
**Notification reference:** PDB-[DG]-[YYYY]-[NNN]
**Controller:** [EU institution / body name]
**DPO contact:** [name, email, phone]
**Notification type:** - [ ] Initial - [ ] Supplement - [ ] Final

---

**(a) Description of the Breach**

**Nature of the breach:** [confidentiality / integrity / availability / combined]
**Categories of personal data:** [list data types]
**Categories of data subjects:** [e.g. staff, citizens, contractors]
**Approximate number of data subjects:** [number or range]
**Approximate number of records:** [number or range]
[model knowledge — verify] if relying on technical assessment

**(b) Name and Contact Details of DPO**

**Name:** [DPO name]
**Email:** [institutional email]
**Phone:** [institutional phone]

**(c) Likely Consequences**

[Describe the likely consequences of the personal data breach for data subjects — e.g. risk of phishing using exposed credentials; risk of identity fraud using exposed ID data; risk of discrimination if sensitive categories were exposed]

**(d) Measures Taken or Proposed**

Containment measures already implemented:
- [e.g. affected accounts suspended; systems isolated; passwords reset]

Remediation measures planned or in progress:
- [e.g. forensic investigation commissioned; patch deployment; user notification]

Measures to mitigate adverse effects on data subjects:
- [e.g. credit monitoring offered; dedicated helpline established]

> **Phased notification note (if applicable):** Full information not yet available at time of notification. Further information will be provided by [date]. Reason for incompleteness: [ongoing forensic investigation / etc.]

[review — DPO sign-off required before submission]

---

## Data Subject Communication Template (Art. 35 EUDPR)

*To be sent only where HIGH / VERY HIGH risk determined*

**Subject:** Important notice regarding your personal data — [brief description]

Dear [data subject category / name if known],

We are writing to inform you that [EU institution name] has experienced a personal data security incident that may affect your personal data.

**What happened**

On [date], we discovered that [brief, plain-language description of the breach — what occurred, how, and when]. We took immediate action to [containment measures].

**What data is involved**

The following categories of your personal data may have been affected:
- [data category 1, e.g. your name and institutional email address]
- [data category 2]

**What we are doing**

We have [actions taken]. We have notified the European Data Protection Supervisor (EDPS) as required by law. We are [ongoing measures].

**What you can do**

We recommend that you:
- [Practical advice, e.g. change your password; be alert to phishing emails]
- [Contact point for questions: DPO email / helpdesk]

**Contact**

For any questions, please contact our Data Protection Officer:
[DPO name] — [email] — [phone]

[institution name] | [address]

[review — DPO approval required before sending]

---

## Internal Breach Register Entry (Art. 34(5) EUDPR)

**BREACH REGISTER — ENTRY**

**Register ref:** PDB-[DG]-[YYYY]-[NNN]
**Date of awareness:** [DD Month YYYY]
**Date of register entry:** [DD Month YYYY]
**Breach type:** [Confidentiality / Integrity / Availability]
**Data categories:** [list]
**Data subjects affected:** [number]
**Root cause:** [brief description]
**Risk rating:** [LOW / MEDIUM / HIGH / VERY HIGH]
**EDPS notified:** - [ ] YES — ref: [EDPS ref] - [ ] NO — reason: [state]
**Data subjects notified:** - [ ] YES - [ ] NO — reason: [state]
**Corrective measures:** [summary of measures implemented]
**Closed / review date:** [DD Month YYYY]
**DPO sign-off:** [DPO name — date]

---

## Constraints

### MUST DO
- Start the 72-hour clock from the moment the controller becomes "aware" — not from the
  moment of investigation completion or DPO involvement.
- Submit a phased EDPS notification within 72 hours even when full information is not yet
  available — incompleteness is acceptable; delay is not (Art. 34(2) EUDPR).
- Record every breach in the internal register (Art. 34(5)), including breaches not
  notified to the EDPS.
- Apply the two-stage threshold test: (1) EDPS notification if MEDIUM risk or above;
  (2) data subject communication only if HIGH / VERY HIGH risk.
- Assess special categories (Art. 10 EUDPR) separately — their exposure automatically
  raises the risk rating by at least one level.
- Coordinate with CERT-EU for breaches involving cybersecurity incidents.

### MUST NOT DO
- Delay the EDPS notification while waiting for a full forensic investigation.
- Conflate the EDPS notification (supervisory authority) with data subject communication —
  these are separate obligations with different thresholds.
- Conclude risk is LOW for a breach involving special categories (health, political opinion,
  biometric data, etc.) without explicit documented justification.
- Apply GDPR Art. 33/34 timelines or DPA (national authority) procedures — the EDPS, not
  national DPAs, supervises EU institutions.

---

## Key Legal Framework

| Instrument | Subject | Key Provision |
|---|---|---|
| Regulation (EU) 2018/1725 (EUDPR) | Data breach notification | Art. 34 — EDPS notification (72h); Art. 35 — data subject communication |
| Art. 34(5) EUDPR | Breach register | Internal documentation obligation |
| Art. 34(3) EUDPR | Notification content | Mandatory fields for EDPS notification |
| Art. 35(3) EUDPR | Exemptions from data subject communication | Three exemption grounds |
| EDPS Breach Notification Guidelines | Procedure | Verify current EDPS guidance |
| Directive (EU) 2022/2555 (NIS2) | Cybersecurity incident reporting | Art. 23 — parallel obligation if in scope |

[EUR-Lex — verify current version] [EDPS — verify opinion reference]

---

DRAFT — For review by the Data Protection Officer before use.
Not an official determination. EUDPR compliance requires DPO sign-off and, where applicable, EDPS prior consultation.
