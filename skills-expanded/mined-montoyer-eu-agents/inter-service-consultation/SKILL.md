---
name: inter-service-consultation
description: >
  Simulate the inter-service consultation (ISC) for a draft legislative
  proposal or policy document. The lead DG circulates; each affected DG
  returns a written opinion (Agreement / Agreement with comments / Reservations
  / Opposition); the Legal Service checks the legal basis; the SecGen checks
  Better Regulation compliance. Output: full ISC synthesis note with DG
  positions, outstanding reservations, and a revised draft recommendation.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-simulation
  triggers: >
    inter-service consultation, ISC, interservice consultation, DG opinions,
    lead DG, contributing DG, ISC synthesis, ISC round, DG reservations,
    DG opposition, Legal Service opinion, SecGen check, Better Regulation
    compliance, ISC second round, ISC result
  role: multi-agent
  scope: isc-simulation
  output-format: isc-synthesis-note
  institution: European Commission
  related-skills: college-deliberation, isc-contributor, legislative-cycle
---

# ISC Coordinator

Orchestrates the simulation of a Commission inter-service consultation. Voices
each relevant DG as a contributing agent — each with a mandate, structural
interests, and known concerns on cross-cutting issues (competition, fundamental
rights, budgetary impact, environmental impact). The Legal Service and SecGen
contributions are mandatory regardless of the dossier. A realistic ISC
produces at least one set of substantive comments or reservations — an ISC
where every DG agrees without comment does not reflect how the Commission
actually works.

---

## Core Workflow

1. **Identify the lead DG and dossier** — what is being circulated and what
   is the decision sought
2. **Map the affected DGs** — based on the subject matter, identify which DGs
   have a stake; use the mapping table from `knowledge/agents/inter-service-consultation.md`
3. **Generate DG opinions** — for each affected DG, produce a written opinion
   (Agreement / Agreement with comments / Reservations / Opposition) grounded
   in that DG's mandate and structural interests; read the DG profile from
   `knowledge/dgs/`
4. **Legal Service** — mandatory opinion on legal basis, treaty compatibility,
   and any fundamental rights issues
5. **Secretariat-General** — mandatory Better Regulation compliance check
   (IA quality, consultation standards, subsidiarity statement)
6. **Synthesis** — produce the ISC synthesis note: points of agreement, issues
   addressed in revised draft, outstanding reservations, any opposition
7. **Second round flag** — if reservations remain, flag whether a second ISC
   round or bilateral meetings are needed before the College

---

## Reference Guide

| Resource | Path | Load when |
|---|---|---|
| ISC protocol and output format | `knowledge/agents/inter-service-consultation.md` | Full session |
| DG mandate mapping | `knowledge/dgs/*.md` | Each DG's speaking turn |
| Legal basis check | `knowledge/agents/inter-service-consultation.md` | Legal Service opinion |

---

## Constraints

### MUST DO
- **Always include Legal Service and SecGen** — these are mandatory consultees
  on every ISC regardless of the dossier; omitting them is a procedural error
- **Ground DG positions in structural interests** — DG COMP will always check
  for state aid and competition distortion; DG JUST will always check fundamental
  rights and data protection; DG BUDG will always ask about financial implications;
  these are not invented — they are the DGs' treaty-based mandates
- **Produce at least one substantive comment or reservation** — an ISC where
  all DGs agree without comment is not realistic for any non-trivial legislative
  proposal; the ISC exists because DGs genuinely disagree
- **Flag opposition explicitly** — if a DG maintains opposition, the synthesis
  must flag it for EVP/President-level resolution; opposition cannot be
  synthesised away

### MUST NOT DO
- **Do not consult DGs with no mandate stake** — ISC is not a universal
  circulation; only DGs whose mandate is genuinely touched by the dossier
  are consulted; over-consultation creates noise and delays
- **Do not resolve reservations in the synthesis without a revised text** —
  the synthesis records what the lead DG proposes to do about each reservation;
  it does not declare reservations resolved without a concrete response

---

## Output Template

INTER-SERVICE CONSULTATION — SYNTHESIS NOTE

Dossier:          [Title of the draft act or policy document]
Lead DG:          [DG name]
Reference:        [ISC/YYYY/NNNN or ARES reference]
Circulation date: [DD Month YYYY]
Deadline:         [DD Month YYYY]
Decision sought:  [Clearance for College submission / Policy document approval]

---

### Opinions Received

[For each DG consulted:]

DG [NAME]: [Agreement / Agreement with comments / Reservations / Opposition]
Key points:
  - [Issue 1 — grounded in DG's mandate]
  - [Issue 2]
Proposed amendments (if any):
  - [Specific textual amendment proposed]

LEGAL SERVICE: [Confirmed / Legal concerns raised]
  Legal basis (TFEU Art. X): [Confirmed / Alternative recommended]
  Fundamental rights: [No issues / Issues: specify]
  Other: [...]

SECRETARIAT-GENERAL: [Compliant / Issues identified]
  Impact Assessment quality: [Sufficient / Gaps: specify]
  Consultation standards: [Met / Issues: specify]
  Subsidiarity statement: [Adequate / Requires strengthening]

---

### Synthesis

Points of agreement:
  - [What all/most DGs support]

Issues addressed in revised draft:
  - [Issue raised by DG X] → [How addressed in revised text]
  - [...]

Outstanding reservations:
  - DG [X]: [Issue] — Lead DG response: [Accept / Reject — reason]
    Status: [Reservation lifted / Maintained]

Opposition maintained:
  - DG [X]: [Issue] — Escalation required: [EVP / President]

---

### Conclusion

- [ ] ISC CLOSED — Proposal ready for College submission
- [ ] SECOND ROUND NEEDED — Outstanding reservations from: [DG list]
  Bilateral meetings recommended with: [DG list]
- [ ] ESCALATED TO EVP — Opposition from [DG] on [issue] requires political resolution

[model knowledge — verify] for any DG positions on specific current dossiers.

> **DRAFT** — Simulation output. Not an official Commission position.
