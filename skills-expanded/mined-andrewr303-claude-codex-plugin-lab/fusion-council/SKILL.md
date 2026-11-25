---
name: fusion-council
description: >-
  Convene the Fusion council for a high-stakes, open-ended decision: blind independent
  analysis, then anonymized cross-examination with anti-conformity pressure, then a
  synthesized verdict with a minority report. Use for architecture calls, irreversible
  choices, "is this plan sound", "what am I missing", pre-mortems. Triggers: "council",
  "convene the council", "deliberate", "pressure-test this decision".
---

# Fusion — Council

This is the **`council`** entrypoint. Load and run **`fusion-orchestrate`** (the Conductor),
forcing `mode = council`. Council is the heavy instrument — reserve it for decisions whose
cost of being wrong justifies three rounds across four model families.

## What makes council different from a plain panel
A panel fuses *independent* answers once. A council makes the panelists **deliberate** —
and the entire value is in keeping that deliberation from collapsing into polite agreement.

Run the three-round mechanic from `references/collaboration-modes.md` (§3) and apply
`references/anti-conformity.md` in full:
1. **R1 blind** independent analysis + recommendation.
2. **R2 anonymized** cross-examination (Member A/B/C/D) with the verbatim name-the-flaw
   directive — "update only for a flaw you can name."
3. **R3 crystallize** (≤120 words, no new arguments).
4. **You chair the synthesis.** Force a counterfactual if agreement >~70%. Carry a
   **Minority Report** if a reasoned dissent survives to R3. Never manufacture consensus.

## Output
Verdict-contract format (`references/verdict-contract.md`), and because this is a decision:
**Kill Criteria** (dated, observable) + exactly **one Concrete Next Step** are mandatory.
Record the run (`mode=council`) so the ledger learns which panelists win deliberations.

If fewer than 3 panelists are live, say so — a 2-member "council" is really a `debate`;
route there or proceed with an honest, downgraded panel.
