---
name: python-uv-development
description: Implement and troubleshoot Python projects with supported runtimes, isolated environments, uv and repository-specific checks.
---

# Python and uv

- Read repository instructions, manifests, lockfiles and existing commands.
  Preserve the project's Python range and package manager.
- Never replace Ubuntu's system Python, install into its environment, or use
  `--break-system-packages`. Select a compatible user-managed runtime explicitly.
- Keep environments project-local. For uv projects use intentional `uv add`,
  `uv sync` and `uv run` changes; do not create one environment for every repo.
- Change manifests and generated lockfiles through the correct tooling.
  Personal tools must not override a project's pinned dependency versions.
- Run focused formatting, lint, type and test checks for the changed behavior.
  Do not hide failures with broad catches or silent defaults.
- Distinguish runtime, import, package and native-library errors. If a
  particular runtime or wheel is incomplete, repair that installation/cache
  rather than deleting all environment or user configuration data.

For GPU Python also use `nvidia-cuda-workflows`. Framework runtime wheels
and a native CUDA development toolkit are not interchangeable.
