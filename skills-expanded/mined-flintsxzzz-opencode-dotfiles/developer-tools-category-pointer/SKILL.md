---
name: developer-tools-category-pointer
description: "Pointer to a library of 6 specialized Developer Tools skills. Use when working on developer-tools-related tasks."
risk: none
---

# Developer Tools Capability Library 🎯

This is a **pointer skill**. The 6 specialized Developer Tools skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **agents-generator** — Generate project-specific AGENTS.md and companion rules by analyzing a codebase. Supports full, minimal, update, and dry-run modes with package-manager detection, monorepos, backups, managed blocks, confidence scoring, and command validation.
- **gh-attach** — Upload and download GitHub user-attachments (screenshots, PDFs, zips, videos) from the terminal; use when asked to attach or embed a file in a PR, issue, or comment, or download an attachment URL.
- **gh-image** — Upload local images to GitHub and get canonical user-attachments embed URLs; use when asked to attach a screenshot to a PR, issue, or comment, or to embed before/after images in a README.
- **mcp-tool-developer** — Build Model Context Protocol (MCP) servers and tools from scratch. Full-stack MCP development with TypeScript/Python, testing, deployment, and registry publishing.
- **skill-porter** — Preview conservative tool-name translations and copy complete local skill bundles for manual adaptation to Google Antigravity.
- **tokenwise** — Measurement-driven model router for Claude Code. Routes Haiku/Sonnet/Opus per task class, logs every routed task with real $ numbers, and A/B tests cheaper tiers before you trust the savings.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/developer-tools/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/developer-tools`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
