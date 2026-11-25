---
name: readme-writer
description: Write or refresh a README grounded in the actual code - real build commands, real flags, real structure. Use when the user asks to create, update, or audit a README or project documentation.
---

# README Writer

Every claim in the README must be verifiable in the repo. No boilerplate.

## Procedure

1. Survey the project: build files (Makefile, package.json, go.mod, etc.),
   entry points, CLI help output, config files, CI workflows, and tests.
   Run the real commands where cheap (e.g. `--help`) rather than guessing.
2. If a README exists, audit it first: list claims that are stale or
   wrong (commands that fail, flags that moved, paths that are gone).
3. Write for the stated audience. Default structure:
   - One-paragraph value proposition (what + why, no marketing fluff)
   - Install/build (commands you verified)
   - Quick start (shortest path to seeing it work)
   - Usage reference (only the surface users actually need)
   - Links to deeper docs rather than inlining everything
4. Keep it scannable: short sections, real code blocks, no walls of text.

## Rules

- Never document a command without confirming it exists.
- Prefer showing one working example over describing three abstractly.
- If something is unfinished, mark it honestly rather than omitting it.
