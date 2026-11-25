---
name: memory-category-pointer
description: "Pointer to a library of 6 specialized Memory skills. Use when working on memory-related tasks."
risk: none
---

# Memory Capability Library 🎯

This is a **pointer skill**. The 6 specialized Memory skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **agent-memory-systems** — Memory is the cornerstone of intelligent agents. Without it, every interaction starts from zero. This skill covers the architecture of agent memory: short-term (context window), long-term (vector stores), and the cognitive architectures that organize them.
- **context-window-management** — Strategies for managing LLM context windows including summarization, trimming, routing, and avoiding context rot
- **conversation-memory** — Persistent memory systems for LLM conversations including short-term, long-term, and entity-based memory
- **hierarchical-agent-memory** — Scoped CLAUDE.md memory system that reduces context token spend. Creates directory-level context files, tracks savings via dashboard, and routes agents to the right sub-context.
- **memory-systems** — Design short-term, long-term, and graph-based memory architectures. Use when building agents that must persist across sessions, needing to maintain entity consistency across conversations, or implementing reasoning over accumulated knowledge.
- **recallmax** — FREE — God-tier long-context memory for AI agents. Injects 500K-1M clean tokens, auto-summarizes with tone/intent preservation, compresses 14-turn history into 800 tokens.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/memory/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/memory`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
