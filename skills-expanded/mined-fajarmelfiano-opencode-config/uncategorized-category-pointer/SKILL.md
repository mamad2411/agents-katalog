---
name: uncategorized-category-pointer
description: "Pointer to a library of 2 specialized Uncategorized skills. Use when working on uncategorized-related tasks."
risk: none
---

# Uncategorized Capability Library 🎯

This is a **pointer skill**. The 2 specialized Uncategorized skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **changelog-entry** — Generate a properly formatted CHANGELOG.md entry in Keep a Changelog format from a commit range or PR. Groups changes into Added/Changed/Deprecated/Removed/Fixed/Security categories and outputs a ready-to-paste block.
- **reverse-engineer-anything** — Use REA to investigate shipped apps, binaries, packages, and runtimes; trace features with evidence, compare versions, or guide reconstruction. Skip ordinary source-code analysis.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `read` to load its `SKILL.md` from the vault:
   `/home/melfiano/.config/opencode/skill-libraries/uncategorized/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `/home/melfiano/.config/opencode/skill-libraries/uncategorized`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
