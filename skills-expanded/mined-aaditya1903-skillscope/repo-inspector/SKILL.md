---
name: repo-inspector
description: Survey an unfamiliar repository and report its structure, entry points, tests and conventions without modifying any file. Use when you need to understand a codebase before touching it.
license: MIT
compatibility: Read-only; makes no commits and writes no files.
allowed-tools: Read Grep Glob
metadata:
  category: software-engineering
---

# Repository inspection

Understand the codebase before changing it, and leave it exactly as you found
it.

## Read-only contract

This skill only reads. It does not format, does not install dependencies and
does not create files. Anything that would change the working tree belongs in a
different skill.

## What to report

1. Entry points and how the project is run.
2. Where the tests live and how they are invoked.
3. The dependency and build tooling actually in use.
4. Conventions the existing code follows, with an example of each.
5. The parts that are unclear, stated as questions rather than guesses.
