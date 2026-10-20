---
name: document-processing-category-pointer
description: "Pointer to a library of 4 specialized Document Processing skills. Use when working on document-processing-related tasks."
risk: none
---

# Document Processing Capability Library 🎯

This is a **pointer skill**. The 4 specialized Document Processing skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **doc-coauthoring** — This skill provides a structured workflow for guiding users through collaborative document creation. Act as an active guide, walking users through three stages: Context Gathering, Refinement & Structure, and Reader Testing.
- **docx-official** — A user may ask you to create, edit, or analyze the contents of a .docx file. A .docx file is essentially a ZIP archive containing XML files and other resources that you can read or edit. You have different tools and workflows available for different tasks.
- **pdf-official** — This guide covers essential PDF processing operations using Python libraries and command-line tools. For advanced features, JavaScript libraries, and detailed examples, see reference.md. If you need to fill out a PDF form, read forms.md and follow its instructions.
- **writer** — Document creation, format conversion (ODT/DOCX/PDF), mail merge, and automation with LibreOffice Writer.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/document-processing/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/document-processing`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
