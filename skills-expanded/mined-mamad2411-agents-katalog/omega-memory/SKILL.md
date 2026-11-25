---
name: omega-memory
description: Persistent memory for AI coding agents. Semantic search, auto-capture, checkpoint/resume across sessions.
version: 1.0.0
requires_binaries: ["python3", "pip3"]
requires_env: []
---

# OMEGA Memory

Persistent memory for AI coding agents. Your agent remembers decisions, learns from mistakes, and picks up where it left off.

## Installation

```bash
pip3 install omega-memory[server]
omega setup
```

The `omega setup` command auto-configures your MCP client (Claude Code, Cursor, Windsurf, or Zed). No API keys needed — runs fully local with CPU-only embeddings.

## What It Does

OMEGA gives your agent a persistent memory layer across coding sessions:

- **Decisions & context** carry forward — no re-explaining
- **Lessons learned** from errors are recalled before you repeat them
- **Checkpoint/resume** lets you pause complex tasks and pick up later
- **Semantic search** over all stored memories with contextual re-ranking

## MCP Tools (12 tools)

| Tool | Purpose |
|------|---------|
| `omega_welcome` | Session briefing with recent memories and profile |
| `omega_protocol` | Retrieve operating rules and behavioral guidelines |
| `omega_store` | Store typed memory (decision, lesson, error, preference, summary) |
| `omega_query` | Semantic or phrase search with tag filters and re-ranking |
| `omega_lessons` | Cross-session lessons ranked by access count |
| `omega_profile` | Read or update the user profile |
| `omega_checkpoint` | Save task state for cross-session continuity |
| `omega_resume_task` | Resume a previously checkpointed task |
| `omega_memory` | Manage a specific memory (edit, delete, feedback, similar, traverse) |
| `omega_remind` | Set, list, or dismiss time-based reminders |
| `omega_maintain` | System housekeeping (health, consolidate, compact, backup, restore) |
| `omega_stats` | Analytics: type breakdown, session stats, weekly digest, access rates |

## Usage Pattern

At the start of every session:
1. Call `omega_welcome()` for context briefing
2. Call `omega_protocol()` for operating instructions
3. Follow the protocol it returns

During work:
- Before non-trivial tasks: `omega_query()` to check for prior context
- After completing tasks: `omega_store(content, "decision")` to save key outcomes
- When context is getting full: `omega_checkpoint()` to save state

## Links

- PyPI: https://pypi.org/project/omega-memory/
- GitHub: https://github.com/omega-memory/omega-memory
- Website: https://omegamax.co
