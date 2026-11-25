---
name: personal-development-category-pointer
description: "Pointer to a library of 2 specialized Personal Development skills. Use when working on personal-development-related tasks."
risk: none
---

# Personal Development Capability Library 🎯

This is a **pointer skill**. The 2 specialized Personal Development skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **quit-sponsor** — Helps an AI agent provide non-judgmental, evidence-informed quit-smoking support with user-consented tracking, craving check-ins, and escalation to human or clinical help. Not medical care.
- **satori** — Clinically informed wisdom companion blending psychology and philosophy into a structured thinking partner

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/personal-development/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/personal-development`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
