---
name: compact
description: >-
  use this when you need a one-line-focus compact — especially
  implement→QA — without clearing or handing off; know when NOT to compact
license: MIT
metadata:
  portability: portable
---
# compact

Squeeze a session that already holds work into a **secondary source**, then continue with a one-line focus.

## Primary vs secondary (lossy historian)
- **Primary source** = the live session (people who were "in the room" — full grilled/implement reasoning).
- **Secondary source** = the summary after compact (or a handoff doc) — a **lossy historian**. Useful for maneuverability; always drops some *why*.
- Trade-off: continue = full info + noise + limited room; compact = less noise + more room + information loss.

Harness command names differ. Canonical action is compact-with-focus. There is no `docs/HARNESS-MATRIX.md`.

## When (same agent / same directory still owns the work)
- Need smart-zone room without a full clear (working budget ~150k — see handoff for the full phase-boundary tree).
- **Cast-iron case: implement → QA** on what you just built — validate, don't re-architect; keep a focused summary so QA doesn't re-explore from zero (re-explore alone is also lossy on *why*).
- Residual default at the bottom of the phase-boundary tree when clear/handoff/subagent don't fit.

## When NOT to compact
- Context is **irrelevant** to what's next → **Clear** (cheapest; most room).
- Crossing **agent / directory / person** → **Handoff** (portable temp doc; compaction can't seed another product).
- **AFK automated review** (no human) → **Subagent** (keep main window clean; don't spend a squeeze you'll never touch).
- Mid-grill / mid-implement while you still need **primary** context *and* you're still in the smart zone (well under ~150k) → **Continue** (grill→implement at ~30k is the textbook Continue). Compacting or handing off there pays loss for nothing. At ≥~150k the tree's first question already fails — **Continue is off the table even mid-grill**; compact or handoff instead (the tree outranks this default).
- **Mid-phase auto-compact** forced by the harness — treat as dangerous (style drift, forgotten features); prefer explicit boundaries.

## How
1. Decide the next phase in **one sentence** (the focus). Example: "We're going to do QA in this area."
2. Run compact with that **one-sentence focus** — the summarizer is an LLM; a bare compact leaves it guessing; pasting a whole spec is wasted — one line is enough.
3. Verify the floor dropped and the focus survived.
4. Proceed with that phase only.

## If auto-compact already fired mid-phase
The harness squeezed without your one-line focus. Recover, don't re-explore:
1. Check context — see what survived and where the floor is now.
2. Re-anchor in one line: the phase goal plus the binding decisions you still hold.
3. `git status` / `git diff` — files are ground truth for uncommitted work.
4. Ask: did the focus survive? If yes, continue. If no, compact again with a one-line focus, or write a handoff doc and clear.
5. Set the next boundary explicitly (see handoff) so the following squeeze is yours, not the harness's.

## Related
handoff (ordered tree + "review" disambiguation) · grill-execute-clear
