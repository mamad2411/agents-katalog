---
name: format-code
description: Formats Python and TypeScript files in the current project with ruff and prettier. Use after editing code.
allowed-tools: Bash(ruff format *) Bash(npx prettier --write *) Read
---

# Format code

Current changes: !`git status --short`

Run `scripts/format.sh` from the project root. It formats only files git knows about.

Never use `--dangerously-skip-permissions` to get past the prompts; approve the two commands instead.
