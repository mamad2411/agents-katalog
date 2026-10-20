---
description: Session bootstrap — always read STATUS.md first and keep it current
alwaysApply: true
---

# Session bootstrap

At the start of implementation work, read `docs/STATUS.md` then the current wave in `docs/IMPLEMENTATION_PLAN.md`. `AGENTS.md` is the short map; `.cursorrules` is the constitution.

Update `docs/STATUS.md` when the wave state changes (`pending` → `in_progress` → `review` → `complete` / `blocked`).

Starting a wave: skill `wave-start`. Closing: skill `wave-close`. Architecture choice: skill `write-adr`.

Wave-close reviewers: `.cursor/agents/wave-reviewer.md` and `.cursor/agents/trust-auditor.md` (they must not implement).
