---
name: s4-safe-reader
description: Read-only mode for exploring code safely. Restricts Claude to read, search, and glob operations only.
allowed-tools: Read, Grep, Glob
---

# S4 — Safe Reader Mode

You are in **read-only mode**. You can explore the codebase but cannot make any changes.

## What You Can Do

- **Read** any file to examine its contents
- **Grep** to search for patterns across the codebase
- **Glob** to find files by name or path pattern

## What You Cannot Do

- Write or edit any files
- Run bash commands
- Create or delete files

## How to Explore

When the user asks you to explore or analyze the codebase:

1. Start with the project structure — glob for `**/*.py` to see all Python files
2. Read key files: `pyproject.toml`, any `README.md`, `CLAUDE.md`
3. Examine the module structure: `models/`, `api/`, `utils/`, `tests/`
4. Identify patterns: naming conventions, import style, error handling
5. Summarize your findings clearly

Focus on providing insights about architecture, patterns, and potential improvements
without actually making changes.
