---
name: agent-evaluation-category-pointer
description: "Pointer to a library of 2 specialized Agent Evaluation skills. Use when working on agent-evaluation-related tasks."
risk: none
---

# Agent Evaluation Capability Library 🎯

This is a **pointer skill**. The 2 specialized Agent Evaluation skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **agent-evaluation-reporting** — Use when summarizing agent evaluations where autonomous, assisted, failed, timed-out, or invalid outcomes must remain distinct and comparable.
- **run-deep-swe** — Run reproducible DeepSWE coding-agent benchmark evaluations through OpenRouter and mini-swe-agent.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/agent-evaluation/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/agent-evaluation`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
