---
name: agent-tooling-category-pointer
description: "Pointer to a library of 3 specialized Agent Tooling skills. Use when working on agent-tooling-related tasks."
risk: none
---

# Agent Tooling Capability Library 🎯

This is a **pointer skill**. The 3 specialized Agent Tooling skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **aas-compose-stack** — Preserve the coding agent's explicit AAS skill selection as a validated stack and optional evidence.
- **aas-discover** — Discover AAS skills for an explicit task and compare their complete instructions without installing them.
- **aas-review-stack** — Review AAS stack manifests, preview plans and selection evidence in Workbench without applying changes.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `read` to load its `SKILL.md` from the vault:
   `/home/melfiano/.config/opencode/skill-libraries/agent-tooling/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `/home/melfiano/.config/opencode/skill-libraries/agent-tooling`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
