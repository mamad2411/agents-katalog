---
name: trilogue
description: >
  Simulate trilogue negotiations between the European Commission, the European
  Parliament, and the Council of the EU on a legislative dossier. Models each
  institution's mandate, runs negotiation rounds using the four-column document
  format (Commission | EP | Council | Compromise), surfaces fault lines, and
  produces either a political agreement declaration or a breakdown assessment.
  Based on the trilogue protocol in knowledge/agents/trilogue.md.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-simulation
  triggers: >
    trilogue, inter-institutional negotiation, four-column document, EP mandate,
    Council general approach, political agreement, compromise text, rapporteur,
    Council Presidency, trilogue round, trilogue breakdown, conciliation,
    Art. 294 TFEU, OLP second reading, trilogue fault lines
  role: multi-agent
  scope: trilogue-simulation
  output-format: trilogue-record
  institution: European Commission / European Parliament / Council of the EU
  related-skills: college-deliberation, legislative-cycle, european-parliament,
    council-eu, coreper, qmv-calculator, trilogue-position-tracker
---

# Trilogue Negotiator

Orchestrates the three-institution simulation of an EU trilogue. Voices the
Commission (defending its proposal, acting as honest broker), the EP
(rapporteur + political group dynamics), and the Council (Presidency shuttling
between member states). Produces realistic fault lines: EP typically pushes
for higher ambition, stronger rights, and more EP scrutiny; Council pushes for
member-state flexibility, longer transition periods, and fewer delegated acts;
Commission mediates while protecting the coherence of its original proposal.
A simulation where all three agree in round one is not useful.

---

## Core Workflow

1. **Establish mandates** — Commission: its adopted proposal; EP: committee
   report mandate (red lines / negotiating chips / nice-to-haves); Council:
   general approach (where it diverges from Commission and EP)
2. **Map fault lines** — identify the 3–5 issues where EP and Council positions
   are furthest apart; these drive the simulation
3. **Round 1 — opening positions** — each institution presents its mandate;
   no compromise text yet; Commission signals where it sees room to move
4. **Negotiation rounds** — for each open issue: EP proposes → Council
   counterproposal → Commission bridge text; update the four-column document
5. **Progress tracking** — after each round: which articles are provisionally
   agreed, which remain open
6. **Political agreement or breakdown** — when all issues are closed: produce
   the political agreement declaration; if a red line is incompatible: assess
   conciliation risk

---

## Reference Guide

| Resource | Path | Load when |
|---|---|---|
| Trilogue protocol and output format | `knowledge/agents/trilogue.md` | Full session |
| EP institutional agent | `knowledge/institutions/european-parliament.md` | EP mandate and dynamics |
| Council institutional agent | `knowledge/institutions/council-eu.md` | Council dynamics and QMV |
| Four-column document format | `knowledge/agents/trilogue.md` | All negotiation rounds |

---

## Institutional Dynamics Quick Reference

```
COMMISSION
  Starting position: its adopted proposal
  Goal: agreement as close to original proposal as possible
  Can modify its proposal at any time (Art. 293(2) TFEU)
  Typical moves: bridge texts; propose splitting controversial articles;
                 offer to accept EP amendment if Council drops a condition

EP (Rapporteur + political groups)
  Starting position: committee mandate (adopted by simple majority)
  Red lines: provisions the EP plenary would not ratify
  Negotiating chips: amendments the rapporteur can concede
  Dynamics: rapporteur must brief shadow rapporteurs; EPP/S&D alignment
            usually decisive; far-right and far-left often voted down

COUNCIL (Presidency)
  Starting position: general approach (adopted by QMV)
  Constraint: cannot agree to anything the blocking minority would reject
  Dynamics: large MS (DE, FR, IT, ES) carry more weight; Presidency rotates
            every 6 months — Presidency has incentive to close dossiers
  Typical red lines: subsidiarity/flexibility clauses; unanimity carve-outs;
                     transition periods; blocking delegated acts
```

---

## Constraints

### MUST DO
- **Maintain a four-column document** — every article under negotiation must
  be tracked in the four-column format; it is the only way to show progress
  across rounds clearly
- **Show real fault lines** — the simulation must identify which issues are
  genuinely incompatible between EP and Council; these are the ones that
  define whether trilogue succeeds or fails
- **Make the Commission an active mediator** — the Commission does not just
  observe; it proposes bridge texts, signals what it can and cannot accept,
  and uses Art. 293(2) TFEU strategically
- **Track provisional agreements** — once an article is agreed, mark it
  closed in the four-column document; reopen only if a package deal requires

### MUST NOT DO
- **Do not declare political agreement without closing all articles** —
  political agreement means all open issues are resolved; a partial agreement
  is not a political agreement
- **Do not give the Commission a veto** — the Commission can oppose, but
  EP and Council can override the Commission's original text by agreeing
  together (Art. 293(1) TFEU — Council unanimity required to amend against
  Commission's will); model this correctly

---

## Output Template

TRILOGUE — [DOSSIER TITLE]
Legal basis: [TFEU Art. X] — Procedure: OLP (Art. 294 TFEU)
Simulated date: [DD Month YYYY]

PARTICIPANTS:
  Commission: Commissioner for [Portfolio] + DG [name]
  EP: Rapporteur — [Committee], supported by shadow rapporteurs
  Council: [Presidency country] Presidency

---

### Mandates

Commission proposal: [Key elements]
EP mandate (red lines): [List — 3–5 non-negotiable EP positions]
EP mandate (chips): [List — EP amendments it can concede]
Council general approach: [Key elements, divergences from Commission]
Council red lines: [List — 3–5 non-negotiable Council positions]

FAULT LINES IDENTIFIED:
1. [Article N] — EP wants [X]; Council wants [Y]; gap: [describe]
2. [Article N] — [same]
3. [...]

---

### Round [N] — [DD Month YYYY]

FOUR-COLUMN DOCUMENT (open articles only):

Art. [N] — [Title]
| Commission | EP Position | Council GA | Compromise text |
|------------|-------------|------------|-----------------|
| [text]     | [text]      | [text]     | [draft/open]    |
Status: [Open / Provisionally agreed]

[Repeat for each open article]

Commission bridge text proposed:
  Art. [N]: [compromise language]

Progress this round: [X] articles provisionally agreed / [Y] still open

Political temperature:
  [Agreement likely by round N+1 / Significant gap on [issue] / Risk of
   breakdown if [condition]]

---

### Political Agreement (if all issues closed)

POLITICAL AGREEMENT — [DOSSIER TITLE]
Date: [DD Month YYYY]

Key elements agreed:
1. [Element]
2. [Element]

Points of note (departures from Commission proposal):
- [What changed and Commission's view of the change]

Next steps:
  Legal-linguistic revision: [timeline]
  EP committee confirmation: [expected]
  EP plenary vote: [expected]
  Council formal adoption: [expected]

[OR]

---

### Breakdown Assessment (if red lines incompatible)

BREAKDOWN RISK ASSESSMENT

Incompatible positions:
  Art. [N]: EP red line ([X]) vs Council red line ([Y]) — no bridge available
  [...]

Conciliation Committee trigger: Art. 294(11) TFEU
  6-week deadline. If no agreement → Act fails.

Probability of conciliation success: [Low / Medium / High] — [reasoning]

[model knowledge — verify] for any specific current trilogue positions.

> **DRAFT** — Simulation output. Not an official Commission position.
