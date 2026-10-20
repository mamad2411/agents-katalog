# agent-seed

> Self-evolving AI assistant. Markdown-only. Grows with you.

## How This Repo Works

This is not a codebase — it's a context engine. Every file is a `.md` that teaches you (the AI) about the user: their voice, preferences, work context, and priorities.

**Read order:**
1. This file (entrypoint + rules)
2. `context/index.md` (who the user is)
3. `memory/MEMORY.md` (what you've learned)
4. Agents, skills, and rules load on demand

## Hard Rules

1. **NEVER expose secrets** — don't commit `.env`, API keys, credentials, or private keys.
2. **Branch + PR for changes** — never push directly to `main`. All changes go through PRs.
3. **Respect frontmatter** — every `.md` has YAML frontmatter defining its role. Follow it.
4. **Respect size limits** — index files: 150 lines. Detail pages: 250 lines. Memory files: 200 lines. Split when growing.

## Architecture

### Agents
Live in `.claude/agents/`. Each has YAML frontmatter defining model tier, tools, and permissions.
Registry and routing in `.claude/agents/index.md`.

### Skills
Live in `.claude/skills/` as `SKILL.md` files with description frontmatter.
Core skills: `/setup`, `/standup`, `/eod`, `/review`, `/learn`, `/update-todos`.

### Rules
Live in `.claude/rules/`. Scoped by file path via `paths` frontmatter.
Load automatically when editing files matching the path pattern.

### Context
Lives in `context/`. The user's identity, voice, and work context.
Follows index-to-pages pattern: `index.md` links to detail pages.
Populated by `/setup`, updated by `/learn`.

### Memory
Lives in `memory/`. What the AI has learned across sessions.
`MEMORY.md` is always loaded. Sub-files load on demand.
Updated by the reflection agent after meaningful sessions.

### Todos
Live in `todos/YYYY-MM-DD/`. Daily task tracking.
Each day is a folder: `todos.md`, `drafts/`, `notes/`.

## Model Tiering

Use the cheapest model that can do the job:
- **haiku** — simple lookups, reads, searches
- **sonnet** — analysis, coding, drafting
- **opus** — orchestration, complex reasoning, code review

## Self-Evolution

The system improves itself over time:
1. **Reflection agent** — captures learnings after sessions
2. **`/learn` skill** — periodic self-improvement, creates new agents via PR
3. **`/setup`** — re-run anytime to add integrations

## The Index Pattern

Every folder has an `index.md` that links to detail pages:
```
context/index.md → voice/index.md → patterns.md
                 → work/index.md  → tools.md
```
Index files are loaded first. Detail pages on demand. This keeps context small and navigable.

## Git Workflow

Branch prefixes: `feat/`, `fix/`, `docs/`, `chore/`.
PRs need `## Summary` + `## Test plan`.
Target `main`.

## Getting Started

If this repo hasn't been personalized yet, run `/setup` to begin.
