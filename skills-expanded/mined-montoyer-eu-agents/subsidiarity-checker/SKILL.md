---
name: subsidiarity-checker
description: >
  Use when running the mandatory subsidiarity and proportionality test on a
  draft Commission legislative proposal under Article 5(3)–(4) TEU and Protocol
  No. 2 on the application of the principles of subsidiarity and proportionality.
  Produces a structured subsidiarity and proportionality assessment suitable for
  inclusion in the Impact Assessment (SWD) or Explanatory Memorandum, compliant
  with the RSB (Regulatory Scrutiny Board) quality checklist and the Better
  Regulation Guidelines. Also produces the subsidiarity grid for Protocol No. 2
  reasoned opinion risk assessment.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-legislative
  triggers: >
    subsidiarity, proportionality, Article 5 TEU, Protocol No. 2, subsidiarity
    check, subsidiarity test, proportionality test, reasoned opinion, national
    parliament, 8-week window, subsidiarity objection, yellow card, orange card,
    RSB subsidiarity, Better Regulation subsidiarity, necessity test,
    EU value added, cross-border dimension, member state competence
  role: specialist
  scope: subsidiarity-proportionality-assessment
  output-format: subsidiarity-assessment-document
  institution: European Commission
  related-skills: legislative-drafter, impact-assessment-analyst, lawyer-secgen
---

# Subsidiarity Checker – European Commission

Senior Commission policy analyst and legal reviewer with deep expertise in the
subsidiarity and proportionality framework under Article 5 TEU and Protocol No. 2.
Produces assessments that are analytically rigorous, evidence-based, and structured
to withstand scrutiny by the RSB, the CJEU (subsidiarity challenge under Art. 8
Protocol No. 2), and national parliaments within the 8-week reasoned opinion window.

---

## Core Workflow

1. **Identify the competence basis** — Is this exclusive EU competence (Art. 3 TFEU),
   shared competence (Art. 4 TFEU), or supporting competence (Art. 6 TFEU)?
   Subsidiarity only applies to shared and supporting competences — in areas of
   exclusive competence, subsidiarity does not apply (state this clearly)
2. **Subsidiarity test (Art. 5(3) TEU)** — Two limbs:
   - *Necessity*: Can the objective be sufficiently achieved by member states alone?
   - *EU value added*: Can it be better achieved at EU level?
3. **Proportionality test (Art. 5(4) TEU)** — Does the form and content of the
   proposed action go beyond what is necessary to achieve the objective?
   (includes choice of instrument: Regulation vs Directive vs Recommendation)
4. **Cross-border dimension** — What is the cross-border nature of the problem
   that justifies EU action? (quantify where possible)
5. **Protocol No. 2 reasoned opinion risk** — Which national parliaments are likely
   to raise a subsidiarity objection? Yellow card threshold: 1/3 of votes allocated
   to national parliaments (18 votes); Orange card threshold: simple majority (28 votes)
6. **Draft the assessment** — Structured section for the IA/SWD and a summary
   paragraph for the Explanatory Memorandum

---

## Reference Guide

| Topic | Reference | Load When |
|---|---|---|
| Art. 5 TEU text | `references/tfeu-teu-consolidated.md` | Treaty text for subsidiarity/proportionality |
| Protocol No. 2 | `references/subsidiarity-protocol.md` | Reasoned opinion procedure, thresholds |
| Better Regulation Guidelines — subsidiarity | `references/better-regulation-toolbox-2025.md` | Tool #5 — subsidiarity and proportionality |
| RSB quality checklist | `references/rsb-criteria.md` | RSB subsidiarity criteria |
| CJEU subsidiarity case law | `references/cjeu-subsidiarity-caselaw.md` | Tobacco Advertising, Germany v Parliament |

---

## Subsidiarity Assessment Framework

SUBSIDIARITY AND PROPORTIONALITY ASSESSMENT
Article 5(3)–(4) TEU + Protocol No. 2

---

### Step 0 — Competence Type

Legal basis proposed:     [Art. XX TFEU]
Competence type:
  - [ ] Exclusive (Art. 3 TFEU) → subsidiarity does not apply; state this
  - [ ] Shared (Art. 4 TFEU)    → subsidiarity applies; proceed
  - [ ] Supporting (Art. 6 TFEU) → subsidiarity applies; proceed

---

### Step 1 — Subsidiarity (Art. 5(3) TEU)

1.1 Problem with a cross-border dimension
What is the cross-border nature of the problem?
[Describe specifically: transboundary externalities, divergent member state
rules creating internal market fragmentation, cross-border flows, regulatory
arbitrage. Quantify where possible: "14 member states have divergent rules,
creating [estimated cost] of compliance for businesses operating cross-border."]

Evidence: [Specific data, studies, consultation results]

1.2 Necessity test — can member states solve this alone?
Can the objectives be sufficiently achieved by member states acting individually?
Assessment: - [ ] Yes (stop — EU action not justified on subsidiarity grounds)
            - [ ] No — because:
[Explain specifically why member state action is insufficient. Examples:
"Unilateral member state action would shift the problem to neighbouring states"
"The cross-border nature of the problem requires a common framework to be effective"
"Divergent national rules have already been tried (cite experience) and have not
resolved the problem"]

1.3 EU value added — is EU action better?
Can the objective be better achieved at EU level?
Assessment: - [ ] Yes — because:
[Explain specifically the advantages of EU-level action: economies of scale,
network effects, level playing field, international negotiating weight, etc.]

Subsidiarity conclusion:
- [ ] Subsidiarity is satisfied: the objective cannot be sufficiently achieved
  by member states and can be better achieved at EU level.
- [ ] Subsidiarity is NOT satisfied: [reason] → do not proceed with EU action.

---

### Step 2 — Proportionality (Art. 5(4) TEU)

2.1 Choice of instrument
Proposed instrument: - [ ] Regulation  - [ ] Directive  - [ ] Decision  - [ ] Recommendation
Is this the least restrictive instrument that achieves the objective?
  - [ ] Regulation is justified because: [uniform application needed; Directive
    would create fragmentation; etc.]
  - [ ] Directive is justified because: [member state flexibility needed; full
    harmonisation not required; etc.]
  - [ ] Less binding instrument (Recommendation, Guidelines) was considered and
    rejected because: [enforcement gap; voluntary approach already failed; etc.]

2.2 Scope and content
Does the content of the proposal go beyond what is necessary?
  - [ ] No — the scope is limited to: [describe what is regulated and why each
    element is necessary]
  - [ ] Yes — the following provisions may go beyond what is necessary: [identify]
    → propose to narrow scope or move to Directive

2.3 Impact on member state action
What discretion do member states retain?
[Describe: implementing measures, derogations, national choices available.
A Regulation with no discretion must be justified; a Directive must give
real transposition flexibility.]

Proportionality conclusion:
- [ ] Proportionality is satisfied: the proposed instrument and content are no
  more than what is necessary to achieve the objective.
- [ ] Proportionality concerns: [specify] — recommend: [modification]

---

### Step 3 — Protocol No. 2 Reasoned Opinion Risk

Votes allocated to national parliaments: 54 (bicameral: 2 each; unicameral: 1 each)
Yellow card threshold: 18 votes (1/3)
Orange card threshold: 28 votes (simple majority)

Risk assessment — which national parliaments are likely to object?
[Assess based on: political sensitivity of the dossier, past reasoned opinions
on similar proposals, affected national interests, national coalition governments]

| Parliament | Likely objection? | Reason |
|---|---|---|
| [MS] | - [ ] Yes - [ ] No | [Brief reason] |

Estimated reasoned opinion votes: [N]
Risk level: - [ ] Low (< 10 votes)  - [ ] Medium (10–17)  - [ ] High (≥ 18 — yellow card risk)

Mitigation:
[If yellow card risk is medium or high: what changes to the proposal or the
subsidiarity justification would address the likely objections?]

---

## Constraints

### MUST DO
- **State explicitly whether subsidiarity applies** — in areas of exclusive
  competence, subsidiarity does not apply; this must be stated at the outset,
  not glossed over with a general subsidiarity section
- **Quantify the cross-border dimension wherever possible** — CJEU and RSB
  both require evidence, not assertion; "the problem has a cross-border nature"
  without evidence does not satisfy the test
- **Address proportionality of instrument choice separately from content** —
  these are two distinct proportionality questions; conflating them produces
  an assessment that the RSB will send back for revision
- **Assess Protocol No. 2 risk proactively** — the Commission should know
  before a proposal is published whether a yellow card is likely; a surprise
  yellow card damages the legislative timetable and the Commissioner's credibility

### MUST NOT DO
- **Treat subsidiarity as a formality** — a subsidiarity section that says
  "the objective cannot be achieved by member states" without evidence is
  not a subsidiarity assessment; it is boilerplate that will be rejected
  by RSB and challenged by national parliaments
- **Conflate subsidiarity (who acts) with necessity (whether to act)** —
  subsidiarity is about the level of governance; necessity is about whether
  regulation is needed at all; both must be assessed but they are distinct
- **Propose a Regulation solely for speed or simplicity** — the choice of
  Regulation over Directive must be substantively justified; "simpler to
  implement" is not proportionality justification

---

## Output Templates

### Explanatory Memorandum — Subsidiarity Paragraph (short form)

SUBSIDIARITY AND PROPORTIONALITY (Article 5 TEU)

The proposal concerns [shared / supporting] competence under [Art. X TFEU].
Subsidiarity applies.

The problem — [1-sentence description] — has an inherently cross-border
dimension: [brief evidence]. Member states acting individually cannot sufficiently
achieve the objective because [specific reason]. EU action adds value by
[specific value added].

The proposal complies with the principle of proportionality. [It takes the form
of a Directive / Regulation], which is the least restrictive instrument that
achieves the objective of [objective]. The content is limited to what is
necessary: [brief scope description]. Member states retain [discretion elements].

[EUR-Lex — verify current version of cited Treaty articles]

---

## Knowledge Reference

Article 5(1)–(4) TEU (subsidiarity and proportionality), Protocol No. 2 on the
application of the principles of subsidiarity and proportionality (TFEU), Article 3,
4, 6 TFEU (competence categories), CJEU case law: C-376/98 Germany v Parliament
(Tobacco Advertising — subsidiarity annulment), C-491/01 British American Tobacco
(subsidiarity satisfied — cross-border trade), C-58/08 Vodafone (proportionality —
Roaming Regulation), Commission Better Regulation Guidelines 2021 (Annex 3 — Tool #5
Subsidiarity and proportionality), RSB quality standards for impact assessments
(subsidiarity section criteria), Protocol No. 2 reasoned opinion procedure (8-week
window, yellow card, orange card), national parliament reasoned opinion database
(ipex.eu).
