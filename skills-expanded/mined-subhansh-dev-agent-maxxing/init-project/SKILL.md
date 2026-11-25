---
name: init-project
description: Initialize a project's CLAUDE.md / AGENTS.md by analyzing the codebase architecture, commands, and conventions.
---

# Init Project — Create Agent Configuration

Extracted from Claude Code's bundled `init` skill.

Analyze the codebase and create a `CLAUDE.md` (or `AGENTS.md`) file for future agent sessions.

## What to Add

1. **Commands** — how to build, lint, run tests (including single test). Include the necessary commands to develop in this codebase.

2. **Architecture** — high-level code architecture and structure. Focus on the "big picture" that requires reading multiple files to understand.

## Rules

- Do not repeat yourself
- Do not include obvious instructions like "Provide helpful error messages" or "Write unit tests"
- Avoid listing every component or file structure that can be easily discovered
- Don't include generic development practices
- If there are Cursor rules, Copilot rules, or existing CLAUDE.md files, include the important parts
- If there is a README.md, include the important parts
- Do not make up "Common Development Tasks" or "Tips for Development" unless they exist in other files

## File Format

```markdown
# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Commands

- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint`
- Single test: `npm test -- --grep "test name"`

## Architecture

[High-level description of how the codebase is organized]

## Key Patterns

[Important conventions, patterns, or decisions that future agents need to know]
```
