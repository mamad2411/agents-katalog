---
name: mcp-category-pointer
description: "Pointer to a library of 7 specialized Mcp skills. Use when working on mcp-related tasks."
risk: none
---

# Mcp Capability Library 🎯

This is a **pointer skill**. The 7 specialized Mcp skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **ai-dev-jobs-mcp** — Search 8,400+ AI and ML jobs across 489 companies, inspect listings and employers, match roles, and view salary and market stats via AI Dev Jobs MCP
- **cowork-to-code-bridge** — Use an already-installed, independently verified cowork-to-code bridge to run narrowly approved actions on the user's own macOS, Linux, or WSL2 machine through a local file queue.
- **mercury-mcp** — Cheatsheet for the Mercury (proton) MCP tools. Use when connected to the Mercury MCP server to look up which mercury_* tool to call for messaging teammates, threads, tasks, automations, or admin team-graph edits.
- **not-human-search-mcp** — Search AI-ready websites, inspect indexed site details, verify MCP endpoints, and discover tools and APIs using the Not Human Search MCP server
- **parallel-search-mcp** — Search the public web and verify sources with Parallel's free Search MCP. Use when the user chooses Parallel or its connected tools for current information and URL extraction.
- **protect-mcp-governance** — Agent governance skill for MCP tool calls — Cedar policy authoring, shadow-to-enforce rollout, and Ed25519 receipt verification.
- **serply-search-mcp** — Search Google, Bing, Google News and Google Scholar, and read public pages, with the Serply MCP server. Use when the user chooses Serply or its connected tools for current information and source verification.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `read` to load its `SKILL.md` from the vault:
   `/home/melfiano/.config/opencode/skill-libraries/mcp/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `/home/melfiano/.config/opencode/skill-libraries/mcp`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
