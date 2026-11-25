---
name: food-chain-monitor
version: 2.1.0
description: >
  Re-stress-tests an idea that was previously battle-tested with food chain. Takes a Battle
  Log from a prior session plus a description of what changed, then runs a focused battle
  targeting only the NEW assumptions introduced by the change. Does not re-test what already
  survived. Works in Claude.ai, Claude Code, Cursor, Windsurf, Copilot with no dependencies.
when_to_use: >
  "food chain monitor", "re-battle this", "what changed since last battle",
  "stress test the pivot", "re-test after changes", "has my moat held up"
argument-hint: "[paste battle log + what changed]"
---

# Food Chain Monitor

## What This Is

A **delta battle** — the ongoing health-check companion to `food-chain-ideation`. Run it after pivots, after major feature additions, after market changes. It tests ONLY what changed since the last battle. Everything that already survived stays untouched.

## What This Is NOT

- **Not a full food chain battle.** That is `food-chain-ideation`. If you want to stress-test an idea from scratch, go there.
- **Not a replacement for the Battle Log.** This skill REQUIRES a prior Battle Log. If the user does not have one, redirect them: *"You need to run food-chain-ideation first to establish a baseline Battle Log. I can't monitor changes to something that hasn't been battle-tested yet."*

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| **Battle Log** | YES | From a prior `food-chain-ideation` session. Contains the original idea, evolved idea, apex predator, patches, and UAS. |
| **What Changed** | YES | A plain-language description: "we pivoted from X to Y", "we added feature Z", "competitor launched W", "market shifted because of Q". |
| **Action Log** | NO | From `apex-to-action`. If provided, the monitor checks whether executed actions are still valid post-change. |

If the user provides no Battle Log, do NOT proceed. Redirect to `food-chain-ideation`.

---

## Step 1 — Delta Analysis

Identify exactly what is new. Do not re-litigate settled assumptions.

```markdown
## Delta Analysis

| Field | Value |
|---|---|
| **Prior battle** | [date, original idea, evolved idea from battle log] |
| **What changed** | [user's description, quoted verbatim] |

### New Assumptions Introduced

| # | Assumption | Why New |
|---|---|---|
| 1 | [assumption] | [why this is new] |
| 2 | [assumption] | [why this is new] |
| ... | [max 5 — pick the 5 most vulnerable] | ... |

### Prior Patches

| Patch | Status |
|---|---|
| [patch from battle log] | STILL VALID / NEEDS RE-EVALUATION |
| ... | ... |

**Prior apex predator:** [animal from battle log] — still relevant? [YES / NO + one sentence why]
```

If the change introduces ZERO new assumptions (cosmetic change, minor UX tweak), skip the battle and issue:
```markdown
> **MONITOR VERDICT:** NO NEW ASSUMPTIONS — PRIOR BATTLE LOG STANDS. No delta battle needed.
```

---

## Step 2 — Focused Ecosystem (3 Animals Max)

Select predators that target ONLY the new assumptions from Step 1. Rules:

- **Maximum 3 animals.** This is a focused strike, not a full ecosystem.
- **Do NOT re-select animals that already attacked in the prior battle** unless the change specifically invalidates their prior elimination (e.g., a patch that neutralized them was removed by the pivot).
- Each animal must map to at least one new assumption. No generic threats.
- Use the same animal format as `food-chain-ideation`:
  ```
  [ANIMAL NAME] — [one-line threat to a specific new assumption]
  Attacks assumption: [number from Step 1]
  ```

If using subagent mode (Ollama available), route ecosystem selection through `gemma4:e2b` for pattern matching against the new assumptions. If Ollama is offline or returns `fallback_required: true`, select animals manually using internal reasoning.

---

## Step 3 — Delta Battle (2 Rounds Max)

Same format as `food-chain-ideation` rounds, but compressed:

**Round structure (per round):**
- Each surviving animal attacks one new assumption with a concrete scenario
- The idea defends — user or AI proposes a patch
- Score each animal 1-10 on threat severity post-defense
- Eliminate animals scoring below 4 after defense
- Absorb eliminated animal strengths into the idea

**Constraints:**
- 3 animals, 2 rounds maximum
- Same scoring, elimination, and absorption rules as `food-chain-ideation`
- Same subagent/fallback dual mode for attack generation
- If all animals are eliminated in Round 1, skip Round 2

After final round, identify the **delta apex predator** — the animal that scored highest against the new assumptions.

---

## Step 4 — Monitor Verdict

Synthesize the delta battle into a clear status update:

```markdown
## Monitor Verdict

| Field | Value |
|---|---|
| **Prior UAS still valid** | [YES / WEAKENED / INVALIDATED] |
| **Detail** | [If WEAKENED: which element dropped. If INVALIDATED: which assumption broke it] |
| **New threat identified** | [one sentence — delta apex predator's core attack, or "none"] |
| **Recommended action** | [CONTINUE / PATCH / RE-BATTLE] |
```

**Decision logic:**
- **CONTINUE** — All new assumptions survived. Prior UAS holds. No action needed.
- **PATCH** — One or more new assumptions are vulnerable but fixable. Provide the specific patch:
  > **RECOMMENDED PATCH:** [concrete change to the idea that neutralizes the new threat]
- **RE-BATTLE** — The change fundamentally undermines the prior battle results. The idea has shifted enough that a full `food-chain-ideation` session is needed with the updated idea.

---

## Step 5 — Updated Battle Log

APPEND to the prior Battle Log. Never overwrite it — the history matters.

```markdown
## Battle Log Update

Append to the prior Battle Log. Never overwrite.

> **Date:** [current date]
> **Type:** Monitor battle
> **Change tested:** [what changed — one line]
> **New assumptions tested:** [count]
> **Delta apex predator:** [animal name, or "prior apex holds" if no new apex emerged]
> **New patches applied:** [list, or "none needed"]
> **UAS status:** [VALID / WEAKENED / INVALIDATED]
> **Recommended action:** [CONTINUE / PATCH / RE-BATTLE]

---
[Full battle log history preserved above this line]
```

If the user has an Action Log from `apex-to-action`, also note:
> **Action Log impact:** [which actions from the prior log are affected by this change, if any]

---

## Speed Guidelines

This skill should complete in **under 5 minutes of interaction**. If you find yourself going deeper than 2 rounds or selecting more than 3 animals, you are overscoping. Stop and recommend a full `food-chain-ideation` re-battle instead.
