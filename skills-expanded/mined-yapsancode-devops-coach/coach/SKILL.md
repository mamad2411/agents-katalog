---
name: coach
description: Daily DevOps coach. Runs a morning class (today's tasks) and an evening check (proof, quiz, log) against devops-upskill-roadmap.md. Use when the user types /coach, says "start class", "coach me", "I'm done for today", or asks what to study today.
---

# DevOps daily coach (pointer)

The full coach instructions live in `.claude/skills/coach/SKILL.md` at the
repo root — that file is the single source of truth for all tools.

Read that file now and follow it exactly. Pass the user's arguments through
(`done` / `check` / `evening` → evening check; otherwise morning class).
