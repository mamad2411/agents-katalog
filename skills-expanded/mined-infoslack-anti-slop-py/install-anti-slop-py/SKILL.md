---
name: install-anti-slop-py
description: Install and configure the anti-slop-py lint layers (Ruff rules, mypy strict flags, and the vendored Flake8 ASP plugin) in a local Python repository. Use whenever a user asks to add anti-slop rules to a Python project, copy the anti-slop Flake8 plugin, or configure opinionated evidence-based lint rules for Python.
---

# Install anti-slop-py

Install the three anti-slop-py layers into the current repository: ready-made Ruff rules, mypy strict flags, and the bundled Flake8 plugin carrying the custom `ASP` rules. Preserve unrelated work and adapt to the project's package manager and configuration style.

## Choose the mode first

- **Scan (no repo changes).** The user wants findings, an audit, or explicitly asked not to touch the repository. Run the rules straight from this skill's bundled copy and report; write nothing to the target repo:

  ```bash
  uv run --with flake8 flake8 --config <skill-directory>/assets/configs/flake8-scan.ini src tests
  ```

  Complement with the ready-made layers as CLI flags, still with zero repo changes: `uv run ruff check --extend-select ANN401,PGH003,B009,B010 src tests` and, when a full type audit is wanted, `uv run mypy --disallow-any-explicit --disallow-any-generics src`. Drop `ASD`/`ASF` via `--select ASP` when the target has no pydantic/fastapi. Report findings grouped by rule with the suggested fix per group.

- **Install (enforcement).** The user wants the rules wired into the repository so CI and every developer runs them. Confirm this is wanted before changing files, then pick the flavor:
  - **Package (default):** add `anti-slop-py` as a development dependency with the repository's own manager (`uv add --dev anti-slop-py`). The entry points register the `ASP` rules automatically; create or merge a `.flake8` with `select = ASP`, adding `,ASD,ASF` plus `enable-extensions = ASD,ASF` when pydantic/fastapi is a direct dependency. Skip steps 2 and the `[flake8:local-plugins]` part of step 4 below; everything else in the procedure applies.
  - **Vendored (only on explicit request):** the user wants to own and edit the rules locally. Follow the full procedure below. Never combine both flavors in one repo; each finding gets reported twice.

## Procedure

1. Inspect the repository before changing it:
   - Read its agent instructions.
   - Check `git status` and preserve unrelated changes.
   - Identify the package/environment manager (`uv.lock`, `poetry.lock`, `requirements*.txt`, `Pipfile.lock`) and use it consistently.
   - Find existing lint and type configuration: Ruff (`pyproject.toml [tool.ruff]`, `ruff.toml`), mypy (`mypy.ini`, `setup.cfg`, `pyproject.toml [tool.mypy]`), Flake8 (`.flake8`, `setup.cfg`, `tox.ini`).
   - Check whether anti-slop files or `ASP` rules already exist, and never overwrite them without reviewing the diff.

2. Copy the bundled Flake8 plugin. Run from the target repository root:

   ```bash
   python <skill-directory>/scripts/install.py
   ```

   This creates `tools/flake8/anti_slop/`. Pass another relative destination as the first argument when the repository has an established tooling layout. The script refuses to replace an existing destination; use `--force` only after backing up and reviewing what is there.

3. Install current compatible dependencies instead of trusting remembered versions:
   - Query current versions on PyPI (`pip index versions flake8`, or the equivalent for the project's manager).
   - Install `flake8` and `ruff` as development dependencies with the repository's own manager (`uv add --dev`, `poetry add --group dev`, or the project's requirements convention). Add `mypy` too when the project has none.
   - Never replace the package manager or rewrite unrelated dependency ranges.

4. Register the Flake8 local plugin. Flake8 does not read `pyproject.toml`, so merge into `.flake8` (or the existing `setup.cfg`/`tox.ini` Flake8 section), using `<skill-directory>/assets/configs/flake8-example.ini` as the template:

   ```ini
   [flake8]
   select = ASP

   [flake8:local-plugins]
   extension =
       ASP = anti_slop.checker:AntiSlopChecker
   paths =
       ./tools/flake8
   ```

   Keep any existing Flake8 configuration. When the repository already uses Flake8 with other codes, extend `select` instead of replacing it, and adjust `paths` when the plugin was copied elsewhere.

5. Merge the Ruff layer from `<skill-directory>/assets/configs/ruff-anti-slop.toml` into the existing Ruff configuration: `extend-select` the listed codes and add the `banned-api` entries. Keep every existing selection and setting. Drop the `typing.Any` ban when mypy `disallow_any_explicit` gets enabled in step 6, so findings aren't duplicated.

6. Merge the mypy layer from `<skill-directory>/assets/configs/mypy-anti-slop.ini` into the existing mypy configuration. A project with no mypy setup gets one scoped to owned source packages. In large untyped codebases, agree with the user on a gradual scope before enabling `disallow_untyped_defs` globally.

   **Framework groups (opt-in).** Enable a group only when its framework is a **direct** dependency in the package manifest (`pyproject.toml`, requirements), never merely transitive, or when the user explicitly asks:

   - **Pydantic** (`ASD`): add `ASD` to `select` and to `enable-extensions` (the framework groups are off_by_default plugins; `select` alone does not run them). In the vendored flavor, also add the `ASD` extension line to `[flake8:local-plugins]`. Install `flake8-pydantic` as a development dependency and add `PYD` to `select`; merge `assets/configs/mypy-anti-slop-pydantic.ini` (the official Pydantic mypy plugin; append to an existing `plugins` line instead of replacing it).
   - **FastAPI** (`ASF`): add `ASF` to `select` and to `enable-extensions`; in the vendored flavor, also add the `ASF` extension line to `[flake8:local-plugins]`. Merge `assets/configs/ruff-anti-slop-fastapi.toml` (Ruff `FAST` and `ASYNC` groups) into the Ruff configuration.

   When a framework is absent, delete its code from `select`, `enable-extensions`, and (vendored flavor) the extension lines, instead of leaving dead registration. Model and endpoint detection in these groups is syntactic (base names, decorator verbs); report heuristic misses as limitations instead of pretending cross-module inheritance is enforced.

7. Configure exclusions so tooling directories aren't linted as application source: add `tools/flake8/anti_slop`, plus any project-local agent tooling directories, to Ruff's `extend-exclude`, Flake8's `extend-exclude`, and mypy's `exclude`. Never broadly ignore all dot-directories.

8. Run all three checks (Ruff, Flake8, mypy) plus the project's test suite. When findings appear in owned project source, report them, and fix them only when the user asked for migration or cleanup. Never suppress rules, weaken severity, add unjustified `# SAFETY:` comments, or mechanically launder types to make lint pass.

9. Review the final diff and clearly report:
   - copied path,
   - dependency versions installed,
   - configuration changed per layer,
   - checks run and any remaining findings.

## Migration guidance

When replacing an older local copy, compare its rules and diagnostics before overwriting. Keep project-specific rules in their own plugin module. Prefer boundary parsing (Pydantic, dataclasses), `TypedDict`, `Final`, and `TypeGuard`/`TypeIs` functions when resolving findings. The `--anti-slop-allow-typeguards` Flake8 option relaxes ASP002 for schema-free projects; enable it only on explicit request.
