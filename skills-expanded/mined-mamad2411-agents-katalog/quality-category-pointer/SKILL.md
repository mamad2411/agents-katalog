---
name: quality-category-pointer
description: "Pointer to a library of 2 specialized Quality skills. Use when working on quality-related tasks."
risk: none
---

# Quality Capability Library 🎯

This is a **pointer skill**. The 2 specialized Quality skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **dos-verify-done-claims** — Before accepting an agent's 'done / shipped / fixed' claim, verify it against ground truth (git ancestry + the commit's own diff) using the DOS kernel's `dos verify` and `dos commit-audit` — never the agent's own narration.
- **pre-ship-gate** — A ship gate that runs before any production deploy: checks the silent failure modes that make a deploy 'succeed' while prod stays broken, then verifies the live revision instead of trusting deploy output.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/quality/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/quality`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
