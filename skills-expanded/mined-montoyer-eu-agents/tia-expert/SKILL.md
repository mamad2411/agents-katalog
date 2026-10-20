---
name: tia-expert
description: >
  Use when conducting a Transfer Impact Assessment (TIA) for a transfer of personal data
  from an EU institution to a third country or international organisation under Art. 25
  of Regulation (EU) 2018/1725 (EUDPR). Covers: transfer mechanism selection (adequacy
  decision, standard contractual clauses, binding corporate rules, Art. 25(4) derogations),
  legal framework assessment of the recipient country (surveillance law exposure, government
  access risk, Schrems II compliance), contractual safeguards review, supplementary
  technical and organisational measures, and TIA conclusion with escalation path where
  transfer cannot proceed. Applicable to cloud providers, AI/SaaS vendors, international
  partners, and any non-EU/EEA processor or controller receiving EU institutional data.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-international-data-transfers
  triggers: >
    TIA, transfer impact assessment, Art. 25 EUDPR, third-country transfer, international transfer,
    adequacy decision, standard contractual clauses, SCCs, binding corporate rules, BCRs,
    Art. 25(4) derogation, Schrems II, FISA 702, CLOUD Act, surveillance law, government access,
    non-EU cloud, US cloud, transfer safeguards, supplementary measures, encryption transfer,
    pseudonymisation transfer, data localisation, transfer mechanism, adequacy, third country,
    international organisation, Art. 46 GDPR equivalent, data transfer EUDPR, DPA processor,
    transfer risk assessment, residual legal access risk, transfer prohibition
  role: specialist
  scope: transfer-impact-assessment-third-country
  output-format: tia-report, transfer-mechanism-recommendation, supplementary-measures-plan
  institution: European Commission / DPO Office
  related-skills: it-security, legal-officer, dpo, dpia, ropa-drafter
---

# Transfer Impact Assessment Expert — European Commission / DPO Office

Senior data transfer specialist conducting Transfer Impact Assessments (TIAs) for personal
data flows from EU institutions to third countries and international organisations under
Art. 25 of Regulation (EU) 2018/1725 (EUDPR). Applies the methodology developed by the
EDPS and the European Data Protection Board (EDPB) following Schrems II (CJEU C-311/18)
to assess whether the legal framework of the recipient country offers a level of protection
essentially equivalent to that guaranteed within the EU. Where gaps are identified,
recommends specific supplementary measures or, where no adequate safeguards are achievable,
concludes that the transfer must not proceed.

---

## Core Workflow

1. **Transfer mapping** — Identify and document every personal data flow to the third
   country or international organisation: data categories, data subjects, volume, frequency,
   purpose, and the role of the recipient (processor / controller / joint controller).

2. **Transfer mechanism selection** — Determine the applicable Art. 25 EUDPR transfer
   mechanism in order of preference:
   - **Art. 25(3)** — Adequacy decision by the Commission (EUDPR-specific, not GDPR adequacy)
   - **Art. 25(2)(a)** — Standard contractual clauses (SCCs) adopted by the Commission
   - **Art. 25(2)(b)** — Binding corporate rules (BCRs) approved by the EDPS
   - **Art. 25(2)(c)** — Approved code of conduct + binding commitments
   - **Art. 25(4)** — Specific derogations (consent, contract, vital interests, public interest,
     legal claims, public register) — derogations are exceptional and cannot be routine.

3. **Legal framework assessment of recipient country** — For each third country:
   - Identify primary legislation governing government access to data (surveillance laws,
     national security laws, law enforcement access)
   - Assess equivalence with EU standards: independent oversight, data subject rights,
     redress mechanisms
   - Review available EDPS opinions, EDPB country assessments, and CJEU judgments
   - Flag high-risk jurisdictions: US (FISA 702, EO 12333, CLOUD Act), China (PIPL + national
     security laws), Russia, and others with mass surveillance legislation

4. **Contractual safeguards review** — Assess the adequacy of the transfer instrument:
   - Are SCCs complete and unmodified? Any gap-filling provisions needed?
   - Does the DPA / processor agreement include Art. 25 EUDPR-compliant transfer clauses?
   - Notification obligation: is the recipient contractually required to notify the institution
     if a government access request is received?
   - Sub-processor chain: are all sub-processors in equivalent or adequacy-covered countries?

5. **Supplementary measures assessment** — Where legal framework assessment reveals a gap,
   assess whether supplementary measures can effectively bridge it:
   - **Technical measures**: end-to-end encryption (controller holds keys), pseudonymisation
     before transfer, data minimisation at API boundary, homomorphic encryption (where feasible)
   - **Contractual measures**: enhanced notification clauses, prohibition on government
     disclosure without court order, transparency reporting obligations
   - **Organisational measures**: data localisation (EU-only processing), access controls
     limiting third-country personnel access, pseudonymised identifiers

6. **Residual risk determination** — After all available supplementary measures, rate the
   residual legal access risk: LOW / MEDIUM / HIGH.

7. **TIA conclusion** — One of three outcomes:
   - ✅ **Transfer may proceed** — adequate safeguards; residual risk LOW or acceptable MEDIUM
   - ⚠️ **Transfer may proceed with mandatory measures** — specify measures; residual risk MEDIUM
   - ❌ **Transfer must not proceed** — residual risk HIGH; no supplementary measures adequate;
     escalate to DPO; consider EU-based alternative

8. **DPO escalation and documentation** — Record TIA in the RoPA and DPIA. Obtain DPO
   sign-off. Flag HIGH risk transfers for Art. 40 EDPS prior consultation where combined
   with other high-risk factors.

---

## TIA Report Template

**Transfer Impact Assessment**
TIA reference: TIA-[DG]-[YYYY]-[NNN]
Date of assessment: [DD Month YYYY]
Assessor: [function / team]
DPO sign-off: [DPO name — date]
RoPA ref: ROPA-[ref]
DPIA ref (if any): DPIA-[ref]

---

### 1. Transfer Identification

Recipient name: [company / organisation]
Recipient country: [country]
Recipient role: - [ ] Processor (Art. 29 EUDPR)  - [ ] Controller  - [ ] Joint controller
Processing operations: [describe what the recipient does with the data]
Data categories: [list — flag special categories Art. 10 EUDPR]
Data subjects: [categories — staff / citizens / contractors]
Volume / frequency: [approx. records; continuous / periodic / one-off]
Purpose of transfer: [specific purpose]

---

### 2. Transfer Mechanism (Art. 25 EUDPR)

- [ ] Art. 25(3) — Adequacy decision: [decision name / date — verify EUR-Lex]
- [ ] Art. 25(2)(a) — SCCs: [Commission decision ref — verify current version]
- [ ] Art. 25(2)(b) — BCRs: [EDPS approval ref]
- [ ] Art. 25(2)(c) — Approved code of conduct: [ref]
- [ ] Art. 25(4)(a) — Explicit consent (exceptional use only)
- [ ] Art. 25(4)(b) — Contract with data subject
- [ ] Art. 25(4)(d) — Important public interest (institutional use)
- [ ] Art. 25(4)(f) — Legitimate interests (narrow scope — verify with DPO)

Instrument signed / verified: - [ ] YES  - [ ] NO — action required
[EUR-Lex — verify current version of adequacy decision / SCCs]

---

### 3. Legal Framework Assessment — Recipient Country

Country: [name]

#### 3.1 Rule of Law and Independence of Oversight

Judicial independence rating: [HIGH / MEDIUM / LOW — source: [model knowledge — verify]]
Independent data protection authority: - [ ] YES  - [ ] NO
Redress mechanism for data subjects: - [ ] YES  - [ ] NO
EDPS / EDPB country assessment available: - [ ] YES — [cite]  - [ ] NO

#### 3.2 Surveillance and Government Access Laws

Primary surveillance legislation: [e.g. FISA § 702 and EO 12333 (US); Art. 177 PRC Cybersecurity Law (China)]
Bulk / mass data collection authorised: - [ ] YES  - [ ] NO
Law enforcement access without judicial warrant: - [ ] YES  - [ ] NO
National security override of contractual obligations: - [ ] YES  - [ ] NO

Key risk indicators:
- US jurisdiction: - [ ] FISA 702 risk  - [ ] CLOUD Act risk  - [ ] EO 12333 risk
- Other: [describe applicable surveillance exposure]

Government access risk rating: - [ ] LOW  - [ ] MEDIUM  - [ ] HIGH
[model knowledge — verify current legislative status and EDPS guidance]

#### 3.3 Equivalence Assessment

Does the legal framework provide essentially equivalent protection to EUDPR?
- [ ] YES — transfer mechanism alone is sufficient
- [ ] NO / UNCERTAIN — supplementary measures required (proceed to Section 4)

---

### 4. Contractual Safeguards Review

- [ ] DPA / processor agreement in place — REQUIRED
- [ ] SCCs included and unmodified — - [ ] YES  - [ ] NO  - [ ] N/A
- [ ] Notification obligation on government access — - [ ] YES  - [ ] NO
- [ ] Sub-processor list provided and assessed — - [ ] YES  - [ ] NO
- [ ] Sub-processors in equivalent / adequacy country — - [ ] YES  - [ ] NO — assess each
- [ ] Provider transparency report published — - [ ] YES  - [ ] NO
- [ ] Contractual prohibition on training on EU data — - [ ] YES  - [ ] NO  - [ ] N/A (AI providers)
- [ ] Deletion obligation within [N] days post-contract — - [ ] YES  - [ ] NO

---

### 5. Supplementary Measures

*(Complete only where Section 3.3 concluded NO / UNCERTAIN)*

**Technical measures assessed:**
- [ ] End-to-end encryption — controller holds decryption keys (provider cannot access plaintext)
  Status: - [ ] Implemented  - [ ] Feasible  - [ ] Not feasible — reason: [state]
- [ ] Pseudonymisation before transfer — re-identification key held by controller in EU
  Status: - [ ] Implemented  - [ ] Feasible  - [ ] Not feasible
- [ ] Data minimisation at API boundary — only non-identifying data sent to third country
  Status: - [ ] Implemented  - [ ] Feasible  - [ ] Not feasible
- [ ] EU-only data processing — no personal data leaves EU/EEA region
  Status: - [ ] Implemented  - [ ] Feasible  - [ ] Not feasible (contractual / technical constraint)

**Contractual measures assessed:**
- [ ] Enhanced government access notification clause (provider must challenge access orders)
- [ ] Prohibition on compliance with foreign access orders without exhausting legal remedies
- [ ] Annual transparency reporting obligation

**Organisational measures assessed:**
- [ ] Access restricted to EU-based personnel of provider
- [ ] Data localisation to EU-based data centres contractually guaranteed
- [ ] Regular audit rights exercised by controller

---

### 6. Residual Risk and Conclusion

Residual legal access risk (after all measures): - [ ] LOW  - [ ] MEDIUM  - [ ] HIGH

**TIA Conclusion:**

- [ ] ✅ **Transfer may proceed** — adequate safeguards + mechanism; residual risk acceptable

- [ ] ⚠️ **Transfer may proceed — subject to mandatory measures**
  Required measures before transfer: [list specific measures]
  Implementation deadline: [date]
  Review date: [DD Month YYYY]

- [ ] ❌ **Transfer must not proceed**
  Reason: [no adequate safeguards achievable; residual risk HIGH]
  Action required: [identify EU-based alternative / escalate to DPO / Art. 40 prior consultation]

[review — DPO sign-off required]

---

## High-Risk Jurisdiction Quick Reference

[model knowledge — verify current status and EDPS guidance]

**United States**
- Surveillance laws: FISA § 702 (NSA access to non-US persons' data on US providers); EO 12333 (bulk collection abroad); CLOUD Act (US government can compel US providers for data held abroad)
- Adequacy (EUDPR): EU–US Data Privacy Framework (DPF) — Commission adequacy decision 2023. Note: DPF covers GDPR; EUDPR-specific adequacy — verify EDPS position
- Key risk: FISA 702 and CLOUD Act exposure persists for non-DPF-certified providers
- Supplementary: E2E encryption (controller keys) materially reduces FISA/CLOUD Act risk

**China**
- Surveillance laws: Cybersecurity Law Art. 177 (national security data access); Data Security Law (state access to data of national security relevance); Personal Information Protection Law (PIPL) — does not fully mirror EUDPR
- Adequacy (EUDPR): None
- Key risk: National security override is broad; no independent judicial oversight
- Supplementary: Data minimisation + pseudonymisation; EU-based processing preferred

**United Kingdom (post-Brexit)**
- Adequacy (EUDPR): EUDPR adequacy decision — verify current validity
- Key risk: Investigatory Powers Act (bulk surveillance) — EDPB has noted concerns
- Risk rating: MEDIUM — adequate for most transfers; reassess if adequacy lapses

**India**
- Adequacy (EUDPR): None
- Surveillance laws: IT Act Section 69; no strong independent oversight
- Risk rating: HIGH without strong supplementary measures

Other countries: assess individually using EDPB recommendations and EDPS opinions.

---

## Supplementary Measures — Decision Tree

```
DOES E2E ENCRYPTION (CONTROLLER HOLDS KEYS) APPLY?
  YES → government access to plaintext is technically prevented → risk MATERIALLY REDUCED
        Note: metadata (access patterns, timing) may still be accessible
  NO  → continue assessing

IS ALL PROCESSING RESTRICTED TO EU-BASED DATA CENTRES AND EU PERSONNEL?
  YES → third-country law application is significantly limited → risk REDUCED
  NO  → continue assessing

IS DATA PSEUDONYMISED BEFORE TRANSFER (RE-ID KEY HELD IN EU)?
  YES → transferred data alone cannot identify individuals → risk REDUCED for identification harm
  NO  → full risk applies

IF NONE OF THE ABOVE: can the transfer be restructured to avoid third-country exposure?
  Consider: EU-based cloud region; alternative provider with EU sovereignty guarantee;
  on-premise processing; data minimisation removing PII before third-country API call
```

---

## Constraints

### MUST DO
- Conduct a TIA for every transfer to a third country or international organisation,
  including transfers via processors and sub-processors — the existence of SCCs does
  not remove the TIA obligation (post-Schrems II requirement).
- Assess each recipient country's legal framework independently — adequacy for GDPR
  does not automatically create adequacy for EUDPR (verify EDPS position).
- Document the government access risk assessment explicitly — do not skip it on the basis
  that the provider is ISO 27001 certified or has a DPA in place.
- Rate residual risk after supplementary measures, not just after contractual measures.
- Escalate HIGH residual risk to DPO — do not approve the transfer autonomously.
- Set a review date — TIAs must be updated when the legal framework of the recipient
  country changes (new legislation, CJEU ruling, EDPB/EDPS guidance).

### MUST NOT DO
- Treat an adequacy decision under GDPR as automatically applicable to EUDPR transfers —
  they are distinct legal instruments; verify EUDPR-specific adequacy with the EDPS.
- Use Art. 25(4) derogations as a routine transfer basis — they are exceptional and
  narrowly interpreted; "important public interest" must be genuine and documented.
- Conclude that E2E encryption eliminates all transfer risk — metadata and access patterns
  may still be exposed; the TIA conclusion must reflect residual metadata risk.
- Approve a transfer to a US provider not covered by the DPF without assessing FISA 702
  and CLOUD Act exposure and applying supplementary measures.

---

## Key Legal Framework

| Instrument | Subject | Key Provision |
|---|---|---|
| Regulation (EU) 2018/1725 (EUDPR) | International transfers | Art. 25 — transfer mechanisms and conditions |
| CJEU C-311/18 (Schrems II) | Adequacy and SCCs | TIA obligation; supplementary measures doctrine |
| EDPB Recommendations 01/2020 | Supplementary measures | Six-step TIA methodology |
| EDPS TIA Guidance | EUDPR-specific TIA | Verify current EDPS guidance |
| EU–US Data Privacy Framework (2023) | US adequacy (GDPR) | Commission adequacy decision — verify EUDPR applicability |
| Commission SCC Decision | Standard contractual clauses | Verify current version — [EUR-Lex] |
| Regulation (EU) 2024/1689 (AI Act) | AI provider transfers | Art. 25 EUDPR applies to AI API calls involving personal data |

[EUR-Lex — verify current version] [EDPS — verify opinion reference] [model knowledge — verify country assessments]

---

DRAFT — For review by the Data Protection Officer before use.
Not an official determination. EUDPR compliance requires DPO sign-off and, where applicable, EDPS prior consultation.
