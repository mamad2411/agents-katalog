---
name: pipfile
description: >-
  Create, update, and manage Python project dependencies via Pipfile and Pipfile.lock.
  This skill MUST be loaded when creating or updating Pipfile or Pipfile.lock content.
license: MIT
---
# pipfile

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

Use this skill for managing the structure and content of `Pipfile` and `Pipfile.lock` files.

## WHEN TO USE

- When manually resolving merge conflicts in a `Pipfile` following standard TOML syntax.
- To strictly review the separation of `[packages]` vs `[dev-packages]` in a Python project.
- When migrating legacy `requirements.txt` declarations into a structured `Pipfile`.

## WHEN NOT TO USE

- When actually installing or resolving the dependencies (use the `pipenv` skill to execute the CLI commands).
- For attempting to manually edit the `Pipfile.lock` (which should never be touched by humans or agents directly).
- If the project relies on `pyproject.toml` instead of Pipenv for dependency definitions.

## Common Pitfalls

- **Syntax Errors**: Breaking the TOML syntax in the `Pipfile` during manual edits, causing subsequent `pipenv lock` commands to fail entirely.
- **Manual Lockfile Edits**: Attempting to resolve hash conflicts by manually editing the `Pipfile.lock` JSON, resulting in a corrupted environment.
- **Dependency Co-mingling**: Placing testing libraries (like `pytest`) in the production `[packages]` block instead of `[dev-packages]`, bloating the deployment artifact.

## Core Process

1. **Structure Definition**: Define the `Pipfile` structure including source, packages, and dev-packages.
2. **Locking**: Ensure all dependencies are pinned in `Pipfile.lock` using deterministic hashing.
3. **Manual Edits**: Manually editing the `Pipfile` is allowed but must adhere strictly to standard TOML syntax.

## Core Principles

- **Deterministic Environments**: Rely on `Pipfile.lock` to guarantee exact versions and hashes. Never edit `Pipfile.lock` manually.
- **Group Separation**: Strictly separate production (`[packages]`) and development (`[dev-packages]`) dependencies.
- **TOML Compliance**: Manually editing the `Pipfile` is allowed but must adhere strictly to standard TOML syntax. Prefer CLI commands over manual edits when possible.
- **Security-First**: Utilize `Pipfile.lock`'s stored hashes to prevent supply-chain attacks. Regularly run vulnerability scans.
- **CI/CD Invariance**: Use `--deploy` to ensure `Pipfile.lock` is up-to-date and fails if not. Use `--system` when running in Docker containers.

## What to Avoid

- **Interactive Subshells**: As an automated agent, you MUST NOT run `pipenv shell`.
- **Manual Lockfile Edits**: NEVER manually edit `Pipfile.lock`.
- **Using requirements.txt blindly**: Migrate dependencies to the `Pipfile` structure instead of using legacy formats.

## Related Skills

- **pipenv**:
  You MUST load this skill when using the pipenv CLI to manage environments or dependencies.
- **python**:
  You MUST load this skill when dealing with Python code execution or debugging.
