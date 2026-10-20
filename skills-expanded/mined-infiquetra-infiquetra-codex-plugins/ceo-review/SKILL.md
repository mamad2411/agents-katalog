---
name: ceo-review
description: Alias-style skill for founder-review. Use when the user asks for CEO review, founder review, scope ambition review, scope expansion/reduction, or whether a plan, strategy, feature, or PR is ambitious enough.
---

# CEO Review

Use the same engine as `founder-review`.

Load `plugins/saga/skills/founder-review/SKILL.md` and run the CEO/founder-mode
scope and ambition review: detect the target type, audit the surrounding
system, challenge the premise, select a committed scope mode, run the opt-in
ceremony, write a `docs/founder-reviews/` scope-decision artifact, and route in
a closed loop.

This is a review skill, not an implementer. It does not make code changes,
commit, push, open PRs, file issues, deploy, or stage files. Keep it separate
from `strategy`, which records the chosen direction.
