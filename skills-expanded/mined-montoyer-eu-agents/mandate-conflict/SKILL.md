---
name: mandate-conflict
description: >
  Given a policy brief or draft proposal, identify every pair of Commissioner
  portfolios where a structural conflict is guaranteed — not merely possible.
  A structural conflict exists when two mandates, both treaty-grounded, point
  in opposite directions on the same question by design. Returns a conflict
  map: portfolio pairs, the legal basis for each position, the nature of the
  incompatibility, and a severity rating. This is not a summary of "tensions"
  — it is a map of the fault lines the proposal must cross before College
  adoption is possible.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-simulation
  triggers: >
    mandate conflict, portfolio conflict, commissioner conflict, conflict map,
    structural conflict, mandate-conflict, who will oppose, which commissioners
    will disagree, college fault lines, portfolio tensions, guaranteed objections
  role: multi-agent-analysis
  scope: conflict-mapping
  output-format: conflict-map
  institution: European Commission
  related-skills: college-deliberation, red-team-college, inter-service-consultation
---

# Mandate Conflict Analyser

Reads all 21 Commissioner knowledge files and the submitted proposal, then
identifies every pair of portfolios where conflict is **structurally
guaranteed** — where both mandates are treaty-grounded and point in opposite
directions on the same question by design. The output is not a deliberation
and not a list of concerns: it is a conflict map that shows which fault lines
must be bridged before the proposal can survive College.

The distinction between a structural conflict and a negotiating position matters.
A structural conflict cannot be resolved by compromise language alone — it
requires either a substantive policy change, an explicit exemption grounded in
the treaty, or a College decision that one mandate takes precedence on this
dossier. The map should help the lead Commissioner decide which fights must be
won, which can be avoided by design, and which require Presidential arbitration.

---

## Core Workflow

1. **Parse the proposal** — identify the policy domain, legal basis, key
   instruments, beneficiaries, and any proposed obligations, prohibitions, or
   delegations
2. **Load all 21 Commissioner knowledge files** — for each portfolio, read
   the mandate, treaty basis, key dossiers, and stated tensions
3. **Map first-order conflicts** — for each Commissioner, assess whether the
   proposal directly implicates their mandate and in which direction
4. **Identify structural pairs** — find every pair (A, B) where both:
   - Commissioner A's mandate creates a positive obligation or entitlement
     that the proposal advances or threatens
   - Commissioner B's mandate creates a positive obligation or entitlement
     that points in the opposite direction on the same element
5. **Assess severity** — rate each conflict:
   - **BLOCKING** — one portfolio cannot support the proposal without a
     fundamental change; College adoption requires Presidential override or
     dossier redesign
   - **SIGNIFICANT** — real incompatibility requiring a textual fix or
     explicit carve-out; will produce strong reservations at College
   - **MANAGEABLE** — genuine tension but resolvable through compromise
     language or a joint note without redesigning the proposal
6. **Identify avoidable conflicts** — note where a design choice in the
   proposal (scope, legal basis, instrument type) is creating a conflict that
   a different design would avoid without sacrificing the policy objective
7. **Identify arbitration points** — flag conflicts where President's
   political authority is the only resolution path

---

## Reference Guide

| Resource | Path | Load when |
|---|---|---|
| All 21 Commissioner personas | `knowledge/commissioners/*.md` | Step 2 — full load required |
| College deliberation protocol | `knowledge/agents/college-deliberation.md` | Step 7 — arbitration rules |

---

## Constraints

### MUST DO
- **Read all 21 Commissioner files** — partial analysis produces a partial
  conflict map; the most dangerous conflicts are often between non-obvious
  portfolio pairs (e.g., Justice vs. Internal Market on data sharing mandates)
- **Distinguish structural from negotiating conflicts** — a Commissioner who
  has reservations is different from a Commissioner whose treaty mandate
  directly contradicts the proposal; only the latter is a structural conflict
- **State the legal basis for each position** — every conflict entry must
  include the TFEU article or secondary legislation that grounds each side;
  a conflict not grounded in treaty text is a political preference, not a
  mandate conflict
- **Rate severity honestly** — understating severity misleads the lead
  Commissioner into underestimating what must be resolved before College

### MUST NOT DO
- **Do not list all possible concerns** — the output is a conflict map, not a
  College simulation; limit entries to structurally guaranteed conflicts
- **Do not propose solutions** — the map describes the problem space;
  resolution is for the lead Commissioner and, where necessary, the President
- **Do not skip portfolios with no stake** — explicitly note them as
  "No structural conflict identified" so the absence is on the record

---

## Output Template

MANDATE CONFLICT MAP
Proposal: [Title / one-line description]
Legal basis (proposed): [TFEU Art. X]
Lead Commissioner: [Portfolio]
Analysis date: [DD Month YYYY]

---

### Summary

Structural conflicts identified: [N]
  — BLOCKING: [N]
  — SIGNIFICANT: [N]
  — MANAGEABLE: [N]

Portfolios with no structural stake: [list]

---

### Conflict Entries

---

**CONFLICT [N] — [SEVERITY: BLOCKING / SIGNIFICANT / MANAGEABLE]**

Portfolio A: [Commissioner for X]
Treaty basis: [TFEU Art. X / Reg. (EU) X/XXXX]
Position: [What this mandate requires or prohibits — one sentence]

Portfolio B: [Commissioner for Y]
Treaty basis: [TFEU Art. X / Reg. (EU) X/XXXX]
Position: [What this mandate requires or prohibits — one sentence]

Nature of incompatibility:
[Why these two positions cannot both be satisfied by the current proposal
design — 2–4 sentences. Be specific: identify the provision, obligation,
or instrument that creates the clash.]

Avoidable by design?
[ ] Yes — [What design change would remove the conflict without sacrificing
    the policy objective]
[ ] No — [Why the conflict is intrinsic to the policy objective]

Resolution path:
[ ] Textual fix — [specific change]
[ ] Explicit carve-out — [scope or instrument adjustment]
[ ] Presidential arbitration — [nature of the political decision required]
[ ] Dossier redesign — [what would need to change fundamentally]

---

[Repeat for each structural conflict]

---

### Arbitration Points for President

[List only the BLOCKING conflicts — for each, one sentence on the political
decision the President must make if the proposal is to proceed unchanged.]

---

### Portfolios with No Structural Stake

[Commissioner for X] — [One sentence: why this mandate is not directly
implicated by this proposal.]
[Repeat for each]

[model knowledge — verify] for all treaty citations and mandate descriptions.

> **DRAFT** — Simulation output. Not an official Commission position.
