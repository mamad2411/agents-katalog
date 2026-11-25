---
name: operations-category-pointer
description: "Pointer to a library of 4 specialized Operations skills. Use when working on operations-related tasks."
risk: none
---

# Operations Capability Library 🎯

This is a **pointer skill**. The 4 specialized Operations skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **anti-sleep** — Keep a Mac awake with caffeinate during long builds, downloads, or supervised automation runs.
- **pi-custom-model** — Register custom Pi Agent model slugs so saved OpenRouter variants resolve correctly.
- **pre-release-review** — Run a read-only pre-release review for deploy readiness, migrations, config, secrets, rollout order, rollback risk, and launch blockers.
- **vps-server-management** — Manage authorized VPS hosts and server-side agents through cautious SSH and operations workflows.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/operations/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/operations`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
