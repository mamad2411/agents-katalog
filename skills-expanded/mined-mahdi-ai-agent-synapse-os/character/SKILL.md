---
name: character
description: Builds or refreshes the character map — who the owner is as the vault shows them: traits, values, concerns, voice, each with evidence. Use for "نقشه‌ی کاراکترم رو بساز", "کاراکترم رو به‌روز کن", "منو بشناس", "build my character map", "refresh my character", or Build / Refresh on it.
---

# character

Writes the one map with `role: character` and what is in it; nothing else. Evidence only: every item cites nodes, counts or the owner's own lines.

## Steps

1. Read `index/INDEX.md` (its **Maps** section says whether the character map exists and which categories it has), every `index/by-area/` file of the mind map's categories (short files), `index/by-type/goal.md`, `habit.md`, `event.md`, the last 14 lines of `index/by-type/journal.md` (open at most 5 journal nodes for the voice), `memory/profile.md` and `memory/insights.md` when they exist, and — on a refresh — the character map's own sub-indexes.
2. First build: create `nodes/maps/<slug>.md` per `.claude/rules/maps.md` — title «کاراکتر من» / "My character", `role: character`, `connects: [mind]`, a summary line on who they are — and four categories with `map: "[[کاراکتر من]]"`: «ویژگی‌ها» / Traits, «ارزش‌ها» / Values, «دغدغه‌ها» / Concerns, «لحن» / Voice. A fifth only when the vault clearly shows another side («مهارت‌ها» / Skills).
3. Items per [references/format.md](references/format.md): 3–6 `note`s per category, each with `area:` one of those categories. Never invent, never diagnose, never moralize; a concern is a worry they wrote about, not your judgement of them.
4. Refresh: update existing items in place (summary, evidence, one dated line `- YYYY-MM-DD: …` when something changed), add what is new, set `status: archived` on what the vault no longer supports. At most 24 items in all.
5. Reply in the user's language with 3–5 lines — what the map says now and what changed since the last build (or that this is the first) — then one line per node created or updated. Nothing before that reply: no progress notes between tool calls, however many files the build touches.
