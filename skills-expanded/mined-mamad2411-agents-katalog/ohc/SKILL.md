---
name: ohc-skill
description: Manage skills: /ohc-skill list | promote <name> | draft <name>
---

# /ohc-skill — Manage Skills

Usage:
  /ohc-skill list              — list installed skills + .ohc/skills/ drafts
  /ohc-skill promote <name>    — promote draft to skills/ folder
  /ohc-skill draft <name>      — scaffold new skill with template

list output:
  Installed (skills/):
    ✓ ohc-coding-discipline
    ✓ explore-codebase
    ...
  Drafts (.ohc/skills/):
    📝 auth-service-quirks → ohc skill promote auth-service-quirks

promote: moves .ohc/skills/{name}.md → skills/{name}/SKILL.md
         creates references/ scripts/ assets/ subdirs
         warns if content >200 lines
