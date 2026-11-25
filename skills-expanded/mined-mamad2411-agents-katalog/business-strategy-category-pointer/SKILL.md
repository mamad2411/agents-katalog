---
name: business-strategy-category-pointer
description: "Pointer to a library of 3 specialized Business Strategy skills. Use when working on business-strategy-related tasks."
risk: none
---

# Business Strategy Capability Library 🎯

This is a **pointer skill**. The 3 specialized Business Strategy skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **find-complementary-founders** — Use when an owner explicitly asks for a cofounder or project partner, or explicitly says they need a complementary builder, operator, go-to-market partner, or scaling capability. Assess and publish only the agent's own owner, then rank only approved own-owner profiles.
- **kotler-macro-analyzer** — Professional PESTEL/SWOT analysis agent based on Kotler's methodology for strategic market audits.
- **osterwalder-canvas-architect** — Iterative consultant agent for building and validating logically consistent 9-block Business Model Canvases.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/business-strategy/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/business-strategy`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
