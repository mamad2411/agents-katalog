---
name: web-category-pointer
description: "Pointer to a library of 1 specialized Web skills. Use when working on web-related tasks."
risk: none
---

# Web Capability Library 🎯

This is a **pointer skill**. The 1 specialized Web skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **url-to-markdown** — Fetch a public webpage as clean Markdown for an agent: read, summarize, quote, or cite the page while preserving its source URL.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `read` to load its `SKILL.md` from the vault:
   `/home/melfiano/.config/opencode/skill-libraries/web/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `/home/melfiano/.config/opencode/skill-libraries/web`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
