---
name: symlink-files
description: Explains how configuration files like CLAUDE.md, .claude/skills, .github/copilot-instructions.md, and .github/skills are symlinked to AGENTS.md and .agents/skills/. Use when managing agent instructions, checking why edits to a mirror file are lost, or setting up new agents.
---
# Symlinked Agent Configuration

`.agents/skills/` and `AGENTS.md` are the single sources of truth for agent behavior in this repository. Every other agent entrypoint is a symlink to them.

## When to Use This Skill

- When wondering where to edit agent instructions.
- When you see a file like `CLAUDE.md` and want to edit it (do not edit the mirror!).
- When setting up new agent platforms that need their own instruction files.

## Architecture

| Symlink                           | Target           |
| --------------------------------- | ---------------- |
| `CLAUDE.md`                       | `AGENTS.md`      |
| `.claude/skills`                  | `.agents/skills` |
| `.github/copilot-instructions.md` | `AGENTS.md`      |
| `.github/skills`                  | `.agents/skills` |

**Never edit the mirror.** Always edit the source file (`AGENTS.md` or the contents of `.agents/skills/`).
