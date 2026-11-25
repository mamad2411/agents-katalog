---
name: fusion-debate
description: >-
  Stage an adversarial two-model debate on a contested either/or, then adjudicate. Use
  when the tension itself is the signal — A vs B, ship vs wait, build vs buy, this stack
  vs that. Two panelists from different families argue opposing sides across rounds; Codex
  names the cruxes and decides. Triggers: "debate", "argue both sides", "X vs Y", "steelman
  each side", "for and against".
---

# Fusion — Debate

This is the **`debate`** entrypoint. Load and run **`fusion-orchestrate`** forcing
`mode = debate`. Debate is the one mode where assigning a **stance** is legitimate, because
it is adversarial by construction — not a persona costume, but a deliberate steel-manning of
each side.

## Mechanic (`references/collaboration-modes.md` §4)
1. Pick **two** strong panelists from **different families** (e.g. 🔴codex vs ⬛grok, or
   🔷copilot vs 🟢opencode). Assign opposing positions.
2. **K rounds (1–3):** each side argues, then revises after reading the other's latest
   argument. Keep a side's prior answer if its revision round fails.
3. **You adjudicate:** name the single strongest point on each side; identify the **actual
   cruxes** they disagree on (often fewer than it looks); then **decide** — pick a side, say
   why, and state what evidence would flip you. Do not split the difference for politeness.

## Output
Verdict-contract format. Because debate resolves a decision: include **Kill Criteria** and
**one Concrete Next Step**. Surface the loser's strongest point honestly — a debate whose
losing side had no good argument was the wrong question. Record the run (`mode=debate`).

For a multi-sided (3+ option) decision, prefer `council`; debate is sharpest on a true
two-sided tension.
