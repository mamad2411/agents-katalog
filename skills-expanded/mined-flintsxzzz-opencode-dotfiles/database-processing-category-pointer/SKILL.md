---
name: database-processing-category-pointer
description: "Pointer to a library of 6 specialized Database Processing skills. Use when working on database-processing-related tasks."
risk: none
---

# Database Processing Capability Library 🎯

This is a **pointer skill**. The 6 specialized Database Processing skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **base** — Database management, forms, reports, and data operations with LibreOffice Base.
- **database-admin** — Expert database administrator specializing in modern cloud databases, automation, and reliability engineering.
- **database-architect** — Expert database architect specializing in data layer design from scratch, technology selection, schema modeling, and scalable database architectures.
- **database-design** — Database design principles and decision-making. Schema design, indexing strategy, ORM selection, serverless databases.
- **database-optimizer** — Expert database optimizer specializing in modern performance tuning, query optimization, and scalable architectures.
- **using-neon** — Neon is a serverless Postgres platform that separates compute and storage to offer autoscaling, branching, instant restore, and scale-to-zero. It's fully compatible with Postgres and works with any language, framework, or ORM that supports Postgres.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/database-processing/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/database-processing`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
