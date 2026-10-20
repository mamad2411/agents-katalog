---
name: py-uv-0-11-tool-and-script-workflows
description: Guides agents through uv 0.11 Python tool execution, uvx usage, uv tool installs, and PEP 723 script dependency workflows. Use when the user mentions uvx, uv tool, standalone Python scripts, inline script dependencies, or uv run --script.
license: MIT
compatibility: Requires uv 0.11. Shell helper scripts assume bash on Unix-like systems or a compatible shell.
---

# py-uv-0-11 Tool and Script Workflows

This skill helps agents use uv `0.11` for one-off tools, persistently installed Python tools, and standalone Python scripts with inline metadata.

## When To Use This Skill

Use this skill for:

- Running Python CLI tools without adding them as project dependencies.
- Deciding between `uvx`, `uv tool run`, and `uv tool install`.
- Managing tools with a specific Python version.
- Creating, reviewing, or locking PEP 723 scripts.
- Keeping tool dependencies separate from project runtime dependencies.

## Workflow References

- `workflows/tool-execution-workflow.md`: Use when selecting or running Python tools through uv.
- `workflows/pep723-script-workflow.md`: Use when creating or maintaining standalone scripts with inline dependencies.

## Resource References

- `resources/uv-tool-script-checklist.md`: Checklist for deciding between project dependencies, tools, and script dependencies.

## Script References

Run scripts with `--help` before using them.

- `scripts/uv-tool-audit.sh`: Lists uv tools and checks that uv is on the 0.11 release line.

## Operating Guidance

1. Use `uvx <tool>` for one-off tool execution.
2. Use `uv tool install <tool>` only when the tool should be persistently available.
3. Keep project runtime dependencies in `pyproject.toml`; do not add CLI-only tools as runtime dependencies unless the project imports them.
4. For tools that require a specific Python version, pass `--python <version>`.
5. For PEP 723 scripts, lock dependencies explicitly with `uv lock --script <script.py>` when reproducibility matters.
6. Do not commit script lockfiles without reviewing whether the repository wants reproducible standalone scripts.
