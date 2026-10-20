# agent-seed

> Self-evolving AI assistant. Markdown-only. Grows with you.

This file is the entrypoint for Devin, Codex, and other LLM agents.
For full details, see `CLAUDE.md` — the content is identical.

## How This Repo Works

This is not a codebase — it's a context engine. Every file is a `.md` that teaches you (the AI) about the user: their voice, preferences, work context, and priorities.

**Read order:**
1. This file (entrypoint + rules)
2. `context/index.md` (who the user is)
3. `memory/MEMORY.md` (what you've learned)
4. Agent definitions in `.claude/agents/` (check `index.md` for routing)

## Rules

1. **NEVER expose secrets** — don't commit `.env`, API keys, credentials, or private keys.
2. **Branch + PR for changes** — never push directly to `main`.
3. **Respect frontmatter** — every `.md` has YAML frontmatter defining its role.
4. **Respect size limits** — index: 150 lines, pages: 250 lines, memory: 200 lines.

## Key Files

| What | Where |
|------|-------|
| Architecture + rules | `CLAUDE.md` |
| Agent definitions | `.claude/agents/` |
| Skills (slash commands) | `.claude/skills/` |
| Scoped rules | `.claude/rules/` |
| User context | `context/` |
| AI memory | `memory/` |
| Daily todos | `todos/` |

## Getting Started

If this repo hasn't been personalized yet, read `.claude/skills/setup/SKILL.md` and follow the wizard.
