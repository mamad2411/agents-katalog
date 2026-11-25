---
name: subsidiarity-stress
description: >
  Tests the subsidiarity justification of a proposal against five different
  member-state configurations — varying by regulatory capacity, economic size,
  existing national legislation, and political orientation — to identify the
  configuration under which the subsidiarity check fails. A proposal that
  satisfies the subsidiarity test in Germany may fail it in Malta. This skill
  surfaces those failures before the text is written, so the proportionality
  and necessity arguments can be hardened in the impact assessment.
  Based on Protocol No. 2 (TEU/TFEU) and the Better Regulation subsidiarity
  test.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-simulation
  triggers: >
    subsidiarity stress, subsidiarity-stress, subsidiarity test, subsidiarity
    check, subsidiarity failure, member state subsidiarity, protocol 2,
    subsidiarity protocol, subsidiarity challenge, yellow card risk,
    necessity test, proportionality subsidiarity, subsidiarity across member states
  role: workflow-analysis
  scope: subsidiarity-testing
  output-format: subsidiarity-stress-report
  institution: European Commission
  related-skills: treaty-check, mandate-conflict, timeline, legislative-cycle
---

# Subsidiarity Stress Tester

Tests the subsidiarity justification of a policy proposal against five
structurally distinct member-state configurations. The goal is not to simulate
a yellow card procedure — it is to find the configuration under which the
subsidiarity argument is weakest, so the Commission can harden the necessity
and proportionality reasoning in the impact assessment before the proposal
is written.

The subsidiarity test under Protocol No. 2 has two dimensions:
1. **Necessity** — could the objective be sufficiently achieved by member
   states acting alone (at central, regional, or local level)?
2. **EU added value** — would EU action produce a clear benefit over national
   action, by reason of scale or effects?

Both dimensions are answered differently depending on the member state's
regulatory capacity, market size, existing legislation, and political
orientation. This skill makes that variation explicit.

---

## Core Workflow

1. **Parse the proposal** — identify the policy objective, instrument type
   (regulation/directive/decision), and the necessity argument implied by the
   legal basis
2. **Select five member-state configurations** — choose configurations that
   maximise stress on the subsidiarity argument; default set below, adjustable:
   - **MS-1: Large, high-capacity, aligned** (e.g., Germany/France) —
     regulatory capacity to act alone; baseline case
   - **MS-2: Large, high-capacity, divergent** (e.g., same states with
     existing national legislation that would be pre-empted)
   - **MS-3: Small, high-capacity** (e.g., Netherlands/Denmark) —
     sufficient capacity but limited scale argument; may not need EU action
   - **MS-4: Small, lower-capacity** (e.g., Bulgaria/Romania) —
     cannot achieve objective alone; strongest case for EU action
   - **MS-5: Large, politically resistant** (e.g., Hungary/Poland on a
     dossier in their area of political contestation) — questions EU
     competence for political reasons; maximum yellow card risk
3. **For each configuration, apply the two-limb test:**
   - Necessity: Could this MS achieve the objective sufficiently alone?
     Consider: existing national legislation, regulatory capacity, market
     size, cross-border spillovers
   - EU added value: Is there a clear benefit from EU-level action for this
     MS that would not exist from national action?
4. **Rate subsidiarity compliance per configuration:**
   - **SATISFIED** — Both limbs met; yellow card risk low
   - **ARGUABLE** — Both limbs technically met but the argument is thin;
     motivated MS national parliament could issue reasoned opinion
   - **CONTESTED** — Necessity limb weak; MS can plausibly argue it could
     act alone; yellow card risk elevated
   - **FAILS** — Necessity not established for this configuration; EU action
     not justified under Protocol No. 2
5. **Identify the critical configuration** — the one where subsidiarity is
   weakest; this is the configuration the impact assessment must address
6. **Assess yellow card risk** — Protocol No. 2 yellow card requires 1/3 of
   national parliamentary chambers to issue reasoned opinions; identify
   whether the weakest configurations cluster around a realistic blocking
   coalition of national parliaments
7. **Recommend impact assessment hardening** — for the weakest configurations,
   identify what additional evidence or legal argument would strengthen the
   subsidiarity justification

---

## Reference Guide

| Resource | Path | Load when |
|---|---|---|
| Treaty check workflow | Knowledge of Protocol No. 2 to TEU/TFEU | All sessions |
| Legislative cycle workflow | `knowledge/workflows/legislative-cycle.md` | Step 6 (yellow card timing) |

---

## Constraints

### MUST DO
- **Apply both necessity and EU added value limbs** — a subsidiarity argument
  that only addresses cross-border effects without establishing that member
  states cannot act alone fails Protocol No. 2
- **Vary configurations meaningfully** — five identical large-country
  configurations do not stress-test subsidiarity; the point is to find the
  weakest case
- **Be honest about FAILS ratings** — if the necessity argument does not hold
  for a configuration, say so; understating subsidiarity weakness leads to
  proposals that fail in Council or are struck down by the ECJ
- **Distinguish subsidiarity from proportionality** — this skill tests
  subsidiarity (whether EU should act at all); proportionality (whether the
  instrument is appropriate in scope and intensity) is a separate test
  addressed by `/treaty-check`

### MUST NOT DO
- **Do not assume cross-border effects automatically satisfy subsidiarity** —
  cross-border effects are a necessary but not sufficient condition; the
  question is whether member states acting in concert (without EU action)
  could achieve the same result
- **Do not run only large-country configurations** — large-country analysis
  systematically understates subsidiarity risk; small MS configurations are
  where the test is hardest
- **Do not conflate yellow card risk with subsidiarity failure** — a proposal
  can be legally sound on subsidiarity and still trigger a yellow card for
  political reasons; flag both risks separately

---

## Output Template

SUBSIDIARITY STRESS TEST
Proposal: [Title / one-line description]
Legal basis (proposed): [TFEU Art. X — competence type: exclusive / shared / supporting]
Policy objective: [One sentence]
Necessity argument (as drafted): [One sentence — the Commission's implied or stated basis]

Overall subsidiarity risk: [LOW / MODERATE / HIGH / CRITICAL]
Yellow card risk: [LOW / ELEVATED / HIGH]

---

### Configuration Results

| Configuration | MS Profile | Necessity | EU Added Value | Verdict |
|---|---|---|---|---|
| MS-1 | [Profile] | [Met / Thin / Not met] | [Met / Thin / Not met] | [SATISFIED / ARGUABLE / CONTESTED / FAILS] |
| MS-2 | [Profile] | [Met / Thin / Not met] | [Met / Thin / Not met] | [SATISFIED / ARGUABLE / CONTESTED / FAILS] |
| MS-3 | [Profile] | [Met / Thin / Not met] | [Met / Thin / Not met] | [SATISFIED / ARGUABLE / CONTESTED / FAILS] |
| MS-4 | [Profile] | [Met / Thin / Not met] | [Met / Thin / Not met] | [SATISFIED / ARGUABLE / CONTESTED / FAILS] |
| MS-5 | [Profile] | [Met / Thin / Not met] | [Met / Thin / Not met] | [SATISFIED / ARGUABLE / CONTESTED / FAILS] |

---

### Critical Configuration Analysis

Configuration: [MS-X — Profile]
Why this is the weakest case: [2–3 sentences on why this configuration produces
the strongest subsidiarity challenge — existing national law, capacity, scale]

Necessity limb weakness: [Specific gap in the necessity argument for this
configuration]

EU added value weakness: [Specific gap in the added value argument for this
configuration]

---

### Yellow Card Assessment

Chambers likely to issue reasoned opinions: [List configurations and the
national parliaments they correspond to]
Count toward 1/3 threshold: [N chambers out of ~40 total]
Yellow card risk: [LOW (<5 chambers) / ELEVATED (5–12) / HIGH (>12)]

[Note: A yellow card does not block the proposal — the Commission must review
and explain whether it maintains, amends, or withdraws the proposal. But it
delays and politically weakens the dossier.]

---

### Impact Assessment Hardening Recommendations

For the critical configuration to move from [FAILS/CONTESTED] to [ARGUABLE]:
1. [Specific evidence or legal argument needed — e.g., quantify cross-border
   spillover for smaller MS; cite existing national legislation gaps]
2. [Specific design change that would strengthen the necessity argument —
   e.g., framework directive approach that leaves implementation to MS]

For yellow card risk reduction:
1. [Specific change to subsidiarity statement in the explanatory memorandum]
2. [Consultation or engagement with national parliaments prior to proposal]

[model knowledge — verify] for all Protocol No. 2 citations and member-state
legislative references.

> **DRAFT** — Simulation output. Not an official Commission position.
