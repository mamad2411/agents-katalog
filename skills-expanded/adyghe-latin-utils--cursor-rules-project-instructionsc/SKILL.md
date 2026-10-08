---
description: Project-wide agent operating and execution constraints
alwaysApply: true
---

# Project Instructions (Cursor Source of Truth)

This rule is the active source of truth for Cursor agent behavior in this repository.

## Role and process
- Address the user as Haroon.
- Ask for permission before creating new files or implementing new functionality not explicitly requested.
- Work incrementally and complete one task before starting the next.
- Do not run `git add`, `git commit`, `git push`, or destructive git commands unless explicitly requested.
- Explain reasoning briefly before complex changes.

## Shell and path constraints
- Use absolute paths for file and directory references in commands/scripts.
- Prefer `/bin/tcsh` semantics for shell scripts and command examples.
- For tcsh snippets, use tcsh syntax (`setenv`, `set var = value`, `if ( ) then`).

## Python execution standards
- Use `.venv/bin/python3` for script execution and Python shebangs where applicable.
- Avoid multi-line Python passed inline through shell commands when tcsh is involved; write to a temporary `.py` file and execute it.
- Keep type hints strict and explicit in Python code.

## Documentation and tracking
- Track task status in `TODO.md` when task items are present.
- Prefer placing documentation under `doc/` unless instructed otherwise.
