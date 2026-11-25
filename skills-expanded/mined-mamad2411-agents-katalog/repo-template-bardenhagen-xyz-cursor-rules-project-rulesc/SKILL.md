---
description: Core project rules and conventions for this repository. Applied by Cursor AI on every interaction.
globs: "*"
---
# Project Rules

## Always Read Project Context
- Read `AGENTS.md`, `AI_CONTEXT.md`, `.cursorrules`, and this file at the start of every session
- Follow the Agentic SDLC protocol documented in `docs/agentic-sdlc.md`

## Workflow
- Run `git pull --ff-only` before making any changes
- Commit after each logical phase of work
- Push changes promptly
- Update `CHANGELOG.md` with significant changes

## Code Quality
- Write tests alongside implementation code
- Run linter before committing
- Use conventional commit format: `type(scope): description`
- Document public APIs

## Architecture Decisions
- Create ADRs in `docs/decisions/` for significant architectural choices
- Keep ADRs short and focused

## Security
- Never commit secrets, passwords, tokens, or API keys
- Use `.env.example` to document required environment variables
- Ensure `.env` is in `.gitignore`
