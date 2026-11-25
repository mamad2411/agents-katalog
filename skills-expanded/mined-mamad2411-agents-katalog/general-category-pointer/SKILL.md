---
name: general-category-pointer
description: "Pointer to a library of 1 specialized General skills. Use when working on general-related tasks."
risk: none
---

# General Capability Library 🎯

This is a **pointer skill**. The 1 specialized General skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **antigravity-agent-manager** — Configure and orchestrate parallel agents using the standalone Antigravity 2.0 Agent Manager and Antigravity IDE.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/general/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/general`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
