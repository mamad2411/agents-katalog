---
name: agent-squad-category-pointer
description: "Pointer to a library of 8 specialized Agent Squad skills. Use when working on agent-squad-related tasks."
risk: none
---

# Agent Squad Capability Library 🎯

This is a **pointer skill**. The 8 specialized Agent Squad skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **alex** — Turns requirements into a precise, dependency-aware implementation plan.
- **aria** — Designs the data model, API contracts, and structural foundation of the system.
- **dep** — Handles containerization, CI/CD pipelines, and deployment setup.
- **luna** — Reviews code for objective correctness, security, and reliability.
- **mason** — Produces clean, functional code that matches the architecture and checklists.
- **max** — Cleans up and improves existing code without changing behavior.
- **quinn** — Proves the system works by writing and executing comprehensive test suites.
- **rex** — Translates user intent into a precise, unambiguous specification and requirements.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/agent-squad/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/agent-squad`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
