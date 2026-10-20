---
name: py-uv-0-11-project-workflows
description: Guides agents through uv 0.11 Python project setup, dependency changes, lockfile checks, sync repair, project health checks, and safe command selection. Use when the user mentions uv, pyproject.toml, uv.lock, uv sync, uv add, uv remove, uv run, uv tree, or Python project dependency management.
license: MIT
compatibility: Requires uv 0.11 and a Python project using pyproject.toml. Shell helper scripts assume bash on Unix-like systems or a compatible shell.
---

# py-uv-0-11 Project Workflows

This skill helps agents make safe, reviewable changes to Python projects that use uv `0.11`.

## When To Use This Skill

Use this skill for:

- Creating or normalizing uv-managed Python projects.
- Adding, removing, or upgrading dependencies.
- Repairing stale lockfiles or out-of-sync `.venv` environments.
- Reviewing `pyproject.toml`, `uv.lock`, and `.python-version`.
- Running health checks before or after uv-related edits.
- Choosing the safest uv command for a task.

## Workflow References

- `workflows/init-project-workflow.md`: Use when creating a new uv project or adding uv project structure to an existing Python repository.
- `workflows/dependency-upgrade-workflow.md`: Use when updating one or more dependencies, especially when lockfile diffs need review.
- `workflows/lock-sync-repair-workflow.md`: Use when `uv run`, `uv sync`, or dependency resolution fails because the environment or lockfile is stale.

## Resource References

- `resources/uv-project-checklist.md`: Checklist for project metadata, lockfile, Python version, dependency groups, and verification commands.
- `resources/uv-command-decision-tree.md`: Decision tree for selecting `uv add`, `uv remove`, `uv lock`, `uv sync`, `uv run`, `uv tree`, and `uv export`.

## Script References

Run scripts with `--help` before using them.

- `scripts/uv-project-health.sh`: Performs safe read-only checks for uv, `pyproject.toml`, `.python-version`, `uv.lock`, lock freshness, and dependency tree availability.
- `scripts/uv-safe-sync.sh`: Runs a safer sync with optional `UV_MALWARE_CHECK=1`, `uv lock --check`, and `uv sync --locked`.
- `scripts/uv-command-guard.sh`: Hook helper that prompts before risky uv-related shell commands.

## Operating Guidance

1. Confirm the repository is actually a uv project before making changes.
2. Confirm `uv --version` begins with `uv 0.11.` when version-specific behavior matters.
3. Prefer `uv run <command>` for repeatable commands instead of assuming an activated `.venv`.
4. Prefer `uv add` and `uv remove` over hand-editing dependency arrays.
5. Use `uv lock --check` before making changes to understand the starting state.
6. Use `uv tree` after dependency changes when transitive dependency changes matter.
7. Use `uv sync --locked` for verification after lockfile updates.
8. Keep broad upgrades isolated and explain direct and transitive changes.
9. Never expose private index credentials in generated files or command output.
