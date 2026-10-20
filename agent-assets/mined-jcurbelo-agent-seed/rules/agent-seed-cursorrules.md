# agent-seed

Self-evolving AI assistant. Markdown-only. Grows with you.

## Read Order
1. This file (entrypoint)
2. `context/index.md` (who the user is)
3. `memory/MEMORY.md` (what you've learned)

## Rules
- NEVER expose secrets (no .env, API keys, credentials)
- Branch + PR for changes (never push directly to main)
- Respect frontmatter in every .md file
- Respect size limits: index 150 lines, pages 250 lines, memory 200 lines

## Key Files
- Full rules: `CLAUDE.md`
- Agent definitions: `.claude/agents/`
- Skills: `.claude/skills/`
- Scoped rules: `.claude/rules/`
- User context: `context/`
- AI memory: `memory/`
- Daily todos: `todos/`

## Getting Started
If not personalized yet, read `.claude/skills/setup/SKILL.md` and follow the wizard.
