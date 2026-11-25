---
name: edps-complaint-handler
description: >
  Use when responding to a complaint or supervisory inquiry from the European Data
  Protection Supervisor (EDPS) under Regulation (EU) 2018/1725 (EUDPR). Covers:
  understanding the EDPS's Art. 57 supervisory powers, handling the EDPS's
  questionnaire or request for information (Art. 58(1) investigative powers),
  drafting the Commission's formal response, managing the contradictory procedure
  before an EDPS corrective decision (Art. 58(2) corrective powers), preparing and
  implementing a remedial action plan, managing EDPS audit visits, and the appeal
  pathway to the CJEU (Art. 263 TFEU) if an EDPS decision is contested. Distinct
  from the preventive privacy skills (dpo, dpia, ropa-drafter) — this skill handles
  the adversarial situation where the EDPS is already investigating.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-privacy-supervisory
  triggers: >
    EDPS complaint, EDPS inquiry, EDPS investigation, EDPS questionnaire, EDPS audit,
    European Data Protection Supervisor, Art. 57 EUDPR, Art. 58 EUDPR, supervisory
    powers, EDPS corrective decision, EDPS formal notice, EDPS reprimand, EDPS ban,
    EDPS order to comply, EDPS investigation EU institution, data protection complaint
    EU institution, EDPS response, EDPS remedial action, EDPS follow-up, EDPS appeal,
    EUDPR complaint procedure, Art. 64 EUDPR complaint, Regulation 2018/1725,
    EDPS prior consultation, EDPS opinion, EDPS recommendation implementation
  role: specialist
  scope: edps-complaint-supervisory-response
  output-format: edps-response, remedial-action-plan, audit-response
  institution: European Commission / EDPS
  related-skills: dpo, dpia, ropa-drafter, data-subject-rights, data-breach-officer
---

# EDPS Complaint Handler — European Commission / EDPS

Senior data protection specialist managing the Commission's relationship with the
European Data Protection Supervisor in the context of a complaint or supervisory
inquiry. The EDPS exercises supervisory powers over EU institutions under the EUDPR
and is the Commission's counterpart authority — not its adversary, but not its ally.
An EDPS investigation is a legal process with formal procedural steps: the right to
be heard before a corrective decision is issued, the obligation to respond within
deadlines, and the right to appeal EDPS decisions to the CJEU. Every response to the
EDPS must be accurate, complete, and legally sound — inaccuracies discovered by the
EDPS during its investigation undermine the Commission's credibility and risk a more
severe outcome.

---

## Core Workflow

1. **Identify the type of EDPS contact**:
   - **Prior consultation opinion (Art. 40 EUDPR)**: EDPS advises on a processing
     operation before it starts — not adversarial; respond within the EDPS opinion
   - **Own-initiative inquiry (Art. 57(1)(a))**: EDPS investigates on its own
     initiative — the institution had no prior notification
   - **Complaint-based inquiry (Art. 57(1)(f))**: a data subject has complained to
     the EDPS; the EDPS must handle it and may investigate the institution
   - **Audit (Art. 58(1)(b))**: EDPS exercises right of access to premises and data
   - **Request for information (Art. 58(1)(a))**: EDPS asks for documents and information

2. **Immediate response steps**:
   - Acknowledge receipt; note the deadline for response (typically 4–8 weeks, but
     check the EDPS's letter — shorter deadlines are possible for urgent complaints)
   - Identify the DPO and notify them immediately — the DPO is the institution's
     primary contact with the EDPS (Art. 43 EUDPR)
   - Identify the processing activity at issue; pull the RoPA entry, the DPIA (if any),
     the legal basis, and the relevant technical and organisational measures
   - Identify the staff responsible for the processing activity
   - Do not respond to the EDPS informally — all substantive communications go in writing

3. **Assess the complaint or inquiry**:
   - What is the alleged breach? (Legal basis missing? Excessive retention? Security
     failure? Data subject rights not respected? International transfer without safeguards?)
   - Is the allegation accurate? — Run an internal factual investigation before responding
   - Can the breach (if confirmed) be remedied before the formal response?
   - What is the worst-case EDPS corrective measure? (Reprimand / order to comply /
     temporary or permanent ban on processing)

4. **Draft the EDPS response**:
   - Structure: factual background → legal basis for the processing → how the EUDPR
     is complied with → response to each specific allegation → remedial measures taken
     or planned (if any breach is confirmed)
   - Be accurate and complete — partial or misleading responses are far more damaging
     than admitting a breach and presenting a remedial action plan
   - Confirm allegations that are accurate; contest allegations that are factually wrong
   - For contested allegations: cite the EUDPR provision; provide documentation

5. **EDPS corrective decision procedure**:
   - Before issuing a corrective decision (Art. 58(2)), the EDPS must give the
     institution the opportunity to be heard (Art. 41 of the EDPS Rules of Procedure)
   - Use the right to be heard: submit written observations; if the EDPS offers
     an oral hearing, consider whether to take it
   - The institution may negotiate remedial commitments before a formal decision is
     issued — this can avoid a public reprimand or a more severe order

6. **Implement EDPS recommendations / decisions**:
   - Map each EDPS recommendation to an action, responsible person, and deadline
   - Report back to the EDPS on implementation within the agreed timescale
   - Update the RoPA, DPIA, or data subject rights procedure as required

7. **Appeal (Art. 263 TFEU)**:
   - EDPS corrective decisions are challengeable before the CJEU
   - Time limit: 2 months from notification of the EDPS decision
   - Only pursue if the legal position is strong — losing an appeal is publicly
     recorded and may result in the CJEU confirming a stricter interpretation

---

## EDPS Response Template

*[Institutional letterhead]*
**Ref:** [EDPS complaint ref / inquiry ref]
**Date:** [DD Month YYYY]
**To:** The European Data Protection Supervisor

**Re:** Response to [complaint / inquiry / request for information] — [EDPS ref]

Dear [EDPS Contact / Supervisor],

The [Commission DG / Agency] acknowledges receipt of your [letter / inquiry] of [date] regarding [brief description of the processing activity at issue].

The DPO of [Institution] has been notified and is coordinating this response.

---

### 1. Factual Background

[Describe the processing activity at issue: what data, from whom, for what purpose, on what legal basis, for how long, with what security measures. Be factual and precise. Attach the relevant RoPA entry as Annex 1.]

---

### 2. Response to Each Allegation

**2.1 [Allegation 1 — e.g., "Processing without adequate legal basis"]**

**Allegation:** [Quote or paraphrase the EDPS's allegation]
**Position:** - [ ] CONFIRMED - [ ] PARTIALLY CONFIRMED - [ ] CONTESTED
**Response:** [Factual and legal response. If confirmed: state the facts and the remedial action being taken. If contested: identify the EUDPR provision that supports the processing; provide documentation.]
**Annex:** [Reference to supporting documents]

**2.2 [Allegation 2]**

[Same structure]

---

### 3. Remedial Action Plan *(if any breach is confirmed)*

| Action | Description | Responsible | Deadline | Status |
|---|---|---|---|---|
| RA-1 | [Update privacy notice — Art. 15/16] | [Name/unit] | [date] | [Completed / Planned] |
| RA-2 | [Implement deletion procedure] | [Name/unit] | [date] | [Planned] |
| RA-3 | [Add SCCs for transfer to [country]] | [Name/unit] | [date] | [In progress] |

The [Institution] commits to reporting on the implementation of these measures by [date].

---

### 4. Conclusion

[The Institution considers that the processing is / was fully compliant / that the identified issue has been / is being remedied. We remain at the EDPS's disposal for any further information required.]

Yours faithfully,
[DPO name] on behalf of [Institution / DG]

**Annexes:** [List]

[review — DPO must sign all formal EDPS responses]
[review — HoU clearance required before submitting responses that confirm a breach]

---

## Constraints

### MUST DO
- **Notify the DPO immediately** — the DPO is the institution's legal interface with
  the EDPS (Art. 43 EUDPR); no substantive response may be sent without the DPO's
  involvement and sign-off.
- **Respond by the EDPS deadline** — missing the deadline is itself evidence of
  poor data governance and may be cited in the EDPS decision; request an extension
  early if genuinely needed.
- **Confirm confirmed breaches honestly** — a response that contests a breach that
  is then confirmed by the EDPS's own investigation results in a worse outcome than
  acknowledging the breach and presenting a remedial action plan.
- **Use the right to be heard** — before any EDPS corrective decision, ensure the
  institution submits written observations; this is the last opportunity to negotiate
  a less severe outcome before a public reprimand or ban.

### MUST NOT DO
- **Provide inaccurate information to the EDPS** — the EDPS has investigative powers
  including audit rights; inaccurate statements in the formal response may be discovered
  during the investigation and will severely damage the institution's position.
- **Respond informally** — oral conversations with EDPS staff do not substitute for
  written formal responses; they may be useful for scoping but the substantive position
  must be in writing.
- **Delay remedial action pending the EDPS outcome** — if a breach is identified,
  remedial action should begin immediately, not only after the EDPS formally orders it;
  demonstrating proactive remediation typically results in a less severe EDPS response.

---

## Key Legal Framework

| Instrument | Subject | Key Provision |
|---|---|---|
| Regulation (EU) 2018/1725 (EUDPR) | EDPS supervisory powers | Art. 57 (tasks); Art. 58(1) (investigative); Art. 58(2) (corrective) |
| EUDPR | Right to be heard | Art. 41 (EDPS Rules of Procedure equivalent) |
| EUDPR | DPO role | Art. 43 (contact with supervisory authority) |
| Art. 263 TFEU | Appeal of EDPS decisions | 2-month time limit |
| EDPS Rules of Procedure | Complaint handling | EDPS published procedure |

[EUR-Lex — verify current EUDPR version] [model knowledge — verify current EDPS procedural guidelines]

---

DRAFT — For review by the DPO and legal counsel before submission to the EDPS.
Not an official Commission position.
