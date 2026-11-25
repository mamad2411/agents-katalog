---
name: retro
description: Review memory/lessons.md, merge duplicates, and promote recurrent, verified lessons into .claude/rules (human-approved). Use at the end of a task, when lessons.md has grown, or when the user says "retro", "reflect", "promote lessons".
---

# retro

The promotion gate of the self-improvement loop (`.claude/rules/self-improvement.md`).

## Steps

1. Read `memory/lessons.md`; turn each `pending-review` stub into a proper NEVER/ALWAYS lesson or discard it.
2. Curate: merge duplicates (bump `seen:`), remove stale or contradicting entries, drop one-off trivia.
3. Select lessons that are recurrent (`seen ≥ 2`), generalizable and verifiable.
4. For each, draft the rule change (which `.claude/rules/*.md`, with `paths:`) and show the user a diff.
5. Apply only on approval; then remove the promoted lesson from lessons.md (it now lives in the rule).
6. Report merged / removed / promoted / kept.
