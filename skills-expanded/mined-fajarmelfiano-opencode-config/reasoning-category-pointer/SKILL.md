---
name: reasoning-category-pointer
description: "Pointer to a library of 2 specialized Reasoning skills. Use when working on reasoning-related tasks."
risk: none
---

# Reasoning Capability Library 🎯

This is a **pointer skill**. The 2 specialized Reasoning skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **axiom** — First-principles assumption auditor. Classifies each hidden assumption (fact / convention / belief / interest-driven), ranks by fragility × impact, and rebuilds conclusions from verified premises. Bilingual: auto-detects Chinese or English.
- **falsify** — The scientific thinking protocol for AI agents. Use when facing complex, ambiguous, or high-stakes questions where guessing is costly: hypothesis → attempt to break it → evidence → calibrated conclusion.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `read` to load its `SKILL.md` from the vault:
   `/home/melfiano/.config/opencode/skill-libraries/reasoning/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `/home/melfiano/.config/opencode/skill-libraries/reasoning`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
