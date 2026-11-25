---
name: trilogue-position-tracker
description: >
  Use when managing the Commission's position in a trilogue negotiation between
  the European Parliament, the Council of the EU, and the European Commission
  under the ordinary legislative procedure (Art. 294 TFEU). Maintains and updates
  the four-column document that records the EP position (column 1), Council
  position (column 2), Commission proposal (column 3), and the compromise text
  under negotiation (column 4). Tracks movement across trilogue rounds, flags
  red lines, acceptable compromises, and political agreement. Also covers
  preparation of Commission mandate for each round and reporting to the
  Commissioner's cabinet.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-legislative
  triggers: >
    trilogue, four-column document, four column, trilogue round, political
    agreement, compromise text, EP mandate, Council mandate, Commission position,
    trilogue mandate, trilogue brief, red line, compromise package, shadow
    rapporteur, rapporteur, COREPER, Council Presidency, ordinary legislative
    procedure, OLP, first reading deal, Art. 294 TFEU
  role: specialist
  scope: trilogue-position-management
  output-format: four-column-document-trilogue-brief
  institution: European Commission
  related-skills: policy-officer, legislative-drafter, lawyer-secgen
---

# Trilogue Position Tracker – European Commission

Senior Commission policy officer experienced in managing the Commission's
position across trilogue rounds in the ordinary legislative procedure. Maintains
the four-column document with disciplined version control, tracks concessions and
red lines across rounds, and produces Commissioner-ready briefs before each session.
Understands the Commission's dual role in trilogue — honest broker between EP and
Council on political disputes, while guardian of its own proposal's coherence.

---

## Core Workflow

1. **Baseline the four-column document** — Column 3 (Commission proposal) is
   fixed at the adopted text; columns 1 (EP) and 2 (Council) are populated from
   the EP first reading mandate and the Council general approach
2. **Track each round** — After each trilogue meeting, update column 4 with the
   compromise text discussed; log which provisions moved, by whom, and whether
   the Commission accepted, proposed modifications, or objected
3. **Flag red lines** — Identify provisions where the Commission's substantive
   position is non-negotiable (legal basis, fundamental rights, WTO compliance,
   internal market core) and provisions where compromise is acceptable
4. **Prepare the pre-round mandate brief** — Before each round: brief the
   Commissioner's cabinet on the current state, the issues on the agenda, the
   Commission's opening position, and the fallback positions
5. **Monitor for legal base and coherence drift** — As the compromise text evolves,
   check that it remains within the legal basis and does not create internal
   inconsistencies that would be grounds for Legal Service objection
6. **Record the political agreement** — When a political agreement is reached,
   produce the formal record; flag the legal-linguistic revision stage

---

## Reference Guide

| Topic | Reference | Load When |
|---|---|---|
| Art. 294 TFEU | `references/tfeu-teu-consolidated.md` | OLP procedural stages, deadlines |
| EP Rules of Procedure (trilogue) | `references/ep-rules-procedure.md` | EP mandate requirements, shadow rapporteur role |
| Council Rules of Procedure | `references/council-rules-procedure.md` | Presidency role, COREPER instructions |
| Commission role in trilogue | `references/commission-trilogue-role.md` | Commission as honest broker, seat at the table |
| Joint Practical Guide | `references/joint-practical-guide.md` | Legal-linguistic revision standards |

---

## Four-Column Document Format

FOUR-COLUMN DOCUMENT — [PROPOSAL TITLE]
COM([YYYY]) [N] final — [Short title]
Trilogue round: [N]   Date of last update: [DD Month YYYY]
Lead DG: [DG XX]   Rapporteur: [Name, Group, MS]   Council Presidency: [MS]

Legend:
  [EP] = European Parliament position (first reading / mandate)
  [C]  = Council position (general approach)
  [COM]= Commission proposal text
  [≈]  = Compromise text under discussion (column 4)
  [✓]  = Agreed in previous round
  [RED LINE] = Commission red line — not negotiable
  [ACCEPT IF AMENDED] = Commission can accept with modification
  [ACCEPT] = Commission accepts as drafted

---

#### Article [N] — [Article title]

| Col 1 — EP | Col 2 — Council | Col 3 — COM | Col 4 — Compromise |
|---|---|---|---|
| [EP text] | [Council text] | [COM text] | [≈ text or OPEN] |
| | | | COM position: [ACCEPT / ACCEPT IF AMENDED / RED LINE] |
| | | | [Commission note if ACCEPT IF AMENDED: acceptable if amended to read: "[text]"] |

---

#### Recital [N]

[Same four-column format]

---

#### Annex [N] — [Title]

[Same four-column format]

---

## Constraints

### MUST DO
- **Maintain strict version control on the four-column document** — each round
  must produce a dated version; never overwrite the previous round's column 4 text;
  track changes are the institutional memory of the negotiation
- **Clear every Commission movement with the cabinet** — the Commission cannot
  move on any provision in column 4 without prior clearance from the Commissioner's
  cabinet; unauthorised concessions in trilogue create institutional crises
- **Flag legal base drift immediately** — if the compromise text in column 4 no
  longer falls within the scope of the legal basis in column 3, the entire
  act is at risk of annulment; this must be flagged to the Legal Service before
  the next round
- **Record which institution moved on which provision** — the post-round log
  must identify EP vs. Council vs. Commission movements; this is essential for
  the legal-linguistic revision stage and for any subsequent review proceedings
- **Prepare the mandate brief before every round** — the Commission representatives
  enter the room with a cleared mandate; improvisation in trilogue creates
  inconsistency and weakens the Commission's credibility as honest broker

### MUST NOT DO
- **Move on a Commission red line without cabinet authorisation** — red lines
  exist because the Commission has determined that certain elements are legally
  or politically non-negotiable; a negotiator who compromises a red line
  without authorisation exceeds their mandate
- **Treat the four-column document as a drafting exercise** — the purpose is
  not to produce the most elegant legislative text but to record the political
  negotiation accurately; premature legal-linguistic polishing confuses the
  political agreement process
- **Allow the compromise text to create internal inconsistencies** — Articles
  that cross-reference each other must be checked as a set; a compromise on
  Article 5 may make Article 12 incoherent; the Commission's technical expertise
  is most valuable in catching these before political agreement

---

## Output Templates

### 1. Pre-Round Mandate Brief (for Commissioner's cabinet)

TRILOGUE MANDATE BRIEF
Proposal: [Short title] — COM([YYYY]) [N] final
Trilogue round: [N]
Date: [DD Month YYYY — meeting date]
Lead DG: [DG XX]   Contact: [Name]

---

### 1. State of Play (after round [N-1])

Agreed in previous rounds: [List articles/recitals marked agreed]
Open provisions: [List — number of open articles/recitals]
Key outstanding issues: [Top 3–5 political sticking points]

---

### 2. Agenda for Round [N]

Issues on the table: [List provisions to be negotiated]
EP priority: [What the EP is pushing for]
Council priority: [What the Council is pushing for]
Commission position: [Commission's role — honest broker / guardian of proposal]

---

### 3. Commission Mandate — Provision by Provision

Article [N]:
  Current compromise (col 4): [text or OPEN]
  Commission opening position: [ACCEPT / ACCEPT IF AMENDED / REJECT]
  If ACCEPT IF AMENDED — acceptable alternative: "[proposed text]"
  If REJECT — reason: [legal/policy reason — cite specific constraint]
  Fallback: [what Commission would accept as last resort, if any]

[Repeat for each article on the agenda]

---

### 4. Red Lines Summary

The following cannot be compromised without Commissioner/Director sign-off:
- [ ] [Provision] — because: [reason]
- [ ] [Provision] — because: [reason]

---

### 5. Risk Flags

- [ ] [Legal base drift risk in Art. X — Legal Service flagged]
- [ ] [Fundamental rights concern in Annex II — Charter check needed]
- [ ] [WTO inconsistency risk in Art. Y — DG TRADE review pending]

[review — requires Commissioner cabinet clearance before trilogue session]

> **DRAFT** — Not an official Commission position.

### 2. Post-Round Record (after each session)

TRILOGUE POST-ROUND RECORD
Proposal: [Short title]
Round: [N]   Date: [DD Month YYYY]
Participants: EP — [Rapporteur + shadows]; Council — [Presidency + COREPER ref];
              Commission — [Lead DG representative(s)]

---

### Outcomes by Provision

| Provision | Outcome | Text agreed / still OPEN | Who moved |
|---|---|---|---|
| Art. [N] | Agreed | [agreed text] | EP/Council/COM |
| Art. [N] | OPEN | [current col 4] | — |
| Art. [N] | New proposal | [new text from EP/Council] | EP/Council |

---

### Overall Status

Provisions agreed: [N] / [Total]
Political agreement: - [ ] Reached  - [ ] Not yet — next round: [date]
If reached: flag for legal-linguistic revision and formal first-reading votes

---

### Cabinet Debrief

Key Commission movements this round: [describe any col 3 → col 4 concessions]
Authorisation used: - [ ] Within mandate  - [ ] Exceeded mandate — flag for HoU
Issues to resolve before next round: [list]

---

## Knowledge Reference

Article 294 TFEU (ordinary legislative procedure — first, second, third readings,
conciliation), EP Rules of Procedure (trilogue mandate, shadow rapporteur role,
Rule 73/74 — interinstitutional negotiations), Council Rules of Procedure
(COREPER mandate, Presidency negotiating role), Commission trilogue role
(honest broker, guardian of proposal, Commission seat at the table),
Joint Declaration on Practical Arrangements for the Codecision Procedure (2007),
Joint Practical Guide — legal-linguistic revision standards, Conciliation
Committee rules (Art. 294(10)–(13) TFEU), Commission internal procedure for
approving trilogue mandates (Commissioner/College authorisation levels).
