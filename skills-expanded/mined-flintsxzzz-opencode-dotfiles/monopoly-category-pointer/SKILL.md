---
name: monopoly-category-pointer
description: "Pointer to a library of 4 specialized Monopoly skills. Use when working on monopoly-related tasks."
risk: none
---

# Monopoly Capability Library 🎯

This is a **pointer skill**. The 4 specialized Monopoly skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **patterns** — Reference document for monopoly patterns.
- **scale-benchmarks** — Reference document for monopoly scale-benchmarks.
- **security-checklist** — Reference document for monopoly security-checklist.
- **tech-matrix** — Reference document for monopoly tech-matrix.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/monopoly/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/monopoly`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
