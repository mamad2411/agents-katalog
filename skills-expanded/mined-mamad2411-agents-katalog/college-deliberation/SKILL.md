---
name: college-deliberation
description: >
  Simulate a full College of Commissioners meeting on a question or dossier.
  All 21 Commissioner agents are convened. The President opens, the lead
  Commissioner presents, EVPs assess cross-cutting implications, each
  Commissioner speaks once, and the President calls consensus or a formal
  vote. Output: full meeting record with positions, vote result, and outcome
  (adopted / referred back / withdrawn).
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-simulation
  triggers: >
    college deliberation, college vote, college of commissioners, college meeting,
    college-deliberate, weekly college, adopt proposal, college decision, college
    vote, commission adopt, commission college, commissioner vote
  role: multi-agent
  scope: college-simulation
  output-format: college-meeting-record
  institution: European Commission
  related-skills: commissioner, inter-service-consultation, trilogue
---

# College Deliberation Coordinator

Orchestrates the simulation of a College of Commissioners meeting. Voices all
21 Commissioner agents in sequence following the formal deliberation protocol.
Each Commissioner speaks strictly from their mandate. The President manages
the process — not as a neutral chair but as the politically responsible leader
who can impose a decision under TEU Art. 17(6)(c) if the College is deadlocked.
Productive tension between portfolios is the point: a College simulation where
everyone agrees immediately is unrealistic.

---

## Core Workflow

1. **Set the scene** — identify the lead Commissioner, the dossier, and the
   decision sought; read the relevant Commissioner knowledge files
2. **President opens** — frames the question, notes the treaty basis, sets the
   decision threshold
3. **Lead Commissioner presents** — 5-minute presentation: problem, options,
   recommendation, DG analysis summary
4. **EVP layer** — each relevant EVP assesses cross-cutting implications
   (Green Deal/DNSH, Digital/tech sovereignty, Economy/competitiveness,
   Democracy/rule of law)
5. **Commissioner contributions** — each of the remaining Commissioners
   speaks once: Support / Reservations / Opposition, grounded in their mandate
6. **President reads the room** — identifies consensus, strong minority, or
   blocking objection
7. **Formal vote if needed** — each Commissioner votes; simple majority 11/21
8. **Outcome + next steps** — Adopted / Referred back (with conditions) /
   Withdrawn

---

## Reference Guide

| Resource | Path | Load when |
|---|---|---|
| College deliberation protocol | `knowledge/agents/college-deliberation.md` | All sessions — full protocol and output format |
| All 21 Commissioner personas | `knowledge/commissioners/*.md` | Each Commissioner's speaking turn |
| Conflict escalation rules | `knowledge/agents/college-deliberation.md` | When two positions are irreconcilable |

---

## Constraints

### MUST DO
- **Voice all 21 Commissioners** — every member of the College speaks;
  silencing Commissioners who would plausibly oppose creates an unrealistic
  simulation; the difficult voices are often the most instructive
- **Ground every position in mandate** — a Commissioner who speaks outside
  their portfolio mandate is not realistic; if their portfolio has no stake in
  the question, their contribution is brief ("This portfolio has no objection
  from a [X] perspective") rather than absent
- **Make the President active, not neutral** — the President frames the
  debate, manages tensions, and ultimately takes responsibility for the
  outcome; a passive President produces an inconclusive simulation
- **Name the fault lines** — after all contributions, the President's
  consensus assessment must explicitly name which portfolios are in tension
  and why, not just count votes

### MUST NOT DO
- **Do not manufacture consensus** — if the dossier genuinely divides
  portfolios (e.g., an industrial subsidy that Competition opposes),
  the simulation must show that division; artificial unanimity is not useful
- **Do not skip the EVP layer** — EVPs hold cross-cutting coordination
  authority; their assessment shapes how individual Commissioners position
  themselves; a simulation without EVP contributions misses the College's
  internal hierarchy

---

## Output Template

COLLEGE OF COMMISSIONERS — [Meeting reference, e.g., PV(2024)2400]
Subject: [Dossier title]
Simulated date: [DD Month YYYY]
Decision sought: [Adopt for transmission to EP/Council / Note / Other]

---

### President — Opening

[Opening statement: question framed, treaty basis noted, key tensions flagged,
decision threshold set]

---

### Lead Commissioner ([Portfolio]) — Presentation

[Problem summary — options considered — recommended approach — DG analysis]

---

### EVP Assessments

EVP Green Deal: [DNSH compatibility / Green Deal alignment / position]
EVP Digital: [Digital/tech sovereignty implications / position]
EVP Economy: [Competitiveness / single market / position]
EVP Democracy: [Rule of law / fundamental rights / position]

---

### Commissioner Contributions

[For each Commissioner — in order of the College roster:]

[PORTFOLIO]: [Support / Reservations / Opposition]
[1–3 sentences grounded in their mandate. Name any specific conditions
or red lines.]

[Repeat for all remaining Commissioners]

---

### President — Consensus Assessment

[Reading of the room:]
Clear majority: [Yes/No]
Key tensions: [Portfolio A vs Portfolio B on [issue] — nature of disagreement]
Blocking objection: [Yes/No — from which portfolio and on what grounds]

[President's call:]
- [ ] Consensus clear → ADOPT
- [ ] Significant reservations → [Modifications requested / Second round]
- [ ] Fundamental division → Formal vote called

---

### Formal Vote (if Called)

In favour ([N]):  [Portfolio list]
Against ([N]):    [Portfolio list]
Abstain ([N]):    [Portfolio list]
Result: [N/21 — threshold: 11 for adoption]

---

### Outcome

- [ ] ADOPTED — [next step: COM document / transmission / publication]
- [ ] REFERRED BACK — Lead DG must address: [specific conditions]
  Return deadline: [date]
- [ ] WITHDRAWN — Reasons: [...]

[model knowledge — verify] for any claims about specific current dossiers
or Commissioner political positions.

> **DRAFT** — Simulation output. Not an official Commission position.
