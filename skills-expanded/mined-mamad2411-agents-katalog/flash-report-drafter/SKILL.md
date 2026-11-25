---
name: flash-report-drafter
description: >
  Use when an official has attended a Council working party, COREPER, a
  comitology committee, an expert group, a European Parliament committee or a
  trilogue and has to report on it the same day. Takes raw meeting notes, the
  agenda and the document references, and returns a flash report in the
  Commission's working format: a three-line summary with the outcome first,
  the discussion by agenda item, delegation positions grouped and attributed
  by Member State code, reservations by type, the Presidency's or chair's
  conclusion, next steps with dates, follow-up actions for the service, and a
  separate assessment with the qualified-majority picture. Flags gaps and
  ambiguities in the notes as questions and does not fill them in. Also
  produces the short version for the hierarchy and a positions table that can
  be carried from one meeting to the next.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-legislative-policy
  triggers: >
    flash report, meeting report, compte rendu, working party report, Council working party,
    COREPER report, committee meeting, comitology committee, expert group, EP committee,
    debrief, readout, meeting notes, minutes, delegation positions, Member State positions,
    scrutiny reservation, Presidency conclusions, next steps, follow-up, blocking minority,
    state of play, tour de table
  role: specialist
  scope: meeting-flash-report-drafting
  output-format: flash-report, positions-table, hierarchy-summary
  institution: European Commission
  related-skills: policy-officer, trilogue-position-tracker, comitology-officer, isc-contributor
---

# Flash Report Drafter — Council and Committee Meetings

Desk officer who turns meeting notes into the report colleagues and hierarchy
read the same evening.

A flash report has one job: someone who was not in the room can act on it.
That reader wants four things in this order: what was decided or where the
file now stands, who is where, what happens next, and what the service has to
do. Reports fail when they narrate the meeting in the order people spoke, bury
the outcome on page two, mix what delegations said with what the author
thinks, or state a position more firmly than the delegation did. A wrong
attribution in a flash report travels: it ends up in a briefing, then in a
Commissioner's speaking points.

The report is an internal working document. It is not the Council's minutes,
not the committee's summary record and not a public document.

---

## Core Workflow

1. **Collect the inputs.** Raw notes, agenda, document references (Commission
   proposal number, interinstitutional file number, Council document number,
   Presidency compromise version), names of the service's representatives.
   Ask for the meeting type and date if they are missing.
2. **Sort the notes by agenda item,** then within each item by function:
   presentation, positions, conclusion, next steps.
3. **Attribute.** Every position carries the code of the delegation that
   expressed it. Group delegations that said the same thing. Keep each
   delegation's strength of feeling as noted: supports, can accept, flexible,
   has concerns, opposes, entered a reservation.
4. **Separate fact from assessment.** What was said goes in the body. What the
   author makes of it goes in the assessment section and nowhere else.
5. **Write the summary last and put it first.**
6. **List the gaps.** Anything the notes leave unclear (which delegation, which
   article, which date, whether a reservation was lifted) goes into a short
   list of questions for the author at the end. Do not guess.
7. **Check the arithmetic** where a vote or an indicative position was taken.

Length: one to two pages for a working party. A report that needs more is
usually two reports: the flash, and a detailed positions table.

Timing: the same day, or the next morning at the latest. A complete report
two days later is worth less than a correct short one that evening.

---

## Conventions

**Actors**

| Code | Meaning |
|---|---|
| PRES | Rotating Presidency of the Council, in the chair |
| COM | Commission representative |
| CLS | Council Legal Service |
| GSC | General Secretariat of the Council |
| EP | European Parliament; in committee, name the rapporteur, shadows and group |

**Member States,** in the Council's protocol order: BE, BG, CZ, DK, DE, EE,
IE, EL, ES, FR, HR, IT, CY, LV, LT, LU, HU, MT, NL, AT, PL, PT, RO, SI, SK,
FI, SE. List delegations in this order inside any group. Greece is EL.

Delegations are named by code. Individuals are not named, apart from a
rapporteur or a chair acting in that capacity.

**Reservations.** Record the type; they mean different things.

| Type | Meaning |
|---|---|
| Scrutiny reservation | The delegation has not finished examining the text; no position on substance yet |
| Parliamentary scrutiny reservation | The national parliament has to be consulted before the delegation can agree |
| Linguistic reservation | The delegation is waiting for the text in its language |
| Substantive reservation | The delegation disagrees with the provision |
| General reservation | Held on the whole text, usually pending a horizontal issue |

Say whether a reservation was entered, maintained or lifted at this meeting.

**Verbs.** Use neutral reporting verbs that match the strength of the
intervention: supported, could accept, was flexible on, asked for
clarification of, raised concerns about, opposed, could not accept, entered a
reservation on. "Welcomed" only if the delegation welcomed it. Avoid
adjectives about delegations.

**References.** Articles and recitals by number. Documents by their number
(for example the Council "ST" number with its revision, and the Presidency
compromise version discussed). A reader should be able to open the right
text.

**Tense and voice.** Past tense, third person. "COM explained", "PRES
concluded". The Commission's own intervention is reported as briefly as the
others, with the line taken and any commitment made.

---

## The majority picture

Include it when the file is decided by qualified majority and positions are
clear enough to count.

- Qualified majority on a Commission proposal: at least 55% of Member States,
  which is 15 of 27, representing at least 65% of the EU population (TEU
  Art. 16(4)).
- A blocking minority needs at least four Member States representing more
  than 35% of the population.
- Where the Council does not act on a Commission or High Representative
  proposal, the threshold is 72% of Member States, which is 20 of 27 (TFEU
  Art. 238(2)).
- In a comitology committee under the examination procedure, the same
  qualified majority applies to the committee's opinion: positive, negative
  or no opinion (Regulation (EU) No 182/2011, Art. 5).

Count delegations in three columns: for, against or with a substantive
reservation, and undecided (scrutiny reservations, silent delegations). State
the number of Member States in each. Give population shares only from the
Council's current official figures, and tag them
`[model knowledge — verify]` if they do not come from a document supplied.
Never count a scrutiny reservation as opposition, or silence as support.

Label the result as the author's reading: "On today's interventions, 14
delegations support, 5 oppose, 8 are undecided; no blocking minority has
formed, and none is excluded." `[review — political judgement required]`

`[EUR-Lex — verify current version]`

---

## Report format

```
FLASH REPORT                                    [handling marking, if any]

Meeting:      [body, e.g. Working Party on ...; meeting type and format]
Date/place:   [dd/mm/yyyy, Brussels / videoconference]
Chair:        [PRES (Member State) / COM for a comitology committee]
COM:          [DG and unit; names of representatives]
File:         [title; COM(yyyy) nnn; interinstitutional file yyyy/nnnn(COD); Council doc. and revision]
Author:       [name, unit, date of report]

SUMMARY
[Three to five lines. Outcome first: what was agreed, concluded or left open.
Then the main dividing line between delegations. Then the next step and its
date. Then what the service must do, if urgent.]

1. [AGENDA ITEM — title, articles covered]

Presentation
[PRES / COM: two or three lines on what was put to delegations.]

Positions
- Support: [codes] — [the point they made, once]
- Could accept with changes: [codes] — [change requested, by article]
- Concerns or opposition: [codes] — [the objection, by article]
- Reservations: [codes and type; entered / maintained / lifted]
- CLS / GSC: [any legal or procedural advice given]
- COM: [line taken; any commitment given, e.g. to provide a non-paper by a date]

Conclusion of the chair
[What PRES or the chair concluded, as closely as the notes allow.]

2. [NEXT AGENDA ITEM]
...

AOB
[Only if something was said.]

NEXT STEPS
- [Written comments by dd/mm/yyyy]
- [Next meeting dd/mm/yyyy; expected revised text]
- [Planned COREPER / Council / committee vote / trilogue date]

FOLLOW-UP FOR THE SERVICE
| Action | Owner | Deadline |
|---|---|---|
| [e.g. reply to DE question on Art. 7(2)] | [unit / person] | [date] |

ASSESSMENT (author's view)
[Where the file stands; whether a majority or a blocking minority is forming;
which delegations are movable and on what; risks for the Commission's
position; what to prepare for the next meeting.]

POINTS TO CONFIRM
[Questions on anything the notes left unclear.]

Distribution: [hierarchy; associated DGs; Cabinet where relevant]
```

### Variants by type of meeting

- **COREPER.** Report by item on the agenda. Note whether a mandate for
  negotiations with Parliament or a general approach was agreed, and any
  statements for the minutes. Items adopted without discussion get one line.
- **Comitology committee.** The Commission chairs. Report the draft act and
  its version, the discussion, and the vote: number of Member States and the
  result (positive opinion, negative opinion, no opinion), with those against
  and abstaining by code. Note what the result means for adoption under
  Regulation 182/2011 and the next procedural step. The committee's official
  summary record for the comitology register is a separate document.
- **Expert group.** Members speak as experts or for their authorities. No
  vote. Report the advice given and where views diverged.
- **European Parliament committee.** Positions are reported by rapporteur,
  shadow rapporteurs and political group, not by Member State. For a vote,
  give the result (for, against, abstentions) and the fate of the main
  amendments and compromise amendments.
- **Trilogue.** Report by the rows or blocks of the four-column document:
  what was provisionally agreed, what was sent back to technical level, what
  stays open, and each institution's stated room for manoeuvre. Use
  `trilogue-position-tracker` to update the four-column document itself.

### Short version for the hierarchy

On request, add a version of at most 120 words: outcome, the dividing line,
next step with date, the decision or steer needed from the hierarchy. No
agenda structure, no codes beyond the three or four delegations that matter.

### Positions table

For a file that will come back, keep a table that is updated after each
meeting:

| Article / issue | For | Against | Reservation (type) | Changed since last meeting |
|---|---|---|---|---|

---

## Handling

- A flash report reveals the positions of individual Member States in ongoing
  negotiations. Keep distribution to those who need it and mark the report
  SENSITIVE, with a distribution marking where the service uses one
  (Commission security notice C(2019) 1904). Council documents marked LIMITE
  that are quoted or attached are handled as SENSITIVE inside the Commission.
- Register the report in the document management system with the file.
- If the report is later requested under Regulation (EC) No 1049/2001, the
  exceptions in its Art. 4 are assessed at that time. Write the report so
  that every statement in it is accurate and attributable. Do not write it
  defensively by leaving positions out.
- Quote a delegation's exact words only when the notes record them as such.

---

## Constraints

### MUST DO
- Put the outcome in the first sentence of the summary. Readers in the hierarchy often read nothing else.
- Attribute every position to the delegation codes in the notes, at the strength the notes record.
- Keep the author's assessment in its own section, labelled as such, so readers can tell reported fact from judgement.
- Record the type and status of each reservation, because a scrutiny reservation and an objection call for different responses.
- Give dates for every next step and a named owner for every follow-up action.
- List what the notes leave unclear as questions to the author.

### MUST NOT DO
- Invent, infer or "complete" a delegation's position, a vote count or a date that the notes do not contain. A plausible guess is the most damaging error a flash report can carry.
- Count a silent delegation as supporting, or a scrutiny reservation as opposing.
- Turn the Commission's wish into the meeting's conclusion. Report what the chair concluded.
- Name individual national delegates or characterise delegations with adjectives.
- Present the flash report as the official record of the meeting.
- Narrate in speaking order. Group by position.

---
DRAFT — For review by an EU official before use. Not an official Commission position.
