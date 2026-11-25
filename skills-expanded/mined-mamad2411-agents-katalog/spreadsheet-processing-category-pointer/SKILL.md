---
name: spreadsheet-processing-category-pointer
description: "Pointer to a library of 4 specialized Spreadsheet Processing skills. Use when working on spreadsheet-processing-related tasks."
risk: none
---

# Spreadsheet Processing Capability Library 🎯

This is a **pointer skill**. The 4 specialized Spreadsheet Processing skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **calc** — Spreadsheet creation, format conversion (ODS/XLSX/CSV), formulas, data automation with LibreOffice Calc.
- **google-sheets-automation** — Read and edit Google Sheets through an available authenticated connector or reviewed API integration, with scoped changes and read-back verification.
- **googlesheets-automation** — Automate Google Sheets operations (read, write, format, filter, manage spreadsheets) via Rube MCP (Composio). Read/write data, manage tabs, apply formatting, and search rows programmatically.
- **xlsx-official** — Unless otherwise stated by the user or existing template

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/spreadsheet-processing/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/spreadsheet-processing`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
