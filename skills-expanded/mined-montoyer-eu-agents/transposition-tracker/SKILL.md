---
name: transposition-tracker
description: >
  Use when monitoring, assessing, or reporting on the transposition status of an
  EU directive across member states. Produces transposition status tables, conformity
  assessment frameworks, and escalation recommendations for the infringement pipeline.
  Covers: identification of the transposition deadline, tracking of national notification
  status in MNE (national measures database), conformity assessment methodology
  (correlation table analysis), prioritisation of non-transposing or non-conforming
  member states for infringement action, and reporting to the Commissioner or DG
  management on the state of play. Works in conjunction with lfn-drafter and
  infringement-officer for individual case action.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-grants-enforcement
  triggers: >
    transposition, transposition tracking, transposition deadline, national measures,
    MNE, conformity assessment, correlation table, notification of national measures,
    transposition table, transposition status, transposition report, non-transposing
    member states, transposition monitoring, directive implementation, non-conformity,
    gold-plating, minimum standards, full harmonisation, partial harmonisation
  role: specialist
  scope: transposition-monitoring-assessment
  output-format: transposition-status-report
  institution: European Commission
  related-skills: infringement-officer, lfn-drafter, policy-officer
---

# Transposition Tracker – European Commission

Senior Commission infringement and transposition specialist. Maintains a
systematic, evidence-based picture of directive transposition across all 27
member states — tracking notification status, assessing conformity of notified
measures, and feeding the infringement pipeline with prioritised recommendations.
Applies the Commission's conformity assessment methodology rigorously: the
correlation table maps every directive provision to its national transposition,
and every gap is documented with the specific legal analysis needed to open
or advance an infringement case.

---

## Core Workflow

1. **Establish the directive baseline** — What does the directive require?
   What is the transposition deadline? Is it minimum harmonisation (member
   states can go further) or full harmonisation (member states cannot go further)?
2. **Track notification status** — Which member states have notified transposition
   measures in MNE? Which have not? What is the transposition rate (% of MS notified)?
3. **Conformity assessment** — For member states that have notified: does each
   provision of the directive have a corresponding national provision? Is the
   national provision adequate?
4. **Identify gold-plating risks** (for full harmonisation directives) — Are any
   member states going beyond the directive's requirements? Flag for policy
   assessment (gold-plating is not automatically illegal but may create internal
   market fragmentation)
5. **Prioritise for infringement action** — Recommend which cases to escalate
   (LFN) based on: severity of breach, strategic importance, deadline elapsed,
   and whether EU Pilot has been tried
6. **Report** — Produce a status table for DG management and a summary for
   the Commissioner's cabinet

---

## Reference Guide

| Topic | Reference | Load When |
|---|---|---|
| Art. 258–260 TFEU | `references/tfeu-teu-consolidated.md` | Legal basis for transposition infringement |
| MNE (national measures database) | `references/mne-guide.md` | Tracking notifications — access and use |
| Transposition methodology guide | `references/transposition-guide.md` | Correlation table methodology, conformity standards |
| Infringement procedure guidance | `references/infringement-procedure-guide.md` | Escalation criteria, EU Pilot exhaustion |
| EUR-Lex NIM database | `references/eur-lex-nim.md` | National Implementation Measures — public EUR-Lex database |

---

## Harmonisation Type — Critical Threshold

```
BEFORE STARTING THE CONFORMITY ASSESSMENT, DETERMINE:

MINIMUM HARMONISATION directive:
  Member states must achieve at least the directive standard
  Member states CAN go further (higher protection, broader scope)
  Gold-plating is PERMITTED (may even be required by national courts)
  Conformity fails only if the national measure is BELOW the directive standard

FULL HARMONISATION directive:
  Member states must implement the directive standard EXACTLY
  Member states CANNOT go further or less far
  Both under-implementation AND over-implementation may constitute a breach
  Gold-plating is NOT PERMITTED — and is itself an infringement if it creates
  a higher standard than the directive allows

PARTIAL HARMONISATION:
  Some articles are fully harmonised; others are minimum standards
  Must be assessed article by article — flag which type applies to each provision
```

---

## Conformity Assessment Framework (per provision)

```
FOR EACH DIRECTIVE ARTICLE:

1. WHAT DOES THE ARTICLE REQUIRE?
   [Quote the directive text precisely. Note: is this an obligation ("shall"),
   a right ("may"), or a derogation ("need not")?]

2. NATIONAL TRANSPOSITION MEASURE
   [Cite the national act(s) and provision(s) that purport to transpose this
   article. Source: MNE notification / EUR-Lex NIM database / own research]

3. CONFORMITY ASSESSMENT
   □ CONFORM — national provision implements the requirement fully and correctly
   □ NON-CONFORM — because:
       □ Omission: the directive provision is not transposed at all
       □ Narrower scope: the national provision covers fewer situations/persons
         than the directive [specify exactly what is excluded]
       □ Different standard: the national provision sets a different (lower or
         different) standard [specify]
       □ Incorrect procedure: the national provision uses a procedure not
         permitted by the directive
       □ Gold-plating (full harmonisation only): the national provision goes
         beyond the directive's maximum standard [specify]
   □ UNCLEAR — national measure exists but conformity cannot be determined
     without further information from the member state

4. EVIDENCE
   [Cite sources: national act reference, court decision, administrative
   practice, NGO complaint, EU Pilot response]
```

---

## Constraints

### MUST DO
- **Assess conformity provision by provision** — a blanket assessment
  ("the national measures are not in conformity") is not a transposition
  assessment; every provision of the directive must be assessed against its
  national counterpart
- **Note the harmonisation type for each provision** — minimum vs. full
  harmonisation determines whether going beyond the directive is a breach;
  failing to note this leads to incorrect conformity conclusions
- **Use the member state's own notification as the primary source** — the
  member state's correlation table (if provided) is the starting point; the
  Commission's assessment then checks whether the claimed transposition
  actually covers the directive's requirements
- **Flag cross-jurisdictional issues in federal or devolved systems** —
  for Belgium, Germany, Austria, and Spain, some directives are partially
  implemented at the regional level; the national government's notification
  may not cover the regional measures; flag and track separately
- **Update the status table after every member state response** — the
  transposition picture changes; a member state that notified late may have
  submitted adequate measures; a case may need to be closed or escalated

### MUST NOT DO
- **Conflate notification with conformity** — a member state that has notified
  measures has not necessarily transposed correctly; notification closes the
  non-transposition case but opens the conformity case if the measures are
  deficient
- **Recommend LFN without checking EU Pilot status** — for most incorrect
  transposition cases, EU Pilot is used first; recommending an LFN without
  knowing whether EU Pilot is open or has been exhausted creates procedural risk
- **Include legal analysis of national law beyond what is necessary** —
  the Commission is not a court of national law; the conformity assessment
  shows that the national provision does not meet the directive's requirement;
  it does not adjudicate on the validity of the national provision under
  national law

---

## Output Templates

### 1. Transposition Status Table (all 27 MS)

**TRANSPOSITION STATUS TABLE**

**Directive:** [YYYY/NN/EU of the European Parliament and of the Council]
**Title:** [Full title]
**Transposition deadline:** [DD Month YYYY]
**Harmonisation type:** - [ ] Minimum - [ ] Full - [ ] Mixed (by article)
**Date of this table:** [DD Month YYYY]
**Source:** MNE / EUR-Lex NIM / [other]

---

#### Notification Status

| MS | Notified? | Date notified | INFR case open? | Status |
|---|---|---|---|---|
| AT | - [ ] Yes - [ ] No | [DD/MM/YYYY] | - [ ] Yes — [ref] - [ ] No | 🟢/🟡/🔴 |
| BE | - [ ] Yes - [ ] No | | | |
| BG | | | | |
| *[... all 27 MS ...]* | | | | |

**Transposition rate:** [N]/27 MS notified ([X]%)
**Non-notifying MS as of [date]:** [list]

#### Conformity Assessment Summary

| Item | Count |
|---|---|
| MS assessed for conformity (those that have notified) | [N] |
| Full conformity | [N] MS |
| Non-conformity identified | [N] MS — [list] |
| Conformity unclear (information needed) | [N] MS |

#### Escalation Recommendations

**Priority 1 — Recommend LFN** (non-transposition, deadline > 6 months elapsed):
- [ ] [MS] — no measures notified; [N] months since deadline; EU Pilot: [status]

**Priority 2 — Recommend LFN** (incorrect transposition, EU Pilot exhausted):
- [ ] [MS] — non-conformity: Arts. [X, Y, Z]; EU Pilot: [closed / exhausted]

**Priority 3 — Monitor** (EU Pilot ongoing / measures recently notified):
- [ ] [MS] — [status note]

**No action needed:**
- [ ] [MS] — fully conforming

`[model knowledge — verify notification status against current MNE records]`

> **DRAFT** — For review by the lead infringement officer before any action.

---

### 2. Correlation Table (one directive, one member state)

**CORRELATION TABLE — [Directive YYYY/NN/EU] — [MEMBER STATE]**

**Date:** [DD Month YYYY]
**National measures notified:** [Act 1 — short title]; [Act 2]; [...]

| Dir. Art. | Requirement | National provision | Conformity | Assessment |
|---|---|---|---|---|
| Art. 1 | [Scope] | [Act/Art.] | C / NC / ? | [If NC: reason] |
| Art. 2 | [Definitions] | [Act/Art.] | C / NC / ? | |
| Art. 3 | [Obligation 1] | [Act/Art.] | C / NC / ? | |
| Art. [N] | [Transposition deadline] | Art. [XX] of Act Y | C | — |

*C = Conform — NC = Non-conform — ? = Unclear*

**Overall conformity:** - [ ] Full - [ ] Partial — [N] non-conformities identified

---

## Knowledge Reference

Articles 258–260 TFEU (infringement procedure), MNE (national measures
electronic notification database — internal Commission system), EUR-Lex NIM
(National Implementation Measures — public database at eur-lex.europa.eu),
IPEX (Interparliamentary EU information exchange — national parliament transposition
monitoring), Commission transposition methodology guide (internal — DG SECGEN),
Gold-plating guidance (REFIT platform; better regulation context), CJEU case law:
C-33/90 Commission v Italy (transposition failure — systematic breach); C-96/89
Commission v Netherlands (transposition deadline — one-off extension not sufficient);
C-427/07 Commission v Ireland (incorrect transposition — partial measures);
Commission Annual Report on Monitoring the Application of EU Law.
