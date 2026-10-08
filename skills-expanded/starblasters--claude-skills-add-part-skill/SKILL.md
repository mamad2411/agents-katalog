---
name: add-part
description: Scaffold a new Starblaster Part (a slotted ship upgrade with Mk.1–9 scaling). Use when adding a new upgrade that mutates player stats. Implements the extend-Part / slot_type / apply+unapply / PartFactory pattern, checks balance, and verifies. Follows docs/contributing/04 and chains the part-author / economy-sim agents.
---

# /add-part — guided Part scaffold

Full reference: `docs/contributing/04-player-parts-economy.md`. Parts are how the
player gets ANY stats — the ship starts at zero and Parts populate it.

## Procedure

### 1. Gather intent
Confirm: which player stat(s) the Part affects, its `slot_type` (see
`scripts/weapons/SlotTypes.gd` for the slot enum), the Mk.1–9 scaling curve
(how the effect grows per mark), and roughly its cost tier. For balance
judgment (is the per-Mk delta worth the price?), consult the **economy-sim** /
**game-design** agents.

### 2. Implement via the part-author agent
The part-author agent owns this pattern:
- Extend `Part`.
- Set `slot_type` in `_init`.
- `apply(ship)` — **additive**: add to the ship's stat AND record the delta.
- `unapply(ship)` — reverse exactly that recorded delta (so swapping/removing
  the Part cleanly undoes it — this is why the delta is recorded, not recomputed).
- Mk scaling via the mark multiplier.
- **Register the Part in `PartFactory`** (else it can't be offered/equipped).

### 3. Verify + ship
Run the **/ship** skill: parse_check + headless boot (confirm the Part script
compiles and the ship can equip it) + commit `.uid`s + push + report to the user.

### 4. Balance pass (if it shifts the curve)
If the Part changes the power/cost curve meaningfully, run the **economy-sim**
agent to sanity-check run economics before considering it final. Mention the
relevant design docs (`docs/archive/economy_2026-05-24.md`,
`docs/archive/weapon_mk_progression_2026-05-25.md`) for context.

## Notes
- For a pure data `.tres` Part instance with no new code, the **data-author**
  agent is the lighter path; new behavior needs part-author (code).
- Cross-refs: `docs/contributing/04`, the "New Part" convention in `CLAUDE.md`.
