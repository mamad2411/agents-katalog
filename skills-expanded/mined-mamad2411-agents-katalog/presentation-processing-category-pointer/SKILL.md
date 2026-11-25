---
name: presentation-processing-category-pointer
description: "Pointer to a library of 5 specialized Presentation Processing skills. Use when working on presentation-processing-related tasks."
risk: none
---

# Presentation Processing Capability Library 🎯

This is a **pointer skill**. The 5 specialized Presentation Processing skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **frontend-slides** — Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files.
- **google-slides-automation** — Read and edit Google Slides through an available authenticated connector or reviewed API integration, with scoped changes and read-back verification.
- **impress** — Presentation creation, format conversion (ODP/PPTX/PDF), slide automation with LibreOffice Impress.
- **nanobanana-ppt-skills** — AI-powered PPT generation with document analysis and styled images
- **pptx-official** — A user may ask you to create, edit, or analyze the contents of a .pptx file. A .pptx file is essentially a ZIP archive containing XML files and other resources that you can read or edit. You have different tools and workflows available for different tasks.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/presentation-processing/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/presentation-processing`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
