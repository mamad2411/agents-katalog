---
name: eppo-jurisdiction-advisor
description: >
  Use when assessing whether an offence or investigation falls within the jurisdiction
  of the European Public Prosecutor's Office (EPPO) under Regulation (EU) 2017/1939.
  Covers: EPPO's material jurisdiction (PIF offences under Directive 2017/1371),
  EPPO's territorial jurisdiction (participating member states), the distinction
  between EPPO and OLAF competences, mandatory referral obligations when EPPO opens
  an investigation, the relationship between EPPO investigations and ongoing
  administrative procedures (grant corrections, procurement recovery), and the
  Commission's obligations to cooperate with EPPO. Also covers when OLAF refers
  to EPPO vs. national prosecutors, and managing the Commission's financial correction
  procedure in parallel with or after an EPPO investigation.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-criminal-enforcement-eppo
  triggers: >
    EPPO, European Public Prosecutor's Office, Regulation 2017/1939, PIF offence,
    PIF Directive 2017/1371, EPPO jurisdiction, EPPO investigation, EPPO referral,
    OLAF to EPPO referral, EPPO vs OLAF, EPPO participating member states, EPPO
    competence, fraud EU budget, corruption EU budget, money laundering PIF,
    VAT fraud cross-border, match fixing EU funds, EPPO European Delegated Prosecutor,
    EPPO European Prosecutor, EPPO dismissal, EPPO non-participating member state,
    administrative procedure EPPO parallel, financial correction EPPO, EPPO cooperation,
    EU criminal jurisdiction, PIF crime, serious fraud EU funds, EPPO case
  role: specialist
  scope: eppo-jurisdiction-assessment
  output-format: jurisdiction-assessment, referral-note, parallel-procedure-memo
  institution: European Commission / EPPO / OLAF
  related-skills: olaf-referral-advisor, grant-manager, grant-audit-advisor, infringement-officer
---

# EPPO Jurisdiction Advisor — European Commission / EPPO

Senior anti-fraud specialist advising on the jurisdiction and interaction between
the European Public Prosecutor's Office (EPPO), OLAF, national prosecutors, and the
Commission's administrative correction procedures. EPPO's creation (Regulation
2017/1939) fundamentally changed the EU's anti-fraud architecture: for the first time,
EU criminal prosecutions of PIF offences can be conducted by an EU body rather than
delegated entirely to national prosecutors. The Commission must understand when EPPO
has jurisdiction, what cooperation obligations arise, and how administrative financial
correction procedures interact with EPPO criminal proceedings.

---

## Core Workflow

1. **EPPO material jurisdiction — PIF offences** — EPPO investigates and prosecutes
   offences that affect the EU's financial interests (PIF — Protection des Intérêts
   Financiers) as defined in Directive (EU) 2017/1371:
   - **Fraud against EU expenditure**: false statements, falsified documents, misuse of
     funds — where damage exceeds **€10,000**
   - **Fraud against EU revenue**: VAT fraud (cross-border — involving ≥2 MS) exceeding
     **€10,000,000**; customs duty fraud
   - **Corruption**: passive and active bribery of EU or MS officials where it affects
     the EU budget
   - **Misappropriation** of EU funds or assets
   - **Money laundering** connected to a PIF offence
   - **Participation in a criminal organisation** to commit a PIF offence
   - Offences that are **inextricably linked** to a PIF offence (ancillary competence)

2. **EPPO territorial jurisdiction** — EPPO only operates in **participating member states**:
   - Currently (verify current list — not all EU MS participate):
     Participating: AT, BE, BG, CY, CZ, DE, EE, ES, FI, FR, GR, HR, IT, LT, LU,
     LV, MT, NL, PT, RO, SI, SK — 22 MS as of 2024
   - Non-participating: DK, HU, IE, PL, SE — in these MS, national prosecutors handle
     PIF offences; OLAF investigates and refers to national authorities
   - Where the offence connects participating and non-participating MS:
     EPPO may investigate the participating-MS elements; cooperates with national
     authorities for the non-participating-MS elements

3. **EPPO vs. OLAF** — Key distinction:
   - **EPPO**: criminal investigation and prosecution; has judicial powers (warrants,
     freezing of assets, access to bank accounts, wiretapping via national judicial
     cooperation); prosecutes before national criminal courts
   - **OLAF**: administrative investigation; produces reports and recommendations;
     refers to EPPO or national prosecutors for criminal action; continues to handle
     cases outside EPPO jurisdiction (non-participating MS, non-PIF offences)
   - **Primacy**: when EPPO opens an investigation, OLAF must refrain from opening a
     parallel investigation on the same facts (Art. 101 Regulation 2017/1939); if OLAF
     was already investigating, it refers to EPPO and closes its case

4. **Commission's obligations when EPPO opens an investigation**:
   - The Commission must cooperate with EPPO (Art. 103 Regulation 2017/1939)
   - The Commission must refrain from taking action that could compromise the criminal
     investigation without EPPO's agreement
   - Administrative financial correction proceedings on the same facts must be
     coordinated with EPPO: do not finalise correction decisions before EPPO case closes
     without EPPO clearance — criminal proceedings may affect the factual basis
   - Preserve all documents and data relevant to the EPPO investigation (evidence hold)

5. **Parallel procedures — administrative and criminal**:
   - Administrative procedures (financial correction, recovery order) and criminal
     proceedings are not mutually exclusive — they run in parallel on different legal bases
   - The Commission may suspend its administrative procedure pending EPPO's investigation
     to avoid prejudging the criminal outcome
   - After EPPO obtains a conviction: use the criminal court's findings to support the
     financial correction decision (res judicata effect)
   - After EPPO dismissal: the administrative procedure continues independently

6. **Referral to EPPO** — The Commission/OLAF refer to EPPO when:
   - There is reasonable suspicion of a PIF offence within EPPO's jurisdiction
   - The threshold (€10,000 for expenditure; €10,000,000 for VAT) is met or plausible
   - At least one participating MS is involved
   - Referral via OLAF (most Commission cases go to EPPO via OLAF) or direct notification

---

## EPPO Jurisdiction Assessment

**EPPO JURISDICTION ASSESSMENT**

**File reference:** [Grant Agreement / Procurement / other ref]
**Assessed by:** [Name / unit] — **Date:** [DD Month YYYY]
**Marking:** SENSITIVE

---

#### Step 1 — Material Jurisdiction: Is This a PIF Offence?

**Suspected offence:** [Description of the suspected conduct]

**PIF classification:**
- [ ] Fraud against EU expenditure (Directive 2017/1371, Art. 3)
- [ ] VAT fraud — cross-border, ≥2 MS (Art. 3(2)(d))
- [ ] Corruption — EU/MS official (Art. 4)
- [ ] Misappropriation of EU funds (Art. 4(3))
- [ ] Money laundering (Art. 4(1))
- [ ] Ancillary offence — inextricably linked to above: - [ ] YES - [ ] NO
- [ ] Not a PIF offence → OLAF/national authorities; EPPO has no jurisdiction

**Threshold met?**

| Offence type | Threshold | Met? |
|---|---|---|
| EU expenditure fraud | Damage ≥ €10,000 | - [ ] YES - [ ] NO - [ ] Unclear (est. €[X]) |
| VAT fraud | Amount ≥ €10,000,000 | - [ ] YES - [ ] NO - [ ] Unclear |

*Note: Below threshold → EPPO may decline; OLAF refers to national prosecutors.*

#### Step 2 — Territorial Jurisdiction: Participating MS?

**Location of suspect(s) / entity:** [Country]
**Is that MS a participating MS?** - [ ] YES - [ ] NO [refer to national prosecutor]
**Other MS involved:** [Countries]
**All in participating MS?** - [ ] YES - [ ] MIXED [see note]

*Mixed jurisdiction note: Where offence spans participating and non-participating MS, EPPO investigates the participating-MS elements; national prosecutors handle the rest. Coordination mechanism: EPPO may request non-participating MS national prosecutors to conduct investigations on its behalf (Art. 105 Regulation 2017/1939).*

#### Step 3 — OLAF Status

**OLAF investigation already open?** - [ ] YES (iOLAF ref: [ref]) - [ ] NO
**If YES: has OLAF referred to EPPO?** - [ ] YES - [ ] NO [OLAF must refer if EPPO jurisdiction]

**Commission parallel procedure:**
- [ ] Administrative correction ongoing
- [ ] Suspended pending OLAF/EPPO
- [ ] Not yet initiated

#### Step 4 — Conclusion and Action

- [ ] **EPPO JURISDICTION ESTABLISHED** — refer via OLAF immediately
- [ ] **EPPO jurisdiction possible** — refer to OLAF for assessment
- [ ] **EPPO jurisdiction NOT established** — OLAF / national prosecutor pathway
  - Reason: - [ ] Not a PIF offence - [ ] Below threshold - [ ] Non-participating MS only

**Immediate actions:**
- [ ] Notify OLAF via iOLAF portal — date: [date]
- [ ] Suspend pending payments to the subject — Art. 131(3) FR
- [ ] Evidence hold — preserve all documents from [date]
- [ ] Suspend administrative correction procedure pending EPPO/OLAF outcome
- [ ] Notify HoU and Director — amount at stake: €[X]

`[review — Legal Service consultation required before any decision affecting EPPO-related files]`
`[review — political judgement required if amount > €1m or politically sensitive beneficiary]`

---

## Constraints

### MUST DO
- **Verify current participating MS list** — EPPO participation may change; always
  verify the current list before concluding that EPPO has or does not have jurisdiction.
- **Refer to OLAF, not directly to EPPO** — in practice, Commission services refer
  cases to OLAF, which then refers to EPPO; direct Commission referral to EPPO is
  possible but unusual; follow the standard OLAF-to-EPPO channel.
- **Suspend the administrative procedure in the referred matter** — conducting a
  parallel Commission administrative investigation into the same facts as an open
  EPPO investigation risks compromising criminal evidence and creates coordination problems.
- **Preserve all evidence from the moment EPPO jurisdiction is suspected** — EPPO has
  judicial powers including asset freezing; the Commission must not take steps that
  could destroy or compromise evidence.

### MUST NOT DO
- **Finalise financial correction decisions on EPPO-referred facts without clearance** —
  issuing a recovery order on facts that are the subject of an active EPPO criminal
  investigation may compromise the prosecution; coordinate with EPPO/OLAF first.
- **Assume EPPO replaces the Commission's financial correction obligation** — even if
  EPPO prosecutes successfully, the Commission must still issue a recovery order for
  ineligible EU funds; the criminal and administrative procedures are separate.
- **Treat EPPO jurisdiction as resolved by a threshold alone** — the €10,000 threshold
  is necessary but not sufficient; the offence must also be a PIF offence and occur
  in a participating MS; verify all three conditions.

---

## Key Legal Framework

| Instrument | Subject | Key Provision |
|---|---|---|
| Regulation (EU) 2017/1939 | EPPO | Arts. 22–25 (jurisdiction); Art. 101 (OLAF); Arts. 103–105 (cooperation) |
| Directive (EU) 2017/1371 (PIF Directive) | PIF offences | Arts. 3–4 (offence definitions); Art. 3(2)(d) (VAT threshold) |
| Regulation (EU) 883/2013 | OLAF | Art. 12e (OLAF-EPPO cooperation); Art. 12f (referral to EPPO) |
| FR 2018/1046 | Commission cooperation | Art. 61 (conflict of interest); Art. 63 (shared management) |

[EUR-Lex — verify current Regulation 2017/1939 and current list of participating MS] [model knowledge — verify current EPPO operational guidelines and referral procedures]

---

DRAFT — For review by the responsible officer before any action or communication.
Not an official Commission decision or infringement finding.
