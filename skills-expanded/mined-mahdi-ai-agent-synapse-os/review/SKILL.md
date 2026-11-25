---
name: review
description: Runs the full review: keeps the vault current — archives the obsolete, sets priorities, updates goals and next actions, adds links, fixes categories — and writes memory/focus.md. Use for "بازبینی کامل", "همه‌چی رو بررسی و به‌روز کن", "اولویت‌هام رو به‌روز کن", "full review", "tidy my brain", or the Full review button.
---

# review

Unlike `/weekly`, which proposes, this skill applies its changes. Each one is reversible — a status, a field, a link, a dated line — and the run is one commit the user can undo. Nothing is deleted.

## Steps

1. Read `index/INDEX.md`, `memory/focus.md` (the last review: its date and what it asked) and the `index/by-type/` files for task, project, goal, habit, idea, note and resource. Finished work older than 30 days is already out of them (`index/archive.md`): leave it. Open a node only when its line cannot decide (at most 25 nodes).
2. Apply [references/rules.md](references/rules.md) in its order: archive · priorities · goals and projects · links · places. Every node you change gets one dated line at the end of its body in the user's language, saying what the review changed and why (`- YYYY-MM-DD: بازبینی کامل: …`).
3. Replace `memory/focus.md` with the format in [references/focus.md](references/focus.md).
4. Reply in the user's language: one sentence with the counts (archived, priorities, progress, links, moved, new tasks), then the **Now** list. Ask only what the focus file lists under **Asked of you**.
