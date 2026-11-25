---
name: skill-authoring-category-pointer
description: "Pointer to a library of 2 specialized Skill Authoring skills. Use when working on skill-authoring-related tasks."
risk: none
---

# Skill Authoring Capability Library 🎯

This is a **pointer skill**. The 2 specialized Skill Authoring skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **writing-great-skills** — Reference for writing and editing skills well — the vocabulary and principles that make a skill predictable.
- **yao-meta-skill** — Create, refactor, evaluate, and package agent skills from workflows, prompts, transcripts, docs, or notes. Use for skill creation, reusable workflow packaging, skill improvement, evals, and team-ready distribution.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/skill-authoring/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/skill-authoring`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
