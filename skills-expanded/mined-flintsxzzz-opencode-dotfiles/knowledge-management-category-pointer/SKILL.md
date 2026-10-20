---
name: knowledge-management-category-pointer
description: "Pointer to a library of 2 specialized Knowledge Management skills. Use when working on knowledge-management-related tasks."
risk: none
---

# Knowledge Management Capability Library 🎯

This is a **pointer skill**. The 2 specialized Knowledge Management skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **maintain-codex-wiki** — Maintain a review-first engineering wiki with provenance, citation-aware queries, explicit capture and promotion, and deterministic checks.
- **wiki-builder** — Create and maintain reusable research wikis with source provenance, configurable structure, and local markdown outputs.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/knowledge-management/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/knowledge-management`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
