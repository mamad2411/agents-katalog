---
name: write-python
description: Python project conventions for this codebase. Use when creating a new Python project, configuring Python tools (ruff, pyright, ty, pytest, bandit, vulture), writing or reviewing pyproject.toml, setting up Nx targets for Python, or asked about Python tooling setup, uv, or the language:python tag. Covers the project.json pattern, pyproject.toml structure, targetDefaults, tool execution via uv run, and ty pre-1.0 configuration rules.
license: MIT
---

# Write Python

All Python projects inherit configuration from the root `pyproject.toml` and Nx `targetDefaults`. Use `uv run` (never `uvx`) for reproducible tool invocations pinned in `uv.lock`.

Every Python project is a member of the uv workspace declared in the root `pyproject.toml`, sharing one `uv.lock` and one `.venv`, both at the repository root.

## Tool Targets

Seven Python tool targets are defined as codebase-wide `targetDefaults` in `nx.json`:

| Target | Tool | Purpose |
| ------ | ---- | ------- |
| `ruff-format` | ruff | Format Python source |
| `ruff-lint` | ruff | Lint Python source |
| `pyright` | pyright | Primary type checker (strict mode) |
| `pytest` | pytest | Run tests (unit/integration/coverage) |
| `vulture` | vulture | Dead code detection |
| `ty` | ty | Supplementary type checker (Astral, pre-1.0) |
| `bandit` | bandit | Security linter (CI `scan-security` only) |

## Project Tags

Every Python project must declare the `language:python` tag in `project.json`. This enables the correct composite target overrides (Python sub-targets instead of TypeScript ones).

```json
{
  "tags": ["language:python", "scope:<name>", "type:application"]
}
```

## project.json Pattern

Declare every sub-target as `{}` so Nx applies the `targetDefaults`. Override composite targets to compose the Python sub-targets:

```json
{
  "tags": ["language:python", "scope:my-app", "type:application"],
  "targets": {
    "format": {
      "configurations": {
        "check": { "commands": ["nx run {projectName}:ruff-format:check"], "parallel": true },
        "write": { "commands": ["nx run {projectName}:ruff-format:write"], "parallel": false }
      }
    },
    "lint": {
      "configurations": {
        "check": { "commands": ["nx run {projectName}:ruff-lint:check"], "parallel": true },
        "write": { "commands": ["nx run {projectName}:ruff-lint:write"], "parallel": false }
      }
    },
    "typecheck": {
      "executor": "nx:run-commands",
      "options": {
        "commands": ["nx run {projectName}:pyright", "nx run {projectName}:ty"],
        "parallel": true
      }
    },
    "test": {
      "executor": "nx:run-commands",
      "options": { "commands": ["nx run {projectName}:pytest"] },
      "configurations": {
        "unit": { "commands": ["nx run {projectName}:pytest:unit"] },
        "integration": { "commands": ["nx run {projectName}:pytest:integration"] },
        "coverage": { "commands": ["nx run {projectName}:pytest:coverage"] }
      }
    },
    "bandit": {},
    "pytest": {},
    "pyright": {},
    "ruff-format": {},
    "ruff-lint": {},
    "ty": {},
    "vulture": {}
  }
}
```

> Each sub-target declared as `{}` tells Nx "this project has this target — use the codebase default."

## pyproject.toml Pattern

```toml
[project]
name = "my-python-app"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [...]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src"]
reproducible = true

# Project-specific overrides only — base config inherited from root pyproject.toml
[tool.ruff]
exclude = ["notebooks/**", ".vulture_whitelist.py"]

[tool.pyright]
# The shared uv workspace venv at the repository root
venvPath = "../.."
venv = ".venv"
reportMissingModuleSource = "none"

# ty: keep project-level until ty reaches 1.0 (do NOT add to root pyproject.toml)
[tool.ty.environment]
python-version = "3.11"

[tool.ty.analysis]
allowed-unresolved-imports = ["my_external_package.**"]

[tool.bandit]
exclude_dirs = ["testing", "output", "notebooks"]
skips = ["B101"]
```

## Root pyproject.toml

The root `pyproject.toml` is the single Python configuration file: it declares the uv workspace, the dev tools the workspace-root Nx targets run (sqlfluff, vulture, yamllint), and the shared `[tool.*]` settings projects pick up via `[tool.ruff] extend`.

```toml
[tool.uv.workspace]
members = ["applications/affirmations"]

[dependency-groups]
dev = ["sqlfluff>=3.0", "vulture>=2.14", "yamllint>=1.35"]

[tool.ruff]
target-version = "py314"
line-length = 100
```

It deliberately has **no `[project]` table**. A virtual workspace root makes `uv sync` install every member and its dev group into the shared `.venv`; adding `[project]` makes uv install only the root package and skip the members entirely.

Note that only ruff inherits: pyright and pytest read solely the `pyproject.toml` of the directory they run in, so their settings must be repeated per project.

## uv Workspace Rules

- **Members are listed explicitly.** A glob such as `applications/*` fails on the TypeScript projects, which have no `pyproject.toml`.
- **Sync from the repository root.** `uv sync --project <member>` prunes the other members' tools out of the shared `.venv`; a bare `uv sync` installs them all.
- **`uv run` works from any member directory.** It resolves the workspace root and uses the shared `.venv` without pruning, so Nx targets keep their `cwd: {projectRoot}`.
- **One resolution for all members.** Dependency conflicts between Python projects have to be settled, not isolated.

## ty Configuration Note

ty is pre-1.0. Keep `[tool.ty]` config **project-level** (in the project's `pyproject.toml`, not root) until ty stabilizes.

## Tool Execution

All tool invocations use `uv run` (not `uvx`) for reproducible versions pinned in `uv.lock`:

```bash
uv run ruff format .
uv run ruff check .
uv run pyright src/
uv run pytest
uv run ty check src/
uv run bandit -c pyproject.toml -r src/
uv run vulture src/ .vulture_whitelist.py --min-confidence 80
```

## Adding a New Python Project

1. Create `project.json` with `language:python` tag and all sub-targets declared as `{}`
2. Create `pyproject.toml` using the pattern above
3. Add the project path to `members` in the root `pyproject.toml`
4. Run `uv sync` from the repository root to update the shared `uv.lock` and `.venv`
5. Add `ty` and `bandit` as dev dependencies: `uv add --dev --package <project> ty 'bandit[toml]'`
6. Declare the leaf targets it needs (`ruff-format`, `ruff-lint`, `pyright`, `ty`, `pytest`, `vulture`) plus `lint-code` and `test-code` in `project.json`
7. Verify: `nx run <project>:lint-code`
