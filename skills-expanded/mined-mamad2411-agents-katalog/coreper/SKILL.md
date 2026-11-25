---
name: coreper
description: >
  Simulate a COREPER session (Committee of Permanent Representatives) preparing
  a Council file for ministerial decision. Models COREPER I (deputy ambassadors —
  technical and sectoral dossiers) or COREPER II (ambassadors — politically sensitive
  dossiers, CFSP, JHA, own resources). Produces the COREPER recommendation to the
  Council configuration: A-point (no discussion needed — adopt without debate),
  B-point (political discussion required), or referral back to working party.
  Use before council-eu to model the ambassadorial layer of Council preparation,
  or standalone when the political negotiation happens at COREPER level rather
  than at ministerial level.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-simulation
  triggers: >
    COREPER, Permanent Representatives, COREPER I, COREPER II, Ambassador level,
    A-point, B-point, Council preparation, working party referral, COREPER mandate,
    general approach COREPER, COREPER recommendation, Antici group, Mertens group,
    PSC, Political and Security Committee, Council agenda, A/B classification,
    COREPER meeting, COREPER note, I/A note, Council preparatory body
  role: multi-agent
  scope: coreper-simulation
  output-format: coreper-note, a-b-classification, council-recommendation
  institution: Council of the European Union
  related-skills: council-eu, council-presidency, qmv-calculator, trilogue, legislative-cycle
---

# COREPER — Committee of Permanent Representatives

The Committee of Permanent Representatives (COREPER) is the engine of Council
decision-making. All legislative and most non-legislative Council acts pass
through COREPER before reaching ministers. COREPER does not decide — it prepares
and filters. Its most important function is the A/B classification: if COREPER can
reach agreement, the item is placed on the Council agenda as an A-point and adopted
without discussion; only items where genuine political disagreement persists at
ambassadorial level become B-points requiring ministerial engagement.

COREPER II (Permanent Representatives — ambassadors) handles politically sensitive
files: institutional matters, CFSP, JHA, own resources, enlargement, and dossiers
that remain contested despite working-party exhaustion.

COREPER I (Deputy Permanent Representatives) handles technical and sectoral files:
internal market, social policy, environment, agriculture, transport, and research
dossiers that do not require ambassadorial political judgment.

The Presidency chairs both. The Commission is present and can adjust its proposal
under Art. 293(2) TFEU. The Council Legal Service (CLS) attends and advises on
legal base and vires issues.

---

## Core Workflow

1. **Classify the file** — COREPER I or COREPER II based on political sensitivity:
   - COREPER II: JHA, CFSP, EPSCO political items, own resources, constitutional
     matters, rule of law, migration, enlargement, anything where heads of state
     have taken positions
   - COREPER I: most OLP technical dossiers — COMPET, ENVI, TTE, AGRI, EMPL
     (technical items), transport, digital/internal market regulation
   - Note: the Presidency and General Secretariat decide the classification;
     a delegation can request escalation from COREPER I to COREPER II

2. **State of play from working party** — Before modelling COREPER, establish:
   - Which articles have been fully agreed at working-party level (no reservations)
   - Which articles carry national scrutiny reservations (parliamentary scrutiny
     reserves — PSR — from member states whose national parliaments must examine
     the text before their government can agree)
   - Which articles carry political reservations (delegations not yet instructed
     by capitals or explicitly holding position for COREPER/ministerial level)
   - Which articles remain in square brackets (text not yet agreed)

3. **COREPER examination** — For each contested article or issue:
   - The Presidency presents the state of play and a proposed compromise
   - Delegations with reservations explain their position
   - The Presidency tests whether a revised text or a declaration to the minutes
     can lift the reservation
   - The Council Legal Service (CLS) clarifies any legal base or subsidiarity
     question
   - The Commission can modify its proposal to facilitate agreement

4. **A/B classification decision** — After examining all contested items:
   - **A-point**: COREPER agrees to recommend to Council for adoption without
     discussion; all delegations (or at least QMV) have lifted reservations;
     remaining PSRs are noted but do not block
   - **B-point**: Political disagreement persists; item goes to Council agenda
     as a discussion item with COREPER's assessment of the state of play
   - **Referral back**: Item sent back to working party for further technical
     examination; COREPER issues guidance on what needs to be resolved

5. **QMV check** — Before recommending an A-point or calling a B-point vote:
   - Run QMV arithmetic: 15 of 27 MS + 65% of EU population
   - Identify whether a blocking minority (≥4 MS, >35% population) has formed
   - If blocking minority present: do not recommend adoption; return to
     negotiation or flag for ministerial decision
   - Use `/qmv-calculator` for precise arithmetic when delegations have stated
     clear positions

6. **Mandate for trilogue** — If the Council is moving toward a general approach
   for trilogue, COREPER:
   - Reviews the Presidency's proposed general approach text
   - Squares brackets that can be resolved at ambassadorial level
   - Identifies issues that must be escalated to ministers before the mandate
     can be given
   - Issues the COREPER recommendation to Council to adopt the general approach

---

## Reference Guide

| Resource | Path | Load when |
|---|---|---|
| Council institutional agent | `knowledge/institutions/council-eu.md` | All sessions |
| QMV rules and population weights | `knowledge/institutions/council-eu.md` | Steps 4–5 |
| Trilogue protocol | `knowledge/agents/trilogue.md` | Step 6 — mandate preparation |

---

## COREPER Layers Quick Reference

```
HIERARCHY OF COUNCIL PREPARATORY BODIES:

  Ministers (Council configuration)
      ▲  B-points only
  COREPER II  (Ambassadors — politically sensitive)
  COREPER I   (Deputy Ambassadors — technical/sectoral)
      ▲  contested items only
  Working Party  (National experts — article-by-article)

SUPPORT BODIES:
  Antici Group:   Prepares COREPER II agendas; coordinates logistics
  Mertens Group:  Prepares COREPER I agendas
  PSC:            Political and Security Committee — CFSP/CSDP files
  SCA:            Special Committee on Agriculture — AGRI files

TYPES OF RESERVATION:
  General scrutiny reservation (GSR):  Delegation has not yet studied the text
  Parliamentary scrutiny reserve (PSR): National parliament must examine first —
    does NOT block adoption but delays final agreement; must be lifted before
    formal adoption
  Political reservation:  Delegation has instructions from capital to hold —
    needs political decision at COREPER or ministerial level
  Square bracket []:  Text not yet agreed — cannot be in an A-point

A-POINT RULE:
  An A-point must be clean — no square brackets, no political reservations;
  PSRs can remain if the delegation confirms they will be lifted before formal
  adoption; GSRs must be lifted
```

---

## National Scrutiny Reserve (PSR) Mechanics

Parliamentary scrutiny reserves are a structural feature of COREPER negotiation
that significantly affect timing. Member states with strong parliamentary oversight
requirements (Denmark, Finland, Sweden, Austria, Germany — Bundestag) routinely
place PSRs on legislative files. A PSR means the delegation cannot agree until
its national parliament has examined the text. This does not give the national
parliament a veto, but it forces the Council to wait.

In COREPER, PSRs are tracked on a separate register. The Presidency must know
which PSRs are outstanding before calling for a general approach or formal
adoption. A delegation that lifts a PSR prematurely (before its parliament has
completed scrutiny) faces political consequences at home.

---

## Typical COREPER Dynamics by Policy Area

```
JHA (COREPER II):
  Most politically divided body in COREPER II; migration and asylum files
  are consistently the hardest; rule-of-law related files (Art. 7 items)
  are procedurally managed with great caution; a single delegation can use
  procedural tools to delay but not ultimately block QMV files

CFSP/CSDP (COREPER II via PSC):
  Unanimity required; Political and Security Committee (PSC) does the
  technical preparation; COREPER II handles the political layer; a single
  holdout can block CFSP decisions

INTERNAL MARKET / DIGITAL (COREPER I):
  Usually less politically contested at COREPER level; technical
  reservations are typically lifted at working-party level; COREPER I
  often clears the majority of articles as A-points

ENVIRONMENT / CLIMATE (COREPER I for technical, COREPER II if politically
  elevated): Transition periods, flexibility mechanisms, and national
  decarbonisation pathways generate systematic disagreements; PL, CZ, HU
  often hold out longest; DE and FR usually decisive in forming the majority
```

---

## Constraints

### MUST DO
- **Distinguish COREPER I from COREPER II** — the classification matters; COREPER II
  ambassadors have broader political mandates and can make political trade-offs that
  deputy ambassadors cannot; flag clearly which body is meeting
- **Track reservation types precisely** — a PSR and a political reservation have
  different implications; a PSR does not prevent a general approach but prevents
  formal adoption; conflating them produces wrong procedural outcomes
- **Check QMV before recommending A-point** — COREPER does not recommend adoption
  of items where a blocking minority is present; run the arithmetic before classifying
- **Model the Commission's role** — the Commission is present at COREPER and can
  amend its proposal under Art. 293(2) TFEU to facilitate agreement; this is a
  significant tool that COREPER uses regularly; the Commission does not simply observe
- **Flag CLS involvement on legal base** — if delegations challenge the legal basis
  or subsidiarity, the Council Legal Service's opinion is determinative for COREPER;
  model this as a formal intervention

### MUST NOT DO
- **Do not treat COREPER as a decision-making body** — COREPER recommends; the Council
  decides; an A-point recommendation means the Council is expected to adopt without
  debate, not that the decision is made at COREPER level
- **Do not ignore the Presidency's dual role** — the Presidency chair at COREPER is
  also a delegation with its own national position on the dossier; the Presidency chair
  does not vote and does not advocate for its national position in the chair, but its
  national delegation sits at the table and may have reservations
- **Do not lift reservations without justification** — every reservation lifted in the
  simulation must have a plausible reason (compromise text offered, declaration to
  minutes agreed, bilateral assurance given); delegations do not lift reservations for
  free

---

## Output Template

COREPER [I / II] — SESSION NOTE
Dossier: [Title — COM reference]
Presidency: [Member state]
Date: [DD Month YYYY]
Configuration for Council adoption: [COMPET / ENVI / EPSCO / ECOFIN / JHA / etc.]
Legal basis: [TFEU Art. X] — Voting rule: [QMV / Unanimity]

---

### State of Play from Working Party

Articles fully agreed (no reservations):
  [Art. list or "none"]

Articles with Parliamentary Scrutiny Reserves (PSR):
  [Delegation — Art. concerned — expected timeline for lift]

Articles with Political Reservations:
  [Delegation — Art. concerned — nature of reservation]

Articles in square brackets:
  [Art. list — brief description of open issue]

---

### COREPER Examination

Issue [N]: [Article / topic]
  Presidency compromise: [Proposed text or approach]
  Reservations: [Delegations holding — nature]
  Discussion outcome: [Reservation lifted / Maintained / Referred back to WP]
  Reason: [Compromise text accepted / Declaration to minutes agreed / No basis for agreement]

[Repeat for each contested issue]

---

### QMV Assessment (pre-classification)

Qualified majority available: [Yes / Marginal / No]
Blocking minority: [Yes — [MS] / No]
PSRs outstanding: [N delegations — will be lifted before formal adoption / Timeline unclear]

→ Use /qmv-calculator for full arithmetic if member-state positions are specified.

---

### A/B Classification Recommendation

RECOMMENDATION TO COUNCIL:

[ ] A-POINT — Adopt without discussion
    Remaining PSRs: [delegations — confirmed they will lift before formal adoption]
    Note to Council: [any element COREPER wishes to flag to ministers]

[ ] B-POINT — Place on Council agenda for political discussion
    Open issues requiring ministerial decision:
      1. [Issue — why it cannot be resolved at COREPER level]
      2. [Issue]
    COREPER assessment: [Majority available if ministers agree on X / Blocking
      minority risk if Y is not resolved]

[ ] REFERRAL TO WORKING PARTY
    Reason: [Technical question unresolved / CLS opinion awaited / New Commission
      text expected]
    Guidance: [What working party should resolve before returning to COREPER]

---

### Trilogue Mandate Recommendation (if applicable)

COREPER [recommends / does not yet recommend] that the Council adopt the
general approach and mandate the Presidency for trilogue negotiations.

Issues still requiring ministerial decision before mandate can be issued:
  1. [Issue]
  2. [Issue]

Presidency red lines for trilogue (cannot concede without COREPER check-back):
  - [Issue: reason — which delegations would break the QMV majority]

Presidency flexibility zones (can trade in trilogue within this range):
  - [Issue: acceptable range]

[model knowledge — verify current member-state political positions and population
figures for QMV calculation]

> **DRAFT** — Simulation output. Not an official Council position.
