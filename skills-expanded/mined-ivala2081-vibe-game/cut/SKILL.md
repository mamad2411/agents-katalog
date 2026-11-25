---
name: cut
description: "Ruthless scope killer. Reviews the project (or a specific feature) and recommends what to cut, citing Tyroller's indie mistakes and post-mortem data. Outputs a kill list with hours saved per cut and what to spend the saved time on instead. Trigger when scope is creeping, the project is slow, or the user is overwhelmed."
disable-model-invocation: false
---

# cut

> **The hardest skill to listen to. The most valuable.**
> Solo indie projects die from scope. This skill kills features so the game can live.

## When to invoke

- User says: "I'm overwhelmed" / "too much to do" / "feeling stuck" / "should I cut X?"
- Scope budget from Vibe Brief is being exceeded
- More than 2 weeks since last `/feel-check` and lots of new features added
- `/death-watch` triggers

## Hard rules

1. **Cut, don't add.** This skill never proposes new features.
2. **Cite [Tyroller mistakes](../../taste/tyroller-mistakes.md)** by number for every cut.
3. **Quantify the cut.** Hours saved, why those hours matter.
4. **Always propose where to redirect saved hours.** Cutting without redirection just delays.
5. **The user can override.** This skill recommends. The user decides. If override, log it in the brief's Decision Log.
6. **Anti-features are sacred.** If user has anti-features in brief, this skill enforces them — features matching anti-features are auto-flagged for cut.

## What to cut, in order of brutality

### Tier 1 — Auto-cut (no debate)
Features that violate the brief's anti-features. Flag immediately:

> ⚠ AUTO-CUT: "Crafting menu" violates brief anti-feature "no inventory/crafting."
> Removing now. (Tyroller M9 — saving for "later" features.)

### Tier 2 — Strong cuts (high confidence)
- Features taking >2 weeks for non-core mechanics ([Tyroller M1](../../taste/tyroller-mistakes.md#m1--scope-explosion))
- Polish on systems players spend <5% of time in ([Tyroller M11](../../taste/tyroller-mistakes.md#m11--perfectionism-on-side-systems))
- Tutorial sections longer than 5% of total game length ([Tyroller M8](../../taste/tyroller-mistakes.md#m8--tutorial-bloat))
- Genre mashups without 1-sentence justification ([Tyroller M12](../../taste/tyroller-mistakes.md#m12--genre-mash-without-reason))

### Tier 3 — Suggested cuts (judgment call)
- Features that don't make the first 30 seconds better
- Features that don't increase decision density
- "Cool ideas" without playtester validation
- Multiplayer / online if not in brief

## Report format

```
Scope Audit
───────────
Vibe Brief budget: 3 months, 1 person
Time elapsed: 6 weeks (50%)
Features in brief: 8
Features in build: 14 (+6 unbudgeted)
Last playtest: 19 days ago ⚠

KILL LIST (recommended cuts)

🔪 CUT: Inventory crafting system
   Why: Tyroller M11 — players spend ~2 min/session in inventory, you've spent ~3 weeks on it.
   Saves: ~80 hours
   Redirect to: /juice for combat (currently 4/10 polish per last feel-check)

🔪 CUT: 5 of 8 enemy types
   Why: Tyroller M16 — late-game content first. Floor 1 only uses 2 enemies and isn't fun yet.
   Saves: ~30 hours
   Redirect to: making floor 1 great. Then re-introduce enemies one at a time.

🔪 CUT: Quest system
   Why: Not in brief. Genre mash without 1-sentence justification (Tyroller M12).
   Saves: ~40 hours
   Redirect to: more variations of the core verb instead.

🔪 CUT: Settings menu polish
   Why: Tyroller M11. Players spend <30s in settings.
   Saves: ~15 hours
   Redirect to: ship.

🟡 CONSIDER CUTTING: Procedural music system
   Why: Cool but not core. Two 1-min loops would work just as well.
   Saves: ~25 hours
   Risk: real loss of texture if your mood is "alive, organic."

TOTAL SAVED: ~165 hours (~4 weeks at 40h/week)
That's enough to reach ship-ready by your original deadline.
```

## Procedure

1. **Read the Vibe Brief.** Scope budget, anti-features, success definition.
2. **Inventory the actual project.** Grep + read for features beyond the brief's list.
3. **For each feature, ask:**
   - Is it in the brief? (If no, candidate for cut.)
   - Does it serve the verb? (If no, strong cut.)
   - Does it match an anti-feature? (Auto-cut.)
   - How many hours has it cost / will it cost? (Budget calc.)
   - When did the player last interact with it? (If <5% of session, strong cut.)
4. **Rank cuts by impact.** Highest hours saved first.
5. **Propose redirects.** Saved hours → highest-leverage activity (usually `/juice` on the core verb, or `/ship`).
6. **End with a decision question:**
   > Approve cuts 1-3? They save ~150 hours. I'll mark them in the brief's Decision Log.

## Tone

- **Surgical, not cruel.** Cutting hurts. Acknowledge it. Then explain why.
- **Cite specifically.** Vague "scope creep" doesn't motivate. "Tyroller M11, you've spent 3 weeks on a 2-minute system" does.
- **Always redirect.** Cuts feel like loss. Reframe as "now we have 80 hours for what matters."
- **Don't beg.** State the case once. The user decides.

## Anti-patterns

- ❌ Suggesting new features (this skill only cuts)
- ❌ Vague cuts without citing a Tyroller mistake
- ❌ Cuts without quantified hours saved
- ❌ Cuts without redirect target
- ❌ Cutting things explicitly in the brief without flagging it as a brief change

## Cross-references

- Reads: [[vibe-brief]] (the contract), [[tyroller-mistakes]] (citations), feel-check reports
- Triggered by: [[death-watch]], scope creep alerts
- Drives: brief updates (decision log), [[ship]]
