---
name: legislative-cycle
description: >
  Run a full simulation of the EU Ordinary Legislative Procedure (OLP) from
  Commission initiative to Official Journal publication. Chains all six phases:
  Commission pre-proposal (impact assessment, consultation, ISC, College vote),
  EP first reading, Council first reading, trilogue, formal adoption, and OJ
  publication. Can run all phases in sequence or jump to a specific phase.
  Based on TFEU Art. 294 and the legislative-cycle workflow.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-simulation
  triggers: >
    legislative cycle, OLP, ordinary legislative procedure, Art. 294 TFEU,
    full cycle, end to end, from proposal to adoption, legislative process,
    commission to adoption, EP first reading, Council position, formal adoption,
    OJ publication, legislative simulation, regulation adoption, directive adoption
  role: workflow
  scope: legislative-cycle-simulation
  output-format: full-legislative-file
  institution: European Commission / European Parliament / Council of the EU
  related-skills: impact-assessment, consultation, inter-service-consultation,
    college-deliberation, european-parliament, council-eu, trilogue
---

# Legislative Cycle Coordinator

Runs the full six-phase simulation of the Ordinary Legislative Procedure. Acts
as a conductor: invokes each phase in sequence, passes the output of each phase
as input to the next, and maintains a running legislative file. Can be run
end-to-end (full simulation) or phase-by-phase (for deep dives). Understands
that the OLP is not linear — trilogue typically short-circuits second reading,
and the Commission's proposal is a living document that evolves through all phases.

---

## Core Workflow

```
PHASE 1 — COMMISSION INITIATIVE (~12–18 months)
  1a. /impact-assessment   → SWD produced by lead DG
  1b. /consultation        → 12-week public consultation
  1c. /treaty-check        → Legal Service opinion on legal basis
  1d. /inter-service-consultation → All DGs comment
  1e. /college-deliberation → College votes on adoption
  OUTPUT: COM([year]) [number] final

PHASE 2 — EP FIRST READING (~12–18 months)
  2a. /european-parliament → EP committee report + political group dynamics
  OUTPUT: EP first reading position (legislative resolution)

PHASE 3 — COUNCIL FIRST READING (~6–24 months)
  3a. /council-eu          → Council working party + COREPER + Council vote
  OUTPUT: Council first reading position (or adoption if EP position accepted)

PHASE 4 — TRILOGUE (informal, replaces second reading in 90% of cases)
  4a. /trilogue            → Rounds of negotiation → political agreement
  OUTPUT: Agreed compromise text

PHASE 5 — FORMAL ADOPTION
  5a. EP committee confirmation + plenary vote
  5b. Council formal adoption (QMV)
  5c. Signature by EP President and Council President
  OUTPUT: Signed legislative act

PHASE 6 — PUBLICATION
  6a. Legal-linguistic revision (all 24 EU languages)
  6b. OJ publication
  6c. Entry into force (20th day after OJ publication, or date in the act)
  OUTPUT: OJ reference — Regulation/Directive [number]/[year]/EU
```

---

## Reference Guide

| Resource | Path | Load when |
|---|---|---|
| Legislative cycle workflow | `knowledge/workflows/legislative-cycle.md` | Full session — phase definitions and timelines |
| College deliberation protocol | `knowledge/agents/college-deliberation.md` | Phase 1e |
| ISC protocol | `knowledge/agents/inter-service-consultation.md` | Phase 1d |
| Trilogue protocol | `knowledge/agents/trilogue.md` | Phase 4 |
| EP institutions agent | `knowledge/institutions/european-parliament.md` | Phase 2 |
| Council institutions agent | `knowledge/institutions/council-eu.md` | Phase 3 |

---

## Constraints

### MUST DO
- **Start with the legal basis** — before Phase 1a, identify the TFEU article
  conferring competence; every subsequent phase flows from this choice
  (QMV or unanimity; OLP or SLP; EP co-legislator or consulted)
- **Pass outputs between phases** — each phase's output is the input for the
  next; the EP cannot amend a proposal that has not been produced; the Council
  cannot adopt a position on text that does not exist
- **Flag where trilogue short-circuits second reading** — in practice, 90%+
  of OLP dossiers are closed in trilogue before formal second reading; model
  this as the default path
- **Note realistic timelines** — the Commission pre-proposal phase takes
  12–18 months; a full OLP cycle is typically 3–5 years; flag when the
  user's scenario implies an unrealistic speed

### MUST NOT DO
- **Do not skip the ISC or treaty-check** — these are not optional pre-proposal
  steps; a proposal that goes to College without ISC or Legal Service clearance
  is procedurally defective and would be sent back
- **Do not declare formal adoption without a political agreement text** —
  formal adoption in EP plenary and Council requires a specific agreed text;
  adoption cannot be declared without one

---

## Output Template

LEGISLATIVE CYCLE — [DOSSIER TITLE]
Instrument: [Regulation / Directive / Decision]
Legal basis: [TFEU Art. X] — Procedure: [OLP Art. 294 / SLP — specify]
Lead Commissioner: [Portfolio]
Lead DG: [DG name]
Simulated period: [YYYY–YYYY]

---

### Phase 1 — Commission Initiative

1a. Impact Assessment (SWD):
    [Key findings — preferred option — proportionality statement]

1b. Public Consultation:
    [Period — responses — key positions — fault lines]

1c. Treaty Check (Legal Service):
    Legal basis: [Confirmed / Alternative recommended]
    Subsidiarity: [Satisfied]
    Proportionality: [Satisfied]
    Charter: [No issues / Issues: specify]

1d. Inter-Service Consultation:
    [Summary of DG opinions — outstanding reservations]
    Conclusion: [ISC closed / Second round needed]

1e. College Deliberation:
    [Outcome: Adopted / Referred back — with conditions]

OUTPUT: COM([YYYY]) [NNN] final transmitted to EP and Council.

---

### Phase 2 — EP First Reading

Responsible committee: [ITRE / ENVI / LIBE / IMCO / etc.]
Rapporteur: [political group]
Key EP amendments: [List of significant EP additions/changes to Commission text]
Political group dynamics: [Where the majority is built]
EP first reading position: [Adopted by [N] votes for / [N] against]

---

### Phase 3 — Council First Reading

Council configuration: [COMPET / ENVI / EPSCO / etc.]
Key Council amendments: [List of significant Council divergences from Commission]
QMV check: [Blocking minority risk — which member states / why]
Council position: [Adopted / Blocking minority — dossier stalled]

[If EP and Council positions identical → Act adopted at Phase 3. Note this.]

---

### Phase 4 — Trilogue

Rounds: [N]
Key fault lines: [List]
[Round-by-round summary or direct to political agreement]

Political agreement: [Date] / Breakdown: [Risk assessment]

---

### Phase 5–6 — Formal Adoption and Publication

EP plenary vote: [N for / N against / N abstain]
Council formal adoption: [QMV — blocking minority check]
OJ publication: [OJ reference — L series]
Entry into force: [Date — 20th day after OJ publication]
Application date: [Date — if different from entry into force]

---

### Final Legislative Act

[REGULATION / DIRECTIVE] ([EU]) [YEAR]/[NUMBER] OF THE EUROPEAN PARLIAMENT
AND OF THE COUNCIL of [date] on [subject matter]

Key elements of the final text (vs. Commission proposal):
- [What changed and why — EP wins / Council wins / compromise]

[model knowledge — verify] for any specific current legislative procedure details.

> **DRAFT** — Simulation output. Not an official Commission position.
