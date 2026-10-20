---
name: finance-category-pointer
description: "Pointer to a library of 2 specialized Finance skills. Use when working on finance-related tasks."
risk: none
---

# Finance Capability Library 🎯

This is a **pointer skill**. The 2 specialized Finance skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **longbridge** — 125+ agent skills for Longbridge Securities — real-time quotes, charts, fundamentals, portfolio analysis, options, and more for HK/US/A-share/SG markets. Trilingual: Simplified Chinese, Traditional Chinese, English.
- **options-flow-analyzer** — Real vs lottery call separation for options P/C ratio analysis — prevents signal inversion from deep OTM noise

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/finance/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/finance`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
