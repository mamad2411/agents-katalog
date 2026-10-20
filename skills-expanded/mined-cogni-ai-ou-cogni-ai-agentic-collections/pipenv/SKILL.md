---
name: pipenv
description: >-
  Manage Python project dependencies, virtual environments, and security using the pipenv CLI.
  This skill MUST be loaded when using pipenv to manage environments or dependencies.
license: MIT
---
# pipenv

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

Use this skill for managing Python project environments and dependencies through the `pipenv` CLI tool.

## WHEN TO USE

- When initializing a new Python project that requires deterministic dependency management.
- To add, update, or remove Python packages while keeping the `Pipfile.lock` strictly synchronized.
- When executing tests or scripts securely within an isolated virtual environment (`pipenv run`).

## WHEN NOT TO USE

- For managing global Python system packages or basic scripting where `pip` or `pipx` is strictly preferred.
- In projects mandated to use `poetry`, `uv`, or raw `requirements.txt` workflows.
- When building Python wheels or distributing packages to PyPI (use `build` or `twine` instead).

## Common Pitfalls

- **Interactive Shell Hangs**: Running `pipenv shell` in an automated agent session, which locks the terminal waiting for human TTY input. (Always use `pipenv run`).
- **Ignoring Lock Failures**: Modifying the `Pipfile` but forgetting to run `pipenv lock`, leading to CI failures due to out-of-sync hashes.
- **Global Pollution**: Using `pip install` while inside the project directory, accidentally modifying the system Python environment instead of the Pipenv virtual environment.

## Core Process

1. **Initialization**: Create a new environment and `Pipfile` if none exists using `pipenv install`.
   **Crucial**: Once an environment is created, you MUST create a `README.md` in the project root detailing how to use the environment
   (e.g., `pipenv install`, `pipenv run <command>`).
2. **Adding Dependencies**: Use `pipenv install <package>` for production or `pipenv install --dev <package>` for development dependencies.
3. **Locking**: Run `pipenv lock` to deterministically pin dependencies into `Pipfile.lock`.
4. **Testing**: Execute tests within the environment using `pipenv run <test-command>` (e.g., `pipenv run pytest`).
5. **Execution**:
   Use `pipenv run <command>` to execute code within the isolated virtual environment.
   As an automated agent, you MUST NOT run `pipenv shell`. `pipenv shell` spawns an interactive subshell environment meant for humans.
   Since you cannot interact with a nested interactive prompt, the terminal simply stalls waiting for human input until `exit` is typed.
   For automated environments, it is always better to prefix the command with `pipenv run`.

## Core Principles

- **Deterministic Environments**: Rely on `Pipfile.lock` to guarantee exact versions and hashes. Never edit `Pipfile.lock` manually.
- **Group Separation**: Strictly separate production (`[packages]`) and development (`[dev-packages]`) dependencies.
- **Security-First**: Utilize `Pipfile.lock`'s stored hashes to prevent supply-chain attacks. Regularly run vulnerability scans.
- **CI/CD Invariance**: Use `--deploy` to ensure `Pipfile.lock` is up-to-date and fails if not. Use `--system` when running in Docker containers.

## Commands / Usage Patterns

- **Install new dependency**: `pipenv install <package>`
- **Install dev dependency**: `pipenv install <package> --dev`
- **Install specific version**: `pipenv install "<package>==<version>"`
- **Update a dependency**: `pipenv update <package>`
- **Generate lockfile**: `pipenv lock`
- **Install from lockfile**: `pipenv sync` (or `pipenv install --deploy` for CI/CD environments)
- **Uninstall a dependency**: `pipenv uninstall <package>`
- **Check for vulnerabilities**: `pipenv check` (Note: Treat this as one layer of security, not a complete supply-chain safeguard).
- **Generate SBOM**: `syft scan Pipfile.lock -o spdx-json > sbom.json` (Requires `syft` dependency; you MUST load the `sbom` skill).
- **List installed packages**: `pipenv graph`
- **Show environment info**: `pipenv --venv`
- **Usage and examples**: `pipenv --help`

## Example Agent Workflow

A typical non-interactive sequence for setting up and verifying an environment:

```bash
# Initialize and install dependencies
pipenv install --dev pytest requests
# Generate a deterministic lockfile
pipenv lock
# Run tests within the virtual environment
pipenv run pytest
```

## Diagnostics and Troubleshooting

- **Lockfile Hash Mismatch**: If `Pipfile.lock out of date` error occurs, run `pipenv lock` to sync the lockfile with recent `Pipfile` changes.
- **Dependency Resolution Failures**: Clear cache with `pipenv lock --clear` or relax constraints inside the `Pipfile`.
- **BackendUnavailable on Editable Installs**: When having parallel install issues, set `PIP_NO_BUILD_ISOLATION=1`.

## What to Avoid

- **Interactive Subshells**: As an automated agent, you MUST NOT run `pipenv shell`. It spawns an interactive subshell environment meant for humans. Since you cannot interact with a nested interactive prompt, the terminal stalls waiting for input. Always prefix commands with `pipenv run` instead.
- **Manual Lockfile Edits**: NEVER manually edit `Pipfile.lock`. Always use `pipenv lock` to regenerate.
- **Using requirements.txt blindly**: Migrate via `pipenv install -r requirements.txt`. If the project requires `requirements.txt` for specific deployment or legacy tooling, keep them in sync instead of abandoning it completely.
- **Deploying without sync**: Do not use `pipenv update` or `pipenv lock` in CI/CD. Use `pipenv install --deploy` to enforce consistency.
- **Avoid Global Installs**: Do NOT use `pip install` outside the `pipenv` environment to avoid dependency drift and contamination.

## Limitations

- Editable installs in parallel can cause race conditions if build isolation is disabled.
- Generating a `Pipfile` automatically creates a virtual environment, which consumes disk space.

## Related Skills

- **pipfile**:
  You MUST load this skill when dealing specifically with Pipfile or Pipfile.lock content.
- **sbom**:
  You MUST load this skill when generating or managing Software Bill of Materials (SBOM).
- **python**:
  You MUST load this skill when dealing with Python code execution, debugging, or log processing.
