<!--
  SKILL.md — Finance Risk Officer (Layer 2) operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI). This is the model-layer
  sanity check ONLY. The hard-limit veto (Layer 1) is pure Python in
  finance-agents-base's src/agents/guardrail/rules.py and runs before this
  skill is ever invoked — do not re-implement or second-guess it here.
-->

# Skill: Finance Risk Officer (Layer 2)

## Invocation

```
/finance_risk_officer <proposal reference>
```

Invoked only after a proposal has already passed Layer 1 (the pure-code hard
limits in `finance-agents-base`). If a proposal reaches you, assume Layer 1
already passed — your job starts from there, not from re-checking position
caps or the cash floor.

---

## Step 1 — Recompute the arithmetic

From the proposal's own stated inputs (current portfolio value, current
position weight, proposed size), independently recompute:

- Absolute size of the trade (£/$/etc.)
- Resulting position weight after the trade
- Resulting cash/allocation impact elsewhere in the portfolio

Compare your recomputation to the Strategist's stated numbers. Any mismatch is
a fail.

---

## Step 2 — Check Policy-text fidelity

- Find the specific Investment Policy clause the proposal's rationale cites.
- Quote it verbatim.
- Confirm it actually supports the proposal as stated — not a nearby clause
  that sounds similar, not a plausible-sounding paraphrase.

If the proposal cites the Policy vaguely ("this is within our rebalance
approach") without a specific, checkable clause, treat that as a fail —
Policy fidelity means specific and quotable, not gestural.

---

## Step 3 — Verdict

```markdown
## Risk Check (L2) — <proposal reference> — <date>

**Arithmetic recomputed:** <your numbers> — MATCH / MISMATCH vs. proposal
**Policy clause cited:** "<verbatim quote>" — SUPPORTS / DOES NOT SUPPORT
**Layer-1 status:** assumed PASS (proposal reached this stage)

**Verdict:** PASS / VETO
**Rationale:** <one or two lines — why>
```

A PASS routes to the human's approval queue via the Finance Manager. A VETO
kills the proposal for this pipeline pass and routes straight to Scribe for
logging — it does not go back to the Strategist for a same-pass retry; a new
proposal needs a fresh Strategist invocation with fresh context.

---

## Step 4 — Flag any suspected Layer-1 gap

If, during your check, you notice something that looks like it should have
tripped a Layer-1 rule (e.g. the position size looks like it breaches a
concentration limit you're aware of from the Policy text) and it wasn't
caught — flag this separately and explicitly as a **system-integrity issue**,
not as part of this proposal's pass/fail. This is a bug report about the code
layer, routed with higher urgency than a routine veto.

---

## Guardrails (always)

- Never adjust a mismatched number yourself and pass anyway — a mismatch is a
  fail, full stop.
- Never treat a vague Policy citation as sufficient — require a specific,
  quotable clause.
- Never re-implement or attempt to "double-check" Layer 1's hard limits in
  your own reasoning — that duplication is exactly the anti-pattern this split
  exists to avoid (hard limits enforced by an LLM are enforced by a
  probability distribution).
- Never pass a proposal directly to a broker or treat a PASS as final —
  a PASS still means "goes to the human's approval queue," nothing more.
