---
name: repository-development-skills
description: Entry point for agents developing this repository. Use it before planning or implementing changes; it points to the canonical development skills in .claude/skills/.
metadata:
  audience: repository-agent
---

# Repository development skills

The canonical development skills for this repository live in `.claude/skills/`. This location
holds only this pointer, so it never needs refreshing.

1. Read root `AGENTS.md` first. It governs every repository agent.
2. List `.claude/skills/*/SKILL.md`. Each directory is one skill, and its front-matter `description`
   says when it applies.
3. Read and follow the skill or skills relevant to your task, directly from `.claude/skills/`. Do
   not copy them here or anywhere else.

Never load anything from `pipeline/skills/`. Those are runtime skills that jobs send to review
workers, not development procedures.
